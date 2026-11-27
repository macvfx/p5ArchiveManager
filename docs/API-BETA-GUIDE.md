# P5 Archive Manager API · User Guide

**v4.6.4 build 100 — pre-release beta.** Talks to the **Archiware P5 REST API v8**
(no `nsdchat`). It is separately installed from P5 Archive Manager CLI 3.x and has
different settings, workflow, and behaviour. The API app is the primary development
focus; both applications can remain installed while it is evaluated.

> ⚠️ **Beta — test only.** **Back up your data first.** Delete and Archive are real,
> destructive actions. Provided **as-is, with no warranty of any kind**. Test on
> disposable data and verify the receipts before trusting it with real projects.

Testers focusing on the new storage workflow should use the
**[v0.8 Phase 1 tester notes](API-BETA-V0.8-TESTER-NOTES.md)**.

---

## 1. What this app is for

**Goal:** quickly confirm whether the files on a disk folder are already archived in
P5, then act on that:

- **Archived & verified →** safe to **delete** from disk (P5 keeps the copy), with a
  receipt as proof.
- **Not archived →** optionally **archive** them to P5.

**Use case:** a project folder that gets archived and restored many times. P5 keeps
every past archive and won't clean up; you need to be sure the files on disk match
what's on tape *before* freeing space — and catch the odd new file that was never
archived. The app gives you per-file proof (disk size/date vs P5 size/date/tape) so a
delete is defensible.

---

## 2. First-time setup

Servers are managed in **Settings** (the **⌘,** window, or the **⚙️ gear** at the top-right
of the main window), so you can keep several P5
servers and switch between them.

1. Open **Settings** (⌘,) → **P5 Servers**. Use **Add** for a new server, then enter:
   - **Host/IP**, **Port** (usually `8000` for the REST API), **API** (`v1`)
   - **Username**, **Index** (e.g. `Default-Archive`)
   - **Password** → **Save** (stored in your Keychain, **per server**)
2. Click **Test Connection** → expect ✅.
3. (Optional) In the **Archive index search** section, toggle **Search all archive
   indexes** if a file might live in any index, not just the one named above.
4. (Optional) Under **Path mapping**, add the current local storage prefix and the path
   prefix recorded in this server's P5 index.

Back on the main window, the compact **server picker** at the top selects which server
the check runs against. Its connection row distinguishes **Connected** (green, with
latency and last-test time), **Authentication failed** (orange), **Server unreachable**
(red), and **Not tested** (gray). Use **Retest** after changing networks or server
settings. Re-open Settings any time to edit or add servers.

#### Import a server list (4.5)

If your servers are already set up in P5 Health Check, P5 Archive Search or P5 Archive
Overview, you do not need to type them in again. Those apps share a file named
`P5Servers.json`.

- **Settings ▸ P5 Servers ▸ Import Servers JSON…** — choose the file. Servers you do not
  have are added; ones already configured are skipped. Two entries count as the same
  server when host, port and username match, so renaming a server does not bring it back.
- **Export Servers JSON…** — saves this app's servers in the same format. The file holds
  host, port, protocol, username, API version and archive index. It never holds passwords,
  pinned certificates or path mappings.
- **At launch**, the app looks for `/Users/Shared/P5Servers.json` and `P5Servers.json` in
  your Documents folder. If one lists servers you do not have, a sheet shows the file's
  path and each server marked *New* or *Already configured*:
  - **Add New Servers** adds them.
  - **Not Now** asks again the next time the app opens.
  - **Ignore This File Version** stops asking until the file's contents change.

  Nothing is added without your choice.
- **After importing**, select each new server and save its **Password**. An HTTPS server
  also needs its certificate reviewed, as for a server entered by hand.
- On a new install, the blank "Default" server is replaced by the first import. Once you
  have edited it, it is kept.

#### Site settings file (4.5) — for administrators

One file can supply the settings that otherwise have to be typed into Settings on every
Mac: where the TSV inventories are, the path mappings, the historical locations. The app
reads the file and does not change it; the one exception is **Import Site Settings JSON…**,
below, which replaces it when you confirm. Deliver it however you deliver files (Munki, a
script, a copy) or import it on the Mac.

**Location:** `/Users/Shared/P5SiteSettings.json`. A complete example is in
[`examples/P5SiteSettings.example.json`](examples/P5SiteSettings.example.json). Every part is optional.

**Putting a file in place on this Mac.** **Settings ▸ General ▸ Site settings ▸ Import Site
Settings JSON…** — choose a file from anywhere. The app checks that it is a site settings
file, shows what it holds and where it will go, and on your confirmation copies it to the
location above (replacing a file already there) and loads it at once. A server list chosen
by mistake is refused. The button is disabled on a Mac where a configuration profile sets
the file's location or mode, since the organisation delivers the file there.

**Making the file from a Mac that is already set up.** **Settings ▸ General ▸ Site settings ▸
Export Site Settings JSON…** writes one from the current configuration:

- the TSV inventory folder and the current value of every on/off setting;
- one entry per server, with its archive index, path mappings, historical locations and
  imported volumes;
- with two or more servers, any mapping or historical location they *all* have is written
  once at the top, as site-wide.

Passwords, pinned certificates and server names are not written. Edit the file before
deploying it: remove any setting the site should not decide, and move a rule to the top
level by hand if it should apply everywhere. Pair it with **Export Servers JSON…**, since
a site file adds settings to servers but does not create them.

| Part | What it does |
|---|---|
| `settings` | App settings by name — see the list below. |
| `pathMappings` (top level) | Path mappings applied to **every** server. |
| `historicalRoots` (top level) | Historical archived locations tried for **every** server. |
| `servers` | Additions for one server: `archiveIndex`, more `pathMappings` and `historicalRoots`, `importedVolumesIndex`, `importedVolumeRoots`. |

A `servers` entry needs a `host`. Add `port` and `username` to narrow it to one
connection; the entry that names the most wins. An entry does not create a server — add
the server in Settings or import it from `P5Servers.json`.

**Setting names** (`settings`): `tsvInventoryFolder` (text), and these on/off values —
`searchAllIndexes`, `blockDeletePlans`, `tagSourcePath`, `autoCheckAfterDrop`,
`verboseLogging`, `restoreWholeRedClips`, `projectRestore.searchAllIndexes`,
`projectRestore.useBrowserCatalog`, `projectRestore.listImportedVolumes`,
`projectRestore.useTSVInventories`. On/off values are `true` or `false`, without quotes.

**How site values combine with yours**

- *Path mappings, historical locations, imported volumes:* added to yours, never replacing
  them. In **Settings ▸ Sources** yours stay editable and the site's appear beneath, marked
  with a lock. Both are used; the longest matching prefix still wins.
- *Archive index:* while the file gives a server an archive index, that one is used.
  Settings shows a note under the field.
- *Settings:* by default they are **suggestions**. A value applies if you have not set that
  setting, and follows later changes to the file, until you choose something else — after
  that your choice stays.

**Holding settings.** Two preferences, set by a configuration profile for
`misterx.P5-Archive-Manager-API` or with `defaults write`:

| Key | Value |
|---|---|
| `P5SiteSettingsMode` | `seed` (default, suggestions) or `enforce` (held: put back on every reload, and disabled in Settings with a lock) |
| `P5SiteSettingsPath` | Full path to the file, if it is not at the default location |

A profile can also lock one setting directly by forcing its preference key — for example
`p5.blockDeletePlans` set to true. That setting shows "Managed by your organisation".

To try it at a desk without a profile:

```
defaults write misterx.P5-Archive-Manager-API P5SiteSettingsMode enforce
```

**Checking it.** **Settings ▸ General ▸ Site settings** shows the file's location, whether
it loaded and what it supplied, whether settings are suggested or held, and any name in the
file the app did not recognise (a misspelt setting is ignored, and listed there). The file
is re-read when the app opens, when it comes to the front, and when Settings opens, so
replacing it needs no relaunch.

**Help & welcome guide.** On first launch the main window shows a short welcome panel.
The **Help** menu has **P5 Archive Manager Help** (⌘?) — getting-started steps and an
Advanced-tools explainer — plus **Show Welcome Guide Again** (also in **Settings ▸
General**). The **About** window (App menu) shows the version.

---

## 3. The main workflow

### Check a folder
- Confirm the selected server shows **Connected**. Before checking, the app requires a
  successful connection result no more than 60 seconds old and automatically retests a
  stale result. A failed preflight stops without classifying files as not archived.
- **Drag the folder onto the drop area** → it auto-scans by default (this is the fast
  path and enables the disk-vs-P5 comparison). Turn off **Automatically check after
  dropping a folder** in Settings ▸ General to review the path first.
- **Local folder to inspect** and **Archived P5 path** are independent. Edit the P5 path
  or use a saved mapping when files have moved to another storage root.
- Or **type a P5 path** and click **Check Archive Status** (P5-only, no disk compare).

#### Storage path mappings (v0.8)

Mappings belong to the selected P5 server. For example:

```text
Current local prefix: /Volumes/storageA
Archived P5 prefix:   Volumes/storageB
```

Dropping `/Volumes/storageA/Projects/Show01` derives
`Volumes/storageB/Projects/Show01`. The longest matching rule wins. The main window
shows the applied rule, and **Recalculate from dropped folder** restores its result after
a manual edit.

**Preview local path** is a temporary mapping calculator. Enter a representative full
current-local path to see the archived P5 path that the draft rules would derive. The
preview value is not saved, is not another mapping, does not select or read a real
folder, does not contact P5, and does not affect checks in the main window.

Mapping changes only the P5 lookup. Enumeration, delete safeguards, and archive
submission continue using the real local folder.

#### Historical archived locations (v0.10)

Mappings rewrite the current path **deterministically** — one dropped folder, one P5
path. But a folder may have been archived from somewhere you can't derive from its
current path: it was moved after archiving, or it lived on older storage over the years
(`MyGreatProject` is on `/Volumes/NAS1/Projects` today, but was archived from
`Volumes/ServerOld/Stuff` or `mnt/Primary/SharedNFS`).

For that, Settings has **Historical archived locations** — an ordered, per-server list
of older P5 storage roots, one per line. When a check finds **nothing archived** at the
current (or mapped) path, the app automatically looks for the dropped folder's **name**
under each location in order — case-insensitively, and across every index when *Search
all archive indexes* is on. A location only wins when the check **actually finds
archived files** there: a same-named folder that exists but holds none of these files is
noted and the search moves on to the next location.

- The result always says which location won and what else was tried.
- If no location has hits, the result lists everything tried — so **not archived** means
  "not archived anywhere the app knows about", not just "not at this path".
- The lookup is by the folder's **name** (its last path component), since the
  surrounding structure is exactly what changes between storage generations.
- A connection problem during the fallback probing is reported as *undetermined*, never
  as "not found".

It enumerates the files **on disk** and asks P5 only about the directories that hold
them — so a folder with a few files left checks in a moment, even if the archive holds
the whole project history.

#### Still nothing? Check tries Restore's own engine (4.4)

P5's REST API has no way to search by name or relative path — only an exact-path lookup
or a one-level listing. A label-rooted index such as Imported-Volumes, or media moved
before archiving into an unnamed wrapper folder, can defeat every path-based attempt
above even when historical locations are set up correctly, because none of it is a path
problem.

When the current path *and* every historical location find nothing, Check builds a path
list of every local file and runs it through **Restore from Project File's own engine**
— the same TSV/P5 Archive Browser search by name, imported-volume label prefixes, and
relocated-media walk described under *How each item is found*, below — then folds the
per-file results back into this window's result. It uses whatever Restore is already
configured to use (Settings ▸ TSV inventories, ▸ Imported volumes); nothing extra to set
up. The result says so when this is how it was found. **Tools ▸ Check Folder (via
Restore Search)…** (just below) runs that same engine directly, on demand, which is
faster when you already expect to need it.

### What 4.6.1 added to Check

**"Could not connect" but the server is fine.** The message now includes the reason macOS gave. If it
says *no route to host* and a browser can reach the server, macOS is probably blocking the app's
access to the local network: choose *Open Local Network Settings* (or open System Settings ▸ Privacy &
Security ▸ Local Network), switch P5 Archive Manager API off and on, and reopen the app. *Connection
refused* instead means nothing is listening at that address and port.

**Archived from a different storage.** If a folder dropped from one storage was archived from
another — say it is on `/Volumes/SAN/Projects/2017/Show` but P5 holds it under
`Volumes/NAS/Projects/2017/Show` — add a path mapping for each storage in Settings ▸ Sources
(for example `/Volumes/SAN → Volumes/SAN` and `/Volumes/NAS → Volumes/NAS`). When nothing is found
at the dropped path, Check swaps the storage root and keeps the rest of the path: the same relative
path under every other mapped storage first, then the dropped path's trailing folders (year and
project, then the project alone) under each historical location and mapping. You never add a year
folder to a mapping. Check Details ▸ *How this was determined* lists every location tried.

**Check Details is a summary with a window per part.** Open it from **Tools ▸ Check Details…** (or the
toolbar's list icon): it shows the counts for the last check and a button for each part — *How this
was determined*, *File provenance*, *Size matches (P5 overhead)*, *Size mismatches*, *Extra proof — entry handles*
and *Deep verify* — each of which opens in its own window, so a long list never holds up the others.
The file lists are shown a page at a time (200 rows) with a name filter; the complete list is in the
proof CSV.

**Where each file was found, and why.** Check Details ▸ *How this was determined* opens with the
answer — "1,737 of 1,737 files matched in P5, found at 2 locations" — then *Where files were
matched*, each location led by its count of matched files and why it was tried. The places that
were looked in and held nothing come after, in a collapsed *Looked in, nothing found* group, and
the path-mapping rules (applied or not) in a collapsed group below that. In the main window the
same answer is one grey line, "Matched at /… (1735) and 1 other location", with an ⓘ button that
lists every location, matched first, and any notes; orange is kept for a check that did not
finish. The same text is at the top of the proof report, which is now saved as soon as a
check finishes — you don't have to delete to get it. If a folder was archived from a different
storage, add that storage's mapping in Settings: its P5 side is tried as another location, and
only for files not already found.

**Path mappings and historical locations are two settings with two jobs.** A *path mapping* swaps the
start of the dropped folder's local path for a P5 path, so the check asks about the right place
**first**; if none matches, the dropped path is used as it is. *Historical archived locations* have
no local side — they are only searched **afterwards**, when the first path finds nothing or only some
of the files, trying the folder's path at several depths under each (and the P5 side of each mapping
is tried then too). Both feed the same list shown in Check Details ▸ *How this was determined*:
where files were matched first, then *Other places tried — none held these files*, which is not a
failure — the files were found elsewhere. Neither needs the other: the historical list works with no
mappings, and a mapping needs no historical location; a mapping simply makes the first guess right,
so a check costs one request instead of probing around.

**Handles (optional extra proof).** In Check Details, *Get handles & extra proof* asks P5 for
each archived file's entry handle and what P5 holds for it — instances, archive times, tapes
and barcodes. It adds a request or two per file, so it is on request (or switch on *Always get
handles after a check* here or in Settings ▸ Archiving ▸ Extra proof). A handle is shown only when P5 itself confirms it; with a TSV
inventory folder set in Settings you get the handle P5 minted at archive time. Run it before
you delete: the deletion receipt includes the handle only if it was fetched first.

**When handles are short.** Once a handles run finishes, Check Details ▸ Extra proof — entry handles
keeps the result and the time it took, and lists any archived files P5 did not confirm a handle for,
grouped by why (P5 does not list the path; P5 returned a handle it does not recognise; the run was
stopped first), each with what to do next. *Retry these* asks again for just those files, so a retry
takes seconds, not the whole run. *Copy the list*, *Show proof report* and *Show session logs* are
beside it. A file without a handle is not "not archived": the check's match stands, the handle is a
separate second confirmation.

**Tapes you can no longer read.** Settings ▸ Archiving ▸ *Tapes this server can no longer read — per
server* has a tick box for each LTO generation (LTO-1 … LTO-9). A library tape's barcode ends in its
generation (`…L6` is LTO-6), and a file whose only copy sits on a ticked generation is **not counted
as archived** and is **never offered for deletion**; the result says how many, how big, and why
(the orange box under the result, and *On unreadable tape* in the file list). A file with a readable
copy anywhere stays archived. Volumes with no barcode (disk, cloud, a tape in a standalone drive)
count as readable. The basic check only knows the one volume the listing names, so those files say
*other copies not checked*: *Check the other copies* in the handles window asks P5 for every copy, and
a file with a readable second copy is freed. Changing the setting re-judges the current result at once,
without asking P5 anything. The proof CSV has a *Not Counted (unreadable media)* column.

These files join the **Archive** action: the blue button counts them with the files not in P5, the orange
box has *Archive them again…*, and the archive sheet has a checkbox (on by default) to include them. The
old copies stay in P5. The **Delete** sheet lists them as not deleted. After archiving, run *Check Entry
handles* so the new copy on a readable tape frees them — the basic check only sees one tape per file.

**Temporary files.** Settings ▸ Archiving ▸ *Temporary files* has *Ignore known temporary files in a
check*, off by default. Office keeps a lock file (`~$Budget.docx`) next to a document while it is open,
and Windows leaves `Thumbs.db` and `desktop.ini`; none is project content, but each reads as "not
archived" and keeps *Safe to delete* off. With the option on, the next check leaves out `~$*`,
`~WRL*.tmp`, `Thumbs.db` and `desktop.ini` and nothing else. They are listed under the result (with why,
and their total size), in the proof report's *IGNORED TEMPORARY FILES* section and in the session log, are
counted nowhere, and are never deleted. Hidden files and `.DS_Store` are always skipped.

**Choosing which indexes are searched.** Settings ▸ Archiving ▸ *Search other archive indexes — per
server* has one control for the server shown: *This index only* (the server's configured index),
*All indexes* (every index P5 lists), or *Only the ones I choose*, which asks P5 for its indexes and
lets you tick them (the configured index is always searched first). A sentence under the control says
what a check will do. A server that has not chosen follows the older app-wide setting, so nothing
changes until you pick. Under *Last-resort search* you can switch the slow Restore engine off, or
choose which of its sources (TSV inventories, P5 Archive Browser's catalogue, imported-volume listing)
it uses.
The search also has a **time limit** (default 10 minutes; 0 for none): when it passes, Check stops
and the files it did not get to are shown as not checked — never as not archived — with a note
saying so. Stop works at any time. Progress shows elapsed time and, once it has enough to go on,
an estimate of the time left.

#### Slow or lost connection — retry and Resume (4.6.2)

A big folder takes hundreds of requests, so a P5 server that gets busy part-way can start
answering slowly and then time out. The check copes in three steps:

- **It eases off.** When a reply takes over 1.5 seconds the next request waits a moment, so a
  struggling server is not driven to a stop.
- **It retries.** A read that times out or is dropped is tried again on a fresh connection, up
  to three more times (after 3, 10 and 30 seconds). The window says "P5 is slow to answer —
  retrying…". Nothing that changes P5 (an archive submit) is ever retried.
- **It lets you resume.** If every try fails, the check stops — it never carries on and calls
  unchecked files "not archived" — but the folder listings already read are kept for 30
  minutes. The window shows how many, with **Resume Check** (reads only the folders not yet
  read) and **Start Over** (reads everything again). Resume applies only to the same server,
  folder, P5 path and index option, and is dropped after 30 minutes, on **Clear**, or when a
  normal check starts. A resumed result says so in its notes and the session log.

**Starting over.** **Clear** beside *Check Archive Status* (or the ✕ in the drop area) resets
the folder, the P5 path and every result. While a check is running the button becomes
**Stop & Clear**, which stops the check and clears once it has finished; plain **Stop** keeps
the partial result.

### Read the result

> **The check is disk-driven.** It compares the files **on disk** to P5, so the counts are
> always about your local files. A folder with no local files (e.g. they were already
> deleted) shows **0 archived** even though P5 still has them on tape — there's just
> nothing on disk to compare. To see what P5 holds at a path regardless of local files,
> use **Deep verify** (below) or **Browse** the index. *(v0.6.3 shows an inline hint when a
> check matches 0 files, pointing you to these tools.)*

- **Total files / Archived / Size** — for the files on disk.
- **Not archived / Needs archiving** — on disk but not in P5. *Needs archiving* also includes
  files found in P5 only on tapes you can no longer read; they have their own orange
  **Unreadable tape** count beside *Not archived*.
- **P5 Volumes / P5 Barcodes** (right-hand pills) — the tapes the files live on; volumes
  show `label · location · media type` where P5 reports them.
- **File provenance — disk vs P5 proof** — per file: disk size + mod date vs P5 size +
  archive date + volume/barcode (+ the **index** it was found in when searching all),
  with a verdict:
  - `✓ exact` — P5's size equals the disk size (rare: see below)
  - `✓ matched (+P5 overhead)` — P5's size is larger than the disk file by a small per-file
    overhead, up to 4,096 bytes; counted as archived. **This is the normal result.**
  - `⚠ size mismatch` — same name, but P5's size is larger by more than that, or the disk file is
    *larger* than P5's copy (changed since it was archived) (review; **not** deletable)
  - `＋ not archived` — P5 doesn't have it
  - `↪` marks a symlink; `✓ link matched` means P5 also holds it as a link entry (a link has no
    bytes to compare, and P5's REST API does not expose where the link points)

  **Why P5's size is a little larger — this is normal.** P5 stores every file with a small header
  and its metadata and reports the total as the file's size. In our testing on a P5 8.0.6 server an
  empty file is listed as 245 bytes and every other file as 257 bytes more than on disk
  (0 B → 245, 1 B → 258, 5,120 B → 5,377, 10,000 B → 10,257, 5 MiB → 5,243,137). Across 110 files
  matched in real proof reports the difference was always between 178 and 710 bytes — never zero,
  and P5 was never smaller than the disk file. So an archived file is almost never byte-for-byte
  equal, and a small positive difference is expected, including **+245 B on a zero-byte file**.
  Every row shows both sizes in exact bytes with the difference (`+447 B`), and the proof CSV's last
  column is that difference. **Units:** the app shows sizes the way Finder does (1 MB = 1,000,000
  bytes); P5's web page shows MiB (1 MiB = 1,048,576 bytes), so the same file reads smaller there
  (8,731,275 bytes is 8.7 MB in Finder and 8.33 MiB in P5). Comparisons always use exact bytes.

### Delete and Archive — the app's two main actions (4.3.2)
Delete and Archive sit together in the right column, under the tape pills, with equal
visual weight (red and blue) — Delete cleans up what's already archived, Archive gets
the rest archived so it, too, can be deleted later.

### Delete
The **Delete** button appears only when there are `exact`/`close` (proven-archived)
files. Clicking it does **not** delete immediately — it opens a confirmation sheet
(what will happen, the files in scope, proof-of-archive links, and typing **DELETE** to
confirm) so deletion is always a deliberate step:

1. **Deep verify entire P5 folder** — run a full scan to double-check before
   committing (see Deep verify below). From 4.6.4 the sheet shows its progress, with
   **Stop Deep Verify**, and **Delete waits for it** — the button reads *Waiting for Deep
   Verify…*. When it finishes, the sheet says how many of the files to delete it found in P5
   under the folder. Fewer than all is not an error when the check matched some files at
   another location or index; Check Details shows where.
2. **Open receipts folder** — review past deletion receipts.
3. **Type DELETE** to enable the delete button, then confirm — the irreversible
   action (red).
4. **Cancel.**

**An archive job still running (4.6.4).** When the sheet opens it asks P5 about the archive
jobs this app started for the folder. P5 lists a file once it is written, so the check already
proves the files archived, but the job keeps going after that: post-archive steps such as
preview generation read the original files on disk. While P5 reports such a job as running, the
sheet shows **ARCHIVE JOB STILL RUNNING** with the job numbers, and Delete stays disabled. Use
**Check Again** once P5's job monitor shows the job finished, or tick **Delete anyway**. A job
whose state P5 cannot report is mentioned but does not hold Delete up, and jobs started outside
this app (from P5 itself or another Mac) are not known to it.

**Proof BEFORE delete.** A **proof report is written before anything is deleted** — both
a **CSV** and a human-readable **TXT** listing every file with its disk size/dates vs P5
size/archive-date/volume/barcode and verdict, plus a **NOT ARCHIVED** section. You can
also write it any time with the **export icon in the toolbar** without deleting. All
reports + receipts live in
`~/Library/Application Support/P5ArchiveManagerAPI/Receipts/`.

When you proceed, it deletes **only** the verified files and **re-checks each file's
existence and size right before removing it** (anything changed since the check is
skipped and logged). It then writes a **deletion receipt** (in-app entry + `.md`) —
**Open receipts folder** (main window) reveals it.

**Progress.** After you type DELETE the sheet stays on screen and shows each stage — preparing
(the proof report is written first), deleting, writing the receipt and audit log, re-checking
the folder — with a progress bar, files removed and space freed so far, elapsed time and an
estimate of the time left. Deleting from a network share is slow, one round trip per file, but
the window stays responsive. The sheet cannot be dismissed while a delete is running.

**One-shot + auto re-check.** Once you delete, the Delete button **disables** (greys out,
relabels "Deleted — re-check to act again") so the same result can't be deleted twice, and
the app **automatically re-checks the folder** — the result then shows the post-delete
state. Run a fresh check to act again.

Recommended chain: **Check → (Deep verify) → review provenance → Save proof → Delete →
receipt.**

### Archive (the not-archived)
- When a check finds not-archived files, an **Archive** button appears right under
  Delete — the same weight, blue instead of red.
- Clicking it opens a confirmation sheet (mirroring Delete's own): **Load archive
  plans & clients**, pick a **Plan** + **Client**, then **Archive N Files**.
- Submits them to P5 and monitors the job briefly, about half a minute. A job that is still
  running after that is named in the status (4.6.4): writing to tape and post-archive steps such
  as previews take longer, and P5's job monitor shows when it finishes. The automatic re-check
  shows which files P5 already holds; Delete waits for the job.
- **Large archives go in parts (4.6.3).** P5's web server refuses a request bigger than about
  1 MB: it answers at once with HTTP 500 "Server Error", and the app showed *Archive submit
  failed*. Every file's full path goes into the request, and source-path tagging sends it
  twice, so a folder of a few thousand files is over the limit. When the request would be
  larger than **Largest request** (Settings ▸ Archiving, 800 KB by default), the sheet shows
  **REQUEST SIZE** with a checkbox, *Send in N parts*, ticked by default. It is the same
  switch as **Split large archives into several P5 jobs** in Settings. Each part is its own P5
  job, titled *… part 2 of 6: 1,150 files*, with its own receipt, and the window follows all
  of them. If P5 refuses a part, the app stops there: the parts already accepted keep running
  and nothing more is sent. The status names the jobs that started, so after they finish you
  can check the folder again and archive what is left. Untick the box to send one request; the
  sheet then warns that P5 will probably refuse it. Raise **Largest request** only if your P5
  server has been set to accept larger requests.
- **Files only on unreadable tapes (4.6.1).** When a server has LTO generations ticked as
  unreadable (Settings ▸ Archiving), files whose only copy is on one are counted in the button
  and the sheet shows a checkbox, on by default, to archive them again. Untick it to archive only
  the files not in P5. The Delete path never includes them. After archiving, the automatic
  re-check is the full check, with every mapped storage and historical location.
- **Filenames with emoji or other characters outside the Unicode Basic Multilingual
  Plane (4.3.3) can't be archived through P5's REST connection at all** — a confirmed
  P5 server limitation, not something this app can work around. The confirmation
  sheet lists any such file and leaves it out of the submission; everything else in
  the same folder archives normally. Use P5's own desktop client for a flagged file.
- **Named job + manifest (v0.5):** the job is submitted with the **full source folder path**
  as its title, so it appears in the **P5 job monitor** as the folder (not a generic "REST
  Archive job"). The accepted files (`path → P5 handle`) are recorded in the saved
  `archive-…-job.log` receipt as an **ARCHIVED ENTRIES** manifest.
- **Source-path tagging (v0.7, Settings ▸ Archiving, ON by default):** each archived file
  also records its **full original path** in the P5 index's per-file `description` metadata,
  so the archive is **searchable by source path** and the origin shows on the entry. Only
  applied when the plan's index has a `description` key (a P5 default), so it never blocks
  archiving. It sends each path twice, doubling the size of the archive request; large archives
  are sent in parts (4.6.3, above), so that is not a reason to turn it off. Turn it off if you
  don't want the app writing metadata into your index.
- **Plans that delete at the source (updated in 4.1):** a P5 archive plan can clean up
  after a successful job in two separate ways — remove the archived **files**, or remove
  the **files and their folders**. Either one marks the plan **"⚠ deletes files"** or
  **"⚠ deletes files and folders"** in the picker, with a matching warning on selection,
  in the confirm dialog and in Server info. Such a plan deletes **P5-side, without the
  app's proof/receipt** — for the proof-first workflow, archive with a plan that keeps
  your originals, then let the app delete (with receipt).
- **Block archive plans that delete at the source (4.1, Settings ▸ Archiving, ON by
  default):** while this is on, a plan carrying either delete setting can still be
  selected and inspected, but **Archive stays disabled** — the proof-first workflow is the
  only one available in the app. Turn it off to allow those plans; they remain flagged and
  still need confirming.
- **Client/path:** files are submitted as the **selected client** sees them. Pick the
  client that actually mounts the volume (e.g. `media-server`/`studio-mac` for
  `/Volumes/SharedSMB`; `localhost` for paths on the P5 server).
- **One-shot + auto re-check:** like Delete, the Archive button **disables after running**
  and the app **re-checks the folder** so newly-archived files move into the archived
  count. Note: P5 indexing can lag job completion — if a re-check still shows files as
  not-archived, the job is likely still finishing; re-check again a moment later.

### Deep verify (paranoid)
- **Deep verify — entire P5 folder** (Tools ▸ Check Details, or the toolbar's list
  icon — also offered as the first step of the Delete confirmation sheet) does a full
  recursive walk of *everything* P5 has under the path, listing it all with your
  on-disk files **highlighted**. Size matches and the full file-provenance list
  live in the same Check Details window (4.3.2) — the main window itself now shows
  only Delete and Archive plus the not-archived/size-mismatch/possible-match lists.
- **(v0.9)** It scans the server's **configured index** — or **every index** when *Search
  all archive indexes* is on, showing a per-index file count in the summary and labelling
  each entry with the index it was found in. While it runs, a live file count and running
  size tick up next to the spinner.

**Why run Deep verify when the check already said "archived"?** The two tools answer
different questions:

- The **check is disk-driven** — it asks P5 only about the files currently on disk.
  It answers *"are my disk files archived?"* fast, but it cannot see anything else.
- **Deep verify is P5-driven** — it lists everything the archive holds under the path.
  It answers *"what does P5 actually have here?"*

Use Deep verify when:

- **Before a delete** — confirm the archive really holds the whole folder (not just the
  files that happen to remain on disk) so freeing the space is defensible.
- **The check found 0 or fewer files than expected** — if the local folder was already
  partly deleted or restored elsewhere, the disk-driven check has nothing (or little) to
  ask about; Deep verify shows what's on tape regardless of the disk.
- **Hunting duplicates / earlier versions** — P5 keeps every past archive; Deep verify
  lists archive-only files that no longer exist locally (they show *without* the
  "on disk" highlight).
- **Cross-index doubt** — with *Search all archive indexes* on, the per-index counts
  show which index actually holds the folder (and whether copies exist in more than one).

### Restore from a project file (4.2)

**File ▸ Restore from Project File…** (⇧⌘R), or the button beside *Local folder to
inspect*, opens a separate window. Instead of dropping a folder, drop the timeline an
editor exported and the app works out which media it needs.

| File | From | What is read |
|---|---|---|
| `.xml` | DaVinci Resolve, Premiere (xmeml) | every `<pathurl>` |
| `.fcpxml` | Final Cut Pro | every `media-rep` of kind *original-media* (proxies are ignored) |
| `.fcpxmld` | Final Cut Pro (a folder) | the `Info.fcpxml` inside it |
| `.drt` | DaVinci Resolve timeline (a zip) | every `<MediaFilePath>` |
| `.txt` `.tsv` `.csv` `.log` | anything | one absolute path or `file://` URL per line, or per tab-separated field |

P5's own *media list* restore takes an XML or FCPXML directly, but not an `.fcpxmld`
or a `.drt`, and it does not know about RED clips.

**Tools ▸ Check Folder (via Restore Search)…** (4.4) builds a `.txt` path list for you:
pick a folder and it's enumerated and opened here already loaded — this is the route
for a label-rooted index such as Imported-Volumes, which the plain Check can't search.
Every file is checked individually (RED clip segments included, rather than folded
into one item the way a timeline is), and a `.p5c`/`.p5a` stub placeholder named in the
list is checked under the real file it stands for, with a badge on the row.

1. **Pick the server** at the top of the window. Paths from the project go through that
   server's **path mappings**, exactly as a dropped folder does.
   **Search all archive indexes** (on by default in this window) starts with the
   server's own index and then tries every other index P5 lists, until each item is
   found; a badge on the row names the index when it is not the server's own.
2. **Drop the file** (or *Choose File…*). The check runs straight away when *auto-check
   after drop* is on in Settings; otherwise click **Check Archive**.
3. **Read the list.** Each row shows P5's size and archive date on the right, and under
   it what to do, checked at the file's **original location** — the path the project
   names, usually on shared storage, as this Mac sees it:
   - **Needs to be restored — not in its original location**; or *— only a 0-byte
     placeholder*, *— only a link*, *— a different size*, or for a RED clip *— 3 of 44
     files* in its original location. Restore puts them back where they were.
   - **In its original location** (green) when it is already there in full.
   - **Not in its original location** (grey) for media P5 does not have — nothing to
     restore.

   The storage has to be mounted on the Mac running the check: an unmounted share reads
   as *not in its original location*. A request that failed shows as *Not checked*
   (orange) — never as *Not in P5*.
4. Rows that are archived and not already here in full are **pre-selected**. Use the
   *Show* filter and the checkboxes to change that. The list scrolls inside its own box;
   *Search options* folds away after a check (its one-line summary says what was used)
   and opens again with a click. The bar above the list holds *Select Needs Restore*,
   *Select None* and **Prepare Restore**.
5. **Prepare Restore** looks up each selected item's archive entry: how many versions P5
   holds (the latest is restored), when it was archived, and which tapes it is on —
   with each tape's online/offline state and P5 *location* field. Nothing is restored yet.
6. Choose where it goes and click **Restore** — the destination and the button sit at
   the top of the Restore section, above the prepared items (which scroll in their own box):
   - **Original location** — back to the path the project expects, so it relinks without
     work. Pick the P5 client that owns that storage.
   - **Into a folder** — a folder that already exists on the chosen P5 client (a path on
     that client, not on this Mac). Files keep their names; two selected files with the
     same name are refused rather than overwriting each other.
7. One P5 restore job is submitted and watched to the end, with its phase, the tape or
   drive it is waiting for, and the job report. **Cancel Job** asks P5 to stop it.

#### How each item is found

The app tries these in order and stops for an item as soon as one finds it. Every find
is confirmed with P5 before the row counts as archived.

1. **The server's index, then every other index** (with *Search all archive indexes*),
   at the project's path after your path mappings — one folder listing per folder.
2. **TSV inventories**, when a folder is set (*Settings ▸ TSV inventories*, or in the
   window). P5 exports one inventory per volume (tape), a `.tsv` named by volume ID; every
   `.tsv` in the folder and its subfolders is read, six- or eight-column. Each project
   file is looked up **by name**, and the row's **entry handle** is confirmed in one
   request — so media moved before archiving is found, and imported volumes too. Millions
   of rows take a few seconds; the files are only read. Does not need P5 Archive Browser.
3. **P5 Archive Browser's tape catalogue**, when P5 Archive Browser is on the same Mac
   (*Look files up in P5 Archive Browser's tape catalogue*, on by default). The same
   lookup by name from its database, which it builds from the TSVs imported there;
   read-only.
4. **Imported-volume roots** from *Settings ▸ Imported volumes*, as a fallback rule: each
   project path is looked up in the imported-volumes index once, without the volume's root, which
   is how P5 stores it.
5. **Listing the imported volumes**, for media moved before archiving. A project that says
   `…/Clients/‹client›/…` may have been archived from `…/Clients/To Archive/‹client›/…`, so no lookup
   at the project's path finds it. The imported-volumes index lists from a plain volume label, so
   for each volume the project's files were on, the app finds the labels that hold it, walks down the
   project's own folder names (looking one level inside each folder where the next one is not
   there, which is how a `To Archive` wrapper turns up) and confirms each path it arrives at with P5.
   It only reads, and it is bounded: a budget of about 600 listing requests, and at most 60
   folders looked into at one level. It needs the volume labels in *Imported volumes* (*Find
   imported volumes…* fills them in) and can be turned off there. This is the route that works
   through the REST API alone.
6. **Locations pasted from the P5 web app.** If P5 web shows where one of the project's
   files or folders is archived, paste that *Archive Location* here. The app lines it up
   with the project's paths from the end and re-roots every item through the folders that
   match — including copies of the same show folder on other drives.

Rows show where each item was found: the index when it is not the server's own, and the
tape or volume when an inventory placed it. A grey note under *Check Archive* says how
many were found which way.

**Imported volumes.** P5's *Imported-Volumes* index is rooted at each imported volume's **label**,
with the original `Volumes/…` path underneath. The P5 web app may show that folder as
`‹VolumeName›-‹uuid›`, but the uuid is not part of the name the REST API accepts, and the folder
only groups the media: `/archive/entries` wants the path **without** it, and every lookup that
included it failed on a live server. A listing does work from the plain label
(`inventory/‹Label›/Volumes/…`), but the index root and `Volumes` are 404, and P5 does not list the
labels.

To give the app the labels, use **Find imported volumes…**, in the *Imported volumes* box of Search
options in the Restore window, or in *Settings ▸ Imported volumes*. It tries each volume's label as
a top-level name in the index and lists the ones the index answers for, with the folders inside; it
only reads, and it has a Stop button. Tick the ones you want and add them. A label with no volume
record cannot be found that way, so **Add names by hand** takes a pasted list and checks each name
against the index. A label two volumes share is flagged. A pasted `‹VolumeName›-‹uuid›` counts as
the same volume as its plain label.

Finding an item does not need the labels: `/archive/entries` looks up an exact path with no root.
The labels are used by the rule-based pass, and to list a volume. The TSV inventory and P5 Archive
Browser's catalogue name each file's archived path directly. To check through the REST API alone,
turn both of those off in Search options. For a first restore of imported media, use **Into a
folder**. Prepare Restore and Restore into a folder work on items found by these routes (verified
live); where P5 puts an *original-location* restore of imported media has not been verified.

**RED footage.** A RED clip is a `.RDC` folder of `_001.R3D`, `_002.R3D`… segments, and
timelines name only `_001.R3D`. Restoring just that file gives a clip that stops after
its first segment. With **Restore the whole RED clip folder** on (the default), any
`.R3D` inside a `.RDC` folder is replaced by the whole folder: the row shows the folder,
how many segments P5 holds, and which segments the project named. On LTO this is also
one linear read instead of a series of single files.

Every restore is recorded **before** it is sent, in
`~/Library/Application Support/P5ArchiveManagerAPI/project-restores.json`, with the
job id added the moment P5 accepts it. A request that times out is reported as
*delivery uncertain* — check P5's job list before submitting again, because a second
submission is a second job.

### Browse the index (Tools ▸ Browse Index…)

Browse lists one level of an archive index at a time — the raw view of what P5 stores,
with the raw JSON response underneath for diagnostics. It's its own window (4.3.2),
reachable from the **Tools** menu. Use it when a check result looks off and you want
to see the index with your own eyes:

- **Roots (4.3.3)** jumps straight to a common starting point — `Volumes`, `mnt`, or
  any imported-volume root you've configured for this server (Settings ▸ Sources ▸
  Imported volumes) — instead of needing to already know the index's first path
  segment. **Browse from root**, **Up**, jump-to-path and **Go** still navigate from
  there; click a folder name to go into it.
- The **Index picker** chooses which archive index to list (defaults to the
  server's configured index; switching re-lists the current folder) — handy for
  confirming which index a folder actually lives in. The diagnostics line names the
  index and full URL of every request.
- Names P5 stores with caret-hex encodings (e.g. `\` as `^5c`) are navigable.
- **Server Info** (also its own Tools-menu window) shows its own raw JSON response for
  List clients / List archive plans now too (4.3.3), instead of it only appearing here.

---

## 4. Feature list (working)

- **Multi-server** manager in Settings (⌘,); per-server Keychain password; Test Connection.
- **Retry and Resume Check (4.6.2)** — slow or dropped reads are retried with back-off; an interrupted
  check keeps its listings for 30 minutes and resumes where it stopped.
- **Delete progress and Clear (4.6.2)** — live stage, bar, space freed and time left; Delete off the main
  thread; Clear / Stop & Clear resets the window.
- **Delete names its symlinks (4.6.2)** — "N files, M of them symlinks (pointers only)".
- **Size matching that follows P5 (4.6.2)** — P5's per-file overhead is expected; symlinks match P5
  links; exact bytes and the difference are shown.
- **Archived from several storages (4.6.1)** — a partial match is completed from every other
  mapped storage and historical location; *How this was determined* shows each step.
- **Tapes you can no longer read (4.6.1)** — per-server LTO generations whose files are not
  counted as archived, are never deleted, and are offered to Archive again.
- **Entry handles with next steps (4.6.1)** — grouped reasons, *Retry these*, kept time.
- **Check Details as a summary plus a window per part (4.6.1)**; lists paged; proof report
  written as soon as a check finishes.
- **Optional ignore of known temporary files (4.6.1)**, off by default, every ignored file listed.
- **Server list import and export (4.5)** — reads and writes the `P5Servers.json` shared
  with the other P5 apps; a file in `/Users/Shared` or Documents is offered for review at
  launch. No passwords in the file.
- **Site settings file (4.5)** — `/Users/Shared/P5SiteSettings.json` supplies the TSV
  inventory folder, site-wide and per-server path mappings and historical locations;
  settings are suggested or, with a profile key, held. Import and export from Settings.
- Main-window **P5 connection status** with latency, last-tested time, Retest, distinct
  authentication/unreachable states, and a required connectivity preflight.
- Fast **local-driven** disk-vs-P5 check (queries only relevant directories).
- **Multi-index search** (optional) — find a file in whichever archive index holds it.
- Live counters; steady result box.
- **Case auto-correction** (`TEST IN PROD` → `Test in Prod`); suggests siblings when a path
  segment isn't found. (The index root isn't listable — start paths from `Volumes`/`mnt`.)
- Drop derives the archived P5 path and auto-scans unless disabled; editing the P5 path
  keeps the local folder connected.
- **Per-server storage-path mapping (v0.8)** with validation, preview, longest-prefix
  selection, and explicit local/P5 evidence labels.
- **Size verification** with exact/close/mismatch verdicts; symlink detection.
- **Per-file provenance** list (the delete proof) — incl. volume location, media type, index.
- **P5 Volumes / Barcodes** pills, populated live; **persistent volume→barcode cache**.
- **Proof report (CSV + TXT)** — written before any delete and on demand.
- **Delete with receipt** (guarded, re-verified, audited); **one-shot + auto re-check**.
  Delete and Archive are the app's two main actions (4.3.2), each with its own
  confirmation sheet.
- **Historical archived locations (v0.10)** — per-server fallback list of older storage
  roots; a check with no hits automatically searches them in order and reports which
  location actually held the archived files.
- **Check for updates (v0.9.1+)** — daily on launch (silent unless an update exists) and
  via **app menu ▸ Check for Updates…**. The 0.10.1 bridge follows final API `0.x` and
  future API `4.x` releases, including prereleases, while ignoring CLI `3.x`.
- **Deep verify** full list with on-disk highlight; honours *Search all archive indexes*
  with per-index counts and live progress (v0.9). Lives in the **Check Details** window
  (4.3.2) alongside size matches and full file provenance.
- **Browse** the archive index + **raw JSON** viewer (diagnostics) — with an **index
  picker** and a **Roots menu** (4.3.3: `Volumes`, `mnt`, or configured imported-volume
  roots) to start exploring without guessing the first path segment.
- **Server info**: clients & plans (with names), volume-cache size + Clear, and its own
  raw JSON response disclosure (4.3.3).
- **Non-BMP filename detection (4.3.3)** — a file whose name contains an emoji or other
  character P5's REST connection can't address is flagged and excluded from an Archive
  submission, instead of failing the job or silently vanishing from one.
- **Settings is a sidebar of tabs (4.3.2)** — Servers, Sources, Archiving, Receipts &
  Mirror, General, Diagnostics & Logs, About — instead of one long scrolling form.
- **Restore from project file (4.2)** — XML, FCPXML, FCPXMLD, DRT or a path list →
  each item's archive status and original location → one restore job, with versions,
  tapes, the whole-RED-clip rule, TSV inventories and imported volumes. See *Restore from
  a project file*.
- Local **check history**.
- **Named archive jobs + manifest (v0.5)** — archive jobs carry the source folder path as
  their title (shown in the P5 job monitor); accepted files (`path → P5 handle`) saved to
  the archive receipt.
- **Source-path tagging (v0.7)** — each archived file records its full original path in the
  index's per-file `description` metadata (searchable; ON by default in Settings ▸ Archiving).
- **Special-character filenames (v0.6)** — files whose name contains a backslash (P5 stores
  it as `^5c`) are correctly recognised as archived, not falsely "not archived". *(v0.6.1:
  the Browse inspector can also navigate into backslash folders.)*
- **Session logs & diagnostics** — every API call, archive job step and error is written
  to a per-launch log; verbose on by default (Settings ▸ Diagnostics & Logs).
  **Tools ▸ Export Anonymized Logs for Support…** (4.6.3) bundles them for support with folder
  and file names replaced (see **§6 Troubleshooting**); **Zip Logs to Desktop (Not Anonymized)**
  keeps them as written, for your own use.

---

## 5. Beta status — what to test & known caveats

Please exercise these and report back (issues / what worked):

- **v0.8 storage mapping** — use the focused
  **[Phase 1 checklist](API-BETA-V0.8-TESTER-NOTES.md)** to test review-before-check,
  manual paths, saved mappings, overlap handling, persistence, and report paths.
- **Cross-check vs the shipping app** — run the **same folders** through both the v3.7
  nsdchat app and this beta; archived vs not-archived counts should agree.
- **Full delete chain on a throwaway folder** — check → proof report → delete → receipt;
  confirm the receipt is accurate and P5 still holds the files.
- **Archive submit on a disposable plan** — confirmed working live (every submitted
  file archived and deleted successfully across several runs); confirm the job runs
  on your own server and a re-check shows the files archived.
- **Job title + manifest (v0.5)** — after an archive, confirm the **P5 job monitor shows
  the source folder path** (not "REST Archive job"), and the saved `archive-…-job.log`
  lists each `path → handle`.
- **Special-character filenames (v0.6)** — archive files with a **backslash in the name**,
  then Check; they should report **archived** (not falsely "not archived").
- **Disk-driven check (don't be surprised by "0 archived")** — check a folder whose files
  are **still on disk**. If you check a folder whose files were already deleted, it
  correctly shows 0 (nothing on disk to compare) and points you to **Deep verify**. That's
  expected, not a bug.
- **Non-default index** — if your files live in an index other than the server's
  configured one, turn on **Settings ▸ Archive index search ▸ Search all archive indexes**,
  then re-check.
- **Logs capture the archive** — after an archive (especially one that misbehaves),
  export the logs (**Tools ▸ Export Anonymized Logs for Support…**) and confirm the session log
  shows the submit, raw response,
  job ID and poll states (see **§6**).
- **Edge cases** — multi-index (a file in a non-default index); size-mismatch handling on
  a re-saved `.drp`/`.drt`; symlinks.

Known caveats:

- **Archive the not-archived** writes to your P5 server — confirmed working live, but
  test on a **disposable/test archive plan** first. It submits the **local absolute
  paths**; those must be valid on the **client** you select.
- **Delete is real/destructive** — test on a **throwaway folder** first and check the
  receipt before using on real projects.
- **Filenames with emoji or other non-BMP characters can't be archived through P5's
  REST API at all** — a confirmed P5 server limitation (not this app). The Archive
  sheet flags and excludes them; everything else in the folder archives normally.
- **P5-overhead allowance = 4,096 bytes** for a size match (observed: 178–710). A file with unusually
  heavy extended attributes could exceed it and show as a mismatch until reviewed; the provenance
  list shows each exact difference.
- **Sub-directory case:** only the *base* path is case-corrected; nested folders use the
  disk's casing, so a nested folder whose case differs from P5 may show as not-archived.

---

## What's New

**Help ▸ What's New…** shows the release notes for every version, newest first. Each
release's headline feature sits on a highlighted card — marked **NEW** while it belongs
to the current release line — above that release's smaller changes. The window opens by
itself once after the app is updated; the Help window's *What's New* card opens it too.
The notes are the app's own `RELEASES.md`, bundled with it.

---

## 6. Troubleshooting — sending logs

If something doesn't work — most commonly **"I archived files but nothing happened"** —
the app keeps a detailed log you can send for diagnosis.

1. **Reproduce the problem** (e.g. select the plan + client and run the archive again).
2. **Tools ▸ Export Anonymized Logs for Support… (4.6.3).** The window lists what goes in:
   - **This app's session logs**, all of them (the app keeps the last 20).
   - **P5 server logs from this Mac**, when the app runs on the P5 server: P5's system log
     (`/usr/local/aw/log/lexxsrv.log`) and its web server's access log
     (`/usr/local/aw/servers/lexxsrv/modules/nslog/access.log`), which shows every request P5
     received and what it answered. By default only the files covering the days of your app
     sessions go in. Tick **Include all server log history** for a problem that built up over
     weeks. No administrator password is needed.
   - **Add Log Files…** for anything else, e.g. the server logs copied off another Mac when P5
     runs elsewhere.
   - **Names to replace**: client, project or company names that appear as plain text.
3. **Anonymize.** Every folder and file name becomes a token such as `N-7KQ2M4.mov` (the same
   name gets the same token everywhere, so the structure still reads), and so do index, pool,
   server, user and host names, IP and email addresses, and quoted values. Kept: timestamps,
   HTTP codes, sizes, timings, plan and job numbers, extensions, and a mark on any name with a
   character P5 is known to mishandle (`{+}`, `{trail-sp}` …). The originals are not changed.
4. **Review.** The window lists the words still in the logs that are neither ordinary English
   nor the app's own vocabulary. If one is a client, project, person or place name, type it in
   and choose **Add and Run Again**.
5. **Save Zip…** and email the zip to support. The **token map** that turns tokens back into
   names is saved on this Mac only, never in the zip. When support asks about a token, type it
   under **Look up a token**.

**Tools ▸ Zip Logs to Desktop (Not Anonymized)** still bundles the session logs exactly as
written, for your own use.

What's in the log:

- Every P5 API call and any network error.
- The full archive sequence: the submit request, P5's raw response, the **job ID**, each
  status poll, and the final result — including a clear line if no job was created (the
  usual cause of "it didn't archive").
- No passwords are ever written to the log.

**Verbose logging is on by default** (Settings ▸ Diagnostics & Logs), so the first report
already has full detail. If logs get large during big **Deep verify** scans you can turn
verbose off there — archive activity and errors are still always logged. **Tools ▸
Reveal Logs** opens the folder if you'd rather attach files yourself.

---

## 7. Where things live

- Receipts: `~/Library/Application Support/P5ArchiveManagerAPI/Receipts/`
- Session logs: `~/Library/Application Support/P5ArchiveManagerAPI/Logs/` (one `session-*.log` per launch)
- Token maps of anonymized log exports: `~/Library/Application Support/P5ArchiveManagerAPI/Log Exports/`
- Volume cache / history: `~/Library/Application Support/P5ArchiveManagerAPI/`
- Live Archiware P5 REST API docs: https://blog.archiware.com/redoc/p5_rest_api/awp5api.html

---

*Feedback: [reach out via GitHub](https://github.com/macvfx). © 2026 code.matx.ca — P5 Archive Tools for macOS & iOS.*
