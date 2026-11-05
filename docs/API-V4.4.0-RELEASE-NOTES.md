# P5 Archive Manager API 4.4.0 (build 62) — pre-release beta

**Status:** Latest · **Date:** 2026-11-05 · **Tag:** `4.4.0+62`

Checking a folder that P5 can't find by path alone — because it's on a label-rooted
index such as Imported-Volumes, or was moved into an unnamed folder before archiving —
used to mean leaving the main window and dropping a hand-built list of paths into
Restore from Project File. Check now does that for you.

## Added: Check now falls back to the Restore search engine

P5's REST API genuinely has no way to search by name or relative path — only an exact
path lookup or a one-level folder listing. That's a server limitation, not a client
bug, and it's why a label-rooted index or relocated media could defeat the main
window's Check even with historical locations configured: neither of those lookups
work without an exact path, and this is neither.

Restore from Project File already works around that with TSV inventories, P5 Archive
Browser's catalogue, imported-volume labels, and a walk that finds media moved into an
unnamed wrapper folder before archiving. When the current path *and* every historical
location both come up empty, Check now tries that same engine as a last resort, using
whatever is already set up for Restore (Settings ▸ TSV inventories, ▸ Imported
volumes) — nothing new to configure.

## Added: Tools ▸ Check Folder (via Restore Search)…

For a label-rooted index, going straight to the engine above can be faster than
waiting on Check to exhaust the current path and every historical location first.
This new Tools menu item picks a folder, builds the same path list by hand, and opens
Restore from Project File with it already loaded.

- Every file in the folder is checked individually — including every segment of a RED
  clip, rather than folding them into one item the way an editor's timeline does.
- A `.p5c`/`.p5a` stub placeholder named directly in the list is checked under the real
  file it stands for, with a badge on the row and a count of how many matched in P5.

## Fixed

- A check that won through the new Restore-search fallback left the spinner and the
  live "P5 Barcodes: resolving…" display running indefinitely, even after the result
  had already appeared. Volume label and barcode are now resolved for these results
  too, and the fallback's own progress is shown live instead of one static message for
  the whole stage.
- A stub placeholder named directly in a path list previously read as "not archived" —
  P5 never indexed the sidecar's own filename, only the file it stands for.

## What to test

1. Drop a folder that's only findable through TSV inventories, P5 Archive Browser's
   catalogue, or imported-volume labels onto the main window — confirm Check finds it
   without any manual steps, and that the spinner stops normally once it does.
2. Tools ▸ Check Folder (via Restore Search)… on a large folder with RED camera media —
   confirm the per-file count matches a plain `find <folder> -type f | wc -l`.
3. Check a folder containing `.p5c`/`.p5a` stubs through either route — confirm each
   one is matched under its real name, not reported as missing.

Guide: [API beta guide](API-BETA-GUIDE.md).

> ⚠️ **Beta — test only.** Back up your data first. Delete, Archive and Restore are real
> actions. Provided as-is, with no warranty.
