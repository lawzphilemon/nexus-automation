"""The shipped plugin stays client-neutral, and the sheet template matches what the queue reads."""
import pathlib
import re

root = pathlib.Path(__file__).resolve().parent.parent
banned = re.compile(r"gwenchana|truemission|prudential|lawrence", re.I)
hits = [f"{p.relative_to(root)}:{n}" for d in ("commands", "skills", "scripts", "templates")
        for p in (root / d).rglob("*") if p.is_file() and p.suffix != ".pyc"
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if banned.search(line)]
assert not hits, f"client-specific text in the plugin: {hits}"

queue = (root / "commands" / "queue.md").read_text(encoding="utf-8")
headers = (root / "templates" / "sheet" / "antrean.tsv").read_text(encoding="utf-8").splitlines()[0].split("\t")
missing = [h for h in headers if h not in queue]
assert not missing, f"sheet headers the queue does not document: {missing}"
assert "Status" in headers and "Client" in headers

statuses = (root / "templates" / "sheet" / "status-values.txt").read_text(encoding="utf-8").split()
assert all(f"`{s}`" in queue for s in statuses), [s for s in statuses if f"`{s}`" not in queue]
print("neutral test passed")
