# Methodology

This document explains the engineering logic behind the toolkit. It is intentionally focused on scenario workflow structure, not on reproducing full regulation text.

## Why Regulation Tests Need Scenario Representation

Regulations and consumer test protocols describe required behavior in human-readable form. Engineering teams need to turn that intent into repeatable test cases with controlled actors, road geometry, timing, speed ranges, target types, and pass criteria.

Scenario representation helps separate three concerns:

- Test intent: what behavior is being evaluated.
- Test setup: actors, road, trigger condition, and parameter range.
- Test evidence: measured outputs, pass/fail decision, and review notes.

Without a scenario layer, test planning often depends on scattered documents and manual interpretation. That makes regression, coverage review, and issue closure harder to defend.

## Why Map Regulation Items to Scenarios

A regulation or protocol item is rarely identical to one simulator file or one proving-ground run. One item may require multiple scenario variants. One scenario may also support multiple protocol interpretations when the parameter set changes.

A mapping table makes these relationships explicit:

- Which protocol item motivated the scenario.
- Which scenario file or implementation is used.
- Which parameters are critical for traceability.
- Which expected behavior and pass criteria are being checked.
- Which data should be recorded for later review.

This mapping is not a substitute for the official protocol. It is an engineering control document that makes the test workflow easier to audit.

## Why Connect Proving-Ground Tests and Simulation Scenarios

Physical proving-ground tests and simulation scenarios answer different questions. Proving-ground tests provide direct evidence under controlled real-world conditions. Simulation helps prepare cases, explore parameter variation, reproduce issues, and perform regression checks before another physical test slot is used.

A useful workflow connects both sides:

- Use protocol mapping to define the scenario intent.
- Use simulation scenarios to prepare and vary the case.
- Use proving-ground records to capture real execution conditions.
- Use result summaries to compare expected behavior, observed behavior, and follow-up actions.

The goal is not to claim that simulation automatically replaces physical validation. The goal is to build a consistent workflow where both sources of evidence can be traced to the same scenario intent.

## Why Result Summary and Issue Closure Matter

Scenario execution is incomplete if the result is only a log file or a simulator screenshot. A useful validation workflow must also answer:

- Was the scenario executed with the expected software, hardware, map, and environment versions?
- Did the observed behavior meet the defined pass criteria?
- If it failed, which issue was opened and who owns it?
- Was the fix verified with the same scenario or an equivalent regression case?
- Is the closure decision supported by recorded evidence?

For this reason, the toolkit includes templates and result aggregation scripts. They keep the workflow connected from test intent to issue closure instead of stopping at scenario playback.
