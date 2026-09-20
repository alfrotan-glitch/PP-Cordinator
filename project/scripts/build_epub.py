#!/usr/bin/env python3
"""
Phase 6 (EPUB 3) - digital edition from the single-source master.

  * one XHTML document per top-level chapter, RTL base direction
  * embedded Vazir (woff2) so the Dari typography travels with the file
  * nav.xhtml + toc.ncx, page-progression-direction="rtl" patched into the OPF
  * callouts, tables and exam questions styled by CSS class
"""
import html
import re
import uuid
from pathlib import Path

from ebooklib import epub

import bookgen
from bookgen import ROOT, inline_runs, parse

OUT_DIR = ROOT / 'output'
OUT = OUT_DIR / 'قانون_زبان_Provincial_Coordinator.epub'
FONTS = ROOT / 'project/assets/fonts'
COVER = ROOT / 'project/assets/cover.png'

CSS = """
@font-face { font-family: 'Vazir'; src: url('../fonts/Vazir.woff2') format('woff2'); font-weight: normal; }
@font-face { font-family: 'Vazir'; src: url('../fonts/Vazir.woff2') format('woff2'); font-weight: bold; }
html { direction: rtl; }
body { font-family: 'Vazir', 'Vazirmatn', 'Noto Naskh Arabic', 'Tahoma', serif;
       direction: rtl; text-align: justify; line-height: 1.85; margin: 5% 6%;
       color: #1a1a1a; }
h1 { font-size: 1.5em; color: #1F3A5F; border-bottom: 3px solid #0F6B5E;
     padding-bottom: 0.35em; margin-top: 1.6em; }
h2 { font-size: 1.18em; color: #0F6B5E; margin-top: 1.4em; }
h3 { font-size: 1.05em; color: #444; margin-top: 1.2em; }
h4 { font-size: 1em; color: #1F3A5F; margin: 1em 0 0.4em; }
p { margin: 0.55em 0; }
ul { margin: 0.4em 1.2em 0.6em 0; padding: 0; }
li { margin: 0.25em 0; }
table { border-collapse: collapse; width: 100%; margin: 0.8em 0; font-size: 0.92em; }
th, td { border: 1px solid #D0D7DE; padding: 0.35em 0.5em; text-align: right;
         vertical-align: top; }
th { background: #E8EEF5; color: #1F3A5F; }
.callout { border: 1px solid #D0D7DE; border-right: 5px solid #1F3A5F;
           padding: 0.7em 0.9em; margin: 0.9em 0; background: #F5F7FA; }
.callout h4 { margin: 0 0 0.4em; }
.callout.concept { background: #E7F3F7; border-right-color: #0E7490; }
.callout.example { background: #F1ECFB; border-right-color: #6D28D9; }
.callout.tip { background: #FDF3E3; border-right-color: #B45309; }
.callout.key { background: #FDECEC; border-right-color: #B91C1C; }
.callout.action { background: #E8F5F1; border-right-color: #0F6B5E; }
.callout.mistake { background: #FDECEC; border-right-color: #B91C1C; }
.callout.scenario { background: #EDF1F7; border-right-color: #1F3A5F; }
.callout.objectives { background: #E8F5F1; border-right-color: #0F6B5E; }
.flow { text-align: center; color: #0F6B5E; }
.cover { text-align: center; }
.cover img { width: 100%; height: auto; }
"""

CALLOUT_TITLE = {
    'concept': 'مفهوم ساده', 'example': 'مثال از دایکندی', 'tip': 'برای امتحان',
    'key': 'حفظ کن', 'action': 'قاعده عملی', 'mistake': 'اشتباه رایج و شکل درست',
    'answer-fa': 'جواب مدل', 'answer-en': 'Sample Answer', 'scenario': 'سناریو',
    'objectives': 'اهداف این فصل',
}


def inline(text, bold_first=False):
    out = []
    for chunk, is_bold in inline_runs(text):
        e = html.escape(chunk)
        out.append(f'<strong>{e}</strong>' if (is_bold or bold_first) else e)
    return ''.join(out)


def blocks_to_html(blocks, level_offset=0):
    out = []
    for b in blocks:
        if b.kind == 'chapter':
            out.append(f'<h1>{inline(b.text)}</h1>')
        elif b.kind == 'section':
            out.append(f'<h2>{inline(b.text)}</h2>')
        elif b.kind == 'subsection':
            out.append(f'<h3>{inline(b.text)}</h3>')
        elif b.kind == 'examq':
            out.append(f'<h4>{inline(b.text)}</h4>')
        elif b.kind == 'para':
            out.append(f'<p>{inline(b.text)}</p>')
        elif b.kind == 'bullet':
            items = ''.join(f'<li>{inline(i)}</li>' for i in b.items)
            out.append(f'<ul>{items}</ul>')
        elif b.kind == 'flow':
            out.append('<p class="flow">↓</p>')
        elif b.kind == 'table':
            rows = b.items
            if not rows:
                continue
            head = ''.join(f'<th>{inline(c)}</th>' for c in rows[0])
            body = ''.join(
                '<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                for r in rows[1:])
            out.append(f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
        elif b.kind == 'callout':
            ctype = b.ctype
            title = b.ctitle or CALLOUT_TITLE.get(ctype, ctype)
            inner = blocks_to_html(b.items, level_offset + 1)
            out.append(f'<div class="callout {html.escape(ctype)}">'
                       f'<h4>{inline(title)}</h4>{inner}</div>')
    return '\n'.join(out)


def split_chapters(blocks):
    """Group blocks into documents at every top-level heading."""
    docs, current = [], None
    for b in blocks:
        if b.kind == 'chapter':
            if current:
                docs.append(current)
            current = {'title': b.text, 'blocks': [b]}
        else:
            if current is None:
                current = {'title': 'سرآغاز', 'blocks': [b]}
            else:
                current['blocks'].append(b)
    if current:
        docs.append(current)
    return docs


def main():
    blocks = parse(bookgen.MASTER)
    book = epub.EpubBook()
    book.set_identifier('shuhada-daikundi-pc-handbook-1405')
    book.set_title('کتاب قانون زبان — راهنمای جامع و عملی Provincial Coordinator')
    book.set_language('fa')
    book.add_author('Shuhada Organization — Daikundi')
    book.add_metadata('DC', 'publisher', 'Shuhada Organization — دفتر ولایتی دایکندی')
    book.add_metadata('DC', 'date', '1405')
    book.add_metadata('DC', 'description',
                      'راهنمای عملی Provincial Coordinator در بخش صحت: ده فصل، سی سناریو، '
                      'سه آزمون آزمایشی، قالب‌های کاری و واژه‌نامه دری–انگلیسی.')
    book.add_metadata('DC', 'rights', 'Shuhada Organization — Daikundi, 1405')

    style = epub.EpubItem(uid='style', file_name='style/main.css',
                          media_type='text/css', content=CSS)
    book.add_item(style)
    font = epub.EpubItem(uid='vazir', file_name='fonts/Vazir.woff2',
                         media_type='font/woff2', content=(FONTS / 'Vazir.woff2').read_bytes())
    book.add_item(font)

    # cover: added manually (image item + XHTML page) so no HTML parsing of the
    # binary image is attempted, and the reading order still starts with it.
    if COVER.exists():
        book.add_item(epub.EpubItem(uid='cover-img', file_name='images/cover.png',
                                    media_type='image/png', content=COVER.read_bytes()))
        cover_page = epub.EpubHtml(title='جلد', file_name='cover.xhtml', lang='fa', uid='cover')
        cover_page.content = ('<html xmlns="http://www.w3.org/1999/xhtml" dir="rtl" lang="fa">'
                              '<head><title>جلد</title>'
                              '<link rel="stylesheet" href="style/main.css" type="text/css"/>'
                              '</head><body dir="rtl" class="cover">'
                              '<div><img src="images/cover.png" alt="جلد کتاب"/></div>'
                              '</body></html>')
        cover_page.add_item(style)
        book.add_item(cover_page)
        book.add_metadata('OPF', 'meta', '', {'name': 'cover', 'content': 'cover-img'})

    spine = ['nav', 'cover']
    docs = split_chapters(blocks)
    for i, doc in enumerate(docs):
        body = blocks_to_html(doc['blocks'])
        item = epub.EpubHtml(title=doc['title'], file_name=f'ch{i:02d}.xhtml', lang='fa',
                             uid=f'ch{i:02d}')
        item.content = (f'<html xmlns="http://www.w3.org/1999/xhtml" dir="rtl" lang="fa">'
                        f'<head><title>{html.escape(doc["title"])}</title>'
                        f'<link rel="stylesheet" href="style/main.css" type="text/css"/>'
                        f'</head><body dir="rtl">{body}</body></html>')
        item.add_item(style)
        book.add_item(item)
        spine.append(item)

    book.toc = [epub.Link(f'ch{i:02d}.xhtml', d['title'], f'ch{i:02d}')
                for i, d in enumerate(docs)]
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    OUT_DIR.mkdir(exist_ok=True)
    epub.write_epub(str(OUT), book)

    # patch page-progression-direction into the OPF (RTL reading order)
    import zipfile
    tmp = OUT.with_suffix('.tmp.epub')
    with zipfile.ZipFile(OUT) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename.endswith('.opf'):
                s = data.decode('utf-8')
                if 'page-progression-direction' not in s:
                    s = s.replace('<spine', '<spine page-progression-direction="rtl"', 1)
                data = s.encode('utf-8')
            elif it.filename.endswith(('.xhtml', '.html')):
                # ebooklib reserialises the documents and drops the dir attribute;
                # put the explicit RTL direction back on <html> and <body>.
                s = data.decode('utf-8')
                s = re.sub(r'<html(?![^>]*\bdir=)', '<html dir="rtl"', s, count=1)
                s = re.sub(r'<body(?![^>]*\bdir=)', '<body dir="rtl"', s, count=1)
                data = s.encode('utf-8')
            zout.writestr(it, data)
    tmp.replace(OUT)
    print('EPUB ->', OUT, f'({len(docs)} documents)')


if __name__ == '__main__':
    main()
