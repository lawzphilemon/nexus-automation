import importlib.util
import pathlib
import shutil
import tempfile

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
assert wp_draft.faq_rows(new_layout, 'q', 'a')[0] == {'q': 'Q one?', 'a': 'Answer one.'}

calls = []
def fake_api(site, path, auth, data=None, warn=False):
    calls.append(path)
    return [{'id': 110}] if 'slug=digital-marketing' in path else []
wp_draft.api = fake_api
assert wp_draft.category_ids('https://x', 'a', 'digital-marketing, seo,', 'id') == [110]
assert calls == ['categories?slug=digital-marketing&_fields=id&lang=id', 'categories?slug=seo&_fields=id&lang=id']

with tempfile.TemporaryDirectory() as tmp:
    project = pathlib.Path(tmp)
    yaml_alt = '---\nh1: "X"\nimage-alt-text-template: "CTR adalah [apa] - [konteks]"\n---\n'
    assert wp_draft.feature_image(project, yaml_alt) == (None, 'CTR adalah apa - konteks')
    (project / 'feature-image-prompt.md').write_text('# Prompt\n\n**Alt text:** Ilustrasi tayangan jadi klik\n',
                                                     encoding='utf-8')
    (project / 'feature-image.webp').write_bytes(b'RIFF\x00\x00\x00\x00WEBP')
    image, alt = wp_draft.feature_image(project, yaml_alt)
    assert image == project / 'feature-image.webp' and alt == 'Ilustrasi tayangan jadi klik'
    (project / 'feature-image-prompt.md').write_text('- Alt text: Older list form\n', encoding='utf-8')
    assert wp_draft.feature_image(project, yaml_alt)[1] == 'Older list form'

    # Drive for desktop folder: the newest file with the article's prefix, only when the project has no image.
    import os
    drive = project / 'drive-image'
    drive.mkdir()
    (drive / 'ACM-IMG-NXS-261018-K7RW.jpg').write_bytes(b'old')
    os.utime(drive / 'ACM-IMG-NXS-261018-K7RW.jpg', (1, 1))
    (drive / 'acm-img-nxs-261018-k7rw-v2.PNG').write_bytes(b'new')
    (drive / 'ACM-IMG-NXS-261018-ZZZZ.png').write_bytes(b'other article')
    (drive / 'ACM-IMG-NXS-261018-K7RW.txt').write_bytes(b'not an image')
    assert wp_draft.feature_image(project, yaml_alt, drive, 'ACM-IMG-NXS-261018-K7RW')[0] == project / 'feature-image.webp'
    (project / 'feature-image.webp').unlink()
    assert wp_draft.feature_image(project, yaml_alt, drive, 'ACM-IMG-NXS-261018-K7RW')[0].name == 'acm-img-nxs-261018-k7rw-v2.PNG'
    assert wp_draft.feature_image(project, yaml_alt, drive, 'ACM-IMG-NXS-261018-NONE')[0] is None
    assert wp_draft.feature_image(project, yaml_alt, project / 'missing', 'ACM-IMG-NXS-261018-K7RW')[0] is None
    (project / 'feature-image.webp').write_bytes(b'RIFF\x00\x00\x00\x00WEBP')
    image = project / 'feature-image.webp'

    calls = []
    def fake_api(site, path, auth, data=None, warn=False, headers=None):
        calls.append((path, data, headers))
        if path == 'media':
            return {'id': 55}
        return {'alt_text': data['alt_text']} if path.startswith('media/') else {'featured_media': data['featured_media']}
    wp_draft.api = fake_api
    post = {'id': 9, 'slug': 'ctr-adalah', 'lang': 'id'}
    assert wp_draft.set_feature_image('https://x', 'a', post, image, 'Alt')
    assert calls[0] == ('media', b'RIFF\x00\x00\x00\x00WEBP',
                        {'Content-Type': 'image/webp', 'Content-Disposition': 'attachment; filename="ctr-adalah.webp"'})
    assert calls[1][:2] == ('media/55', {'alt_text': 'Alt', 'lang': 'id'})
    assert calls[2][:2] == ('posts/9', {'featured_media': 55})

    calls.clear()
    wp_draft.api = lambda *args, **kw: calls.append(args[1]) or None  # upload refused
    assert not wp_draft.set_feature_image('https://x', 'a', post, image, 'Alt') and calls == ['media']

if shutil.which('pandoc'):
    assert 'acf' not in wp_draft.payload(md, 'id')  # no --faq-acf: the FAQ is not sent
    data = wp_draft.payload(md, 'id', 'faq:faq_title:faq_content')
    assert data['slug'] == 'ctr-adalah' and data['status'] == 'draft' and data['lang'] == 'id'
    assert '<!-- wp:html -->\n<div style="color:#1E1E1E">CTA</div>' in data['content']
    assert '<h2 id="closing">Closing</h2>' in data['content']
    assert len(data['acf']['faq']) == 2
    assert data['meta'] == {'_yoast_wpseo_title': 'CTR Adalah: Rumus',
                            '_yoast_wpseo_metadesc': 'CTR adalah persentase tayangan yang diklik.'}
print('wp-draft test passed')
