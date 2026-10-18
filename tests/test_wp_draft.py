import importlib.util
import pathlib
import shutil

path = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'wp-draft.py'
spec = importlib.util.spec_from_file_location('wp_draft', path)
wp_draft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wp_draft)

md = '''---
title: "CTR Adalah: Rumus"
slug: "/id/blog/ctr-adalah/"
h1: "CTR Adalah: Rumus, \\"Cara\\" Hitung"
related-keywords:
  - "rumus ctr"
---

# CTR Adalah: Rumus, "Cara" Hitung

Intro paragraph.

```html
<div style="color:#1E1E1E">CTA</div>
```

[Paste this block in WordPress Classic Editor → Text tab. Do not switch to Visual tab after pasting.]

## Closing

# FAQ metabox (paste per field)

1. **Q?**

   Answer stays out of the post.

# Schema Markup (JSON-LD)

```json
{}
```
'''

meta, rest = wp_draft.front_matter(md)
assert meta['h1'] == 'CTR Adalah: Rumus, "Cara" Hitung'
assert meta['slug'] == '/id/blog/ctr-adalah/'
assert 'related-keywords' not in meta

body = wp_draft.article_body(rest)
assert body.startswith('Intro paragraph.')
assert '```{=html}\n<!-- wp:html -->\n<div style="color:#1E1E1E">CTA</div>\n<!-- /wp:html -->\n```' in body
assert 'FAQ metabox' not in body and 'Answer stays' not in body and 'Schema' not in body and '# CTR' not in body
assert 'Paste this block' not in body

if shutil.which('pandoc'):
    data = wp_draft.payload(md, 'id')
    assert data['slug'] == 'ctr-adalah' and data['status'] == 'draft' and data['lang'] == 'id'
    assert '<!-- wp:html -->\n<div style="color:#1E1E1E">CTA</div>' in data['content']
    assert '<h2 id="closing">Closing</h2>' in data['content']
print('wp-draft test passed')
