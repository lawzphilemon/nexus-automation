---
name: export-gdoc
description: Export the canonical NEXUS article artifact to a Google Doc with the SEO metadata table, real headings, links, tables, CTA code, and JSON-LD schema
argument-hint: [source.md]
allowed-tools: Read, Write, Bash
---

# NEX-GD - Google Docs Export

**Mission:** Put the latest complete NEX-Fn or NEX-U artifact in a Google Doc for review, comments, or client handoff, without rewriting or changing its content.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`.

## Source

Use `<project>/latest.md` by default, or the `.md` path given as an argument. It needs valid YAML with `title`, `slug`, and `meta-description`, the complete article from its H1, and `Schema Markup (JSON-LD)` as the final heading. If `/convert` ran, use the converted artifact. If no artifact exists, say so and suggest running `/finaldraft` first.

## Workflow

1. Confirm Pandoc is available with `command -v pandoc`. If absent, stop with the official install link: `https://pandoc.org/installing.html`.
2. Build the HTML with the bundled filter, so the Doc starts with the metadata table: `Judul Artikel`, `Slug`, `Meta Description`, `Main Keyword`, `Related Keywords`, and `Notes` (rows without a value are skipped). When `<project>/feature-image-prompt.md` exists, pass it as the **first** input: the Doc then shows the metadata table, the **Feature image** block (size, where to save the image, prompt, negative prompt, alt text), and then the article, so the reviewer sees and can comment on the image prompt with the article:

```bash
pandoc "<project>/feature-image-prompt.md" "<source.md>" --from=markdown+yaml_metadata_block+raw_html --to=html --wrap=none --no-highlight --lua-filter="${CLAUDE_PLUGIN_ROOT}/scripts/nexus-gdoc.lua" --output="<project>/<slug>.gdoc.html"
```

Without that file, run the same command with `"<source.md>"` as the only input.

   CTA HTML and the JSON-LD stay in plain (unhighlighted) code blocks, so they arrive as paste-ready code with no stray links or styling.

3. Upload with the Google Drive connector's create-file tool:
   - Title and folder: see **Doc names and folders** below, with type `AR`.
   - Content: the full `.gdoc.html` file as text, exactly as Pandoc wrote it (the connector cannot read local files, so copy the HTML character for character; never turn it into Markdown or shorten it), content type `text/html`. Leave conversion to Google Docs on.

   No Google Drive connector: say so, keep the `.gdoc.html` file, and tell the user to upload it to Google Drive and open it with Google Docs. Skip steps 4 and 5.

4. **Read-back check.** Read the new Doc with the Drive `read_file_content` tool (its file ID from step 3), save the returned `fileContent` unchanged as `<project>/<slug>.readback.md`, and compare it with the uploaded HTML:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/gdoc-check.py" "<project>/<slug>.gdoc.html" "<project>/<slug>.readback.md"
```

   It compares the H2 and H3 headings, links, code blocks (CTA HTML and JSON-LD), and word count (2% tolerance), prints both columns, and exits 1 with the differences on a mismatch.
   - `OK`: go on.
   - `MISMATCH`: upload once more from the same `.gdoc.html` (step 3), move the first Doc to the Drive trash with the connector's trash tool (it stays restorable there), and run the check on the new Doc. A second mismatch keeps the second Doc and becomes a note: return the link with `Read-back check: [the differences the script printed]`, so the reviewer knows what to look at. Never let a difference pass silently.

5. Delete `<project>/<slug>.gdoc.html` and `<project>/<slug>.readback.md`. Keep the source artifact.

Return only the Google Doc link. Do not paste the article again.

End with: "Google Doc ready - metadata table, formatted article, and schema included. Read-back check: OK." (or the note from step 4).

## Doc names and folders

Every Doc the pipeline creates (this command and the queue's outline export) follows one pattern, so a client's Docs sort together and the outline and article of one article pair up by code.

**Name:** `<INITIALS>-<TYPE>-<CODE>[-v<N>] <H1>`, for example `ACM-AR-NXS-261018-K7RW Judul Artikel`.

- `<INITIALS>`: the client's `Inisial brand` Default in `clients/<client>/facts.md` (2 to 4 capital letters). Missing: in an interactive run, suggest initials from the brand name, ask once, and save the confirmed value to `facts.md`; in queue mode, name the Doc without the prefix and write "add `Inisial brand` to facts.md" in the notes.
- `<TYPE>`: `AR` for the article Doc (this command), `OL` for the outline Doc (the queue's outline export).
- `<CODE>`: the project code.
- `-v<N>`: the version. Every Doc created is logged in `<project>/drive-docs.md` (`| Type | Version | Title | Link | Date |`). The first Doc of a type has no suffix; the next one of the same type is `-v2`, then `-v3`.

**Folder:** the client's main folder, named after the client's brand (for example `Acme`), holds three subfolders, `Outline`, `Article`, and `Image`. Outline Docs go into `Outline`, article Docs into `Article`, and the team saves each generated feature image into `Image` as `<INITIALS>-IMG-<CODE>.png` (or `.jpg`/`.webp`; a `-v2` suffix for a newer one is fine). Their IDs are the `Folder Drive`, `Folder Drive outline`, `Folder Drive article`, and `Folder Drive image` Defaults in `facts.md`; `Folder Drive image lokal` is the same Image folder as a local path when Google Drive for desktop syncs it. For a missing ID: search Drive for the folder by exact name inside its parent (the main folder's parent is the `drive_folder` from `nexus-output/queue.json` when set, else My Drive), create it only when the search finds none, and write the ID back to `facts.md`. Never create a second folder with the same name in the same place.

**No client** (`<project>/client.txt` missing or `none`): the Doc's title is the H1 (outline: `<CODE> outline - <H1>`), and it goes into `drive_folder` when set, else My Drive.

## Rules

- Don't change sharing. The Doc stays private to the user until they share it.
- Upload only the article artifact. Never upload research notes, earlier stage files, or contact details that are not in the article.
