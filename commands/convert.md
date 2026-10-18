---
name: convert
description: Add site-branded contact CTAs and factual product or service mentions to a finished article
allowed-tools: Read, Write, WebFetch, WebSearch
---

# NEX-U — Conversion Layer

**Mission:** Turn a finished article into a lead-generating asset by adding relevant contact CTAs and optional product or service mentions at natural reading pauses, without breaking GEO/SEO structure or making unsupported claims.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Client context:** if `<project>/client.txt` names a client, read `clients/<client>/facts.md` and `<project>/context-profile.json` (when the project has one) before writing. Follow the profile's brand voice. `facts.md` wins when the two conflict, and its Defaults answer any input the user has not given. Claim nothing that the user, `facts.md`, or the profile does not support, and never put prices or rate-card data from the profile into the article.

**Dependency:** Requires a finished article draft, ideally `<project>/latest.md` from NEX-Fn. Read that artifact first. If neither the artifact nor a complete draft exists: "Paste the final draft, or run /finaldraft first."

Retrieve the `wa-cta-standard` and `product-upsell` skills before writing any output.

**Client conversion rules.** When `clients/<client>/conversion.md` exists, read it too. It may fix the CTA palette (the `wa-cta-standard` tokens), the CTA channel and how to get its destination, an offer mapping, required sources (for example a product brochure or a regulator page), formulas the client approved, and compliance rules or disclaimers. Where it conflicts with `product-upsell`, the client file wins; `facts.md` still wins on what may be claimed, and an explicit instruction from the user wins after you confirm it. Never load one client's `conversion.md` for another client.

## Step 0 — Confirm conversion inputs

Confirm these inputs from context or ask for them:

1. **Target website domain** for brand-color detection.
2. **CTA contact**: always asked, see the contact question below.
3. **Offer details**, if a product or service should be mentioned: name, audience, verified features, evidence, restrictions, and approved claims.

Never invent or reuse a domain, contact detail, brand palette, credential, product detail, price, or claim.

### Contact question (every run, before any CTA is written)

There is no default phone number, email, or address, in this plugin or anywhere else. Before writing a CTA block, ask the user in one message:

1. **Channel:** phone, email, address, or all of them (any combination is fine).
2. **Details for each chosen channel:**
   - Phone: the number, and whether the button opens a WhatsApp chat or a phone call. For WhatsApp, an optional pre-filled message.
   - Email: the address, and an optional subject line.
   - Address: the full address as it should appear, and an optional maps link the user supplies.
3. **Button label** for each button.

When `clients/<client>/facts.md` has a **Kontak untuk CTA** list, or the queue row or the user's notes give a contact or label, show them in the same message as numbered choices. They are choices only: the user picks one, several, or types new details. Never choose for the user, never take a contact from the website, the context profile, or an earlier article or session without asking, and never fill a missing detail yourself. In queue mode the queue asks this once per brand at the start of the run (`queue.md` section 3) and passes the answer here: use that answer and ask nothing more.

Build the links from the answer: WhatsApp `https://wa.me/<digits>` (international format with no `+` or spaces; a number starting with `0` gets the country code of the article's market, for example `0812…` → `62812…` for Indonesia), with `?text=` and the URL-encoded message when one was given; phone call `tel:+<digits>`; email `mailto:<address>`, with `?subject=` and the URL-encoded subject when one was given. An address is text, linked only to a maps URL the user gave. Confirm the channels, details, and labels in one line before writing.

### Brand-color detection

1. WebFetch the website homepage.
2. Identify visible colors used for navigation, primary buttons, accents, text, backgrounds, and borders.
3. Map them to the `wa-cta-standard` color slots.
4. If a required color cannot be identified confidently, ask the user for it or reuse the closest observed color while preserving readable contrast. Do not invent a brand color.
5. Confirm the palette and the CTA contact in one line before proceeding.

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

Follow `wa-cta-standard` for the three HTML variants. Match each block's copy to the section immediately above it. Use only the channels, details, and button labels confirmed in the contact question.

Never exceed two CTA blocks per article.

## Step 4 — Validate

Before delivery, verify:

- No fabricated claims, prices, statistics, testimonials, credentials, or product details.
- No guaranteed outcomes or unsupported comparisons.
- Every link and color comes from confirmed input or the target website.
- Every phone number, email, and address in a CTA block was chosen in this run's contact question.
- Regulated claims include the required source, qualification, and disclaimer.
- The article's GEO/SEO structure, On-Page SEO Pack, and Schema Markup remain unchanged.

Fix every failure before delivery.

## Output

Write the full converted article back to `<project>/latest.md`, preserving its YAML metadata and replacing only the article body with CTA blocks inserted at their exact positions. Keep any `FAQ metabox (paste per field)` block unchanged, with no CTA copy in it. Take the FAQ delivery mode from the artifact's `faq-delivery` YAML field, not from line positions. Put every CTA block in a fenced `html` block so Pandoc exports it as plaintext, paste-ready code.

Preserve the On-Page SEO Pack fields in YAML and keep Schema Markup unchanged as the final heading and fenced `json` block.

Directly below each CTA block, add:

`[Paste this block in WordPress Classic Editor → Text tab. Do not switch to Visual tab after pasting.]`

Do not duplicate the full article in chat unless explicitly requested. End with: "CTA placement done - [N] block(s) inserted in <project>/latest.md. Run /export-gdoc to export this converted version."
