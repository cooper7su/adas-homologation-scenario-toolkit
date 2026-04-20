# ADAS Homologation Scenario Toolkit Audit Report

## Executive Summary

Audit date: 2026-04-21  
Workspace: `/Users/coopersu/Documents/ADAS_TEST`  
Audited repository name: `adas-homologation-scenario-toolkit`

Final verdict: **Ready to publish**

The repository is structurally aligned with the original project requirements. It presents a personal engineering-method repository for ADAS homologation, proving-ground testing, certification testing, and NCAP-oriented scenario validation. The core workflow is represented end to end: regulation-to-scenario mapping, scenario indexing, OpenSCENARIO parameter extraction, esmini dry-run execution planning, result summary, and issue/regression templates.

No evidence was found that full third-party repositories, third-party source trees, or large upstream scenario libraries were copied into this repository. The only third-party integration content is reference documentation under `third_party/README.md` and license boundary notes under `LICENSE-NOTICE.md`.

Post-audit remediation completed:

- Generated ignored artifacts were removed from the working tree.
- `tools/build_scenario_index.py` now includes `file_path` and `detected_parameters` in the Markdown scenario index.
- `.github/workflows/ci.yml` was added to validate Python syntax and run the example workflow.

## Audit Scope and Method

The audit used local file inspection, syntax validation, and example workflow execution. Script outputs were written to `/tmp/adas_audit_*` to avoid modifying repository source files during the audit.

Verification commands run:

```bash
python3 -B -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in sorted(pathlib.Path('tools').glob('*.py'))]"
python3 -B tools/build_scenario_index.py examples --output-dir /tmp/adas_audit_scenario_index
python3 -B tools/extract_xosc_params.py examples --output /tmp/adas_audit_xosc_parameter_summary.csv
python3 -B tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run --output-log-dir /tmp/adas_audit_logs --report /tmp/adas_audit_run_plan.md
python3 -B tools/export_result_summary.py --scenario-index examples/example_scenario_list.csv --results examples/example_result_input.csv --issues examples/example_issue_log.csv --output-dir /tmp/adas_audit_result_summary
```

Counts before audit artifacts were added:

- Publishable non-ignored files reported by `git ls-files --others --exclude-standard`: 25
- Files excluding `.git` and `tools/__pycache__`: 31
- Python scripts: 4
- Templates: 5
- Example files: 4

## Check Matrix by Section

| Section | Status | Evidence | Gaps | Recommended fixes |
| --- | --- | --- | --- | --- |
| 1. Repository structure | Pass | Required directories exist: `docs/`, `scenario_map/`, `tools/`, `templates/`, `third_party/`, `reports/`, `examples/`, `assets/`. Required base files exist: `README.md`, `LICENSE`, `LICENSE-NOTICE.md`, `.gitignore`, `requirements.txt`. | No blocking gap after generated artifacts were cleaned. | Commit intended source, docs, templates, examples, and audit files only. |
| 2. README audit | Pass | `README.md` includes project intro, motivation, problems, architecture, structure, capabilities, third-party integration, license boundaries, implemented content, usage, and future extensions. | No blocking gap. | No action required. |
| 3. Third-party dependency notes | Pass | `third_party/README.md:7-49` covers all four upstream projects with role, category, license notes, integration approach, and non-copied content. `LICENSE-NOTICE.md:5-31` documents boundaries. | Unable to verify legal sufficiency; this is not legal advice. Upstream license statements were spot-checked from official GitHub pages only. | Keep upstream URLs, commit hashes, and license files with any local external checkout. |
| 4. Scenario mapping framework | Pass | `scenario_map/regulation_to_scenario_template.csv`, `scenario_map/ncap_scenario_catalog_template.csv`, and `scenario_map/field_definition.md` exist. Required CSV headers are present. `docs/methodology.md:1-54` covers the required method topics. | No blocking gap. | Consider adding a second synthetic row covering a non-AEB domain if broader interview demonstration is desired. |
| 5. Tool scripts | Pass | Four scripts exist under `tools/`. AST syntax check passed. Example runs succeeded using `/tmp/adas_audit_*` outputs. Markdown index now includes `file_path` and `detected_parameters`. | `run_esmini_batch.py` is dry-run only, by design. | Add real execution mode only when esmini availability and command semantics are explicitly handled. |
| 6. Templates | Pass | Required templates exist under `templates/`. Combined templates cover pre-checks, scenario info, versions, environment, execution records, abnormal observations, ownership, closure, and regression results. | No blocking gap. Some fields are distributed across templates rather than repeated in every template. | Keep templates focused; optionally add a short README in `templates/` describing intended use order. |
| 7. Example data | Pass | Required example CSVs exist. `examples/minimal_aeb_scenario.xosc` is synthetic and supports indexing and parameter extraction. Example CSVs support dry-run planning and result summary. | `example_scenario_list.csv` maps two scenario IDs to the same synthetic XOSC file; acceptable for minimal demo but limited. | Add one more distinct synthetic scenario if showing multiple-case indexing matters. |
| 8. License and boundaries | Pass | `LICENSE` is MIT. `LICENSE-NOTICE.md:3-31` separates original content from upstream references. `.gitignore:17-19` prevents ignored local upstream checkouts under `third_party/` from being committed. | Unable to verify all future user-added upstream local checkouts. | Keep `third_party/*/` ignored and require upstream license preservation in documentation. |
| 9. Overall conclusion | Pass | Project positioning, structure, docs, tools, examples, CI, and boundaries are aligned. | No blocking gap. | Ready for initial public push. |

## Detailed Findings

### 1. Repository Structure Check

Status: **Pass**

Evidence:

- Required directories are present: `docs/`, `scenario_map/`, `tools/`, `templates/`, `third_party/`, `reports/`, `examples/`, `assets/`.
- Required base files are present: `README.md`, `LICENSE`, `LICENSE-NOTICE.md`, `.gitignore`, `requirements.txt`.
- `third_party/` contains only `third_party/README.md`, not upstream source trees.
- No files larger than 200 KB were found outside `.git` and `tools/__pycache__`.
- Generated outputs are ignored by `.gitignore`, and post-audit cleanup removed the local generated files from the working tree.

Assessment:

- Structure is clear and aligned with the project goal.
- No unrelated source files were found.
- No obvious third-party repository copy was found.
- `logs/` exists as a generated output directory and is ignored by `.gitignore`.

Recommended fix:

- Before public release, confirm that ignored generated artifacts are not committed or packaged as source.

### 2. README Audit

Status: **Pass**

Evidence:

- Project introduction: `README.md:1-5`
- Workflow text diagram: `README.md:7-24`
- Motivation: `README.md:26-30`
- Problems addressed: `README.md:32-39`
- Architecture diagram: `README.md:41-67`
- Directory structure: `README.md:69-81`
- Main capabilities: `README.md:83-126`
- Third-party integration: `README.md:128-139`
- License boundaries: `README.md:141-145`
- Implemented content: `README.md:147-155`
- Example usage: `README.md:157-184`
- Future extensions: `README.md:186-193`

Style assessment:

- The README is professional and not inflated.
- It does not claim official certification capability or legal completeness.
- It emphasizes scenario workflow, engineering integration, execution planning, and closure.
- It is suitable for a technical interview discussion because it explains why the repository exists and what has actually been implemented.

Gaps:

- No blocking gap. README examples now use `python3` for platform clarity.

### 3. Third-Party Dependency Notes Audit

Status: **Pass**

Evidence:

- `openMSL/sl-3-1-osc-alks-scenarios`: `third_party/README.md:7-16`
- `vectorgrp/OSC-NCAP-scenarios`: `third_party/README.md:18-27`
- `esmini/esmini`: `third_party/README.md:29-38`
- `BeamNG/BeamNG_NCAP_Tests`: `third_party/README.md:40-49`
- Recommended external layout: `third_party/README.md:51-64`
- License boundary table: `LICENSE-NOTICE.md:11-18`
- Non-included content: `LICENSE-NOTICE.md:20-25`

External spot-check:

- The openMSL repository page describes ALKS scenario interpretation using OpenSCENARIO and states MPL-2.0 licensing for the corresponding OpenSCENARIO bundle.
- The Vector repository page describes NCAP scenarios modelled in OpenSCENARIO/OpenDRIVE and states MPL-2.0 licensing for OpenSCENARIO XML and OpenDRIVE files.
- The esmini repository page identifies esmini as a basic OpenSCENARIO XML player and is marked MPL-2.0.
- The BeamNG repository page is marked MIT licensed and describes selected NCAP test workflows for BeamNG.tech.

Assessment:

- No exaggerated or fabricated capability was found.
- No statement implies that this repository contains the complete upstream source.
- The integration model is reference-based and consistent with the original requirement.

Gaps:

- Legal compliance cannot be fully verified from README-level inspection alone.

Recommended fix:

- If upstream files are later used locally, record upstream URL, commit hash, license file path, and attribution in the generated report or mapping row.

### 4. Regulation-to-Scenario Mapping Framework Audit

Status: **Pass**

Evidence:

- `scenario_map/regulation_to_scenario_template.csv` exists and contains the required fields.
- `scenario_map/ncap_scenario_catalog_template.csv` exists and contains the required fields.
- `scenario_map/field_definition.md:1-28` defines all key fields and usage notes.
- `docs/methodology.md:5-54` covers scenario representation, mapping, real/simulation linkage, and closure.

Required CSV field check:

All required fields are present:

- `regulation_family`
- `protocol_name`
- `scenario_id`
- `scenario_name`
- `feature_domain`
- `target_type`
- `road_type`
- `key_parameters`
- `trigger_condition`
- `expected_behavior`
- `pass_criteria`
- `data_to_record`
- `upstream_reference`
- `remarks`

Assessment:

- The mapping framework is intentionally lightweight and suitable for an interview-oriented method repository.
- It avoids turning the repo into a regulation encyclopedia.

Recommended fix:

- Optional: add a short `scenario_map/README.md` later if multiple mapping files are introduced.

### 5. Tool Script Audit

Status: **Pass**

#### `build_scenario_index.py`

Evidence:

- Supported extensions include `.xosc`, `.xml`, `.json`, `.yaml`, `.yml`: `tools/build_scenario_index.py:21`
- Output fields include the required suggested fields plus `scenario_id`: `tools/build_scenario_index.py:22-32`
- XML, JSON, and YAML metadata extraction are separated into functions: `tools/build_scenario_index.py:97-210`
- Output paths are `scenario_index.csv` and `scenario_index.md`: `tools/build_scenario_index.py:288-291`
- Error handling for missing/non-directory input: `tools/build_scenario_index.py:277-282`

Verification result:

- Command succeeded.
- Output CSV contained one synthetic XOSC scenario and detected three parameters.

Gap:

- No blocking gap. Markdown output now includes `file_path` and `detected_parameters`.

#### `extract_xosc_params.py`

Evidence:

- Extracts `ParameterDeclaration`: `tools/extract_xosc_params.py:83-86`
- Extracts storyboard/story/act/maneuver/event names where present: `tools/extract_xosc_params.py:87-90`
- Extracts entity names from `ScenarioObject` and `EntitySelection`: `tools/extract_xosc_params.py:91-94`
- Writes `reports/xosc_parameter_summary.csv` by default: `tools/extract_xosc_params.py:33-37`
- Handles missing input and XML parse/read errors: `tools/extract_xosc_params.py:95-130`

Verification result:

- Command succeeded.
- Output found 3 parameters, story/act/maneuver/event names, and 2 entities from `examples/minimal_aeb_scenario.xosc`.

Gap:

- No blocking gap.

#### `run_esmini_batch.py`

Evidence:

- Supports `--input`: `tools/run_esmini_batch.py:20-25`
- Supports `--esmini-path`: `tools/run_esmini_batch.py:26-30`
- Supports `--dry-run`: `tools/run_esmini_batch.py:31-36`
- Supports `--output-log-dir`: `tools/run_esmini_batch.py:37-42`
- Builds command lines without executing esmini: `tools/run_esmini_batch.py:109-119`
- Writes run plan Markdown: `tools/run_esmini_batch.py:122-149`
- Creates log directories: `tools/run_esmini_batch.py:162-168`

Verification result:

- Command succeeded.
- It generated two planned esmini commands and created `/tmp/adas_audit_logs/SCN-001` and `/tmp/adas_audit_logs/SCN-002`.

Gap:

- The script is dry-run only. This is consistent with the requested minimal version, but it should remain documented if users expect real execution.

#### `export_result_summary.py`

Evidence:

- Accepts scenario index/list, result CSV, and issue CSV: `tools/export_result_summary.py:27-51`
- Merges scenario rows, result rows, and issue rows by scenario ID: `tools/export_result_summary.py:85-132`
- Computes issue counts and closure status: `tools/export_result_summary.py:97-128`
- Writes CSV and Markdown summaries: `tools/export_result_summary.py:135-182`

Verification result:

- Command succeeded.
- Output summary reported 2 result rows, 1 pass, 1 fail, and 1 open linked issue.

Gap:

- The current merge is intentionally minimal and assumes simple CSV schemas. This is acceptable for the requested minimum version.

### 6. Template File Audit

Status: **Pass**

Required templates exist:

- `templates/test_execution_record.md`
- `templates/issue_tracking_template.csv`
- `templates/regression_verification_record.md`
- `templates/regulation_to_scenario_review.md`
- `templates/test_day_checklist.md`

Coverage assessment:

| Required element | Evidence |
| --- | --- |
| Pre-test checks | `templates/test_execution_record.md`, `templates/test_day_checklist.md`, `templates/regression_verification_record.md` |
| Scenario information | `templates/test_execution_record.md`, `templates/regulation_to_scenario_review.md` |
| Version information | `templates/test_execution_record.md`, `templates/regression_verification_record.md` |
| Environment conditions | `templates/test_execution_record.md`, `templates/test_day_checklist.md` |
| Execution record | `templates/test_execution_record.md`, `templates/test_day_checklist.md`, `templates/regression_verification_record.md` |
| Abnormal observations | `templates/test_execution_record.md`, `templates/issue_tracking_template.csv` |
| Responsibility domain | `templates/issue_tracking_template.csv`, `templates/regression_verification_record.md` |
| Closure status | `templates/issue_tracking_template.csv`, `templates/test_execution_record.md`, `templates/regression_verification_record.md` |
| Regression result | `templates/issue_tracking_template.csv`, `templates/regression_verification_record.md` |

Assessment:

- The templates are realistic for lightweight test workflow management.
- They are suitable for explaining test traceability and issue closure in an interview.
- Structure is clear and not overloaded.

Recommended fix:

- Optional: add a template usage order document later.

### 7. Example Data Audit

Status: **Pass**

Evidence:

- Required example CSVs exist:
  - `examples/example_scenario_list.csv`
  - `examples/example_result_input.csv`
  - `examples/example_issue_log.csv`
- Synthetic scenario file exists:
  - `examples/minimal_aeb_scenario.xosc`

Verification result:

- `example_scenario_list.csv` drives `run_esmini_batch.py`.
- `example_result_input.csv` and `example_issue_log.csv` drive `export_result_summary.py`.
- `minimal_aeb_scenario.xosc` drives indexing and parameter extraction.

Assessment:

- Examples are minimal but sufficient.
- No evidence suggests the synthetic XOSC file was copied from a third-party repository.

Gap:

- Two scenario IDs point to the same synthetic XOSC file. This is acceptable for a compact demo but limits demonstration depth.

Recommended fix:

- Optional: add a second distinct synthetic scenario if broader demo coverage is needed.

### 8. License and Boundary Audit

Status: **Pass**

Evidence:

- `LICENSE` exists and uses MIT.
- `LICENSE-NOTICE.md:3-31` separates original content from upstream content and states that no full upstream scenario library, simulator source tree, ASAM standard text, or schema package is redistributed.
- `third_party/README.md:3-5` states that external checkouts should remain outside the repo or in ignored local directories.
- `.gitignore:17-19` ignores `third_party/*/` while allowing `third_party/README.md`.
- `requirements.txt` contains no runtime dependency list because the scripts use Python standard library only.

Suspicious copy scan:

No suspicious third-party copy was found.

| Suspicious file path | Reason | Risk | Recommendation |
| --- | --- | --- | --- |
| None found | `third_party/` contains only reference documentation; no large source/vendor directories found. | Low | Continue keeping upstream checkouts ignored or external. |

Gaps:

- Unable to verify future user-added local upstream checkouts.
- Unable to provide legal advice on upstream license sufficiency.

Recommended fix:

- Keep upstream license files and commit hashes with any local or downstream use of upstream scenario content.

## README Claim Verification

| README claim | Evidence | Status |
| --- | --- | --- |
| Personal engineering repository for ADAS homologation and NCAP scenario validation | `README.md:3-5` and repository structure | Pass |
| Does not redistribute third-party scenario libraries | `README.md:5`, `third_party/README.md:3-5`, `LICENSE-NOTICE.md:20-25` | Pass |
| Scenario mapping exists | `scenario_map/*.csv`, `scenario_map/field_definition.md` | Pass |
| Scenario indexing exists | `tools/build_scenario_index.py`; audit command succeeded | Pass |
| Parameter extraction exists | `tools/extract_xosc_params.py`; audit command succeeded | Pass |
| esmini dry-run planning exists | `tools/run_esmini_batch.py`; audit command succeeded | Pass |
| Result summary exists | `tools/export_result_summary.py`; audit command succeeded | Pass |
| Test records and closure templates exist | `templates/` | Pass |
| Future CI is planned | `README.md:192` | Pass as future item; not implemented |

## Gaps and Recommended Fixes

| Priority | Gap | Impact | Recommended fix |
| --- | --- | --- | --- |
| Low | `run_esmini_batch.py` remains dry-run only. | This is acceptable for the current minimal version but should not be confused with full simulator automation. | Add real execution mode later only when esmini installation, return codes, and log validation are handled. |
| Low | Example data has two scenario IDs pointing to one synthetic XOSC file. | Demonstration is valid but narrow. | Add a second synthetic scenario when demonstrating multi-scenario indexing. |

## Final Verdict

**Ready to publish**

Reasoning:

- Project positioning is clear and matches the requested ADAS homologation / NCAP scenario engineering direction.
- Engineering structure is solid for a personal portfolio repository.
- Documentation is credible and avoids claiming official certification evidence.
- Toolchain forms a minimal but working loop: map, index, extract, plan, summarize, and close issues.
- Personal project ownership is clear because the repository contributes workflow structure, scripts, templates, and documentation rather than copying upstream assets.
- Interview value is sufficient: the README and templates provide a concrete story around traceability, execution planning, and issue closure.

Publication can proceed. The remaining gaps are refinements, not blockers.
