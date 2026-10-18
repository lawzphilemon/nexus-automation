#!/usr/bin/env python3
"""Send a finished NEXUS article (latest.md) to WordPress as a draft. Never publishes: the status is always "draft".

Usage:
  wp-draft.py <project>/latest.md --site https://example.com [--lang id] [--category slug[,slug]]
              [--faq-acf field:question:answer] [--auth-env NAME] [--dry-run]

Title = the YAML h1, slug = the last segment of the YAML slug, content = the article body after the H1 up to
"# FAQ metabox" or "# Schema Markup". ```html fences (the /convert CTA blocks) become Custom HTML blocks.
--lang sets the Polylang language. --category takes category slugs, looked up in that language; a slug the site
does not have is printed as a note and the draft keeps the default category.
After the draft exists, the YAML title and meta-description go to the Yoast SEO title and meta description in a
second request; if WordPress refuses that, the draft stays and a note says to paste them by hand.
With --faq-acf (for example `faq:faq_title:faq_content`), the "# FAQ metabox" Q/A pairs go to that ACF repeater
and its two sub-fields in a third request, with the same rule; without it the FAQ is not sent. A feature-image.{png,jpg,jpeg,webp} next to latest.md (else the newest --image-prefix file in --image-dir) is uploaded to the media library, gets the
`**Alt text:**` line of feature-image-prompt.md (else the YAML image-alt-text-template without brackets) and the
post's language, and becomes the featured image; same rule again. The JSON-LD is not sent: it stays in the article
Doc for a manual paste.
A post that already has this slug (any status) stops the run, so a re-run never creates a duplicate.
Auth: the environment variable named by --auth-env (default WP_NEXUS_AUTH) = base64 of "username:application
password" (WordPress Users > Profile > Application Passwords). One variable per site.
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


def faq_rows(rest, question="faq_title", answer="faq_content"):
    """Q/A pairs of the "# FAQ metabox" block. Accepts `1. **Q?**` + an indented answer paragraph (2.11.0+) and the
    older `1. Q?` with the answer on the next line."""
    m = re.search(r"^# FAQ metabox[^\n]*\n(.*?)(?=^# |\Z)", rest, flags=re.M | re.S)
    rows = []
    for item in re.split(r"^\d+\.[ \t]+", m[1], flags=re.M)[1:] if m else []:
        q, _, a = item.strip().partition("\n")
        rows.append({question: q.strip().strip("*").strip(), answer: " ".join(a.split())})
    return rows


IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}


def feature_image(project, md, image_dir=None, prefix=None):
    """(image path or None, alt text). The image is <project>/feature-image.*, else the newest file in image_dir
    (a Drive folder synced by Google Drive for desktop) whose name starts with prefix, e.g. ACM-IMG-NXS-261018-K7RW.
    Alt = the `**Alt text:**` line of feature-image-prompt.md, else the YAML image-alt-text-template without brackets."""
    image = next((project / f"feature-image{ext}" for ext in IMAGE_TYPES
                  if (project / f"feature-image{ext}").is_file()), None)
    if image is None and image_dir and prefix and Path(image_dir).is_dir():
        found = [p for p in Path(image_dir).iterdir() if p.is_file() and p.suffix.lower() in IMAGE_TYPES
                 and p.name.lower().startswith(prefix.lower())]
        image = max(found, key=lambda p: p.stat().st_mtime, default=None)
    prompt = project / "feature-image-prompt.md"
    m = re.search(r"^[-*\s]*\**Alt text:\**\s*(\S.*)$",
                  prompt.read_text(encoding="utf-8") if prompt.is_file() else "", flags=re.M | re.I)
    alt = m[1].strip() if m else re.sub(r"[\[\]]", "", front_matter(md)[0].get("image-alt-text-template", ""))
    return image, alt


def set_feature_image(site, auth, post, image, alt):
    """Upload the image, set its alt text (and the post's Polylang language), make it the featured image.
    Returns False at the first step WordPress refuses."""
    ext = image.suffix.lower()
    name = urllib.parse.quote(post.get("slug") or f"post-{post['id']}") + ext
    media = api(site, "media", auth, image.read_bytes(), warn=True,
                headers={"Content-Type": IMAGE_TYPES[ext], "Content-Disposition": f'attachment; filename="{name}"'})
    if not (media or {}).get("id"):
        return False
    # WordPress ignores `lang` on media when Polylang does not translate media, so it can ride along.
    fields = {k: v for k, v in {"alt_text": alt, "lang": post.get("lang")}.items() if v}
    if fields and (api(site, f"media/{media['id']}", auth, fields, warn=True) or {}).get("alt_text") != alt:
        return False
    saved = api(site, f"posts/{post['id']}", auth, {"featured_media": media["id"]}, warn=True) or {}
    return saved.get("featured_media") == media["id"]


def to_html(markdown):
    pandoc = shutil.which("pandoc")
    if not pandoc:
        sys.exit("Pandoc not found: https://pandoc.org/installing.html")
    return subprocess.run([pandoc, "--from=markdown-smart", "--to=html", "--wrap=none"], input=markdown,
                          capture_output=True, text=True, encoding="utf-8", check=True).stdout


def payload(md, lang=None, faq_acf=None):
    """faq_acf = "field:question:answer" names the ACF repeater for the FAQ; None leaves the FAQ out."""
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
    if faq_acf:
        field, question, answer = faq_acf.split(":")
        data["acf"] = {field: faq_rows(rest, question, answer)}
    return data


def api(site, path, auth, data=None, warn=False, headers=None):
    """JSON request; bytes `data` (a media upload) is sent as is, with `headers` overriding the defaults."""
    body = data if isinstance(data, bytes) else json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(f"{site.rstrip('/')}/wp-json/wp/v2/{path}", data=body,
                                 headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json",
                                          **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        msg = f"WordPress said {e.code}: {e.read().decode(errors='replace')[:300]}"
    except OSError as e:  # network error or timeout
        msg = f"request failed: {e}"
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
    p.add_argument("--faq-acf", help="ACF repeater for the FAQ as field:question:answer, e.g. faq:faq_title:faq_content")
    p.add_argument("--image-dir", help="local folder of synced Drive images (Google Drive for desktop)")
    p.add_argument("--image-prefix", help="file name prefix of this article's image, e.g. ACM-IMG-NXS-261018-K7RW")
    p.add_argument("--auth-env", default="WP_NEXUS_AUTH", help="environment variable that holds the auth")
    p.add_argument("--dry-run", action="store_true", help="print what would be sent; no network, no auth")
    a = p.parse_args()

    md = Path(a.latest_md).read_text(encoding="utf-8").replace("\r\n", "\n")
    data = payload(md, a.lang, a.faq_acf)
    project = Path(a.latest_md).parent
    image, alt = feature_image(project, md, a.image_dir, a.image_prefix)
    if a.dry_run:
        print(json.dumps({**data, "content": data["content"][:400] + "...", "category slugs": a.category,
                          "feature image": str(image) if image else None, "alt text": alt},
                         ensure_ascii=False, indent=2))
        return
    auth = os.environ.get(a.auth_env)
    if not auth:
        sys.exit(f"{a.auth_env} is not set")
    site = a.site.rstrip("/")

    statuses = "draft,pending,future,private,publish"
    existing = api(site, f"posts?slug={urllib.parse.quote(data['slug'])}&status={statuses}&_fields=id,status", auth)
    if existing:
        sys.exit(f"a post with slug '{data['slug']}' already exists ({existing[0]['status']}): "
                 f"{site}/wp-admin/post.php?post={existing[0]['id']}&action=edit")

    ids = category_ids(site, auth, a.category, a.lang) if a.category else []
    if ids:
        data["categories"] = ids
    seo, acf = data.pop("meta"), data.pop("acf", None)
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
    field, faq = next(iter(acf.items())) if acf else (None, [])
    if faq:
        saved = api(site, f"posts/{post['id']}", auth, {"acf": acf}, warn=True) or {}
        if len((saved.get("acf") or {}).get(field) or []) != len(faq):
            print("note: FAQ metabox not saved; paste the Q/A in the editor")
    if not image:
        where = f"{a.image_prefix}.png in {a.image_dir}" if a.image_dir and a.image_prefix else project / "feature-image.png"
        print(f"note: no feature image; save it as {where} and add it in the editor")
    elif set_feature_image(site, auth, post, image, alt):
        print(f"feature image set: {image.name}")
    else:
        print(f"note: feature image not set; add {image} in the editor (alt text: {alt})")
    print(f"edit: {site}/wp-admin/post.php?post={post['id']}&action=edit")
    print(f"preview: {site}/?p={post['id']}&preview=true")


if __name__ == "__main__":
    main()
