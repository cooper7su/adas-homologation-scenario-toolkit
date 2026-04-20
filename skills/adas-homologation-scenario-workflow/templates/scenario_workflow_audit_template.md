# Scenario Workflow Audit Template

## Audit Scope

| Item | Value |
| --- | --- |
| Audit date |  |
| Repository commit |  |
| Workflow reviewed | Mapping / external source / index / extraction / validation / dry-run / execution / summary / closure / report |
| Reviewer |  |

## Required File Checks

| Check | Status | Evidence |
| --- | --- | --- |
| Skill exists at `skills/adas-homologation-scenario-workflow/SKILL.md` |  |  |
| Repository README documents the skill entry point |  |  |
| Mapping fields align with `scenario_map/field_definition.md` |  |  |
| Tools referenced exist under `tools/` |  |  |
| Templates referenced exist under `templates/` or skill `templates/` |  |  |
| Third-party boundaries align with `third_party_manifest.yaml` and `LICENSE-NOTICE.md` |  |  |

## Capability Accuracy

| Claim | Status | Evidence / Correction |
| --- | --- | --- |
| Scenario indexing capability is accurately described |  |  |
| XOSC parameter extraction capability is accurately described |  |  |
| XML/XSD validation capability is accurately described |  |  |
| esmini dry-run / execute capability is accurately described |  |  |
| Result summary capability is accurately described |  |  |
| Issue closure / regression workflow is accurately described |  |  |
| Interview report generation does not overclaim official evidence |  |  |

## Compliance Boundary

| Check | Status | Evidence / Notes |
| --- | --- | --- |
| No third-party complete scenario library copied |  |  |
| No simulator source or binary copied |  |  |
| No standards text or schema package copied |  |  |
| External metadata is small and attributed if committed |  |  |
| Evidence classification is present |  |  |
| Generated outputs are in `/tmp` or ignored paths |  |  |

## Validation Commands

Record commands run and outputs:

```bash
python3 -B -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in sorted(pathlib.Path('tools').glob('*.py'))]"
python3 -B tools/build_scenario_index.py examples --output-dir /tmp/adas_skill_validation/scenario_index
python3 -B tools/extract_xosc_params.py examples --output /tmp/adas_skill_validation/xosc_parameter_summary.csv
python3 -B tools/validate_xosc_schema.py --input examples --output-dir /tmp/adas_skill_validation/validation
python3 -B tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run --output-log-dir /tmp/adas_skill_validation/logs --report /tmp/adas_skill_validation/run_plan.md
python3 -B tools/export_result_summary.py --scenario-index examples/example_scenario_list.csv --results examples/example_result_input.csv --issues examples/example_issue_log.csv --output-dir /tmp/adas_skill_validation/result_summary
git status --short --ignored
```

## Findings

| Finding ID | Severity | Description | Fix | Re-audit Result |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Final Verdict

Ready to publish / Needs fixes

中文辅助：审计重点是能力真实、边界清晰、没有第三方误提交、输出可复核。
