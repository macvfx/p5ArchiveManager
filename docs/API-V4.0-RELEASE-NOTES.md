# P5 Archive Manager API 4.0.0 (build 25) — pre-release beta

**Status:** pre-release · **Date:** 2026-08-13 · **Tag:** `4.0.0+25`

First release on the 4.x line, per
[`PRODUCT-LINEAGE-AND-VERSIONING.md`](PRODUCT-LINEAGE-AND-VERSIONING.md). This continues
the same API application — same name, same bundle identifier
(`misterx.P5-Archive-Manager-API`), same saved servers, mappings, history and receipts.
It does **not** convert the app into, or migrate it from, the separate CLI (nsdchat) 3.x
application.

The version number moves from 0.10.1 to 4.0.0 because the prototype numbering is
retired, not because the app was rewritten.

---

## Headline: files and folders with `:` in their names are matched correctly

Two defects, one root cause. Plain-language explanation, including what it means for
archives you already have:
[**What was wrong with colon filenames**](API-V4.0-COLON-FILENAME-FIX.md).

- **Files with a colon reported as "not archived" even when archived.** P5 returns two
  views of every name — the real bytes, and a Finder-style display form in which macOS
  shows a `:` as `/` and P5 encodes it as `^2f`. The check compared against the display
  form, producing a key containing a literal `/`, which cannot occur inside a filename
  and so matched nothing.
- **Folders with a colon were unreachable entirely.** Listing such a directory works only
  in P5's caret form; the raw and percent-encoded forms both return 404. Every file
  underneath was reported not archived, and Browse could not enter the folder. This was
  found while testing the first fix and would not have been solved by it.

**Nothing was ever renamed or lost.** Verified by restore: colon-named files come back
byte-identical, names included. Archives made before this release are correct and need no
repair.

## Also in this release

- **Possible-match suggestions.** Files that remain unmatched are compared against the
  archived names in the same folder, and close ones are surfaced as "possible match —
  confirm by hand". Advisory only: still counted as not archived, still not deletable,
  never auto-linked.
- **Browse shows real filenames** (`colon:semi;.txt`, not `colon^2fsemi;.txt`).
- **Update channel moves to 4.x only.** Installed 0.10.1 bridge copies still match both
  lines, so they will find this release.
- Removed a deep-verify alias key that could turn a real `^41` in a filename into a
  spurious `A` key inside delete-safety data.

---

## What to test

Priority order. Please report results against the fixture or against real project
folders — both are useful.

### 1. The fix itself (highest value)

- **A folder with colon-named files** that previously reported "not archived" — re-check
  it. Expect the count to drop, likely to zero.
- **A folder *inside* a colon-named folder** — the worst case before. Expect files to be
  found.
- **Colon variants:** leading (`:name.txt`), trailing (`name:.txt`), doubled
  (`a::b.txt`), colons beside spaces, and colons combined with accented characters.
- **Browse into a colon-named folder** and confirm the listing loads and names display
  with a real `:`.

To build a test folder by hand, create files from Terminal (not Finder — Finder will
turn a typed `/` into the colon for you, which is fine too, but Terminal makes the real
bytes obvious):

```bash
mkdir -p ~/p5-colon-test/"Shoot:Day1"
cd ~/p5-colon-test
echo x > "colon:semi;.txt"; echo x > "Reel_01:23:45.mov"
echo x > ":leading.txt";    echo x > "trailing:.txt"
echo x > "Shoot:Day1/take:01.mov"
```

Archive that folder, then check it. All five files should report as archived.

### 2. Regressions — things that worked before and must still work

- **Backslash filenames already in the archive** are still detected (this was the v0.6
  fix; it must not have been traded away).
- **Ordinary folders with no special characters** — counts, sizes and volumes unchanged.
- **Accented / non-ASCII names** (NFC vs NFD) still match.
- **Case-insensitive matching** still works.
- **Deep verify** and **Browse** still search the index you selected (the v0.9 fix).
- **Path mapping** rules still apply (v0.8).
- **Existing check history is still there after upgrading.** Please confirm explicitly —
  the saved-history format gained fields in this release, and it was written to migrate
  old records rather than discard them.

### 3. Delete safety — please be deliberate here

- A folder reporting fully archived and size-verified still offers deletion, and the
  receipt is still written.
- A file with only a **possible match** does **not** become deletable, and the folder
  does **not** report safe to delete.
- Size mismatches are still flagged and still block deletion.

> ⚠️ Delete and Archive are real and destructive. Test with disposable data.

### 4. Distribution

- Opens without a Gatekeeper warning on a Mac that has never run it.
- Runs natively on Intel as well as Apple Silicon.
- **Check for Updates…** works and now follows 4.x.

---

## Known issues

- **Filenames containing `\` cannot be archived.** P5 consumes the backslash unless it is
  doubled in the submitted path (Finding 3 of the API report), and the app does not
  double it. The whole submission fails, not just that entry. *Checking* backslash files
  already in the archive works correctly. Fix planned for the next release; this is a
  different character and a different code path from the colon work.
- **Saved history is loaded with a silent fallback.** If the history file cannot be
  parsed it is discarded without an error. This release was written to decode older
  records correctly, but the underlying fragility remains and is tracked.
- Archive and Delete remain explicitly beta.

## What is *not* fixed by this release

- Duplicates you may already have created by re-archiving folders the app wrongly
  reported as incomplete. They are harmless to data but consume tape. They will be
  reported correctly from now on; there is no automatic cleanup.

---

## Verification performed

- 96 automated checks against the app's real translation and matching code.
- Live run against P5 8.0.4: 16 of 16 fixture files matched, including inside a
  colon-named directory; the one withheld file reported not-archived with a 96%
  suggestion.
- Restore round-trip: colon-named files restored byte-identical, contents `diff`-clean.

What that means in practice is covered in
[What was wrong with colon filenames](API-V4.0-COLON-FILENAME-FIX.md).
