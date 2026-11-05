# P5 Archive Manager API 4.3.4 (build 59) — pre-release beta

**Status:** pre-release · **Date:** 2026-11-05 · **Tag:** `4.3.4+59`

A correctness fix for the archived-file count, plus two quick filters for the detail
windows that make sense once you have hundreds of files in front of you.

## Fixed: a fully stub-ified folder reported "none of these files are archived"

When a folder's local files are `.p5c`/`.p5a` stub placeholders that P5 still matches by
name, the **Archived** count stayed at 0 and the main window showed "None of the N files
on disk are archived here" — even though the per-directory proof correctly showed, say,
526 of 531 stubs matched in P5. The top-level archived count only tracked ordinary
exact/close/mismatch matches, never a matched stub, so the two summaries disagreed with
each other. Matched stubs now count toward Archived, and toward the P5 Volumes and
archive-date range shown for the check — a stub's own placeholder size is still never
counted as deletable, that part is unchanged.

## Added

- **Check Details ▸ File provenance** has an All / Not archived filter, so a long
  provenance list jumps straight to what still needs attention.
- **Deep Verify's "Everything P5 has here" list** has a name filter — useful once that
  list runs to hundreds or thousands of entries.
- Section headers in Check Details and the main result now sit on a shaded panel so each
  section reads as a distinct block in a long scroll, instead of blending into the file
  list under it.

## What to test

1. Check a folder whose local files are entirely `.p5c`/`.p5a` stubs matched in P5 —
   confirm Archived shows the matched count (not 0) and the "none of these are archived"
   callout does not appear.
2. In Check Details, use the file provenance All / Not archived filter on a check with a
   mix of archived and not-archived files.
3. Run Deep Verify on a path with a few hundred entries and confirm the name filter
   narrows the list as you type.

Guide: [API beta guide](API-BETA-GUIDE.md).

> ⚠️ **Beta — test only.** Back up your data first. Delete, Archive and Restore are real
> actions. Provided as-is, with no warranty.
