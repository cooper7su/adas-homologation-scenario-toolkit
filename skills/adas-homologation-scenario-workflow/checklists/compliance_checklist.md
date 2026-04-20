# Compliance Checklist

Use this checklist before committing or publishing any ADAS scenario workflow artifact.

| Check | Status | Evidence / Notes |
| --- | --- | --- |
| Repository docs read: `README.md`, `docs/methodology.md`, `docs/upstream_integration_workflow.md`, `docs/demo_walkthrough.md` |  |  |
| Mapping fields align with `scenario_map/field_definition.md` |  |  |
| Existing `tools/` scripts used for automation where applicable |  |  |
| Existing `templates/` files used for records where applicable |  |  |
| `third_party_manifest.yaml` reviewed for external source boundaries |  |  |
| External source URL recorded |  |  |
| External source commit/release recorded |  |  |
| External source license note recorded |  |  |
| External checkout kept outside repo or under ignored `third_party/*/` |  |  |
| No full third-party scenario library committed |  |  |
| No simulator source tree or binary committed |  |  |
| No standards text or XSD schema package redistributed |  |  |
| Generated reports/logs written to `/tmp` or ignored paths |  |  |
| esmini execution stayed dry-run unless user explicitly requested `--execute` |  |  |
| XSD validation used only user-provided schema |  |  |
| Evidence labeled as synthetic, external metadata, or official evidence |  |  |
| Claims match actual repository capability |  |  |
| `git status --short --ignored` reviewed |  |  |
| No `__pycache__` or accidental generated reports staged |  |  |

中文说明：提交前重点检查第三方边界、生成物位置、证据类型标注和能力表述是否真实。
