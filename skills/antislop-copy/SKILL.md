---
name: antislop-copy
description: "Use at the end of /finaldraft (and when /queue finalizes an article) to run the antislop prose gate: a PASS/FAIL check of the finished article against the antislop copywriting rules (no fabricated claims, stats, testimonials, or weasel attributions; AI-vocabulary and rhythm tells). Non-interactive; checks, does not rewrite."
---

# antislop-copy (NEXUS prose gate)

Prose-only adaptation of anti-slop v3.2.28 (MIT, see `UPSTREAM.md`). The upstream core is built for UI work and asks the user questions. NEXUS runs headless, so use only this file plus the two references:

- `references/core-rules.md`: the rules that govern prose (R-02, R-15, R-16, R-17, R-18, R-36, R-38, C-5).
- `references/copywriting.md`: the pattern catalog with before/after fixes and the "What NOT to flag" and "Signs of human writing" sections.

Never ask the user a question, never ask for a mode, never create assets. Silent unless a check fails.

## Where it runs

After the humanizer. It is a **gate**, not a second rewrite: the humanizer writes, antislop checks. Run once per article, in the article's language. The patterns are English-first; for Bahasa Indonesia judge the same patterns by meaning (empty vocabulary, significance inflation, weasel attribution, rule of three, generic closers), and trust `humanizer-id`'s own catalog for Indonesian wording.

## Precedence

Verified facts, the CTA from `/convert`, and Layer 0 SQEG of the humanizer beat antislop. A CTA the owner asked for is not a violation of R-15, a brand voice the owner approved is not a violation of "no voice", and the em dash ban (R-02) does not apply inside quoted source text, code, or schema.

## Gate

Read the finished article (`latest.md` or the file the stage names). Answer each line with PASS, WARN, or FAIL and one line of evidence. WARN means supported but needing the owner's action, for example a claim backed by `facts.md` that the reader cannot check because the article gives no link. WARN is not fixed by rewriting: it goes to the notes. Skip a line only if its element is absent and say `n/a`.

1. **R-17 numbers:** every statistic, percentage, price, or date has a source named in the article or in `facts.md`? No invented "10K+ users" style figures.
2. **R-18 testimonials:** no quote, customer name, or case result that is not in a verified source.
3. **R-36 / R-38 fabricated claims:** no invented security, compliance, performance, award, or customer claims; no ghost links or fictional team members.
4. **Weasel attribution:** no "experts say", "studies show", "industry observers" without a named source.
5. **R-16 buzzwords:** none of the empty AI vocabulary or significance inflation listed in `references/copywriting.md` (Tone and Voice).
6. **R-02 em dashes:** none in body text outside quotes, code, and schema.
7. **Rhythm and structure:** no clusters of rule-of-three, negative parallelism, staccato drama, theatrical takeaways, or a generic positive conclusion (clusters, not single hits).
8. **Hygiene:** no bold on every key term, no emoji in headings, no inline-header lists that restate the item, no chatbot closers or signposting announcements.
9. **Honesty:** no speculative gap-filling: a missing detail is left out or marked for the owner, not invented.

Do not flag anything under "What NOT to flag" in `references/copywriting.md`. Do not strip real voice to satisfy a pattern (over-sterilizing is itself a tell).

## Output

Write the report to `<project>/06a-antislop.md` (overwrite if it exists), one line per check. Never write it into `06-critique.md`: `/constructive-self-criticize` overwrites that file. If any line is FAIL, fix only the failing sentences in the source file (keep YAML, FAQ metabox, CTA blocks, and schema in sync), re-run the gate once, and record the result. If it still fails, list the remaining items in the notes for the reviewer instead of looping. Standalone use (no project folder): return the report in the reply.
