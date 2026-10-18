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

Builds a GEO-compliant outline, discovers verified internal links from the supplied domain, and tags natural conversion points.

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

Runs the whole pipeline from a Google Sheet, one row per article, with two review gates and no questions in chat. `ready` rows get research, intent, GEO, and an outline, exported to a Google Doc (`outline-review`). After you comment and set `outline-approved`, the queue writes the draft, final draft, self-critique, CTA blocks, and the article Doc (`review`). Comment and set `revisi` for another pass, set `approved` to send the article to WordPress as a draft (`wp-draft`), or set `done`.

Up to 3 rows run in parallel, one subagent each; `/research` runs one row at a time because it drives the browser. Config lives in `nexus-output/queue.json` (`spreadsheet_id`, `tab`, optional `drive_folder`, optional `wp_site`). Columns are found by header name: Keyword, Market, Domain are required; Voice, FAQ, Word count, First-hand material, Internal links, CTA destination, Button label, Offer and allowed claims, Convert, Profile are optional or conditional. Claude writes the NXS code, slug, both Doc links, last run, and notes. It never publishes, shares, or sends anything. Only Doc comments are read back, not edits typed into the Doc.

`scripts/wp-draft.py` sends an `approved` article's `latest.md` to WordPress through the REST API as a **draft** (never published): the H1 as the title, the slug, the article body with the CTA blocks as Custom HTML blocks, and the Polylang language (`--lang`). It stops instead of creating a duplicate when the slug already exists. The FAQ metabox, the Yoast title and meta description, the JSON-LD, the category, and the feature image stay manual. Auth comes from `WP_NEXUS_AUTH` (base64 of `username:application password`, from WordPress Users > Profile > Application Passwords); `--dry-run` shows the payload without sending anything.

### `/export-gdoc` — NEX-GD

Exports the latest final or converted article to a Google Doc through the Google Drive connector, containing:

- A metadata table for article title, slug, meta description, main keyword, related keywords, and publisher notes (when any).
- Real headings for the article hierarchy.
- Preserved lists, links, article tables, and CTA HTML as paste-ready code.
- The FAQ metabox block, when that mode is used.
- JSON-LD schema at the end.

It uses Pandoc with the bundled Lua filter; install Pandoc from [pandoc.org/installing.html](https://pandoc.org/installing.html). The Doc stays private until you share it. Without a Google Drive connector, the command keeps the generated HTML file so you can upload it to Drive and open it with Google Docs.

### `/humanize` — NEX-H

Humanizes Indonesian, English, or mixed text while preserving meaning and E-E-A-T signals.

## Supporting skills

- `humanizer-id` and `humanizer-en` — language-specific humanization.
- `wa-cta-standard` — three generic, site-branded CTA layouts.
- `product-upsell` — evidence-gated product or service mapping for any industry.
- `truemission-prudential` — isolated Claude-only profile loaded by `/convert-truemission`.
