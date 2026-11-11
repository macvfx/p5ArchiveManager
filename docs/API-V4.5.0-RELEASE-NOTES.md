# P5 Archive Manager API 4.5.0 (build 67)

**Status:** Latest · **Date:** 2026-11-10

Import and export the server list the other P5 apps use.

- **Import Servers JSON…** in Settings ▸ Servers reads a `P5Servers.json` and adds the
  servers this app does not have. Servers already configured are skipped.
- **Export Servers JSON…** saves this app's servers in the same format. Passwords, pinned
  certificates and path mappings are never included.
- **Review at launch.** A `P5Servers.json` in `/Users/Shared` or the Documents folder is
  offered when the app opens, showing which servers it would add. Choose Add New Servers,
  Not Now, or Ignore This File Version.
- **HTTPS is kept** whichever app wrote the file.
- **Site settings file.** `/Users/Shared/P5SiteSettings.json` supplies the TSV inventory
  folder, path mappings and historical locations, site-wide or per server. Your own mappings
  stay editable and the site's are added beneath them. Settings are suggestions by default;
  an administrator can hold them with a profile key. **Export Site Settings JSON…** writes
  the file from a Mac that is already set up, and **Import Site Settings JSON…** puts one
  in place. See the [API beta guide](API-BETA-GUIDE.md), "Site settings file".

## What to test

1. Export a server list from P5 Health Check that includes an HTTPS server, import it here,
   and confirm the server shows HTTPS and port 8443.
2. Put a `P5Servers.json` in `/Users/Shared`, open the app, and try each of the three
   buttons across launches. Ignore This File Version should stay quiet until the file is
   edited.
3. On a fresh install, import a file and confirm the blank "Default" server is gone.
4. Export from this app and import the file into P5 Archive Search and P5 Health Check.

5. In Settings ▸ General ▸ Site settings choose Export Site Settings JSON… and save to
   `/Users/Shared/P5SiteSettings.json`. Settings ▸ General ▸ Site settings should say
   Loaded, and Settings ▸ Sources should show the mappings again beneath yours with a lock.
   Then delete one of your own mappings: it should still apply, now from the file.
6. Drop a folder under a site-mapped prefix and confirm the derived P5 path uses the mapping.
7. Set `P5SiteSettingsMode` to `enforce`, bring the app to the front, and confirm the
   settings named in the file are disabled with a lock.
8. Delete the file and confirm your own mappings and settings are as you left them.

9. Save an export somewhere other than `/Users/Shared`, edit it, then use Import Site
   Settings JSON… to put it in place. Try importing a `P5Servers.json` too: it should be
   refused.

Guide: [API beta guide](API-BETA-GUIDE.md) · example site file:
[P5SiteSettings.example.json](examples/P5SiteSettings.example.json).

> ⚠️ **Beta — test only.** Back up your data first. Delete, Archive and Restore are real
> actions. Provided as-is, with no warranty.
