# From P5 Archive Check to P5 Archive Manager API

## Methodology, architecture, security, and tool evolution

**Scope:** public repository and source-history review through **P5 Archive Manager API
4.6.1 (build 84), released 2026-11-21**, plus the 4.6.2 work in testing at the time of
writing (marked as such; it is not a release).

P5 Archive Manager did not begin as a conventional application. It began as a focused
operational question expressed as a shell procedure:

> For every file under this folder, can Archiware P5 return an `ArchiveEntry` handle?

That question stayed at the centre of the product, but almost everything around it
changed. The project moved from a local script, to an app-shaped script, to a native
Swift interface around a command-line engine, and finally to a REST-based application
that treats checking, proof, deletion, archiving, and restoration as related but distinct
workflows.

The most important evolution was therefore not visual. It was methodological:

- from **handle presence** to **per-file evidence and a verification verdict**;
- from **one local P5 server** to **multiple local or remote servers and indexes**;
- from **one source path** to **mapped, historical, imported-volume, and relocated paths**;
- from **read-only checking** to **guarded delete, archive submission, and restore**;
- from **a shell command sequence** to **an application-owned domain model, transport,
  receipts, tests, and recovery tools**.

## Evolution timeline

| Date / era | Generation | Method and capability change |
| --- | --- | --- |
| Before the public repository | Shell procedure | The operational method was established with `find`, `nsdchat`, temporary text files, and CSV assembly: enumerate local files, request an `ArchiveEntry` handle for each path, then query status, size, archive time, volume, and barcode for the handles that exist. |
| 2025-11-13 | **P5 Check shell script published** | The first public `p5ArchiveCheck` commit recorded the local-server script. `p5-check-dialog.sh` added progress reporting through swiftDialog, wrote reports to `/Users/Shared`, and produced a tarball of intermediate evidence. The target remained the local P5 installation and its default archive index. |
| November 2025 | **Platypus + swiftDialog app** | Platypus turned the drag-and-drop shell workflow into a macOS app bundle. Bundled swiftDialog made the long-running check visible. This improved access and distribution, but the execution model was still the shell script and local `nsdchat`. |
| November 2025 | **Basic native Swift app** | A Swift/SwiftUI application replaced the script wrapper as the main interface. Folder drop, progress, and output-file presentation became app state. The checker itself was still a bundled shell script, so this was a native UI around the established CLI method—not yet a native archive engine. |
| 2025-11-20 to 2025-11-23 | **Remote `nsdchat` Swift manager** | P5 Archive Manager added named servers, port and user settings, a selectable Archive index, and passwords stored in macOS Keychain. The Swift app built an `awsock://` connection and launched the bundled checker, which called remote `nsdchat -s`. This separated the operator's Mac from the P5 server while preserving the proven handle-by-path workflow. Public documentation identified version 2.8 by 2025-11-23. |
| February-April 2026 | **Operational CLI product, 3.x** | The app added guarded deletion, proof links, typed confirmation, audit logging, partial delete, cancellation, broken-link reporting, shared server configuration, and better progress. The key change was from “report what is archived” to “support an operator decision after showing evidence.” The engine was still Swift → shell → `nsdchat`. |
| 2026-06-14 | **REST API prototype begins** | A separate P5 Archive Manager API repository was scaffolded with no `nsdchat` dependency. The first day established browsing, live-server diagnostics, local-versus-P5 comparison, local-driven directory queries, size verification, per-file provenance, delete receipts, deep verification, and archive submission. |
| June-July 2026 | **REST workflow becomes a product** | The API line added proof-before-delete, archive job IDs and reports, receipts mirrored to an optional external location, multi-index search, multi-server settings, logging, special-character handling, source-path metadata, path mapping, historical archived locations, and update/release infrastructure. Versions 0.2 through 0.10 documented this rapid beta sequence. |
| 2026-08-11 to 2026-08-13 | **Separate CLI and API lineages formalised** | CLI remained the separately installed stable 3.x application; the REST successor became the 4.x line. API 0.10.1 acted as the transition bridge, followed by 4.0. The change was deliberately not presented as an in-place upgrade because settings, workflows, bundle identity, and behaviour differ. |
| 2026-09-18 to 2026-09-19 | **Native transport and TLS trust** | The API app replaced password-bearing subprocess transport with P5Kit/`URLSession`, moved Keychain operations to Apple's Security APIs, added per-server HTTP/HTTPS choice, certificate inspection and pinning, refused redirects and HTTPS-to-HTTP fallback, and live-tested Keychain continuity plus self-signed certificate trust. |
| 2026-09-22 | **Restore from Project File, 4.2** | XML, FCPXML/FCPXMLD, Resolve DRT, and path lists became restoration inputs. The application now parsed editorial intent, found corresponding P5 entries across indexes and imported volumes, expanded RED media to its `.RDC` folder, reported what was missing locally, and submitted one monitored restore job. |
| 2026-11-03 to 2026-11-05 | **Stub and recovery-aware manager, 4.3-4.4** | The app learned to recognise and restore `.p5c`/`.p5a` stubs, promoted Delete and Archive to parallel main actions, excluded filenames the REST layer could not safely archive, and reused the project-restore search engine when an ordinary folder check could not locate relocated or label-rooted media. |
| 2026-11-10 | **Deployable site configuration, 4.5** | Server-list import/export, reviewed discovery, site settings, path rules, historical roots, optional enforced settings, and site-file import/export turned a single-user utility into a tool that can be configured consistently across multiple Macs without exporting passwords or certificate pins. |
| 2026-11-21 | **Multi-storage and unreadable-tape awareness, 4.6.1** | Check swaps each storage's root in and lists every location tried, so a folder archived from several storages is found whole. Per server, LTO generations the drives cannot read can be ticked, and files held only on them stop counting as archived and join the Archive button. An entry-handles window says what to do about files P5 did not confirm; Check Details became a window per part; known temporary files can optionally be ignored. |
| 2026-11 (in testing as 4.6.2, unreleased) | **A check that survives a slow P5, and sizes that follow P5** | GET requests retry with back-off on timeouts, and a check that still loses P5 can be resumed from its cached listings. Delete runs its file-system work off the main thread and shows live progress. Size matching was rewritten from measured P5 behaviour (see section 6). |

## Methodology changes

### 1. Handle existence became evidence

The early algorithm classified a file as archived when `nsdchat` returned an archive
handle for its path. Additional calls enriched the row with status, size, date, volume,
and barcode, but the core decision was binary: handle or no handle.

The REST application made the decision explicit and inspectable. It compares the local
file with the P5 entry and records a per-file verdict such as exact, close, mismatch,
not archived, or matched stub. Size mismatches remain visible and are not silently
promoted to deletion evidence. A proof report is written before deletion, and every
delete outcome is recorded in a receipt and audit log.

This changes the question from “does P5 know this path?” to “what evidence supports the
action we are about to take?”

### 2. Per-file remote calls became local-driven, bounded queries

The CLI engine calls `ArchiveEntry handle` for each file, then makes more `nsdchat`
calls for each archived handle's metadata. It is direct and understandable, but command
count grows with the number of files and fields.

The REST checker enumerates the local folder first and queries only the P5 directories
needed for those local files. Volume information is cached. Deep Verify remains
available when the operator needs a P5-driven scan. Later versions reuse the Restore
search engine only as a fallback after the cheaper current-path and historical-path
checks find nothing.

The method therefore became layered:

1. use the fastest exact or mapped path;
2. try known historical locations;
3. use broader imported-volume, catalogue, TSV, or relocated-media searches;
4. preserve “undetermined” when connectivity or authentication fails instead of
   misclassifying the file as absent.

### 3. Path identity became a model, not an assumption

The original workflow assumes the present filesystem path is the path P5 indexed.
The REST application separates the **local folder being inspected** from the
**archived P5 path**. Per-server prefix mappings address storage migrations, while
historical roots address projects whose earlier locations cannot be derived from the
current path.

Restore adds other identities: the path named by an editing project, a P5 path learned
from an imported volume, a P5 Archive Browser catalogue path, a TSV inventory path,
and the projected original name represented by a P5 stub.

### 4. A check became a transaction with evidence

The original output is a set of files: a not-archived list, an archived CSV, a log, and
a backup of intermediate data. The newer app treats actions as transactions:

- **Check** produces structured per-file provenance.
- **Delete** writes proof first, re-checks the candidate immediately before removal,
  deletes only eligible files, and writes a receipt.
- **Archive** records the submitted paths and returned P5 handles, monitors the job,
  and saves the job report.
- **Restore** prepares candidate versions and media, submits a bounded selection, and
  follows the restore job.

### 5. One workflow became a set of cooperating engines

The current application no longer assumes that folder checking is sufficient for every
recovery task. The main check, deep verification, archive browser, project restore,
stub restore, path mapper, server manager, receipt store, and site-settings layer each
have a distinct responsibility. When the normal Check cannot find relocated media, it
calls the Restore search engine instead of duplicating that search logic.

### 6. A size match became a measured rule, and a check became resumable

Through 4.6.0 the check treated a size as matching only when the two numbers were equal
or within a loose tolerance, so a file P5 reported a few hundred bytes larger than the
disk showed up as a mismatch and the explanation was guesswork. The 4.6.x work replaced
the guess with a measurement. Testing against a lab P5 server and 110 real matches showed
that P5 reports the file's bytes plus a small per-entry overhead (245 bytes for an empty
file, a few hundred more otherwise), never less than the disk and never zero.

The rule now follows that behaviour:

- equal sizes are an exact match;
- P5 larger by 1 to 4096 bytes is a close match, labelled as P5 overhead;
- P5 larger by more, or smaller than the disk, is a mismatch;
- a symbolic link on disk matches only a P5 Link entry;
- exact byte counts and the difference are shown, with a plain-language explanation of
  why the extra bytes are normal.

The same line of work addressed failure rather than accuracy. A timeout part-way through
a long check used to discard every result. Reads are now retried with back-off and eased
off when P5 is slow, writes are never retried, and listings that P5 answered are cached
so an interrupted check can be resumed instead of restarted. This was proven by
interrupting a real P5 server through a proxy during a check. Separately, Delete's file
work moved off the main thread, which removed a freeze when deleting from an SMB share,
and the confirmation sheet gained live progress.

Boundary: sizes above 2 GiB have not been tested; the API documents the inventory size
as a 32-bit value.

## Current workflow flowchart

```mermaid
flowchart TD
    A[Choose P5 server and index] --> B{Operator intent}

    B -->|Folder| C[Enumerate local files]
    C --> D[Derive mapped P5 path]
    D --> E[Query required P5 directories]
    E --> F{Archived matches found?}
    F -->|No| G[Try historical roots]
    G --> H{Matches found?}
    H -->|No| I[Use Restore search engine<br/>TSV, catalogue, imported volumes, bounded walk]
    F -->|Yes| J[Build per-file provenance]
    H -->|Yes| J
    I --> J
    J --> K{Per-file verdict}
    K -->|Exact or allowed close match| L[Eligible for guarded delete]
    K -->|Not archived| M[Eligible for archive submission]
    K -->|Mismatch or uncertain| N[Hold for review]
    L --> O[Write proof report]
    O --> P[Re-verify candidate]
    P --> Q[Delete and write receipt/audit log]
    M --> R[Confirm plan and client]
    R --> S[Submit archive job]
    S --> T[Monitor job and save manifest/report]

    B -->|Project file or path list| U[Parse XML, FCPXML/FCPXMLD, DRT, or paths]
    U --> V[Resolve media across indexes and alternate sources]
    V --> W[Prepare versions, tapes, and destination]
    W --> X[Submit and monitor one restore job]

    B -->|P5 stub| Y[Project original name and confirm matching P5 entry]
    Y --> W
```

## Product and component relationships

```mermaid
flowchart LR
    S[P5 Check shell scripts<br/>local nsdchat] --> P[Platypus P5 Archive Checker<br/>script app + swiftDialog]
    P --> L[Basic Swift/SwiftUI app<br/>local bundled checker]
    L --> C[P5 Archive Manager CLI 3.x<br/>remote nsdchat over awsock]
    C -. operational lessons and workflow lineage .-> A[P5 Archive Manager API 4.x<br/>REST + P5Kit/URLSession]

    C --> NSD[Archiware nsdchat<br/>port 9001]
    NSD --> P5[Archiware P5]

    A --> REST[P5 REST API v8<br/>/rest/v1 endpoints]
    REST --> P5
    A --> KC[macOS Keychain<br/>Security framework]
    A --> TLS[Per-server TLS trust<br/>system trust or certificate pin]
    A --> PR[Project parsers<br/>XML, FCPXML, FCPXMLD, DRT]
    A --> AUX[Optional discovery sources<br/>TSV inventories and Browser catalogue]
    A --> EVID[Proof reports, manifests,<br/>receipts, logs, audit trail]
```

The dotted connection is deliberate: the API app is the successor in the product
lineage, but it is not the CLI app with its transport swapped in place. CLI 3.x and API
4.x are separate applications with separate installation and update channels. They can
coexist while an operator compares results or retains a CLI-specific workflow.

## Security analysis by generation

### Shell and Platypus generations

**Strengths**

- Local execution avoided sending credentials over a network.
- The command sequence was transparent and produced human-readable evidence.
- The workflow excluded P5 stub sidecars from ordinary file checks.

**Risks and limits**

- Predictable shared temporary filenames such as `/private/tmp/files.txt` created
  collision, stale-data, and local tampering risks when runs overlap or another process
  can write there.
- Shell parsing, newline-delimited paths, `grep`, `paste`, and unescaped CSV fields are
  fragile around unusual filenames. The separate Perl variation was introduced partly
  to handle commas more correctly.
- A Platypus wrapper and bundled swiftDialog improve usability but do not remove shell,
  temporary-file, or dependency trust boundaries.
- Generated reports may reveal filenames, paths, archive handles, volume names, and
  barcodes. Their permissions and retention need to match the sensitivity of the media
  environment.

### Remote `nsdchat` Swift generation

**Improvements**

- Passwords were stored per server in macOS Keychain rather than in the saved server
  list.
- Server and Archive-index selection became explicit.
- The app added confirmation gates, proof review, and an audit trail before destructive
  deletion.

**Residual risks**

- The app assembled an `awsock://username:password@host:port` string and placed it in the
  child process environment; the shell then passed it to `nsdchat`. Keychain protected
  the credential at rest, but the secret still crossed a subprocess boundary in a
  connection string.
- The app still depended on a fixed external executable path and a bundled shell script.
- Shell output files were the contract between the engine and the UI, making stale or
  malformed artifacts a safety concern. Later CLI versions narrowed collection to the
  active run folder and added diagnostics.
- Permanent deletion was intentionally used instead of Trash for reliable operation on
  network storage. That makes the proof and confirmation controls essential rather than
  optional convenience.

### REST API generation

**Current controls**

- Passwords remain per-server Keychain items and are excluded from server and site
  configuration exports.
- Since September 2026, requests use P5Kit/`URLSession`; credentials are placed in the
  HTTP Authorization header in memory rather than in shell command arguments.
- Keychain operations use Apple's Security APIs. Update-first behaviour avoids deleting
  the old credential before a replacement is known to have succeeded.
- HTTPS can use normal macOS trust or an explicitly reviewed SHA-256 certificate pin.
  Inspection does not grant trust; editing an endpoint invalidates its old pin.
- HTTPS failures never fall back to HTTP. Redirects are refused, including for archive
  submissions, so credentials and mutations are not silently replayed to another URL.
- Imported server files contain no passwords or certificate pins. An imported HTTPS
  server arrives unpinned and requires local review.
- Discovery is reviewed before it changes the server list. Ignored file revisions are
  tracked by SHA-256 fingerprint.
- Connection and authentication failures stop classification. They are not converted
  into “not archived,” which would be unsafe input to an archive or delete decision.
- Delete eligibility is limited to verified verdicts. Proof is written before deletion,
  each candidate is checked again, and all outcomes are receipted.
- Archive plans that delete source files or folders are identified; delete-at-source
  plans are blocked by default unless the operator changes that policy.

**Remaining operational cautions**

- HTTP is still available for P5 installations that require it. Basic credentials over
  HTTP are not confidential; use HTTPS wherever the server deployment supports it.
- A pinned self-signed certificate is only as trustworthy as the independent channel
  used to verify its fingerprint.
- Archive, delete, and restore are real mutations. Test new server, plan, client,
  mapping, and restore-destination combinations with disposable data first.
- A client timeout after a mutation request can leave an uncertain outcome: the server
  may have accepted the job even when the client did not receive its ID. Do not blindly
  repeat a submission; reconcile against P5 jobs and saved evidence.
- Stopping local monitoring does not necessarily stop a server-side archive or restore
  job.
- Site files and server-list files intentionally omit secrets, but they still disclose
  infrastructure names, ports, usernames, storage mappings, and archive topology. Treat
  them as configuration data, not as public examples.
- Generated logs, receipts, project parse results, and provenance reports can expose
  production paths and media names. Redaction and access control remain deployment
  responsibilities.

## Tool-change history

| Layer | Early approach | Intermediate approach | Current API approach | Why it changed |
| --- | --- | --- | --- | --- |
| User interface | Terminal/script output | Platypus app with swiftDialog, then SwiftUI front end | Native SwiftUI application with dedicated Check, Delete, Archive, Browse, Restore, Settings, Help, and receipts | Better feedback, explicit choices, reusable state, and safer presentation of mutations |
| File discovery | `find` to newline-delimited text files | Bundled shell script launched by Swift | `FileManager` enumeration and typed models, with explicit error reporting for skipped subtrees | Remove text-file coupling and avoid silently incomplete scans |
| P5 lookup | Local `nsdchat -c` | Remote `nsdchat -s awsock://…` | P5 REST API v8 via P5Kit/`URLSession` | Remove the `nsdchat` installation dependency, support portable remote operation, and enable richer workflows |
| Query strategy | One handle lookup per path, then metadata calls per handle | Same method with selectable server/index | Local-driven directory inventory, cache, multi-index search, historical fallback, and Restore-engine fallback | Reduce calls and find data whose current path differs from its archived identity |
| Credentials | None for local-only access or ad hoc script configuration | Per-server password in Keychain, expanded into an `awsock` subprocess connection string | Per-server Keychain via Security APIs; Authorization header built in memory | Protect secrets at rest and remove password-bearing process arguments/environment from the REST transport |
| Network trust | Local IPC / CLI assumption | `awsock` connection managed by `nsdchat` | Explicit HTTP/HTTPS, system trust or reviewed certificate pin, no downgrade, no redirects | Make transport security visible and enforceable per server |
| Data interchange | Temporary `.txt` files, `paste`, CSV, tarball | Dated output directory consumed by Swift UI | Codable domain models, JSON REST responses, structured history and receipts; CSV/TXT remain export evidence | Preserve human-readable proof without making temporary files the application protocol |
| Deletion | Not part of the first checker | Delete archived list after gates and typed confirmation | Verdict-limited delete, proof-before-delete, immediate re-verification, receipt and audit log | Turn a destructive convenience into a defensible procedure |
| Archive write | Outside the original checker | CLI line remained primarily check/delete | Plan/client selection, REST submission, manifest, job polling, and saved P5 report | Close the loop for files proven not archived |
| Restore | External/manual P5 workflow | Not a core CLI-manager function | Project-file restore, path-list restore, imported-volume search, RED-folder expansion, and restore from stub | Move from storage inspection to editorially informed recovery |
| Configuration | Script constants | Saved servers and custom index | Multiple servers, mappings, historical roots, reviewed server import, site settings, optional managed enforcement | Support repeatable deployment across users and Macs |
| Testing | Manual runs and inspection | Incremental UI and live operational testing | SwiftPM/XCTest contract tests, filename and path harnesses, loopback TLS tests, disposable REST probes, and bounded live acceptance | Separate source confidence from live-server and destructive-workflow acceptance |
| Build/distribution | Script files | Platypus bundle, then Xcode app signing/notarization | Xcode universal builds, separate CLI/API release lines, shared release tooling, signed/notarized releases | Make provenance, updates, and migration boundaries explicit |

## What stayed constant

Despite the large expansion, the product retained several sound ideas from the first
script:

- Start with the files the operator actually has in front of them.
- Ask P5 for evidence rather than infer archive state from local filenames alone.
- Keep archived and not-archived results separately inspectable.
- Preserve logs and intermediate evidence for troubleshooting.
- Make progress visible during operations that may take a long time.

The modern application is best understood as those ideas made explicit, testable, and
safe enough to support consequential actions.

## Sources and evidence boundary

Primary sources reviewed:

- [`macvfx/p5ArchiveCheck`](https://github.com/macvfx/p5ArchiveCheck), including
  [`p5-check-dialog.sh`](https://github.com/macvfx/p5ArchiveCheck/blob/main/p5-check-dialog.sh)
  and its Git history.
- [`macvfx/p5ArchiveManager`](https://github.com/macvfx/p5ArchiveManager), including the
  public README, release notes, API guide, product-lineage document, and current public
  documentation history.
- The local source histories for P5 Archive Manager CLI and P5 Archive Manager API,
  including the API User Guide, changelog, credential/TLS assessment, TLS review build,
  request/job trace, tests, Keychain helper, request client, project restore service,
  and receipt store.
- [“A blog about archives, storage and everything”](https://macvfx.blog/), which records
  the Platypus, swiftDialog, signing/notarization, and move-to-native-Swift context.

Repository history proves when the public files and implementations were recorded; it
does not necessarily prove the first private experiment or first production use. Live
acceptance is stated only where the project records it. In particular, successful
builds and automated tests should not be treated as proof of every P5 plan, network,
certificate, archive, delete, or restore workflow in a production environment.
