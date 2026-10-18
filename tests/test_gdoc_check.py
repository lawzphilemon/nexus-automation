import importlib.util
import pathlib

path = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'gdoc-check.py'
spec = importlib.util.spec_from_file_location('gdoc_check', path)
gdoc_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gdoc_check)

# Pandoc HTML as /export-gdoc uploads it, and the read-back in the format read_file_content returned on 2026-10-18.
source = '''<table><tbody><tr><th scope="row"><strong>Slug</strong></th><td>/id/blog/ctr/</td></tr></tbody></table>
<h1 id="ctr">CTR Adalah</h1>
<p>Oleh <a href="https://www.linkedin.com/in/x">Lawrence</a> &amp; tim.</p>
<h2 id="rumus">Rumus CTR</h2>
<ol type="1"><li>Ambil klik.</li><li>Bagi tayangan.</li></ol>
<h3 id="meta">Meta Ads</h3>
<p>Menurut <a href="https://example.com/a_b">Meta</a>, CTR [all] berbeda.</p>
<pre><code>&lt;div style=&quot;background:#1E1D1C;&quot;&gt;
&lt;a href=&quot;https://example.com/cta&quot;&gt;Konsultasi gratis&lt;/a&gt;
&lt;/div&gt;</code></pre>
<h1 id="faq">FAQ metabox (paste per field)</h1>
<ol type="1"><li><p><strong>CTR itu apa?</strong></p><p>Rasio klik per tayangan.</p></li></ol>
<pre><code>{
  &quot;@context&quot;: &quot;https://schema.org&quot;
}</code></pre>
'''

readback = r'''|  |  |
| :-: | :-: |
| \*\*Slug\*\* | /id/blog/ctr/ |

# **CTR Adalah**

Oleh [Lawrence](https://www.linkedin.com/in/x) &amp; tim.

## **Rumus CTR**

1.  Ambil klik.
2.  Bagi tayangan.

### **Meta Ads**

Menurut [Meta](https://example.com/a\_b), CTR \[all\] berbeda.

\<div style="background:\#1E1D1C;"\>
\<a href="https://example.com/cta"\>Konsultasi gratis\</a\>
\</div\>

# **FAQ metabox (paste per field)**

1.  **CTR itu apa?**

    Rasio klik per tayangan.

{
  "@context": "https://schema.org"
}'''

counts, _ = gdoc_check.source_counts(source)
assert counts == {'h2': 1, 'h3': 1, 'links': 2, 'code blocks': 2, 'words': counts['words']}, counts
rows, problems = gdoc_check.compare(source, readback)
assert problems == [], (rows, problems)
assert dict((name, doc) for name, _, doc in rows)['words'] == counts['words']

# A Doc that lost a heading, a link, the CTA code block, and a paragraph is reported, not passed.
broken = readback.replace('### **Meta Ads**', 'Meta Ads').replace('[Lawrence](https://www.linkedin.com/in/x)', 'Lawrence')
broken = broken.split('\\<div')[0] + broken.split('\\</div\\>')[1]
broken = broken.replace('Menurut [Meta](https://example.com/a\\_b), CTR \\[all\\] berbeda.', '')
_, problems = gdoc_check.compare(source, broken)
assert [p.split()[0] for p in problems] == ['h3', 'links', 'code', 'words'], problems
print('gdoc-check test passed')
