# Demo Workflow Checklist

Use this checklist when running or explaining the repository synthetic demo.

| Step | Command / Artifact | Status | Notes |
| --- | --- | --- | --- |
| Review demo walkthrough | `docs/demo_walkthrough.md` |  |  |
| Review mapping row | `examples/demo_regulation_mapping.csv` |  | Synthetic only |
| Build scenario index | `python3 -B tools/build_scenario_index.py examples --output-dir /tmp/adas_demo/scenario_index` |  |  |
| Extract XOSC parameters | `python3 -B tools/extract_xosc_params.py examples --output /tmp/adas_demo/xosc_parameter_summary.csv` |  |  |
| Validate XML well-formedness | `python3 -B tools/validate_xosc_schema.py --input examples --output-dir /tmp/adas_demo/validation` |  | No XSD unless supplied |
| Generate esmini dry-run plan | `python3 -B tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run --output-log-dir /tmp/adas_demo/logs --report /tmp/adas_demo/run_plan.md` |  | Dry-run only |
| Export result summary | `python3 -B tools/export_result_summary.py --scenario-index examples/example_scenario_list.csv --results examples/example_result_input.csv --issues examples/example_issue_log.csv --output-dir /tmp/adas_demo/result_summary` |  |  |
| Review issue linkage | `examples/example_issue_log.csv` |  |  |
| Review regression record | `examples/demo_regression_record.md` |  |  |
| Confirm no generated repo pollution | `git status --short --ignored` |  |  |

Demo limitation: this proves workflow shape, not official homologation compliance, NCAP scoring, or vehicle-level performance.

中文说明：demo 只验证流程闭环，不代表官方认证结果。
