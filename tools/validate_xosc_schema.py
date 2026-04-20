#!/usr/bin/env python3
"""Validate OpenSCENARIO/XML files for XML well-formedness and optional XSD.

The script always performs a basic XML parse. If --schema is provided and lxml
is installed, it also performs XSD validation. The toolkit does not redistribute
ASAM schemas; users must provide schema files from an authorized source.
"""

from __future__ import annotations

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


FIELDS = [
    "file_name",
    "file_path",
    "validation_mode",
    "well_formed",
    "schema_valid",
    "status",
    "message",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate .xosc/.xml files for XML well-formedness and optional XSD schema compliance."
    )
    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="OpenSCENARIO/XML file or directory containing .xosc/.xml files.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        help="Optional XSD schema path. Requires lxml. ASAM schemas are not included in this repository.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Output directory. Default: reports",
    )
    return parser.parse_args()


def find_xml_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() in {".xosc", ".xml"} else []
    if input_path.is_dir():
        return sorted(
            path
            for path in input_path.rglob("*")
            if path.is_file() and path.suffix.lower() in {".xosc", ".xml"}
        )
    return []


def load_lxml_schema(schema_path: Path) -> tuple[Any | None, str | None]:
    try:
        from lxml import etree  # type: ignore
    except ImportError:
        return None, "lxml is not installed; install lxml to enable XSD validation."

    try:
        schema_doc = etree.parse(str(schema_path))
        return etree.XMLSchema(schema_doc), None
    except Exception as exc:  # lxml exposes several schema-specific exceptions.
        return None, f"Unable to load schema: {exc}"


def validate_well_formed(path: Path) -> tuple[bool, str]:
    try:
        ET.parse(path)
        return True, ""
    except ET.ParseError as exc:
        return False, f"XML parse error: {exc}"
    except OSError as exc:
        return False, f"Read error: {exc}"


def validate_schema(path: Path, schema: Any) -> tuple[bool, str]:
    from lxml import etree  # type: ignore

    try:
        doc = etree.parse(str(path))
        valid = bool(schema.validate(doc))
        if valid:
            return True, ""
        return False, "; ".join(str(error) for error in schema.error_log)
    except Exception as exc:
        return False, f"Schema validation error: {exc}"


def build_row(
    path: Path,
    root_dir: Path,
    schema: Any | None,
    schema_error: str | None,
) -> dict[str, str]:
    try:
        relative_path = path.relative_to(root_dir).as_posix()
    except ValueError:
        relative_path = path.as_posix()

    well_formed, xml_message = validate_well_formed(path)
    validation_mode = "well_formed"
    schema_valid = "not_run"
    message = xml_message

    if schema_error:
        validation_mode = "well_formed_only_schema_unavailable"
        message = xml_message or schema_error
    elif schema is not None and well_formed:
        validation_mode = "well_formed_and_xsd"
        valid, schema_message = validate_schema(path, schema)
        schema_valid = "true" if valid else "false"
        message = schema_message

    if not well_formed:
        status = "fail"
    elif schema_valid == "false":
        status = "fail"
    elif schema_error:
        status = "partial"
    else:
        status = "pass"

    return {
        "file_name": path.name,
        "file_path": relative_path,
        "validation_mode": validation_mode,
        "well_formed": "true" if well_formed else "false",
        "schema_valid": schema_valid,
        "status": status,
        "message": message,
    }


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], output_path: Path) -> None:
    pass_count = sum(1 for row in rows if row["status"] == "pass")
    fail_count = sum(1 for row in rows if row["status"] == "fail")
    partial_count = sum(1 for row in rows if row["status"] == "partial")

    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("# XOSC Validation Report\n\n")
        handle.write(f"- Total files: {len(rows)}\n")
        handle.write(f"- Passed: {pass_count}\n")
        handle.write(f"- Failed: {fail_count}\n")
        handle.write(f"- Partial: {partial_count}\n\n")
        handle.write("| file_path | validation_mode | well_formed | schema_valid | status | message |\n")
        handle.write("| --- | --- | --- | --- | --- | --- |\n")
        for row in rows:
            safe = {key: str(value).replace("|", "\\|") for key, value in row.items()}
            handle.write(
                "| {file_path} | {validation_mode} | {well_formed} | {schema_valid} | {status} | {message} |\n".format(
                    **safe
                )
            )


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()

    if not input_path.exists():
        print(f"ERROR: input path does not exist: {input_path}", file=sys.stderr)
        return 2

    schema = None
    schema_error = None
    if args.schema:
        schema_path = args.schema.resolve()
        if not schema_path.exists():
            print(f"ERROR: schema path does not exist: {schema_path}", file=sys.stderr)
            return 2
        schema, schema_error = load_lxml_schema(schema_path)

    root_dir = input_path if input_path.is_dir() else input_path.parent
    files = find_xml_files(input_path)
    rows = [build_row(path, root_dir, schema, schema_error) for path in files]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "xosc_validation_report.csv"
    md_path = args.output_dir / "xosc_validation_report.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    fail_count = sum(1 for row in rows if row["status"] == "fail")
    partial_count = sum(1 for row in rows if row["status"] == "partial")
    print(f"Validated {len(rows)} file(s).")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    if partial_count:
        print(f"Partial validations: {partial_count}")
    return 1 if fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
