# Third-Party Integration Notes

This directory documents how external scenario repositories, simulators, and implementation references can be connected to this toolkit. The main repository keeps only references and adapter assumptions. It does not copy full upstream repositories into source control.

For local experiments, users may place external checkouts outside this repository, or use ignored subdirectories under `third_party/` when appropriate. If an upstream checkout is used, keep its license file and source URL with the local copy.

See also:

- `third_party_manifest.yaml` for structured upstream metadata and integration boundaries.
- `docs/upstream_integration_workflow.md` for the recommended external checkout workflow.
- `examples/external_sources.example.yaml` for placeholder local path configuration.

## openMSL/sl-3-1-osc-alks-scenarios

- Repository: `openMSL/sl-3-1-osc-alks-scenarios`
- URL: <https://github.com/openMSL/sl-3-1-osc-alks-scenarios>
- Main purpose: Provides an ALKS scenario interpretation using OpenSCENARIO.
- Role in this project: External scenario source reference for ALKS-oriented scenario indexing and mapping experiments.
- Category: Scenario library reference.
- License notes: The upstream repository states that its corresponding OpenSCENARIO bundle is licensed under MPL-2.0. It also references ASAM schema license terms and Apache-2.0 checker-related components.
- Integration approach: Keep a local checkout outside this repository or in an ignored `third_party/` subdirectory. Use `tools/build_scenario_index.py` and `tools/extract_xosc_params.py` against that checkout path.
- Not copied here: Upstream `.xosc`, `.xodr`, validation tooling, schemas, CI configuration, and full repository history.

## vectorgrp/OSC-NCAP-scenarios

- Repository: `vectorgrp/OSC-NCAP-scenarios`
- URL: <https://github.com/vectorgrp/OSC-NCAP-scenarios>
- Main purpose: Provides Euro NCAP-oriented scenarios modelled with ASAM OpenSCENARIO XML and OpenDRIVE.
- Role in this project: External scenario source reference for NCAP catalog review, scenario indexing, and parameter extraction.
- Category: Scenario library reference.
- License notes: The upstream repository states that its OpenSCENARIO XML and OpenDRIVE files are licensed under MPL-2.0. It also notes that ASAM schema files are governed by ASAM license terms.
- Integration approach: Keep a local checkout outside this repository or in an ignored `third_party/` subdirectory. Run the indexing and extraction tools against the checkout and keep generated summaries in `reports/`.
- Not copied here: Upstream OpenSCENARIO files, OpenDRIVE files, catalog files, generated road networks, schemas, and protocol-derived scenario tables.

## esmini/esmini

- Repository: `esmini/esmini`
- URL: <https://github.com/esmini/esmini>
- Main purpose: Provides a basic OpenSCENARIO player and related applications for scenario playback, OpenDRIVE visualization, and replay workflows.
- Role in this project: Candidate execution backend for OpenSCENARIO dry-run planning and future execution adapters.
- Category: Execution backend.
- License notes: The upstream repository is marked as MPL-2.0 licensed. Users should verify binary distribution and dependency obligations before redistribution.
- Integration approach: Install or build esmini separately. Point `tools/run_esmini_batch.py` to the local executable through `--esmini-path`.
- Not copied here: esmini source code, binaries, build scripts, dependencies, examples, and test suites.

## BeamNG/BeamNG_NCAP_Tests

- Repository: `BeamNG/BeamNG_NCAP_Tests`
- URL: <https://github.com/BeamNG/BeamNG_NCAP_Tests>
- Main purpose: Implements selected NCAP test workflows for BeamNG.tech using the BeamNG Python API.
- Role in this project: Implementation reference for simulator-specific NCAP workflow design and result recording concepts.
- Category: Test implementation reference.
- License notes: The upstream repository is marked as MIT licensed. BeamNG.tech itself is a separate product with its own license and usage terms.
- Integration approach: Use as a reference for how simulator-specific NCAP tests are structured. Any BeamNG.tech execution should live in a separate adapter or project environment.
- Not copied here: Python implementation files, BeamNG scenario assets, simulator-specific setup scripts, and BeamNG.tech product content.

## Recommended Local Layout

```text
external-workspace/
├── sl-3-1-osc-alks-scenarios/
├── OSC-NCAP-scenarios/
├── esmini/
└── BeamNG_NCAP_Tests/

adas-homologation-scenario-toolkit/
└── tools/
```

The toolkit can then be run against external paths without bringing upstream source trees into this repository.
