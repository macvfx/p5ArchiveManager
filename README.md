# P5 Archive Manager (app)
Check a remote (or local) P5 server to see if a folder is archived with drag and drop ease. Check any custom archive index or the default. Delete diles with confidence. 

Note: to check local only servers and the Default-Index you can see the early version of [P5 Archive Check repo] (https://github.com/macvfx/p5ArchiveCheck)

![P5ArchiveManager-UI](https://github.com/user-attachments/assets/55d39389-f5ae-4026-8579-b1b1cfab8fab)


![macOS](https://img.shields.io/badge/macOS-14.0+-blue) ![Swift](https://img.shields.io/badge/Swift-5.9-orange) ![License](https://img.shields.io/badge/License-MIT-green)
## Features

- **Drag & drop** any folder to check if its files are archived on P5
- **Multiple server support** -- configure and switch between P5 servers
- **Custom Archive Index** -- use the default "Default-Archive" or specify your own
- **Live progress** -- real-time status updates showing each step of the check
- **Detailed reports** -- CSV with full P5 metadata (handle, status, size, archive date, volume, label, location, barcode)
- **Delete archived files** (v3.0) -- permanently delete local copies of files confirmed archived on P5, with multiple safety layers

## Overview
P5 Archive Manager is a macOS application that verifies whether files in a selected folder
have been archived by Archiware P5 in a local or remote P5 server in a custom Archive index or the Default-Archive index.

## How to Use
1. Open the P5 Archive Manager application.
2. Add a remote P5 server with "Managed Servers"
   - Configure a server name
   - Add the IP
   - Set the Port (default is 9001)
   - Add a user name and password (saved to keychain)
   - Select a P5 Archive Index (default is Default-Archive)
4. Select a server to use.
5. Drag any folder onto the main window.
6. Click on "Run Verification Check" to begin verification.
7. Note: You can drop files to check then select a server, which allows you to check various servers. 
8. Watch the live progress updates.
9. When complete, the csv of archived files and their metadata, or the list of files not archived, are listed in the app so you can open and inspect as needed

## Output Files
- A list of files NOT archived (if any).
- A CSV listing all archived files with metadata.
- A full log of the process.
- A backup tar.gz of all temp intermediate data fetched from P5.

## Delete Archived Files (v3.0)

After a successful check confirms that **100% of files are archived**, you can delete the local copies to free up storage space.

### How It Works

1. Enable the **"Delete archived files after check"** checkbox (optional -- enables auto-prompt).
2. Run an archive check. If all files are archived, a red **Delete Archived Files** button appears.
3. A confirmation dialog shows:
   - File count and folder path
   - Links to open the CSV report and log file as **proof of archive**
   - You must type **DELETE** to confirm
4. Files are **permanently deleted immediately** (not moved to Trash). This ensures reliable batch deletion on all volume types, including network storage.
5. A full deletion audit log is appended to the log file.

### Safety Layers

| Layer | Protection |
|-------|------------|
| Scope gate | Delete only available when 100% of files are archived |
| Opt-in toggle | Off by default, persists across sessions |
| Visual warning | Red-themed confirmation dialog |
| Proof review | Open CSV and log to verify archive status before confirming |
| Type to confirm | Must type "DELETE" to enable the button |
| Audit trail | Every deleted file logged with timestamp |

## Requirements
- macOS 14.6 minimum
- Archiware P5 server that will be checked --> remote or local as configured by your network
- Files archived in your custon set archive index or Default-Archive index 
- 'nsdchat' available at /usr/local/aw/bin/nsdchat
- Full Disk Access for `nsd` binary in /usr/local/aw/bin

## Changelog
- CHANGED in 3.0 -- File deletion option if all files checked are archived.
- FIXED in 2.9 - **Detailed progress messages** -- The app UI now reflects each individual step from the archive check script instead of showing a vague "Gathering metadata" message. Progress updates now show specific steps:
  - "Checking archive status..." with file count progress
  - "All files archived!" or "Some files not archived" result
  - "Gathering file details..." with sub-steps: fetching archive status, file sizes, converting sizes to GB, fetching backup timestamps, converting timestamps
  - "Gathering tape details..." with sub-steps: fetching volume information, tape barcodes, tape labels, tape locations
  - "Creating reports..." when generating CSV
  - "Finalizing..." when creating backup archive
- FIXED in 2.8 build 2 -- Sometimes the app would open a previous output file, new output folder fixes this
- CHANGED in 2.8 build 2 -- Output folder created by date and folder checked
- CHANGED in 2.8 -- Added P5 volume ID and location fields for each volume (i.e. tape) in output csv
- FIXED in 2.7 -- Show log file in Output files section from the start of checking
- CHANGED in 2.6 -- Configure a P5 Archive Index or use the default Default-Archive option
- *FIXED* in 2.6 (Issue only for 2.5 and below) -- Now checks files in the specified Archive index.
- FIXED in 2.4 -- Adding a new server would not show up until you left that section. Thanks to David Fox!
- CHANGED in 2.4 -- Text file of un-archived items or the csv of archived files no longer auto-open. Also thanks David.
- CHANGED in 2.4 -- minimum macOS is now 14.6 (this was required by a swift change to fix the server add bug)

## Known Issues
- KNOWN ISSUE -- UI window size needs to be manually re-sized occassionally depending on output files in the list 


