# ADAS Homologation Scenario Toolkit

`adas-homologation-scenario-toolkit` is a personal engineering repository for ADAS homologation, proving-ground testing, certification testing, and NCAP-oriented scenario validation workflows.

The repository does not attempt to publish a complete legal interpretation database or redistribute full third-party scenario libraries. Its focus is the engineering layer between public regulations or protocols and repeatable scenario-based testing:

```text
regulation/protocol
        |
        v
scenario mapping
        |
        v
scenario indexing and parameter extraction
        |
        v
execution wrapper
        |
        v
result summary
        |
        v
issue closure and regression verification
```

## Why This Project Exists

ADAS validation work often crosses several boundaries: public protocols, scenario descriptions, simulation tools, proving-ground execution records, and issue tracking. In many teams, these artifacts are handled in separate spreadsheets, simulator projects, and test reports.

This project demonstrates a practical method to connect those artifacts without claiming ownership of third-party standards, scenario libraries, or simulators. It is designed as a portfolio-ready repository that shows how to structure scenario-based homologation work in a traceable and automatable way.

## Problems Addressed

- Map regulation or protocol items to scenario-level test intent.
- Index scenario files from external repositories or local workspaces without copying them into this repository.
- Extract basic OpenSCENARIO parameters for review and coverage tracking.
- Validate OpenSCENARIO/XML well-formedness and optionally validate against a user-provided XSD schema.
- Generate dry-run execution plans or guarded execution summaries for esmini-based scenario playback.
- Merge execution results, scenario metadata, and issue logs into summary reports.
- Provide practical templates for test-day records, issue closure, and regression verification.
- Document upstream integration boundaries through a manifest and external checkout workflow.

## Architecture

```text
+------------------------+
| Regulation / Protocol  |
| UNECE, NCAP, internal  |
+-----------+------------+
            |
            v
+------------------------+       +-------------------------+
| scenario_map/          |       | third_party/            |
| mapping templates      |<----->| upstream integration    |
+-----------+------------+       | notes and boundaries    |
            |                    +-------------------------+
            v
+------------------------+
| tools/                 |
| index, extract, plan,  |
| summarize              |
+-----------+------------+
            |
            v
+------------------------+       +-------------------------+
| reports/               |<----->| templates/              |
| generated CSV/Markdown |       | execution and closure   |
+------------------------+       +-------------------------+
```

## Repository Structure

```text
.
├── assets/              # Reserved for diagrams or lightweight project assets
├── docs/                # Methodology notes
├── examples/            # Small self-contained example inputs
├── reports/             # Generated reports, ignored except .gitkeep
├── scenario_map/        # Regulation-to-scenario mapping templates
├── templates/           # Test execution, issue, and regression templates
├── third_party/         # Upstream project references and integration boundaries
├── tools/               # Python workflow utilities
└── third_party_manifest.yaml
```

## Main Capabilities

### 1. Regulation-to-Scenario Mapping

The files in `scenario_map/` define a compact schema for connecting a regulation family, protocol, scenario identity, trigger condition, expected behavior, pass criteria, and data to record. The goal is not to rewrite the regulation, but to capture the engineering interpretation required to prepare a test case.

### 2. Scenario Indexing

`tools/build_scenario_index.py` scans a directory for `.xosc`, `.xml`, `.json`, `.yaml`, and `.yml` files and writes a unified scenario index to:

- `reports/scenario_index.csv`
- `reports/scenario_index.md`

It is intended for local copies, submodule checkouts, or simulator project folders that are kept outside this repository.

### 3. OpenSCENARIO Parameter Extraction

`tools/extract_xosc_params.py` parses OpenSCENARIO XML files and extracts:

- `ParameterDeclaration` entries
- storyboard or story-level names where present
- entity names from `ScenarioObject` and `EntitySelection`

Output:

- `reports/xosc_parameter_summary.csv`

### 4. esmini Batch Planning

`tools/run_esmini_batch.py` reads a scenario list and generates a dry-run execution plan for esmini. Dry-run is the default mode. If `--execute` is provided, the script checks that `--esmini-path` resolves to an executable, runs each planned command, captures return codes, and writes execution summary files.

Output:

- `reports/run_plan.md`
- per-scenario log directory placeholders under `logs/`
- `reports/esmini_execution_summary.csv` and `.md` when `--execute` is used

### 5. OpenSCENARIO Validation

`tools/validate_xosc_schema.py` validates `.xosc` and `.xml` files. By default it performs XML well-formedness checks. If users provide `--schema` and install optional `lxml`, it can also perform XSD validation.

Output:

- `reports/xosc_validation_report.csv`
- `reports/xosc_validation_report.md`

### 6. Result Summary and Closure

`tools/export_result_summary.py` combines scenario metadata, result input, and issue records into:

- `reports/result_summary.csv`
- `reports/result_summary.md`

The summary highlights pass/fail status, open issue count, and closure status.

### 7. Upstream Integration Manifest

`third_party_manifest.yaml` records each referenced upstream repository, its role, license boundary, recommended local path, allowed integration mode, and content that must not be copied into this repository.

`docs/upstream_integration_workflow.md` explains how to keep upstream checkouts outside the main repository and run this toolkit against those external paths.

`docs/external_source_scan_example.md` records a local smoke-test pattern for scanning a real external scenario library path without committing upstream files.

### 8. End-to-End Synthetic Demo

`docs/demo_walkthrough.md` shows a complete synthetic workflow:

```text
regulation item -> scenario -> execution plan -> result -> issue -> regression
```

The demo uses only local synthetic files and does not copy third-party scenario content.

## Third-Party Project Integration

This repository references the following upstream projects as external inputs or integration targets:

- [openMSL/sl-3-1-osc-alks-scenarios](https://github.com/openMSL/sl-3-1-osc-alks-scenarios): ALKS-oriented OpenSCENARIO interpretation.
- [vectorgrp/OSC-NCAP-scenarios](https://github.com/vectorgrp/OSC-NCAP-scenarios): NCAP scenarios modelled with ASAM OpenSCENARIO XML and OpenDRIVE.
- [esmini/esmini](https://github.com/esmini/esmini): OpenSCENARIO player used as a possible execution backend.
- [BeamNG/BeamNG_NCAP_Tests](https://github.com/BeamNG/BeamNG_NCAP_Tests): BeamNG.tech NCAP test implementation reference.

Integration is intentionally reference-based. This repository may point to local checkouts, submodule locations, or external simulator projects, but it does not vendor complete upstream scenario libraries or simulator source trees.

See `third_party/README.md` and `LICENSE-NOTICE.md` for boundary notes.

## License Boundaries

The original content in this repository is released under the MIT License unless otherwise stated.

Third-party repositories, standards, schemas, scenario files, and simulator code remain under their own licenses and terms. This repository does not change those licenses and does not provide legal advice. Before using upstream assets in commercial, academic, or publication work, verify the upstream license and attribution requirements directly from the source repository or standard owner.

## Implemented Content

- Repository structure for scenario engineering workflow.
- Mapping and catalog templates under `scenario_map/`.
- Methodology document under `docs/`.
- Third-party integration boundary document under `third_party/`.
- Upstream integration manifest and external checkout workflow documentation.
- Python utilities for indexing, OpenSCENARIO parameter extraction, XOSC validation, esmini dry-run or guarded execution, and result summary export.
- Test execution, issue tracking, review, checklist, external source review, and regression templates.
- Small synthetic example data under `examples/`.
- Synthetic end-to-end demo artifacts and a sample summary report.
- A minimal GitHub Actions workflow that validates Python syntax and runs the example workflow.

## Example Usage

Build an index from the synthetic example scenario:

```bash
python3 tools/build_scenario_index.py examples
```

Extract OpenSCENARIO parameters:

```bash
python3 tools/extract_xosc_params.py examples
```

Validate OpenSCENARIO/XML well-formedness:

```bash
python3 tools/validate_xosc_schema.py --input examples
```

Generate an esmini dry-run plan:

```bash
python3 tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run
```

Execute with esmini only after installing it separately:

```bash
python3 tools/run_esmini_batch.py \
  --input examples/example_scenario_list.csv \
  --esmini-path /path/to/esmini \
  --execute
```

Export a result summary:

```bash
python3 tools/export_result_summary.py \
  --scenario-index examples/example_scenario_list.csv \
  --results examples/example_result_input.csv \
  --issues examples/example_issue_log.csv
```

Review the full synthetic demo workflow:

```bash
cat docs/demo_walkthrough.md
```

## Future Extensions

- Add richer OpenSCENARIO and OpenDRIVE metadata extraction.
- Add adapter profiles for esmini, BeamNG.tech, and other simulation backends.
- Add report templates aligned with specific internal test review gates.
- Expand CI checks for template consistency and report schema validation.
- Add optional submodule instructions for users who want to keep upstream scenario repositories outside the main source tree.
