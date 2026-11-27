# P5 Archive Manager API 4.6.4 (build 100) — Delete waits for a running archive job and for Deep verify

**Status:** pre-release beta · **Date:** 2026-11-27

> ⚠️ **Beta — test only.** Back up your data first. Delete and Archive are real, destructive actions.

### Delete waits until P5 has finished with the files

P5 lists an archived file in its index as soon as the file is written, so right after an archive
the check can already prove the files archived and offer to delete them. The job is not finished
then. Writing a large archive to tape takes a while, and after that P5 runs post-archive steps
such as preview generation, which read the original files on disk. Deleting during that step can
leave files without previews, or leave the job waiting.

- **The Delete sheet asks P5.** When it opens, it asks for the state of every archive job this app
  started for the folder (a large archive is several). While P5 reports one as running, the sheet
  shows *ARCHIVE JOB STILL RUNNING* with the job numbers and keeps Delete disabled. **Check Again**
  once P5's job monitor shows it finished, or tick **Delete anyway**.
- **A job P5 cannot report does not block.** For example, a job P5 no longer knows. It is named so
  you can look it up. Jobs started outside this app, from P5 itself or another Mac, are not known to
  the sheet; the check remains the proof that files are archived.
- **After archiving, the status says what is still running.** The app watches the jobs for about
  half a minute. A job still running after that is now named, with what it is likely doing, instead
  of "(still running — monitor in P5)".

### Deep verify in the Delete sheet

The sheet's **Deep verify entire P5 folder** button started a scan the sheet never showed. Delete
stayed available while it ran behind the sheet.

- **Progress and Stop.** While it runs, the sheet shows how many files it has found in P5 so far,
  with **Stop Deep Verify**, and the Delete button reads *Waiting for Deep Verify…*.
- **The answer.** When it ends, the sheet says how many of the files to delete it found in P5 under
  the folder. Fewer than all is expected when the check matched some files at another location or in
  another index; Check Details shows where.
- **No more overlap.** A check and a Deep verify use the same working state. A Deep verify still
  running when the re-check after a Delete started could disturb that re-check's result. Starting a
  check now stops a running Deep verify and waits for it; a Deep verify is not started during a check.

### Fixed while building this

- A reply from P5 that carries no job state, which is how it answers for a job it no longer knows,
  would have read as "running".

Confirmed live before this release: 4.6.3 archived 7,000 small files in 5 parts, and every file
re-checked as archived.
