#!/usr/bin/env python3
"""
EPUB review preview — a browser rendition of the packaged EPUB.

An EPUB cannot be opened in a normal browser tab, so this script unpacks the
built package into project/preview/ and stitches a single page together from
the book's own files (same stylesheet, same embedded fonts, same cover), so the
typography, the tables and the callout boxes can be reviewed without an
e-reader: cover, table of contents, three sample chapters and the colophon.

    python3 project/scripts/preview_epub.py
    python3 -m http.server 8000 --bind 0.0.0.0 --directory project/preview
"""
import html
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output'
DST = ROOT / 'project/preview'
SAMPLES = ['cover.xhtml', 'toc.xhtml', 'ch05.xhtml', 'ch07.xhtml', 'ch12.xhtml',
           'colophon.xhtml']


def body_of(doc: str) -> str:
    m = re.search(r'<body[^>]*>(.*?)</body>', doc, re.S)
    return m.group(1) if m else doc


def clean(fragment: str) -> str:
    fragment = re.sub(r'\s+epub:[a-zA-Z-]+="[^"]*"', '', fragment)
    # single-page preview: links point to their own document
    fragment = re.sub(r'href="ch\d+\.xhtml#([^"]+)"', r'href="#\1"', fragment)
    fragment = re.sub(r'href="ch(\d+)\.xhtml"', r'href="#ch\1"', fragment)
    return fragment


def main() -> None:
    epub = next(OUT.glob('*.epub'))
    if DST.exists():
        shutil.rmtree(DST)
    (DST / 'style').mkdir(parents=True)
    (DST / 'fonts').mkdir()
    (DST / 'images').mkdir()

    parts = []
    with zipfile.ZipFile(epub) as z:
        for name in z.namelist():
            base = name.split('/')[-1]
            if name.endswith('style/main.css'):
                (DST / 'style/main.css').write_bytes(z.read(name))
            elif name.endswith('.woff2'):
                (DST / 'fonts' / base).write_bytes(z.read(name))
            elif name.endswith('cover.png'):
                (DST / 'images' / base).write_bytes(z.read(name))
            elif base in SAMPLES:
                parts.append(clean(body_of(z.read(name).decode('utf-8'))))

        banner = (
            '<div class="preview-banner">'
            f'<strong>پیش‌نمایش مرورگر</strong> — این صفحه از همان فایل‌های '
            f'<span lang="en" xml:lang="en">{html.escape(epub.name)}</span> ساخته شده است '
            '(فونت، استایل، جلد، جدول‌ها و جعبه‌ها). متن کامل کتاب در خود فایل EPUB است؛ '
            'این صفحه فقط جلد، فهرست مطالب، سه فصل نمونه و صفحه پایانی را نشان می‌دهد.'
            '</div>')
        page = (
            '<!DOCTYPE html>\n<html dir="rtl" lang="fa-AF">\n<head>\n'
            '<meta charset="utf-8"/>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
            '<title>پیش‌نمایش نسخه الکترونیکی — قانون زبان</title>\n'
            '<link rel="stylesheet" href="style/main.css" type="text/css"/>\n'
            '<style>\n.preview-banner { position: sticky; top: 0; background: #1F3A5F; '
            'color: #fff; padding: .6em .9em; font-size: .85em; line-height: 1.7; '
            'text-align: right; }\n.preview-wrap { max-width: 44em; margin: 0 auto; '
            'padding: 1.5em 1em 4em; }\n.preview-doc { border-top: 1px dashed #c9d2dc; '
            'margin-top: 2.5em; padding-top: 1em; }\n.preview-label { color: #6b7684; '
            'font-size: .78em; text-align: left; direction: ltr; }\n'
            'body { margin: 0; background: #fff; }\n</style>\n</head>\n<body dir="rtl">\n'
            f'{banner}\n<div class="preview-wrap">\n'
            + '\n'.join(f'<div class="preview-doc">{p}</div>' for p in parts)
            + '\n</div>\n</body>\n</html>\n')
    (DST / 'index.html').write_text(page, encoding='utf-8')
    size = sum(f.stat().st_size for f in DST.rglob('*') if f.is_file())
    print(f'preview -> {DST}/index.html ({size / 1024:.0f} KB, '
          f'{len(parts)} documents from {epub.name})')


if __name__ == '__main__':
    main()
