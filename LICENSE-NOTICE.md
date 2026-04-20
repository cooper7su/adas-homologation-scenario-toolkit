# License Notice

This repository contains original workflow documentation, templates, and Python utilities for scenario-based ADAS homologation workflow management. Unless otherwise stated, original content in this repository is licensed under the MIT License.

## Third-Party Boundaries

This repository references upstream projects for scenario sources, simulator execution, or implementation comparison. It does not vendor full third-party repositories, scenario libraries, simulator source trees, ASAM standards, or proprietary tool content.

Users are responsible for reviewing and complying with the upstream license terms before copying, modifying, executing, or redistributing upstream content.

## Referenced Upstream Projects

| Upstream project | Role in this repository | License note |
| --- | --- | --- |
| openMSL/sl-3-1-osc-alks-scenarios | External ALKS-oriented OpenSCENARIO scenario source reference | Upstream states that the corresponding OpenSCENARIO bundle is licensed under MPL-2.0. It also references ASAM schema license terms and Apache-2.0 components for checker tooling. |
| vectorgrp/OSC-NCAP-scenarios | External NCAP OpenSCENARIO/OpenDRIVE scenario source reference | Upstream states that its OpenSCENARIO XML and OpenDRIVE files are licensed under MPL-2.0, with ASAM schema license terms applying to schemas. |
| esmini/esmini | Candidate OpenSCENARIO player and execution backend | Upstream repository is marked as MPL-2.0 licensed. |
| BeamNG/BeamNG_NCAP_Tests | BeamNG.tech NCAP test implementation reference | Upstream repository is marked as MIT licensed. BeamNG.tech itself has separate product terms. |

## What Is Not Included

- No full upstream scenario library is copied into this repository.
- No simulator binaries or simulator source trees are included.
- No ASAM standard text or schema package is redistributed here.
- No claim is made that generated reports are official homologation evidence.

## Attribution Practice

When using upstream files in local experiments, keep the original repository URL, commit hash or release tag, license file, and any required attribution with the local copy or downstream report.

For publication, commercial usage, certification programs, or customer delivery, verify license obligations from the upstream source and from the relevant standard or protocol owner.
