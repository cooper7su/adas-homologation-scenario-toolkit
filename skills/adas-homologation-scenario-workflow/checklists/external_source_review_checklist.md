# External Source Review Checklist

Use this checklist before scanning, summarizing, or referencing an upstream scenario repository or simulator project.

| Review Item | Required | Evidence / Notes |
| --- | --- | --- |
| Upstream repository name and URL identified | Yes |  |
| Local checkout path is outside the toolkit or under ignored `third_party/*/` | Yes |  |
| Commit SHA or release tag recorded | Yes |  |
| License statement reviewed from upstream | Yes |  |
| Role matches `third_party_manifest.yaml` | Yes |  |
| Allowed integration mode confirmed | Yes |  |
| Non-copied boundary reviewed | Yes |  |
| No upstream `.xosc`, `.xodr`, catalog, variation, schema, source, binary, or generated road network staged | Yes |  |
| `templates/external_source_review.md` prepared or updated | Recommended |  |
| Scenario index generated to `/tmp` | Recommended |  |
| Parameter extraction generated to `/tmp` | Recommended |  |
| XML validation generated to `/tmp` | Recommended |  |
| XSD validation skipped unless user supplied authorized schema | Yes |  |
| esmini dry-run used unless user explicitly requested execution | Yes |  |
| Derived metadata labeled as external metadata, not official evidence | Yes |  |

中文说明：外部库接入前必须确认 URL、commit、license、路径和不复制边界。
