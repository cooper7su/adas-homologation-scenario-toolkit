# Interview Project Summary Template

## Project Title

ADAS Homologation Scenario Toolkit / ADAS 法规认证场景工程工具箱

## One-Sentence Pitch

Describe how the repository connects regulation/protocol intent, scenario metadata, OpenSCENARIO tooling, execution planning, result summary, issue closure, and regression verification without vendoring third-party assets.

中文辅助：一句话说明这个项目如何把法规/协议意图、场景文件、工具链、结果和闭环记录连接起来。

## Problem

- ADAS validation artifacts are often split across protocols, spreadsheets, scenario files, simulator projects, logs, and issue trackers.
- The project demonstrates a lightweight traceability workflow between those artifacts.
- It does not claim to replace official protocol interpretation or homologation authority.

## Repository Capabilities

| Capability | Repository Asset | Evidence Type |
| --- | --- | --- |
| Regulation-to-scenario mapping | `scenario_map/` | Synthetic / engineering record |
| External source boundary | `third_party_manifest.yaml`, `third_party/README.md`, `LICENSE-NOTICE.md` | Boundary documentation |
| Scenario index | `tools/build_scenario_index.py` | Synthetic or external metadata |
| XOSC parameter extraction | `tools/extract_xosc_params.py` | Synthetic or external metadata |
| XML/XSD validation | `tools/validate_xosc_schema.py` | Validation metadata |
| esmini dry-run / guarded execution | `tools/run_esmini_batch.py` | Execution plan or run summary |
| Result summary | `tools/export_result_summary.py` | Synthetic or project result record |
| Issue and regression closure | `templates/issue_tracking_template.csv`, `templates/regression_verification_record.md` | Engineering closure record |

## Demo Flow

```text
regulation/protocol item
  -> scenario mapping
  -> scenario index
  -> OpenSCENARIO parameter extraction
  -> XML validation
  -> esmini dry-run plan
  -> result summary
  -> issue closure
  -> regression verification
```

## Validation Commands

```bash
python3 -B -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in sorted(pathlib.Path('tools').glob('*.py'))]"
python3 -B tools/build_scenario_index.py examples --output-dir /tmp/adas_project_demo/scenario_index
python3 -B tools/extract_xosc_params.py examples --output /tmp/adas_project_demo/xosc_parameter_summary.csv
python3 -B tools/validate_xosc_schema.py --input examples --output-dir /tmp/adas_project_demo/validation
python3 -B tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run --output-log-dir /tmp/adas_project_demo/logs --report /tmp/adas_project_demo/run_plan.md
python3 -B tools/export_result_summary.py --scenario-index examples/example_scenario_list.csv --results examples/example_result_input.csv --issues examples/example_issue_log.csv --output-dir /tmp/adas_project_demo/result_summary
```

## Evidence Classification

- Synthetic evidence: local examples and demo records authored in this repository.
- External metadata: derived indexes, parameter summaries, and validation summaries from external checkouts.
- Official evidence: only evidence supplied and approved by the user's official review process; this repository does not create official certification authority.

## Engineering Decisions

- Keep upstream scenario repositories external or ignored.
- Use metadata extraction and review templates instead of copying third-party scenario files.
- Default esmini workflow to dry-run.
- Require user-supplied XSD schemas for schema validation.
- Keep result summaries linked to issue and regression records.

## Limitations

- No official protocol database.
- No redistributed ASAM schema package.
- No bundled simulator binary.
- Synthetic demo does not prove real vehicle performance, simulator accuracy, or NCAP scoring.
- External metadata must be reviewed against upstream license and source context before publication.

## Interview Talking Points

- Why traceability matters in ADAS validation.
- How a regulation/protocol item becomes a scenario mapping row.
- How scenario metadata can be indexed without copying external files.
- How dry-run planning reduces execution risk.
- How issue closure and regression records make failures auditable.
- How license and evidence boundaries were preserved.

中文辅助：面试重点是工程流程、可追踪性、工具化、边界意识和不夸大能力。
