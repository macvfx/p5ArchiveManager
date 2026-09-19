# P5 Archive Manager API 4.1.0 (build 29) — pre-release beta

**Status:** pre-release · **Date:** 2026-09-18 · **Tag:** `4.1.0+30`

> ⚠️ **Beta — test only.** Back up your data first. **Delete and Archive are real,
> destructive actions.** Provided **as-is, with no warranty**. Test on disposable data
> and verify the receipts before trusting it with real projects.

Two areas changed: how the app talks to your P5 server, and how it handles archive plans
that delete your originals. Same application, same saved servers, mappings, history and
receipts — nothing needs re-entering.

---

## HTTPS support, with certificates you approve explicitly

P5 serves its REST API over TLS on port 8443 as well as plain HTTP on 8000. The app can
now use either, chosen per server.

- **Per-server protocol.** Each saved server carries its own HTTP/HTTPS setting. Existing
  servers keep what they had, including custom ports.
- **Certificate inspection and explicit trust.** A certificate can be inspected before it
  is used, and trust is something you grant rather than something assumed.
  **Forget Certificate** in Settings revokes it again.
- **No silent fallback.** Redirects are refused, there is no automatic downgrade to HTTP,
  and an archive submission is never replayed.
- **A changed certificate is its own error**, so a swapped certificate cannot be mistaken
  for a cancelled request.

P5's shipped certificate is a self-signed placeholder and will not validate against the
system trust store — which is why per-certificate trust exists.

Passwords also stopped travelling through command-line tools: the app now uses the
system networking and Security frameworks directly, so a password is never written into
a subprocess argument list. Existing saved passwords are preserved.

## Fixed: archive plans that delete *folders* were never flagged

A P5 archive plan can be configured to clean up after a successful job in two different
ways — remove the archived **files**, or remove the **files and their folders**. These
are two separate settings on the plan.

The app only ever looked at the first. A plan set to remove files *and folders* appeared
completely clean in the plan picker, gave no warning when selected and none in the
confirmation — and then removed the directory tree on the server.

Both settings are now read, and every warning says what the plan actually removes:
"deletes files" or "deletes files and folders". You will see it in the plan picker, on
selection, in the confirmation dialog, and in Server info.

## New: "Block archive plans that delete at the source"

**Settings ▸ Archiving · ON by default.**

When a plan deletes your originals, P5 does that itself — without this app's proof report
or receipt. The safe default is now to refuse such a plan rather than only warn about it.
The plan stays selectable so you can inspect it, but **Archive** is disabled and says
why.

Turn the setting off if you want those plans back; they remain flagged and still require
confirmation.

## Clearer archive confirmation

The confirmation before submitting an archive no longer says "mutates the server" — that
was developer jargon. It now says plainly that this starts a real archive job and writes
to P5 rather than checking it, and refers to the **files** you selected.

---

## What to test

This release has not been exercised against a live P5 server with saved credentials.
Most useful to try:

1. **HTTPS against a real server on 8443.** Inspect the certificate, grant trust, run a
   check. Then **Forget Certificate** and confirm the next request refuses rather than
   quietly falling back to HTTP.
2. **A saved password over HTTPS** — that your existing password is found, and Test
   Connection succeeds without re-entering it.
3. **A plan set to delete files and folders.** It should read **⚠ deletes files and
   folders**, and Archive should be disabled while the new setting is on. If it says only
   "deletes files", please report it.
4. **The setting turned off** — the plan becomes submittable again, still flagged.
5. **A normal archive on a plan that keeps your originals**, to confirm the ordinary path
   is unchanged.

## Known limitations

- **Plans that leave stub files cannot be told apart** from plans that delete outright.
  P5's plan information does not say which it does, so both appear simply as deleting
  plans.
- Job-monitor reporting and archive outcome reconciliation remain open work.
