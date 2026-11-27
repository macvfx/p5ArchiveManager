# P5 Archive Manager API 4.6.3 (build 99) — Large archives no longer fail with "Server Error", and logs for support are anonymized

**Status:** pre-release beta · **Date:** 2026-11-27

> ⚠️ **Beta — test only.** Back up your data first. Delete and Archive are real, destructive actions.

### A large archive is sent in parts

Archiving a folder of a few thousand files failed at once with *Archive submit failed — check the
plan/client and the raw response*. The response was an HTML "Server Error" page from P5's web server.

The cause is the size of the request. The app sends the whole list of files to P5 in one request,
and P5's web server (NaviServer) refuses any request body over its `maxinput` limit, 1 MB by default.
It does so before doing any work, in a few hundredths of a second. Two things make the list large:

- **Source-path tagging**, on by default since v0.7, sends every path twice: once as the file and once
  as its `description` metadata.
- **Every `/` in a path** is written as `\/` in the request.

In the field, 6,933 files came to a 4.24 MB request and 15,009 files to 9.25 MB; both were refused.
Every archive of 891 files or fewer, up to 0.40 MB, had worked. The behaviour was not new; the
folders were larger.

- **It splits by size.** The Archive sheet works out the size of the request when it opens. When it is
  over **Largest request** (Settings ▸ Archiving, 800 KB by default), a *REQUEST SIZE* section shows
  *Send in N parts*, ticked by default. Each part is its own P5 job, titled *… part 2 of 6: 1,150 files*,
  with its own receipt, and the window follows all of them.
- **A refused part stops the run.** The parts already accepted keep running, nothing more is sent, and
  the window names the jobs that started. When they finish, check the folder again and archive what is
  left.
- **You can turn it off.** Untick *Send in N parts* in the sheet, or turn off **Split large archives
  into several P5 jobs** in Settings ▸ Archiving; the sheet then warns that P5 will probably refuse the
  request. Raise **Largest request** only if your P5 server has been set to accept larger requests. A
  site settings file can hold the switch (`splitArchiveSubmits`).

Until now the workaround was to archive one subfolder at a time, which keeps each request small.

### Logs for support, anonymized, with the P5 server's own logs

**Tools ▸ Export Anonymized Logs for Support…** (also in Settings ▸ Diagnostics & Logs) prepares logs to
send to support without the client's folder and file names.

- **What goes in.** All of this app's session logs. When the app runs on the P5 server, P5's own system
  log and access log are offered too, for the days your sessions cover. The access log shows every
  request P5 received and what it answered, so a refused archive appears there as an HTTP 500. **Include
  all server log history** takes every file; **Add Log Files…** takes logs copied from another Mac. No
  administrator password is needed.
- **What is replaced.** Every folder and file name becomes a token such as `N-7KQ2M4.mov`, the same name
  always giving the same token, so the structure still reads. So do index, pool, server, user and host
  names, IP and email addresses, quoted values, and any name you type in. Kept: timestamps, HTTP codes,
  sizes, timings, plan and job numbers, file extensions, and a mark on any name holding a character P5
  is known to mishandle, such as `{+}` or `{trail-sp}`. The originals are not changed.
- **You review it first.** Before saving, the window lists the words left that are neither ordinary
  English nor the app's own vocabulary. If one is a name, add it and run again.
- **Tokens can be looked up on this Mac.** The map from token back to name is saved on this Mac only,
  never in the zip. When support asks about a token, type it under **Look up a token**.

**Zip Logs to Desktop** is now labelled *(Not Anonymized)*. It still saves the logs exactly as written.

Support reads the anonymized logs with a matching analyzer, which lines each failed archive up with what
the P5 server logged at the same moment.

### Also found

- **An index name saved with a trailing space** (seen in the same field logs) makes every check also
  search a copy of the index that P5 does not have. Each of those lookups returns 404: 10,281 of them in
  one set of logs. The app does not fix this yet; re-enter the index name in the server's settings
  without the space.

