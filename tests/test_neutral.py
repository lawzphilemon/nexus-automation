"""The shipped plugin stays client-neutral, and the sheet template matches what the queue reads."""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
banned = re.compile(r"gwenchana|truemission|prudential|lawrence", re.I)
hits = [f"{p.relative_to(root)}:{n}" for d in ("commands", "skills", "scripts", "templates")
        for p in (root / d).rglob("*") if p.is_file() and p.suffix != ".pyc"
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if banned.search(line)]
assert not hits, f"client-specific text in the plugin: {hits}"

# No default contact: CTA phone numbers, emails, and addresses are asked every run, never shipped.
contact = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}|wa\.me/\d|tel:\+?\d|(?<![\w-])\+?\d{2,4}[\s-]?\d{3,4}[\s-]?\d{3,5}(?![\w-])", re.I)
contacts = [f"{p.relative_to(root)}:{n}" for d in ("commands", "skills", "templates")
            for p in (root / d).rglob("*") if p.is_file()
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if contact.search(line)]
assert not contacts, f"contact details in the plugin: {contacts}"
# No default brand: no fallback client, WordPress site, or auth variable.
fallbacks = [f"{p.relative_to(root)}:{n}" for d in ("commands", "scripts", "templates")
             for p in (root / d).rglob("*") if p.is_file() and p.suffix != ".pyc"
             for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
             if re.search(r"default_client|wp_site|WP_NEXUS_AUTH", line)]
assert not fallbacks, f"default brand fallbacks in the plugin: {fallbacks}"
convert = (root / "commands" / "convert.md").read_text(encoding="utf-8")
assert "Contact question" in convert and "Contact question first" in (root / "commands" / "queue.md").read_text(encoding="utf-8")

queue = (root / "commands" / "queue.md").read_text(encoding="utf-8")
headers = (root / "templates" / "sheet" / "antrean.tsv").read_text(encoding="utf-8").splitlines()[0].split("\t")
missing = [h for h in headers if h not in queue]
assert not missing, f"sheet headers the queue does not document: {missing}"
assert "Status" in headers and "Client" in headers

statuses = (root / "templates" / "sheet" / "status-values.txt").read_text(encoding="utf-8").split()
assert all(f"`{s}`" in queue for s in statuses), [s for s in statuses if f"`{s}`" not in queue]
print("neutral test passed")
