---
name: adas-homologation-scenario-workflow
description: Use this skill for ADAS homologation, NCAP, ALKS, AEB, OpenSCENARIO, esmini, external scenario library, issue closure, regression verification, and interview-ready project reporting workflows in the adas-homologation-scenario-toolkit repository.
---

# ADAS Homologation Scenario Workflow Skill

## 1. Skill Name

ADAS Homologation Scenario Workflow / ADAS 法规认证场景工程工作流

## 2. When To Use

Use this skill when the user asks a Codex agent to work inside `adas-homologation-scenario-toolkit` on:

- regulation/protocol item to scenario mapping
- NCAP, ALKS, AEB, LSS, or internal ADAS scenario workflow traceability
- external scenario library review without vendoring upstream content
- scenario indexing, OpenSCENARIO parameter extraction, XML/XSD validation
- esmini dry-run planning or explicitly requested guarded execution
- result summary, issue closure, regression verification, or demo walkthrough
- interview/portfolio project report generation based on this repository

中文辅助说明：当任务涉及 ADAS 法规/NCAP 场景映射、外部场景库接入、XOSC 工具链、esmini 计划执行、问题闭环、回归验证或求职展示报告时使用。

## 3. When Not To Use

Do not use this skill to:

- provide legal advice or official homologation certification conclusions
- reproduce full regulation text, protocol text, ASAM schema packages, or third-party scenario files
- vendor upstream repositories, simulator source trees, binaries, or generated road networks
- claim real vehicle performance, NCAP scoring, or simulator accuracy from the synthetic demo
- implement simulator-specific adapters that do not exist in this repository
- execute esmini unless the user explicitly asks for execution and provides or approves a valid executable path

中文辅助说明：不要把本 Skill 当成法规原文、官方认证结论、第三方源码库或仿真器发布包。

## 4. Required Inputs

Collect or infer these inputs before producing durable outputs:

- repository root of `adas-homologation-scenario-toolkit`
- target workflow: mapping, indexing, extraction, validation, dry-run, execution, summary, closure, regression, or report
- regulation/protocol reference name and version, without copying long official text
- scenario source path: local synthetic examples, project scenario folder, or external checkout path
- external source metadata when applicable: upstream URL, license note, commit/release, local path, and intended role
- XSD schema path only if the user supplies an authorized local schema
- esmini executable path only for explicit `--execute` workflows
- result CSV and issue CSV paths for summary/closure work

If data is missing, proceed with a clearly marked placeholder only when safe. For external assets, prefer stopping for source metadata over guessing.

## 5. Expected Outputs

Produce concise, auditable artifacts. Common outputs include:

- mapping rows based on `scenario_map/regulation_to_scenario_template.csv`
- review notes using `templates/regulation_to_scenario_review.md`
- external source review records using `templates/external_source_review.md`
- generated scenario metadata from `tools/build_scenario_index.py`
- generated XOSC parameter metadata from `tools/extract_xosc_params.py`
- generated validation reports from `tools/validate_xosc_schema.py`
- generated esmini dry-run plans from `tools/run_esmini_batch.py`
- result summaries from `tools/export_result_summary.py`
- test, issue, and regression records using `templates/test_execution_record.md`, `templates/issue_tracking_template.csv`, and `templates/regression_verification_record.md`
- interview/project summaries using `skills/adas-homologation-scenario-workflow/templates/interview_project_summary_template.md`

Always label evidence as `synthetic`, `external metadata`, or `official evidence` where relevant. This repository normally produces synthetic demo evidence or derived external metadata, not official certification evidence.

## 6. Core Workflow

Start by reading the repository documents instead of inventing a new process:

1. Read `README.md` for implemented capabilities and boundaries.
2. Read `docs/methodology.md` for scenario workflow rationale.
3. Read `docs/upstream_integration_workflow.md` and `third_party_manifest.yaml` before using external repositories.
4. Read `docs/demo_walkthrough.md` for the synthetic end-to-end example.
5. Use `scenario_map/field_definition.md` and the CSV templates for mapping fields.
6. Use scripts under `tools/` for automation.
7. Use templates under `templates/` and this skill's `templates/` for records and reports.
8. Write generated outputs to `/tmp` unless the user explicitly asks to create repository artifacts.
9. Run validation and audit checks before committing.

中文辅助说明：先读现有 README/docs/manifest，再调用 tools；不要重造流程，不要把生成物或上游文件误提交。

## 7. File And Tool References

Canonical repository references:

- Method: `README.md`, `docs/methodology.md`, `docs/demo_walkthrough.md`
- External integration: `docs/upstream_integration_workflow.md`, `docs/external_source_scan_example.md`, `third_party/README.md`, `third_party_manifest.yaml`, `LICENSE-NOTICE.md`
- Mapping schema: `scenario_map/field_definition.md`, `scenario_map/regulation_to_scenario_template.csv`, `scenario_map/ncap_scenario_catalog_template.csv`
- Automation tools: `tools/build_scenario_index.py`, `tools/extract_xosc_params.py`, `tools/validate_xosc_schema.py`, `tools/run_esmini_batch.py`, `tools/export_result_summary.py`
- Project templates: `templates/external_source_review.md`, `templates/regulation_to_scenario_review.md`, `templates/test_execution_record.md`, `templates/test_day_checklist.md`, `templates/issue_tracking_template.csv`, `templates/regression_verification_record.md`
- Synthetic examples: `examples/`
- Skill checklists: `skills/adas-homologation-scenario-workflow/checklists/`
- Skill report templates: `skills/adas-homologation-scenario-workflow/templates/`

## 8. External Third-Party Boundary

The repository owns workflow glue, templates, and lightweight Python utilities. Upstream content stays external.

Rules:

- Use `third_party_manifest.yaml` as the first source for upstream role, license notes, allowed integration modes, and non-copied boundaries.
- Clone upstream repositories outside the toolkit, for example `../external-workspace/<repo>`, or into ignored `third_party/*/` paths.
- Do not commit full third-party scenario libraries, simulator source trees, binaries, ASAM schemas, standards text, catalogs, generated road networks, or full upstream history.
- If scanning an external source, commit only small derived metadata or a short review document when needed.
- Record upstream URL, commit/release, license, local path, and source role in every external-source review.
- Generated external metadata is not official homologation or NCAP evidence.

中文辅助说明：第三方内容只能外部引用或本地 ignored 使用；主仓库只保留 workflow、metadata、小样例和边界说明。

## 9. Regulation/Protocol To Scenario Mapping

Process:

1. Identify the protocol family, protocol name/version, and item intent without copying long official text.
2. Read `scenario_map/field_definition.md`.
3. Create or update rows using `scenario_map/regulation_to_scenario_template.csv` or `scenario_map/ncap_scenario_catalog_template.csv`.
4. Keep `scenario_id` stable and independent from file names.
5. Fill target type, road type, key parameters, trigger condition, expected behavior, pass criteria, data to record, upstream reference, and remarks.
6. If the scenario comes from an external repository, format `upstream_reference` with repository URL, commit/release, and relative path.
7. Use `templates/regulation_to_scenario_review.md` for review evidence.

Do not present the mapping row as legal interpretation. It is an engineering traceability record.

## 10. Scenario Indexing

Use `tools/build_scenario_index.py` for scenario-like files:

```bash
python3 -B tools/build_scenario_index.py <input_dir> --output-dir /tmp/adas_scenario_index
```

Current script capability:

- scans `.xosc`, `.xml`, `.json`, `.yaml`, `.yml`
- skips `third_party_manifest.yaml` and `*.example.yaml`
- extracts lightweight XML/JSON/YAML metadata
- infers possible source project and possible protocol from names/text
- writes `scenario_index.csv` and `scenario_index.md`

For external repositories, scan the external checkout path and review the metadata before committing any derived sample.

## 11. OpenSCENARIO Parameter Extraction

Use `tools/extract_xosc_params.py`:

```bash
python3 -B tools/extract_xosc_params.py <xosc_file_or_dir> --output /tmp/adas_xosc_parameter_summary.csv
```

Current script capability:

- scans `.xosc` and `.xml`
- extracts `ParameterDeclaration` entries
- extracts names for `Storyboard`, `Story`, `Act`, `ManeuverGroup`, `Maneuver`, and `Event`
- extracts `ScenarioObject` and `EntitySelection` names
- writes CSV metadata only

It does not prove scenario correctness, OpenDRIVE compatibility, or simulator behavior.

## 12. XOSC/XML Validation

Use `tools/validate_xosc_schema.py`:

```bash
python3 -B tools/validate_xosc_schema.py --input <xosc_file_or_dir> --output-dir /tmp/adas_xosc_validation
```

Default validation is XML well-formedness only. For XSD validation:

```bash
python3 -B tools/validate_xosc_schema.py \
  --input <xosc_file_or_dir> \
  --schema /path/to/user/provided/OpenSCENARIO.xsd \
  --output-dir /tmp/adas_xosc_validation
```

Rules:

- XSD schema files must be supplied by the user from an authorized source.
- This repository does not distribute ASAM schema packages.
- Optional XSD validation requires `lxml`; if unavailable, the script reports partial validation.

## 13. esmini Dry-Run / Execute

Default to dry-run:

```bash
python3 -B tools/run_esmini_batch.py \
  --input <scenario_list.csv_or_dir> \
  --dry-run \
  --output-log-dir /tmp/adas_esmini_logs \
  --report /tmp/adas_esmini_run_plan.md
```

Only use `--execute` when the user explicitly requests execution and provides/approves the esmini executable:

```bash
python3 -B tools/run_esmini_batch.py \
  --input <scenario_list.csv_or_dir> \
  --esmini-path /path/to/esmini \
  --execute \
  --output-log-dir /tmp/adas_esmini_logs \
  --report /tmp/adas_esmini_run_plan.md \
  --execution-summary /tmp/adas_esmini_execution_summary.csv
```

Guardrails:

- Verify the executable resolves and is executable.
- Check scenario paths, catalogs, OpenDRIVE references, and simulator compatibility before execution.
- Keep esmini source and binaries outside the repository.
- Treat execution results as workflow evidence unless reviewed under the user's official process.

## 14. Result Summary

Use `tools/export_result_summary.py`:

```bash
python3 -B tools/export_result_summary.py \
  --scenario-index <scenario_index_or_list.csv> \
  --results <result_input.csv> \
  --issues <issue_log.csv> \
  --output-dir /tmp/adas_result_summary
```

Current script capability:

- merges scenario metadata, result rows, and optional issue rows by scenario ID
- computes issue count, open issue count, and closure status
- writes `result_summary.csv` and `result_summary.md`

Result inputs should be concise, evidence-linked, and clear about synthetic / external metadata / official evidence status.

## 15. Issue Closure / Regression Verification

Use:

- `templates/issue_tracking_template.csv` for issue records
- `templates/regression_verification_record.md` for regression closure evidence
- `templates/test_execution_record.md` for execution context
- `tools/export_result_summary.py` for open/closed issue visibility

Closure process:

1. Link each failing scenario to an issue ID and owner.
2. Record severity, responsibility domain, root cause or TBD, fix version, and closure evidence.
3. Mark whether regression is required.
4. Run or plan the same scenario or an reviewed equivalent regression case.
5. Record result, logs, configuration snapshot, reviewer, and remaining risk.
6. Do not mark closed unless evidence supports the closure status.

## 16. Interview / Project Report Generation

Use `skills/adas-homologation-scenario-workflow/templates/interview_project_summary_template.md`.

Report structure should cover:

- project purpose and problem statement
- workflow architecture
- implemented repository capabilities
- external boundary and license discipline
- demo workflow and validation commands
- evidence classification: synthetic, external metadata, official evidence
- engineering impact and limitations
- next steps that are clearly marked as future work

Do not overclaim. State that the repository demonstrates an engineering workflow, not official certification authority.

## 17. Audit And Compliance Checks

Before publishing or committing:

1. Confirm the skill exists and required sections are present.
2. Confirm references match real repository files and scripts.
3. Confirm no nonexistent capability is claimed.
4. Confirm third-party boundaries are explicit.
5. Confirm no third-party source, scenario library, standard text, schema package, or simulator binary is committed.
6. Confirm generated reports/logs are under `/tmp` or ignored.
7. Confirm documentation includes English-first content with Chinese auxiliary notes.
8. Confirm final artifacts are suitable for future Codex agents and project presentation.
9. Run `git status --short --ignored`.
10. Check for `__pycache__`, accidental `reports/` outputs, `logs/`, and copied external directories.

Use `skills/adas-homologation-scenario-workflow/checklists/compliance_checklist.md` and `skills/adas-homologation-scenario-workflow/templates/scenario_workflow_audit_template.md`.

## 18. Common Commands

```bash
python3 -B -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in sorted(pathlib.Path('tools').glob('*.py'))]"
python3 -B tools/build_scenario_index.py examples --output-dir /tmp/adas_skill_validation/scenario_index
python3 -B tools/extract_xosc_params.py examples --output /tmp/adas_skill_validation/xosc_parameter_summary.csv
python3 -B tools/validate_xosc_schema.py --input examples --output-dir /tmp/adas_skill_validation/validation
python3 -B tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run --output-log-dir /tmp/adas_skill_validation/logs --report /tmp/adas_skill_validation/run_plan.md
python3 -B tools/export_result_summary.py --scenario-index examples/example_scenario_list.csv --results examples/example_result_input.csv --issues examples/example_issue_log.csv --output-dir /tmp/adas_skill_validation/result_summary
git status --short --ignored
```

## 19. Common Errors And Handling

- Missing input path: check whether the path is relative to the repository root or an external checkout.
- Empty scenario index: confirm files use supported extensions and are not only `*.example.yaml`.
- XML parse error: report the file path and parse message; do not "fix" upstream files in the toolkit repo.
- XSD validation unavailable: ask for a user-provided schema and ensure `lxml` is installed.
- esmini executable not found: stay in dry-run mode unless the user provides a valid executable.
- External checkout inside repo appears in status: ensure it is under ignored `third_party/*/` or move it outside the repository.
- Generated reports show in git status: move outputs to `/tmp` or confirm `.gitignore`.
- User asks for official compliance: clarify that this toolkit supports engineering traceability and does not replace official protocol review.

## 20. Short Bilingual Summary

English: This skill turns the repository into a repeatable Codex workflow for ADAS regulation-to-scenario traceability, external scenario library review, OpenSCENARIO metadata extraction, XML/XSD validation, esmini planning, result summary, issue closure, regression verification, and professional project reporting. It preserves strict third-party boundaries and defaults to safe dry-run behavior.

中文：这个 Skill 用于指导 Codex 在本仓库内完成 ADAS 法规/NCAP 场景工程流程，包括场景映射、外部库合规接入、XOSC 参数提取、XML/XSD 验证、esmini dry-run、结果汇总、issue 闭环、回归验证和项目展示报告。默认不复制第三方内容，默认 dry-run，避免夸大为官方认证结论。
