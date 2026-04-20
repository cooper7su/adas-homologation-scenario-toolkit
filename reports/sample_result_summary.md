# Sample Result Summary

This report is a synthetic demonstration artifact. It is not official homologation evidence and does not contain third-party scenario content.

## Summary

| Metric | Value |
| --- | --- |
| Demo workflow | Regulation mapping -> scenario -> execution plan -> result -> issue -> regression |
| Scenario source | `examples/minimal_aeb_scenario.xosc` |
| Result input | `examples/example_result_input.csv` |
| Issue input | `examples/example_issue_log.csv` |
| Total result rows | 2 |
| Passed rows | 1 |
| Failed rows | 1 |
| Open linked issues | 1 |

## Scenario Results

| Scenario ID | Scenario name | Execution status | Pass/Fail | Key result | Issue status |
| --- | --- | --- | --- | --- | --- |
| SCN-001 | Synthetic lead vehicle braking | completed | Pass | minimum_distance=1.8m; collision=false | no linked issue |
| SCN-002 | Synthetic NCAP-style result placeholder | completed | Fail | impact_speed=4.2m/s; collision=true | ISSUE-001 open |

## Issue and Regression Link

| Issue ID | Linked scenario | Owner | Responsibility domain | Closure status | Regression record |
| --- | --- | --- | --- | --- | --- |
| ISSUE-001 | SCN-002 | ADAS_function | Planning | Open | `examples/demo_regression_record.md` |

## Interpretation

The sample demonstrates the reporting shape expected from the toolkit:

1. A mapping row defines the scenario intent and pass criteria.
2. A scenario file provides machine-readable structure for indexing and parameter extraction.
3. A dry-run execution plan provides repeatable command intent.
4. Result input records observed pass/fail state.
5. Issue tracking links failures to an owner and responsibility domain.
6. Regression verification keeps the closure decision traceable.

The failed row is intentional. It shows how an unresolved issue remains visible in the final summary.
