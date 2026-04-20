# ADAS Homologation Scenario Toolkit / ADAS 法规认证场景工程工具箱

English | [中文说明](#中文说明)

`adas-homologation-scenario-toolkit` is a personal engineering repository for ADAS homologation, proving-ground testing, certification testing, and NCAP-oriented scenario validation workflows.

The repository does not attempt to publish a complete legal interpretation database or redistribute full third-party scenario libraries. Its focus is the engineering layer between public regulations or protocols and repeatable scenario-based testing:

```text
regulation/protocol
        |
        v
scenario mapping
        |
        v
scenario indexing and parameter extraction
        |
        v
execution wrapper
        |
        v
result summary
        |
        v
issue closure and regression verification
```

A companion Codex Skill is maintained in a separate repository: [adas-homologation-scenario-workflow-skill](https://github.com/cooper7su/adas-homologation-scenario-workflow-skill). The skill guides future AI agents through this toolkit's workflow using the repository's tools, templates, examples, and third-party boundary rules. It does not include third-party scenario files, regulation full text, schema packages, or simulator binaries.

## Why This Project Exists

ADAS validation work often crosses several boundaries: public protocols, scenario descriptions, simulation tools, proving-ground execution records, and issue tracking. In many teams, these artifacts are handled in separate spreadsheets, simulator projects, and test reports.

This project demonstrates a practical method to connect those artifacts without claiming ownership of third-party standards, scenario libraries, or simulators. It is designed as a portfolio-ready repository that shows how to structure scenario-based homologation work in a traceable and automatable way.

## Problems Addressed

- Map regulation or protocol items to scenario-level test intent.
- Index scenario files from external repositories or local workspaces without copying them into this repository.
- Extract basic OpenSCENARIO parameters for review and coverage tracking.
- Validate OpenSCENARIO/XML well-formedness and optionally validate against a user-provided XSD schema.
- Generate dry-run execution plans or guarded execution summaries for esmini-based scenario playback.
- Merge execution results, scenario metadata, and issue logs into summary reports.
- Provide practical templates for test-day records, issue closure, and regression verification.
- Document upstream integration boundaries through a manifest and external checkout workflow.

## Architecture

```text
+------------------------+
| Regulation / Protocol  |
| UNECE, NCAP, internal  |
+-----------+------------+
            |
            v
+------------------------+       +-------------------------+
| scenario_map/          |       | third_party/            |
| mapping templates      |<----->| upstream integration    |
+-----------+------------+       | notes and boundaries    |
            |                    +-------------------------+
            v
+------------------------+
| tools/                 |
| index, extract, plan,  |
| summarize              |
+-----------+------------+
            |
            v
+------------------------+       +-------------------------+
| reports/               |<----->| templates/              |
| generated CSV/Markdown |       | execution and closure   |
+------------------------+       +-------------------------+
```

## Repository Structure

```text
.
├── assets/              # Reserved for diagrams or lightweight project assets
├── docs/                # Methodology notes
├── examples/            # Small self-contained example inputs
├── reports/             # Generated reports, ignored except .gitkeep
├── scenario_map/        # Regulation-to-scenario mapping templates
├── templates/           # Test execution, issue, and regression templates
├── third_party/         # Upstream project references and integration boundaries
├── tools/               # Python workflow utilities
└── third_party_manifest.yaml
```

## Main Capabilities

### 1. Regulation-to-Scenario Mapping

The files in `scenario_map/` define a compact schema for connecting a regulation family, protocol, scenario identity, trigger condition, expected behavior, pass criteria, and data to record. The goal is not to rewrite the regulation, but to capture the engineering interpretation required to prepare a test case.

### 2. Scenario Indexing

`tools/build_scenario_index.py` scans a directory for `.xosc`, `.xml`, `.json`, `.yaml`, and `.yml` files and writes a unified scenario index to:

- `reports/scenario_index.csv`
- `reports/scenario_index.md`

It is intended for local copies, submodule checkouts, or simulator project folders that are kept outside this repository.

### 3. OpenSCENARIO Parameter Extraction

`tools/extract_xosc_params.py` parses OpenSCENARIO XML files and extracts:

- `ParameterDeclaration` entries
- storyboard or story-level names where present
- entity names from `ScenarioObject` and `EntitySelection`

Output:

- `reports/xosc_parameter_summary.csv`

### 4. esmini Batch Planning

`tools/run_esmini_batch.py` reads a scenario list and generates a dry-run execution plan for esmini. Dry-run is the default mode. If `--execute` is provided, the script checks that `--esmini-path` resolves to an executable, runs each planned command, captures return codes, and writes execution summary files.

Output:

- `reports/run_plan.md`
- per-scenario log directory placeholders under `logs/`
- `reports/esmini_execution_summary.csv` and `.md` when `--execute` is used

### 5. OpenSCENARIO Validation

`tools/validate_xosc_schema.py` validates `.xosc` and `.xml` files. By default it performs XML well-formedness checks. If users provide `--schema` and install optional `lxml`, it can also perform XSD validation.

Output:

- `reports/xosc_validation_report.csv`
- `reports/xosc_validation_report.md`

### 6. Result Summary and Closure

`tools/export_result_summary.py` combines scenario metadata, result input, and issue records into:

- `reports/result_summary.csv`
- `reports/result_summary.md`

The summary highlights pass/fail status, open issue count, and closure status.

### 7. Upstream Integration Manifest

`third_party_manifest.yaml` records each referenced upstream repository, its role, license boundary, recommended local path, allowed integration mode, and content that must not be copied into this repository.

`docs/upstream_integration_workflow.md` explains how to keep upstream checkouts outside the main repository and run this toolkit against those external paths.

`docs/external_source_scan_example.md` records a local smoke-test pattern for scanning a real external scenario library path without committing upstream files.

### 8. End-to-End Synthetic Demo

`docs/demo_walkthrough.md` shows a complete synthetic workflow:

```text
regulation item -> scenario -> execution plan -> result -> issue -> regression
```

The demo uses only local synthetic files and does not copy third-party scenario content.

### 9. Companion Codex Skill for AI Agents

[adas-homologation-scenario-workflow-skill](https://github.com/cooper7su/adas-homologation-scenario-workflow-skill) turns this repository's methodology into a reusable Codex Skill. It instructs future AI agents to:

- read the existing repository documentation before acting,
- use `tools/` scripts for workflow automation,
- use `templates/` and `scenario_map/` for traceable records,
- apply `third_party_manifest.yaml` and license-boundary notes before external integration,
- default to dry-run behavior for esmini,
- keep third-party scenario libraries, standards text, schema packages, and simulator binaries out of the main repository,
- label generated evidence as synthetic, external metadata, or official evidence.

The skill is maintained outside this main toolkit repository. It is a workflow guide only and does not redistribute third-party content or official regulation text.

## Third-Party Project Integration

This repository references the following upstream projects as external inputs or integration targets:

- [openMSL/sl-3-1-osc-alks-scenarios](https://github.com/openMSL/sl-3-1-osc-alks-scenarios): ALKS-oriented OpenSCENARIO interpretation.
- [vectorgrp/OSC-NCAP-scenarios](https://github.com/vectorgrp/OSC-NCAP-scenarios): NCAP scenarios modelled with ASAM OpenSCENARIO XML and OpenDRIVE.
- [esmini/esmini](https://github.com/esmini/esmini): OpenSCENARIO player used as a possible execution backend.
- [BeamNG/BeamNG_NCAP_Tests](https://github.com/BeamNG/BeamNG_NCAP_Tests): BeamNG.tech NCAP test implementation reference.

Integration is intentionally reference-based. This repository may point to local checkouts, submodule locations, or external simulator projects, but it does not vendor complete upstream scenario libraries or simulator source trees.

See `third_party/README.md` and `LICENSE-NOTICE.md` for boundary notes.

## License Boundaries

The original content in this repository is released under the MIT License unless otherwise stated.

Third-party repositories, standards, schemas, scenario files, and simulator code remain under their own licenses and terms. This repository does not change those licenses and does not provide legal advice. Before using upstream assets in commercial, academic, or publication work, verify the upstream license and attribution requirements directly from the source repository or standard owner.

## Implemented Content

- Repository structure for scenario engineering workflow.
- Mapping and catalog templates under `scenario_map/`.
- Methodology document under `docs/`.
- Third-party integration boundary document under `third_party/`.
- Upstream integration manifest and external checkout workflow documentation.
- Python utilities for indexing, OpenSCENARIO parameter extraction, XOSC validation, esmini dry-run or guarded execution, and result summary export.
- Test execution, issue tracking, review, checklist, external source review, and regression templates.
- Small synthetic example data under `examples/`.
- Synthetic end-to-end demo artifacts and a sample summary report.
- A companion Codex Skill maintained separately at [adas-homologation-scenario-workflow-skill](https://github.com/cooper7su/adas-homologation-scenario-workflow-skill).
- A minimal GitHub Actions workflow that validates Python syntax and runs the example workflow.

## Example Usage

Build an index from the synthetic example scenario:

```bash
python3 tools/build_scenario_index.py examples
```

Extract OpenSCENARIO parameters:

```bash
python3 tools/extract_xosc_params.py examples
```

Validate OpenSCENARIO/XML well-formedness:

```bash
python3 tools/validate_xosc_schema.py --input examples
```

Generate an esmini dry-run plan:

```bash
python3 tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run
```

Execute with esmini only after installing it separately:

```bash
python3 tools/run_esmini_batch.py \
  --input examples/example_scenario_list.csv \
  --esmini-path /path/to/esmini \
  --execute
```

Export a result summary:

```bash
python3 tools/export_result_summary.py \
  --scenario-index examples/example_scenario_list.csv \
  --results examples/example_result_input.csv \
  --issues examples/example_issue_log.csv
```

Review the full synthetic demo workflow:

```bash
cat docs/demo_walkthrough.md
```

## Future Extensions

- Add richer OpenSCENARIO and OpenDRIVE metadata extraction.
- Add adapter profiles for esmini, BeamNG.tech, and other simulation backends.
- Add report templates aligned with specific internal test review gates.
- Expand CI checks for template consistency and report schema validation.
- Add optional submodule instructions for users who want to keep upstream scenario repositories outside the main source tree.

## 中文说明

`adas-homologation-scenario-toolkit` 是一个面向 ADAS 法规测试场、认证测试和 NCAP 场景验证的个人工程方法仓库。

它不是法规知识大全，也不是完整仿真器或第三方场景库集合。这个仓库的重点是把公开法规/协议、外部场景库、执行工具、测试记录、结果汇总和问题闭环连接成一个清晰、可验证、适合面试展示的工程流程。

核心工作流：

```text
法规/协议
    |
    v
场景映射
    |
    v
场景索引与参数提取
    |
    v
执行封装
    |
    v
结果汇总
    |
    v
问题闭环与回归验证
```

### 为什么做这个项目

ADAS 测试工作通常会横跨法规协议、场景文件、仿真工具、测试场执行记录、问题跟踪和回归验证。很多信息容易分散在 Excel、仿真工程、日志目录和测试报告里。

本项目展示的是一个工程化整理方法：不声称拥有第三方标准、场景库或仿真器，而是在它们之间建立可追踪、可复用、可自动化的工作流。

### 这个项目解决什么问题

- 将法规或 NCAP 协议条目映射到可执行的测试场景意图。
- 对外部场景库或本地场景目录进行索引，而不把第三方整库复制进本仓库。
- 提取 OpenSCENARIO 文件中的参数、Storyboard 名称和 Entity 名称。
- 对 `.xosc` / `.xml` 做基础 XML 合法性检查，并支持用户自带 XSD schema 做可选验证。
- 生成 esmini dry-run 执行计划，也支持受保护的 `--execute` 执行模式。
- 汇总执行结果、场景信息和 issue log，输出 CSV / Markdown 报告。
- 提供测试记录、问题闭环、外部源审查和回归验证模板。

### 仓库结构

```text
.
├── assets/              # 图表或轻量资源预留
├── docs/                # 方法论、demo 和上游接入流程
├── examples/            # 最小化 synthetic 示例数据
├── reports/             # 生成报告目录，默认忽略生成物
├── scenario_map/        # 法规到场景映射模板
├── templates/           # 测试记录、issue、回归和外部源审查模板
├── third_party/         # 第三方项目引用和边界说明
├── tools/               # Python 工作流工具
└── third_party_manifest.yaml
```

### 主要能力

1. **法规到场景映射**  
   `scenario_map/` 中的 CSV 模板用于记录 regulation family、protocol name、scenario ID、关键参数、触发条件、预期行为、通过标准、记录数据和上游引用。

2. **场景索引**  
   `tools/build_scenario_index.py` 扫描 `.xosc`、`.xml`、`.json`、`.yaml` 文件，生成统一索引：
   - `reports/scenario_index.csv`
   - `reports/scenario_index.md`

3. **OpenSCENARIO 参数提取**  
   `tools/extract_xosc_params.py` 提取：
   - `ParameterDeclaration`
   - Story / Act / Maneuver / Event 名称
   - `ScenarioObject` / `EntitySelection` 名称

4. **XOSC / XML 验证**  
   `tools/validate_xosc_schema.py` 默认执行 XML well-formedness 检查；如果用户提供 `--schema` 并安装可选依赖 `lxml`，可进行 XSD validation。

5. **esmini 执行封装**  
   `tools/run_esmini_batch.py` 默认生成 dry-run 命令计划。使用 `--execute` 时，会检查 `--esmini-path` 是否存在且可执行，并输出执行摘要。

6. **结果汇总与闭环**  
   `tools/export_result_summary.py` 将场景信息、执行结果和 issue 记录合并，输出结果摘要，并保留 open issue / closure status。

7. **上游接入规范**  
   `third_party_manifest.yaml` 和 `docs/upstream_integration_workflow.md` 说明如何把 openMSL、Vector、esmini、BeamNG 等上游项目放在仓库外部，通过本仓库工具扫描和引用。

8. **完整 synthetic demo**  
   `docs/demo_walkthrough.md` 展示：

   ```text
   法规条目 -> 场景 -> 执行计划 -> 结果 -> issue -> regression
   ```

   demo 使用本仓库自造的 synthetic 示例，不复制第三方真实场景文件。

9. **配套 Codex Skill**  
   [adas-homologation-scenario-workflow-skill](https://github.com/cooper7su/adas-homologation-scenario-workflow-skill) 将本仓库的方法论、工具链、模板、第三方边界和 demo 工作流沉淀成可复用的 AI 代理执行指南。它指导 Codex 优先读取现有文档，调用 `tools/`，使用 `templates/` 和 `scenario_map/`，通过 `third_party_manifest.yaml` 判断外部接入边界，并默认使用 esmini dry-run。

   该 Skill 已拆分到独立仓库，不包含第三方场景文件、法规全文、ASAM schema 包或仿真器二进制。

### 第三方项目如何接入

本仓库参考并对接以下上游项目，但不直接复制完整源码或场景库：

- [openMSL/sl-3-1-osc-alks-scenarios](https://github.com/openMSL/sl-3-1-osc-alks-scenarios)：ALKS OpenSCENARIO 场景参考。
- [vectorgrp/OSC-NCAP-scenarios](https://github.com/vectorgrp/OSC-NCAP-scenarios)：Euro NCAP OpenSCENARIO / OpenDRIVE 场景参考。
- [esmini/esmini](https://github.com/esmini/esmini)：OpenSCENARIO 执行后端候选。
- [BeamNG/BeamNG_NCAP_Tests](https://github.com/BeamNG/BeamNG_NCAP_Tests)：BeamNG.tech NCAP 测试实现参考。

推荐做法是将这些仓库 clone 到主仓库外部，例如：

```text
external-workspace/
├── sl-3-1-osc-alks-scenarios/
├── OSC-NCAP-scenarios/
├── esmini/
└── BeamNG_NCAP_Tests/
```

然后用本仓库工具对外部路径进行索引、参数提取、验证和执行计划生成。

### 许可证和边界

本仓库原创内容默认使用 MIT License。

第三方仓库、标准、schema、场景文件和仿真器代码仍然遵循各自许可证和使用条款。本仓库不改变这些许可证，也不提供法律意见。任何商业、科研、发布或认证用途，都应直接核对上游许可证和标准所有者要求。

本仓库明确不包含：

- 第三方完整场景库
- 仿真器源码或二进制
- ASAM 标准正文或 schema 包
- 官方认证测试结论

### 示例用法

构建 synthetic 示例索引：

```bash
python3 tools/build_scenario_index.py examples
```

提取 OpenSCENARIO 参数：

```bash
python3 tools/extract_xosc_params.py examples
```

验证 XML 合法性：

```bash
python3 tools/validate_xosc_schema.py --input examples
```

生成 esmini dry-run 执行计划：

```bash
python3 tools/run_esmini_batch.py --input examples/example_scenario_list.csv --dry-run
```

在单独安装 esmini 后执行：

```bash
python3 tools/run_esmini_batch.py \
  --input examples/example_scenario_list.csv \
  --esmini-path /path/to/esmini \
  --execute
```

生成结果汇总：

```bash
python3 tools/export_result_summary.py \
  --scenario-index examples/example_scenario_list.csv \
  --results examples/example_result_input.csv \
  --issues examples/example_issue_log.csv
```

查看完整 demo：

```bash
cat docs/demo_walkthrough.md
```

### 当前已实现内容

- 法规到场景映射模板
- 第三方接入 manifest
- 上游外部 checkout 工作流
- 场景索引工具
- OpenSCENARIO 参数提取工具
- XOSC / XML validation 工具
- esmini dry-run 与受保护执行模式
- 结果汇总工具
- 测试执行、issue、回归、外部源审查模板
- synthetic end-to-end demo
- 配套 Codex Skill 独立仓库：[adas-homologation-scenario-workflow-skill](https://github.com/cooper7su/adas-homologation-scenario-workflow-skill)
- GitHub Actions CI

### 后续扩展方向

- 增强 OpenDRIVE 元数据提取。
- 增加更多真实外部场景库的 metadata scan 示例。
- 针对 esmini、BeamNG.tech 等执行环境设计 adapter profile。
- 增加报告 schema consistency 检查。
- 增加更接近企业测试评审流程的报告模板。
