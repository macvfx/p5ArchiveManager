# P5 Archive Manager API 4.6.1 (build 84) — Archived from several storages, tapes you can't read, and big folders

**Status:** Latest · **Date:** 2026-11-21

### A folder archived from several storages is found whole

A folder dropped from one storage that was archived from others used to read as mostly
"not archived" as soon as a few files matched at the current path. Check now completes the
picture.

- Each storage's root is swapped in and the rest of the path kept, so you never add a year
  or project folder to a mapping. Add one path mapping per storage in Settings ▸ Sources.
- Only the files still unaccounted for are asked about at each further location, and the
  numbers on screen only go up while it works.
- **Check Details ▸ How this was determined** lists every mapping rule and every P5 location
  tried, with what it gave. Each file records the P5 folder it was found in, and the proof
  report carries it.
- Settings ▸ Archiving has one control per server for which indexes are searched: this index
  only, all indexes, or only the ones you choose. The last-resort search has a time limit.

### Tapes you can no longer read

If your drives cannot read an older LTO generation, a file whose only copy is on one is not a
safe archive. Settings ▸ Archiving ▸ *Tapes this server can no longer read* has a tick box per
LTO generation, for each server.

- A library tape's barcode ends in its generation (`…L6` is LTO-6). Disk, cloud and
  standalone-drive volumes have no barcode and count as readable.
- Such files are not counted as archived and are never offered for deletion. An orange box
  shows how many and how big, and Check Details has an *On unreadable tape* filter.
- **They join the Archive action.** The blue button counts them with the files not in P5
  ("Needs archiving"), and the archive sheet has a checkbox, on by default, to archive them
  again. The Delete sheet lists them as not deleted.
- A file with a readable copy elsewhere stays archived. *Check the other copies* asks P5 for
  every copy of just those files and frees the ones that have one.
- Changing the setting re-judges the current result at once, and clearing it restores every
  count. Nothing is asked of P5 for that.

### Entry handles that tell you what to do next

- **Get handles & extra proof** asks P5 for each archived file's handle and what it holds:
  instances, archive times, tapes and barcodes. A handle shows only when P5 confirms it.
  Every file is looked up, with elapsed time and an estimate of the time left.
- When it finishes, the time it took stays on screen. Files without a confirmed handle are
  grouped by reason, each with a next step. *Retry these* asks again for just those files.
- **Always get handles after a check** is also in Settings ▸ Archiving ▸ Extra proof.

### Check Details and large folders

- **Check Details is a summary with a window per part**, so a long list never holds up the
  others. Lists are shown a page at a time with a name filter.
- A folder of 26,000 files or more is no longer cut off at 5,000, and "possible match" leads
  no longer take hours on a folder of image sequences.
- The proof report (CSV and TXT) is written as soon as a check finishes. The CSV has a
  *Volume Label* column beside *Volume*, and separate tape volume, label and barcode columns
  for the handles.

### Smaller changes

- **Ignore known temporary files** (Settings ▸ Archiving, off by default): Office lock files
  (`~$…`), Word `~WRL….tmp`, `Thumbs.db` and `desktop.ini` can be left out of a check. Every
  ignored file is listed under the result and in the proof report, and none is deleted.
- Tapes that are in no drive or slot show as `(OFFLINE)`, grouped, instead of P5's `<empty>`.
- Deletion receipts and the audit log now carry each tape's P5 label beside its volume id.

### Fixes

- After you archive or delete, the automatic re-check now uses the full multi-storage check.
  Before, it looked only at the first path and the numbers fell sharply.
- "Could not connect" now says why. If macOS is blocking local network access, there is a
  button to open that setting.
- The result no longer falls to zero while another location is being checked.


The 4.6.0 builds were never released; everything since 4.5.0 ships in 4.6.1.

## What to test

1. Drop a folder archived from several storages (one path mapping per storage). Check Details ▸
   How this was determined should list each location, and the counts should only go up while it works.
2. If your drives cannot read an old LTO generation, tick it in Settings ▸ Archiving. Files only on it
   should show in the orange box, count under Needs archiving, and not be offered for Delete.
3. Run Check Entry handles on a large result. Files without a confirmed handle should be grouped by
   reason, and Retry these should finish quickly.
4. Archive, then check the result again. The numbers should match the check you acted on.
5. Turn on Ignore known temporary files, check a folder with a `~$` file, and confirm it is listed, not
   counted and not deleted.
