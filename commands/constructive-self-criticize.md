---
name: constructive-self-criticize
description: Critique a finished NEXUS article the way its reader, the brand owner, and a senior editor would, rank concrete fixes, then apply the approved ones without adding new claims
argument-hint: "[project code or article.md]"
allowed-tools: Read, Write, Edit
---

# NEX-C — Constructive Self-Critique

**Mission:** Catch what the stage checklists miss, such as a confusing point of view, contradictions, weak answers, or claims the brand cannot back, before the article goes to `/convert` or the client. Every finding comes with a fix.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Context profile:** if `<project>/context-profile.json` exists, read it before writing and follow its brand voice, facts, and services. Never put prices or rate-card data from it into the article.

**Source:** `<project>/latest.md`, else `<project>/05-firstdraft.md`. An `.md` path given as an argument or text pasted in chat also works, without a project. Read the outline header (`FAQ delivery`, `CTAs`, `Voice`), `02-improve.md`, and `03-geo.md` when they exist; they are the yardstick.

## Step 1 — Read it three times, as three people

1. **The target reader** (from the NEX-I intent): Is the question in the H1 answered early and fully? Where would they get lost, bored, or doubt the text? Who is speaking to them, and is that consistent from start to finish?
2. **The brand owner:** Does the article speak in the confirmed `Voice` (in `brand` voice, the brand is "we"/"kami" and never described from outside)? Does it claim services, results, numbers, clients, or credentials the brand has not confirmed? Is anything off-brand, off-scope, or a price the brand does not publish?
3. **A senior editor (SEO/GEO):** Do numbers, names, dates, and terms contradict each other between sections, the FAQ, the SEO pack, and the schema? Is any stat unsourced or stale? Does each H2 open with an answer that stands alone? Is anything repeated, padded, or missing compared with the NEX-G fan-out?

## Step 2 — Report

Save to `<project>/06-critique.md` (overwrite if it exists) and show it in chat:

```text
Verdict: [ready / ready after must-fix items / needs another draft] — [one sentence]
What works: [at most 3 short points worth keeping]

| # | Severity | Where (heading + short quote) | Problem | Why it matters | Fix (exact rewrite or action) |
|---|---|---|---|---|---|
```

- Severity: `must fix` (wrong, unsupported, contradictory, or wrong voice), `should fix` (weakens the answer or trust), `nice to have`.
- At most 10 findings, most severe first. Quote at most 15 words per finding.
- Every fix is concrete: the rewritten sentence, the line to cut, or the source to add. "Make it clearer" is not a fix.
- If nothing is wrong, say so. Never invent problems to fill the table.

End: "Reply with the numbers to apply (or 'all'), or 'skip'."

## Step 3 — Apply

Apply only the approved findings, in the source file, without changing anything else. Keep the YAML, the FAQ metabox block, and the schema intact, and keep the schema in sync when a fix changes text it repeats (for example a FAQ answer). Run the matching humanizer (`humanizer-en` or `humanizer-id`) on changed paragraphs only. Mark each applied row `applied` in `06-critique.md`.

End: "Critique applied to [file]. Run /convert or /export-gdoc next."

## Rules

- No new facts, numbers, sources, or claims in fixes. Use only what is already in the article or the project files; if a fix needs evidence that is missing, the fix is to remove or soften the claim, or to ask the user.
- Do not restructure the GEO layout (Direct Answer Block, FAQ, Definition Boxes) or change the primary keyword placement unless that is the finding.
- Never use em dashes in the article.
