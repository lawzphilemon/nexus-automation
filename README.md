# NEXUS Content Pipeline

General-purpose Claude Code plugin for SEO/GEO article research, drafting, conversion, and Google Docs export. It has no default client, domain, contact destination, product, or brand palette.

## Install

```text
/plugin marketplace add lawzphilemon/nexus-automation
/plugin install nexus-automation@nexus-automation
```

## Claude Code pipeline

```text
/research → /improve → /geo → /outline → /firstdraft → /finaldraft → /constructive-self-criticize → [/convert | /convert-truemission] → /export-gdoc
```

`/humanize` also works standalone.

`/research` gives every article a unique project code, `NXS-YYMMDD-XXXX` (for example `NXS-261014-7QF3`). Each stage saves its output to that project's own folder, `nexus-output/<CODE>_<slug>/` (`01-research.md` to `05-firstdraft.md`, then `latest.md`), and `nexus-output/PROJECTS.md` lists every project with its status. A new session never overwrites another article's files, and the pipeline can resume after the conversation is compacted or restarted.

**Clients.** Each client gets a folder in `clients/<client>/` in the working directory (git-ignored): `context-profiles/` (brand JSON profiles), `facts.md` (Defaults such as domain, voice, FAQ delivery and CTA; team roles; allowed and forbidden claims; usable cases), and `links.md` (service pages and scheduled posts that are not in the sitemap yet). `/research` asks for the client and profile, writes `<project>/client.txt`, and copies the profile to `<project>/context-profile.json`; every writing stage reads them, and `facts.md` wins over the profile. `/queue` takes both from the sheet. Prices and rate-card data in a profile never go into an article.

`/research` also validates the keyword with Semrush and Ubersuggest when those connectors are available. `/outline` collects 3–6 verified external sources, `/firstdraft` cites them inline, and `/finaldraft` writes a 16:9 feature image prompt to `feature-image-prompt.md`.

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
- Requires a confirmed CTA destination and button label.
- Uses only supplied or verified offer details.
- Applies stronger source and disclaimer checks to regulated or high-stakes claims.
- Never supplies a default domain, contact, palette, credential, product, or claim.

Requires `WebFetch` and `WebSearch`.

### `/convert-truemission` — NEX-U-TM

Runs the same conversion workflow with an isolated TrueMission/Prudential profile containing the approved domain, WhatsApp destination, brand palette, RIPLAY sourcing rules, UP planning formula, and insurance compliance checks.

This profile is Claude Code-only and is never loaded by the general `/convert` command.

### `/queue` — NEX-Q

Runs the whole pipeline from a Google Sheet, one row per article, with two review gates and no questions in chat. `ready` rows first get a cannibalization check: by search intent, not exact keyword, against the client's `links.md`, the sitemap, a `site:` search, the sheet's articles in progress, and the other `ready` rows of the run. Rows that share an intent are flagged together, and a row whose question an existing page already answers goes to `error` with that URL in the notes and three options (update that article, give the row a clearly different angle and set it to `ready` again, or skip it); a partial overlap continues with a named angle and opens the review brief. Then they get research, intent, GEO, and an outline, exported to a Google Doc (`outline-review`). After you comment and set `outline-approved`, the queue writes the draft, final draft, self-critique, CTA blocks, and the article Doc (`review`). Comment and set `revisi` for another pass, set `approved` to send the article to WordPress as a draft (`wp-draft`), or set `done`.

Up to 3 rows run in parallel, one subagent each; `/research` runs one row at a time because it drives the browser. Config lives in `nexus-output/queue.json` (`spreadsheet_id`, `tab`, optional `drive_folder`, optional `wp_site`, optional `default_client`). Columns are found by header name: Keyword, Market, Domain are required; Voice, FAQ, Word count, First-hand material, Internal links, CTA destination, Button label, Offer and allowed claims, Convert, Profile are optional or conditional. The sheet can also start with the keyword-research columns No, Month - Year, Keywords, Volume, Judul Artikel, Lang, and Notes, so research rows can be pasted in as they are: Judul Artikel becomes the working H1, Lang can stand in for Market (`id` = Indonesia), and Notes are the research brief (SERP observations, gap, angle, link and CTA hints, restrictions) that every stage checks against live data. Claude writes the NXS code, slug, both Doc links, last run, and notes. It never publishes, shares, or sends anything. Only Doc comments are read back, not edits typed into the Doc.

`scripts/wp-draft.py` sends an `approved` article's `latest.md` to WordPress through the REST API as a **draft** (never published): the H1 as the title, the slug, the article body with the CTA blocks as Custom HTML blocks, the Polylang language (`--lang`), the categories (`--category`, slugs looked up in that language; the queue takes them from the row's Notes or the client's `Kategori blog` Default), the Yoast SEO title and meta description from the YAML `title` and `meta-description`, and the FAQ metabox Q/A pairs to the ACF repeater `faq` (`faq_title`, `faq_content`, the gwenchana.digital field names), and the feature image: when `feature-image.png` (or `.jpg`, `.jpeg`, `.webp`) sits next to `latest.md`, it is uploaded to the media library with the `**Alt text:**` line of `feature-image-prompt.md` as alt text and the post's language, then set as the featured image. It stops instead of creating a duplicate when the slug already exists. An unknown category slug, Yoast fields or FAQ rows the site refuses to save, or a feature image it cannot set become notes; the draft is still created. The JSON-LD and the "Diperbarui" byline date stay manual, and so does the feature image when no file was saved. Auth comes from `WP_NEXUS_AUTH` (base64 of `username:application password`, from WordPress Users > Profile > Application Passwords); `--dry-run` shows the payload without sending anything.

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
- `truemission-prudential` — isolated Claude-only profile loaded by `/convert-truemission`.
