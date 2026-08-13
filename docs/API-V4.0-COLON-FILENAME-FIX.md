# Files with a colon in the name — what was wrong and what changed

**P5 Archive Manager API 4.0.0** · 2026-08-13
Plain-language version. See also the
[release notes](API-V4.0-RELEASE-NOTES.md) for the full test checklist.

---

## The short version

Files with a `:` in their name were reported as **"not archived" even when they were
safely archived**. That is fixed. Folders with a `:` in their name were affected even
more badly — nothing inside them could be found at all — and that is fixed too.

**Your files were never damaged, renamed, or lost.** They archived correctly the whole
time. Only the app's report about them was wrong.

---

## Why it happened

This comes from a 25-year-old quirk of the Mac, not from anything wrong with your files
or with P5.

On the original Mac, `:` was the character that separated folders in a path — the role
`/` plays today. When macOS moved to its current Unix foundations, the two characters
swapped jobs. To keep old files working, the Mac kept a translation layer: if a filename
contains a `:`, the Finder *displays* it as `/`, and vice versa.

So one file can honestly be described two different ways:

| Where you look | What you see |
|---|---|
| Terminal, and the actual bytes on disk | `Reel_01:23:45.mov` |
| Finder, and P5's file listing | `Reel_01/23/45.mov` |

Both are correct. It is one file with one name, shown through two different lenses.

P5 reports **both** forms. Our app was reading the display form and comparing it against
the real name from your disk. They never matched, so the file was declared missing from
the archive.

## Why it looked like P5 was renaming files

It genuinely looks that way from the outside, and that was the reasonable first reading.
It is not what happens.

We tested this directly: we archived files with colons to a P5 server, then restored
them. They came back **byte-for-byte identical, names included** — the colon still a
colon. P5 stores the name exactly as it is. The `/` only ever appears in P5's *reporting*
of the name, never in the stored file.

That is worth knowing for its own sake: **nothing in your archive needs re-archiving or
repairing because of this.** The archives were always correct.

---

## The second problem we found

While testing the fix we found something worse that nobody had reported yet, because the
first problem was hiding it.

If a **folder** had a colon in its name — `Shoot:Day1`, say — the app could not open that
folder in the archive at all. Every file inside it was reported as not archived, and the
Browse window could not go into it. This would have kept happening even after fixing the
filename problem.

Both are fixed in this release.

---

## What is different now

**Files and folders with colons are matched correctly.** They will now show as archived
when they are archived. If a folder previously showed a long list of "not archived"
files that you believed *were* archived, re-run the check — the list should be right this
time.

**New: "possible match" suggestions.** Sometimes a file on disk nearly matches something
in the archive but not exactly — it was renamed since archiving, or truncated, or a
different tool cleaned up a character. The app now points these out:

> Possible matches (1) — similar names in the archive; still counted as NOT archived,
> confirm by hand
>
> `Interview_Reel_A_Mastr.mov — possible match: Interview_Reel_A_Master.mov (96%)`

This is a **lead, not a verdict**. Deliberately:

- The file is still counted as **not archived**.
- It does **not** become safe to delete.
- The app will never quietly treat a near-match as a real match.

Deciding that two similarly-named files are the same file is a judgement call with real
consequences — if the app got it wrong and you deleted the original, the file would be
gone. So the app shows you the candidate and leaves the decision to you.

**Browse shows real filenames.** The archive browser now lists `colon:semi;.txt` — the
name you would see in Terminal — instead of the encoded `colon^2fsemi;.txt`.

---

## What to check after updating

1. **Re-check a folder that had unexplained "not archived" files.** Especially one with
   colons in names. The count should drop, possibly to zero.
2. **Re-check a folder inside a colon-named folder.** This is the case that was worst
   before.
3. **Before deleting anything**, confirm the folder now reports as fully archived and
   size-verified, exactly as you would for any other folder. The delete safety rules are
   unchanged — a "possible match" never makes a file deletable.

---

## Still to be fixed

**Filenames containing a backslash (`\`) cannot be archived through the app.** The
archive request fails, and it fails as a whole — the other files in the same request are
not archived either.

This is a separate, older issue on a different character. It affects *adding* files to
the archive, not checking them. Files with a backslash that are **already archived** are
detected correctly. A fix is planned for the next release.

If you have files with `\` in their names waiting to be archived, hold them back from
batch archive submissions for now, or rename them first.

---

## Questions you might reasonably ask

**Do I need to re-archive anything?**
No. The archives were always correct; only the reporting was wrong.

**Could this have caused me to delete something that wasn't archived?**
No — the error ran the safe direction. It reported archived files as *not* archived,
which meant the app refused to delete them and might have prompted you to archive them
again. It never reported an unarchived file as archived.

**Could I have archived duplicates because of this?**
Possibly, if you re-archived folders that the app said were incomplete. Duplicates are
harmless to your data but do consume space on tape. They will be identified correctly
from now on.

**Does this affect the CLI app?**
This release is P5 Archive Manager **API** 4.0.0. The separate CLI (nsdchat) app 3.x is
a different implementation and is not covered by this fix.
