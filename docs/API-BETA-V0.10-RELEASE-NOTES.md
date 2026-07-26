# P5 Archive Manager API Beta v0.10 — Release Notes

Version: **0.10 (build 22)**

Release date: **2026-07-25**

Focus: **Historical archived locations — automatic fallback search**

> **Beta — test only.** Back up your data first. Checking and the fallback search are
> read-only, but Delete and Archive are real actions. Use disposable data for
> destructive tests and verify the proof report before deleting anything.

## The workflow this release adds

Path mappings rewrite the current path **deterministically** — one dropped folder, one
P5 path. But folders survive storage migrations: `MyGreatProject` may sit on
`/Volumes/NAS1/Projects` today while its archive was made from `Volumes/ServerOld/Stuff`
or `mnt/Primary/JellyfishNFS` years ago — and after archiving, a folder may simply have
been moved to another spot on the same server. Until now the check could only answer for
the one path it was given.

**Settings ▸ Historical archived locations** is a per-server, ordered list of older P5
storage roots (one per line, saved with the path mappings). When a check finds **zero
archived files** at the current or mapped path, the app automatically looks for the
dropped folder's **name** under each listed location in order — case-insensitively, and
across every archive index when *Search all archive indexes* is on.

**Hits decide, not existence:** a location only wins when the full disk-vs-P5 check
actually finds archived files there. A same-named folder that exists but holds none of
these files is noted and the search continues to the next location.

The result always tells the story: which location won, what else was tried and why it
missed — so **"not archived" now means "not archived anywhere the app knows about."**
A connection problem during probing reports as *fallback status undetermined*, never as
"not found anywhere."

## What to test

1. **Moved folder:** archived from one path, later moved elsewhere — the fallback should
   find and verify it at the old path, naming the location in the result.
2. **Multi-generation:** archive lives under the second or third listed root — earlier
   locations should be tried, noted, and passed over.
3. **Same-named decoy:** a location with a right-named folder but wrong/no files — the
   search should note it and continue.
4. **Nothing anywhere:** a never-archived folder — the result should list every location
   tried.
5. **Regression:** a folder archived at its current path behaves exactly as before (no
   extra requests).

## Known limitations

- Files split across two historical locations are not merged — the first location with
  any archived hits wins.
- The fallback matches the folder by **name** (last path component); a folder renamed
  since archiving must be checked by typing its old path directly.
- Deep verify and Browse operate on the path shown in the result; they don't repeat the
  fallback search themselves.

**Full user guide:** [`API-BETA-GUIDE.md`](API-BETA-GUIDE.md) ·
**Full API-beta history:** [`API-BETA-RELEASE-NOTES.md`](API-BETA-RELEASE-NOTES.md)
