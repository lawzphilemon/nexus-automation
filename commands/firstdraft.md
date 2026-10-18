---
name: firstdraft
description: Write the full article draft following the confirmed outline, then silently apply the NEXUS humanizer before delivering
allowed-tools: Read, Write
---

# NEX-F — First Draft

**Mission:** Write the full article draft. Apply humanizer before delivery.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Client context:** if `<project>/client.txt` names a client, read `clients/<client>/facts.md` and `<project>/context-profile.json` before writing. Follow the profile's brand voice. `facts.md` wins when the two conflict, and its Defaults answer any input the user has not given. Claim nothing that the user, `facts.md`, or the profile does not support, and never put prices or rate-card data from the profile into the article.

**Dependency:** Confirmed outline from NEX-O. Missing → "Please confirm the outline from /outline first." If it is not in the conversation, read `<project>/04-outline.md`; it counts as confirmed only when its first line is `Status: confirmed`. Read `02-improve.md` and `03-geo.md` the same way when their data is needed.

1. Confirm language, word count, tone, brand voice from context. Ask if missing.
2. Write the complete draft following the approved outline. Apply:

**Keyword placement**
- Primary keyword: in H1, within first 100 words, in at least one H2, in final paragraph
- Semantic keywords from NEX-I: naturally distributed, not forced

**GEO writing rules**
- Direct Answer Block: 40–60 words, self-contained — must make sense if extracted with no surrounding context
- Definition Boxes: "[Term] is..." lead sentence format
- FAQ: each Q&A self-contained — answer makes sense without re-reading the question
- FAQ delivery (from the `FAQ delivery:` line in the first 3 lines of the outline, which is line 2 once confirmed; `body` if absent):
  - `body`: write the FAQ as an H2 section in the article.
  - `metabox`: the body has no FAQ section. After the article, add a separate `# FAQ metabox (paste per field)` block. Write each pair as a numbered item with the question in bold on its own line, a blank line, and the answer indented three spaces as its own paragraph (format in /finaldraft step 6), so the Doc shows the question and the answer on separate lines. The bold is only for review; the publisher pastes the question text and the answer into their own fields as plain text. Answers are plain text only (no links, bold, or lists), 40–60 words, and the first sentence answers the question directly
- Section answer sentences: every H2 opens with one sentence that answers the section and makes sense if extracted alone
- External sources: link each source from the outline where its claim appears, as a markdown link with descriptive anchor text (the source or page name), never a bare URL. Use only the recorded quote, if any
- Stat Blocks: cite inline — "According to [Source], [year], [stat]" — using only stats verified in NEX-G. Leave out any stat marked "Needs source"; never fill it from memory

**Voice** (from the outline's `Voice:` line; `brand` if absent and the article is for the brand's own site)
- `brand`: the brand speaks as "we"/"kami" and addresses the reader directly. Name the brand only where it helps as an entity signal (first self-reference such as "We at [Brand]…" / "Kami di [Brand]…", case studies, CTA). Never describe the brand from outside: no "[Brand]'s service page lists…", "[Brand] runs…", "according to [Brand]…". Brand claims still need the same evidence.
- `third-party`: name the brand in the third person and keep any disclosure from the outline.

**Human writing rules (apply before finalizing draft)**
- No transition fillers: delete Furthermore, Moreover, In addition, It is worth noting, In conclusion
- No stacked hedges: "could potentially possibly" → "may"
- No hollow paragraph openers — first sentence must carry information
- Paragraphs: maximum 4 sentences. Vary length throughout.
- Active voice as default.

3. **Apply humanizer before delivery, silently:**
   - Detect language. English → retrieve the `humanizer-en` skill. Indonesian → retrieve the `humanizer-id` skill. Mixed content → apply the correct skill per section, and state this once after delivery (not before).
   - Run the skill's self-check. Fix all failures. In metabox mode, humanize the FAQ metabox block too; it is visible on-page text.
   - Deliver only the humanized output. Do not announce this process before output.

4. Save the complete stage output to `<project>/05-firstdraft.md` (overwrite if it exists), then deliver it in chat.
5. End: "Review the draft. Run /finaldraft for final polish, compliance checks, and SEO pack."

## Rules
- Do not write without a confirmed outline.
- Do not deliver without running the humanizer skill.
- If brand voice guidelines are available in context, apply them before humanizing — brand voice wins over Layer 2 humanizer patterns, but never over Layer 0 SQEG protections in the skill.
- If the draft exceeds word count by more than 20%, flag it and suggest specific sections to trim before delivering.
- If the draft is more than 20% under word count, do not pad with filler — expand thin sections using NEX-I/NEX-G data and tell the user which sections were expanded and why.
