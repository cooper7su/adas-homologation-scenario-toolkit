# External Source Scan Example

This document records a local integration smoke test against an upstream scenario repository. It demonstrates how the toolkit can scan an external checkout without copying upstream scenario files into the main repository.

## Source

| Item | Value |
| --- | --- |
| Upstream repository | `vectorgrp/OSC-NCAP-scenarios` |
| URL | <https://github.com/vectorgrp/OSC-NCAP-scenarios> |
| Local checkout path used for smoke test | `/tmp/adas_external_sources/OSC-NCAP-scenarios` |
| Smoke-test commit | `ee7aa111386a47ada64b001338e688d9134a83b0` |
| Integration mode | External checkout only |
| License boundary | Upstream states that OpenSCENARIO XML and OpenDRIVE files are licensed under MPL-2.0, with ASAM schema license terms applying to schemas. Verify upstream terms before redistribution. |

## Commands

```bash
git clone --depth 1 https://github.com/vectorgrp/OSC-NCAP-scenarios.git /tmp/adas_external_sources/OSC-NCAP-scenarios

python3 tools/build_scenario_index.py \
  /tmp/adas_external_sources/OSC-NCAP-scenarios \
  --output-dir /tmp/adas_external_scan/index

python3 tools/extract_xosc_params.py \
  /tmp/adas_external_sources/OSC-NCAP-scenarios \
  --output /tmp/adas_external_scan/xosc_parameter_summary.csv

python3 tools/validate_xosc_schema.py \
  --input /tmp/adas_external_sources/OSC-NCAP-scenarios \
  --output-dir /tmp/adas_external_scan/validation
```

## Expected Use

The generated files under `/tmp/adas_external_scan/` are local metadata artifacts. They should be reviewed before any derived data is committed. Do not commit upstream `.xosc`, `.xodr`, catalog, variation, or schema files into this repository.

## Smoke-Test Result

The local smoke test completed successfully on the commit listed above.

| Check | Result |
| --- | --- |
| Repository cloned outside main repo | Pass |
| Scenario-like files indexed by toolkit | 138 |
| XOSC/XML files inspected by parameter extractor | 138 |
| XML well-formedness validations | 138 pass, 0 fail |
| XSD validation | Not run; no schema supplied |

## Review Notes

- This smoke test validates that the toolkit can operate on a real external checkout path.
- The default validation mode checks XML well-formedness only unless a schema is supplied.
- XSD validation requires a user-provided schema and the optional `lxml` package.
- Generated metadata is not official NCAP evidence and does not replace protocol review.
