"""Read-back check for Google Doc exports. Usage:
  python gdoc-check.py SOURCE.html             counts for the Pandoc HTML that was uploaded
  python gdoc-check.py READBACK.md             counts for the Drive read_file_content text, saved as-is
  python gdoc-check.py SOURCE.html READBACK.md compare; exit 1 and list the differences on a mismatch

Counts: H2 and H3 headings, links (real hyperlinks), code blocks, and words. The Doc read-back is
Markdown-like: headings as #, links as [text](url), code blocks as plain escaped paragraphs, so a code
block counts as found when its first substantial line appears in the read-back.
"""
import collections
import html
import html.parser
import re
import sys

WORD_TOLERANCE = 0.02  # list numbers and table syntax shift the read-back word count by well under 2%


def words(text):
    return len(re.findall(r"[^\W_]+", text))


def squash(text):
    return re.sub(r"\s+", "", text.replace("\\", ""))


def signature(code):
    """First line with at least 8 visible characters, squashed, so it can be found in the read-back."""
    lines = [squash(line) for line in code.splitlines()]
    return next((line for line in lines if len(line) >= 8), "".join(lines))


class _Source(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.counts = collections.Counter()
        self.text, self.code, self.in_pre = [], [], False

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3"):
            self.counts[tag] += 1
        elif tag == "a" and dict(attrs).get("href"):
            self.counts["links"] += 1
        elif tag == "pre":
            self.in_pre = True
            self.code.append("")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
        elif tag in ("p", "li", "td", "th", "br", "h1", "h2", "h3", "h4", "tr"):
            self.text.append(" ")  # block ends separate words, as they do in the Doc

    def handle_data(self, data):
        self.text.append(data)
        if self.in_pre:
            self.code[-1] += data


def source_counts(markup):
    parser = _Source()
    parser.feed(markup)
    parser.close()
    return {"h2": parser.counts["h2"], "h3": parser.counts["h3"], "links": parser.counts["links"],
            "code blocks": len(parser.code), "words": words("".join(parser.text))}, [signature(c) for c in parser.code]


LINK = re.compile(r"(?<!\\)\[((?:[^\]\\]|\\.)*)\]\([^)\s]+\)")


def readback_counts(text):
    text = html.unescape(text)
    prose = LINK.sub(r"\1", text)  # the URL of a hyperlink is not visible text
    prose = re.sub(r"^\s*(?:\d+\.|[-*+])\s+", "", prose, flags=re.M)  # list markers
    return {"h2": len(re.findall(r"^## ", text, flags=re.M)), "h3": len(re.findall(r"^### ", text, flags=re.M)),
            "links": len(LINK.findall(text)), "words": words(prose.replace("\\", " "))}


def compare(markup, text):
    """Return (rows, problems). rows: (name, source, doc); problems: human-readable mismatches."""
    src, signatures = source_counts(markup)
    doc = readback_counts(text)
    haystack = squash(html.unescape(text))
    wanted = collections.Counter(signatures)
    doc["code blocks"] = sum(min(n, haystack.count(sig)) for sig, n in wanted.items())
    rows = [(name, src[name], doc[name]) for name in src]
    problems = []
    for name, a, b in rows:
        if name == "words":
            if a and abs(b - a) / a > WORD_TOLERANCE:
                problems.append(f"words {a} -> {b} ({(b - a) / a:+.1%}, tolerance {WORD_TOLERANCE:.0%})")
        elif a != b:
            problems.append(f"{name} {a} -> {b}")
    return rows, problems


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


if __name__ == "__main__":
    paths = sys.argv[1:]
    if len(paths) == 1:
        content = _read(paths[0])
        counts = source_counts(content)[0] if paths[0].lower().endswith((".html", ".htm")) else readback_counts(content)
        for name, value in counts.items():
            print(f"{name:12} {value}")
    elif len(paths) == 2:
        rows, problems = compare(_read(paths[0]), _read(paths[1]))
        print(f"{'':12} {'source':>7} {'doc':>7}")
        for name, a, b in rows:
            print(f"{name:12} {a:>7} {b:>7}")
        print("MISMATCH: " + "; ".join(problems) if problems else "OK")
        sys.exit(1 if problems else 0)
    else:
        sys.exit(__doc__)
