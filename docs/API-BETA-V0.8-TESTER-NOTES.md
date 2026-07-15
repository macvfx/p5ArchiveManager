# P5 Archive Manager API Beta v0.8 — Phase 1 Tester Notes

Build: **0.8 (12)**  
Focus: **Storage-path mapping and review-before-check**

> ⚠️ **Beta — test only.** Path mapping and checking are read-only, but Delete and
> Archive are real actions. Back up your data, use disposable files for destructive
> tests, and review the proof report before deleting anything.

## What changed

### Optional automatic check after a drop

Folder drops continue to start a check automatically by default. Turn off **Settings ▸
General ▸ Automatically check after dropping a folder** to review or edit the derived P5
path before clicking **Check Archive Status**.

### Independent local and archived paths

The main window now keeps two explicit roots:

- **Local folder to inspect** — where the files are currently stored.
- **Archived P5 path** — where those files were recorded in the P5 index.

Editing the P5 path no longer clears the local folder. Files can therefore be checked
after moving between storage volumes, provided their relative paths remain the same.

### Per-server prefix mappings

Mappings are configured under **Settings ▸ Path mapping** for the selected P5 server.

```text
Current local prefix: /Volumes/storageA
Archived P5 prefix:   Volumes/storageB
```

Dropping `/Volumes/storageA/Projects/Show01` then derives
`Volumes/storageB/Projects/Show01`.

The editor includes long path fields, in-field examples, validation, and a preview.
Multiple rules are allowed; the longest matching prefix wins. The main window shows the
applied mapping, identifies manual edits as custom, and offers **Recalculate from dropped
folder**.

### Both paths appear in evidence

History, proof CSV/TXT files, deletion receipts, and diagnostics distinguish the real
local folder from the P5 archive path.

## Safety boundary

Mapping changes only the P5 inventory lookup:

- Enumeration, delete re-verification, and deletion use the real local folder.
- Archive submission uses the real local source path as seen by the selected P5 client.
- Exact/close size verification is still required before a file is deletable.

`.p5a` and `.p5c` stub verification is a separate future feature and is not included in
this phase.

## What to test

### 1. Existing drop behavior

Leave automatic checking on and drop an ordinary folder whose current and archived
paths match.

Expected: checking starts automatically and results agree with the previous beta.

### 2. Review before checking

Turn automatic checking off, then drop a folder.

Expected: both paths fill in, no P5 request starts, and the folder waits for **Check
Archive Status**.

### 3. Manual path substitution

Drop a folder and manually change only the storage prefix in **Archived P5 path**.

Expected: the local folder remains connected and the check compares files using their
shared relative paths.

### 4. Saved mapping

Add the real current-local and archived-P5 prefixes in Settings. Confirm the preview,
save, and drop a matching folder.

Expected: the correct P5 path is derived and the main window names the applied rule.

### 5. No-match fallback

Drop a folder that matches no rule.

Expected: the P5 path defaults to the dropped path without its leading slash, and the UI
reports that no saved mapping matched.

### 6. Longest rule wins

Test overlapping mappings such as:

```text
/Volumes/storageA          → Volumes/GeneralArchive
/Volumes/storageA/Projects → Volumes/ProjectArchive
```

Expected for `/Volumes/storageA/Projects/Show01`:
`Volumes/ProjectArchive/Show01`.

### 7. Per-server persistence

Save different mappings for two P5 servers, switch between them, and relaunch the app.

Expected: each server retains its own rules and existing credentials/settings remain
available.

### 8. Reports and disposable safety test

Run a mapped check and save the proof report. Confirm History and both proof formats show
the local and P5 roots. If testing Delete or Archive, use disposable data and confirm the
action still targets the real local source path rather than the mapped archive path.

## Report a problem

Include:

- Version/build `0.8 (12)`
- Whether automatic checking was on or off
- An anonymized current-local prefix and archived-P5 prefix
- Expected and actual derived P5 paths
- Whether the UI showed mapped, custom, or unmatched
- Whether the issue affected Check, proof, Delete, or Archive

Reproduce the problem, then use **Receipts, audit & logs ▸ Zip logs to Desktop** and
attach the resulting diagnostics archive. Passwords are not logged.
