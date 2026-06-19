# P5 Archive Manager

A macOS application that verifies whether files in a selected folder have been archived by Archiware P5, with support for local or remote P5 servers and custom Archive indexes.

# WARNING
Use with caution, if you choose to delete files that are identified as archived by P5 then you will actually delete files. Use this app only with proper Archiware P5 tape backups or other full backups in place. Only delete files if you are confident you can restore files as needed. We are not responsible for the files you choose to delete. 

Note: to check local only servers and the Default-Index you can see the early version of [P5 Archive Check repo](https://github.com/macvfx/p5ArchiveCheck)

## Editions

P5 Archive Manager comes in two builds:

| Edition | Version | Engine | Status |
|---|---|---|---|
| **Shipping** | **v3.7 build 2** | `nsdchat` (Archiware CLI) | **Stable** — recommended for everyday use |
| **API beta** | **v0.6.1** (preview of the upcoming **v4**) | Archiware P5 **REST API** | **Beta — ready for testing** |

- **v3.7 build 2 — shipping (nsdchat).** The current, stable app documented on this page. It talks to P5 through the `nsdchat` CLI and is the build to use for real work.
- **v0.6.1 — API beta (future v4).** A rewrite onto the Archiware P5 **REST API** (no `nsdchat` dependency): faster local-driven checks, optional multi-index search, per-file disk-vs-P5 proof, a proof-first delete that writes a receipt before anything is removed, and **per-session diagnostic logs you can zip and send** if anything misbehaves. **Ready for beta testing** → **[API Beta — User Guide](docs/API-BETA-GUIDE.md)**.

> ⚠️ **The v0.6.1 API build is a beta — test only.** **Back up your data before using it.** Delete and Archive are real, destructive actions, and the Archive-to-P5 write is still unproven against live servers. Provided **as-is, with no warranty of any kind** — test on disposable data and verify the receipts before trusting it with real projects.

### What’s new in the v0.6.1 API beta

Same job as the shipping app — confirm what's archived in P5, delete the proven-archived, **and** archive the rest — rebuilt on the **Archiware P5 REST API v8** instead of the `nsdchat` CLI bridge. Full details in the **[API Beta — User Guide](docs/API-BETA-GUIDE.md)**.

**What changed from nsdchat**

- **Transport:** P5 REST API over HTTP (via `curl`) instead of shelling out to `nsdchat` per call — fewer moving parts, no `nsdchat` dependency.
- **Faster checks:** local-driven and batched — enumerates the disk folder and queries only the P5 directories that hold those files, rather than per-file lookups.
- **Multi-server & multi-index:** manage several P5 servers (per-server Keychain); optionally search every archive index, not just one.

**What's new (the API makes possible)**

- **Per-file proof** — disk size/date vs P5 size/archive-date/volume/barcode/location/media-type, with an `exact` / `close` / `mismatch` / `not-archived` verdict per file.
- **Proof before delete** — a CSV+TXT report is written *before* anything is removed; deletes only verified files, re-checks each just before removal, saves a receipt (+ optional NAS mirror & audit log).
- **Archive the not-archived** — submit straight to a P5 plan/client and monitor the job.
- **Named archive jobs + manifest (new in 0.5)** — archive submissions now carry the **full source folder path** as the job title, so the P5 **job monitor shows the folder** instead of a generic "REST Archive job". The accepted files (`path → P5 handle`) are also logged and saved to the archive receipt as a durable record of what was archived.
- **Special-character filenames fixed (new in 0.6)** — files with a **backslash in the name** (which P5 stores internally as `^5c`) are now correctly recognised as archived instead of being wrongly reported as "not archived". Verified against a live server.
- **Browse handles backslash folders (new in 0.6.1)** — the Browse inspector (Advanced tools) can now navigate into folders whose names contain a backslash. Diagnostics-only; the Check/Delete/Archive workflow was already unaffected.
- **Session logging (new in 0.4)** — every API call, archive job step and error is written to a per-launch log. **Verbose logging is on by default**, so if anything misbehaves (e.g. an archive that doesn't archive) the log already captures the submit request, P5's raw response, the job ID and each status poll. Use **Receipts, audit & logs ▸ Zip logs to Desktop** to bundle it into a single `.zip` and send it in — no passwords are ever logged. Turn verbose off in **Settings ▸ Diagnostics** if logs get large.
- **One-shot actions + auto re-check**, plus onboarding (welcome guide, in-app Help/About).

**What to test**

- Run the **same folders** through both apps and compare: archived vs not-archived counts should agree.
- The **full chain** on a throwaway folder: check → proof report → delete → receipt; confirm the receipt is accurate and P5 still holds the files.
- An **archive submit** on a disposable plan; confirm the job runs and a re-check shows the files archived. Then check the **P5 job monitor shows the folder path** (not "REST Archive job"), and the saved archive receipt lists each `path → handle`.
- **Multi-index** on a file in a non-default index; **size-mismatch** handling on a re-saved `.drp`/`.drt`.
- **Special characters:** archive files that have a **backslash in the name**, then Check — they should show **archived** (not falsely "not archived").
- **Logging:** after an archive, **Zip logs to Desktop** and confirm the log shows the submit, response, job ID and poll states.

![P5ArchiveManager-UI](https://github.com/user-attachments/assets/55d39389-f5ae-4026-8579-b1b1cfab8fab)


![macOS](https://img.shields.io/badge/macOS-14.0+-blue) ![Swift](https://img.shields.io/badge/Swift-5.9-orange) ![License](https://img.shields.io/badge/License-MIT-green)

## Features — shipping app (v3.7 build 2, nsdchat)

> Looking for the REST-API build? See the **[API Beta — User Guide](docs/API-BETA-GUIDE.md)** (v0.3, preview of v4).

- **Drag & drop** any folder to check if its files are archived on P5
- **Multiple server support** -- configure and switch between P5 servers
- **Custom Archive Index** -- use the default "Default-Archive" or specify your own
- **Live progress** -- real-time status updates showing each step of the check
- **Detailed reports** -- CSV with full P5 metadata (handle, status, size, archive date, volume, label, location, barcode)
- **Delete archived files** (v3.0) -- permanently delete local copies of files confirmed archived on P5, with multiple safety layers
- **Partial delete** (v3.5) -- delete only the archived files even when some files are not yet archived
- **Delete diagnostics** (v3.5 build 3) -- the run log now records which output files were detected and whether the delete action was enabled or blocked
- **Broken symbolic link reporting** (v3.5 build 4) -- delete runs now flag broken symlinks, include them in the summary, and show the count in the app
- **Cancel check** (v3.5) -- stop an in-progress archive check at any time
- **Password status indicators** (v3.4) -- green/orange dots in the server dropdown and inline warnings when a server has no password saved
- **Server import port override** (v3.5) -- imported servers automatically use port 9001 (nsdchat) instead of the API port (8000)

## How to Use

1. Open P5 Archive Manager.
2. Click **Manage Servers** to add a remote P5 server:
   - Server name (display label)
   - Host IP address
   - Port (default: 9001)
   - Username
   - Password (stored in macOS Keychain)
   - Archive Index (default: Default-Archive)
3. Select a server from the dropdown. A green dot means the password is saved; an orange dot means it's missing — open **Manage Servers** to add one.
4. Drag a folder onto the drop zone.
5. Click **Run Archive Check** to begin. You can click **Cancel** at any time to stop the check.
6. Watch the live progress updates as the app checks each file.
7. When complete, review the results:
   - **Results Summary** -- total files, archived count, not archived count
   - **Output Files** -- click any file to open it

> **Tip:** You can drop a folder first, then switch between servers to check the same folder against different P5 instances.

## Output Files

| File | Description |
|------|-------------|
| Archived Files Report (.csv) | All archived files with full P5 metadata |
| Not Archived List (.txt) | Files not found in the P5 archive (if any) |
| Archived File List (.txt) | List of archived file paths (used by delete feature) |
| Backup Archive (.bak.tar.gz) | Backup of all intermediate data fetched from P5 |
| Log File (.log) | Full timestamped log of the entire process, including app-side diagnostics and deletion summaries |

All output files are saved to `/Users/Shared/{timestamp}-{folder name}/`.

## Delete Archived Files (v3.0+)

After an archive check, you can delete the local copies of files confirmed archived on P5 to free up storage space. Since v3.5, this works even when only some files are archived — un-archived files are always kept.

### How It Works

1. Enable the **"Delete archived files after check"** checkbox (optional).
2. Run an archive check. When archived files are found, a red **Delete Archived Files** button appears.
   - If all files are archived: "All X files confirmed archived"
   - If some files are not archived: "X of Y files confirmed archived" with a note that un-archived files will be kept
3. A confirmation dialog shows:
   - The number of archived files to be deleted
   - A warning about un-archived files that will NOT be deleted (if any)
   - Links to open the CSV report and log file as **proof of archive**
   - You must type **DELETE** to confirm
4. Files are **permanently deleted immediately** (not moved to Trash). This ensures reliable batch deletion on all volume types, including network storage.
5. A full deletion audit log is appended to the log file.
6. If the delete candidates include broken symbolic links, the log calls them out explicitly and the completed summary shows a broken symlink count.

### Safety Layers

| Layer | Protection |
|-------|------------|
| Scope gate | Only archived files are deleted; un-archived files are always kept |
| Auto-prompt gate | Auto-prompt only triggers when 100% archived; partial delete requires manual click |
| Opt-in toggle | Off by default, persists across sessions |
| Visual warning | Red-themed confirmation dialog |
| Proof review | Open CSV and log to verify archive status before confirming |
| Type to confirm | Must type "DELETE" to enable the button |
| Audit trail | Every deleted file logged with timestamp, plus app-side diagnostics about output-file detection and delete eligibility |
| Broken link visibility | Broken symbolic links are counted and identified in the deletion log instead of appearing only as generic failures |

## Server List Import & Export

P5 Archive Manager can share server configurations with other P5 Archive apps using a common JSON file.

### Auto-detection at launch

Place a file named `P5Servers.json` in either location and the app picks it up automatically on next launch:

- `/Users/Shared/P5Servers.json` — shared across all users
- `~/Documents/P5Servers.json` — current user only

### Import & Export buttons

In the **Manage Servers** panel (open via the **Manage Servers** button in the toolbar):

- **Import Servers JSON** — load servers from any `.json` file in the standard format
- **Export Servers JSON** — save the current server list to a `.json` file (passwords excluded)

Imported entries that already exist are skipped automatically. Imported servers have their port set to **9001** (nsdchat) regardless of the value in the JSON file, since other P5 apps use port 8000 for the REST API. After importing, edit each new server once to enter its password (stored in Keychain).

The JSON format matches the other P5 utility apps: `{ "servers": [{ "alias", "host", "port", "username", "apiVersion", "useHTTPS" }] }`.

## Requirements

- macOS 14.6 or later
- Archiware P5 server (local or remote)
- `nsdchat` available at `/usr/local/aw/bin/nsdchat`
- Files archived in your configured Archive Index or "Default-Archive"

## Known Issues
- KNOWN ISSUE -- UI window size needs to be manually re-sized occassionally depending on output files in the list 

## 2026 code.matx.ca - P5 Archive Tools for macOS & iOS
[For feedback, reach out via GitHub](https://github.com/macvfx) and [Support this project by optional donation](https://www.paypal.com/ncp/payment/ZX52VNS49SRZA)
