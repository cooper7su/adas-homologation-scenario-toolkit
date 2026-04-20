#!/usr/bin/env python3
"""Extract basic metadata from OpenSCENARIO XML files."""

from __future__ import annotations

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


FIELDS = [
    "file_name",
    "file_path",
    "parameter_count",
    "parameters",
    "storyboard_names",
    "entity_names",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract ParameterDeclarations, storyboard names, and entity names from .xosc files."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="OpenSCENARIO file or directory containing .xosc files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/xosc_parameter_summary.csv"),
        help="Output CSV path. Default: reports/xosc_parameter_summary.csv",
    )
    return parser.parse_args()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def find_xosc_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() in {".xosc", ".xml"} else []
    if input_path.is_dir():
        return sorted(
            path
            for path in input_path.rglob("*")
            if path.is_file() and path.suffix.lower() in {".xosc", ".xml"}
        )
    return []


def format_parameter(elem: ET.Element) -> str:
    name = elem.attrib.get("name", "")
    param_type = elem.attrib.get("parameterType", "")
    value = elem.attrib.get("value", "")
    if param_type or value:
        return f"{name}({param_type}={value})"
    return name


def unique_join(values: list[str]) -> str:
    cleaned = [value for value in values if value]
    return "; ".join(dict.fromkeys(cleaned))


def extract_file(path: Path, root_dir: Path | None = None) -> dict[str, str]:
    notes: list[str] = []
    parameters: list[str] = []
    storyboard_names: list[str] = []
    entity_names: list[str] = []

    try:
        tree = ET.parse(path)
        root = tree.getroot()
        for elem in root.iter():
            tag = local_name(elem.tag)
            if tag == "ParameterDeclaration":
                formatted = format_parameter(elem)
                if formatted:
                    parameters.append(formatted)
            elif tag in {"Storyboard", "Story", "Act", "ManeuverGroup", "Maneuver", "Event"}:
                name = elem.attrib.get("name")
                if name:
                    storyboard_names.append(f"{tag}:{name}")
            elif tag in {"ScenarioObject", "EntitySelection"}:
                name = elem.attrib.get("name")
                if name:
                    entity_names.append(name)
    except ET.ParseError as exc:
        notes.append(f"XML parse error: {exc}")
    except OSError as exc:
        notes.append(f"Read error: {exc}")

    try:
        file_path = path.relative_to(root_dir).as_posix() if root_dir else path.as_posix()
    except ValueError:
        file_path = path.as_posix()

    return {
        "file_name": path.name,
        "file_path": file_path,
        "parameter_count": str(len(parameters)),
        "parameters": unique_join(parameters),
        "storyboard_names": unique_join(storyboard_names),
        "entity_names": unique_join(entity_names),
        "notes": unique_join(notes),
    }


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    input_path = args.input.resolve()

    if not input_path.exists():
        print(f"ERROR: input path does not exist: {input_path}", file=sys.stderr)
        return 2

    root_dir = input_path if input_path.is_dir() else input_path.parent
    files = find_xosc_files(input_path)
    rows = [extract_file(path, root_dir) for path in files]
    write_csv(rows, args.output)

    print(f"Processed {len(rows)} OpenSCENARIO/XML file(s).")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
