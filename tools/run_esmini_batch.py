#!/usr/bin/env python3
"""Create a batch execution plan for esmini and optionally execute it.

Dry-run is the default. Real execution requires --execute and a resolvable
--esmini-path.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
import shlex
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SUMMARY_FIELDS = [
    "scenario_id",
    "scenario_name",
    "scenario_path",
    "log_dir",
    "return_code",
    "status",
    "stdout_log",
    "stderr_log",
    "command",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an esmini batch run plan.")
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Scenario list CSV/TXT file or directory containing .xosc files.",
    )
    parser.add_argument(
        "--esmini-path",
        default="esmini",
        help="Path to esmini executable. Default: esmini",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate commands without executing them. This is the default unless --execute is provided.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute planned esmini commands. Requires a resolvable --esmini-path.",
    )
    parser.add_argument(
        "--output-log-dir",
        type=Path,
        default=Path("logs"),
        help="Directory for planned log folders. Default: logs",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/run_plan.md"),
        help="Run plan Markdown output. Default: reports/run_plan.md",
    )
    parser.add_argument(
        "--execution-summary",
        type=Path,
        default=Path("reports/esmini_execution_summary.csv"),
        help="Execution summary CSV output when --execute is used. Default: reports/esmini_execution_summary.csv",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Per-scenario execution timeout in seconds when --execute is used. Default: 300",
    )
    return parser.parse_args()


def read_scenario_rows(input_path: Path) -> list[dict[str, str]]:
    if input_path.is_dir():
        return [
            {
                "scenario_id": path.stem,
                "scenario_name": path.stem,
                "file_path": path.as_posix(),
            }
            for path in sorted(input_path.rglob("*.xosc"))
        ]

    if not input_path.is_file():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    if input_path.suffix.lower() == ".csv":
        with input_path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = []
            for index, row in enumerate(reader, start=1):
                file_path = (
                    row.get("file_path")
                    or row.get("scenario_path")
                    or row.get("path")
                    or row.get("xosc_path")
                    or ""
                )
                if not file_path:
                    continue
                rows.append(
                    {
                        "scenario_id": row.get("scenario_id") or f"row-{index}",
                        "scenario_name": row.get("scenario_name") or Path(file_path).stem,
                        "file_path": file_path,
                    }
                )
            return rows

    rows = []
    with input_path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle, start=1):
            value = line.strip()
            if not value or value.startswith("#"):
                continue
            rows.append(
                {
                    "scenario_id": f"line-{index}",
                    "scenario_name": Path(value).stem,
                    "file_path": value,
                }
            )
    return rows


def quote_command(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def build_command_parts(esmini_path: str, scenario_path: str, log_dir: Path) -> list[str]:
    return [
        esmini_path,
        "--osc",
        scenario_path,
        "--headless",
        "--record",
        (log_dir / "record.dat").as_posix(),
    ]


def resolve_executable(esmini_path: str) -> str | None:
    candidate = Path(esmini_path).expanduser()
    if candidate.exists() and candidate.is_file() and os.access(candidate, os.X_OK):
        return candidate.as_posix()
    return shutil.which(esmini_path)


def write_run_plan(
    rows: list[dict[str, str]],
    commands: list[dict[str, str]],
    report_path: Path,
    execute: bool,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("# esmini Batch Run Plan\n\n")
        handle.write(f"Generated at: {datetime.now().isoformat(timespec='seconds')}\n\n")
        handle.write(f"Mode: {'execute' if execute else 'dry-run'}\n\n")
        handle.write(f"Scenario count: {len(rows)}\n\n")
        handle.write("| scenario_id | scenario_name | scenario_path | log_dir | command |\n")
        handle.write("| --- | --- | --- | --- | --- |\n")
        for command in commands:
            safe = {
                key: str(value).replace("|", "\\|")
                for key, value in command.items()
            }
            handle.write(
                "| {scenario_id} | {scenario_name} | {scenario_path} | {log_dir} | `{command}` |\n".format(
                    **safe
                )
            )
        handle.write("\n## Notes\n\n")
        handle.write("- Dry-run is the default mode. Use `--execute` only after validating the simulator setup.\n")
        handle.write("- Verify the esmini executable, OpenSCENARIO version, catalogs, and OpenDRIVE references before execution.\n")
        handle.write("- Keep upstream scenario licenses and attribution with any local scenario checkout.\n")


def execute_commands(
    commands: list[dict[str, str]],
    executable_path: str,
    timeout: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for command in commands:
        log_dir = Path(command["log_dir"])
        stdout_log = log_dir / "stdout.log"
        stderr_log = log_dir / "stderr.log"
        parts = build_command_parts(executable_path, command["scenario_path"], log_dir)
        command_text = quote_command(parts)
        return_code = -1
        status = "not_run"

        try:
            completed = subprocess.run(
                parts,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return_code = completed.returncode
            status = "pass" if completed.returncode == 0 else "fail"
            stdout_log.write_text(completed.stdout or "", encoding="utf-8")
            stderr_log.write_text(completed.stderr or "", encoding="utf-8")
        except subprocess.TimeoutExpired as exc:
            status = "timeout"
            stdout_log.write_text(exc.stdout or "", encoding="utf-8")
            stderr_log.write_text(exc.stderr or f"Timed out after {timeout} seconds.", encoding="utf-8")
        except OSError as exc:
            status = "error"
            stderr_log.write_text(str(exc), encoding="utf-8")

        rows.append(
            {
                "scenario_id": command["scenario_id"],
                "scenario_name": command["scenario_name"],
                "scenario_path": command["scenario_path"],
                "log_dir": command["log_dir"],
                "return_code": str(return_code),
                "status": status,
                "stdout_log": stdout_log.as_posix(),
                "stderr_log": stderr_log.as_posix(),
                "command": command_text,
            }
        )

    return rows


def write_execution_summary(rows: list[dict[str, str]], csv_path: Path) -> Path:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SUMMARY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    md_path = csv_path.with_suffix(".md")
    pass_count = sum(1 for row in rows if row["status"] == "pass")
    fail_count = sum(1 for row in rows if row["status"] in {"fail", "timeout", "error"})
    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# esmini Execution Summary\n\n")
        handle.write(f"- Total scenarios: {len(rows)}\n")
        handle.write(f"- Passed commands: {pass_count}\n")
        handle.write(f"- Failed/timeout/error commands: {fail_count}\n\n")
        handle.write("| scenario_id | scenario_name | return_code | status | log_dir |\n")
        handle.write("| --- | --- | --- | --- | --- |\n")
        for row in rows:
            safe = {key: str(value).replace("|", "\\|") for key, value in row.items()}
            handle.write(
                "| {scenario_id} | {scenario_name} | {return_code} | {status} | {log_dir} |\n".format(
                    **safe
                )
            )
    return md_path


def main() -> int:
    args = parse_args()
    input_path = args.input

    if args.dry_run and args.execute:
        print("ERROR: choose either --dry-run or --execute, not both.", file=sys.stderr)
        return 2

    execute = args.execute

    try:
        rows = read_scenario_rows(input_path)
    except (FileNotFoundError, OSError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    args.output_log_dir.mkdir(parents=True, exist_ok=True)
    commands: list[dict[str, str]] = []

    for row in rows:
        scenario_id = row["scenario_id"] or Path(row["file_path"]).stem
        log_dir = args.output_log_dir / scenario_id
        log_dir.mkdir(parents=True, exist_ok=True)
        command_parts = build_command_parts(args.esmini_path, row["file_path"], log_dir)
        command = quote_command(command_parts)
        commands.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": row["scenario_name"],
                "scenario_path": row["file_path"],
                "log_dir": log_dir.as_posix(),
                "command": command,
            }
        )

    write_run_plan(rows, commands, args.report, execute)

    print(f"Prepared {len(commands)} command(s).")
    print(f"Wrote {args.report}")
    print(f"Created log directory root: {args.output_log_dir}")

    if execute:
        executable_path = resolve_executable(args.esmini_path)
        if not executable_path:
            print(f"ERROR: esmini executable not found: {args.esmini_path}", file=sys.stderr)
            return 2
        execution_rows = execute_commands(commands, executable_path, args.timeout)
        summary_md = write_execution_summary(execution_rows, args.execution_summary)
        print(f"Wrote {args.execution_summary}")
        print(f"Wrote {summary_md}")
        if any(row["status"] != "pass" for row in execution_rows):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
