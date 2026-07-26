# P5 Archive Manager API Beta v0.9 — Release Notes

Version: **0.9 (build 17)**

Release date: **2026-07-25**

Focus: **Deep verify and Browse search the correct archive index**

> **Beta — test only.** Back up your data first. Folder checking, Deep verify, and
> Browse are read-only, but Delete and Archive are real actions. Use disposable data for
> destructive tests and verify the proof report before deleting anything.

## The defect this release fixes

The main folder check looks every file up in **every** archive index (when *Search all
archive indexes* is on), so it finds files wherever they live. Deep verify and Browse,
however, silently reused whatever index the previous operation happened to leave
selected internally. After an all-indexes check that leftover index was effectively
arbitrary — Deep verify could scan an index that doesn't hold the folder and report
**"0 files in P5 under this path"** while the check directly above showed the same files
as archived.

Every tool now chooses its archive index deliberately, and shows which one it used.

## What changed

- **Deep verify — deliberate index scope:** scans the server's configured index, or
  **every** index when *Search all archive indexes* is on. With multiple indexes the
  summary shows a per-index file count (e.g. `Default-Archive: 736 · ProjectArchives: 0`)
  and each entry row is labeled with the index it was found in.
- **Deep verify — live progress:** an increasing file count and running size appear next
  to the spinner while scanning, so long scans visibly make progress.
- **Browse — index picker:** choose which archive index Browse lists (names loaded from
  the server; defaults to the configured index; switching re-lists the current folder).
  The diagnostics line names the index in use.
- **Browse checked path:** one click starts Browse at the P5 path from the check above,
  and the jump field is pre-filled after every check — explore exactly what you just
  checked.
- **Clearer all-indexes result note:** the check's note now reports where archived files
  were actually found — `Searched 4 indexes — archived files found in: ProjectArchives
  (736)` — instead of only listing what was searched. When nothing matched, it names the
  index the path resolved in, if any.
- **P5-only checks** (typed path, no dropped folder) walk the index where the path
  actually resolved, not whichever index the server listed first, and the result names
  the single index walked.

## What was fixed

- Deep verify and Browse no longer inherit leftover index state from a previous check —
  the "check finds files but Deep verify/Browse show nothing" contradiction is gone.
- The check's internal index state is cleared on every exit, so no tool ever runs on a
  stale index again.
- Long Browse listings scroll inside their panel instead of drawing over the header
  controls.

## What to test

1. **Deep verify agreement:** check a folder whose files live in a non-default index
   (all-indexes ON), then run **Deep verify** — it should list those files, with a
   per-index count in the summary matching the check's note.
2. **Live progress:** deep-scan a large folder and confirm the file count and size tick
   up while the spinner runs.
3. **Browse picker:** after a check, open Browse — the picker defaults to the configured
   index; switching to the index that holds the folder lists it; the diagnostics line
   names the index.
4. **Browse checked path:** jumps straight to the checked folder.
5. **Result note:** an all-indexes check on an archived folder reports which index held
   the files; a never-archived folder reports "no archived files found in any".
6. **Regression:** single-index checks, Delete (proof + receipt) and Archive flows
   behave as in v0.8 build 13.

## Known limitations

- Deep verify walks indexes sequentially; scanning all indexes on a large server takes
  proportionally longer.
- `.p5a` and `.p5c` stub verification remains a separate Phase 2 investigation.
- Archive-to-P5 is still beta and must be tested with a disposable plan.

**Full user guide:** [`API-BETA-GUIDE.md`](API-BETA-GUIDE.md) ·
**Full API-beta history:** [`API-BETA-RELEASE-NOTES.md`](API-BETA-RELEASE-NOTES.md)
