# P5 Archive Manager API 4.6.2 (build 97) — A check that survives a slow P5, a Delete that shows progress, and size matching that follows P5

**Status:** pre-release beta · **Date:** 2026-11-23

> ⚠️ **Beta — test only.** Back up your data first. Delete and Archive are real, destructive actions.

### A check survives a slow or lost P5, and can be resumed

A big folder takes hundreds of requests, and a P5 server that gets busy part-way can start answering
slowly and then time out. Until now one timed-out request ended the whole check and everything it had
found disappeared.

- **It eases off.** When P5 takes over 1.5 seconds to answer, the next request waits a moment, so a
  struggling server is not driven to a stop.
- **It retries.** A read that times out or is dropped is tried again on a fresh connection, up to three
  more times (after 3, 10 and 30 seconds). The window says "P5 is slow to answer — retrying…". Nothing
  that changes P5, such as an archive submit, is ever retried.
- **It can be resumed.** If every try fails, the check stops — it never carries on and calls unchecked
  files "not archived" — but the folder listings already read are kept for 30 minutes. **Resume Check**
  reads only the folders not yet read; **Start Over** reads everything again. A resumed result says so.

### Delete shows what is happening, and never freezes the app

- **Deleting from a network share no longer freezes the app.** The delete ran on the main thread, so every
  check and removal on an SMB share stalled the window for the length of the delete. It now runs in the
  background. Other waits on a network share — the receipts mirror folder, stub clean-up after a restore,
  Restore from Project File, Check Folder (via Restore Search) — were moved off the main thread too.
- **The Delete sheet shows progress.** After you type DELETE it names the stage (preparing — the proof
  report is written first — deleting, writing the receipt, re-checking), with a progress bar, files removed
  and space freed so far, elapsed time and an estimate of the time left. It stays on screen to the end.

### Size matching follows how P5 reports sizes

P5 lists a file's bytes **plus a small per-file overhead** — its stored header and metadata. In our
testing on a P5 8.0.6 server an empty file is listed as 245 bytes and every other file as exactly 257 bytes
more than on disk (0 B → 245, 1 B → 258, 5,120 B → 5,377, 10,000 B → 10,257, 5 MiB → 5,243,137). Across 110
files matched in real proof reports the difference was always between 178 and 710 bytes — never zero, and
P5's size was never smaller than the disk file. So an archived file is almost never byte-for-byte equal,
and a small positive difference is **normal and expected**, including +245 B on a zero-byte file.

- **The rule.** A file matches when P5's size equals the disk size or is larger by up to 4,096 bytes. A disk
  file *larger* than P5's copy (it has changed since it was archived), or P5 larger by more than that, is a
  size mismatch and is never deleted. The old fixed 64 KB allowance let a 1 KB file match a 60 KB one.
- **Symlinks match P5 links.** P5 holds a symlink as a *Link* entry. A disk symlink now counts as archived
  when P5 holds a link of that name (shown "link matched"); before, every symlink was a mismatch, so an FCP
  library with links could never read as safe to delete. P5 does not say where an archived link points, so
  the match is by name and type; deleting such a link removes only the pointer.
- **Exact bytes.** Each file row shows the size the way Finder does (1 MB = 1,000,000 bytes) with the exact
  byte count beside it, then P5's size and the signed difference ("+447 B"). P5's own web page shows MiB
  (1,048,576 bytes), so the same file reads smaller there — 8,731,275 bytes is 8.7 MB in Finder and 8.33 MiB
  in P5. The proof CSV gains a *Size Difference* column, and the **Size matches** window explains all of this.

### Results first in Check Details

- **Check Details ▸ How this was determined** opens with the answer — "1,737 of 1,737 files matched in P5" —
  then each location where files were matched, led by its count. The places that held nothing follow in a
  collapsed group, *Other places tried — none held these files*, which is not a failure.
- **Path mappings and historical locations are explained.** A path mapping chooses the *first* place to
  look; historical locations are searched afterwards, when the first path finds nothing or only some of the
  files. The window, Settings and Help now say so.
- **The main window shows one grey line**, "Matched at /… (1735)", with an ⓘ button listing every location
  and any notes. Orange is kept for a check that did not finish.

### Smaller changes

- **The Delete count names the symlinks.** A folder of symlinks (an FCP library, say) reads "571 files, all
  symlinks (pointers only)" rather than hundreds of near-empty "files": P5 holds each as a Link entry, and a
  symlink's size on disk is only the length of its target path. Deleting one removes the pointer, never the
  file it points to. The main button, the Delete sheet and the receipt all say so.
- **Clear** beside *Check Archive Status* resets the folder, the P5 path and every result; during a check
  it becomes **Stop & Clear**. The ✕ in the drop area now clears the previous folder's results too, not just
  its path.
- The Check Details file filter (All / Not archived / On unreadable tape) is readable again — "All" had
  shrunk to a sliver.

### Fixes

- Right after a Delete removed everything, the re-check no longer searches other locations and the Restore
  search engine for files that are not there; it says "Nothing is left in this folder on disk…" at once.
- A symlink whose target is on an unmounted volume is no longer skipped as "missing" when deleting.
- The Delete sheet no longer turns back into the empty Type-DELETE sheet while the folder is re-checked
  after a delete or an archive.
- The Archive button could open as a tiny blank square on the first click; the Archive and Delete sheets
  now always draw.
- The main window's *Not archived* list can no longer show a count above an empty list or read "first 0".
- Check ▸ File provenance rows are no longer clipped on the left; the details wrap to the window.
- A folder dropped from under a symlinked location (for example `/tmp`, `/var` or an alias to a volume) no longer reads as entirely "not archived": every file's path came back as its full absolute path and matched nothing in P5.

Everything in 4.6.2 was tested through a run of test builds that carried the version 4.6.1 (builds 85 to 92); they are listed in the private changelog.
