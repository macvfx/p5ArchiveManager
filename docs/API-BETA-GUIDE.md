# P5 Archive Manager — API Beta · User Guide

**v0.9 — beta preview of the upcoming v4.** Talks to the **Archiware P5 REST API v8**
(no `nsdchat`). This is the REST-API rewrite of the shipping P5 Archive Manager; the
stable nsdchat app (v3.7 build 2) is documented in the [main README](../README.md).

> ⚠️ **Beta — test only.** **Back up your data first.** Delete and Archive are real,
> destructive actions, and the Archive-to-P5 write is still **unproven against live
> servers**. Provided **as-is, with no warranty of any kind**. Test on disposable data
> and verify the receipts before trusting it with real projects.

Testers focusing on the new storage workflow should use the
**[v0.8 Phase 1 tester notes](API-BETA-V0.8-TESTER-NOTES.md)**.

---

## 1. What this app is for

**Goal:** quickly confirm whether the files on a disk folder are already archived in
P5, then act on that:

- **Archived & verified →** safe to **delete** from disk (P5 keeps the copy), with a
  receipt as proof.
- **Not archived →** optionally **archive** them to P5.

**Use case:** a project folder that gets archived and restored many times. P5 keeps
every past archive and won't clean up; you need to be sure the files on disk match
what's on tape *before* freeing space — and catch the odd new file that was never
archived. The app gives you per-file proof (disk size/date vs P5 size/date/tape) so a
delete is defensible.

---

## 2. First-time setup

Servers are managed in **Settings** (the **⌘,** window, or the **⚙️ gear** at the top-right
of the main window), so you can keep several P5
servers and switch between them.

1. Open **Settings** (⌘,) → **P5 Servers**. Use **Add** for a new server, then enter:
   - **Host/IP**, **Port** (usually `8000` for the REST API), **API** (`v1`)
   - **Username**, **Index** (e.g. `Default-Archive`)
   - **Password** → **Save** (stored in your Keychain, **per server**)
2. Click **Test Connection** → expect ✅.
3. (Optional) In the **Archive index search** section, toggle **Search all archive
   indexes** if a file might live in any index, not just the one named above.
4. (Optional) Under **Path mapping**, add the current local storage prefix and the path
   prefix recorded in this server's P5 index.

Back on the main window, the compact **server picker** at the top selects which server
the check runs against. Its connection row distinguishes **Connected** (green, with
latency and last-test time), **Authentication failed** (orange), **Server unreachable**
(red), and **Not tested** (gray). Use **Retest** after changing networks or server
settings. Re-open Settings any time to edit or add servers.

**Help & welcome guide.** On first launch the main window shows a short welcome panel.
The **Help** menu has **P5 Archive Manager Help** (⌘?) — getting-started steps and an
Advanced-tools explainer — plus **Show Welcome Guide Again** (also in **Settings ▸
General**). The **About** window (App menu) shows the version.

---

## 3. The main workflow

### Check a folder
- Confirm the selected server shows **Connected**. Before checking, the app requires a
  successful connection result no more than 60 seconds old and automatically retests a
  stale result. A failed preflight stops without classifying files as not archived.
- **Drag the folder onto the drop area** → it auto-scans by default (this is the fast
  path and enables the disk-vs-P5 comparison). Turn off **Automatically check after
  dropping a folder** in Settings ▸ General to review the path first.
- **Local folder to inspect** and **Archived P5 path** are independent. Edit the P5 path
  or use a saved mapping when files have moved to another storage root.
- Or **type a P5 path** and click **Check Archive Status** (P5-only, no disk compare).

#### Storage path mappings (v0.8)

Mappings belong to the selected P5 server. For example:

```text
Current local prefix: /Volumes/storageA
Archived P5 prefix:   Volumes/storageB
```

Dropping `/Volumes/storageA/Projects/Show01` derives
`Volumes/storageB/Projects/Show01`. The longest matching rule wins. The main window
shows the applied rule, and **Recalculate from dropped folder** restores its result after
a manual edit.

**Preview local path** is a temporary mapping calculator. Enter a representative full
current-local path to see the archived P5 path that the draft rules would derive. The
preview value is not saved, is not another mapping, does not select or read a real
folder, does not contact P5, and does not affect checks in the main window.

Mapping changes only the P5 lookup. Enumeration, delete safeguards, and archive
submission continue using the real local folder.

It enumerates the files **on disk** and asks P5 only about the directories that hold
them — so a folder with a few files left checks in a moment, even if the archive holds
the whole project history.

### Read the result

> **The check is disk-driven.** It compares the files **on disk** to P5, so the counts are
> always about your local files. A folder with no local files (e.g. they were already
> deleted) shows **0 archived** even though P5 still has them on tape — there's just
> nothing on disk to compare. To see what P5 holds at a path regardless of local files,
> use **Deep verify** (below) or **Browse** the index. *(v0.6.3 shows an inline hint when a
> check matches 0 files, pointing you to these tools.)*

- **Total files / Archived / Size** — for the files on disk.
- **Not archived / Needs archiving** — on disk but not in P5.
- **P5 Volumes / P5 Barcodes** (right-hand pills) — the tapes the files live on; volumes
  show `label · location · media type` where P5 reports them.
- **File provenance — disk vs P5 proof** — per file: disk size + mod date vs P5 size +
  archive date + volume/barcode (+ the **index** it was found in when searching all),
  with a verdict:
  - `✓ exact` — byte-identical
  - `≈ close` — within 64 KB (rounding/metadata; counted as archived)
  - `⚠ size mismatch` — same name, different size (review; **not** deletable)
  - `＋ not archived` — P5 doesn't have it
  - `↪` marks a symlink

### Delete (verify-first chain)
The **Delete** button lives in the right column, under the tape pills. It appears only
when there are `exact`/`close` (proven-archived) files. Clicking it does **not** delete
immediately — it opens a **verify-first** dialog so deletion is always a deliberate step:

1. **Deep verify entire P5 folder first** — run a full scan to double-check before
   committing (see Deep verify below).
2. **Open receipts folder** — review past deletion receipts.
3. **Delete N files (size) now** — the irreversible action (red).
4. **Cancel.**

**Proof BEFORE delete.** A **proof report is written before anything is deleted** — both
a **CSV** and a human-readable **TXT** listing every file with its disk size/dates vs P5
size/archive-date/volume/barcode and verdict, plus a **NOT ARCHIVED** section. You can
also write it any time with **Save proof report (CSV + TXT)** without deleting. All
reports + receipts live in
`~/Library/Application Support/P5ArchiveManagerAPI/Receipts/`.

When you proceed, it deletes **only** the verified files and **re-checks each file's
existence and size right before removing it** (anything changed since the check is
skipped and logged). It then writes a **deletion receipt** (in-app entry + `.md`) —
**Open last receipt** (under Delete) reveals it.

**One-shot + auto re-check.** Once you delete, the Delete button **disables** (greys out,
relabels "Deleted — re-check to act again") so the same result can't be deleted twice, and
the app **automatically re-checks the folder** — the result then shows the post-delete
state. Run a fresh check to act again.

Recommended chain: **Check → (Deep verify) → review provenance → Save proof → Delete →
receipt.**

### Archive (the not-archived)
- When a check finds not-archived files, an **Archive** panel appears.
- **Load archive plans & clients**, pick a **Plan** + **Client**, then **Archive N files…**
- Submits them to P5 and monitors the job briefly.
- **Named job + manifest (v0.5):** the job is submitted with the **full source folder path**
  as its title, so it appears in the **P5 job monitor** as the folder (not a generic "REST
  Archive job"). The accepted files (`path → P5 handle`) are recorded in the saved
  `archive-…-job.log` receipt as an **ARCHIVED ENTRIES** manifest.
- **Source-path tagging (v0.7, Settings ▸ Archiving, ON by default):** each archived file
  also records its **full original path** in the P5 index's per-file `description` metadata,
  so the archive is **searchable by source path** and the origin shows on the entry. Only
  applied when the plan's index has a `description` key (a P5 default), so it never blocks
  archiving. Turn it off if you don't want the app writing metadata into your index.
- **Plan `deletefiles` flag:** plans configured to delete sources after archiving are
  marked **"⚠ deletes source"** in the picker, with a warning on selection and in the
  confirm dialog. Such a plan archives **and deletes the source P5-side, without the
  app's proof/receipt** — for the proof-first workflow, archive with a *non*-deletefiles
  plan, then let the app delete (with receipt).
- **Client/path:** files are submitted as the **selected client** sees them. Pick the
  client that actually mounts the volume (e.g. `jellyfish`/`VanMacStudio` for
  `/Volumes/JellyfishSMB`; `localhost` for paths on the P5 server).
- **One-shot + auto re-check:** like Delete, the Archive button **disables after running**
  and the app **re-checks the folder** so newly-archived files move into the archived
  count. Note: P5 indexing can lag job completion — if a re-check still shows files as
  not-archived, the job is likely still finishing; re-check again a moment later.

### Deep verify (paranoid)
- **Deep verify — entire P5 folder** (the button under Delete, or the first option in the
  Delete dialog) does a full recursive walk of *everything* P5 has under the path,
  listing it all with your on-disk files **highlighted**. It's the belt-and-braces step
  in the delete chain.
- **(v0.9)** It scans the server's **configured index** — or **every index** when *Search
  all archive indexes* is on, showing a per-index file count in the summary and labelling
  each entry with the index it was found in. While it runs, a live file count and running
  size tick up next to the spinner.

**Why run Deep verify when the check already said "archived"?** The two tools answer
different questions:

- The **check is disk-driven** — it asks P5 only about the files currently on disk.
  It answers *"are my disk files archived?"* fast, but it cannot see anything else.
- **Deep verify is P5-driven** — it lists everything the archive holds under the path.
  It answers *"what does P5 actually have here?"*

Use Deep verify when:

- **Before a delete** — confirm the archive really holds the whole folder (not just the
  files that happen to remain on disk) so freeing the space is defensible.
- **The check found 0 or fewer files than expected** — if the local folder was already
  partly deleted or restored elsewhere, the disk-driven check has nothing (or little) to
  ask about; Deep verify shows what's on tape regardless of the disk.
- **Hunting duplicates / earlier versions** — P5 keeps every past archive; Deep verify
  lists archive-only files that no longer exist locally (they show *without* the
  "on disk" highlight).
- **Cross-index doubt** — with *Search all archive indexes* on, the per-index counts
  show which index actually holds the folder (and whether copies exist in more than one).

### Browse the index (Advanced tools)

Browse lists one level of an archive index at a time — the raw view of what P5 stores,
with the raw JSON response underneath for diagnostics. Use it when a check result looks
off and you want to see the index with your own eyes:

- **Browse checked path (v0.9)** starts at the P5 path from the check above (the jump
  field is pre-filled after every check), so "go look at what P5 has there" is one click.
- The **Index picker (v0.9)** chooses which archive index to list (defaults to the
  server's configured index; switching re-lists the current folder) — handy for
  confirming which index a folder actually lives in. The diagnostics line names the
  index and full URL of every request.
- Names P5 stores with caret-hex encodings (e.g. `\` as `^5c`) are navigable.

---

## 4. Feature list (working)

- **Multi-server** manager in Settings (⌘,); per-server Keychain password; Test Connection.
- Main-window **P5 connection status** with latency, last-tested time, Retest, distinct
  authentication/unreachable states, and a required connectivity preflight.
- Fast **local-driven** disk-vs-P5 check (queries only relevant directories).
- **Multi-index search** (optional) — find a file in whichever archive index holds it.
- Live counters; steady result box.
- **Case auto-correction** (`TEST IN PROD` → `Test in Prod`); suggests siblings when a path
  segment isn't found. (The index root isn't listable — start paths from `Volumes`/`mnt`.)
- Drop derives the archived P5 path and auto-scans unless disabled; editing the P5 path
  keeps the local folder connected.
- **Per-server storage-path mapping (v0.8)** with validation, preview, longest-prefix
  selection, and explicit local/P5 evidence labels.
- **Size verification** with exact/close/mismatch verdicts; symlink detection.
- **Per-file provenance** list (the delete proof) — incl. volume location, media type, index.
- **P5 Volumes / Barcodes** pills, populated live; **persistent volume→barcode cache**.
- **Proof report (CSV + TXT)** — written before any delete and on demand.
- **Delete with receipt** (guarded, re-verified, audited); **one-shot + auto re-check**.
- **Deep verify** full list with on-disk highlight; honours *Search all archive indexes*
  with per-index counts and live progress (v0.9).
- **Browse** the archive index + **raw JSON** viewer (diagnostics) — with an **index
  picker** and **Browse checked path** to start exploring at the folder you just
  checked (v0.9).
- **Server info**: clients & plans (with names), volume-cache size + Clear.
- Local **check history**.
- **Named archive jobs + manifest (v0.5)** — archive jobs carry the source folder path as
  their title (shown in the P5 job monitor); accepted files (`path → P5 handle`) saved to
  the archive receipt.
- **Source-path tagging (v0.7)** — each archived file records its full original path in the
  index's per-file `description` metadata (searchable; ON by default in Settings ▸ Archiving).
- **Special-character filenames (v0.6)** — files whose name contains a backslash (P5 stores
  it as `^5c`) are correctly recognised as archived, not falsely "not archived". *(v0.6.1:
  the Browse inspector can also navigate into backslash folders.)*
- **Session logs & diagnostics** — every API call, archive job step and error is written
  to a per-launch log; verbose on by default (Settings ▸ Diagnostics). *Receipts, audit &
  logs ▸ Zip logs to Desktop* bundles them for support (see **§6 Troubleshooting**).

---

## 5. Beta status — what to test & known caveats

Please exercise these and report back (issues / what worked):

- **v0.8 storage mapping** — use the focused
  **[Phase 1 checklist](API-BETA-V0.8-TESTER-NOTES.md)** to test review-before-check,
  manual paths, saved mappings, overlap handling, persistence, and report paths.
- **Cross-check vs the shipping app** — run the **same folders** through both the v3.7
  nsdchat app and this beta; archived vs not-archived counts should agree.
- **Full delete chain on a throwaway folder** — check → proof report → delete → receipt;
  confirm the receipt is accurate and P5 still holds the files.
- **Archive submit on a disposable plan** — the **first live write**, still unproven;
  confirm the job runs and a re-check shows the files archived.
- **Job title + manifest (v0.5)** — after an archive, confirm the **P5 job monitor shows
  the source folder path** (not "REST Archive job"), and the saved `archive-…-job.log`
  lists each `path → handle`.
- **Special-character filenames (v0.6)** — archive files with a **backslash in the name**,
  then Check; they should report **archived** (not falsely "not archived").
- **Disk-driven check (don't be surprised by "0 archived")** — check a folder whose files
  are **still on disk**. If you check a folder whose files were already deleted, it
  correctly shows 0 (nothing on disk to compare) and points you to **Deep verify**. That's
  expected, not a bug.
- **Non-default index** — if your files live in an index other than the server's
  configured one, turn on **Settings ▸ Archive index search ▸ Search all archive indexes**,
  then re-check.
- **Logs capture the archive** — after an archive (especially one that misbehaves),
  **Zip logs to Desktop** and confirm the `session-*.log` shows the submit, raw response,
  job ID and poll states (see **§6**).
- **Edge cases** — multi-index (a file in a non-default index); size-mismatch handling on
  a re-saved `.drp`/`.drt`; symlinks.

Known caveats:

- **Archive the not-archived** is the **first write to your P5 server** and is **unproven
  against a live server**. Test on a **disposable/test archive plan** first. It submits
  the **local absolute paths**; those must be valid on the **client** you select.
- **Delete is real/destructive** — test on a **throwaway folder** first and check the
  receipt before using on real projects.
- **Size tolerance = 64 KB** for "close" (the provenance list shows the exact Δ).
- **Sub-directory case:** only the *base* path is case-corrected; nested folders use the
  disk's casing, so a nested folder whose case differs from P5 may show as not-archived.

---

## 6. Troubleshooting — sending logs

If something doesn't work — most commonly **"I archived files but nothing happened"** —
the app keeps a detailed log you can send for diagnosis.

1. **Reproduce the problem** (e.g. select the plan + client and run the archive again).
2. **Receipts, audit & logs ▸ Zip logs to Desktop.** This bundles the session logs into
   `P5ArchiveManager-logs-<date>.zip` on your Desktop and reveals it in Finder.
3. **Email the zip** to support.

What's in the log:

- Every P5 API call and any network/curl error.
- The full archive sequence: the submit request, P5's raw response, the **job ID**, each
  status poll, and the final result — including a clear line if no job was created (the
  usual cause of "it didn't archive").
- No passwords are ever written to the log.

**Verbose logging is on by default** (Settings ▸ Diagnostics), so the first report already
has full detail. If logs get large during big **Deep verify** scans you can turn verbose
off there — archive activity and errors are still always logged. *Reveal logs* opens the
folder if you'd rather attach files yourself.

---

## 7. Where things live

- Receipts: `~/Library/Application Support/P5ArchiveManagerAPI/Receipts/`
- Session logs: `~/Library/Application Support/P5ArchiveManagerAPI/Logs/` (one `session-*.log` per launch)
- Volume cache / history: `~/Library/Application Support/P5ArchiveManagerAPI/`
- Live Archiware P5 REST API docs: https://blog.archiware.com/redoc/p5_rest_api/awp5api.html

---

*Feedback: [reach out via GitHub](https://github.com/macvfx). © 2026 code.matx.ca — P5 Archive Tools for macOS & iOS.*
