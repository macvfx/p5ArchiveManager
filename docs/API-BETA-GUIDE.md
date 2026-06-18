# P5 Archive Manager — API Beta · User Guide

**v0.4 — beta preview of the upcoming v4.** Talks to the **Archiware P5 REST API v8**
(no `nsdchat`). This is the REST-API rewrite of the shipping P5 Archive Manager; the
stable nsdchat app (v3.7 build 2) is documented in the [main README](../README.md).

> ⚠️ **Beta — test only.** **Back up your data first.** Delete and Archive are real,
> destructive actions, and the Archive-to-P5 write is still **unproven against live
> servers**. Provided **as-is, with no warranty of any kind**. Test on disposable data
> and verify the receipts before trusting it with real projects.

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

Servers are managed in **Settings** (the **⌘,** window), so you can keep several P5
servers and switch between them.

1. Open **Settings** (⌘,) → **P5 Servers**. Use **Add** for a new server, then enter:
   - **Host/IP**, **Port** (usually `8000` for the REST API), **API** (`v1`)
   - **Username**, **Index** (e.g. `Default-Archive`)
   - **Password** → **Save** (stored in your Keychain, **per server**)
2. Click **Test Connection** → expect ✅.
3. (Optional) Toggle **Search all archive indexes** if a file might live in any index,
   not just the one named above.

Back on the main window, the compact **server picker** at the top selects which server
the check runs against; the status line shows `user@host · index` (and `· no password` /
`· all indexes` when relevant). Re-open Settings any time to edit or add servers.

**Help & welcome guide.** On first launch the main window shows a short welcome panel.
The **Help** menu has **P5 Archive Manager Help** (⌘?) — getting-started steps and an
Advanced-tools explainer — plus **Show Welcome Guide Again** (also in **Settings ▸
General**). The **About** window (App menu) shows the version.

---

## 3. The main workflow

### Check a folder
- **Drag the folder onto the drop area** → it auto-scans (this is the fast path and
  enables the disk-vs-P5 comparison).
- Or **type a P5 path** and click **Check Archive Status** (P5-only, no disk compare).

It enumerates the files **on disk** and asks P5 only about the directories that hold
them — so a folder with a few files left checks in a moment, even if the archive holds
the whole project history.

### Read the result
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

---

## 4. Feature list (working)

- **Multi-server** manager in Settings (⌘,); per-server Keychain password; Test Connection.
- Fast **local-driven** disk-vs-P5 check (queries only relevant directories).
- **Multi-index search** (optional) — find a file in whichever archive index holds it.
- Live counters; steady result box.
- **Case auto-correction** (`BC CANCER` → `BC Cancer`); suggests siblings when a path
  segment isn't found. (The index root isn't listable — start paths from `Volumes`/`mnt`.)
- Drop = auto-scan + replaces typed path; typing = manual scan + clears the drop.
- **Size verification** with exact/close/mismatch verdicts; symlink detection.
- **Per-file provenance** list (the delete proof) — incl. volume location, media type, index.
- **P5 Volumes / Barcodes** pills, populated live; **persistent volume→barcode cache**.
- **Proof report (CSV + TXT)** — written before any delete and on demand.
- **Delete with receipt** (guarded, re-verified, audited); **one-shot + auto re-check**.
- **Deep verify** full list with on-disk highlight.
- **Browse** the archive index + **raw JSON** viewer (diagnostics).
- **Server info**: clients & plans (with names), volume-cache size + Clear.
- Local **check history**.
- **Session logs & diagnostics** — every API call, archive job step and error is written
  to a per-launch log; verbose on by default (Settings ▸ Diagnostics). *Receipts, audit &
  logs ▸ Zip logs to Desktop* bundles them for support (see **§6 Troubleshooting**).

---

## 5. Beta status — what to test & known caveats

Please exercise these and report back (issues / what worked):

- **Cross-check vs the shipping app** — run the **same folders** through both the v3.7
  nsdchat app and this beta; archived vs not-archived counts should agree.
- **Full delete chain on a throwaway folder** — check → proof report → delete → receipt;
  confirm the receipt is accurate and P5 still holds the files.
- **Archive submit on a disposable plan** — the **first live write**, still unproven;
  confirm the job runs and a re-check shows the files archived.
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
