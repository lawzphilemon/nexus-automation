---
name: convert-truemission
description: Apply the NEXUS conversion layer using the isolated TrueMission brand profile and Prudential-specific sourcing and compliance rules
allowed-tools: Read, Write, WebFetch, WebSearch
---

# NEX-U-TM — TrueMission Conversion Layer

**Project:** `<project>` is `nexus-output/<CODE>_<slug>/`, where `<CODE>` (`NXS-YYMMDD-XXXX`) is the project code from /research. Use the code from this conversation or given as an argument; if there is none, show `nexus-output/PROJECTS.md` and ask which project. Read and write this project's files only, never the `nexus-output/` root, so parallel sessions never overwrite each other. After saving, update this project's Status in `PROJECTS.md`.

**Dependency:** Requires a finished article draft, ideally NEX-Fn output. If missing: "Paste the final draft, or run /finaldraft first."

Read and follow these files completely:

1. `${CLAUDE_PLUGIN_ROOT}/commands/convert.md`
2. `${CLAUDE_PLUGIN_ROOT}/skills/wa-cta-standard/SKILL.md`
3. `${CLAUDE_PLUGIN_ROOT}/claude-skills/truemission-prudential/SKILL.md`

Apply the general `/convert` workflow with these overrides:

- Use the TrueMission domain and palette from `truemission-prudential`. Ask the user for the WhatsApp CTA destination; it is not stored in the profile.
- Use the profile's Prudential offer-mapping, RIPLAY sourcing, UP calculation, and compliance rules instead of generic `product-upsell`.
- Ask only for the CTA destination, missing article inputs, the applicable product/RIPLAY, requested CTA-message changes, and any credentials intended for publication.
- Let explicit user instructions override profile defaults after confirming the change.

Do not copy this profile into `/convert` or load it for another brand.

Deliver the same file-based output structure as `/convert`, preserving the YAML On-Page SEO Pack fields and final Schema Markup. Do not duplicate the article in chat. End with: "TrueMission conversion done - [N] CTA block(s) inserted in <project>/latest.md. Run /export-gdoc to export this converted version."
