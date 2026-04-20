#!/usr/bin/env python3
"""Merge scenario metadata, execution results, and issue logs into summaries."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


OUTPUT_FIELDS = [
    "scenario_id",
    "scenario_name",
    "possible_protocol",
    "execution_status",
    "pass_fail",
    "measured_result",
    "issue_count",
    "open_issue_count",
    "closure_status",
    "remarks",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export scenario result summaries.")
    parser.add_argument(
        "--scenario-index",
        type=Path,
        default=Path("reports/scenario_index.csv"),
        help="Scenario index or scenario list CSV. Default: reports/scenario_index.csv",
    )
    parser.add_argument(
        "--results",
        type=Path,
        required=True,
        help="Execution result CSV.",
    )
    parser.add_argument(
        "--issues",
        type=Path,
        help="Issue tracking CSV. Optional.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Output directory. Default: reports",
    )
    return parser.parse_args()


def read_csv(path: Path, required: bool = True) -> list[dict[str, str]]:
    if not path:
        return []
    if not path.exists():
        if required:
            raise FileNotFoundError(f"CSV not found: {path}")
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_status(value: str) -> str:
    return (value or "").strip().lower()


def is_open_issue(row: dict[str, str]) -> bool:
    status = normalize_status(row.get("status", ""))
    return status not in {"closed", "verified", "rejected", "duplicate", "won't fix", "wont fix"}


def scenario_key(row: dict[str, str]) -> str:
    return (
        row.get("scenario_id")
        or row.get("file_name")
        or row.get("scenario_name")
        or row.get("file_path")
        or ""
    )


def build_summary(
    scenario_rows: list[dict[str, str]],
    result_rows: list[dict[str, str]],
    issue_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    scenarios = {scenario_key(row): row for row in scenario_rows if scenario_key(row)}
    issues_by_scenario: dict[str, list[dict[str, str]]] = defaultdict(list)
    for issue in issue_rows:
        key = issue.get("scenario_id") or issue.get("linked_scenario_id") or ""
        if key:
            issues_by_scenario[key].append(issue)

    summaries: list[dict[str, str]] = []
    for result in result_rows:
        key = scenario_key(result)
        scenario = scenarios.get(key, {})
        linked_issues = issues_by_scenario.get(key, [])
        open_count = sum(1 for issue in linked_issues if is_open_issue(issue))
        issue_count = len(linked_issues)

        if issue_count == 0:
            closure_status = "no linked issue"
        elif open_count == 0:
            closure_status = "closed"
        else:
            closure_status = "open"

        summaries.append(
            {
                "scenario_id": key,
                "scenario_name": result.get("scenario_name")
                or scenario.get("scenario_name")
                or scenario.get("file_name")
                or "",
                "possible_protocol": scenario.get("possible_protocol")
                or result.get("possible_protocol")
                or "",
                "execution_status": result.get("execution_status") or result.get("status") or "",
                "pass_fail": result.get("pass_fail") or result.get("verdict") or "",
                "measured_result": result.get("measured_result") or result.get("measurement") or "",
                "issue_count": str(issue_count),
                "open_issue_count": str(open_count),
                "closure_status": closure_status,
                "remarks": result.get("remarks") or result.get("tester_notes") or "",
            }
        )

    return summaries


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], output_path: Path) -> None:
    total = len(rows)
    passed = sum(1 for row in rows if normalize_status(row.get("pass_fail", "")) == "pass")
    failed = sum(1 for row in rows if normalize_status(row.get("pass_fail", "")) == "fail")
    open_issues = sum(int(row.get("open_issue_count", "0") or 0) for row in rows)

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("# Result Summary\n\n")
        handle.write(f"- Total scenarios with results: {total}\n")
        handle.write(f"- Passed: {passed}\n")
        handle.write(f"- Failed: {failed}\n")
        handle.write(f"- Open linked issues: {open_issues}\n\n")
        handle.write(
            "| scenario_id | scenario_name | execution_status | pass_fail | "
            "issue_count | open_issue_count | closure_status |\n"
        )
        handle.write("| --- | --- | --- | --- | --- | --- | --- |\n")
        for row in rows:
            safe = {key: str(value).replace("|", "\\|") for key, value in row.items()}
            handle.write(
                "| {scenario_id} | {scenario_name} | {execution_status} | {pass_fail} | "
                "{issue_count} | {open_issue_count} | {closure_status} |\n".format(**safe)
            )


def main() -> int:
    args = parse_args()
    try:
        scenarios = read_csv(args.scenario_index, required=True)
        results = read_csv(args.results, required=True)
        issues = read_csv(args.issues, required=False) if args.issues else []
    except (FileNotFoundError, OSError, csv.Error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = build_summary(scenarios, results, issues)
    csv_path = args.output_dir / "result_summary.csv"
    md_path = args.output_dir / "result_summary.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    print(f"Merged {len(rows)} result row(s).")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
