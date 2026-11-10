# Upstream

- Repo: https://github.com/adhiprib/humanizer-indonesia (MIT, see `LICENSE`)
- Version: 1.7
- Commit: 62fe1aed5932c26cfcfc7ed096415e59aae5b0db
- Vendored: 2026-11-10

Copied verbatim:

| Here | Upstream |
|------|----------|
| `references/upstream-skill.md` | `SKILL.md` (renamed so it is not loaded as a second skill) |
| `references/id-ai-tells.md` | `references/id-ai-tells.md` |
| `scripts/metrik.py` | `scripts/metrik.py` |

Left out: `references/voice-prib-id.md` (the author's own voice preset), `portable/`, README.

`SKILL.md` in this folder is NEXUS's own wrapper (Layer 0 SQEG, register, precedence, self-check). Do not overwrite it when updating.

Update: clone upstream, copy the three files above over the vendored ones, update the version and commit here.
