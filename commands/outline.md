---
name: outline
description: Build the GEO-compliant article outline, discover real internal links from the target website, and tag conversion points for later CTA placement
allowed-tools: WebFetch, WebSearch, Read, Write, Bash
---

# NEX-O — Article Outline

**Mission:** Build the GEO-compliant article outline with real, verified internal links and pre-tagged conversion points.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Client context:** if `<project>/client.txt` names a client, read `clients/<client>/facts.md` and `<project>/context-profile.json` (when the project has one) before writing. Follow the profile's brand voice. `facts.md` wins when the two conflict, and its Defaults answer any input the user has not given. Claim nothing that the user, `facts.md`, or the profile does not support, and never put prices or rate-card data from the profile into the article.

**Dependency:** Requires NEX-R, NEX-I, NEX-G output. Missing → "Run /research, /improve, /geo first." Read `<project>/01-research.md`, `02-improve.md`, and `03-geo.md` for any output not in the conversation.

## Step 1 — Confirm basics
Confirm: target language, word count, tone of voice, end-goal CTA. Ask if missing, recommend best practice if unsure (informational 1,500–2,500 words, comparison 2,000–3,000, how-to 1,200–2,000, based on NEX-R SERP average if available).

Also confirm **FAQ delivery: body (default) | metabox**:
- `body`: the FAQ is an H2 section in the article, and the article's JSON-LD includes FAQPage.
- `metabox`: the site's CMS has a FAQ field or metabox that renders the FAQ and emits its own FAQPage schema. The FAQ is delivered as a separate block, not in the body.

If the user does not know, offer a read-only check on 1–3 existing posts of the target site:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/faq-scan.py" "<post URL>" ["<post URL>" ...]
```

Each line reads `<questions> <placement> <url>`. `standalone` FAQPage nodes suggest a metabox or widget; `graph` suggests an SEO plugin and an in-body FAQ. If any post shows `0`, tell the user their template outputs an empty FAQPage (`mainEntity: []`), which is invalid structured data, and that it should print only when at least one question exists. Suggest a mode from the result and let the user confirm. If Python is unavailable, ask the user instead. Default to `body` when unknown.

Also confirm **Voice: brand (default) | third-party**, i.e. who is speaking in the article:
- `brand`: the article is published on the brand's own site, so the brand speaks as "we" ("kami" in Indonesian) and addresses the reader directly. Use this whenever the target domain belongs to the brand.
- `third-party`: a media, review, or guest post where the writer is outside the brand and names it in the third person, with a disclosure if there is a relationship.

## Step 2 — Internal Link Discovery

If the user has already provided specific internal links to use, skip discovery and go straight to Step 3 using those.

If `<project>/client.txt` names a client, read `clients/<client>/links.md` first. Its service table and notes take priority over topics inferred from URLs. Rows under "Terjadwal" may be used before they reach the sitemap: mark each one `(scheduled, live <date>)` in the outline, and list it in the notes so the publisher confirms it is live before publishing.

Otherwise:
1. Ask for the target website domain if not already known. Never assume a default domain.
2. Try fetching the sitemap: `https://{domain}/sitemap.xml`, then `https://{domain}/sitemap_index.xml` if the first fails, via WebFetch. Parse out URLs.
3. If no sitemap is reachable, fall back to WebSearch: `site:{domain} [seed keyword]` and `site:{domain} [related semantic term from NEX-I]`.
4. From the candidate URLs, keep only same-domain content pages — drop tag/category/pagination/author archive pages. Prioritize by topical relevance to the seed keyword and NEX-I semantic terms.
5. Present a shortlist (max 8) to the user as: `URL — inferred topic`. Ask which ones fit this article and what anchor text to use for each. If a page's exact topic is unclear from the URL/title alone, briefly fetch that page to check before recommending it.
6. If sitemap and search both fail to surface anything usable, tell the user directly and ask them to paste links manually. Never invent a URL that wasn't actually found or verified.

**Existing coverage (cannibalization).** If `<project>/00-cannibalization.md` exists (queue runs), follow it and skip this check. Otherwise, while scanning `links.md`, the sitemap, and the `site:` results, look for pages in the article's language that already answer the same search intent: compare the intent from NEX-I with each page's title, H1, and H2s, not the exact keyword. A page that already answers the main question (the keyword is its topic, a synonym of it, or one of its H2s), or covers the same topic with the same angle, goes to the user before the outline is written, with its URL and the H2 that shows the overlap, and three options: update that article instead, take a clearly different angle (name it), or stop. Write the outline only after the user picks the angle. A page that shares only one subtopic becomes an internal link for that subtopic, and the outline does not cover it again.

## Step 2b — External sources

Find 3–6 authoritative external sources for the article's key claims: official documentation, platform help centers, regulators, standards bodies, primary research, or recognized industry data. Prefer primary over secondary, and current over old. Reuse the stats already verified in NEX-G.

Open each page (browser or WebFetch) and confirm it says what the article will claim. Record for each source: the claim it supports, the source name, the exact URL, its publish or update date, and at most one short quote (under 15 words) if a direct quote helps. A claim without a source that confirms it is softened or dropped, never cited from memory. Never link a competitor agency or a page that sells the same service as the brand.

## Step 3 — Produce the outline

```
H1: [keyword-optimized, under 60 characters]

[DIRECT ANSWER BLOCK] — 40–60 words. Immediately after H1.
Self-contained. Must answer the seed keyword without needing surrounding context.

H2: [section title]
  — Basis: [NEX-I or NEX-G finding that justifies this section]
  — GEO structure: [structure this section uses]
  — Conversion point: [None / Variant 1 or 2 (earlier CTA, only if the CTA count is 2) / Variant 3 (closing CTA)]
  — External sources: [source name -> verified URL -> claim it supports, or None]
  — Estimated words: [X–Y]
  H3: [subsection if needed]

[repeat for all sections]

H2: Frequently Asked Questions          ← body mode only
  — Questions: [exact FAQ questions, minimum 5]
  — Source: PAA + NEX-G fan-out
  — Schema: FAQPage

[CLOSING SECTION]
  — CTA: [action the reader takes]
  — Internal links: [anchor text → verified URL]

[FAQ — METABOX, not in the body]         ← metabox mode only
  — Questions: [exact FAQ questions, minimum 5]
  — Source: PAA + NEX-G fan-out
  — Schema: generated by the CMS metabox
  — Estimated words: [X–Y], counted outside the body word count
```

Start the outline with two header lines: `FAQ delivery: [body / metabox]` and `CTAs: [1 / 2] — [one-line reason]`, for example `CTAs: 1 — no section past 40% maps to the offer` or `CTAs: 2 — after "[section]", where the reader [reason]`. In metabox mode, the last CTA (Variant 3) stays at the end of the body, because the metabox renders after it.

**CTA count — decide 1 or 2.** The closing CTA (Variant 3) at the end of the body is always used. Add one earlier CTA only when all of these are true:

1. The planned body is at least 1,500 words.
2. A section ends where the reader has just seen the problem the offer solves, or a task they would rather hand off, so the CTA follows naturally from it: Variant 1 after a mechanism or process, Variant 2 after a problem or risk.
3. That section starts at least 40% into the body. Never use the introduction, the Direct Answer Block, or the first H2.
4. At least two H2 sections separate it from the closing CTA.

If any condition fails, use 1 CTA. When in doubt, use 1.

**Conversion point tagging rule:** tag only where a reader naturally pauses after getting real value. Never tag the Direct Answer Block, a Definition Box, or the FAQ section — those must stay self-contained. Tag the closing CTA, plus the earlier CTA only when the CTA count is 2.

## Step 4 — Confirm
Ask the user to confirm the outline, including the internal links, the CTA count with its reason, and the conversion point tags, before proceeding. The user can override the CTA count.

Save the outline to `<project>/04-outline.md` (overwrite if it exists), then deliver it in chat. When the user confirms it, apply any requested changes to that file and insert `Status: confirmed` above the existing header. A confirmed outline always starts:

```text
Status: confirmed
FAQ delivery: [body / metabox]
CTAs: [1 / 2] — [reason]
Voice: [brand — <Brand> as "we"/"kami" / third-party]
```

End: "Confirm the outline above, then run /firstdraft."

## Rules
- Every H2/H3 needs a stated basis. Direct Answer Block + FAQ are non-negotiable in both FAQ delivery modes.
- Every internal link must be a real, discovered or user-provided URL — never fabricated.
- Every external source must be opened and confirmed in Step 2b — never cited from memory.
- Conversion points are tagged here, not decided later during /convert — /convert should place CTA copy at these exact tagged positions, not re-scan the draft.
- NEX-F is blocked until this outline is confirmed.
