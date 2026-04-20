# Demo Regression Verification Record

## Issue Information

| Item | Value |
| --- | --- |
| Issue ID | ISSUE-001 |
| Linked scenario ID | SCN-002 |
| Original failed run ID | RUN-002 |
| Title | Synthetic impact not mitigated |
| Severity | Medium |
| Owner | ADAS_function |
| Responsibility domain | Planning |
| Fix version | DEMO_FIX_PENDING |

## Regression Scope

| Item | Value |
| --- | --- |
| Scenario file | `examples/minimal_aeb_scenario.xosc` |
| Mapping source | `examples/demo_regulation_mapping.csv` |
| Expected behavior | Brake request and no collision in synthetic lead vehicle braking scenario |
| Pass criteria | `collision_flag=false` and `minimum_distance_m >= 1.0` |
| Required evidence | Result CSV row, run plan, issue closure note |

## Pre-Regression Checks

| Check item | Status | Notes |
| --- | --- | --- |
| Fix version installed | Not applicable | Synthetic demo only |
| Scenario unchanged or reviewed | Pass | Scenario source is the local synthetic XOSC example |
| Logging enabled | Planned | Dry-run command plan creates log folder placeholders |
| Environment comparable to failed run | Pass | Same synthetic input files |

## Verification Runs

| Run ID | Execution status | Pass/Fail | Key measured result | Log path | Notes |
| --- | --- | --- | --- | --- | --- |
| REG-001 | planned | TBD | TBD | `logs/SCN-002` | To be filled after fix verification |

## Closure Decision

| Item | Value |
| --- | --- |
| Regression result | Pending |
| Issue closure status | Open |
| Remaining risk | Synthetic fail case remains unresolved until a pass result is recorded |
| Reviewer | Demo reviewer |

## Evidence

- Mapping: `examples/demo_regulation_mapping.csv`
- Original result: `examples/example_result_input.csv`
- Issue log: `examples/example_issue_log.csv`
- Sample summary: `reports/sample_result_summary.md`
