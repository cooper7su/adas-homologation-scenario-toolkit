# Example Skill Task

## User Request

Use the ADAS workflow skill to review an external NCAP OpenSCENARIO checkout, create a small metadata-only scenario index, extract parameters, validate XML well-formedness, produce an esmini dry-run plan, and summarize what can be shown in an interview report. Do not commit upstream files.

## Expected Agent Inputs

- Repository root: `adas-homologation-scenario-toolkit`
- External checkout path: `../external-workspace/OSC-NCAP-scenarios`
- Upstream URL: `https://github.com/vectorgrp/OSC-NCAP-scenarios`
- Upstream commit/release: provided by `git -C <checkout> rev-parse HEAD`
- License note: taken from upstream and cross-checked with `third_party_manifest.yaml`
- Output root: `/tmp/adas_external_review`

## Expected Agent Actions

1. Read `SKILL.md`, `README.md`, `docs/upstream_integration_workflow.md`, and `third_party_manifest.yaml`.
2. Confirm the external source is outside the main repository or under ignored `third_party/*/`.
3. Run `tools/build_scenario_index.py` to `/tmp`.
4. Run `tools/extract_xosc_params.py` to `/tmp`.
5. Run `tools/validate_xosc_schema.py` to `/tmp`; use no XSD unless supplied by the user.
6. Generate an esmini dry-run plan only.
7. Draft an external source review using `templates/external_source_review.md`.
8. Draft an interview summary using `templates/interview_project_summary_template.md`.
9. Check `git status --short --ignored` before committing any repository changes.

## Expected Boundaries

- Do not copy `.xosc`, `.xodr`, catalog, variation, schema, simulator source, or binary files into this repository.
- Commit only original review text or small metadata samples if the user explicitly asks.
- Mark outputs as external metadata, not official evidence.

中文说明：这个示例任务展示外部场景库如何只做 metadata 级接入，不把第三方场景文件提交进主仓库。
