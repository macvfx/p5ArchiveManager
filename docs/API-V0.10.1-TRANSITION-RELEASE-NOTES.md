# P5 Archive Manager API 0.10.1 — transition to version 4

Version: **0.10.1 (build 24)**

Release date: **2026-08-11**

> **Beta — test carefully.** Checking is read-only, but Delete and Archive are real
> actions. Use disposable data for destructive tests and review proof reports and
> receipts before removing local files.

The REST API rewrite was originally planned as P5 Archive Manager v4. Its temporary 0.x
prototype sequence reached 0.10 and made the relationship with CLI 3.x unnecessarily
unclear. This is the final 0.x build; the next API version is 4.0.

P5 Archive Manager API remains separate from P5 Archive Manager CLI. It keeps its API
bundle identifier, settings, interface, and REST workflow. Moving to 4.0 does not install
or convert the `nsdchat` app.

## What changed

- The updater accepts API releases tagged `0.x` or `4.x`, including prereleases, while
  continuing to ignore CLI `3.x` releases.
- A one-time explanation tells existing API users about the version transition.
- The main header and About window identify the REST API application without the obsolete
  generic "prototype" label.
- No archive-checking, deletion, or archive-submission behaviour changed in this bridge.

Install 0.10.1, then use **app menu ▸ Check for Updates…** after API 4 is published. The
updater opens the GitHub release page; it never downloads or installs automatically.
