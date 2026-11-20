import importlib.util
import pathlib
import tempfile
import zipfile

path = pathlib.Path(__file__).resolve().parent.parent / 'scripts' / 'clean-invisible.py'
spec = importlib.util.spec_from_file_location('clean_invisible', path)
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)

dirty = 'a​b﻿c­ d‮e\U000e0041f g　h'
text, count = ci.clean(dirty)
assert text == 'abc def g h', repr(text)
assert count == 7, count

plain = 'Teks biasa, "kutipan", é, 日本語.\n'
assert ci.clean(plain) == (plain, 0)

with tempfile.TemporaryDirectory() as d:
    d = pathlib.Path(d)
    (d / 'a.md').write_text('x​y', encoding='utf-8')
    docx = d / 'b.docx'
    with zipfile.ZipFile(docx, 'w') as z:
        z.writestr('word/document.xml', '<w:t>x​y</w:t>')
        z.writestr('docProps/core.xml', 'keep​')
    # check mode reports and changes nothing
    assert ci.process(str(d / 'a.md'), True) == {'U+200B': 1}
    assert (d / 'a.md').read_text(encoding='utf-8') == 'x​y'
    assert ci.process(str(docx), True) == {'U+200B': 1}
    # clean mode rewrites
    ci.process(str(d / 'a.md'), False)
    ci.process(str(docx), False)
    assert (d / 'a.md').read_text(encoding='utf-8') == 'xy'
    with zipfile.ZipFile(docx) as z:
        assert z.read('word/document.xml').decode() == '<w:t>xy</w:t>'
        assert z.read('docProps/core.xml').decode() == 'keep​'
    assert sorted(pathlib.Path(p).name for p in ci.files_under(str(d))) == ['a.md', 'b.docx']
print('ok')
