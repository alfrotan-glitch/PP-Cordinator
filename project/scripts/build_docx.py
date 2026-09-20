#!/usr/bin/env python3
"""
Phase 6 (DOCX) - build the editable Word edition from the single-source master.

Real Word paragraph/character styles (no manual per-paragraph formatting), so the
author can keep editing, and the automatic table of contents works:
  - styles : Title, Subtitle, Author, Chapter, Section, Subsection, Body Text,
             Note, Warning, Clinical Pearl, Key Point, Table, Caption, Reference,
             Front Matter, Exam Question
  - RTL    : bidi paragraphs + rtl runs, mirrored margins, RTL tables
  - TOC    : a real TOC field with updateFields=true, so Word refreshes it on open
"""
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

import bookgen
from bookgen import ROOT, inline_runs, parse

OUT_DIR = ROOT / 'output'
OUT = OUT_DIR / 'قانون_زبان_Provincial_Coordinator_DOCX_نسخه_نهایی.docx'
FONT = 'Vazirmatn'
FONT_FALLBACK = 'Tahoma'

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT = RGBColor(0x0F, 0x6B, 0x5E)
GREY = RGBColor(0x44, 0x44, 0x44)

CALLOUT_STYLE = {
    'concept': ('Note', '0E7490', 'مفهوم ساده'),
    'example': ('Note', '6D28D9', 'مثال از دایکندی'),
    'tip': ('Clinical Pearl', 'B45309', 'برای امتحان'),
    'key': ('Key Point', 'B91C1C', 'حفظ کن'),
    'action': ('Key Point', '0F6B5E', 'قاعده عملی'),
    'mistake': ('Warning', 'B91C1C', 'اشتباه رایج و شکل درست'),
    'answer-fa': ('Note', '1F3A5F', 'جواب مدل'),
    'answer-en': ('Reference', '1F3A5F', 'Sample Answer'),
    'scenario': ('Warning', '1F3A5F', 'سناریو'),
    'objectives': ('Clinical Pearl', '0F6B5E', 'اهداف این فصل'),
}


# --------------------------------------------------------------------- helpers
def rtl_para(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    pPr.append(bidi)
    p.alignment = align
    return p


def rtl_run(run):
    rPr = run._element.get_or_add_rPr()
    rtl = OxmlElement('w:rtl')
    rPr.append(rtl)
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:cs'), FONT)
    rFonts.set(qn('w:ascii'), FONT)
    rFonts.set(qn('w:hAnsi'), FONT)
    return run


def add_field(paragraph, instr):
    run = paragraph.add_run()
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), instr)
    run._element.addprevious(fld)
    return paragraph


def shade(element, color):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    element.append(shd)


def set_table_rtl(table):
    tblPr = table._tbl.tblPr
    bidi = OxmlElement('w:bidiVisual')
    tblPr.append(bidi)


def cell_borders(cell, color='D0D7DE', size=6, left_accent=None):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge, col in (('top', color), ('bottom', color), ('left', color), ('right', color)):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(size))
        el.set(qn('w:color'), col)
        borders.append(el)
    tcPr.append(borders)
    if left_accent:
        el = OxmlElement('w:tcBorders')
        b = OxmlElement('w:right')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '24')
        b.set(qn('w:color'), left_accent)
        el.append(b)
        tcPr.append(el)


def define_styles(doc):
    """Create the named styles the reference-DOCX checklist requires."""
    styles = doc.styles
    base = styles['Normal']
    base.font.name = FONT
    base.font.size = Pt(11)
    base.paragraph_format.space_after = Pt(6)
    base.paragraph_format.line_spacing = 1.35
    rpr = base.element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    rf.set(qn('w:cs'), FONT)
    rf.set(qn('w:ascii'), FONT)
    rf.set(qn('w:hAnsi'), FONT)

    from docx.enum.style import WD_STYLE_TYPE

    def new(name, size, bold=False, color=None, space_before=0, space_after=6,
            base_style='Normal', italic=False, align=None):
        try:
            st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        except Exception:
            st = styles[name]
        st.base_style = styles[base_style]
        st.font.name = FONT
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.italic = italic
        if color is not None:
            st.font.color.rgb = color
        st.paragraph_format.space_before = Pt(space_before)
        st.paragraph_format.space_after = Pt(space_after)
        st.paragraph_format.line_spacing = 1.35
        if align:
            st.paragraph_format.alignment = align
        ppr = st.element.get_or_add_pPr()
        ppr.append(OxmlElement('w:bidi'))
        rpr2 = st.element.get_or_add_rPr()
        rf2 = rpr2.find(qn('w:rFonts'))
        if rf2 is None:
            rf2 = OxmlElement('w:rFonts')
            rpr2.insert(0, rf2)
        rf2.set(qn('w:cs'), FONT)
        rf2.set(qn('w:ascii'), FONT)
        rf2.set(qn('w:hAnsi'), FONT)
        return st

    new('Title', 28, True, NAVY, 0, 10, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('Subtitle', 15, False, ACCENT, 0, 6, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('Author', 12, False, GREY, 0, 4, align=WD_ALIGN_PARAGRAPH.CENTER)
    new('Front Matter', 18, True, NAVY, 18, 10)
    new('Chapter', 20, True, NAVY, 24, 12, base_style='Heading 1',
        align=WD_ALIGN_PARAGRAPH.RIGHT)
    new('Section', 15, True, ACCENT, 16, 8, base_style='Heading 2')
    new('Subsection', 12.5, True, GREY, 12, 6, base_style='Heading 3')
    new('Exam Question', 11.5, True, NAVY, 10, 4)
    new('Body Text', 11, False, None, 0, 6)
    new('Note', 10.5, False, None, 4, 4)
    new('Warning', 10.5, False, None, 4, 4)
    new('Clinical Pearl', 10.5, False, None, 4, 4)
    new('Key Point', 10.5, True, None, 4, 4)
    new('Caption', 9.5, False, GREY, 2, 8, italic=True)
    new('Reference', 10, False, None, 2, 4)
    new('Bibliography', 10, False, None, 2, 4)


def add_para(doc, text, style='Body Text', bold=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph(style=style)
    rtl_para(p, align)
    for chunk, is_bold in inline_runs(text):
        run = p.add_run(chunk)
        run.bold = bold or is_bold
        rtl_run(run)
    return p


def add_callout(doc, block):
    style, hexcolor, default_title = CALLOUT_STYLE.get(
        block.ctype, ('Note', '1F3A5F', block.ctype))
    title = block.ctitle or default_title
    if not title.startswith(('⭐', '🔴', '❌', '✅')):
        title = f'{title}'
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_rtl(table)
    cell = table.cell(0, 0)
    shade(cell._tc.get_or_add_tcPr(), 'F5F7FA')
    cell_borders(cell, 'D0D7DE', left_accent=hexcolor)
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)

    p = cell.add_paragraph(style=style)
    rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
    run = p.add_run(title)
    run.bold = True
    run.font.color.rgb = RGBColor.from_string(hexcolor)
    rtl_run(run)

    for sub in block.items:
        if sub.kind in ('para',):
            p = cell.add_paragraph(style=style)
            rtl_para(p)
            for chunk, is_bold in inline_runs(sub.text):
                r = p.add_run(chunk)
                r.bold = is_bold
                rtl_run(r)
        elif sub.kind == 'bullet':
            for item in sub.items:
                p = cell.add_paragraph(style=style)
                rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
                p.paragraph_format.left_indent = Cm(0)
                p.paragraph_format.right_indent = Cm(0.4)
                for chunk, is_bold in inline_runs('• ' + item):
                    r = p.add_run(chunk)
                    r.bold = is_bold
                    rtl_run(r)
        elif sub.kind == 'table':
            add_table(cell, sub)
        elif sub.kind in ('section', 'subsection', 'examq', 'chapter'):
            p = cell.add_paragraph(style='Subsection')
            rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT)
            r = p.add_run(sub.text)
            rtl_run(r)
        elif sub.kind == 'flow':
            p = cell.add_paragraph(style=style)
            rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
            r = p.add_run('⇩')
            rtl_run(r)
    doc.add_paragraph()


def add_table(container, block):
    rows = block.items
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    table = container.add_table(rows=len(rows), cols=ncols)
    table.style = 'Table Grid'
    set_table_rtl(table)
    for ri, row in enumerate(rows):
        for ci in range(ncols):
            cell = table.cell(ri, ci)
            txt = row[ci] if ci < len(row) else ''
            cell.text = ''
            p = cell.paragraphs[0]
            rtl_para(p, WD_ALIGN_PARAGRAPH.RIGHT if ri == 0 else WD_ALIGN_PARAGRAPH.RIGHT)
            for chunk, is_bold in inline_runs(txt):
                run = p.add_run(chunk)
                run.font.size = Pt(9.5)
                run.bold = is_bold or ri == 0
                rtl_run(run)
            if ri == 0:
                shade(cell._tc.get_or_add_tcPr(), 'E8EEF5')
            else:
                shade(cell._tc.get_or_add_tcPr(), 'FFFFFF')
    container.add_paragraph()


COVER = ROOT / 'project/assets/cover.png'


def title_page(doc, meta):
    if COVER.exists():
        p = doc.add_paragraph()
        rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
        p.add_run().add_picture(str(COVER), width=Cm(16.2))
        doc.add_page_break()
    for _ in range(3):
        doc.add_paragraph()
    p = add_para(doc, meta['title'], 'Title', align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, meta['subtitle'], 'Subtitle', align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()
    add_para(doc, meta['org_fa'], 'Author', align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, meta['org_en'], 'Author', align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, meta['motto'], 'Author', align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()
    add_para(doc, meta['edition'], 'Author', align=WD_ALIGN_PARAGRAPH.CENTER)
    add_para(doc, meta['year'], 'Author', align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()


def toc_page(doc):
    p = add_para(doc, 'فهرست مطالب', 'Chapter')
    para = doc.add_paragraph()
    rtl_para(para, WD_ALIGN_PARAGRAPH.RIGHT)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), r'TOC \o "1-2" \h \z \u')
    inner = OxmlElement('w:p')
    r = OxmlElement('w:r')
    t = OxmlElement('w:t')
    t.text = 'فهرست به‌روز می‌شود — در صورت نیاز Ctrl+A و سپس F9 را بزنید.'
    r.append(t)
    inner.append(r)
    fld.append(inner)
    para._p.append(fld)
    doc.add_page_break()


def header_footer(section, meta):
    section.different_first_page_header_footer = True
    hp = section.header.paragraphs[0]
    rtl_para(hp, WD_ALIGN_PARAGRAPH.CENTER)
    run = hp.add_run(meta['title'] + ' — ' + meta['subtitle'])
    run.font.size = Pt(8.5)
    run.font.color.rgb = GREY
    rtl_run(run)

    fp = section.footer.paragraphs[0]
    rtl_para(fp, WD_ALIGN_PARAGRAPH.CENTER)
    run = fp.add_run('صفحه ')
    run.font.size = Pt(9)
    rtl_run(run)
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    fp._p.append(fld)


def set_mirror_margins(doc):
    settings = doc.settings.element
    el = OxmlElement('w:mirrorMargins')
    settings.append(el)
    uf = OxmlElement('w:updateFields')
    uf.set(qn('w:val'), 'true')
    settings.append(uf)


def main():
    blocks = parse(bookgen.MASTER)
    meta = {
        'title': 'کتاب قانون زبان',
        'subtitle': 'راهنمای جامع و عملی Provincial Coordinator',
        'org_fa': 'سازمان شهدا — ولایت دایکندی',
        'org_en': 'Shuhada Organization — Daikundi',
        'motto': '«Working for a better tomorrow»',
        'edition': 'نسخه دوم — ویرایش‌شده، تصحیح‌شده و آماده نشر',
        'year': '۱۴۰۵ خورشیدی',
    }

    doc = Document()
    define_styles(doc)
    sect = doc.sections[0]
    sect.page_width = Cm(21)
    sect.page_height = Cm(29.7)
    sect.top_margin = sect.bottom_margin = Cm(2.2)
    sect.left_margin = sect.right_margin = Cm(2.4)
    header_footer(sect, meta)
    set_mirror_margins(doc)

    title_page(doc, meta)
    toc_page(doc)

    front_matter = True
    for b in blocks:
        if b.kind == 'chapter':
            front_matter = not b.text.startswith(('فصل ', 'پیوست', 'پایان کتاب', 'درباره این نسخه'))
            if b.text.startswith('فصل ') or b.text.startswith('پیوست'):
                doc.add_page_break()
            add_para(doc, b.text, 'Front Matter' if front_matter else 'Chapter',
                     align=WD_ALIGN_PARAGRAPH.RIGHT)
            # running-head bookmark so the TOC picks the real heading text up
            for run in doc.paragraphs[-1].runs:
                rtl_run(run)
        elif b.kind == 'section':
            add_para(doc, b.text, 'Section', align=WD_ALIGN_PARAGRAPH.RIGHT)
        elif b.kind == 'subsection':
            add_para(doc, b.text, 'Subsection', align=WD_ALIGN_PARAGRAPH.RIGHT)
        elif b.kind == 'examq':
            add_para(doc, b.text, 'Exam Question', align=WD_ALIGN_PARAGRAPH.RIGHT)
        elif b.kind == 'table':
            add_table(doc, b)
        elif b.kind == 'bullet':
            for item in b.items:
                p = doc.add_paragraph(style='Body Text')
                rtl_para(p)
                p.paragraph_format.right_indent = Cm(0.5)
                for chunk, is_bold in inline_runs('• ' + item):
                    run = p.add_run(chunk)
                    run.bold = is_bold
                    rtl_run(run)
        elif b.kind == 'flow':
            p = doc.add_paragraph(style='Body Text')
            rtl_para(p, WD_ALIGN_PARAGRAPH.CENTER)
            run = p.add_run('⇩')
            rtl_run(run)
        elif b.kind == 'callout':
            add_callout(doc, b)
        else:
            add_para(doc, b.text)

    OUT_DIR.mkdir(exist_ok=True)
    doc.save(OUT)
    print('DOCX ->', OUT)
    print('  paragraphs:', len(doc.paragraphs), ' tables:', len(doc.tables))


if __name__ == '__main__':
    main()
