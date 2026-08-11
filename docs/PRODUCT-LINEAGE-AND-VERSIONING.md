# P5 Archive Manager product lineage and versioning

Status: **adopted 2026-08-11**

P5 Archive Manager has two separately installed implementations:

| Application | Transport | Release line | Status |
| --- | --- | --- | --- |
| P5 Archive Manager CLI | Archiware `nsdchat` | 3.x | Supported; may continue where CLI-specific capabilities are useful |
| P5 Archive Manager API | Archiware P5 REST API | 4.x | Primary focus for new development |

The API app is the recommended successor in the product lineage, but it is not an
in-place conversion of the CLI app. The applications retain separate names, bundle
identifiers, settings, workflows, and behaviour. Both may be installed during evaluation
or migration.

Versions use three numeric components and public tags include the build, for example
`4.0.0+25`. GitHub's prerelease state identifies beta builds. CLI updates match only
`3.x`; API updates match `4.x` after transition. The final API bridge `0.10.1+24`
temporarily matches both API `0.x` and `4.x` so existing API users can discover v4.

Public asset names identify the implementation explicitly:

- `P5-Archive-Manager-API-4.0.0.dmg`
- `P5-Archive-Manager-CLI-3.7.2.dmg`
