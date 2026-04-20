# ADAS Homologation Scenario Workflow Skill

This directory contains a Codex Skill for repeatable ADAS homologation and NCAP-oriented scenario engineering work in this repository.

The skill is not a third-party scenario library, standards package, simulator, or legal interpretation database. It documents how a future Codex agent should use the existing repository docs, tools, templates, examples, and license-boundary files to complete workflow tasks safely.

中文说明：这个目录是给未来 Codex 代理使用的工作流 Skill。它沉淀流程、命令、判断标准和边界提醒，不包含第三方完整场景库、法规全文、schema 包或仿真器二进制。

## Relationship To This Repository

The skill references repository-owned assets instead of duplicating them:

- methodology and demo docs under `docs/`
- mapping fields and CSV templates under `scenario_map/`
- automation scripts under `tools/`
- workflow templates under `templates/`
- external boundary files `third_party_manifest.yaml`, `third_party/README.md`, and `LICENSE-NOTICE.md`
- synthetic examples under `examples/`

## How To Use

When a Codex agent is asked to perform ADAS scenario workflow work, it should read `SKILL.md`, then load only the relevant checklist or template:

- `checklists/compliance_checklist.md`
- `checklists/external_source_review_checklist.md`
- `checklists/demo_workflow_checklist.md`
- `templates/interview_project_summary_template.md`
- `templates/scenario_workflow_audit_template.md`

Generated reports, scan outputs, and execution logs should normally be written to `/tmp` unless the user explicitly requests repository artifacts.

## Boundaries

- Do not copy upstream repositories, scenario libraries, standards text, schema packages, or simulator binaries into the main repository.
- Use external checkouts or ignored `third_party/*/` paths only.
- Default to esmini dry-run; use `--execute` only after explicit user request.
- Label evidence as synthetic, external metadata, or official evidence.
