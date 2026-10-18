---
name: setup
description: Set up a NEXUS workspace and a client in one run - working folders, the client's facts and links from the template, a read-only WordPress check, and the Google Sheet queue
argument-hint: "[client-name]"
---

# NEX-S — Setup

**Mission:** Take a new user, or a new client, from nothing to a working pipeline in one run, without writing anything that was not provided or verified.

Argument: $ARGUMENTS

## Rules

- Never ask for, write, or repeat a password, application password, or token. WordPress auth is set by the user in their own environment.
- Never overwrite an existing file. For an existing client folder, show what is missing and add only that, after the user agrees.
- Never invent client facts. Fill in what the user says or what is verified on the client's own site; everything else stays `TODO`.
- Do not change the sharing of any Google file.

## 1. Workspace

The current working directory is the workspace. Stop if it is inside the plugin cache (`.claude/plugins`) and ask for a normal folder. Create `nexus-output/` and `clients/` when missing. If the workspace is a git repository, add both to its `.gitignore`, because they hold client data. Tell the user to open future sessions in this folder.

## 2. Prerequisites

Report one table: item, required or optional, found or missing, and how to fix it. Missing items do not stop setup.

| Item | Needed for | Check |
|---|---|---|
| Pandoc | Google Doc exports (required) | `pandoc --version`; on Windows also `%LOCALAPPDATA%\Pandoc\pandoc.exe`. Install: https://pandoc.org/installing.html |
| Python 3 | WordPress drafts and helper scripts (required for those) | `python --version` or `python3 --version` |
| Google Drive and Google Sheets connectors | Docs and the queue (required) | their tools are available in this session; else connect them in Claude's connector settings |
| Browser (Claude in Chrome or the built-in browser) | live SERP in /research (recommended) | without one, /research uses web search |
| Semrush, Ubersuggest connectors | keyword validation (optional) | their tools are available |

## 3. Client

Client name: the argument, else ask for a short kebab-case name (for example `acme`). If `clients/<name>/` already exists, list the template files it lacks and add only those.

Copy `${CLAUDE_PLUGIN_ROOT}/templates/client/` to `clients/<name>/` (`facts.md`, `links.md`, `context-profiles/README.md`, `conversion.example.md`) and fill `{{CLIENT_NAME}}` and `{{DATE}}`.

Ask in one message for what only the user knows (each may be skipped): the website domain; the article languages; the CTA destination and button label per language; the author's name, role, and public profile URL; the blog category slug; what the brand must never claim; and the case studies the client allows, with what may be named.

Suggest the client's initials from its brand name (2 to 4 capital letters, for example `ACM` for Acme) and save the confirmed value as `Inisial brand`; every Doc name starts with it.

Then verify and prefill from the site, read-only:

- The domain loads; take the brand name from the homepage title.
- FAQ delivery: run `python "${CLAUDE_PLUGIN_ROOT}/scripts/faq-scan.py" <1-3 post URLs>` and suggest `body` or `metabox` from the result.
- `links.md` from the sitemap (`/sitemap.xml`, else `/sitemap_index.xml`): service and landing pages, other pages, and blog posts split by language (for example an `/id/` path prefix), each with its lastmod. Skip tag, category, author, and pagination pages.
- Every CTA URL the user gave: open it and keep it only if it loads.
- Context profile: if the user has one, save it in `context-profiles/` and put its file name in the `Context profile` Default; else leave the Default empty (the stages then use `facts.md` alone).

Anything still unknown is written as `TODO`. Show the filled Defaults block before saving.

## 4. WordPress (optional)

Ask whether approved articles should go to this client's WordPress as drafts. If yes:

1. Site URL: confirm `<site>/wp-json/` responds, then write it as the `WordPress` Default.
2. Variable name: `WP_<CLIENT>_AUTH` (upper case, dashes become underscores); write it as `WordPress auth env`.
3. Tell the user to create an Application Password (WordPress → Users → Profile → Application Passwords) for an account that can create posts, and to set the variable themselves, then restart Claude. Windows PowerShell (the password is typed at the prompt, not stored in history):

   ```powershell
   $u = Read-Host "WordPress username"; $p = Read-Host "Application password"; [Environment]::SetEnvironmentVariable('WP_ACME_AUTH', [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($u):$($p)")), 'User')
   ```

   macOS or Linux: add `export WP_ACME_AUTH="$(printf '%s' 'username:application password' | base64)"` to the shell profile. Replace `WP_ACME_AUTH` with the client's variable name.
4. When the variable is set (on Windows, a session started before it was set can read it from the user scope), check read-only: `GET /wp-json/wp/v2/users/me?context=edit` (the account can create posts), `OPTIONS /wp-json/wp/v2/posts` (a `lang` field means Polylang; `_yoast_wpseo_title` in `meta` means the Yoast fields are writable; an `acf` field), and one recent post with `context=edit` to find an ACF repeater that holds the FAQ. Write `FAQ ACF field` only when one is found, as `field (question_sub_field, answer_sub_field)`. Check the blog category slug with `GET /wp-json/wp/v2/categories?slug=<slug>`.
5. Report what the draft step will do automatically and what stays manual, and what site change would automate the rest: Yoast needs `_yoast_wpseo_title` and `_yoast_wpseo_metadesc` registered for REST; an ACF FAQ needs its field group's "Show in REST API" switch.

Never create, edit, or delete posts or media during setup.

## 5. Drive folders (with the Google Drive connector)

Create the client's main folder (named after the brand, for example `Acme`) with two subfolders, `Outline` and `Article`, inside `drive_folder` from `nexus-output/queue.json` when set, else My Drive. Search by exact name first and reuse a folder that already exists in that place; never create a duplicate. Write the three IDs to `facts.md` as `Folder Drive`, `Folder Drive outline`, and `Folder Drive article`. Doc names and filing then follow /export-gdoc **Doc names and folders**.

## 6. Queue sheet (optional)

Each brand has its own queue sheet in its main Drive folder. If the client's `facts.md` already has a `Queue sheet`, keep it. Otherwise ask whether to create one:

1. Create a Google Sheet with the Drive create-file tool (`mimeType: application/vnd.google-apps.spreadsheet`) inside the client's main folder (`Folder Drive`), named `<INITIALS>-QUEUE <Brand>`.
2. Rename its first tab to `Antrean`. Write `${CLAUDE_PLUGIN_ROOT}/templates/sheet/antrean.tsv` (tab-separated) from cell A1, bold row 1, and freeze row 1 and columns A to C.
3. Find the `Status` column by its header and give rows 2 onward a strict dropdown with the values in `templates/sheet/status-values.txt`.
4. Add a tab `Panduan` and write `templates/sheet/panduan.tsv` from A1.
5. Write the sheet's ID to `facts.md` as `Queue sheet`.
6. Read the header row back and confirm it matches the template.

## 7. Summary

One table of what was created or changed (paths and the sheet link), the `TODO` lines left in `facts.md`, and what stays manual. Then the next steps:

- Fill the `TODO` lines in `clients/<name>/facts.md`; every stage reads it live.
- One article by hand: `/nexus-automation:research <keyword>`, choose the client, and follow each stage's prompt.
- From the brand's queue sheet: paste keyword-research rows from column A, set Status to `ready`, and run `/nexus-automation:queue <client>` (or `/nexus-automation:queue` for every brand).
- Another client later: `/nexus-automation:setup <other-client>`.
