# P5 Archive Manager API 4.3.0 (build 45) — pre-release beta

**Status:** pre-release · **Date:** 2026-09-25 · **Tag:** `4.3.0+45`

Restore from Project File can now find a project's media in an imported-volumes index through the
REST API alone.

## Headline: imported volumes without the TSVs

On a real project file, **53 of 53** items were found in Imported-Volumes with the TSV inventories
and the P5 Archive Browser catalogue turned off. Prepare Restore and Restore into a folder were run
on items found this way and worked.

- **Find imported volumes…** (Restore window ▸ Search options ▸ Imported volumes, and
  Settings ▸ Imported volumes) tries each volume's label as a top-level name in the index and lists
  the ones the index answers for. **Add names by hand** takes a pasted list, each name checked.
- **Media moved before archiving** is found by listing the imported volumes for the project's
  folders, then confirming each path with P5. It is read-only and bounded (600 requests, 60 folders
  per level) and can be turned off.
- A volume that cannot be listed is reported as a warning.

## Fixed

- (Build 45) The results row no longer resizes: the **All** segment of the Show filter grew and shrank
  with the window and covered its label, and the four count tiles changed width as a check counted up.
  Both are now fixed width.

- A check through the REST API alone found nothing in Imported-Volumes: the lookup used a path form
  P5 refuses, and only worked after the TSV or catalogue route had taught the app the right one.
- The Show filter and the progress text no longer jump around.

## What to test

1. Turn off *Look files up in TSV inventories* and *Look files up in P5 Archive Browser's tape
   catalogue*, open *Imported volumes*, click *Find imported volumes…* and add what it finds.
2. Check a project file whose media was moved before archiving. Items should be found through
   *listing the imported volume …*.
3. Prepare Restore and Restore into a folder on one item.

Where P5 puts an original-location restore of imported media is still unverified.

Guide: [API beta guide](API-BETA-GUIDE.md), *Restore from Project File*.

> ⚠️ **Beta — test only.** Back up your data first. Delete, Archive and Restore are real actions.
> Provided as-is, with no warranty.
