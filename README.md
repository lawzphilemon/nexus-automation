# NEXUS Content Pipeline

General-purpose Claude Code plugin for SEO/GEO article research, drafting, conversion, and Google Docs export. It has no default brand, client, domain, WordPress site, contact, product, or brand palette: every run works for the client you name.

## Install

```text
/plugin marketplace add lawzphilemon/nexus-automation
/plugin install nexus-automation@nexus-automation
```

The repository must be readable by your GitHub account. Update later with `/plugin marketplace update nexus-automation` and restart Claude.

## Quick start

1. Make an empty folder for your work (for example `content-workspace`) and open Claude Code in it. Every session for these articles starts in this folder.
2. Run `/nexus-automation:setup acme` (use your client's short name). It checks Pandoc, Python, the Google connectors, and a browser; creates `nexus-output/` and `clients/acme/` from the template; prefills the client from its website (sitemap links, FAQ mode); checks the client's WordPress read-only when you want drafts there; and creates the Google Sheet queue.
3. Fill the `TODO` lines in `clients/acme/facts.md`: what the brand may and may not claim, its services, and its team.
4. Write an article by hand with `/nexus-automation:research <keyword>` and follow each stage's prompt, or paste keyword rows into the sheet, set Status to `ready`, and run `/nexus-automation:queue`.

Add another client any time with `/nexus-automation:setup <name>`. Each client keeps its own facts, links, profiles, CTA, and WordPress site.

## Workspace

```text
content-workspace/
├── clients/
│   └── acme/
│       ├── facts.md            Defaults (domain, voice, FAQ, CTA, author, category, WordPress), claims, team, cases
│       ├── links.md            service pages, scheduled posts, live posts from the sitemap
│       ├── context-profiles/   optional brand JSON profiles (one per author or tone)
│       └── conversion.md       optional CTA, offer, source, and compliance rules for /convert
└── nexus-output/
    ├── queue.json              optional: parent Drive folder, legacy shared sheet
    ├── PROJECTS.md             every article with its status
    └── NXS-YYMMDD-XXXX_<slug>/ one folder per article
```

**Google Drive.** Each client has a main folder named after the brand with two subfolders, `Outline` and `Article`. The brand's queue sheet (`<INITIALS>-QUEUE <Brand>`) sits in the main folder, and its ID is the `Queue sheet` line in `facts.md`; `/nexus-automation:queue <client>` runs one brand, `/nexus-automation:queue` all of them. Docs are named `<INITIALS>-<TYPE>-<CODE>[-vN] <H1>`, for example `ACM-OL-NXS-261018-K7RW …` for an outline and `ACM-AR-NXS-261018-K7RW …` for its article; revisions get `-v2`, `-v3`. The initials and folder IDs live in the client's `facts.md`, and each project logs its Docs in `drive-docs.md`. The article Doc opens with a **Feature image** block (size, prompt, negative prompt, alt text, where to save it); the team saves the generated image in the brand's `Image` folder as `<INITIALS>-IMG-<CODE>.png`, and the WordPress draft step attaches it when Google Drive for desktop syncs that folder (`Folder Drive image lokal`), or when it is saved as `<project>/feature-image.png`.

`clients/` and `nexus-output/` stay on your machine. Nothing leaves it except the Google Docs and WordPress drafts the pipeline creates for you, and it never publishes, shares, or sends anything.

## Pipeline

```text
/research → /improve → /geo → /outline → /firstdraft → /finaldraft → /constructive-self-criticize → /convert → /export-gdoc
```

`/humanize` also works standalone.

`/research` gives every article a unique project code, `NXS-YYMMDD-XXXX` (for example `NXS-261014-7QF3`). Each stage saves its output to that project's own folder, `nexus-output/<CODE>_<slug>/` (`01-research.md` to `05-firstdraft.md`, then `latest.md`), and `nexus-output/PROJECTS.md` lists every project with its status. A new session never overwrites another article's files, and the pipeline can resume after the conversation is compacted or restarted.

**Clients.** `/research` asks for the client and profile, writes `<project>/client.txt`, and copies the profile to `<project>/context-profile.json` (a client without profiles works from `facts.md` alone); every writing stage reads them, and `facts.md` wins over the profile. `/queue` takes both from the sheet. Prices and rate-card data in a profile never go into an article.

`/research` also validates the keyword with Semrush and Ubersuggest when those connectors are available. `/outline` collects 3–6 verified external sources, `/firstdraft` cites them inline, and `/finaldraft` writes a 16:9 feature image prompt to `feature-image-prompt.md`.

### `/setup` — NEX-S

Sets up the workspace folders, a client from `templates/client/`, a read-only check of the client's WordPress (Application Password, Polylang, Yoast, ACF FAQ field), and the Google Sheet queue with its Antrean and Panduan tabs. It never asks for or stores a password, never overwrites an existing file, and marks anything it cannot verify as `TODO`.

### `/resume` — NEX-0

Reopens an article by its code, slug, or keyword (or lists all projects), shows which stages are done, and names the next command. Later stages in that conversation keep using the same code.

### `/research` — NEX-R

Captures the live Google results page in a browser (Claude in Chrome or the built-in browser): top 5 organic results, AI Overview and its cited domains, featured snippet, PAA, and related searches. It then inspects each result page for headings, word count, JSON-LD schema types, and last-modified date. It falls back to web search when no browser is available or Google shows a CAPTCHA, and never fabricates inaccessible data.

### `/improve` — NEX-I

Identifies search intent, semantic gaps, SQEG/SQRG requirements, and E-E-A-T improvements grounded in NEX-R findings.

### `/geo` — NEX-G

Builds a query fan-out, GEO structure prescription, schema recommendation, and information-gain proposition.

### `/outline` — NEX-O

Builds a GEO-compliant outline, discovers verified internal links from the supplied domain, and tags natural conversion points. Before writing, it checks the site for pages that already answer the same search intent and, when one does, asks whether to update that page, take a named different angle, or stop.

It also confirms **FAQ delivery**: `body` (default, FAQ as an H2 with FAQPage in the article schema) or `metabox` (for sites whose CMS renders the FAQ from a separate field and emits its own FAQPage). In metabox mode, later stages deliver the FAQ as a separate plain-text Q/A block and leave FAQPage out of the custom JSON-LD. `scripts/faq-scan.py` (Python stdlib, read-only) can detect the mode from existing posts and flags empty `FAQPage` output.

It also confirms **Voice**: `brand` (default, the article is on the brand's own site, so the brand speaks as "we"/"kami" and never describes itself from outside) or `third-party` (media, review, or guest posts). `/firstdraft`, `/finaldraft`, and `/convert` follow and check it.

Requires `WebFetch` and `WebSearch`.

### `/firstdraft` — NEX-F

Writes the full article from the confirmed outline and silently applies the appropriate language humanizer.

### `/finaldraft` — NEX-Fn

Re-runs the humanizer and GEO/SEO checks, then saves the final article, On-Page SEO Pack, and Schema JSON-LD once to `nexus-output/latest.md`. Later stages read this artifact directly instead of repeating the article in chat.

### `/constructive-self-criticize` — NEX-C

Reviews a finished article as its target reader, the brand owner, and a senior SEO/GEO editor: point of view, unsupported claims, contradictions, weak answers, and gaps against NEX-G. It saves up to 10 ranked findings, each with a concrete fix, to `06-critique.md`, then applies only the ones you approve, without adding new claims. Also works on any pasted article.

### `/convert` — NEX-U

Adds one or two site-branded contact CTA blocks (always a closing CTA; an earlier one only when the article is long enough and a section past 40% maps to the offer) and optional factual product or service mentions.

- Detects colors from the supplied website.
- Asks before every CTA which channel to use (phone, email, address, or all of them) and the details: the number (WhatsApp or call), the email, the address, and the button labels. There is no default contact; the client's saved contacts in `facts.md` are offered as choices only.
- Uses only supplied or verified offer details.
- Applies stronger source and disclaimer checks to regulated or high-stakes claims.
- Never supplies a default domain, contact, palette, credential, product, or claim.
- Reads `clients/<client>/conversion.md` when the client has one: a fixed palette, CTA channel, offer mapping, required sources, and compliance rules (see `templates/client/conversion.example.md`).

Requires `WebFetch` and `WebSearch`.

### `/queue` — NEX-Q

Runs the whole pipeline from a Google Sheet, one row per article, with two review gates. The only question in chat is the CTA contact, asked once per brand at the start of a run (a scheduled run with nobody to answer sends those rows to `error`). `ready` rows first get a cannibalization check: by search intent, not exact keyword, against the client's `links.md`, the sitemap, a `site:` search, the sheet's articles in progress, and the other `ready` rows of the run. Rows that share an intent are flagged together, and a row whose question an existing page already answers goes to `error` with that URL in the notes and three options (update that article, give the row a clearly different angle and set it to `ready` again, or skip it); a partial overlap continues with a named angle and opens the review brief. Then they get research, intent, GEO, and an outline, exported to a Google Doc (`outline-review`). After you comment and set `outline-approved`, the queue writes the draft, final draft, self-critique, CTA blocks, and the article Doc (`review`). Comment and set `revisi` for another pass, set `approved` to send the article to WordPress as a draft (`wp-draft`), or set `done`.

Up to 3 rows run in parallel, one subagent each; `/research` runs one row at a time because it drives the browser. Each brand's queue sheet is the `Queue sheet` line in its `facts.md`; `nexus-output/queue.json` is optional (`drive_folder`, and the older single shared sheet with `spreadsheet_id` and `tab`, where every row must name its Client). Columns are found by header name: Keyword, Market, Domain are required; Voice, FAQ, Word count, First-hand material, Internal links, CTA destination, Button label, Offer and allowed claims, Convert, Context profile, Client are optional or conditional. The sheet can also start with the keyword-research columns No, Month - Year, Keywords, Volume, Judul Artikel, Lang, and Notes, so research rows can be pasted in as they are: Judul Artikel becomes the working H1, Lang can stand in for Market (`id` = Indonesia), and Notes are the research brief (SERP observations, gap, angle, link and CTA hints, restrictions) that every stage checks against live data. Claude writes the NXS code, slug, both Doc links, last run, and notes. It never publishes, shares, or sends anything. Only Doc comments are read back, not edits typed into the Doc.

`scripts/wp-draft.py` sends an `approved` article's `latest.md` to WordPress through the REST API as a **draft** (never published): the H1 as the title, the slug, the article body with the CTA blocks as Custom HTML blocks, the Polylang language (`--lang`), the categories (`--category`, slugs looked up in that language; the queue takes them from the row's Notes or the client's `Kategori blog` Default), the Yoast SEO title and meta description from the YAML `title` and `meta-description`, the FAQ metabox Q/A pairs to an ACF repeater when `--faq-acf field:question:answer` is given (the queue passes the client's `FAQ ACF field` Default), and the feature image: when `feature-image.png` (or `.jpg`, `.jpeg`, `.webp`) sits next to `latest.md`, it is uploaded to the media library with the `**Alt text:**` line of `feature-image-prompt.md` as alt text and the post's language, then set as the featured image. It stops instead of creating a duplicate when the slug already exists. An unknown category slug, Yoast fields or FAQ rows the site refuses to save, or a feature image it cannot set become notes; the draft is still created. The JSON-LD and the "Diperbarui" byline date stay manual, and so does the feature image when no file was saved. Auth comes from the environment variable named by `--auth-env` (required; the queue passes the client's `WordPress auth env`), holding base64 of `username:application password` from WordPress Users > Profile > Application Passwords, one variable per site. The site is the client's `WordPress` Default; there is no fallback site. `--dry-run` shows the payload without sending anything.

### `/export-gdoc` — NEX-GD

Exports the latest final or converted article to a Google Doc through the Google Drive connector, containing:

- A metadata table for article title, slug, meta description, main keyword, related keywords, and publisher notes, one bullet per note (when any).
- Real headings for the article hierarchy.
- Preserved lists, links, article tables, and CTA HTML as paste-ready code.
- The FAQ metabox block, when that mode is used: each question in bold on its own line with the answer as its own paragraph below, ready to paste per field.
- JSON-LD schema at the end.

It uses Pandoc with the bundled Lua filter; install Pandoc from [pandoc.org/installing.html](https://pandoc.org/installing.html).

**Read-back check.** The Drive connector cannot read local files, so the HTML is copied into the upload by hand. After the upload, the Doc is read back with the connector's `read_file_content`, and `scripts/gdoc-check.py` (Python stdlib) compares it with the generated HTML: H2 and H3 headings, links, code blocks, and word count within 2%. A mismatch uploads once more (the first Doc goes to the Drive trash); a second mismatch keeps the Doc and reports the differences as a note instead of letting them pass silently. `/queue` runs the same check on the outline Doc. The Doc stays private until you share it. Without a Google Drive connector, the command keeps the generated HTML file so you can upload it to Drive and open it with Google Docs.

### `/humanize` — NEX-H

Humanizes Indonesian, English, or mixed text while preserving meaning and E-E-A-T signals.

## Supporting skills

- `humanizer-id` and `humanizer-en` — language-specific humanization.
- `wa-cta-standard` — three generic, site-branded CTA layouts.
- `product-upsell` — evidence-gated product or service mapping for any industry.

## Upgrading from 2.x

- `/convert-truemission` is gone. Put a client's fixed CTA, offer, and compliance rules in `clients/<client>/conversion.md`; `/convert` reads it for that client only.
- The sheet's `Profil` column is no longer read; you can delete it.
- WordPress settings move into each client's `facts.md` (`WordPress`, `WordPress auth env`, `FAQ ACF field`). The FAQ is only sent when the client names its `FAQ ACF field`.

## Upgrading to 3.4

- No default brand: `default_client`, `wp_site` in `queue.json`, and the `WP_NEXUS_AUTH` default are gone. Name every client's `WordPress` and `WordPress auth env` in its `facts.md`, and fill the Client column in an old shared sheet.
- No default CTA contact (3.3): the queue and `/convert` ask which phone, email, or address to use.
