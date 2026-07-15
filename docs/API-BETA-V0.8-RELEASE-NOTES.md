# P5 Archive Manager API Beta v0.8 — Release Notes

Version: **0.8 (build 13)**

Release date: **2026-07-15**

Focus: **Phase 1 storage-path mapping and connection safety**

> **Beta — test only.** Back up your data first. Folder checking and mapping are
> read-only, but Delete and Archive are real actions. Use disposable data for destructive
> tests and verify the proof report before deleting anything.

## What changed

- **Review before checking:** automatic checking after a folder drop remains enabled by
  default but can be turned off in Settings so the P5 path can be reviewed or edited.
- **Independent local and archived roots:** files on a current storage volume can be
  compared with the different path from which they were originally archived.
- **Per-server path mappings:** save current-local → archived-P5 prefix substitutions.
  Multiple rules are supported, matches stop at path-component boundaries, and the
  longest matching prefix wins.
- **Improved mapping editor:** longer fields, in-field examples, validation, preview,
  prominent saving, and automatic saving of valid changes when Settings closes or the
  selected server changes.
- **P5 connection indicator:** the main window distinguishes **Connected**,
  **Authentication failed**, **Server unreachable**, and **Not tested**, including
  latency, last-tested time, and **Retest**.
- **Required connectivity preflight:** a folder check requires a recent successful P5
  connection result. Status older than 60 seconds is retested automatically.
- **Clearer evidence:** History, proof reports, deletion receipts, and diagnostics show
  both the real local folder and the archived P5 path.
- **Universal tester build:** Release archives contain Apple silicon and Intel code.

## What was fixed

- Valid mappings no longer disappear after closing Settings or switching servers.
- Reopening Settings after editing a mapping no longer crashes.
- P5 timeouts, refused connections, rejected credentials, and invalid responses stop the
  check as undetermined instead of being reported as **not archived** evidence.
- Mapping and server text fields no longer retain unsafe array-index bindings after rows
  or server selections change.

## What to test

1. **Connectivity states:** verify green for a working server, orange for rejected
   credentials, red for an unavailable server, and that **Retest** updates the result.
2. **Connection safety:** attempt a folder check while P5 is unavailable. Confirm no file
   receives a not-archived verdict from the failed request.
3. **Mapping persistence:** add a valid mapping, close and reopen Settings, switch
   servers, and relaunch. Confirm each server retains its own rule and no crash occurs.
4. **Mapped comparison:** drop a folder under the current-local prefix and confirm the
   derived P5 path uses the saved archived prefix while local operations retain the real
   dropped path.
5. **Review before checking:** turn off automatic checking, drop a folder, and confirm
   the app waits for **Check Archive Status**.
6. **Mapping rules:** test no-match fallback and overlapping mappings; confirm the
   longest valid rule wins.
7. **Evidence and safety:** confirm reports and History show both roots. Use disposable
   data if testing Delete or Archive.
8. **Regression:** check a normal folder whose current and archived paths match and
   compare its results with the previous beta.

Use the complete [v0.8 Phase 1 Tester Notes](API-BETA-V0.8-TESTER-NOTES.md) when reporting
results or attaching diagnostic logs.

## Known limitations

- `.p5a` and `.p5c` stub verification remains a separate Phase 2 investigation.
- Archive-to-P5 remains beta and should be tested only with a disposable plan.
- Signed/notarized distribution requires valid Apple signing certificates.
