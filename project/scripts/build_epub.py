#!/usr/bin/env python3
"""
Phase 6 (EPUB 3.3) - the digital edition, built from the single-source master.

What this build does beyond a plain export:

  * one XHTML document per top-level heading, semantic `epub:type` on each
    (frontmatter / chapter / appendix / backmatter / colophon)
  * real in-book navigation: a visible table of contents page **and** a nav
    document / NCX with two levels (chapter -> section, both linked to anchors)
  * landmarks (cover, toc, start of text) for reading systems' menus
  * cover page built as SVG so it scales on any screen, with the cover image
    declared as `cover-image` in the manifest
  * embedded Dari fonts: Vazir for text, Samim as the bold face (same pairing
    as the print edition) plus a small symbol subset for check marks/stars,
    with the licence notices inside the package
  * accessibility metadata (EPUB Accessibility 1.1) and accessible markup:
    real tables with header cells, aside callouts, alt text, Latin runs
    tagged `lang="en"`, RTL declared on every document
  * a colophon page describing this electronic edition, and passthrough of the
    text-2-speech friendly structure (no images except the cover)
"""
import html
import re
import uuid
import zipfile
from pathlib import Path

from ebooklib import epub

import bookgen
from bookgen import ROOT, inline_runs, parse

OUT_DIR = ROOT / 'output'
OUT = OUT_DIR / 'قانون_زبان_Provincial_Coordinator.epub'
ASSETS = ROOT / 'project/assets'
FONTS = ASSETS / 'fonts'
COVER = ASSETS / 'cover.png'

LANG = 'fa-AF'
TITLE = 'کتاب قانون زبان — راهنمای جامع و عملی Provincial Coordinator'
SUBTITLE = 'در بخش صحت — با سناریوهای واقعی، تمرین و جواب مدل'
IDENTIFIER = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL,
                                           'shuhada-daikundi/pc-handbook/1405'))
ORGANISATION = 'Shuhada Organization — Daikundi'

CALLOUT_TITLE = {
    'concept': 'مفهوم ساده', 'example': 'مثال از دایکندی', 'tip': 'برای امتحان',
    'key': 'حفظ کن', 'action': 'قاعده عملی', 'mistake': 'اشتباه رایج و شکل درست',
    'answer-fa': 'جواب مدل', 'answer-en': 'Sample Answer', 'scenario': 'سناریو',
    'objectives': 'اهداف این فصل',
}

# EPUB structural semantics for the callout boxes (values from the EPUB SSV)
CALLOUT_EPUB_TYPE = {
    'objectives': 'learning-objectives',
    'example': 'sidebar',
    'scenario': 'sidebar',
    'concept': 'sidebar',
    'answer-fa': 'answer',
    'answer-en': 'answer',
    'key': 'notice',
    'tip': 'tip',
    'action': 'practice',
    'mistake': 'warning',
}

CSS = """
@font-face { font-family: 'DariBook'; font-weight: normal; font-style: normal;
             src: url('../fonts/Vazir.woff2') format('woff2'); }
@font-face { font-family: 'DariBook'; font-weight: bold; font-style: normal;
             src: url('../fonts/Samim.woff2') format('woff2'); }
@font-face { font-family: 'DariSymbols'; font-weight: normal; font-style: normal;
             src: url('../fonts/BookSymbols.woff2') format('woff2'); }

body { font-family: 'DariBook', 'DariSymbols', 'Vazirmatn', 'Noto Naskh Arabic', Tahoma, serif;
       text-align: justify; line-height: 1.85; margin: 0 5%; color: #1a1a1a;
       -webkit-hyphens: none; hyphens: none; }
p { margin: 0.6em 0; orphans: 2; widows: 2; }
h1, h2, h3, h4 { font-weight: bold; line-height: 1.45; page-break-after: avoid; }
h1 { font-size: 1.45em; color: #1F3A5F; border-bottom: 3px solid #0F6B5E;
     padding-bottom: 0.35em; margin: 1.2em 0 0.8em; }
h1.newpage { page-break-before: always; }
h2 { font-size: 1.18em; color: #0F6B5E; margin: 1.5em 0 0.5em; }
h3 { font-size: 1.05em; color: #3d3d3d; margin: 1.2em 0 0.4em; }
h4 { font-size: 1em; color: #1F3A5F; margin: 1em 0 0.35em; }
strong { font-weight: bold; }
ul { margin: 0.5em 1.4em 0.7em 0; padding: 0; }
li { margin: 0.3em 0; }
table { border-collapse: collapse; width: 100%; margin: 0.9em 0; font-size: 0.9em; }
table.t-wide { font-size: 0.78em; }
th, td { border: 1px solid #D0D7DE; padding: 0.35em 0.45em; text-align: right;
         vertical-align: top; overflow-wrap: break-word; }
th { background: #E8EEF5; color: #1F3A5F; font-weight: bold; }
tr { page-break-inside: avoid; }
.callout { border: 1px solid #D0D7DE; border-right: 5px solid #1F3A5F;
           padding: 0.7em 0.9em; margin: 1em 0; background: #F5F7FA;
           page-break-inside: avoid; }
.callout h4 { margin: 0 0 0.4em; }
.callout.concept { background: #E7F3F7; border-right-color: #0E7490; }
.callout.example { background: #F1ECFB; border-right-color: #6D28D9; }
.callout.tip { background: #FDF3E3; border-right-color: #B45309; }
.callout.key { background: #FDECEC; border-right-color: #B91C1C; }
.callout.action { background: #E8F5F1; border-right-color: #0F6B5E; }
.callout.mistake { background: #FDECEC; border-right-color: #B91C1C; }
.callout.scenario { background: #EDF1F7; border-right-color: #1F3A5F; }
.callout.objectives { background: #E8F5F1; border-right-color: #0F6B5E; }
.flow { text-align: center; margin: 0.5em 0; }
.flow::before { content: ""; display: inline-block; width: 0; height: 0;
                border-left: 0.45em solid transparent;
                border-right: 0.45em solid transparent;
                border-top: 0.75em solid #0F6B5E; }
.cover { margin: 0; padding: 0; text-align: center; }
.cover svg { width: 100%; height: auto; }
.toc-page { page-break-after: always; }
.toc-page ol { list-style: none; margin: 0.4em 0; padding: 0 1em 0 0; }
.toc-page li { margin: 0.35em 0; }
.toc-page .lvl1 { font-weight: bold; }
.toc-page .lvl2 { font-size: 0.92em; }
.toc-page a { text-decoration: none; color: #1F3A5F; }
.colophon { font-size: 0.95em; }
.colophon h2 { font-size: 1.05em; }
pre.licence { font-family: monospace; font-size: 0.75em; line-height: 1.5;
              white-space: pre-wrap; word-wrap: break-word; }
"""

# ---------------------------------------------------------------- inline ----

LATIN = re.compile(r'[A-Za-z][A-Za-z0-9]*')


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def tag_latin(text: str) -> str:
    """Wrap Latin runs in lang="en" so screen readers switch voice."""
    out, last = [], 0
    for m in LATIN.finditer(text):
        out.append(esc(text[last:m.start()]))
        out.append(f'<span xml:lang="en" lang="en">{esc(m.group(0))}</span>')
        last = m.end()
    out.append(esc(text[last:]))
    return ''.join(out)


def inline(text: str, bold_first: bool = False) -> str:
    out = []
    for chunk, is_bold in inline_runs(text):
        body = tag_latin(chunk)
        out.append(f'<strong>{body}</strong>' if (is_bold or bold_first) else body)
    return ''.join(out)


# -------------------------------------------------------------- renderer ----

class Context:
    """Per-document state: anchor counters and the collected TOC entries."""

    def __init__(self, doc_id: str):
        self.doc_id = doc_id
        self.h1 = 0
        self.h2 = 0
        self.sections = []          # [(title, anchor)] - level-2 nav entries

    def chapter_anchor(self) -> str:
        self.h1 += 1
        return self.doc_id if self.h1 == 1 else f'{self.doc_id}-h{self.h1}'

    def section_anchor(self) -> str:
        self.h2 += 1
        return f'{self.doc_id}-s{self.h2}'


def render_blocks(blocks, ctx: Context, nested: bool = False) -> str:
    out = []
    for b in blocks:
        if b.kind == 'chapter':
            anchor = ctx.chapter_anchor()
            cls = ' class="newpage"' if ctx.h1 > 1 else ''
            out.append(f'<h1 id="{anchor}"{cls}>{inline(b.text)}</h1>')
        elif b.kind == 'section':
            anchor = ctx.section_anchor()
            out.append(f'<h2 id="{anchor}">{inline(b.text)}</h2>')
            if not nested:
                ctx.sections.append((b.text, anchor))
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
            out.append('<p class="flow"></p>')
        elif b.kind == 'table':
            rows = [r for r in b.items if r]
            if not rows:
                continue
            width = max(len(r) for r in rows)
            cls = ' class="t-wide"' if width >= 5 else ''
            head = ''.join(f'<th scope="col">{inline(c)}</th>' for c in rows[0])
            body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                           for r in rows[1:])
            out.append(f'<table{cls}><thead><tr>{head}</tr></thead>'
                       f'<tbody>{body}</tbody></table>')
        elif b.kind == 'callout':
            ctype = b.ctype
            title = b.ctitle or CALLOUT_TITLE.get(ctype, ctype)
            etype = CALLOUT_EPUB_TYPE.get(ctype)
            attrs = f' class="callout {esc(ctype)}"'
            if etype:
                attrs += f' epub:type="{etype}"'
            inner = render_blocks(b.items, ctx, nested=True)
            out.append(f'<aside{attrs}><h4 class="callout-title">{inline(title)}</h4>'
                       f'{inner}</aside>')
    return '\n'.join(x for x in out if x)


def split_documents(blocks):
    """Group blocks at every top-level heading (one XHTML file per group)."""
    docs, current = [], None
    for b in blocks:
        if b.kind == 'chapter':
            if current:
                docs.append(current)
            current = {'title': b.text, 'blocks': [b]}
        elif current is None:
            current = {'title': 'سرآغاز', 'blocks': [b]}
        else:
            current['blocks'].append(b)
    if current:
        docs.append(current)
    return docs


def doc_type(title: str, index: int, total: int) -> str:
    if title.startswith('فصل '):
        return 'chapter'
    if title.startswith('پیوست ۱'):
        return 'appendix glossary'
    if title.startswith('پیوست '):
        return 'appendix'
    if title.startswith('درباره این نسخه'):
        return 'backmatter'
    return 'frontmatter'


def html_doc(title: str, body: str, etype: str = '') -> str:
    section = (f'<section epub:type="{etype}">{body}</section>') if etype else body
    return (f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
            f'xml:lang="{LANG}" lang="{LANG}" dir="rtl">'
            f'<head><title>{esc(title)}</title>'
            f'<link rel="stylesheet" href="style/main.css" type="text/css"/></head>'
            f'<body dir="rtl">{section}</body></html>')


def cover_doc() -> str:
    body = ('<section epub:type="cover" class="cover">'
            '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'version="1.1" viewBox="0 0 1600 2400" preserveAspectRatio="xMidYMid meet" '
            'role="img" aria-label="جلد کتاب قانون زبان — راهنمای جامع و عملی Provincial Coordinator">'
            '<image width="1600" height="2400" xlink:href="images/cover.png"/>'
            '</svg></section>')
    return html_doc('جلد کتاب', body)


def toc_doc(entries, extra_title) -> str:
    """Visible table of contents page, linked to every chapter and section."""
    items = []
    for e in entries:
        sub = ''
        if e['sections']:
            sub = '<ol>' + ''.join(
                f'<li class="lvl2"><a href="{e["href"]}#{anchor}">{esc(t)}</a></li>'
                for t, anchor in e['sections']) + '</ol>'
        items.append(f'<li class="lvl1"><a href="{e["href"]}">{esc(e["title"])}</a>{sub}</li>')
    items.append(f'<li class="lvl1"><a href="colophon.xhtml">{esc(extra_title)}</a></li>')
    body = ('<section role="doc-toc"><h1>فهرست مطالب</h1>'
            f'<nav><ol>{"".join(items)}</ol></nav></section>')
    return html_doc('فهرست مطالب', body)


def licence_doc() -> str:
    """The font licence notices, as an XHTML document (linked from the colophon)."""
    text = (FONTS / 'LICENSE-fonts.txt').read_text(encoding='utf-8')
    body = ('<section epub:type="notice">'
            '<h1>اجازه‌نامه فونت‌های جاسازی‌شده</h1>'
            '<p>این کتاب سه فونت را در خود جاسازی کرده است. متن کامل اجازه‌نامه‌های آن‌ها '
            'در پایین آمده است.</p>'
            f'<pre class="licence" dir="ltr" xml:lang="en" lang="en">{esc(text)}</pre>'
            '</section>')
    return html_doc('اجازه‌نامه فونت‌ها', body)


def colophon_doc(n_docs: int, built: str) -> str:
    body = f'''
<h1>درباره این نسخه الکترونیکی</h1>
<p class="colophon">این فایل، نسخه <strong>EPUB 3</strong> کتاب «قانون زبان — راهنمای جامع و
عملی Provincial Coordinator» (نسخه دوم، ۱۴۰۵) است که از همان متن واحدِ نسخه چاپی ساخته شده؛
هیچ متنی مخصوص این نسخه تغییر نکرده است، فقط نحو (Markup) و صفحه‌آرایی آن برای صفحه‌های
الکترونیکی تنظیم شده است. برای بازکردن آن از هر خواننده EPUB (مانند Apple Books،
Google Play Books، Calibre، Thorium یا KOReader) می‌توانید استفاده کنید.</p>

<h2>ساختار و ناوبری</h2>
<ul>
<li>فهرست مطالب درونی (این صفحه) و فهرست ناوبری کتاب — هر دو با لینک به بخش‌های هر فصل.</li>
<li>{n_docs} سند محتوایی، هر فصل یک فایل جدا، با ترتیب راست‌به‌چپ.</li>
<li>صفحه جلد، نشانه‌های ساختاری (فصل، پیوست، واژه‌نامه) و «راهنمای بخش‌ها» برای
پرش سریع به جلد، فهرست و آغاز متن.</li>
</ul>

<h2>فونت‌ها و اجازه‌نامه</h2>
<ul>
<li><strong>Vazir</strong> برای متن اصلی و <strong>Samim</strong> به‌عنوان قلم برجسته و
سرفصل‌ها — همان ترکیب نسخه چاپی. هر دو در خودِ فایل جاسازی شده‌اند تا نوشتار دری همه‌جا
درست دیده شود.</li>
<li><strong>BookSymbols</strong> — زیرمجموعه‌ای کوچک از DejaVu Sans که فقط برای نشانه‌هایی
مانند ✓ ✗ ★ ● ↓ به کار می‌رود (این نشانه‌ها در فونت‌های دری نیستند).</li>
<li>متن کامل اجازه‌نامه‌ها همراه کتاب است:
<a href="license.xhtml">license.xhtml</a></li>
</ul>

<h2>دسترس‌پذیری</h2>
<ul>
<li>متن کامل به‌صورت متن واقعی (قابل بزرگ‌نمایی و جست‌وجو)، بدون تصویر اسکن‌شده.</li>
<li>عنوان‌ها در سطوح واقعی (h1 تا h4)، جدول‌های واقعی با سرستون، و جعبه‌های هشدار/مثال
به‌صورت بخش‌های معنایی (aside).</li>
<li>متن انگلیسی و اصطلاحات لاتین با نشانه‌گذاری زبان انگلیسی، تا خواننده صفحه یا
برنامه گفتاری آن را درست بخواند.</li>
<li>تنها تصویر کتاب، صفحه جلد است و متن جانشین (alt) دارد.</li>
</ul>

<h2>نسخه و مشخصات ساخت</h2>
<ul>
<li>شناسه کتاب (identifier): <span lang="en" xml:lang="en">{IDENTIFIER}</span></li>
<li>تاریخ ساخت این فایل: {built} (به وقت ساخت ماشین)</li>
<li>ناشر: {ORGANISATION}</li>
</ul>
'''
    return html_doc('درباره این نسخه الکترونیکی', body, etype='colophon')


# ------------------------------------------------------------------ build ---

def main() -> None:
    blocks = parse(bookgen.MASTER)
    book = epub.EpubBook()
    book.set_identifier(IDENTIFIER)
    book.set_title(TITLE)
    book.set_language(LANG)
    book.set_direction('rtl')
    book.add_author(ORGANISATION, file_as='Shuhada Organization')
    book.add_metadata('DC', 'publisher', ORGANISATION)
    book.add_metadata('DC', 'date', '2026')
    book.add_metadata('DC', 'rights', f'© {ORGANISATION}، ۱۴۰۵ / 2026')
    book.add_metadata('DC', 'description',
                      f'{SUBTITLE}. ده فصل، سناریوهای واقعی، تمرین و جواب مدل، '
                      'قالب‌های کاری، واژه‌نامه دری–انگلیسی و آزمون‌های آزمایشی.')
    for subject in ('صحت عامه — افغانستان', 'BPHS و EPHS', 'مدیریت پروژه',
                    'HMIS و DHIS2', 'راهنمای آموزشی و کاری'):
        book.add_metadata('DC', 'subject', subject)
    # EPUB Accessibility 1.1
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
                      'متن کامل و قابل جست‌وجو، ساختار عنوان‌بندی‌شده، جدول‌های واقعی با '
                      'سرستون، فهرست ناوبری دو‌سطحی، جلد با متن جانشین. هیچ عنصر صوتی یا '
                      'ویدیویی ندارد؛ به خواننده صفحه یا صفحه‌کلید نیاز ندارد.',
                      {'property': 'schema:accessibilitySummary'})

    # ---- stylesheet and fonts
    book.add_item(epub.EpubItem(uid='style', file_name='style/main.css',
                                media_type='text/css', content=CSS))
    for uid, name in (('vazir', 'Vazir.woff2'), ('samim', 'Samim.woff2'),
                      ('symbols', 'BookSymbols.woff2')):
        book.add_item(epub.EpubItem(uid=uid, file_name=f'fonts/{name}',
                                    media_type='font/woff2',
                                    content=(FONTS / name).read_bytes()))
    licence = epub.EpubHtml(uid='font-licence', file_name='license.xhtml',
                            title='اجازه‌نامه فونت‌ها', lang=LANG)
    licence.content = licence_doc()

    # ---- cover image + cover page
    cover_item = epub.EpubItem(uid='cover-img', file_name='images/cover.png',
                               media_type='image/png', content=COVER.read_bytes())
    cover_item.properties = ['cover-image']
    book.add_item(cover_item)
    book.add_metadata('OPF', 'meta', '', {'name': 'cover', 'content': 'cover-img'})

    cover = epub.EpubHtml(uid='cover', file_name='cover.xhtml', title='جلد کتاب', lang=LANG)
    cover.content = cover_doc()
    cover.properties = ['svg']
    book.add_item(cover)

    # ---- body documents, one per top-level heading
    docs = split_documents(blocks)
    entries, items = [], []
    for i, doc in enumerate(docs):
        doc_id = f'ch{i:02d}'
        ctx = Context(doc_id)
        body = render_blocks(doc['blocks'], ctx)
        etype = doc_type(doc['title'], i, len(docs))
        item = epub.EpubHtml(uid=doc_id, file_name=f'{doc_id}.xhtml',
                             title=doc['title'], lang=LANG)
        item.content = html_doc(doc['title'], body, etype=etype)
        book.add_item(item)
        items.append(item)
        entries.append({'title': doc['title'], 'href': f'{doc_id}.xhtml',
                        'sections': ctx.sections})

    # ---- visible table of contents
    toc_item = epub.EpubHtml(uid='toc', file_name='toc.xhtml', title='فهرست مطالب', lang=LANG)
    toc_item.content = toc_doc(entries, 'درباره این نسخه الکترونیکی')
    book.add_item(toc_item)

    # ---- colophon
    colophon = epub.EpubHtml(uid='colophon', file_name='colophon.xhtml',
                             title='درباره این نسخه الکترونیکی', lang=LANG)
    colophon.content = colophon_doc(len(items), '۱۴۰۵ (ساخته‌شده از متن واحد نسخه دوم)')
    book.add_item(colophon)
    book.add_item(licence)

    # ---- navigation: two levels, both in nav.xhtml and toc.ncx
    toc_entries = []
    for e in entries:
        link = epub.Link(e['href'], e['title'], e['href'].split('.')[0])
        if e['sections']:
            children = tuple(epub.Link(f"{e['href']}#{anchor}", title,
                                       f"{e['href'].split('.')[0]}-s{k}")
                             for k, (title, anchor) in enumerate(e['sections'], 1))
            toc_entries.append((link, children))
        else:
            toc_entries.append(link)
    toc_entries.append(epub.Link('colophon.xhtml', 'درباره این نسخه الکترونیکی', 'colophon-link'))
    book.toc = tuple(toc_entries)

    nav = epub.EpubNav(title='فهرست مطالب')
    book.add_item(nav)
    book.add_item(epub.EpubNcx())

    # ---- landmarks / reading order
    first_chapter = next((e['href'] for e in entries if e['title'].startswith('فصل ')),
                         entries[0]['href'])
    book.guide = [
        {'type': 'cover', 'title': 'جلد', 'href': 'cover.xhtml'},
        {'type': 'toc', 'title': 'فهرست مطالب', 'href': 'toc.xhtml'},
        {'type': 'text', 'title': 'آغاز متن', 'href': first_chapter},
    ]
    book.spine = [cover, toc_item, *items, colophon, (licence, 'no'), nav]

    OUT_DIR.mkdir(exist_ok=True)
    epub.write_epub(str(OUT), book,
                    {'epub2_guide': False, 'epub3_landmark': True,
                     'epub3_pages': False, 'landmark_title': 'راهنمای بخش‌ها'})

    normalise(OUT)
    print(f'EPUB -> {OUT}')
    print(f'  documents: {len(items) + 3} (content {len(items)}, toc, cover, colophon) '
          f'+ nav + ncx')
    print(f'  sections linked in the TOC: {sum(len(e["sections"]) for e in entries)}')
    print(f'  size: {OUT.stat().st_size / 1024:.0f} KB')


def normalise(path: Path) -> None:
    """Final pass over the package: RTL spine and dir attributes.

    ebooklib serialises the documents through lxml, which drops the `dir`
    attribute we put on <html>/<body>, and it only writes
    page-progression-direction when the book direction is set - we enforce both
    so the file is correct even if the library changes.
    """
    tmp = path.with_suffix('.tmp.epub')
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
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
            zout.writestr(it, data)
    tmp.replace(path)


if __name__ == '__main__':
    main()
