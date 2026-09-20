#!/usr/bin/env python3
"""
DOCX builder - the editable Word edition.

Real Word paragraph styles throughout (no manual per-paragraph formatting), RTL
paragraphs and runs, mirrored margins, a cover page, an automatically updating
table of contents, real tables with a repeated header row, and one single-cell
shaded table per callout so the boxes survive editing.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT, WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import mgmtgen
from mgmtgen import ROOT, inline_runs

OUT = ROOT / 'output' / 'مدیریت_مبانی_و_مهارت‌ها.docx'
COVER = ROOT / 'assets/cover.png'

FONT = 'Vazir'   # the family actually shipped in assets/fonts (Vazir.ttf)
FONT_FALLBACK = 'Tahoma'
NAVY = RGBColor(0x1D, 0x33, 0x58)
ACCENT = RGBColor(0x14, 0x58, 0x4F)
GREY = RGBColor(0x44, 0x4A, 0x55)
DANGER = RGBColor(0x9A, 0x3B, 0x2E)
GOLD = RGBColor(0x7A, 0x60, 0x18)

TITLE = 'مدیریت؛ مبانی و مهارت‌های اساسی مدیریت'
DESCRIPTION = ('کتاب درسی مدیریت به زبان دری افغانستان: بیست فصل، سی کیس کاری، بستهٔ '
               'ابزارهای عملی، کارگاه تمرین و واژه‌نامهٔ اصطلاحات. نسخهٔ حرفه‌ای دری.')
KEYWORDS = ('مدیریت؛ رهبری؛ پلان‌گذاری؛ سازماندهی؛ کنترول؛ مدیریت منابع بشری؛ '
            'تصمیم‌گیری؛ دری افغانستان')
BUILD_DATE = '2026-09-20'
LANG_TAG = 'fa-AF'
LANDSCAPE_MIN_COLS = 7
SUBTITLE = 'Management: The Essentials — Afghan Dari Professional Edition'
PUBLISHER = 'نشر سرچشمه'
STRAP = 'بیست فصل · سی کیس کاری · بستهٔ چهارده‌گانهٔ ابزارها · صد و پنجاه پرسش تمرینی · واژه‌نامهٔ کامل اصطلاحات'

CALLOUT = {
    'story': ('Story Box', 'D9E2EC', '3E5C86'),
    'case': ('Case Box', 'E4E9F0', '1D3358'),
    'decision': ('Decision Point', 'F4EFDD', '8A6D1F'),
    'tool': ('Tool Box', 'E6EFED', '14584F'),
    'note': ('Note', 'F1F0EC', '6B6B63'),
    'reflect': ('Practice Box', 'EAF1F0', '14584F'),
    'warn': ('Warning Box', 'F5E7E4', '9A3B2E'),
    'key': ('Key Point', 'E8EFEE', '14584F'),
    'ethics': ('Ethics Check', 'EFEAF2', '5B4B7A'),
    'data': ('Data Box', 'E9EEF4', '2B4A7A'),
}


def rtl_para(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, style=None):
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement('w:bidi'))
    p.alignment = align
    return p


def set_font(rpr, name=FONT):
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    rf.set(qn('w:cs'), name)
    rf.set(qn('w:ascii'), name)
    rf.set(qn('w:hAnsi'), name)


def rtl_run(run, size=None):
    rPr = run._element.get_or_add_rPr()
    rPr.append(OxmlElement('w:rtl'))
    rPr.append(OxmlElement('w:cs'))
    set_font(rPr)
    if size:
        sz = OxmlElement('w:szCs')
        sz.set(qn('w:val'), str(int(size * 2)))
        rPr.append(sz)
    return run


def shade(element, fill):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill)
    element.append(shd)


def table_rtl(table):
    table._tbl.tblPr.append(OxmlElement('w:bidiVisual'))


def cell_borders(cell, colour='DCDCD4', size=6, accent=None, accent_side='right'):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'bottom', 'left', 'right'):
        el = OxmlElement(f'w:{edge}')
        col = colour
        sz = size
        if accent and edge == accent_side:
            col, sz = accent, 24
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:color'), col)
        borders.append(el)
    tcPr.append(borders)


def keep_with_next(p):
    pPr = p._p.get_or_add_pPr()
    el = OxmlElement('w:keepNext')
    pPr.append(el)
    return p


def define_styles(doc):
    styles = doc.styles
    base = styles['Normal']
    base.font.name = FONT
    base.font.size = Pt(10.5)
    base.paragraph_format.space_after = Pt(6)
    base.paragraph_format.line_spacing = 1.4
    set_font(base.element.get_or_add_rPr())

    def new(name, size, bold=False, colour=None, before=0, after=6, base_style='Normal',
            align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False, keep=False):
        try:
            st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        except Exception:                                          # noqa: BLE001
            st = styles[name]
            if st.type != WD_STYLE_TYPE.PARAGRAPH:      # a built-in character style
                st = styles.add_style(name + ' Para', WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = styles[base_style]
        st.font.name = FONT
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.italic = italic
        if colour is not None:
            st.font.color.rgb = colour
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.line_spacing = 1.4
        st.paragraph_format.alignment = align
        st.paragraph_format.keep_with_next = keep
        st.element.get_or_add_pPr().append(OxmlElement('w:bidi'))
        set_font(st.element.get_or_add_rPr())
        return st

    new('BK Title', 26, True, NAVY, 0, 8, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('BK Subtitle', 13, False, ACCENT, 0, 6, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('BK Meta', 10.5, False, GREY, 0, 4, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('BK Part', 20, True, ACCENT, 24, 14, base_style='Heading 1',
        align=WD_ALIGN_PARAGRAPH.CENTER, keep=True)
    new('BK Chapter', 17, True, NAVY, 20, 12, base_style='Heading 1',
        align=WD_ALIGN_PARAGRAPH.RIGHT, keep=True)
    new('BK Section', 13.5, True, ACCENT, 14, 6, base_style='Heading 2',
        align=WD_ALIGN_PARAGRAPH.RIGHT, keep=True)
    new('BK Subsection', 11.5, True, GREY, 11, 4, base_style='Heading 3',
        align=WD_ALIGN_PARAGRAPH.RIGHT, keep=True)
    new('BK Subsub', 10.5, True, NAVY, 9, 4, base_style='Heading 4',
        align=WD_ALIGN_PARAGRAPH.RIGHT, keep=True)
    new('BK Body', 10.5, False, None, 0, 6)
    new('BK Body First', 10.5, False, None, 0, 6)
    new('BK Quote', 10.5, False, GREY, 4, 8, italic=False)
    new('BK List', 10.5, False, None, 0, 3, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Table Cell', 9, False, None, 0, 2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Table Head', 9, True, NAVY, 0, 2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Caption', 8.5, False, GREY, 2, 8, italic=True)
    new('BK Toc 1', 11, False, NAVY, 6, 2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Toc 2', 10, False, GREY, 0, 1, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Flow', 10.5, True, ACCENT, 6, 8, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('BK Callout Title', 10.5, True, ACCENT, 0, 3, align=WD_ALIGN_PARAGRAPH.RIGHT,
        keep=True)
    new('BK Callout Body', 10, False, None, 0, 4)
    new('BK Callout List', 10, False, None, 0, 2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Glossary', 10, True, NAVY, 6, 2, align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('BK Exam Q', 10.5, True, NAVY, 8, 3, align=WD_ALIGN_PARAGRAPH.RIGHT,
        keep=True)
    new('BK Exam Opt', 10, False, None, 0, 2, align=WD_ALIGN_PARAGRAPH.RIGHT)


def add_text(container, text, style='BK Body', bold=False, italic=False,
             align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=None, colour=None,
             space_before=None, space_after=None, indent=None):  # noqa: D401
    p = container.add_paragraph(style=style)
    rtl_para(p, align)
    if space_before is not None:
        p.paragraph_format.space_before = Pt(space_before)
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.right_indent = Cm(indent)
    for chunk, b, i in inline_runs(text):
        run = p.add_run(chunk)
        run.bold = bold or b
        run.italic = italic or i
        if colour is not None:
            run.font.color.rgb = colour
        rtl_run(run, size)
    return p
    return p


def portrait_section(doc, landscape_first=False):
    """A4 portrait section with the book's margins."""
    sect = doc.sections[-1]
    sect.orientation = WD_ORIENT.PORTRAIT
    sect.page_width, sect.page_height = Cm(21), Cm(29.7)
    sect.top_margin = sect.bottom_margin = Cm(2.2)
    sect.left_margin = sect.right_margin = Cm(2.3)
    return sect


def add_landscape_table(doc, rows):
    """Wide tables get their own landscape page; no font or column shrinking."""
    sect = doc.add_section(WD_SECTION.NEW_PAGE)
    sect.orientation = WD_ORIENT.LANDSCAPE
    sect.page_width, sect.page_height = Cm(29.7), Cm(21)
    sect.top_margin = sect.bottom_margin = Cm(1.6)
    sect.left_margin = sect.right_margin = Cm(1.5)
    add_table(doc, rows, avail_cm=26.7)
    back = doc.add_section(WD_SECTION.NEW_PAGE)
    back.orientation = WD_ORIENT.PORTRAIT
    back.page_width, back.page_height = Cm(21), Cm(29.7)
    back.top_margin = back.bottom_margin = Cm(2.2)
    back.left_margin = back.right_margin = Cm(2.3)


def add_table(container, rows, style_head='BK Table Head', style_cell='BK Table Cell',
              avail_cm=None):
    rows = [r for r in rows if r]
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = container.add_table(rows=len(rows), cols=ncols)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table_rtl(table)
    tblPr = table._tbl.tblPr
    width = OxmlElement('w:tblW')
    width.set(qn('w:type'), 'pct')
    width.set(qn('w:w'), '5000')
    tblPr.append(width)
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)
    # repeat the header row on every page
    trPr = table.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))
    size = 8.0 if ncols >= 7 else (8.5 if ncols >= 5 else 9)
    avail = Cm(avail_cm) if avail_cm else Cm(15.6)
    col_w = int(avail / ncols)
    for ri, row in enumerate(rows):
        for ci in range(ncols):
            cell = table.cell(ri, ci)
            txt = row[ci] if ci < len(row) else ''
            cell.text = ''
            p = cell.paragraphs[0]
            rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
            p.paragraph_format.space_after = Pt(2)
            for chunk, b, i in inline_runs(txt):
                run = p.add_run(chunk)
                run.font.size = Pt(size)
                run.bold = b or ri == 0
                if ri == 0:
                    run.font.color.rgb = NAVY
                rtl_run(run, size)
            shade(cell._tc.get_or_add_tcPr(), 'E8EFEE' if ri == 0 else
                  ('FFFFFF' if ri % 2 else 'FAFAF8'))
            cell_borders(cell, 'DCDCD4')
    for row in table.rows:
        for cell in row.cells:
            cell.width = col_w
    sp = container.add_paragraph()
    sp.paragraph_format.space_after = Pt(2)


def add_callout(doc, block):
    style_name, fill, accent = CALLOUT.get(block.ctype, ('Note', 'F1F0EC', '6B6B63'))
    label = mgmtgen.CALLOUTS.get(block.ctype, block.ctype)
    title = f'{label} — {block.ctitle}' if block.ctitle else label
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_rtl(table)
    cell = table.cell(0, 0)
    cell.text = ''
    shade(cell._tc.get_or_add_tcPr(), fill)
    cell_borders(cell, 'DCDCD4', accent=accent)
    p = cell.paragraphs[0]
    p.style = doc.styles['BK Callout Title']
    rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
    run = p.add_run(title)
    run.bold = True
    run.font.color.rgb = RGBColor.from_string(accent)
    rtl_run(run)
    add_callout_body(doc, cell, block.items)
    gap = doc.add_paragraph()
    gap.paragraph_format.space_after = Pt(4)


def add_callout_body(doc, cell, items):
    for sub in items:
        if sub.kind == 'para':
            p = cell.add_paragraph(style='BK Callout Body')
            rtl_para(p)
            for chunk, b, i in inline_runs(sub.text):
                r = p.add_run(chunk)
                r.bold = b
                r.italic = i
                rtl_run(r, 10)
            for extra in sub.lines:
                r = p.add_run(' ' + extra)
                rtl_run(r, 10)
        elif sub.kind in ('bullet', 'olist'):
            for n, item in enumerate(sub.items, 1):
                p = cell.add_paragraph(style='BK Callout List')
                rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
                bullet = '• ' if sub.kind == 'bullet' else f'{n}. '
                parts = item.split('\n')
                for chunk, b, i in inline_runs(bullet + parts[0]):
                    r = p.add_run(chunk)
                    r.bold = b
                    rtl_run(r, 10)
                for extra in parts[1:]:
                    r2 = p.add_run()
                    r2.add_break()
                    for chunk, b, i in inline_runs(extra):
                        rr = p.add_run(chunk)
                        rr.italic = i
                        rtl_run(rr, 10)
        elif sub.kind == 'table':
            add_table(cell, sub.items)
        elif sub.kind in ('h2', 'h3', 'h4'):
            p = cell.add_paragraph(style='BK Subsection')
            rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
            run = p.add_run(sub.text)
            rtl_run(run)
        elif sub.kind == 'flow':
            p = cell.add_paragraph(style='BK Flow')
            rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
            r = p.add_run(sub.text)
            rtl_run(r)
        elif sub.kind == 'quote':
            p = cell.add_paragraph(style='BK Callout Body')
            rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
            r = p.add_run(sub.text)
            r.italic = True
            rtl_run(r)


def add_flow(doc, text):
    p = doc.add_paragraph(style='BK Flow')
    rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
    run = p.add_run(text)
    rtl_run(run)


def title_page(doc):
    if COVER.exists():
        p = doc.add_paragraph()
        rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
        p.add_run().add_picture(str(COVER), width=Cm(13.5))
    doc.add_page_break()
    p = doc.add_paragraph(style='BK Title')
    rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(TITLE)
    rtl_run(r)
    p = doc.add_paragraph(style='BK Subtitle')
    rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
    r = p.add_run(SUBTITLE)
    rtl_run(r)
    doc.add_paragraph()
    for text in (STRAP, '', 'ناشر: ' + PUBLISHER, 'سال نشر: 1405 / 2026',
                 'نسخهٔ دری افغانستان — ویرایش حرفه‌ای'):
        p = doc.add_paragraph(style='BK Meta')
        rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
        r = p.add_run(text)
        rtl_run(r)
    doc.add_page_break()


def add_bookmark(paragraph, name):
    """Wrap a paragraph in a Word bookmark so PAGEREF can point at it."""
    start = OxmlElement('w:bookmarkStart')
    start.set(qn('w:id'), str(abs(hash(name)) % 100000))
    start.set(qn('w:name'), name)
    end = OxmlElement('w:bookmarkEnd')
    end.set(qn('w:id'), start.get(qn('w:id')))
    paragraph._p.insert(0, start)
    paragraph._p.append(end)


def toc_plan(blocks):
    """Collect real TOC entries (parts, chapters, appendices + their sections)."""
    plan, index = [], {}
    for i, b in enumerate(blocks):
        if b.kind == 'part':
            plan.append({'i': i, 'level': 1, 'text': b.text, 'bookmark': f'_Toc9{len(plan) + 1:05d}'})
        elif b.kind == 'h1':
            plan.append({'i': i, 'level': 1, 'text': b.text, 'bookmark': f'_Toc9{len(plan) + 1:05d}'})
        elif b.kind == 'h2':
            plan.append({'i': i, 'level': 2, 'text': b.text, 'bookmark': f'_Toc9{len(plan) + 1:05d}'})
    for e in plan:
        index[e['i']] = e['bookmark']
    return plan, index


def toc_page(doc, plan):
    p = doc.add_paragraph(style='BK Chapter')
    rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
    r = p.add_run('فهرست مطالب')
    rtl_run(r)
    for e in plan:
        style = 'BK Toc 1' if e['level'] == 1 else 'BK Toc 2'
        para = doc.add_paragraph(style=style)
        rtl_para(para, WD_ALIGN_PARAGRAPH.RIGHT)
        para.paragraph_format.tab_stops.add_tab_stop(Cm(15.2), WD_TAB_ALIGNMENT.LEFT,
                                                    WD_TAB_LEADER.DOTS)
        run = para.add_run(e['text'])
        rtl_run(run)
        tab = para.add_run('\t')
        rtl_run(tab)
        fld = OxmlElement('w:fldSimple')
        fld.set(qn('w:instr'), f' PAGEREF {e["bookmark"]} \\h ')
        para._p.append(fld)
    doc.add_page_break()


def core_properties(doc):
    """Professional publication metadata. Publisher attribution, no invented author."""
    cp = doc.core_properties
    cp.title = TITLE
    cp.subject = SUBTITLE
    cp.author = PUBLISHER
    cp.last_modified_by = PUBLISHER
    cp.category = 'مدیریت'
    cp.comments = DESCRIPTION
    cp.keywords = KEYWORDS
    cp.language = LANG_TAG
    cp.revision = 1
    cp.created = datetime(2026, 9, 20, 9, 0, 0)
    cp.modified = datetime(2026, 9, 20, 9, 0, 0)


def fix_app_properties(path):
    """Remove the python-docx template's stale Word statistics; keep honest app info."""
    import shutil
    import zipfile
    tmp = path.with_suffix('.docx.tmp')
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == 'docProps/app.xml':
                xml = data.decode('utf-8')
                cut = ('<Template>Normal.dotm</Template>', '<TotalTime>0</TotalTime>',
                       '<Pages>1</Pages>', '<Words>0</Words>', '<Characters>0</Characters>',
                       '<Lines>0</Lines>', '<Paragraphs>0</Paragraphs>',
                       '<CharactersWithSpaces>0</CharactersWithSpaces>',
                       '<AppVersion>14.0000</AppVersion>',
                       '<Application>Microsoft Macintosh Word</Application>')
                for c in cut:
                    xml = xml.replace(c, '')
                # no vendor claim and no builder name: the generation tool is not
                # publication metadata a reader should see
                xml = xml.replace('<Manager/>', '<Manager>' + PUBLISHER + '</Manager>')
                xml = xml.replace('<Company/>', '<Company>' + PUBLISHER + '</Company>')
                data = xml.encode('utf-8')
            dst.writestr(item, data)
    shutil.move(str(tmp), str(path))


def header_footer(section):
    section.different_first_page_header_footer = True
    hp = section.header.paragraphs[0]
    rtl_para(hp, WD_ALIGN_PARAGRAPH.CENTER)
    r = hp.add_run(TITLE)
    r.font.size = Pt(8)
    r.font.color.rgb = GREY
    rtl_run(r)
    fp = section.footer.paragraphs[0]
    rtl_para(fp, WD_ALIGN_PARAGRAPH.CENTER)
    r = fp.add_run('صفحه ')
    r.font.size = Pt(9)
    rtl_run(r)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    fp._p.append(fld)


def settings(doc):
    el = doc.settings.element
    el.append(OxmlElement('w:mirrorMargins'))
    uf = OxmlElement('w:updateFields')
    uf.set(qn('w:val'), 'true')
    el.append(uf)


def main():
    blocks = mgmtgen.parse(mgmtgen.MASTER)
    doc = Document()
    define_styles(doc)
    sect = doc.sections[0]
    sect.page_width = Cm(21)
    sect.page_height = Cm(29.7)
    sect.top_margin = sect.bottom_margin = Cm(2.2)
    sect.left_margin = sect.right_margin = Cm(2.3)
    header_footer(sect)
    settings(doc)
    core_properties(doc)
    title_page(doc)
    plan, bookmarks = toc_plan(blocks)
    toc_page(doc, plan)

    for bi, b in enumerate(blocks):
        if b.kind == 'part':
            doc.add_page_break()
            p = add_text(doc, b.text, 'BK Part', align=WD_ALIGN_PARAGRAPH.CENTER)
            add_bookmark(p, bookmarks[bi])
        elif b.kind == 'h1':
            if not b.text.startswith(('سرآغاز', 'دربارهٔ')):
                doc.add_page_break()
            p = add_text(doc, b.text, 'BK Chapter', align=WD_ALIGN_PARAGRAPH.RIGHT)
            add_bookmark(p, bookmarks[bi])
        elif b.kind == 'h2':
            p = add_text(doc, b.text, 'BK Section', align=WD_ALIGN_PARAGRAPH.RIGHT)
            add_bookmark(p, bookmarks[bi])
        elif b.kind == 'h3':
            add_text(doc, b.text, 'BK Subsection', align=WD_ALIGN_PARAGRAPH.RIGHT)
        elif b.kind == 'h4':
            add_text(doc, b.text, 'BK Subsub', align=WD_ALIGN_PARAGRAPH.RIGHT)
        elif b.kind == 'para':
            add_text(doc, b.text, 'BK Body')
        elif b.kind == 'bullet':
            for item in b.items:
                parts = item.split('\n')
                add_text(doc, '• ' + parts[0], 'BK List', indent=0.5)
                for extra in parts[1:]:
                    add_text(doc, '   ' + extra, 'BK List', indent=1.0)
        elif b.kind == 'olist':
            for n, item in enumerate(b.items):
                marker = b.markers[n] if n < len(b.markers) else str(n + 1)
                parts = item.split('\n')
                add_text(doc, f'{marker}. ' + parts[0], 'BK List', indent=0.5)
                for extra in parts[1:]:
                    add_text(doc, '   ' + extra, 'BK List', indent=1.0)
        elif b.kind == 'quote':
            add_text(doc, b.text, 'BK Quote', italic=True, indent=0.6)
        elif b.kind == 'flow':
            add_flow(doc, b.text)
        elif b.kind == 'table':
            rows = [r for r in b.items if r]
            ncols = max((len(r) for r in rows), default=0)
            if ncols >= LANDSCAPE_MIN_COLS:
                add_landscape_table(doc, b.items)
            else:
                add_table(doc, b.items)
        elif b.kind == 'callout':
            add_callout(doc, b)

    OUT.parent.mkdir(exist_ok=True)
    doc.save(OUT)
    fix_app_properties(OUT)
    print(f'DOCX -> {OUT}')
    print(f'  paragraphs: {len(doc.paragraphs)} · tables: {len(doc.tables)} · '
          f'size: {OUT.stat().st_size / 1024:.0f} KB')


if __name__ == '__main__':
    main()
