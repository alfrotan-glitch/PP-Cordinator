#!/usr/bin/env python3
"""
EPUB 3 builder - the primary digital edition.

Design notes
------------
* Reflowable, one XHTML document per top-level heading, `dir="rtl"` everywhere
  and `page-progression-direction="rtl"` on the spine.
* Three-level navigation (part -> chapter -> section) in both the navigation
  document and the NCX, plus a reading-order page that also works without CSS.
* Every Latin run is wrapped in `<span xml:lang="en">` so screen readers and
  hyphenation engines treat it correctly; the direction is fixed in the CSS with
  `bdi`/`bdo`-free markup that also holds in readers without CSS.
* Dark mode through a `prefers-color-scheme` block, and higher-contrast colours
  through `prefers-contrast`.
* No images except the cover; tables have header cells; callouts are `<aside>`
  with EPUB structural semantics.
"""
from __future__ import annotations

import html
import re
import uuid
import zipfile
from pathlib import Path

from ebooklib import epub

import mgmtgen
from mgmtgen import ARROW, ROOT, inline_runs, split_documents

OUT = ROOT / 'output' / 'مدیریت_مبانی_و_مهارت‌ها.epub'
FONTS = ROOT / 'assets/fonts'
COVER = ROOT / 'assets/cover.jpg'
COVER_THUMB = ROOT / 'assets/cover.jpg'

LANG = 'fa-AF'
TITLE = 'مدیریت؛ مبانی و مهارت‌های اساسی مدیریت'
SUBTITLE = 'Management: The Essentials — Afghan Dari Professional Edition'
PUBLISHER = 'نشر سرچشمه'
IDENTIFIER = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL,
                                           'sarcheshma/management-essentials/da/1405'))
DATE = '1405 / 2026'
DATE_ISO = '2026-03-21'

CALLOUT_TITLE = {
    'story': 'داستان', 'case': 'کیس کاری', 'decision': 'نقطهٔ تصمیم', 'tool': 'ابزار کار',
    'note': 'نکته', 'reflect': 'تأمل و تمرین', 'warn': 'کجای کار می‌شکند',
    'key': 'درس کلیدی', 'ethics': 'آزمون اخلاقی', 'data': 'ارقام و شواهد',
}
CALLOUT_TYPE = {
    'story': 'sidebar', 'case': 'case-study', 'decision': 'sidebar', 'tool': 'practice',
    'note': 'note', 'reflect': 'practice', 'warn': 'warning', 'key': 'notice',
    'ethics': 'sidebar', 'data': 'sidebar',
}

CSS = """@charset "utf-8";
@font-face { font-family: "DariBook"; font-weight: normal; font-style: normal;
  src: url("../fonts/Vazir.woff2") format("woff2"); }
@font-face { font-family: "DariBook"; font-weight: bold; font-style: normal;
  src: url("../fonts/Samim.woff2") format("woff2"); }
@font-face { font-family: "DariDisplay"; font-weight: normal;
  src: url("../fonts/Samim.woff2") format("woff2"); }
@font-face { font-family: "BookSymbols"; font-weight: normal;
  src: url("../fonts/BookSymbols.woff2") format("woff2"); }

:root {
  --ink: #1b2430; --ink-soft: #3d4653; --paper: #ffffff; --paper-soft: #f6f5f1;
  --rule: #dcdcd4; --accent: #14584f; --accent-soft: #e9f1ef; --navy: #1d3358;
}
html { font-size: 100%; }
body {
  font-family: "DariBook", "BookSymbols", "Vazirmatn", "Noto Naskh Arabic", serif;
  color: var(--ink); background: var(--paper);
  line-height: 1.95; margin: 0 5.2%; padding: 0 0 2em;
  text-align: justify; text-justify: inter-word;
  hyphens: none; -webkit-hyphens: none;
  orphans: 2; widows: 2;
}
p { margin: 0.55em 0; }
h1, h2, h3, h4 { font-family: "DariDisplay", "DariBook", sans-serif; font-weight: bold;
  line-height: 1.5; page-break-after: avoid; break-after: avoid; text-align: right; }
h1 { font-size: 1.6em; color: var(--navy); margin: 0 0 1.1em;
     border-bottom: 2px solid var(--accent); padding-bottom: 0.4em; }
h1.newpage { page-break-before: always; break-before: page; margin-top: 0; }
h2 { font-size: 1.22em; color: var(--accent); margin: 1.7em 0 0.55em; }
h3 { font-size: 1.06em; color: var(--ink-soft); margin: 1.3em 0 0.4em; }
h4 { font-size: 1em; color: var(--navy); margin: 1em 0 0.3em; }
strong { font-weight: bold; }
em { font-style: normal; color: var(--ink-soft); }
ul, ol { margin: 0.5em 1.6em 0.7em 0; padding: 0; }
li { margin: 0.28em 0; }
ul.compact li { margin: 0.15em 0; }
ol.exam { list-style: none; margin-right: 0; }
ol.exam > li { margin: 0.5em 0; font-weight: bold; }
ol.exam ul, ol.exam ol { font-weight: normal; }
blockquote { margin: 0.9em 0; padding: 0.1em 1em 0.1em 0; border-right: 3px solid var(--rule);
             color: var(--ink-soft); }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em;
        page-break-inside: auto; }
table.t-wide { font-size: 0.78em; }
table.t-xwide { font-size: 0.68em; }
th, td { border: 1px solid var(--rule); padding: 0.35em 0.5em; text-align: right;
         vertical-align: top; overflow-wrap: break-word; }
th { background: var(--accent-soft); color: var(--navy); font-weight: bold; }
tr { page-break-inside: avoid; break-inside: avoid; }
thead { display: table-header-group; }
.keytable { font-size: 0.8em; margin-top: 0.6em; }

aside.callout { margin: 1.15em 0; padding: 0.85em 1em 0.9em;
  border: 1px solid var(--rule); border-right: 4px solid var(--accent);
  background: var(--paper-soft); page-break-inside: avoid; break-inside: avoid; }
aside.callout > h4.callout-title { margin: 0 0 0.45em; font-size: 1.02em;
  color: var(--accent); }
aside.case { border-right-color: var(--navy); }
aside.warning { border-right-color: #9a3b2e; }
aside.warning > h4.callout-title { color: #9a3b2e; }
aside.decision { border-right-color: #8a6d1f; }
aside.decision > h4.callout-title { color: #7a6018; }
aside.tool { background: #f4f8f7; }
aside.story > p:first-of-type { font-style: normal; }
p.flow { text-align: center; text-indent: 0; margin: 1.1em 0; font-weight: bold;
         color: var(--accent); font-size: 0.97em; line-height: 2; }
span.q { color: var(--ink-soft); }
.review-item { margin: 0.7em 0; }
.review-item strong { color: var(--navy); }

/* cover */
section.cover { margin: 0; padding: 0; text-align: center; }
section.cover img { max-width: 100%; height: auto; }
figure.cover { margin: 0; padding: 0; }
.toc-page h1 { margin-bottom: 0.8em; }
.toc-page ol { list-style: none; margin: 0; padding: 0; }
.toc-page li { margin: 0.3em 0; line-height: 1.6; }
.toc-page li.lvl1 { font-weight: bold; margin-top: 0.7em; }
.toc-page li.lvl1.part { color: var(--accent); font-size: 1.02em; }
.toc-page li.lvl2 { font-weight: normal; font-size: 0.9em; padding-right: 1.2em; }
.toc-page a { text-decoration: none; color: inherit; }
.colophon { font-size: 0.95em; }
.licence { font-family: monospace; font-size: 0.72em; line-height: 1.5;
  white-space: pre-wrap; word-wrap: break-word; text-align: left; }
dl.glossary { margin: 0; }
dl.glossary dt { font-weight: bold; color: var(--navy); margin-top: 0.6em; }
dl.glossary dd { margin: 0 1em 0 0; }
hr { border: none; border-top: 1px solid var(--rule); margin: 1.6em 0; }

@media (prefers-color-scheme: dark) {
  :root { --ink: #e8e6e1; --ink-soft: #b9bcc4; --paper: #14161a; --paper-soft: #1d2026;
          --rule: #3a3f47; --accent: #6fc2ae; --accent-soft: #1f2a2c; --navy: #cfe0f2; }
  body { background: var(--paper); color: var(--ink); }
  h1 { border-bottom-color: var(--accent); }
  th { background: #1f2a2c; color: var(--navy); }
  aside.warning { border-right-color: #d98a7c; }
  aside.warning > h4.callout-title { color: #d98a7c; }
  aside.decision { border-right-color: #d8bd6a; }
  aside.decision > h4.callout-title { color: #d8bd6a; }
}
@media (prefers-contrast: more) {
  body { color: #000; }
  th, td { border-color: #666; }
}
@media (max-width: 480px) {
  body { margin: 0 4%; line-height: 1.85; }
  table { font-size: 0.82em; }
  h1 { font-size: 1.4em; }
}
"""

LATIN = re.compile(r'[A-Za-z][A-Za-z0-9\.\-\+/#:]*')


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def with_latin(text: str) -> str:
    out, last = [], 0
    for m in LATIN.finditer(text):
        out.append(esc(text[last:m.start()]))
        out.append(f'<span xml:lang="en" lang="en">{esc(m.group(0))}</span>')
        last = m.end()
    out.append(esc(text[last:]))
    return ''.join(out)


def inline(text: str) -> str:
    out = []
    for chunk, bold, ital in inline_runs(text):
        body = with_latin(chunk)
        if bold:
            body = f'<strong>{body}</strong>'
        if ital:
            body = f'<em>{body}</em>'
        out.append(body)
    return ''.join(out)


class Ctx:
    def __init__(self, doc_id: str):
        self.doc_id = doc_id
        self.h1 = 0
        self.h2 = 0
        self.sections = []

    def chapter_anchor(self):
        self.h1 += 1
        return self.doc_id if self.h1 == 1 else f'{self.doc_id}--h{self.h1}'

    def section_anchor(self):
        self.h2 += 1
        return f'{self.doc_id}--s{self.h2}'


def render(blocks, ctx: Ctx, nested=False) -> str:
    out = []
    for b in blocks:
        if b.kind == 'h1':
            anchor = ctx.chapter_anchor()
            cls = ' class="newpage"' if ctx.h1 > 1 else ''
            out.append(f'<h1 id="{anchor}"{cls}>{inline(b.text)}</h1>')
        elif b.kind == 'h2':
            anchor = ctx.section_anchor()
            out.append(f'<h2 id="{anchor}">{inline(b.text)}</h2>')
            if not nested:
                ctx.sections.append((b.text, anchor))
        elif b.kind == 'h3':
            out.append(f'<h3>{inline(b.text)}</h3>')
        elif b.kind == 'h4':
            out.append(f'<h4>{inline(b.text)}</h4>')
        elif b.kind == 'para':
            extra = ''.join(f' {inline(x)}' for x in b.lines)
            out.append(f'<p>{inline(b.text)}{extra}</p>')
        elif b.kind == 'bullet':
            items = ''.join('<li>' + '<br/>'.join(inline(x) for x in i.split('\n')) + '</li>'
                            for i in b.items)
            out.append(f'<ul>{items}</ul>')
        elif b.kind == 'olist':
            items = ''
            for n, i in enumerate(b.items):
                marker = b.markers[n] if n < len(b.markers) else str(n + 1)
                body = '<br/>'.join(inline(x) for x in i.split('\n'))
                items += f'<li value="{esc(marker)}">{body}</li>'
            out.append(f'<ol>{items}</ol>')
        elif b.kind == 'flow':
            steps = b.text.replace('→', ARROW)
            out.append(f'<p class="flow">{"‏" + inline(steps) + "‎"}</p>'
                       .replace('\u200f', '').replace('\u200e', ''))
        elif b.kind == 'quote':
            out.append(f'<blockquote><p>{inline(b.text)}</p></blockquote>')
        elif b.kind == 'table':
            rows = [r for r in b.items if r]
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            cls = ''
            if ncols == 2 and len(rows) == 2 and rows[0][0] == 'پرسش':
                cls = ' class="keytable"'
            elif ncols >= 7:
                cls = ' class="t-xwide"'
            elif ncols >= 5:
                cls = ' class="t-wide"'
            head = ''.join(f'<th scope="col">{inline(c)}</th>' for c in rows[0])
            body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                           for r in rows[1:])
            out.append(f'<table{cls}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
        elif b.kind == 'callout':
            ctype = b.ctype
            label = CALLOUT_TITLE.get(ctype, ctype)
            title = f'{label} — {b.ctitle}' if b.ctitle else label
            etype = CALLOUT_TYPE.get(ctype)
            attrs = f' class="callout {esc(ctype)}"'
            if etype:
                attrs += f' epub:type="{etype}"'
            inner = render(b.items, ctx, nested=True)
            out.append(f'<aside{attrs}><h4 class="callout-title">{inline(title)}</h4>'
                       f'{inner}</aside>')
    return '\n'.join(x for x in out if x)


def doc_shell(title: str, body: str, extra_class: str = '', etype: str = '') -> str:
    section = f'<section epub:type="{etype}" class="{extra_class}">{body}</section>' \
        if etype else (f'<section class="{extra_class}">{body}</section>' if extra_class else body)
    return ('<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"\n'
            f'      xml:lang="{LANG}" lang="{LANG}" dir="rtl">\n'
            f'<head><meta charset="utf-8"/><title>{esc(title)}</title>\n'
            '<link rel="stylesheet" href="style/main.css" type="text/css"/></head>\n'
            f'<body dir="rtl" xml:lang="{LANG}" lang="{LANG}">\n{section}\n</body></html>')


# ------------------------------------------------------------------ documents --

def title_page() -> str:
    body = f'''
<section class="titlepage" epub:type="titlepage" style="text-align:center">
<h1 style="border:none;font-size:2.1em;margin-top:1.4em">{esc(TITLE)}</h1>
<p style="font-size:1.1em;color:#14584f;margin:0.2em 0 1.6em">{esc(SUBTITLE)}</p>
<hr/>
<p style="font-size:1.02em">نسخهٔ دری افغانستان — ویرایش حرفه‌ای</p>
<p style="color:#3d4653">بیست فصل · سی کیس کاری · بستهٔ چهارده‌گانهٔ ابزارها ·
صد و پنجاه پرسش تمرینی · واژه‌نامهٔ کامل اصطلاحات</p>
<p style="margin-top:2.4em;color:#3d4653">{esc(PUBLISHER)} — 1405 / 2026</p>
</section>'''
    return doc_shell('عنوان', body)


def toc_page(entries) -> str:
    items = []
    for e in entries:
        if e['kind'] == 'part':
            items.append(f'<li class="lvl1 part">{esc(e["title"])}</li>')
            continue
        sub = ''
        if e['sections']:
            sub = '<ol>' + ''.join(
                f'<li class="lvl2"><a href="{e["href"]}#{a}">{esc(t)}</a></li>'
                for t, a in e['sections']) + '</ol>'
        items.append(f'<li class="lvl1"><a href="{e["href"]}">{esc(e["title"])}</a>{sub}</li>')
    body = ('<section class="toc-page" epub:type="toc" role="doc-toc"><h1>فهرست مطالب</h1>'
            f'<nav epub:type="toc" id="toc"><ol>{"".join(items)}</ol></nav></section>')
    return doc_shell('فهرست مطالب', body)


def colophon(n_docs: int) -> str:
    body = f'''
<h1>دربارهٔ این نسخهٔ الکترونیکی</h1>
<p class="colophon">این فایل، نسخهٔ <strong>EPUB 3</strong> کتاب «{esc(TITLE)}» است. متن آن با
نسخهٔ چاپی و دیجیتال یکی است؛ تنها صفحه‌آرایی برای صفحه‌های الکترونیکی تنظیم شده است.
برای بازکردن آن می‌توانید از هر خوانندهٔ EPUB (Apple Books، Google Play Books، Calibre،
Thorium یا KOReader) استفاده کنید.</p>
<h2>ساختار و ناوبری</h2>
<ul>
<li>{n_docs} سند محتوایی، با ترتیب راست‌به‌چپ و ناوبری سه‌سطحی (بخش، فصل، عنوان).</li>
<li>فهرست مطالب درونی، فهرست ناوبری کتاب، و نشانه‌های ساختاری برای پرش سریع.</li>
<li>سطوح عنوان‌ها معنایی است (h1 تا h4)، جدول‌ها سرستون دارند و جعبه‌ها با
نشانه‌های ساختاری مشخص شده‌اند.</li>
</ul>
<h2>قلم‌ها</h2>
<p>سه قلم در این فایل جاسازی شده است: <strong>Vazir</strong> برای متن،
<strong>Samim</strong> برای عنوان‌ها و <strong>BookSymbols</strong> برای نشانه‌هایی مانند
فلش و تیک. هر سه با اجازه‌نامهٔ باز منتشر شده‌اند و متن اجازه‌نامه‌ها همراه کتاب است
(<a href="licence.xhtml">licence.xhtml</a>).</p>
<h2>دسترس‌پذیری</h2>
<ul>
<li>متن کامل به‌صورت متن واقعی؛ قابل بزرگ‌نمایی، جست‌وجو و خواندن با صفحه‌خوان.</li>
<li>متن انگلیسی و اصطلاحات لاتین با نشانه‌گذاری زبان، تا درست خوانده شوند.</li>
<li>حالت شبانه (<span xml:lang="en" lang="en">dark mode</span>) با احترام به تنظیمات
خواننده.</li>
<li>تنها تصویر کتاب، جلد آن است و متن جانشین دارد.</li>
</ul>
<h2>مشخصات نشر</h2>
<ul>
<li>شناسه: <span xml:lang="en" lang="en">{IDENTIFIER}</span></li>
<li>ناشر: {esc(PUBLISHER)}</li>
<li>سال: {esc(DATE)}</li>
</ul>
'''
    return doc_shell('دربارهٔ این نسخهٔ الکترونیکی', body, 'colophon', 'colophon')


def licence_page() -> str:
    text = (FONTS / 'LICENSE-fonts.txt').read_text(encoding='utf-8')
    body = ('<h1>اجازه‌نامهٔ قلم‌های جاسازی‌شده</h1>'
            '<p>متن کامل اجازه‌نامه‌های سه قلمی که در این کتاب جاسازی شده‌اند، در زیر آمده '
            'است.</p>'
            f'<pre class="licence" dir="ltr" xml:lang="en" lang="en">{esc(text)}</pre>')
    return doc_shell('اجازه‌نامهٔ قلم‌ها', body)


def cover_page() -> str:
    body = ('<section epub:type="cover" class="cover">'
            '<img src="images/cover.jpg" alt="جلد کتاب مدیریت؛ مبانی و مهارت‌های اساسی '
            'مدیریت" epub:type="cover"/>'
            '</section>')
    return doc_shell('جلد', body)


# ---------------------------------------------------------------------- build --

def main() -> None:
    blocks = mgmtgen.parse(mgmtgen.MASTER)
    book = epub.EpubBook()
    book.set_identifier(IDENTIFIER)
    book.set_title(TITLE)
    book.set_language(LANG)
    book.set_direction('rtl')
    book.add_author(PUBLISHER)
    book.add_metadata('DC', 'publisher', PUBLISHER)
    book.add_metadata('DC', 'date', DATE_ISO)
    book.add_metadata('DC', 'rights', f'© {PUBLISHER}، 1405 / 2026')
    book.add_metadata('DC', 'description',
                      'کتاب مدیریت به زبان دری افغانستان: مبانی، مهارت‌های اساسی، سی کیس '
                      'کاری، بستهٔ ابزارهای عملی، کارگاه تمرین و واژه‌نامهٔ اصطلاحات.')
    for subject in ('مدیریت', 'رهبری', 'تصمیم‌گیری', 'پلان‌گذاری', 'سازمان و مدیریت',
                    'مدیریت منابع بشری', 'افغانستان'):
        book.add_metadata('DC', 'subject', subject)
    for prop, value in (('schema:accessMode', 'textual'),
                        ('schema:accessMode', 'visual'),
                        ('schema:accessModeSufficient', 'textual'),
                        ('schema:accessibilityFeature', 'tableOfContents'),
                        ('schema:accessibilityFeature', 'structuralNavigation'),
                        ('schema:accessibilityFeature', 'readingOrder'),
                        ('schema:accessibilityFeature', 'alternativeText'),
                        ('schema:accessibilityHazard', 'none')):
        book.add_metadata(None, 'meta', value, {'property': prop})
    book.add_metadata(None, 'meta',
                      'متن کامل و قابل جست‌وجو با عنوان‌بندی معنایی، جدول‌های سرستون‌دار، '
                      'ناوبری سه‌سطحی و جلد با متن جانشین. بدون عنصر صوتی یا ویدیویی؛ '
                      'خواندن آن به صفحه‌خوان یا صفحه‌کلید نیازی ندارد.',
                      {'property': 'schema:accessibilitySummary'})

    book.add_item(epub.EpubItem(uid='style', file_name='style/main.css',
                                media_type='text/css', content=CSS))
    for uid, name in (('vazir', 'Vazir.woff2'), ('samim', 'Samim.woff2'),
                      ('symbols', 'BookSymbols.woff2')):
        book.add_item(epub.EpubItem(uid=uid, file_name=f'fonts/{name}',
                                    media_type='font/woff2', content=(FONTS / name).read_bytes()))

    cover_item = epub.EpubItem(uid='cover-image', file_name='images/cover.jpg',
                               media_type='image/jpeg', content=COVER.read_bytes())
    cover_item.properties = ['cover-image']
    book.add_item(cover_item)
    book.add_metadata('OPF', 'meta', '', {'name': 'cover', 'content': 'cover-image'})

    # ---- content documents
    docs = split_documents(blocks)
    entries, items = [], []
    for i, doc in enumerate(docs):
        doc_id = f'doc{i:02d}'
        if doc['kind'] == 'part':
            ctx = Ctx(doc_id)
            entries.append({'title': doc['title'], 'kind': 'part', 'href': f'{doc_id}.xhtml',
                            'sections': []})
            body = render(doc['blocks'], ctx)
            item = epub.EpubHtml(uid=doc_id, file_name=f'{doc_id}.xhtml',
                                 title=doc['title'], lang=LANG)
            item.content = doc_shell(doc['title'], body, 'partpage', 'part')
            book.add_item(item)
            items.append(item)
            continue
        ctx = Ctx(doc_id)
        body = render(doc['blocks'], ctx)
        etype = {'chapter': 'chapter', 'appendix': 'appendix',
                 'frontmatter': 'frontmatter', 'glossary': 'glossary',
                 'backmatter': 'backmatter'}.get(doc['kind'], 'chapter')
        item = epub.EpubHtml(uid=doc_id, file_name=f'{doc_id}.xhtml', title=doc['title'],
                             lang=LANG)
        item.content = doc_shell(doc['title'], body, etype=etype)
        book.add_item(item)
        items.append(item)
        entries.append({'title': doc['title'], 'kind': doc['kind'], 'href': f'{doc_id}.xhtml',
                        'sections': ctx.sections})

    title_it = epub.EpubHtml(uid='titlepage', file_name='titlepage.xhtml',
                             title='عنوان', lang=LANG)
    title_it.content = title_page()
    toc_it = epub.EpubHtml(uid='toc', file_name='toc.xhtml', title='فهرست مطالب', lang=LANG)
    toc_it.content = toc_page(entries)
    cover_it = epub.EpubHtml(uid='cover', file_name='cover.xhtml', title='جلد', lang=LANG)
    cover_it.content = cover_page()
    colo_it = epub.EpubHtml(uid='colophon', file_name='colophon.xhtml',
                            title='دربارهٔ این نسخهٔ الکترونیکی', lang=LANG)
    colo_it.content = colophon(len(items))
    lic_it = epub.EpubHtml(uid='licence', file_name='licence.xhtml',
                           title='اجازه‌نامهٔ قلم‌ها', lang=LANG)
    lic_it.content = licence_page()
    for it in (title_it, toc_it, cover_it, colo_it, lic_it):
        book.add_item(it)

    # ---- navigation: part -> chapter -> section
    def link(e):
        return epub.Link(e['href'], e['title'], e['href'].split('.')[0])

    nav_parts = []
    current = None
    for e in entries:
        if e['kind'] == 'part':
            current = (link(e), [])
            nav_parts.append(current)
            continue
        chapter = link(e)
        children = tuple(epub.Link(f"{e['href']}#{a}", t, f"{e['href'].split('.')[0]}-{k}")
                         for k, (t, a) in enumerate(e['sections'], 1))
        node = (chapter, children) if children else chapter
        if current is None:
            nav_parts.append(node)
        else:
            current[1].append(node)
    def as_node(x):
        return (x[0], tuple(x[1])) if isinstance(x, tuple) else x

    toc_tree = tuple(as_node(x) for x in nav_parts)
    toc_tree = toc_tree + (epub.Link('colophon.xhtml', 'دربارهٔ این نسخهٔ الکترونیکی', 'colo'),)
    book.toc = toc_tree

    book.add_item(epub.EpubNav(title='فهرست مطالب'))
    book.add_item(epub.EpubNcx())

    first_chapter = next((e['href'] for e in entries if e['kind'] == 'chapter'),
                         items[0].file_name)
    book.guide = [
        {'type': 'cover', 'title': 'جلد', 'href': 'cover.xhtml'},
        {'type': 'title-page', 'title': 'عنوان', 'href': 'titlepage.xhtml'},
        {'type': 'toc', 'title': 'فهرست مطالب', 'href': 'toc.xhtml'},
        {'type': 'text', 'title': 'آغاز متن', 'href': first_chapter},
    ]
    book.spine = [cover_it, title_it, toc_it, *items, colo_it, (lic_it, 'no')]

    OUT.parent.mkdir(exist_ok=True)
    epub.write_epub(str(OUT), book,
                    {'epub2_guide': False, 'epub3_landmark': True,
                     'epub3_pages': False, 'landmark_title': 'راهنمای بخش‌ها'})
    fix_package(OUT)
    print(f'EPUB -> {OUT}')
    print(f'  documents: {len(items) + 5} (content {len(items)}) · '
          f'sections in TOC: {sum(len(e["sections"]) for e in entries)} · '
          f'size: {OUT.stat().st_size / 1024:.0f} KB')


def fix_package(path: Path) -> None:
    """ebooklib writes a valid package; we pin the two things readers depend on."""
    tmp = path.with_suffix('.tmp.epub')
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w') as zout:
        names = zin.namelist()
        if names[0] != 'mimetype':
            raise SystemExit('mimetype must be the first entry in the package')
        for it in zin.infolist():
            data = zin.read(it.filename)
            if it.filename.endswith('.opf'):
                s = data.decode('utf-8')
                if 'page-progression-direction' not in s:
                    s = s.replace('<spine', '<spine page-progression-direction="rtl"', 1)
                data = s.encode('utf-8')
            elif it.filename.endswith(('.xhtml', '.html')):
                s = data.decode('utf-8')
                s = re.sub(r'<html(?![^>]*\bdir=)', '<html dir="rtl"', s, count=1)
                s = re.sub(r'<body(?![^>]*\bdir=)', '<body dir="rtl"', s, count=1)
                data = s.encode('utf-8')
            if it.filename == 'mimetype':
                zout.writestr(it, data, zipfile.ZIP_STORED)
            else:
                zout.writestr(it, data, zipfile.ZIP_DEFLATED)
    tmp.replace(path)


if __name__ == '__main__':
    main()
