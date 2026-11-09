# P5 Archive Manager API 4.4.0 (build 62)

**Status:** Latest · **Date:** 2026-11-05

Check now finds folders that P5 can't locate by path alone.

- **Restore-search fallback.** When the current path and every historical location come
  up empty, Check tries Restore from Project File's engine (TSV inventories, P5 Archive
  Browser catalogue, imported-volume labels). No new settings.
- **Tools ▸ Check Folder (via Restore Search)…** opens Restore with a folder's file list
  already loaded; every file is checked individually.
- **Stubs.** A `.p5c`/`.p5a` placeholder named in a path list is matched under the real
  file it stands for.
- **Fixed:** the spinner and "P5 Barcodes: resolving…" no longer run on after a fallback
  result appears.

## What to test

1. Drop a folder findable only through TSV inventories or imported-volume labels onto the
   main window — Check should find it and the spinner should stop.
2. Check Folder (via Restore Search)… on a folder with RED media — the count should match
   `find <folder> -type f | wc -l`.

Guide: [API beta guide](API-BETA-GUIDE.md).

> ⚠️ **Beta — test only.** Back up your data first. Delete, Archive and Restore are real
> actions. Provided as-is, with no warranty.
