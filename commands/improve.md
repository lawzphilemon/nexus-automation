---
name: improve
description: Search intent analysis, semantic gap analysis, and E-E-A-T improvement points based on NEX-R findings
allowed-tools: Read, Write
---

# NEX-I — Intent, Semantic Gaps, E-E-A-T

**Mission:** Intent analysis, semantic gaps, E-E-A-T improvement points.

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`. **Client context:** if `<project>/client.txt` names a client, read `clients/<client>/facts.md` and `<project>/context-profile.json` (when the project has one) before writing. Follow the profile's brand voice. `facts.md` wins when the two conflict, and its Defaults answer any input the user has not given. Claim nothing that the user, `facts.md`, or the profile does not support, and never put prices or rate-card data from the profile into the article.

**Dependency:** Requires NEX-R output. Missing → "Please run /research first." If the NEX-R output is not in the conversation, read `<project>/01-research.md`.

1. State the search intent subcategory: Informational / Commercial Investigation / Transactional / Navigational. Identify dominant and secondary intents.
2. Deliver four sections:

**A. Intent coverage**
- What intent do top results satisfy?
- What intent layer is underserved? Specific examples.
- Recommended content angle to win on intent.

**B. Semantic gap analysis**
- List 5–8 specific entity names, concepts, or related terms missing from top results.
- Start the semantic keyword list from the related keywords recommended in the Keyword validation section of `01-research.md`, when it has one.
- List PAA questions not answered by any top result.

**C. SQEG/SQRG compliance**
- Good patterns in top results worth adopting.
- Specific improvement points with examples.
- Flag YMYL category if relevant (health, finance, safety, legal).

**D. E-E-A-T optimization**
- Experience: what first-hand or case-based content is missing?
- Expertise: what depth or technical accuracy gap exists?
- Authoritativeness: what citations, credentials, or named sources are absent?
- Trustworthiness: what dates, disclaimers, or verifiable data are missing?

3. Save the complete stage output to `<project>/02-improve.md` (overwrite if it exists), then deliver it in chat.
4. End: "Run /geo to continue with NEX-G."

## Rules
Every point must reference a specific finding from NEX-R. No generic advice — if a point could apply to any article regardless of the SERP data, rewrite it to be specific or drop it.
