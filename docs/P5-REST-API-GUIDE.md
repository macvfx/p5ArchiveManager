# Using the Archiware P5 REST API — what we call, and why

A practical guide to the **Archiware P5 REST API** (v8), based on how **P5 Archive
Manager**'s API beta uses it to check whether files are archived and to submit new
archive jobs. Intended to help anyone else building against P5 get oriented faster than
the [full API reference](https://blog.archiware.com/redoc/p5_rest_api/awp5api.html) alone
provides.

This is a usage guide, not a reference — for the complete endpoint/schema list, always
check the live docs above; P5 versions can add fields or change defaults.

## The basics

- **Base URL:** `http://<host>:<port>/rest/<version>/...` — the path version is `v1` even
  on a P5 v8 server. The REST *path* versioning and the *server* version are different
  numbers; don't assume they match.
- **Auth:** HTTP Basic auth (username/password of a P5 user with API access).
- **Format:** JSON request/response bodies; most list endpoints also accept an `/{id}`
  suffix to fetch a single item instead of the collection.
- **Read vs. write:** browsing indexes, clients, plans, and jobs is all `GET` and has no
  side effects. The only "write" most apps need is submitting an archive (or restore) job.

## Checking what's already archived

P5 archive indexes work like a filesystem-shaped catalog. To find out whether a given
local file is archived, you query the **inventory** of an index at the matching path —
you generally don't search by filename across the whole archive.

| Endpoint | Purpose |
|---|---|
| `GET /archive/indexes` | List the archive indexes available on the server |
| `GET /archive/indexes/{index}/inventory/{path}` | List entries at one directory level of that index |
| `GET /general/volumes/{id}` | Resolve a volume ID (returned on inventory entries) to its label, barcode, location, and media type |

The practical pattern: walk the **local** folder you care about, and only query the P5
directory levels that correspond to it — recursing into subfolders as needed. This is far
cheaper than trying to enumerate or search an entire index, and it's how P5 Archive
Manager's check works. A file is judged "archived" when an inventory entry with the same
name exists at that path; comparing sizes lets you flag an exact match vs. a mismatch
worth a second look.

If a server has more than one archive index, there's no cross-index search endpoint —
you check each index's inventory in turn for the path in question.

## Submitting an archive job

Archiving is done by creating an **archive selection** against a chosen **plan**, scoped
to a **client**.

1. `GET /general/clients` — list clients (a "client" in P5 terms is the machine/filesystem
   whose paths you're submitting; the files are interpreted *as that client sees them*).
2. `GET /archive/plans` — list archive plans (each plan has its own index, schedule, and
   options — e.g. whether it deletes the source after a successful archive).
3. `POST /archive/plans/{planID}/archiveselections` — create the selection and run it.

```
POST /rest/v1/archive/plans/{planID}/archiveselections
Headers:
  client: <clientID>     # required — whose filesystem the paths below belong to
  time: now               # start immediately instead of waiting for the plan's schedule
  Content-Type: application/json

Body:
{
  "paths": [ { "path": "/absolute/path/to/file1" }, { "path": "/absolute/path/to/file2" } ],
  "description": "My human-readable job title"
}
```

A few things worth knowing that aren't obvious from a quick read of the schema:

- **`description` sets the job title.** Without it, jobs created this way all show up in
  the P5 job monitor as a generic "REST Archive job" with no indication of what they
  contain. Setting `description` to something meaningful (e.g. the source folder path) is
  the single most useful thing you can do to keep REST-submitted jobs auditable alongside
  GUI-submitted ones.
- **The response includes per-file handles.** `entries[].handle` gives you a durable
  `ArchiveEntry` handle per accepted path — this is what P5 uses internally to reference
  that archived file later (for restore/search). It's worth logging or persisting
  alongside your own record of "what did we just archive," since the job ID alone doesn't
  tell you which files succeeded.
- **`paths[].meta`** lets you attach metadata key/value pairs to each path at archive
  time (e.g. a provenance tag like the file's original source path), which then becomes
  searchable in the index. The keys must already exist on the index — create them first
  with `POST /archive/indexes/{indexID}/keys` if needed.

## Monitoring a job

| Endpoint | Purpose |
|---|---|
| `GET /general/jobs/{id}` | Poll job status (queued/running/done/error) |
| `GET /general/jobs/{id}/report` | Human-readable progress/result text |
| `GET /general/jobs/{id}/protocol` | Fuller completion log, supports `format=json` or `format=xml` |
| `GET /general/jobs/{id}/inventory` | The list of files the job processed — written to a file on the named client, not returned inline |

For a short-lived submit-and-confirm flow, polling `/general/jobs/{id}` every couple of
seconds until it leaves the running state is usually enough; reach for `/report` or
`/protocol` if you need to show or store what actually happened.

## A quirk worth knowing: special characters in names

P5 stores certain special characters in archived names/paths using **caret + two hex
digits** — `^XX`, where `XX` is the byte's hex value. For example, a literal backslash
(`0x5C`) is stored as `^5c`. The P5 web GUI decodes this back to the literal character for
display, but the REST API returns the encoded form. If you're matching names returned by
the API against names on disk (or names you're building requests with), decode `^XX`
sequences back to the literal byte before comparing — otherwise an archived file with a
backslash, or another encoded character, in its name will look like a non-match.

## Quick reference

| Purpose | Method & endpoint |
|---|---|
| List archive indexes | `GET /archive/indexes` |
| Browse an index's inventory | `GET /archive/indexes/{index}/inventory/{path}` |
| Resolve a volume (label, barcode, location) | `GET /general/volumes/{id}` |
| List clients | `GET /general/clients` (+ `/{id}`) |
| List archive plans | `GET /archive/plans` (+ `/{id}`) |
| Submit an archive job | `POST /archive/plans/{planID}/archiveselections` |
| Job status | `GET /general/jobs/{id}` |
| Job report (text) | `GET /general/jobs/{id}/report` |
| Job protocol (json/xml) | `GET /general/jobs/{id}/protocol` |
| Job inventory (file list) | `GET /general/jobs/{id}/inventory` |
| Create index metadata keys | `GET`/`POST /archive/indexes/{index}/keys` |

---

This guide reflects what **P5 Archive Manager**'s API beta uses today; the P5 REST API has
more endpoints (restore, backup, sync, etc.) not covered here. See the
[official P5 REST API reference](https://blog.archiware.com/redoc/p5_rest_api/awp5api.html)
for the full surface.
