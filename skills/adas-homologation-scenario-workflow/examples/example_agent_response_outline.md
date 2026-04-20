# Example Agent Response Outline

Use this outline for concise final responses after completing a workflow task.

## Completed Work

- Read the repository workflow docs and skill instructions.
- Confirmed third-party source boundaries against `third_party_manifest.yaml`.
- Ran scenario indexing, parameter extraction, XML validation, esmini dry-run planning, and result summary commands with outputs under `/tmp`.
- Prepared review/report artifacts using repository templates.

## Key Results

- Scenario-like files indexed: `<count>`
- XOSC/XML files inspected: `<count>`
- XML well-formedness: `<pass/fail/partial>`
- XSD validation: `<not run; no schema supplied>` or `<result>`
- esmini mode: `dry-run` unless explicitly executed
- Linked open issues: `<count>`

## Evidence Classification

- Synthetic evidence: `<repo example files or demo records>`
- External metadata: `<derived index/parameter/validation files>`
- Official evidence: `<none unless supplied by user-approved authority>`

## Boundaries Observed

- No third-party scenario files, simulator binaries, schemas, or standards text were committed.
- External checkout path remained outside the main repository or under ignored `third_party/*/`.

## Verification

- `python3 -B -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in sorted(pathlib.Path('tools').glob('*.py'))]"`
- `git status --short --ignored`

## Final Notes

State limitations plainly: the workflow supports engineering traceability and demo reporting; it does not replace official homologation review.

中文说明：最终回复应简洁列出完成项、验证结果、边界和限制，不夸大为官方认证结论。
