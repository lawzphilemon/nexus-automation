#!/usr/bin/env python3
"""Send a finished NEXUS article (latest.md) to WordPress as a draft. Never publishes: the status is always "draft".

Usage:
  wp-draft.py <project>/latest.md --site https://example.com [--lang id] [--dry-run]

Title = the YAML h1, slug = the last segment of the YAML slug, content = the article body after the H1 up to
"# FAQ metabox" or "# Schema Markup". ```html fences (the /convert CTA blocks) become Custom HTML blocks.
--lang sets the Polylang language. The FAQ metabox, Yoast title and meta description, and the JSON-LD are not
sent: they stay in the article Doc for a manual paste.
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
    return re.sub(r"^```html\n(.*?)^```", r"```{=html}\n<!-- wp:html -->\n\1<!-- /wp:html -->\n```",
                  body, flags=re.M | re.S).strip()


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
    return data


def api(site, path, auth, data=None):
    req = urllib.request.Request(f"{site.rstrip('/')}/wp-json/wp/v2/{path}",
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"WordPress said {e.code}: {e.read().decode(errors='replace')[:300]}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("latest_md")
    p.add_argument("--site", required=True)
    p.add_argument("--lang")
    p.add_argument("--dry-run", action="store_true", help="print what would be sent; no network, no auth")
    a = p.parse_args()

    data = payload(Path(a.latest_md).read_text(encoding="utf-8").replace("\r\n", "\n"), a.lang)
    if a.dry_run:
        print(json.dumps({**data, "content": data["content"][:400] + "..."}, ensure_ascii=False, indent=2))
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

    post = api(site, "posts", auth, data)
    assert post["status"] == "draft", post["status"]
    print(f"draft {post['id']}")
    if a.lang and post.get("lang") != a.lang:
        print(f"warning: language is '{post.get('lang')}', not '{a.lang}'; set it in the editor")
    print(f"edit: {site}/wp-admin/post.php?post={post['id']}&action=edit")
    print(f"preview: {site}/?p={post['id']}&preview=true")


if __name__ == "__main__":
    main()
