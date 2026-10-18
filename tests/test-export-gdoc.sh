#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

cat >"$work_dir/article.md" <<'MARKDOWN'
---
title: "Panduan Contoh"
slug: "/panduan-contoh"
meta-description: "Meta description untuk menguji export Google Docs NEXUS."
faq-delivery: "body"
main-keyword: "panduan contoh"
related-keywords:
  - "contoh artikel"
  - "uji export"
notes:
  - "Ganti <placeholder> & cek sumber"
---

# Panduan Contoh

Paragraf pembuka dengan **teks tebal** dan [tautan](https://example.com).

```html
<div class="cta">CTA tetap menjadi plaintext HTML.</div>
```

# FAQ metabox (paste per field)

1. **Apa itu contoh?**

   Jawaban contoh di paragraf sendiri.

# Schema Markup (JSON-LD)

```json
{"@context": "https://schema.org", "@type": "Article"}
```
MARKDOWN

pandoc "$work_dir/article.md" --from=markdown+yaml_metadata_block+raw_html --to=html --wrap=none --no-highlight \
  --lua-filter="$repo_root/scripts/nexus-gdoc.lua" --output="$work_dir/article.html"

html="$(cat "$work_dir/article.html")"
for expected in "Judul" "Panduan Contoh" "/panduan-contoh" "Meta description untuk"   "Main Keyword" "panduan contoh" "Related Keywords" "contoh artikel, uji export"   "Ganti &lt;placeholder&gt; &amp; cek sumber" '<h1 id="panduan-contoh">' \
  'href="https://example.com"' '<li><p><strong>Apa itu contoh?</strong></p>' '<p>Jawaban contoh di paragraf sendiri.</p></li>' '&lt;div class=&quot;cta&quot;&gt;' "Schema Markup (JSON-LD)"; do
  grep -Fq "$expected" <<<"$html" || { echo "missing: $expected" >&2; exit 1; }
done

if sed '/^slug:/d' "$work_dir/article.md" | pandoc --to=html --lua-filter="$repo_root/scripts/nexus-gdoc.lua" >/dev/null 2>&1; then
  echo "filter must fail when required metadata is missing" >&2
  exit 1
fi
if sed '/^notes:/,/^---$/{/^notes:/d;/^  - /d}' "$work_dir/article.md" | pandoc --to=html --wrap=none --lua-filter="$repo_root/scripts/nexus-gdoc.lua" | grep -Fq "Notes"; then
  echo "Notes row must be skipped when there are no notes" >&2
  exit 1
fi
echo "Google Docs export test passed"
