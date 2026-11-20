"""Strip invisible Unicode from text files. Usage: python clean-invisible.py [--check] PATH [PATH...]

PATH is a file or a folder (searched recursively for .md .txt .html .htm .docx).
Removes zero-width chars, BOM, soft hyphen, bidi controls and tag chars; turns
exotic spaces (NBSP, thin, ideographic...) into a plain space.
--check only reports (per file: count by character), changes nothing.
shortcut: ZWJ/ZWNJ are removed too, fine for EN/ID articles, not for emoji sequences or Persian/Indic text.
shortcut: .docx rewrites word/*.xml only, headers/footers included, other parts untouched; fine for articles.
"""
import collections
import os
import re
import shutil
import sys
import tempfile
import zipfile

INVISIBLE = re.compile('[​-‏‪-‮⁠-⁤⁦-⁩­᠎﻿\U000e0000-\U000e007f]')
SPACES = re.compile('[   -   　]')
TEXT_EXT = ('.md', '.txt', '.html', '.htm')


def clean(text):
    text, n = INVISIBLE.subn('', text)
    text, m = SPACES.subn(' ', text)
    return text, n + m


def found(text):
    """Counter of 'U+XXXX' -> occurrences."""
    c = collections.Counter()
    for ch in INVISIBLE.findall(text) + SPACES.findall(text):
        c[f'U+{ord(ch):04X}'] += 1
    return c


def files_under(path):
    if os.path.isfile(path):
        yield path
        return
    for root, _, names in os.walk(path):
        for name in sorted(names):
            if name.lower().endswith(TEXT_EXT + ('.docx',)) and not name.startswith('~$'):
                yield os.path.join(root, name)


def docx_parts(zf):
    return [n for n in zf.namelist() if n.startswith('word/') and n.endswith('.xml')]


def process(path, check):
    """Return Counter of what was found; rewrite the file unless check."""
    if path.lower().endswith('.docx'):
        with zipfile.ZipFile(path) as zf:
            parts = {n: zf.read(n).decode('utf-8') for n in docx_parts(zf)}
        found_here = collections.Counter()
        for text in parts.values():
            found_here += found(text)
        if found_here and not check:
            fd, tmp = tempfile.mkstemp(suffix='.docx', dir=os.path.dirname(path))
            os.close(fd)
            with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as dst:
                for item in src.infolist():
                    data = src.read(item.filename)
                    if item.filename in parts:
                        data = clean(parts[item.filename])[0].encode('utf-8')
                    dst.writestr(item, data)
            shutil.move(tmp, path)
        return found_here
    with open(path, encoding='utf-8', newline='') as f:
        text = f.read()
    found_here = found(text)
    if found_here and not check:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            f.write(clean(text)[0])
    return found_here


if __name__ == '__main__':
    args = sys.argv[1:]
    check = '--check' in args
    paths = [a for a in args if a != '--check']
    if not paths:
        sys.exit(__doc__)
    total_files = dirty_files = total = 0
    for p in paths:
        for path in files_under(p):
            total_files += 1
            try:
                hits = process(path, check)
            except (OSError, ValueError, zipfile.BadZipFile) as e:
                print(f'SKIP {path}: {e}')
                continue
            if hits:
                dirty_files += 1
                total += sum(hits.values())
                print(f'{sum(hits.values()):>5}  {path}  ({", ".join(f"{k}x{v}" for k, v in sorted(hits.items()))})')
    verb = 'found' if check else 'cleaned'
    print(f'{verb} {total} invisible characters in {dirty_files} of {total_files} files')
