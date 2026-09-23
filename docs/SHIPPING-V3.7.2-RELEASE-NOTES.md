# P5 Archive Manager CLI 3.7.2 (Build 6)

Released 2026-09-22 for the stable `nsdchat` edition.

This release separates the CLI app from the newer REST API app. Checking, deleting and
server discovery are unchanged from 3.7.1.

## Its own update channel

Update checks now look only at CLI 3.x releases. Earlier 3.x builds asked GitHub for the
newest release of any kind, so they could have offered the separate API app as if it were
an update to this one. From 3.7.2, the API app is never presented as an update.

## A clear name

The app now calls itself **P5 Archive Manager CLI** in its About window, Help menu and
headings, so it cannot be mistaken for the REST API app. The installed `.app` keeps its
name, so existing installs and deployment tools are unaffected.

## A note about the API app

A one-time, dismissible notice at launch says that P5 Archive Manager API exists: it uses
the Archiware P5 REST API instead of `nsdchat`, is where new development happens, and is
**still a beta**. It installs separately, so both apps can stay installed. This CLI app
remains the stable choice.

Choose **View API Releases**, **Remind Me Later** or **Don't Show Again**.
