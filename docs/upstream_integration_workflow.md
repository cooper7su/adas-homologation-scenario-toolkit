# Upstream Integration Workflow

This document explains how to connect external scenario repositories and simulator tools to this toolkit without copying full third-party projects into the main repository.

## Integration Principle

The toolkit owns the workflow layer:

- regulation-to-scenario mapping
- scenario indexing
- parameter extraction
- execution planning
- result summary
- issue closure and regression records

The upstream projects remain external inputs:

- scenario libraries stay in external checkouts
- simulator source trees and binaries stay outside this repository
- upstream licenses and attribution stay with the upstream content

## Recommended Local Layout

Use a sibling workspace for external projects:

```text
work/
├── adas-homologation-scenario-toolkit/
└── external-workspace/
    ├── sl-3-1-osc-alks-scenarios/
    ├── OSC-NCAP-scenarios/
    ├── esmini/
    └── BeamNG_NCAP_Tests/
```

This keeps the toolkit repository small and clearly separates original workflow content from upstream assets.

## Optional Local Checkout Commands

Run these commands outside the toolkit repository:

```bash
mkdir -p ../external-workspace
cd ../external-workspace

git clone https://github.com/openMSL/sl-3-1-osc-alks-scenarios.git
git clone https://github.com/vectorgrp/OSC-NCAP-scenarios.git
git clone https://github.com/esmini/esmini.git
git clone https://github.com/BeamNG/BeamNG_NCAP_Tests.git
```

If you place local checkouts under `third_party/`, keep them uncommitted. The repository `.gitignore` intentionally ignores `third_party/*/`.

## Record Upstream Metadata

Before generating indexes or reports from an external checkout, record:

- repository URL
- upstream license
- local checkout path
- commit SHA or release tag
- role in the test workflow

Use `third_party_manifest.yaml` as the canonical reference for expected upstream roles and boundaries.

Example command:

```bash
git -C ../external-workspace/OSC-NCAP-scenarios rev-parse HEAD
```

## Build a Scenario Index from an External Checkout

From the toolkit repository:

```bash
python3 tools/build_scenario_index.py ../external-workspace/OSC-NCAP-scenarios
```

Outputs:

- `reports/scenario_index.csv`
- `reports/scenario_index.md`

These generated files are ignored by default. If you want to publish a derived metadata sample, keep it small, avoid copying scenario file contents, and include upstream URL and commit information.

## Extract OpenSCENARIO Parameters

```bash
python3 tools/extract_xosc_params.py ../external-workspace/OSC-NCAP-scenarios
```

Output:

- `reports/xosc_parameter_summary.csv`

The extractor is intentionally lightweight. It reads XML metadata and does not validate scenario correctness.

## Validate OpenSCENARIO/XML Files

Run a basic XML well-formedness check:

```bash
python3 tools/validate_xosc_schema.py \
  --input ../external-workspace/OSC-NCAP-scenarios
```

If you have an authorized local XSD schema file and optional `lxml` installed, run:

```bash
python3 tools/validate_xosc_schema.py \
  --input ../external-workspace/OSC-NCAP-scenarios \
  --schema /path/to/OpenSCENARIO.xsd
```

The toolkit does not redistribute ASAM schemas. Keep schema files outside this repository unless their license explicitly allows redistribution.

## Generate an esmini Dry-Run Plan

If esmini is installed separately:

```bash
python3 tools/run_esmini_batch.py \
  --input reports/scenario_index.csv \
  --esmini-path ../external-workspace/esmini/bin/esmini \
  --dry-run
```

This creates a command plan only. The toolkit does not execute esmini by default.

To execute after installing esmini separately:

```bash
python3 tools/run_esmini_batch.py \
  --input reports/scenario_index.csv \
  --esmini-path ../external-workspace/esmini/bin/esmini \
  --execute
```

Execution writes `reports/esmini_execution_summary.csv`, `reports/esmini_execution_summary.md`, and per-scenario log files. Use this only after verifying catalog paths, OpenDRIVE references, and simulator compatibility.

## Link External Scenarios to Mapping Rows

Use `scenario_map/regulation_to_scenario_template.csv` or a project-specific copy to connect:

- protocol item
- scenario ID
- scenario name
- key parameters
- trigger condition
- expected behavior
- pass criteria
- upstream reference

Recommended `upstream_reference` format:

```text
repo=https://github.com/vectorgrp/OSC-NCAP-scenarios; commit=<sha>; path=<relative scenario path>
```

## BeamNG Reference Usage

`BeamNG/BeamNG_NCAP_Tests` should be treated as a simulator-specific implementation reference. Keep any BeamNG.tech project, scenario setup, sensor configuration, or controller implementation outside this toolkit unless a separate adapter is designed and its license boundary is reviewed.

## What Not to Commit

Do not commit:

- full upstream repositories
- simulator binaries
- OpenSCENARIO/OpenDRIVE schema packages copied from standards
- large generated reports from complete upstream scans
- third-party scenario files without a clear license review

Commit only:

- original workflow documentation
- original tooling
- small synthetic examples
- small derived metadata samples with attribution, when necessary
- configuration examples that use placeholder paths

## Minimal Review Checklist

Before publishing any upstream-derived artifact:

| Check | Required |
| --- | --- |
| Upstream URL recorded | Yes |
| Commit or release recorded | Yes |
| License reviewed | Yes |
| No full third-party file copied | Yes |
| Generated output is metadata only | Yes |
| Report states that it is not official homologation evidence | Yes |
