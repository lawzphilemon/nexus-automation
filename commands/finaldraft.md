---
name: finaldraft
description: Final polish on a first draft - re-run humanizer, GEO/SEO/humanizer compliance checklists, On-Page SEO Pack, and Schema JSON-LD
allowed-tools: Read, Write
---

# NEX-Fn - Final Polish + SEO Pack + Schema

**Mission:** Final polish, three compliance checks, On-Page SEO Pack, Schema JSON-LD.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Context profile:** if `<project>/context-profile.json` exists, read it before writing and follow its brand voice, facts, and services. Never put prices or rate-card data from it into the article.

**Dependency:** Requires a NEX-F draft. Missing -> "Run /firstdraft first." If the draft is not in the conversation, read `<project>/05-firstdraft.md`. Read `02-improve.md` and `03-geo.md` the same way for the compliance checks. Take the FAQ delivery mode from the `FAQ delivery:` line in the first 3 lines of `<project>/04-outline.md`; if that is unavailable, use `metabox` when the draft has a `FAQ metabox (paste per field)` block, otherwise `body`.

1. Re-run the humanizer skill (`humanizer-en` or `humanizer-id`, matching the draft's language) on the draft - same process as NEX-F step 3. Do not announce.

2. Run three compliance checklists. Fix all failures internally before delivering - never deliver non-compliant content.

**GEO compliance**
- [ ] Direct Answer Block present, self-contained, 40-60 words?
- [ ] All FAQ Q&As self-contained?
- [ ] Metabox mode only: no FAQ section in the body, metabox answers are plain text and 40–60 words, and the metabox block matches the questions from the outline?
- [ ] Definition Boxes use "[Term] is..." format?
- [ ] Every H2 opens with a self-contained answer sentence?
- [ ] Stat Blocks cite source + year inline, and every stat was verified in NEX-G?
- [ ] Comparison Table present (if NEX-G prescribed it)?
- [ ] All fan-out sub-queries from NEX-G covered in content?

**SEO compliance**
- [ ] Primary keyword in H1, first 100 words, at least one H2, final paragraph?
- [ ] Semantic keywords from NEX-I distributed naturally?
- [ ] Internal links present with descriptive anchor text?
- [ ] Heading hierarchy correct (H1 -> H2 -> H3, no skipped levels)?
- [ ] No duplicate heading text?

**Voice compliance** (from the outline's `Voice:` line; `brand` if absent and the article is for the brand's own site)
- [ ] `brand`: the brand speaks as "we"/"kami" throughout, including the FAQ, and no sentence describes the brand from outside ("[Brand]'s service page lists…", "[Brand] runs…")?
- [ ] `third-party`: the brand is named in the third person, with the disclosure if there is one?

**Humanizer compliance:** run the humanizer skill's self-check in full. Fix failures before delivery.

3. Finalize the article in clean markdown. Bold technical terms on first use only.

4. Build the On-Page SEO Pack:

```text
Title tag (under 60 characters): [title]
Meta description (under 160 characters): [meta - include primary keyword + benefit or action signal]
URL slug: /[keyword-slug-no-stopwords]
H1: [final H1]
Image alt text template: "[descriptive phrase including primary keyword] - [context]"
Internal links used: [anchor text] -> [destination URL]
```

5. Generate Schema Markup (JSON-LD) based on NEX-G's recommendation. In body mode, include FAQPage with all Q&A pairs verbatim. In metabox mode, exclude FAQPage entirely, because the CMS metabox emits it.

6. Write the complete result once to `<project>/latest.md`. Do not duplicate the article in chat. Use this exact artifact structure:

````markdown
---
title: "[Title tag]"
slug: "/[slug]"
meta-description: "[Meta description]"
h1: "[H1]"
image-alt-text-template: "[Image alt text template]"
internal-links-used: "[anchor -> URL; anchor -> URL]"
faq-delivery: "[body or metabox]"
main-keyword: "[primary keyword]"
related-keywords:
  - "[related keyword]"
notes:
  - "[open item for the publisher]"
---

# [H1]

[Complete article]

# FAQ metabox (paste per field)

[Metabox mode only: numbered plain-text Q/A pairs. Omit this heading in body mode.]

# Schema Markup (JSON-LD)

```json
{
  "@context": "https://schema.org",
  "@type": "[schema type]"
}
```
````

`main-keyword` and `related-keywords` are mandatory. Related keywords are the NEX-I semantic keywords actually used in the article. `notes` lists only open items the publisher must act on before publishing, such as a stat still marked "Needs source", an image or screenshot to add, a disclaimer to confirm, or notes the user asked to include. Omit `notes` entirely when there are none. These fields appear in the metadata table of `/export-gdoc`.

Write valid YAML and escape values when needed. The article must contain no duplicated SEO pack. The schema heading and fenced JSON block must be last.

7. Offer the next action:

```text
Final draft complete and saved to <project>/latest.md. Choose:
1. Revise the article
2. Run /constructive-self-criticize (recommended before /convert)
3. Run /convert
4. Run /export-gdoc (Google Docs)
5. Run /convert, then /export-gdoc
```

If the user chooses option 5, complete `/convert` first and export that converted version without asking them to repeat the request.

Paste the full article into chat only when the user explicitly asks to see it.

## Rules

- On-Page SEO Pack and Schema are mandatory - never skip.
- All compliance failures must be fixed before delivery.
- Never use em dashes in any output - article body, checklist items, or SEO pack.
- Never write `anchor text (url)` - this exposes the URL visibly. Use proper markdown links, or ask the user to confirm the output medium if it is ambiguous whether markdown will render.
