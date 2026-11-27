# P5 Archive Manager API 4.6.5 — The anonymized log export leaves no names behind; unreadable-tape files explained

### The anonymized log export catches every name

The first real export, from 4.6.4, still had folder and file names in some lines. If you exported
logs with 4.6.3 or 4.6.4, **export them again with 4.6.5 before sending them**, and delete the old
zip.

The anonymizer finds a path by its leading `/` or `Volumes/`. Three things got past it:

- **Paths relative to the checked folder.** The entry handle lines (one per file, so tens of
  thousands in a large check), the list of ignored temporary files, the files left out for a non-BMP
  name, and the stub-restore lines print paths without the folder in front. Each now has its own rule.
- **P5 handles.** In `Index#…`, the part after `#` is often the file's whole path in base64, which
  anyone can decode. It now becomes a `K-` token.
- **Two spaces in a row inside a name.** A double space ended the path, so everything after it was
  left as written. Names hold double spaces, so it no longer ends a path.

The review list before saving did show these names, but the rules should not need it.

### Files only on unreadable tape

When a server is set to treat a tape generation as unreadable (Settings ▸ Archiving), a file whose only
copy is on such a tape is not counted as archived and needs archiving again.

- **The Done line matches the tiles.** It counted these files as archived. In a field test it said
  *1610 of 4212 archived* while the Archived tile said 730. It now says *730 of 4212 archived · 880 only on
  unreadable tape*.
- **They are already in the archive total.** The orange box said they "count as needing a new archive
  copy", which read as a step still to take. It now says they are already in *Needs archiving* and in the
  blue Archive button, so there is nothing to add.
- **Archive only these N…** replaces *Archive them again…*, which opened the same sheet as the blue
  button, with every file to archive. The new button's sheet sends only the files on unreadable tape and
  says which files it leaves for the blue button.
