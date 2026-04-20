#!/usr/bin/env python3
"""Build a lightweight scenario index from scenario-like files.

The script scans a directory for OpenSCENARIO XML, generic XML, JSON, and YAML
files. It does not validate scenario correctness. It extracts enough metadata
to support review, catalog building, and execution planning.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_EXTENSIONS = {".xosc", ".xml", ".json", ".yaml", ".yml"}
DEFAULT_FIELDS = [
    "scenario_id",
    "file_name",
    "file_path",
    "scenario_name",
    "scenario_type",
    "source_project",
    "possible_protocol",
    "detected_parameters",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan scenario-like files and generate CSV/Markdown indexes."
    )
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Directory containing scenario files or external scenario checkout.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Directory for generated reports. Default: reports",
    )
    return parser.parse_args()


def local_name(tag: str) -> str:
    """Return XML local name without namespace."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def safe_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def infer_source_project(path: Path) -> str:
    lower_parts = [part.lower() for part in path.parts]
    joined = "/".join(lower_parts)
    if "sl-3-1-osc-alks-scenarios" in joined or "openmsl" in joined:
        return "openMSL/sl-3-1-osc-alks-scenarios"
    if "osc-ncap-scenarios" in joined or "vectorgrp" in joined:
        return "vectorgrp/OSC-NCAP-scenarios"
    if "beamng_ncap_tests" in joined or "beamng" in joined:
        return "BeamNG/BeamNG_NCAP_Tests"
    if "esmini" in joined:
        return "esmini/esmini"
    return "local_or_unknown"


def infer_possible_protocol(path: Path, text: str = "") -> str:
    probe = f"{path.as_posix()} {text}".lower()
    matches: list[str] = []
    if "ncap" in probe or "euroncap" in probe or "euro ncap" in probe:
        matches.append("NCAP")
    if "alks" in probe or "r157" in probe or "un r157" in probe:
        matches.append("ALKS / UNECE R157 candidate")
    if "aeb" in probe:
        matches.append("AEB candidate")
    if "lss" in probe or "lane support" in probe:
        matches.append("LSS candidate")
    return "; ".join(dict.fromkeys(matches)) if matches else "unknown"


def scenario_id_from_path(path: Path) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", path.stem).strip("-")
    return cleaned.upper() if cleaned else "UNKNOWN"


def collect_xml_metadata(path: Path) -> dict[str, str]:
    notes: list[str] = []
    scenario_name = ""
    scenario_type = "xml"
    detected_parameters: list[str] = []
    text_probe = ""

    try:
        tree = ET.parse(path)
        root = tree.getroot()
        root_name = local_name(root.tag)
        scenario_type = "OpenSCENARIO" if root_name == "OpenSCENARIO" else root_name

        for elem in root.iter():
            name = local_name(elem.tag)
            if name == "FileHeader":
                scenario_name = (
                    elem.attrib.get("description")
                    or elem.attrib.get("revMajor")
                    or scenario_name
                )
            elif name in {"Story", "Storyboard", "Act"} and not scenario_name:
                scenario_name = elem.attrib.get("name", "")
            elif name == "ParameterDeclaration":
                param_name = elem.attrib.get("name")
                if param_name:
                    detected_parameters.append(param_name)

        text_probe = " ".join([scenario_name, " ".join(detected_parameters)])
    except ET.ParseError as exc:
        notes.append(f"XML parse error: {exc}")
    except OSError as exc:
        notes.append(f"Read error: {exc}")

    return {
        "scenario_name": scenario_name or path.stem,
        "scenario_type": scenario_type,
        "detected_parameters": "; ".join(detected_parameters),
        "text_probe": text_probe,
        "notes": "; ".join(notes),
    }


def flatten_json_keys(data: Any, prefix: str = "") -> Iterable[str]:
    if isinstance(data, dict):
        for key, value in data.items():
            next_key = f"{prefix}.{key}" if prefix else str(key)
            yield next_key
            yield from flatten_json_keys(value, next_key)
    elif isinstance(data, list):
        for index, value in enumerate(data[:10]):
            yield from flatten_json_keys(value, f"{prefix}[{index}]")


def collect_json_metadata(path: Path) -> dict[str, str]:
    notes: list[str] = []
    scenario_name = path.stem
    detected_parameters: list[str] = []
    text_probe = ""

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, dict):
            scenario_name = safe_text(
                data.get("scenario_name")
                or data.get("name")
                or data.get("scenarioId")
                or scenario_name
            )
        keys = list(dict.fromkeys(flatten_json_keys(data)))[:30]
        detected_parameters = keys
        text_probe = " ".join([scenario_name, " ".join(keys)])
    except json.JSONDecodeError as exc:
        notes.append(f"JSON parse error: {exc}")
    except OSError as exc:
        notes.append(f"Read error: {exc}")

    return {
        "scenario_name": scenario_name,
        "scenario_type": "json",
        "detected_parameters": "; ".join(detected_parameters),
        "text_probe": text_probe,
        "notes": "; ".join(notes),
    }


def collect_yaml_metadata(path: Path) -> dict[str, str]:
    notes: list[str] = []
    scenario_name = path.stem
    detected_parameters: list[str] = []
    text_probe = ""

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:", line)
            if match:
                detected_parameters.append(match.group(1))
        name_match = re.search(r"^\s*(scenario_name|name)\s*:\s*(.+)$", text, re.M)
        if name_match:
            scenario_name = name_match.group(2).strip().strip("'\"")
        detected_parameters = list(dict.fromkeys(detected_parameters))[:30]
        text_probe = " ".join([scenario_name, " ".join(detected_parameters), text[:500]])
    except OSError as exc:
        notes.append(f"Read error: {exc}")

    return {
        "scenario_name": scenario_name,
        "scenario_type": "yaml",
        "detected_parameters": "; ".join(detected_parameters),
        "text_probe": text_probe,
        "notes": "; ".join(notes),
    }


def collect_metadata(path: Path, root_dir: Path) -> dict[str, str]:
    if path.suffix.lower() in {".xosc", ".xml"}:
        metadata = collect_xml_metadata(path)
    elif path.suffix.lower() == ".json":
        metadata = collect_json_metadata(path)
    else:
        metadata = collect_yaml_metadata(path)

    try:
        relative_path = path.relative_to(root_dir)
    except ValueError:
        relative_path = path

    return {
        "scenario_id": scenario_id_from_path(path),
        "file_name": path.name,
        "file_path": relative_path.as_posix(),
        "scenario_name": safe_text(metadata["scenario_name"]),
        "scenario_type": metadata["scenario_type"],
        "source_project": infer_source_project(path),
        "possible_protocol": infer_possible_protocol(path, metadata.get("text_probe", "")),
        "detected_parameters": metadata["detected_parameters"],
        "notes": metadata["notes"],
    }


def find_scenario_files(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=DEFAULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]], output_path: Path) -> None:
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("# Scenario Index\n\n")
        handle.write(f"Total indexed files: {len(rows)}\n\n")
        handle.write(
            "| scenario_id | file_name | file_path | scenario_name | scenario_type | "
            "source_project | possible_protocol | detected_parameters | notes |\n"
        )
        handle.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for row in rows:
            handle.write(
                "| {scenario_id} | {file_name} | {file_path} | {scenario_name} | {scenario_type} | "
                "{source_project} | {possible_protocol} | {detected_parameters} | {notes} |\n".format(
                    **{key: safe_text(value).replace("|", "\\|") for key, value in row.items()}
                )
            )


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir

    if not input_dir.exists():
        print(f"ERROR: input directory does not exist: {input_dir}", file=sys.stderr)
        return 2
    if not input_dir.is_dir():
        print(f"ERROR: input path is not a directory: {input_dir}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    files = find_scenario_files(input_dir)
    rows = [collect_metadata(path, input_dir) for path in files]

    csv_path = output_dir / "scenario_index.csv"
    md_path = output_dir / "scenario_index.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    print(f"Indexed {len(rows)} file(s).")
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
