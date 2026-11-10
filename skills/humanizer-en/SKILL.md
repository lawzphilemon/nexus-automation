---
name: humanizer-en
description: "Use when writing or finalizing English article content (NEX-F, NEX-Fn, or /humanize). NEXUS wrapper (Layer 0 SQEG, register, brand voice, self-check) around the blader/humanizer pattern catalog, so output reads like a competent human writer, not AI, while preserving E-E-A-T signals."
---

# Humanizer English (NEXUS)
Version 3.0 | Pattern catalog: blader/humanizer (MIT), see `UPSTREAM.md`

## Purpose

Humanizer filter for all English article output. Apply it to every piece of content you write or rewrite. Do not announce this process to the user. Apply it silently before delivering.

The goal is writing that sounds like a knowledgeable person, not an AI, while meeting Google's Page Quality standards (E-E-A-T, MC Quality, Needs Met).

NEXUS owns Layer 0, the register, and the self-check. The AI-pattern catalog (Layer 2) comes from upstream and is read from `references/`.

## How to Apply This

1. **Layer 0 first**: protect SQEG-critical elements before touching anything
2. **Layer 1**: determine the register (formal / semi-formal / casual)
3. **Layer 2**: scan and fix AI patterns with the upstream catalog (see the Layer 2 section)
4. **Self-check**: run the checklist before delivering
5. **Output only**: deliver the rewritten text with no preamble, no changelog

**Precedence when rules clash:** verified facts and the CTA from `/convert` > Layer 0 SQEG > brand voice (if present) > Layer 2 AI patterns. Brand voice beats Layer 2 patterns, never Layer 0.

---
## LAYER 0: SQEG PROTECTIONS (Non-Negotiable)

These six rules override everything in Layer 2. No pattern may break them.

---

### G1. Format Hyperlinks Based on Output Medium

Hyperlink format MUST match the output medium.
Using the wrong format causes raw URLs to appear in parentheses — a clear sign of unpolished AI output.

**Detect the output medium before writing any link:**

| Medium | Correct format | Example |
|---|---|---|
| Website / blog / CMS | Markdown anchor text | `[anchor text](url)` |
| Instagram / Facebook caption | Plain text + separate CTA | `Click the link in bio to book.` |
| WhatsApp / Telegram | Plain URL, no markdown | `Chat with me: s.id/example` |
| Email (plain text) | Plain URL | `s.id/example` |
| Email (HTML / rich text) | HTML anchor | `<a href="url">anchor text</a>` |
| Word doc / PDF | Anchor text + URL in parentheses | `See the guide (example.com/guide)` |

**Universal rules — apply across all mediums:**
- NEVER combine anchor text with a URL in the same sentence unless the medium is a document
- NEVER write `anchor text (url)` — this is the pattern that exposes the URL outside the link
- NEVER use a bare URL as anchor text for website content
- If the medium is not clear from context, ask the user BEFORE writing any links

❌ Wrong (all mediums): "Click here to chat with me (s.id/example)"
❌ Wrong (all mediums): "Read the full guide at https://example.com/guide"
✅ Correct (website): "Book a [free consultation](s.id/example) — no pressure, no sales script."
✅ Correct (Instagram): "Want a policy review or coverage projection? Link in bio."
✅ Correct (WhatsApp): "Message me directly at s.id/example"

---

### G2. Preserve List Format for Procedural and Spec Content

Do NOT convert to prose: how-to steps, technical specs, checklists, FAQ sections, product comparisons.
For these: remove AI-style bold labels but keep the list structure.
Convert to prose ONLY narrative and argumentative sections.

❌ Do not convert procedural steps:
"- **Step 1:** Power down the main circuit
- **Step 2:** Mount the MCB on the DIN rail"

✅ Correct — remove bold labels, keep list:
"1. Power down the main circuit before touching any panel components
2. Mount the MCB on the DIN rail with even pressure along the clip"

---

### G3. Keep YMYL Safety Caveats

YMYL topics: electrical safety, health and nutrition, financial guidance, regulatory compliance, workplace safety.

Keep these phrases (do NOT strip them as filler):
- "Consult a certified electrician before installation."
- "Switch off the main breaker before proceeding."
- "Results may vary depending on local grid conditions."
- "Verify current compliance requirements with your local authority."

Still delete: "As of my last training update", stacked hedges like "could potentially possibly suggest".

---

### G4. Make Headings Specific and Descriptive

All H2/H3 headings must be specific enough to stand alone as informative statements.

❌ Generic: "Benefits of Phoenix Contact Relays"
✅ Specific: "Phoenix Contact vs Omron relay: response time and service life compared"

Sentence case only. No Title Case In Every Word.

---

### G5. Keep First-Hand Experience and Practitioner Observations

Do not strip anecdotal or field-based evidence. These are E-E-A-T experience signals.

❌ Delete (vague): "Experts believe it plays a crucial role"
✅ Preserve (specific experience): "From three commissioning projects in Bekasi's industrial zone,
this configuration consistently outperformed the manufacturer's default setting under peak load."

---

### G6. Replace Deleted Transitions — Do Not Just Delete Them

When you remove AI transition phrases (Pattern 7), replace them with a specific logical connection.
An article with no transitions feels choppy. That signals low quality to Google raters.

❌ Delete the phrase: "Furthermore, it is important to consider the load characteristics."
✅ Replace with specific connection: "Relay selection comes down to one number from the load
analysis: peak inrush current at motor startup."

---

## LAYER 1: DETERMINE REGISTER

Before running patterns, establish the register and hold it throughout.

- **Formal**: full sentences, no contractions → B2B content, technical documentation, legal/financial
- **Semi-formal**: natural tone, occasional contractions → blog posts, LinkedIn, email marketing
- **Casual**: conversational, direct → social posts, lifestyle content

---

---

## LAYER 2: AI PATTERNS (upstream catalog)

Read `references/upstream-skill.md` (the 26-pattern catalog, process, and examples) and apply it with these NEXUS adjustments:

- **Ignore** upstream's interactive steps (asking for a writing sample, asking the user questions) and its report or change-summary output. The NEXUS pipeline must not stop to ask and delivers only the finished text.
- Voice: use the client's brand voice when it is in context. Without one, follow the register from Layer 1.
- Do not apply patterns to code, JSON, data tables, or the CTA blocks produced by `/convert`.

---

## SELF-CHECK (Run before every delivery)

**Layer 0 — SQEG:**
1. All internal links have descriptive anchor text? No naked URLs?
2. Procedural, spec, and comparison lists kept as lists (bold labels removed only)?
3. YMYL content still has appropriate professional caveats?
4. All headings specific and descriptive? Sentence case?
5. Deleted transitions replaced with specific logical connections?

**Layer 2 (AI patterns):**
6. Every pattern group in `references/upstream-skill.md` scanned (staging, rhythm, inflation, formatting, chatbot leftovers, wrong reader)?
7. Paragraphs varied in length and sentence rhythm mixed?
8. Any trailing present-participle clauses or "In today's X" openers left?
9. More than one em dash in any paragraph? Any en dash mid-sentence?
10. Ending specific, not inspirational?
11. Read aloud, does it sound like a person?

---

## When the User Says "Humanize This"

1. Determine register (formal / semi-formal / casual)
2. Run Layer 0, protect all SQEG-critical elements before touching anything
3. Run Layer 2 with the upstream catalog
4. Preserve all meaning: change HOW it is said, not WHAT it says
5. Run the 11-point self-check
6. Output only the rewritten text, no preamble and no explanation of changes
