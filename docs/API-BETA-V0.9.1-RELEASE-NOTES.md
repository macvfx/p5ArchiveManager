# P5 Archive Manager API Beta v0.9.1 — Release Notes

Version: **0.9.1 (build 18)**

Release date: **2026-07-25**

Focus: **Check for updates**

> **Beta — test only.** Back up your data first. Folder checking, Deep verify, and
> Browse are read-only, but Delete and Archive are real actions. Use disposable data for
> destructive tests and verify the proof report before deleting anything.

v0.9.1 is v0.9 (see the **[v0.9 release notes](API-BETA-V0.9-RELEASE-NOTES.md)** for the
Deep verify / Browse index fixes) plus automatic update checking.

## What changed

- **Check for updates** — the app now checks this repo's releases for a newer API-beta
  build: automatically once a day on launch (silent unless an update is available), and
  on demand via **app menu ▸ Check for Updates…** — same as the other macvfx apps.
- The check follows **only the API-beta release line** (tags `0.x`, including
  pre-releases). Releases of the shipping nsdchat app (tags `3.x`) in this same repo are
  ignored, so the beta can neither miss its own pre-releases nor false-alert on a
  shipping-app release.
- No file is ever downloaded automatically — the alert shows the release notes and a
  **Download** button that opens the release page in your browser.

## What to test

1. **Menu check:** app menu ▸ **Check for Updates…** — on the current build it should
   report "No Updates Found".
2. **Update alert:** when a newer `0.x` release is published, the same check (or the
   next launch) should offer it with its release notes; **Download** opens the release
   page.
3. **No cross-talk:** shipping-app releases (`3.x`) must never trigger an alert in the
   API beta.

## Included from v0.9 (build 17)

- Deep verify and Browse now search the **correct archive index** (per-index counts,
  index picker, Browse checked path, live scan progress). Full details:
  **[v0.9 release notes](API-BETA-V0.9-RELEASE-NOTES.md)**.

**Full user guide:** [`API-BETA-GUIDE.md`](API-BETA-GUIDE.md) ·
**Full API-beta history:** [`API-BETA-RELEASE-NOTES.md`](API-BETA-RELEASE-NOTES.md)
