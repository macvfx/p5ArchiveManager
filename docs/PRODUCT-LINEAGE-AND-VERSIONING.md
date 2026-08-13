# P5 Archive Manager product lineage and versioning

Status: **adopted 2026-08-11**

## Product relationship

P5 Archive Manager has two separately installed implementations:

| Application | Transport | Release line | Development status |
| --- | --- | --- | --- |
| P5 Archive Manager CLI | Archiware `nsdchat` | 3.x | Supported; development may continue where CLI-specific capabilities are useful |
| P5 Archive Manager API | Archiware P5 REST API | 4.x | Primary focus for new development |

The API app is the recommended successor in the product lineage, but it is not an
in-place conversion of the CLI app. The applications retain separate names, bundle
identifiers, settings, workflows, and behaviour. Both may be installed while an operator
evaluates or migrates.

## Version policy

- Versions use three numeric components: `major.minor.patch`.
- Build numbers are separate monotonically increasing integers within each app.
- Public tags use `version+build`, for example `4.0.0+25`.
- GitHub's prerelease state, rather than a suffix in the tag, identifies beta builds.
- CLI updates match only `3.x`; API updates match `4.x` after the transition.
- The final API bridge `0.10.1+24` temporarily matches both API `0.x` and `4.x` so
  existing API users can discover the new release line.

## Transition sequence

1. Publish API `0.10.1+24` as the final 0.x bridge.
2. Preserve older API release metadata and binaries, then retire their GitHub Release
   objects while retaining source tags.
3. Publish API `4.0.0+25` as a prerelease until its acceptance gates are complete.
   ✅ Done 2026-08-13. From this build the app's own update pattern matches `4.x` only;
   the `0.10.1+24` bridge continues to match both lines so installed bridge copies can
   discover it.
4. Keep API and CLI assets unambiguous, for example
   `P5-Archive-Manager-API-4.0.0.dmg` and `P5-Archive-Manager-CLI-3.7.2.dmg`.

## User communication

The CLI app tells users that API 4 is the recommended, more portable REST implementation
and that its operation differs from the CLI workflow. This is a successor notice, not an
ordinary update alert. The API 0.10.1 bridge explains that version 4 continues the API
app and preserves its API-specific identity and settings.
