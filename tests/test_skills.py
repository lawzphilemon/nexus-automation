"""Every skill a command names exists, and the vendored upstream files the wrappers point to are present."""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
skills = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
for name in ("humanizer-id", "humanizer-en", "antislop-copy"):
    assert name in skills, f"missing skill {name}"

named = set()
for p in list((root / "commands").glob("*.md")) + [root / "skills" / "nexus-hermes" / "SKILL.md"]:
    named |= set(re.findall(r"`((?:humanizer-(?:id|en)|antislop-copy|product-upsell|wa-cta-standard))`", p.read_text(encoding="utf-8")))
assert not named - skills, f"commands name skills that do not exist: {named - skills}"

for rel in ("humanizer-id/references/upstream-skill.md", "humanizer-id/references/id-ai-tells.md",
            "humanizer-id/scripts/metrik.py", "humanizer-en/references/upstream-skill.md",
            "antislop-copy/references/copywriting.md", "antislop-copy/references/core-rules.md"):
    assert (root / "skills" / rel).is_file(), f"missing vendored file {rel}"
for d in ("humanizer-id", "humanizer-en", "antislop-copy"):
    assert (root / "skills" / d / "LICENSE").is_file() and (root / "skills" / d / "UPSTREAM.md").is_file(), d

# Upstream SKILL.md files are renamed, so no second skill is loaded from a subfolder.
assert len(list((root / "skills").rglob("SKILL.md"))) == len(skills)

# The wrappers keep the NEXUS layer.
for d in ("humanizer-id", "humanizer-en"):
    text = (root / "skills" / d / "SKILL.md").read_text(encoding="utf-8")
    assert "LAYER 0" in text and "SELF-CHECK" in text and "references/" in text, d
print("ok")
