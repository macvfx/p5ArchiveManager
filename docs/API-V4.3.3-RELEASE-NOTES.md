# P5 Archive Manager API 4.3.3 (build 58) — pre-release beta

**Status:** pre-release · **Date:** 2026-11-04 · **Tag:** `4.3.3+58`

This release covers everything since 4.3.0 — restoring directly from a P5 stub, a full
redesign of the main window and Settings around Delete and Archive as the app's two main
actions, and two fixes from live-testing that redesign against a real server.

## Headline: Delete and Archive are now the two obvious actions

Check → Delete/Archive is the app's whole original point — see what's archived and clean
it up, or get the rest archived so it can be cleaned up too. The main window now reads
that way: two equal-weight buttons, red and blue, each opening its own confirmation sheet
(scope, proof links, and for Delete, typing DELETE to confirm) in place of a plain system
dialog or a disclosure you had to find and open.

- **Settings** is a sidebar of tabs (Servers, Sources, Archiving, Receipts & Mirror,
  General, Diagnostics & Logs, About) instead of one long scrolling form.
- **Browse, Server Info, Check History, and the new Check Details window** moved to a
  **Tools** menu, each its own window. Check Details holds close size matches, full file
  provenance, and Deep Verify. Save proof report is now a toolbar export icon.
- **Restore directly from a P5 stub** (`.p5c`/`.p5a` left behind after an archive-and-
  delete) — Check and Deep Verify now recognize one by name and show how many P5 still
  matches; "Restore N stub(s)…" restores the real file with one action, no project file
  needed.

## Fixed

- The main window could clip the top/bottom of a check's result until resized by hand —
  fixed by forcing a clean relayout when a new result replaces the old one.
- **Browse Index now has a Roots menu** — `Volumes`, `mnt`, and any imported-volume roots
  configured for the server, instead of needing to already know what to type.
- **Server Info** now shows its own raw JSON response instead of it only appearing in a
  separately-opened Browse Index window.
- **Files with emoji in their name are flagged before archiving**, not after a confusing
  failure. P5's REST connection can't address those filenames at all — a confirmed,
  already-reported P5 limitation, not something this app can work around — so the Archive
  confirmation sheet now explains it and leaves those files out of the submission.
- The stub-restore "could not resolve handle" failure is fixed: re-pinning the shared
  `P5Kit` package removed a double-percent-encoding bug in a handle P5's REST API already
  returns pre-encoded. Confirmed with a completed restore job against a real server.

## What to test

1. Drop a folder, run Check, and confirm the result is fully visible without resizing.
2. Click Delete and Archive in turn — confirm each sheet shows the right scope and that
   Archive correctly excludes any file it can't address.
3. Open each Tools-menu window (Browse, Server Info, Check History, Check Details) and
   confirm they reflect the same session as the main window's last check.
4. If a folder has a leftover `.p5c`/`.p5a` stub, confirm Check recognizes it and that
   Restore puts the real file back.

Known, deliberate trim: Browse's old "Browse checked path" / "Use for Check ↑" shortcuts
are gone — a separate Tools window has no way to read or write the main window's own
check-path field. Ordinary navigation (root / Up / jump-to-path / Roots / click a folder)
is unaffected.

Guide: [API beta guide](API-BETA-GUIDE.md), *Delete and Archive — the app's two main
actions*.

> ⚠️ **Beta — test only.** Back up your data first. Delete, Archive and Restore are real
> actions. Provided as-is, with no warranty.
