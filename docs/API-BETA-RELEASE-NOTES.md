# P5 Archive Manager — API Beta v0.8

The REST-API rewrite of P5 Archive Manager (preview of the upcoming **v4**). Talks to the
**Archiware P5 REST API v8** — no `nsdchat` dependency. Same job as the shipping app:
confirm what's archived in P5, delete the proven-archived files, and archive the rest.

> ⚠️ **Beta — test only.** Back up your data first. **Delete and Archive are real,
> destructive actions**, and the Archive-to-P5 write is still unproven against live
> servers. Provided **as-is, with no warranty**. Test on disposable data and verify the
> receipts before trusting it with real projects.

---

## 🆕 New in v0.8 — storage-path mapping

- **Independent roots:** the dropped local folder and archived P5 path can now differ.
  Editing the P5 path no longer clears the local folder.
- **Per-server prefix mappings:** translate a current local prefix such as
  `/Volumes/storageA` to an archived P5 prefix such as `Volumes/storageB`. Longest match
  wins, with path-component boundary protection and an in-Settings preview.
- **Review before checking:** automatic checking after a drop remains on by default but
  can be disabled under Settings ▸ General.
- **Clearer evidence:** History, proof CSV/TXT files, deletion receipts, and diagnostics
  identify both roots.
- **Safety preserved:** mapping affects only the P5 lookup. Enumeration, deletion, and
  archive submission still use the real local source path.

### Connection status and safe preflight — build 13

- The main server row shows **Connected**, **Authentication failed**, **Server
  unreachable**, or **Not tested**, plus response time and last-tested time.
- **Retest** checks the selected server on demand; server/settings changes trigger a new
  test automatically.
- Folder checks require a recent successful connection result. A timeout, rejected
  login, or invalid P5 response stops the check and cannot become a misleading “not
  archived” result.
- Path mappings now save on Settings close/server switch, and reopening Settings after
  editing a mapping no longer crashes.

Step-by-step validation: **[v0.8 Phase 1 tester notes](API-BETA-V0.8-TESTER-NOTES.md)**.

---

## New in v0.7 — source-path tagging

When the app archives a file, it now records that file's **full original path** in the P5
index's per-file **`description`** metadata. So every file archived through the app stays
**traceable to where it came from**: you can search the archive index by source path and
the origin is visible directly on the entry — independent of the job log.

Why it matters: P5's Archive Overview does not attribute REST-created archive jobs to a
plan, so this is how the app keeps archived files auditable by their source. It's **on by
default** (Settings ▸ Archiving), and only applied when the plan's index has a `description`
key (a P5 default), so it never interferes with archiving. Turn it off if you'd rather the
app not write metadata into your index.

---

## ✨ Features

- **Fast disk-vs-P5 check** — drop a folder; it enumerates the files on disk and queries
  only the P5 directories that hold them. Per-file verdict: `exact` / `close` (±64 KB) /
  `size mismatch` / `not archived`.
- **Storage-path mapping** *(new in 0.8)* — compare a current local storage root against
  the different path stored in P5, with saved mappings per server.
- **Per-file proof** — disk size & date vs P5 size, archive date, volume, barcode,
  location, media type, and the matching index.
- **Proof-first delete with receipt** — a CSV + TXT proof report is written **before**
  anything is removed; only verified files are deleted, each re-checked immediately before
  removal, and a receipt (+ optional NAS mirror & running audit log) is saved.
- **Archive the not-archived** — submit straight to a P5 plan/client and monitor the job.
- **Source-path tagging** *(new in 0.7)* — each archived file records its full original path
  in the index's per-file `description` metadata, so the archive is searchable by source
  path (ON by default; guarded so it never blocks archiving).
- **Named archive jobs + manifest** *(0.5)* — submissions carry the **full source folder
  path** as the job title, so the P5 **job monitor shows the folder** (not a generic
  "REST Archive job"). Accepted files (`path → P5 handle`) are logged and saved to the
  archive receipt.
- **Session logging** *(0.4)* — every API call, archive job step and error is written to a
  per-launch log. **Verbose logging is on by default**, so a failed archive is already
  captured (request, raw response, job ID, poll states). **Receipts, audit & logs ▸ Zip
  logs to Desktop** bundles it into one `.zip` to send in — no passwords are ever logged.
- **Multi-server & multi-index** — manage several P5 servers (per-server Keychain
  password); optionally **Search all archive indexes** so a file is found wherever it lives.
- **Deep verify** — full recursive walk of everything P5 holds under a path, with your
  on-disk files highlighted.
- **Browse + raw JSON**, **clients/plans** (named), **check history**, one-shot actions
  with auto re-check, welcome guide, in-app Help/About.
- **Settings gear** *(0.6.2)* in the main window, field guidance via hover tooltips
  *(0.6.4)*.

## 🐛 Fixes

- **Backslash (and special-character) filenames** *(0.6)* — files with a `\` in the name
  (which P5 stores internally as `^5c`) were wrongly reported **"not archived"** even
  though they were on tape. The check now decodes P5's `^XX` encoding when matching, so
  they're correctly recognised. P5-side decode only, guarded by the size check.
  *Verified against a live server.*
- **Browse into backslash folders** *(0.6.1)* — the Browse inspector can now navigate into
  folders whose names contain a backslash. (Diagnostics-only; the main workflow was
  unaffected.)
- **Clearer empty results** *(0.6.3)* — when a check matches **0 files**, an inline hint
  explains the check is **disk-driven** and points to **Deep verify** / **Browse** to see
  what P5 holds. Prevents mistaking "files deleted locally" for "P5 lost them".
- **Surfaced the index-search toggle** *(0.6.2)* — **"Search all archive indexes"** now
  has its own clearly-labelled **Archive index search** section in Settings (was buried in
  the server form). Turn it on if your files live in a non-default index.

## 🔎 Good to know when testing

- **The check is disk-driven.** It compares files **on disk** to P5. A folder with no (or
  already-deleted) local files shows **0 archived** even though P5 still has them — use
  **Deep verify** or **Browse** to see the P5 side.
- **Non-default index?** Turn on **Settings ▸ Archive index search ▸ Search all archive
  indexes**, then re-check.
- **Hit a problem?** Reproduce it, then **Receipts, audit & logs ▸ Zip logs to Desktop**
  and send the `.zip`.

**Full user guide:** [`API-BETA-GUIDE.md`](API-BETA-GUIDE.md)
