# P5 Archive Manager API 4.6.1 (build 91) — Archived from several storages, tapes you can't read, and big folders

**Status:** pre-release beta · **Date:** 2026-11-23

### A folder archived from several storages is found whole

A folder dropped from one storage that was archived from others used to read as mostly
"not archived" as soon as a few files matched at the current path. Check now completes the
picture.

- Each storage's root is swapped in and the rest of the path kept, so you never add a year
  or project folder to a mapping. Add one path mapping per storage in Settings ▸ Sources.
- Only the files still unaccounted for are asked about at each further location, and the
  numbers on screen only go up while it works.
- **Check Details ▸ How this was determined** opens with how many files matched and where —
  each matched location led by its count — then the places that held nothing, then every
  mapping rule. The main window shows one grey line ("Matched at /… (1735)") with an ⓘ button
  for every location and any notes, instead of orange note text. Each file records the P5 folder it was found in, and the proof
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

- Deleting files from an SMB share no longer freezes the app. The delete ran on the main thread, so
  every file check and removal on the network share stalled the window; it now runs in the
  background and the progress counter keeps updating (build 85).
- The Delete sheet shows what is happening after you confirm: the stage, a progress bar, files
  removed and space freed so far, elapsed time and an estimate of the time left (build 86).
- Other waits on a network share no longer freeze the window: the receipts mirror folder's
  reachable check and copies, stub clean-up after a restore, Restore from Project File, and
  Check Folder (via Restore Search) (build 86).
- The ✕ beside the dropped folder now clears the previous folder's results too, not just the path
  (build 87).
- **Size matching now follows how P5 reports sizes (build 91).** P5 lists a file's bytes *plus* a small per-file overhead, so an archived file is normally a few hundred bytes larger in P5 than on disk (empty file → 245 bytes, other files +257 in our testing; 178–710 bytes across 110 real matches) — expected, not a defect. A file matches when P5's size is equal or larger by up to 4,096 bytes; a disk file *larger* than P5's copy, or P5 larger by more than that, is a mismatch (the old fixed 64 KB allowance let a 1 KB file match a 60 KB one). A disk symlink now matches a P5 link entry. Rows show exact byte counts beside Finder-style sizes, with the signed difference, and the proof CSV gains a Size Difference column.
- The Archive and Delete sheets always draw: Archive could open as a tiny blank square on the first click until you clicked again (build 90).
- The main window's "Not archived" list can no longer show a count above an empty list or read "first 0" (build 90).
- Check ▸ File provenance's All / Not archived / On unreadable tape filter no longer shrinks "All" to a sliver (build 89).
- A check that loses P5 part-way no longer starts from nothing: slow or dropped requests are retried, a slowing server is eased off, and if P5 still cannot be reached **Resume Check** reads only the folders not yet read (kept for 30 minutes) (build 88).
- The Delete sheet no longer turns back into the empty Type-DELETE sheet while the folder is re-checked after a delete or an archive (build 88).
- Check ▸ File provenance rows are no longer clipped on the left; the details wrap to the window (build 88).
- **Clear** button beside Check Archive Status resets the folder and every result; during a check
  it becomes **Stop & Clear** (build 87).
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
6. Delete archived files from a folder on an SMB share. The window should stay responsive and the
   "Deleting n of N" counter should keep climbing.
7. Confirm a delete and watch the sheet: it should name each stage, show the progress bar and time left.
8. After a check, press Clear (or the ✕ beside the folder): the status and counts should reset. During a check,
   press Stop & Clear and confirm the old result does not come back.
9. Interrupt P5 part-way through a big check (or wait for a timeout): the window should say P5 is slow and retry, and if it
   still fails offer Resume Check, which reads only the folders not yet read.
10. After a delete, the sheet should stay on "Re-checking the folder…" until the re-check ends.
11. Open Check Details ▸ How this was determined: it should open with "N of N files matched in P5" and the matched
    locations, with the places that held nothing in a collapsed group below. Open File provenance and confirm
    the All / Not archived / On unreadable tape filter shows all three choices.
12. Open Check Details ▸ Size matches: it should explain that P5's size is normally a few hundred bytes larger. In File provenance every
    row should show exact bytes and a difference such as +447 B. A file larger on disk than in P5 should be a size mismatch.
13. Click Archive several times, including right after a check: the sheet should draw every time.
