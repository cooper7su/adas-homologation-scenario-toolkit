# Demo Test Execution Record

## Basic Information

| Item | Value |
| --- | --- |
| Demo ID | DEMO-AEB-001 |
| Scenario name | Synthetic lead vehicle braking |
| Feature domain | AEB |
| Protocol reference | Synthetic AEB demonstration protocol v0.1 |
| Scenario source | `examples/minimal_aeb_scenario.xosc` |
| Execution mode | Dry-run planning with synthetic result record |
| Test engineer | Example engineer |
| Review status | Demonstration record only |

## Traceability

| Artifact | Path |
| --- | --- |
| Mapping row | `examples/demo_regulation_mapping.csv` |
| Scenario file | `examples/minimal_aeb_scenario.xosc` |
| Scenario list | `examples/example_scenario_list.csv` |
| Result input | `examples/example_result_input.csv` |
| Issue log | `examples/example_issue_log.csv` |
| Regression record | `examples/demo_regression_record.md` |
| Sample summary | `reports/sample_result_summary.md` |

## Version Information

| Component | Version / Identifier |
| --- | --- |
| Toolkit commit | To be filled when publishing a release |
| Scenario file | Synthetic local example |
| Execution wrapper | `tools/run_esmini_batch.py` |
| Result summary tool | `tools/export_result_summary.py` |
| Simulator | Not executed in this demo |

## Environment Conditions

| Item | Value |
| --- | --- |
| Environment | Local workflow demonstration |
| Road type | Straight road |
| Target type | Lead vehicle |
| Ego speed | 50 kph |
| Initial distance | 40 m |
| Target deceleration | -4.0 m/s2 |

## Execution Record

| Run ID | Scenario ID | Execution status | Pass/Fail | Key result | Log path | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| RUN-001 | SCN-001 | completed | Pass | minimum_distance=1.8m; collision=false | `logs/SCN-001` | Synthetic pass case |
| RUN-002 | SCN-002 | completed | Fail | impact_speed=4.2m/s; collision=true | `logs/SCN-002` | Synthetic fail case used to demonstrate issue linkage |

## Abnormal Observation

| Observation ID | Linked run | Description | Initial owner | Severity |
| --- | --- | --- | --- | --- |
| OBS-001 | RUN-002 | Synthetic collision remained after planned AEB mitigation | ADAS_function | Medium |

## Issue Closure Link

| Issue ID | Linked scenario | Status | Responsibility domain | Regression required |
| --- | --- | --- | --- | --- |
| ISSUE-001 | SCN-002 | Open | Planning | Yes |

## Decision

This demo record is not official homologation evidence. It demonstrates how a scenario mapping row, scenario execution record, issue log, and regression record can be connected in one workflow.
