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
2. Build the HTML with the bundled filter, so the Doc starts with the metadata table: `Judul Artikel`, `Slug`, `Meta Description`, `Main Keyword`, `Related Keywords`, and `Notes` (rows without a value are skipped):

```bash
pandoc "<source.md>" --from=markdown+yaml_metadata_block+raw_html --to=html --wrap=none --no-highlight --lua-filter="${CLAUDE_PLUGIN_ROOT}/scripts/nexus-gdoc.lua" --output="<project>/<slug>.gdoc.html"
```

   CTA HTML and the JSON-LD stay in plain (unhighlighted) code blocks, so they arrive as paste-ready code with no stray links or styling.

3. Upload with the Google Drive connector's create-file tool:
   - Title: the article's H1.
   - Content: the full `.gdoc.html` file as text, exactly as Pandoc wrote it (the connector cannot read local files, so copy the HTML character for character; never turn it into Markdown or shorten it), content type `text/html`. Leave conversion to Google Docs on.
   - Folder: only if the user names one. Find it with the connector's search first.

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

## Rules

- Don't change sharing. The Doc stays private to the user until they share it.
- Upload only the article artifact. Never upload research notes, earlier stage files, or contact details that are not in the article.
