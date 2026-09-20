#!/usr/bin/env python3
"""
Phase 6 (PDF) - two PDF editions from the single-source master:

  * print-ready PDF : 17 x 24 cm trim, mirrored (gutter) margins, no live links
  * screen PDF      : A4, live internal links, roomier margins

RTL/Dari handling: Vazir (body) + Samim (headings/bold) are embedded, and every
Dari run is reshaped then bidi-reordered before layout, so mixed Dari/English
lines (drug names, acronyms, numbers, units) do not scramble.
"""
import re
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

import bookgen
from bookgen import ROOT, inline_runs, parse

FONT_DIR = ROOT / 'project/assets/fonts'
OUT_DIR = ROOT / 'output'
RESHAPER = arabic_reshaper.ArabicReshaper(
    configuration={'delete_harakat': False, 'support_ligatures': True})

NAVY = colors.HexColor('#1F3A5F')
ACCENT = colors.HexColor('#0F6B5E')
GREY = colors.HexColor('#4A4A4A')
LIGHT = colors.HexColor('#F5F7FA')
BORDER = colors.HexColor('#D0D7DE')

CALLOUT_COLOR = {
    'concept': (colors.HexColor('#E7F3F7'), colors.HexColor('#0E7490'), 'مفهوم ساده'),
    'example': (colors.HexColor('#F1ECFB'), colors.HexColor('#6D28D9'), 'مثال از دایکندی'),
    'tip': (colors.HexColor('#FDF3E3'), colors.HexColor('#B45309'), 'برای امتحان'),
    'key': (colors.HexColor('#FDECEC'), colors.HexColor('#B91C1C'), 'حفظ کن'),
    'action': (colors.HexColor('#E8F5F1'), colors.HexColor('#0F6B5E'), 'قاعده عملی'),
    'mistake': (colors.HexColor('#FDECEC'), colors.HexColor('#B91C1C'), 'اشتباه رایج و شکل درست'),
    'answer-fa': (colors.HexColor('#EDF1F7'), colors.HexColor('#1F3A5F'), 'جواب مدل'),
    'answer-en': (colors.HexColor('#EDF1F7'), colors.HexColor('#1F3A5F'), 'Sample Answer'),
    'scenario': (colors.HexColor('#EDF1F7'), colors.HexColor('#1F3A5F'), 'سناریو'),
    'objectives': (colors.HexColor('#E8F5F1'), colors.HexColor('#0F6B5E'), 'اهداف این فصل'),
}

DARI_RE = re.compile(r'[\u0600-\u06FF]')


COVERED = set()
SYMBOL_FONT = 'DejaVu'


def register_fonts():
    from fontTools.ttLib import TTFont as FTFont
    pdfmetrics.registerFont(TTFont('Vazir', str(FONT_DIR / 'Vazir.ttf')))
    pdfmetrics.registerFont(TTFont('Samim', str(FONT_DIR / 'Samim.ttf')))
    pdfmetrics.registerFont(TTFont(SYMBOL_FONT, '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    for name in ('Vazir', 'Samim'):
        f = FTFont(str(FONT_DIR / f'{name}.ttf'))
        for tb in f['cmap'].tables:
            COVERED.update(tb.cmap.keys())
    pdfmetrics.registerFontFamily('Vazir', normal='Vazir', bold='Samim',
                                  italic='Vazir', boldItalic='Samim')


def shape(text: str) -> str:
    """Reshape + bidi-reorder a Dari (or mixed) string for visual layout."""
    if not DARI_RE.search(text):
        return text
    return get_display(RESHAPER.reshape(text))


def esc(t: str) -> str:
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def markup(text: str, bold_font='Samim', normal_font='Vazir') -> str:
    """Inline **bold** -> shaped spans. Characters the text fonts do not cover
    (arrows, marks) are rendered from the symbol font so nothing prints as a box."""
    parts = []
    for chunk, is_bold in inline_runs(text):
        font = bold_font if is_bold else normal_font
        for seg, is_sym in split_symbols(chunk):
            f = SYMBOL_FONT if is_sym else font
            parts.append(f'<font name="{f}">{esc(seg if is_sym else shape(seg))}</font>')
    return ''.join(parts)


def split_symbols(chunk: str):
    out, buf, prev = [], '', None
    for ch in chunk:
        is_sym = ord(ch) not in COVERED
        if prev is None or is_sym == prev:
            buf += ch
        else:
            out.append((buf, prev))
            buf = ch
        prev = is_sym
    if buf:
        out.append((buf, prev))
    return out


def styles(scale=1.0):
    s = {}
    s['title'] = ParagraphStyle('title', fontName='Samim', fontSize=26 * scale,
                                leading=36 * scale, alignment=TA_CENTER, textColor=NAVY)
    s['subtitle'] = ParagraphStyle('subtitle', fontName='Vazir', fontSize=14 * scale,
                                   leading=22 * scale, alignment=TA_CENTER, textColor=ACCENT)
    s['front'] = ParagraphStyle('front', fontName='Samim', fontSize=19 * scale,
                                leading=27 * scale, alignment=TA_RIGHT, textColor=NAVY,
                                spaceBefore=14, spaceAfter=8)
    s['chapter'] = ParagraphStyle('chapter', fontName='Samim', fontSize=19 * scale,
                                  leading=28 * scale, alignment=TA_RIGHT, textColor=NAVY,
                                  spaceBefore=6, spaceAfter=10)
    s['section'] = ParagraphStyle('section', fontName='Samim', fontSize=14 * scale,
                                  leading=21 * scale, alignment=TA_RIGHT, textColor=ACCENT,
                                  spaceBefore=12, spaceAfter=5)
    s['subsection'] = ParagraphStyle('subsection', fontName='Samim', fontSize=11.5 * scale,
                                     leading=18 * scale, alignment=TA_RIGHT, textColor=GREY,
                                     spaceBefore=9, spaceAfter=4)
    s['examq'] = ParagraphStyle('examq', fontName='Samim', fontSize=11 * scale,
                                leading=17 * scale, alignment=TA_RIGHT, textColor=NAVY,
                                spaceBefore=7, spaceAfter=3)
    s['body'] = ParagraphStyle('body', fontName='Vazir', fontSize=10.5 * scale,
                               leading=17.5 * scale, alignment=TA_JUSTIFY, textColor=colors.black,
                               wordWrap='RTL', spaceAfter=5)
    s['bodyr'] = ParagraphStyle('bodyr', parent=s['body'], alignment=TA_RIGHT)
    s['small'] = ParagraphStyle('small', parent=s['body'], fontSize=9.5 * scale,
                                leading=15 * scale, alignment=TA_RIGHT, textColor=GREY)
    s['cell'] = ParagraphStyle('cell', fontName='Vazir', fontSize=8.6 * scale,
                               leading=13.5 * scale, alignment=TA_RIGHT, wordWrap='RTL')
    s['cellh'] = ParagraphStyle('cellh', fontName='Samim', fontSize=8.8 * scale,
                                leading=13.5 * scale, alignment=TA_RIGHT, textColor=NAVY,
                                wordWrap='RTL')
    s['callout_title'] = ParagraphStyle('callout_title', fontName='Samim',
                                        fontSize=10 * scale, leading=15 * scale,
                                        alignment=TA_RIGHT)
    s['callout_body'] = ParagraphStyle('callout_body', fontName='Vazir', fontSize=9.8 * scale,
                                       leading=16 * scale, alignment=TA_JUSTIFY,
                                       wordWrap='RTL', spaceAfter=3)
    s['toc1'] = ParagraphStyle('toc1', fontName='Samim', fontSize=11 * scale,
                               leading=19 * scale, alignment=TA_RIGHT, textColor=NAVY)
    s['toc2'] = ParagraphStyle('toc2', fontName='Vazir', fontSize=9.8 * scale,
                               leading=16 * scale, alignment=TA_RIGHT)
    s['caption'] = ParagraphStyle('caption', fontName='Vazir', fontSize=8.5 * scale,
                                  textColor=GREY, alignment=TA_CENTER)
    return s


class Book(BaseDocTemplate):
    def __init__(self, filename, meta, styl, pagesize, mirror=True, **kw):
        self.meta = meta
        self.styl = styl
        self.mirror = mirror
        BaseDocTemplate.__init__(self, filename, pagesize=pagesize,
                                 title=meta['title'] + ' — ' + meta['subtitle'],
                                 author=meta['org_en'], subject=meta['subtitle'],
                                 creator='Shuhada Organization — editorial pipeline',
                                 lang='fa-AF', **kw)
        w, h = pagesize
        self.odd_frame = Frame(3.0 * cm, 2.4 * cm, w - 5.4 * cm, h - 4.8 * cm,
                               id='odd', showBoundary=0)
        self.even_frame = Frame(2.4 * cm, 2.4 * cm, w - 5.4 * cm, h - 4.8 * cm,
                                id='even', showBoundary=0)
        self.cover_frame = Frame(0.3 * cm, 0.3 * cm, w - 0.6 * cm, h - 0.6 * cm,
                                 id='cover', showBoundary=0)
        self.addPageTemplates([
            PageTemplate(id='Cover', frames=[self.cover_frame],
                         onPage=lambda c, d: None),
            PageTemplate(id='Odd', frames=[self.odd_frame], onPage=self.decorate),
            PageTemplate(id='Even', frames=[self.even_frame], onPage=self.decorate),
        ])

    def decorate(self, canvas, doc):
        canvas.saveState()
        page = canvas.getPageNumber()
        canvas.setFont('Vazir', 8)
        canvas.setFillColor(GREY)
        label = shape('صفحه ') + str(page)
        canvas.drawCentredString(doc.pagesize[0] / 2, 1.4 * cm, label)
        canvas.setFont('Vazir', 7.5)
        head = shape(self.meta['title'] + ' — ' + self.meta['subtitle'])
        canvas.drawCentredString(doc.pagesize[0] / 2, doc.pagesize[1] - 1.5 * cm, head)
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.4)
        canvas.line(2.4 * cm, doc.pagesize[1] - 1.8 * cm,
                    doc.pagesize[0] - 2.4 * cm, doc.pagesize[1] - 1.8 * cm)
        canvas.line(2.4 * cm, 1.9 * cm, doc.pagesize[0] - 2.4 * cm, 1.9 * cm)
        canvas.restoreState()

    # --- TOC support ---------------------------------------------------
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style = flowable.style.name
            text = flowable.getPlainText()
            if style in ('chapter', 'front'):
                self.notify('TOCEntry', (0, text, self.page))
            elif style == 'section':
                self.notify('TOCEntry', (1, text, self.page))


def table_flowable(block, styl, avail_width):
    rows = block.items
    if not rows:
        return Spacer(1, 1)
    ncols = max(len(r) for r in rows)
    data = []
    for ri, row in enumerate(rows):
        cells = []
        for ci in range(ncols):
            txt = row[ci] if ci < len(row) else ''
            cells.append(Paragraph(markup(txt, bold_font='Samim'),
                                   styl['cellh'] if ri == 0 else styl['cell']))
        cells.reverse()                      # RTL: first logical column on the right
        data.append(cells)
    t = Table(data, colWidths=[avail_width / ncols] * ncols, repeatRows=1, hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8EEF5')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t


def callout_flowable(block, styl, avail_width):
    bg, line, default_title = CALLOUT_COLOR.get(block.ctype, (LIGHT, NAVY, block.ctype))
    title = block.ctitle or default_title
    inner = [Paragraph(markup(title), ParagraphStyle(
        'ct', parent=styl['callout_title'], textColor=line))]
    for sub in block.items:
        if sub.kind == 'para':
            inner.append(Paragraph(markup(sub.text), styl['callout_body']))
        elif sub.kind == 'bullet':
            for item in sub.items:
                inner.append(Paragraph(markup('• ' + item),
                                       ParagraphStyle('cb', parent=styl['callout_body'],
                                                      rightIndent=8, spaceAfter=2)))
        elif sub.kind == 'table':
            inner.append(table_flowable(sub, styl, avail_width - 20))
            inner.append(Spacer(1, 4))
        elif sub.kind in ('section', 'subsection', 'chapter', 'examq'):
            inner.append(Paragraph(markup(sub.text), ParagraphStyle(
                'cs', parent=styl['subsection'])))
        elif sub.kind == 'flow':
            inner.append(Paragraph('⇩', ParagraphStyle('cf', parent=styl['bodyr'],
                                                       alignment=TA_CENTER)))
    t = Table([[inner]], colWidths=[avail_width], hAlign='CENTER')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('LINEAFTER', (0, 0), (0, 0), 2.4, line),
        ('BOX', (0, 0), (-1, -1), 0.4, BORDER),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


def build(blocks, meta, styl, pagesize, out_path, mirror=True, links=True):
    doc = Book(str(out_path), meta, styl, pagesize, mirror=mirror)
    w = pagesize[0] - 5.4 * cm
    story = []

    # ---- title page -------------------------------------------------
    cover_path = ROOT / 'project/assets/cover.png'
    if cover_path.exists():
        from PIL import Image as PILImage
        iw, ih = PILImage.open(cover_path).size
        ratio = iw / ih
        aw = doc.cover_frame._getAvailableWidth() - 2
        ah = doc.cover_frame._aH - 2
        if aw / ah > ratio:
            ch, cw = ah, ah * ratio
        else:
            cw, ch = aw, aw / ratio
        story += [Image(str(cover_path), width=cw, height=ch, hAlign='CENTER'),
                  NextPageTemplate('Odd'), PageBreak()]

    story += [Spacer(1, 3.2 * cm),
              Paragraph(markup(meta['title']), styl['title']),
              Spacer(1, 0.5 * cm),
              Paragraph(markup(meta['subtitle']), styl['subtitle']),
              Spacer(1, 2.2 * cm),
              Paragraph(shape(meta['org_fa']), styl['subtitle']),
              Paragraph(meta['org_en'], styl['subtitle']),
              Paragraph(markup(meta['motto']), styl['subtitle']),
              Spacer(1, 2.0 * cm),
              Paragraph(shape(meta['edition']), styl['bodyr']),
              Paragraph(shape(meta['year']), styl['bodyr']),
              PageBreak()]

    # ---- table of contents ------------------------------------------
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle('toc1', parent=styl['toc1'], leftIndent=0, firstLineIndent=0),
        ParagraphStyle('toc2', parent=styl['toc2'], leftIndent=14, firstLineIndent=0),
    ]
    toc.dotsMinLevel = 0
    story += [Paragraph(markup('فهرست مطالب'), styl['chapter']), toc, PageBreak()]

    first = True
    for b in blocks:
        if b.kind in ('chapter', 'front'):
            if not first:
                story.append(PageBreak())
            first = False
            style = 'front' if not b.text.startswith(('فصل ', 'پیوست', 'پایان کتاب', 'درباره این نسخه')) \
                else 'chapter'
            story.append(Paragraph(markup(b.text), styl[style]))
            story.append(Table([['']], colWidths=[w / 3], rowHeights=[2],
                               style=[('BACKGROUND', (0, 0), (-1, -1), ACCENT)]))
            story.append(Spacer(1, 6))
        elif b.kind == 'section':
            story.append(Paragraph(markup(b.text), styl['section']))
        elif b.kind == 'subsection':
            story.append(Paragraph(markup(b.text), styl['subsection']))
        elif b.kind == 'examq':
            story.append(Paragraph(markup(b.text), styl['examq']))
        elif b.kind == 'table':
            story.append(table_flowable(b, styl, w))
            story.append(Spacer(1, 8))
        elif b.kind == 'bullet':
            for item in b.items:
                story.append(Paragraph(markup('• ' + item),
                                       ParagraphStyle('bl', parent=styl['body'],
                                                      rightIndent=10, spaceAfter=2)))
        elif b.kind == 'flow':
            story.append(Paragraph('⇩', ParagraphStyle('fl', parent=styl['body'],
                                                       alignment=TA_CENTER)))
        elif b.kind == 'callout':
            story.append(Spacer(1, 4))
            story.append(callout_flowable(b, styl, w))
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(markup(b.text), styl['body']))

    doc.multiBuild(story)
    print(f'PDF -> {out_path}')


def main():
    blocks = parse(bookgen.MASTER)
    OUT_DIR.mkdir(exist_ok=True)
    meta = {
        'title': 'کتاب قانون زبان',
        'subtitle': 'راهنمای جامع و عملی Provincial Coordinator',
        'org_fa': 'سازمان شهدا — ولایت دایکندی',
        'org_en': 'Shuhada Organization — Daikundi',
        'motto': '«Working for a better tomorrow»',
        'edition': 'نسخه دوم — ویرایش‌شده، تصحیح‌شده و آماده نشر',
        'year': '۱۴۰۵ خورشیدی',
    }
    register_fonts()
    build(blocks, meta, styles(0.98), (17 * cm, 24 * cm),
          OUT_DIR / 'قانون_زبان_Provincial_Coordinator_چاپی_17x24.pdf')
    build(blocks, meta, styles(1.0), (21 * cm, 29.7 * cm),
          OUT_DIR / 'قانون_زبان_Provincial_Coordinator_دیجیتال_A4.pdf')


if __name__ == '__main__':
    main()
