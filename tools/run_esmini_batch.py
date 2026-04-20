#!/usr/bin/env python3
"""Create a dry-run batch execution plan for esmini.

The current implementation generates command lines and log folder structure.
It intentionally avoids assuming that esmini is installed.
"""

from __future__ import annotations

import argparse
import csv
import shlex
import sys
from datetime import datetime
from pathlib import Path


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
        default=True,
        help="Generate commands without executing them. This is the current default.",
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


def build_command(esmini_path: str, scenario_path: str, log_dir: Path) -> str:
    return quote_command(
        [
            esmini_path,
            "--osc",
            scenario_path,
            "--headless",
            "--record",
            (log_dir / "record.dat").as_posix(),
        ]
    )


def write_run_plan(
    rows: list[dict[str, str]],
    commands: list[dict[str, str]],
    report_path: Path,
    dry_run: bool,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("# esmini Batch Run Plan\n\n")
        handle.write(f"Generated at: {datetime.now().isoformat(timespec='seconds')}\n\n")
        handle.write(f"Mode: {'dry-run' if dry_run else 'planned execution'}\n\n")
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
        handle.write("- This script currently creates a dry-run plan and log directories only.\n")
        handle.write("- Verify the esmini executable, OpenSCENARIO version, catalogs, and OpenDRIVE references before execution.\n")
        handle.write("- Keep upstream scenario licenses and attribution with any local scenario checkout.\n")


def main() -> int:
    args = parse_args()
    input_path = args.input

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
        command = build_command(args.esmini_path, row["file_path"], log_dir)
        commands.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": row["scenario_name"],
                "scenario_path": row["file_path"],
                "log_dir": log_dir.as_posix(),
                "command": command,
            }
        )

    write_run_plan(rows, commands, args.report, args.dry_run)

    print(f"Prepared {len(commands)} command(s).")
    print(f"Wrote {args.report}")
    print(f"Created log directory root: {args.output_log_dir}")
    if not args.dry_run:
        print("NOTE: execution is not implemented in this minimal version; only the plan was generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
