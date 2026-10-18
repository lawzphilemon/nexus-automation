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
meta-description: "CTR adalah persentase tayangan yang diklik."
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

1. Q one?
Answer one,
second line.

2. Q two?
Answer two.

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
assert 'FAQ metabox' not in body and 'Answer one' not in body and 'Schema' not in body and '# CTR' not in body
assert 'Paste this block' not in body

assert wp_draft.faq_rows(rest) == [{'faq_title': 'Q one?', 'faq_content': 'Answer one, second line.'},
                                   {'faq_title': 'Q two?', 'faq_content': 'Answer two.'}]
new_layout = '''# FAQ metabox (paste per field)

1. **Q one?**

   Answer one.

2. **Q two?**

   Answer two.
'''
assert wp_draft.faq_rows(new_layout) == [{'faq_title': 'Q one?', 'faq_content': 'Answer one.'},
                                         {'faq_title': 'Q two?', 'faq_content': 'Answer two.'}]
assert wp_draft.faq_rows('# H1\n\nNo FAQ.\n') == []

calls = []
def fake_api(site, path, auth, data=None, warn=False):
    calls.append(path)
    return [{'id': 110}] if 'slug=digital-marketing' in path else []
wp_draft.api = fake_api
assert wp_draft.category_ids('https://x', 'a', 'digital-marketing, seo,', 'id') == [110]
assert calls == ['categories?slug=digital-marketing&_fields=id&lang=id', 'categories?slug=seo&_fields=id&lang=id']

if shutil.which('pandoc'):
    data = wp_draft.payload(md, 'id')
    assert data['slug'] == 'ctr-adalah' and data['status'] == 'draft' and data['lang'] == 'id'
    assert '<!-- wp:html -->\n<div style="color:#1E1E1E">CTA</div>' in data['content']
    assert '<h2 id="closing">Closing</h2>' in data['content']
    assert len(data['acf']['faq']) == 2
    assert data['meta'] == {'_yoast_wpseo_title': 'CTR Adalah: Rumus',
                            '_yoast_wpseo_metadesc': 'CTR adalah persentase tayangan yang diklik.'}
print('wp-draft test passed')
