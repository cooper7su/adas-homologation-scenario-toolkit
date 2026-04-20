# Scenario Mapping Field Definitions

The mapping CSV files in this directory are working templates. They are designed to capture traceability between a protocol item, scenario implementation, execution evidence, and review status.

| Field | Description |
| --- | --- |
| `regulation_family` | High-level regulation, protocol family, or internal validation program name. Examples: UNECE, NCAP, internal AEB regression. |
| `protocol_name` | Specific protocol, version, test group, or internal requirement set used as the source of test intent. |
| `scenario_id` | Stable project-level identifier. This should remain stable even if the underlying scenario file is renamed. |
| `scenario_name` | Human-readable scenario name. |
| `feature_domain` | ADAS function or validation domain, such as AEB, LSS, ACC, ALKS, VRU, or HMI warning. |
| `target_type` | Primary object or actor type, such as vehicle, pedestrian, bicyclist, motorcycle, lane marking, or static obstacle. |
| `road_type` | Road or proving-ground layout type, such as straight road, curve, intersection, lane change, or parking area. |
| `key_parameters` | Parameters that define the scenario variant, such as ego speed, target speed, overlap, headway, trigger timing, or weather. Use semicolon-separated values for readability. |
| `trigger_condition` | Condition that starts the relevant event or evaluation window. |
| `expected_behavior` | Intended system behavior under the mapped scenario. Keep this concise and measurable where possible. |
| `pass_criteria` | Pass/fail decision rule or reference to a detailed protocol rule. Avoid copying long official text. |
| `data_to_record` | Signals, logs, measurements, or artifacts that must be captured for review. |
| `upstream_reference` | Source repository, protocol reference, local scenario path, or simulator project reference. Include commit or version when available. |
| `remarks` | Open assumptions, review notes, known limitations, or owner comments. |

## Usage Notes

- Treat each row as an engineering mapping record, not as a legal restatement of a regulation.
- Keep protocol versions explicit.
- Prefer stable scenario IDs over file names for issue tracking.
- Record upstream repository URLs and commit hashes when using external scenario files.
- Keep parameter definitions short in the CSV and move detailed discussion to review notes or test records.
