# P5 Archive Manager 3.7.1 (Build 5)

Released 2026-08-10 for the stable `nsdchat` edition.

## Reviewed server discovery

- `P5Servers.json` is discovered at launch without silently changing the saved server list.
- A review sheet shows the source file and each connection before anything is added.
- Choose **Add New Servers**, **Not Now**, or **Ignore This File Version**.
- Accepted and ignored file revisions are remembered by SHA-256 fingerprint, so an unchanged deployment file does not keep prompting or repopulate a server you removed locally.
- Connection identity uses host, effective nsdchat port, and username. The editable alias is deliberately excluded, so renaming an imported connection does not invalidate it.

Passwords are never read from or written to the JSON file. Enter credentials in the app after import; they remain in macOS Keychain.
