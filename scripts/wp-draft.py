#!/usr/bin/env python3
"""Send a finished NEXUS article (latest.md) to WordPress as a draft. Never publishes: the status is always "draft".

Usage:
  wp-draft.py <project>/latest.md --site https://example.com [--lang id] [--category slug[,slug]] [--dry-run]

Title = the YAML h1, slug = the last segment of the YAML slug, content = the article body after the H1 up to
"# FAQ metabox" or "# Schema Markup". ```html fences (the /convert CTA blocks) become Custom HTML blocks.
--lang sets the Polylang language. --category takes category slugs, looked up in that language; a slug the site
does not have is printed as a note and the draft keeps the default category.
After the draft exists, the YAML title and meta-description go to the Yoast SEO title and meta description in a
second request; if WordPress refuses that, the draft stays and a note says to paste them by hand.
The "# FAQ metabox" Q/A pairs go to the ACF repeater `faq` (faq_title, faq_content) in a third request, with the
same rule. The JSON-LD is not sent: it stays in the article Doc for a manual paste.
A post that already has this slug (any status) stops the run, so a re-run never creates a duplicate.
Auth: WP_NEXUS_AUTH = base64 of "username:application password" (WordPress Users > Profile > Application Passwords).
Needs Pandoc in PATH. Prints the draft's edit and preview links.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def front_matter(md):
    """Top-level `key: value` pairs of the YAML block /finaldraft writes. Lists (related-keywords, notes) are skipped."""
    m = re.match(r"---\n(.*?)\n---\n", md, flags=re.S)
    if not m:
        sys.exit("latest.md has no YAML front matter")
    meta = {}
    for k, v in re.findall(r"^([\w-]+):[ \t]*(\S.*)$", m[1], flags=re.M):
        meta[k] = json.loads(v) if v.startswith('"') else v  # YAML double-quoted escapes match JSON's
    return meta, md[m.end():]


def article_body(rest):
    """Markdown between the H1 and the FAQ metabox / schema headings, with CTA fences turned into raw HTML blocks."""
    m = re.search(r"^# .+$", rest, flags=re.M)
    if not m:
        sys.exit("latest.md has no H1")
    body = rest[m.end():]
    end = re.search(r"^# (FAQ metabox|Schema Markup)", body, flags=re.M)
    body = body[:end.start()] if end else body
    body = re.sub(r"^\[Paste this block[^\n]*\]\n?", "", body, flags=re.M)  # /convert's note for manual pasting
    return re.sub(r"^```html\n(.*?)^```", r"```{=html}\n<!-- wp:html -->\n\1<!-- /wp:html -->\n```",
                  body, flags=re.M | re.S).strip()


def faq_rows(rest):
    """Q/A pairs of the "# FAQ metabox" block. Accepts `1. **Q?**` + an indented answer paragraph (2.11.0+) and the
    older `1. Q?` with the answer on the next line."""
    m = re.search(r"^# FAQ metabox[^\n]*\n(.*?)(?=^# |\Z)", rest, flags=re.M | re.S)
    rows = []
    for item in re.split(r"^\d+\.[ \t]+", m[1], flags=re.M)[1:] if m else []:
        q, _, a = item.strip().partition("\n")
        # shortcut: field names are gwenchana.digital's ACF repeater; make them flags when another site needs the FAQ
        rows.append({"faq_title": q.strip().strip("*").strip(), "faq_content": " ".join(a.split())})
    return rows


def to_html(markdown):
    pandoc = shutil.which("pandoc")
    if not pandoc:
        sys.exit("Pandoc not found: https://pandoc.org/installing.html")
    return subprocess.run([pandoc, "--from=markdown-smart", "--to=html", "--wrap=none"], input=markdown,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def payload(md, lang=None):
    meta, rest = front_matter(md)
    for key in ("h1", "slug"):
        if not meta.get(key):
            sys.exit(f"latest.md YAML has no {key}")
    data = {"title": meta["h1"], "slug": meta["slug"].strip("/").split("/")[-1],
            "content": to_html(article_body(rest)), "status": "draft"}
    if lang:
        data["lang"] = lang
    seo = {"_yoast_wpseo_title": meta.get("title"), "_yoast_wpseo_metadesc": meta.get("meta-description")}
    data["meta"] = {k: v for k, v in seo.items() if v}
    data["acf"] = {"faq": faq_rows(rest)}
    return data


def api(site, path, auth, data=None, warn=False):
    req = urllib.request.Request(f"{site.rstrip('/')}/wp-json/wp/v2/{path}",
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        msg = f"WordPress said {e.code}: {e.read().decode(errors='replace')[:300]}"
        if warn:
            print(f"warning: {msg}")
            return None
        sys.exit(msg)


def category_ids(site, auth, slugs, lang):
    """IDs for the category slugs in this language (Polylang keeps one term per language). Unknown slugs are notes."""
    ids = []
    for slug in filter(None, (s.strip() for s in slugs.split(","))):
        q = f"categories?slug={urllib.parse.quote(slug)}&_fields=id" + (f"&lang={lang}" if lang else "")
        found = api(site, q, auth)
        if len(found) == 1:
            ids.append(found[0]["id"])
        else:
            print(f"note: category '{slug}' {'not found' if not found else 'is ambiguous'}"
                  f"{f' in {lang}' if lang else ''}; set the category in the editor")
    return ids


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("latest_md")
    p.add_argument("--site", required=True)
    p.add_argument("--lang")
    p.add_argument("--category", help="comma-separated category slugs, looked up in --lang")
    p.add_argument("--dry-run", action="store_true", help="print what would be sent; no network, no auth")
    a = p.parse_args()

    data = payload(Path(a.latest_md).read_text(encoding="utf-8").replace("\r\n", "\n"), a.lang)
    if a.dry_run:
        print(json.dumps({**data, "content": data["content"][:400] + "...", "category slugs": a.category},
                         ensure_ascii=False, indent=2))
        return
    auth = os.environ.get("WP_NEXUS_AUTH")
    if not auth:
        sys.exit("WP_NEXUS_AUTH is not set")
    site = a.site.rstrip("/")

    statuses = "draft,pending,future,private,publish"
    existing = api(site, f"posts?slug={urllib.parse.quote(data['slug'])}&status={statuses}&_fields=id,status", auth)
    if existing:
        sys.exit(f"a post with slug '{data['slug']}' already exists ({existing[0]['status']}): "
                 f"{site}/wp-admin/post.php?post={existing[0]['id']}&action=edit")

    ids = category_ids(site, auth, a.category, a.lang) if a.category else []
    if ids:
        data["categories"] = ids
    seo, faq = data.pop("meta"), data.pop("acf")["faq"]
    post = api(site, "posts", auth, data)
    assert post["status"] == "draft", post["status"]
    print(f"draft {post['id']}")
    if a.lang and post.get("lang") != a.lang:
        print(f"warning: language is '{post.get('lang')}', not '{a.lang}'; set it in the editor")
    # Separate requests after the draft exists: a refused write must not fail the run or block the other one.
    if seo:
        saved = api(site, f"posts/{post['id']}", auth, {"meta": seo}, warn=True) or {}
        if any(saved.get("meta", {}).get(k) != v for k, v in seo.items()):
            print("note: Yoast SEO title / meta description not saved; paste them in the editor")
    if faq:
        saved = api(site, f"posts/{post['id']}", auth, {"acf": {"faq": faq}}, warn=True) or {}
        if len((saved.get("acf") or {}).get("faq") or []) != len(faq):
            print("note: FAQ metabox not saved; paste the Q/A in the editor")
    print(f"edit: {site}/wp-admin/post.php?post={post['id']}&action=edit")
    print(f"preview: {site}/?p={post['id']}&preview=true")


if __name__ == "__main__":
    main()
