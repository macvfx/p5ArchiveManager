# P5 Archive Manager API 4.2.0 (build 42) — pre-release beta

**Status:** pre-release · **Date:** 2026-09-22 · **Tag:** `4.2.0+42`

One new feature: **Restore from Project File**. Drop the timeline an editor exported, see
which of its media P5 has archived and where, and restore what is missing — without
building a restore selection by hand.

Same application, same bundle identifier (`misterx.P5-Archive-Manager-API`), same saved
servers, mappings, history and receipts. Nothing needs re-entering.

---

## Headline: Restore from Project File

**File ▸ Restore from Project File…** (⇧⌘R), or the button beside *Local folder to
inspect*, opens its own window.

| File | From |
|---|---|
| `.xml` | DaVinci Resolve or Premiere (xmeml) |
| `.fcpxml` | Final Cut Pro — camera originals only; proxies are ignored |
| `.fcpxmld` | Final Cut Pro bundle (a folder) |
| `.drt` | DaVinci Resolve timeline (a zip) |
| `.txt` `.tsv` `.csv` `.log` | a list of paths |

P5's own media-list restore takes an XML or FCPXML, but not an `.fcpxmld` or a `.drt`.

1. **Check.** Each item is looked up in the P5 index — through the server's path
   mappings, across every archive index — and its original location on storage is
   checked. Rows say *Needs to be restored — not in its original location* (or a 0-byte
   placeholder, a link, a different size, or part of a RED clip is there), *In its
   original location*, or *Not in P5*.
2. **Prepare Restore.** For the selected items: how many versions P5 holds, when they were
   archived, which tapes they are on, and whether each tape is online, with P5's location
   field. Nothing is restored yet.
3. **Restore.** One P5 restore job, to the original location or into a folder on a P5
   client, watched to the end with its phase, the tape or drive it is waiting for, and
   the job report. Every attempt is recorded before it is sent and never retried
   automatically.

### RED clips come back whole

A RED clip is a `.RDC` folder of `_001.R3D`, `_002.R3D`… segments, and timelines name
only the first. Restoring what the timeline names brings back a clip that stops after
its first segment — in the test project, one clip had 43 segments. Any `.R3D` inside a
`.RDC` folder is now checked and restored as the whole folder (a setting turns this off).
On LTO this is also one linear read rather than a series of single files.

### Media that was moved before archiving, and imported volumes

Media is often moved before it is archived — into a *To Archive* folder, say — so the
project's paths no longer match P5's. Three ways to find it anyway, all optional:

- **TSV inventories** (*Settings ▸ TSV inventories*, or in the window). P5's per-volume
  inventory exports: each file is found by name, with its exact archived path and entry
  handle. Reading millions of rows takes seconds.
- **P5 Archive Browser's tape catalogue**, when P5 Archive Browser is on the same Mac —
  the same lookup from its database, read-only.
- **A location pasted from the P5 web app** — one known location shows how the project's
  folders were re-rooted, and the app applies it to every item.

**Imported volumes** (P5's *Imported-Volumes* index) work through all three. Verified on
a live server with a real Resolve timeline: all 53 items found, on one imported tape.

## What to test

1. A Resolve `.xml` or `.drt` and an FCPXML from your own projects: are the item counts
   right, and are proxies left out?
2. A project with RED footage: each clip should show its segment count.
3. **Prepare Restore**, then **Restore into a folder** on a P5 client, and check what
   lands. Restoring **imported** media has not yet been run end to end.
4. **Original location** restore on a clip whose original is safe elsewhere — it has
   not been exercised against a live server.

## Known limitations

- **Original-location restore is unverified**, and for imported media, where it lands is
  unknown. Use *Into a folder* first.
- **Only the latest version** of an entry is restored; older versions are shown but not
  selectable.
- OTIO, EDL, ALE and AAF are not read yet.
- Earlier releases: [API history](API-BETA-RELEASE-NOTES.md). How to use it: [User Guide](API-BETA-GUIDE.md), *Restore from a project file*.
