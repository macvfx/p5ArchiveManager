# P5 Archive Manager API 4.6.6 — The Archive sheet waits for its jobs

### No re-check, and no reset, while the archive jobs run

In the first live two-part archive on 4.6.5, both parts reached P5: one job started and the other
waited for a tape, as expected. The app watches new jobs for about half a minute. When that ended,
the sheet re-checked the folder while the jobs were still running, and then reset itself to an empty
form, asking for a plan and a client as if nothing had been sent.

Two things were wrong:

- **The re-check came too early.** P5 lists files as it writes them, so while a job is still writing
  most of its files read as not archived, and the window offered to archive them again.
- **The sheet lost what it knew.** When the re-check published its result, the part of the window
  that holds the sheet was rebuilt, and the sheet with it. Its plan, client and *submitted* state were
  gone, and the form could have been sent a second time.

Now:

- **When the jobs are still running**, the sheet stays open as *Archive submitted*, with the jobs,
  their report and a **Close** button. The folder is not re-checked. The main window says *Archive
  submitted — re-check to act again*. Check the folder again when P5's job monitor shows the jobs
  finished.
- **When the jobs have finished** within that half-minute, the app re-checks the folder as before.
- **The Archive sheet warns** when an archive job this app started for the folder is still running,
  and holds Archive until it ends (**Check Again**, or **Archive anyway**), as the Delete sheet
  already did. A re-check by hand mid-job can no longer lead to archiving the same files twice.
- **If P5 refuses the first part**, nothing was started, so the form stays, with the reason shown,
  for another try.
