---
name: convert
description: Add site-branded contact CTAs and factual product or service mentions to a finished article
allowed-tools: Read, Write, WebFetch, WebSearch
---

# NEX-U — Conversion Layer

**Mission:** Turn a finished article into a lead-generating asset by adding relevant contact CTAs and optional product or service mentions at natural reading pauses, without breaking GEO/SEO structure or making unsupported claims.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Client context:** if `<project>/client.txt` names a client, read `clients/<client>/facts.md` and `<project>/context-profile.json` before writing. Follow the profile's brand voice. `facts.md` wins when the two conflict, and its Defaults answer any input the user has not given. Claim nothing that the user, `facts.md`, or the profile does not support, and never put prices or rate-card data from the profile into the article.

**Dependency:** Requires a finished article draft, ideally `<project>/latest.md` from NEX-Fn. Read that artifact first. If neither the artifact nor a complete draft exists: "Paste the final draft, or run /finaldraft first."

Retrieve the `wa-cta-standard` and `product-upsell` skills before writing any output.

## Step 0 — Confirm conversion inputs

Confirm these inputs from context or ask for them:

1. **Target website domain** for brand-color detection.
2. **CTA destination and button label**, such as a WhatsApp link, contact form, email link, booking page, or product page.
3. **Offer details**, if a product or service should be mentioned: name, audience, verified features, evidence, restrictions, and approved claims.

Never invent or reuse a domain, contact destination, brand palette, credential, product detail, price, or claim.

### Brand-color detection

1. WebFetch the website homepage.
2. Identify visible colors used for navigation, primary buttons, accents, text, backgrounds, and borders.
3. Map them to the `wa-cta-standard` color slots.
4. If a required color cannot be identified confidently, ask the user for it or reuse the closest observed color while preserving readable contrast. Do not invent a brand color.
5. Confirm the palette and CTA destination in one line before proceeding.

## Step 1 — Locate conversion points

Each article gets 1 or 2 CTAs. The closing CTA (Variant 3) is always used; an earlier CTA is optional.

If the outline has a `CTAs:` header line, use its `Conversion point` tags exactly. If it has no `CTAs:` line (an outline made before this rule), or no tags at all, apply this rule and keep at most one earlier tag that passes it:

**CTA count — decide 1 or 2.** The closing CTA (Variant 3) at the end of the body is always used. Add one earlier CTA only when all of these are true:

1. The planned body is at least 1,500 words.
2. A section ends where the reader has just seen the problem the offer solves, or a task they would rather hand off, so the CTA follows naturally from it: Variant 1 after a mechanism or process, Variant 2 after a problem or risk.
3. That section starts at least 40% into the body. Never use the introduction, the Direct Answer Block, or the first H2.
4. At least two H2 sections separate it from the closing CTA.

If any condition fails, use 1 CTA. When in doubt, use 1.

Never place a CTA mid-sentence, mid-list, inside a Direct Answer Block, FAQ answer, FAQ metabox block, Definition Box, metadata section, or schema. State the CTA count and its one-line reason in the delivery message.

## Step 2 — Map the offer

Follow `product-upsell` using only verified offer details from Step 0.

- Add one soft, factual sentence connecting the offer to the section above, in the article's voice: in `brand` voice the brand speaks as "we"/"kami" ("Our team…", "Tim kami…"), never "[Brand] provides…".
- Add a short comparison table only when the supplied data supports it.
- If offer details are missing, ask for them or skip the offer mention and insert CTAs only.
- For regulated or high-stakes topics, use current authoritative sources and include required qualifications or disclaimers. If those inputs are unavailable, do not publish the claim.

## Step 3 — Write and inject CTA blocks

Follow `wa-cta-standard` for the three HTML variants. Match each block's copy to the section immediately above it. Use the confirmed CTA destination and button label.

Never exceed two CTA blocks per article.

## Step 4 — Validate

Before delivery, verify:

- No fabricated claims, prices, statistics, testimonials, credentials, or product details.
- No guaranteed outcomes or unsupported comparisons.
- Every link and color comes from confirmed input or the target website.
- Regulated claims include the required source, qualification, and disclaimer.
- The article's GEO/SEO structure, On-Page SEO Pack, and Schema Markup remain unchanged.

Fix every failure before delivery.

## Output

Write the full converted article back to `<project>/latest.md`, preserving its YAML metadata and replacing only the article body with CTA blocks inserted at their exact positions. Keep any `FAQ metabox (paste per field)` block unchanged, with no CTA copy in it. Take the FAQ delivery mode from the artifact's `faq-delivery` YAML field, not from line positions. Put every CTA block in a fenced `html` block so Pandoc exports it as plaintext, paste-ready code.

Preserve the On-Page SEO Pack fields in YAML and keep Schema Markup unchanged as the final heading and fenced `json` block.

Directly below each CTA block, add:

`[Paste this block in WordPress Classic Editor → Text tab. Do not switch to Visual tab after pasting.]`

Do not duplicate the full article in chat unless explicitly requested. End with: "CTA placement done - [N] block(s) inserted in <project>/latest.md. Run /export-gdoc to export this converted version."
