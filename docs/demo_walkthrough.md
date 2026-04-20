# Demo Walkthrough

This walkthrough shows the intended end-to-end workflow using only synthetic data contained in this repository.

The demo path is:

```text
regulation item
  -> scenario mapping
  -> scenario file
  -> scenario index
  -> parameter extraction
  -> execution plan
  -> result summary
  -> issue tracking
  -> regression verification
```

## Demo Artifacts

| Step | Artifact |
| --- | --- |
| Regulation-to-scenario mapping | `examples/demo_regulation_mapping.csv` |
| Scenario source | `examples/minimal_aeb_scenario.xosc` |
| Scenario execution list | `examples/example_scenario_list.csv` |
| Synthetic result input | `examples/example_result_input.csv` |
| Synthetic issue log | `examples/example_issue_log.csv` |
| Execution record | `examples/demo_execution_record.md` |
| Regression record | `examples/demo_regression_record.md` |
| Sample final report | `reports/sample_result_summary.md` |

## Step 1: Review the Mapping Row

Open:

```text
examples/demo_regulation_mapping.csv
```

The row maps a synthetic AEB demonstration protocol item to `DEMO-AEB-001`. It captures:

- feature domain
- target type
- road type
- key parameters
- trigger condition
- expected behavior
- pass criteria
- data to record
- upstream or local scenario reference

This row is not an official protocol definition. It is a traceability record for the demo workflow.

## Step 2: Index the Scenario File

Run:

```bash
python3 tools/build_scenario_index.py examples
```

Expected generated outputs:

```text
reports/scenario_index.csv
reports/scenario_index.md
```

The index should detect `examples/minimal_aeb_scenario.xosc` and identify it as an OpenSCENARIO file with synthetic AEB-related parameters.

## Step 3: Extract OpenSCENARIO Parameters

Run:

```bash
python3 tools/extract_xosc_params.py examples
```

Expected generated output:

```text
reports/xosc_parameter_summary.csv
```

The extractor should capture:

- `ego_speed_kph`
- `target_initial_distance_m`
- `target_deceleration_mps2`
- story and maneuver names
- `EgoVehicle` and `LeadVehicle`

## Step 4: Generate an Execution Plan

Run:

```bash
python3 tools/run_esmini_batch.py \
  --input examples/example_scenario_list.csv \
  --dry-run
```

Expected generated output:

```text
reports/run_plan.md
```

The run plan creates command lines for esmini but does not execute esmini. This keeps the demo runnable on machines without esmini installed.

## Step 5: Export Result Summary

Run:

```bash
python3 tools/export_result_summary.py \
  --scenario-index examples/example_scenario_list.csv \
  --results examples/example_result_input.csv \
  --issues examples/example_issue_log.csv
```

Expected generated outputs:

```text
reports/result_summary.csv
reports/result_summary.md
```

The synthetic result data contains:

- one passing row: `SCN-001`
- one failing row: `SCN-002`
- one open issue linked to `SCN-002`

## Step 6: Review Issue and Regression Closure

Open:

```text
examples/demo_execution_record.md
examples/demo_regression_record.md
reports/sample_result_summary.md
```

These files show how a failed scenario is connected to:

- abnormal observation
- issue owner
- responsibility domain
- regression requirement
- closure status

## What This Demo Proves

The demo proves that the repository can express a realistic test workflow:

- a scenario can be traced back to a protocol-like intent
- the scenario file can be indexed
- basic OpenSCENARIO parameters can be extracted
- an execution plan can be generated without assuming simulator installation
- result rows can be linked to issue records
- regression records can preserve closure context

## What This Demo Does Not Prove

The demo does not prove:

- official homologation compliance
- real NCAP scoring
- simulator accuracy
- esmini execution success
- vehicle-level AEB performance

Those require validated scenarios, a configured simulator or proving-ground setup, measured logs, and review by the responsible technical authority.
