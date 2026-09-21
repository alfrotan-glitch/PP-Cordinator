# -*- coding: utf-8 -*-
"""
docx.py — the Word (DOCX) production renderer.

The DOCX is a first-class deliverable: A4 with mirrored (gutter) margins, a right-to-left
section, complex-script (Dari) font mapping, real Word fields (an automatic table of
contents, STYLEREF running heads, PAGE folios), repeating table header rows, keep-with-next
on headings and callout boxes.

Nothing is added to or removed from the frozen manuscript except the publishing front
matter (title page, copyright/about page, contents) and the appendix banners.
"""
from __future__ import annotations

import os
import re
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmodel as bm
import design
import units as U

# ------------------------------------------------------------------ helpers

W = qn  # shorthand


def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


def rgb(hexstr):
    h = hexstr.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_rtl(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.append(_el("w:bidi"))


def keep_next(paragraph, keep=True):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.append(_el("w:keepNext", val="1" if keep else "0"))


def keep_lines(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.append(_el("w:keepLines", val="1"))


def run_fonts(run, dari_font, latin_font):
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:ascii"), latin_font)
    rFonts.set(qn("w:hAnsi"), latin_font)
    rFonts.set(qn("w:cs"), dari_font)


def set_run_props(run, size=None, bold=None, italic=None, color=None, rtl=False,
                  dari_font="Vazirmatn", latin_font="Source Serif 4"):
    run_fonts(run, dari_font, latin_font)
    rPr = run._element.get_or_add_rPr()
    if size is not None:
        rPr.append(_el("w:sz", val=int(size * 2)))
        rPr.append(_el("w:szCs", val=int(size * 2)))
    if bold:
        rPr.append(_el("w:b", val="1"))
        rPr.append(_el("w:bCs", val="1"))
    if italic:
        rPr.append(_el("w:i", val="1"))
        rPr.append(_el("w:iCs", val="1"))
    if color is not None:
        val = str(color).lstrip("#")
        if len(val) != 6:
            val = "%02X%02X%02X" % (color[0] if isinstance(color, tuple) else 0,
                                    color[1] if isinstance(color, tuple) else 0,
                                    color[2] if isinstance(color, tuple) else 0)
        rPr.append(_el("w:color", val=val))
    if rtl:
        rPr.append(_el("w:rtl", val="1"))
        rPr.append(_el("w:cs", val="1"))


def add_field(paragraph, instr, placeholder=" ", rtl=False, size=None, color=None):
    run = paragraph.add_run()
    set_run_props(run, size=size, color=color, rtl=rtl)
    r = run._r
    f1 = _el("w:fldChar", fldCharType="begin")
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    f2 = _el("w:fldChar", fldCharType="separate")
    t = OxmlElement("w:t")
    t.text = placeholder
    f3 = _el("w:fldChar", fldCharType="end")
    r.append(f1)
    r.append(it)
    r.append(f2)
    r.append(t)
    r.append(f3)
    return run


def shade(cell_or_par, fill):
    el = cell_or_par._tc.get_or_add_tcPr() if hasattr(cell_or_par, "_tc") else \
        cell_or_par._p.get_or_add_pPr()
    el.append(_el("w:shd", val="clear", color="auto", fill=fill.lstrip("#")))


def cell_borders(cell, color="c2ced2", sz=4):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = _el("w:" + edge, val="single", sz=sz, space=0, color=color.lstrip("#"))
        borders.append(e)
    tcPr.append(borders)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(_el("w:tblHeader", val="true"))


def table_rtl(table):
    tblPr = table._tbl.tblPr
    tblPr.append(_el("w:bidiVisual", val="1"))


# ------------------------------------------------------------------ styles

def build_styles(doc):
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Source Serif 4"
    normal.font.size = Pt(design.S["body"])
    rpr = normal.element.get_or_add_rPr()
    rpr.get_or_add_rFonts().set(qn("w:cs"), "Vazirmatn")
    rpr.append(_el("w:szCs", val=int(design.S["body"] * 2)))
    pf = normal.paragraph_format
    pf.space_after = Pt(3)
    pf.line_spacing = 1.1

    def new(name, size, color=design.INK, bold=False, space_before=0, space_after=4,
            base="Normal"):
        st = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        st.base_style = styles[base]
        st.font.size = Pt(size)
        st.font.bold = bold
        st.font.color.rgb = rgb(color)
        st.paragraph_format.space_before = Pt(space_before)
        st.paragraph_format.space_after = Pt(space_after)
        rpr = st.element.get_or_add_rPr()
        rpr.get_or_add_rFonts().set(qn("w:cs"), "Vazirmatn")
        rpr.append(_el("w:szCs", val=int(size * 2)))
        if bold:
            rpr.append(_el("w:bCs", val="1"))
        ppr = st.element.get_or_add_pPr()
        ppr.append(_el("w:bidi"))
        return st

    new("BookTitle", 30, design.ACCENT, True, 0, 6)
    new("BookSubtitle", 11.5, design.INK, False, 0, 4)
    new("BookTitleEn", 17, design.GREY, False, 0, 10)
    new("BookSubtitleEn", 10, design.GREY, False, 0, 10)
    new("FrontKicker", 8.4, design.GREY, False, 0, 2)
    new("FrontKickerEn", 8.4, design.GREY, False, 0, 0)
    new("AboutHead", 13, design.ACCENT, True, 0, 8)
    new("AboutLine", 9.2, design.INK_SOFT, False, 0, 5)
    new("ChapterKicker", 10.5, design.WARM_RULE, True, 0, 2)
    new("ChapterTitle", 23, design.ACCENT, True, 0, 4)
    new("ChapterTitleEn", 12.5, design.GREY, False, 0, 10)
    new("TopicKicker", 9.5, design.WARM_RULE, True, 0, 1)
    new("TopicTitle", 14.5, design.INK, True, 0, 2)
    new("TopicTitleEn", 9, design.GREY, False, 0, 6)
    new("SectionHead", 11.4, design.ACCENT, True, 10, 4)
    new("HighYieldHead", 11.4, "#7a5c12", True, 12, 4)
    new("SubHead", 10.4, design.INK, True, 8, 3)
    new("BodyFa", design.S["body"], design.INK, False, 0, 4)
    new("BodyEn", design.S["body_en"], design.INK_SOFT, False, 0, 6)
    new("LeadText", design.S["lead"], design.INK, True, 4, 4)
    new("ListItem", design.S["list"], design.INK, False, 0, 3)
    new("Callout", design.S["callout"], design.INK, False, 0, 3)
    new("CalloutItem", design.S["callout"], design.INK, False, 0, 3)
    new("AppendixText", design.S["appendix"], design.APPENDIX_INK, False, 0, 3)
    new("AppendixHead", 9.6, design.APPENDIX_INK, True, 8, 4)
    new("AppendixChapter", 12.5, design.ACCENT, True, 12, 4)
    new("BackTitle", 19, design.ACCENT, True, 0, 4)
    new("BackTitleEn", 10.5, design.GREY, False, 0, 4)
    new("BackNote", 9, design.INK_SOFT, False, 0, 6)
    new("TableCaption", 8.3, design.INK, False, 2, 4)
    new("ListMarker", design.S["list"], design.ACCENT, True, 0, 3)
    return styles


def para(doc, text_or_spans, style="BodyFa", rtl=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
         size=None, color=None, dari_font="Vazirmatn", latin_font="Source Serif 4"):
    p = doc.add_paragraph(style=style)
    if rtl:
        set_rtl(p)
    p.alignment = align
    spans = text_or_spans if isinstance(text_or_spans, list) else [bm.Span(text_or_spans)]
    for s in spans:
        add_span_run(p, s, size, rtl=rtl, color=color, dari_font=dari_font,
                     latin_font=latin_font)
    return p


# ------------------------------------------------------------------ content

def add_title_page(doc):
    for _ in range(3):
        doc.add_paragraph(style="Normal")
    para(doc, [bm.Span("مرجعِ معیار — Reference standard")], "FrontKicker", True,
         WD_ALIGN_PARAGRAPH.CENTER, color=rgb(design.GREY))
    p = doc.add_paragraph(style="FrontKickerEn")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(design.REFERENCE_LINE)
    set_run_props(r, size=8.4, color=rgb(design.GREY))
    para(doc, [bm.Span(design.TITLE_FA)], "BookTitle", True, WD_ALIGN_PARAGRAPH.CENTER)
    p = doc.add_paragraph(style="BookTitleEn")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(design.TITLE_EN)
    set_run_props(r, size=17, color=rgb(design.GREY))
    para(doc, [bm.Span(design.SUBTITLE_FA)], "BookSubtitle", True, WD_ALIGN_PARAGRAPH.CENTER)
    p = doc.add_paragraph(style="BookSubtitleEn")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(design.SUBTITLE_EN)
    set_run_props(r, size=10, color=rgb(design.GREY))
    para(doc, [bm.Span(design.AUDIENCE_LINE)], "BodyFa", True, WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, [bm.Span("۲۳ فصل · ۱۰۸ مبحث · ۱۳ بخشِ ثابت در هر مبحث · واژه‌نامهٔ ۶۹۰ اصطلاح")],
         "BodyFa", True, WD_ALIGN_PARAGRAPH.CENTER, color=rgb(design.ACCENT))
    para(doc, [bm.Span(design.EDITION_LINE)], "BodyFa", True, WD_ALIGN_PARAGRAPH.CENTER,
         color=rgb(design.GREY))
    doc.add_page_break()


def add_about_page(doc, doc_model):
    para(doc, [bm.Span("دربارهٔ این نسخه — About this edition")], "AboutHead", True,
         WD_ALIGN_PARAGRAPH.RIGHT)
    lines = [
        ("کتاب", f"{design.TITLE_FA} — {design.TITLE_EN}"),
        ("زبان", "دوزبانه — دری (افغانستان) + English"),
        ("مرجعِ معیار", design.REFERENCE_LINE),
        ("سطح", design.AUDIENCE_LINE),
        ("ساختار", "۲۳ فصل · ۱۰۸ مبحث · هر مبحث در ۱۳ بخشِ ثابت (تعریف، طبقه‌بندی، ساختمان، "
                   "حجرات، وظیفه، رابطهٔ ساختمان–وظیفه، نمای هستولوژیک، تشخیص، مقایسه، "
                   "همبستگی بالینی، نکاتِ امتحانی، جدولِ خلاصه، پرسش و پاسخ)."),
        ("ماهیتِ اثر", "این کتاب یک اثرِ آموزشیِ مستقل است؛ نه ترجمه، نه نقلِ متنِ مرجع و نه "
                       "بازنویسیِ نزدیک به آن. مبنای محتوا تجزیه و تحلیلِ مستقلِ مطالبِ مرجعِ "
                       "معیار و مقادیرِ متعارفِ هستولوژی است."),
        ("اصطلاح‌شناسی", "نام‌های بین‌المللیِ طبی (اندوتلیوم، ساینوسویید، ترومبوسیت، "
                         "کیموتراپی) به شکلِ رایجِ بین‌المللی و نام‌های تثبیت‌شدهٔ دری (کبد، "
                         "کلیه) به شکلِ معیارِ آموزشیِ افغانستان آمده‌اند؛ اتصالاتِ حجروی به "
                         "نامِ بین‌المللی (Tight junction / Zonula occludens، Adherens "
                         "junction / Zonula adherens، Gap junction) و کاربوهایدریت به همین "
                         "شکل ثبت شده‌اند."),
        ("قلم‌ها", "قلمِ دری: Vazirmatn؛ قلمِ لاتین: Source Serif 4؛ در صورت نبودِ این "
                   "قلم‌ها در دستگاه، خواندنِ فایل با قلمِ جانشینِ Word ادامه می‌یابد."),
    ]
    for head, body in lines:
        p = doc.add_paragraph(style="AboutLine")
        set_rtl(p)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r1 = p.add_run(f"{head}: ")
        set_run_props(r1, size=9.2, bold=True)
        r2 = p.add_run(body)
        set_run_props(r2, size=9.2)
    doc.add_page_break()


def add_toc_field(doc, doc_model):
    para(doc, [bm.Span("فهرست مطالب")], "BackTitle", True, WD_ALIGN_PARAGRAPH.RIGHT)
    p = doc.add_paragraph(style="BackTitleEn")
    r = p.add_run("Contents")
    set_run_props(r, size=10.5, color=rgb(design.GREY))
    note = doc.add_paragraph(style="BackNote")
    set_rtl(note)
    r = note.add_run("شمارهٔ صفحه‌ها در همین فایل به‌صورتِ خودکار به‌روز می‌شود.")
    set_run_props(r, size=9, color=rgb(design.GREY))
    p = doc.add_paragraph(style="Normal")
    set_rtl(p)
    add_field(p, "TOC \\o \"1-2\" \\h \\z \\u", placeholder=" ")
    doc.add_page_break()


def add_preface(doc, doc_model):
    head_done = 0
    for blk in doc_model.front:
        if blk.kind == "heading" and blk.level == 1 and head_done < 2:
            head_done += 1
            style = "BackTitle" if head_done == 1 else "BackTitleEn"
            para(doc, blk.spans[0], style, True,
                 WD_ALIGN_PARAGRAPH.RIGHT if head_done == 1 else WD_ALIGN_PARAGRAPH.LEFT)
            continue
        add_block(doc, blk, level=1)
    doc.add_page_break()


def add_chapter(doc, ch):
    p = doc.add_paragraph(style="ChapterKicker")
    set_rtl(p)
    r = p.add_run(f"فصل {U.fa_num(ch.number)}")
    set_run_props(r, size=10.5, bold=True, color=rgb(design.WARM_RULE))
    p = doc.add_paragraph(style="ChapterTitle")
    set_rtl(p)
    p.paragraph_format.page_break_before = True
    keep_next(p)
    r = p.add_run(ch.fa_title)
    set_run_props(r, size=23, bold=True, color=rgb(design.ACCENT))
    bm_start = add_bookmark(p, U.ch_id(ch.number))
    p = doc.add_paragraph(style="ChapterTitleEn")
    keep_next(p)
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run(f"Chapter {ch.number} — {ch.en_title}")
    set_run_props(r, size=12.5, color=rgb(design.GREY))

    for blk in ch.blocks:
        add_block(doc, blk, level=2)
    for t in ch.topics:
        p = doc.add_paragraph(style="TopicKicker")
        set_rtl(p)
        keep_next(p)
        r = p.add_run(f"مبحث {t.number}")
        set_run_props(r, size=9.5, bold=True, color=rgb(design.WARM_RULE))
        p = doc.add_paragraph(style="TopicTitle")
        set_rtl(p)
        keep_next(p)
        add_bookmark(p, U.tp_id(t.number))
        r = p.add_run(t.fa_title)
        set_run_props(r, size=14.5, bold=True)
        if t.en_title:
            p = doc.add_paragraph(style="TopicTitleEn")
            keep_next(p)
            r = p.add_run(t.en_title)
            set_run_props(r, size=9, color=rgb(design.GREY))
        for blk in t.blocks:
            add_block(doc, blk, level=2)
    for blk in ch.review:
        add_block(doc, blk, level=1)


def add_appendix_a(doc, doc_model):
    para(doc, [bm.Span("پیوستِ الف — پرسش‌های مروریِ فصل‌ها")], "BackTitle", True,
         WD_ALIGN_PARAGRAPH.RIGHT)
    p = doc.add_paragraph(style="BackTitleEn")
    r = p.add_run("Appendix A — Chapter Self-Assessment (Questions & Answers)")
    set_run_props(r, size=10.5, color=rgb(design.GREY))
    bm_start = add_bookmark(p, "bk-sa")
    para(doc, [bm.Span("برای هر فصل، پرسش‌های مروری و پاسخ‌های کوتاهِ آن. پاسخ‌ها را پس از "
                       "حلِ پرسش‌ها ببینید.")], "BackNote", True)
    for ch in doc_model.chapters:
        p = doc.add_paragraph(style="AppendixChapter")
        set_rtl(p)
        keep_next(p)
        r = p.add_run(f"فصل {U.fa_num(ch.number)} — {ch.fa_title}")
        set_run_props(r, size=12.5, bold=True, color=rgb(design.ACCENT))
        for blk in ch.sa:
            add_block(doc, blk, level=2)


def add_appendix_b(doc, doc_model):
    para(doc, [bm.Span("پیوستِ ب — ممیزیِ انطباق با مرجع")], "BackTitle", True,
         WD_ALIGN_PARAGRAPH.RIGHT)
    p = doc.add_paragraph(style="BackTitleEn")
    r = p.add_run("Appendix B — Reference Alignment Records (Junqueira’s Basic Histology, "
                  "17th ed.)")
    set_run_props(r, size=10.5, color=rgb(design.GREY))
    add_bookmark(p, "bk-audit")
    para(doc, [bm.Span("برای هر فصل، دوازده بررسیِ انطباقِ محتوا با مرجعِ معیار و موردهای "
                       "مقدارِ معیارِ آن ثبت شده است. این پیوست سندِ کیفیتِ کتاب است و بخشی "
                       "از متنِ درسی نیست.")], "BackNote", True)
    for ch in doc_model.chapters:
        for blk in ch.audit:
            add_block(doc, blk, level=1, audit=True)


def add_glossary(doc, doc_model):
    para(doc, [bm.Span("پیوستِ ج — واژه‌نامهٔ اصطلاح‌ها")], "BackTitle", True,
         WD_ALIGN_PARAGRAPH.RIGHT)
    p = doc.add_paragraph(style="BackTitleEn")
    r = p.add_run("Appendix C — Terminology Glossary (Afghan Dari · English · Latin)")
    set_run_props(r, size=10.5, color=rgb(design.GREY))
    add_bookmark(p, "bk-glossary")
    para(doc, [bm.Span("شکلِ معیاریِ هر اصطلاح در کتاب و برابرِ انگلیسی/لاتینِ آن؛ ستونِ آخر "
                       "نخستین فصلی است که اصطلاح در آن آمده است.")], "BackNote", True)
    rows = U.glossary_rows()
    table = doc.add_table(rows=1, cols=4)
    table.style = "Table Grid"
    table_rtl(table)
    hdr = table.rows[0]
    for i, txt in enumerate(("اصطلاح (دری)", "English", "Latin / مخفف", "فصل")):
        cell = hdr.cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        set_rtl(p)
        r = p.add_run(txt)
        set_run_props(r, size=8.3, bold=True)
        shade(cell, design.ACCENT_SOFT)
    repeat_header(hdr)
    for dari, eng, lat, chp in rows:
        cells = table.add_row().cells
        for i, (txt, rtl_) in enumerate(((dari, True), (eng, False), (lat, False), (chp, False))):
            cell = cells[i]
            cell.text = ""
            p = cell.paragraphs[0]
            if rtl_:
                set_rtl(p)
            r = p.add_run(txt)
            set_run_props(r, size=8.1, rtl=rtl_)
    for row in table.rows:
        for cell in row.cells:
            cell_borders(cell)


# ------------------------------------------------------------------ blocks

def add_bookmark(paragraph, name):
    bid = str(abs(hash(name)) % 100000 + 1000)
    start = _el("w:bookmarkStart", id=bid, name=name)
    end = _el("w:bookmarkEnd", id=bid)
    paragraph._p.insert(0, start)
    paragraph._p.append(end)
    return bid


def add_span_run(paragraph, span, size, rtl=True, color=None, dari_font="Vazirmatn",
                 latin_font="Source Serif 4"):
    """Add one manuscript span as file runs; comparison signs become LTR runs.

    Word mirrors Bidi_Mirrored characters (``<`` and ``>`` among them) inside an RTL run,
    so an author's «>۳» would print as «<۳».  A run without ``w:rtl`` is laid out LTR and
    keeps the sign the manuscript wrote; the stored characters are untouched either way.
    """
    parts = re.split(r"([<>])", span.text) if (rtl and any(c in "<>" for c in span.text)) \
        else [span.text]
    runs = []
    for part in parts:
        if not part:
            continue
        run = paragraph.add_run(part)
        set_run_props(run, size=size, bold=span.bold, italic=span.italic, color=color,
                      rtl=False if part in ("<", ">") else rtl,
                      dari_font=dari_font, latin_font=latin_font)
        if getattr(span, "sup", False):
            run.font.superscript = True
        elif getattr(span, "sub", False):
            run.font.subscript = True
        runs.append(run)
    return runs[0] if len(runs) == 1 else runs


def add_block(doc, blk, level=2, audit=False):
    role = getattr(blk, "role", "")
    style_txt = "AppendixText" if audit else None
    if blk.kind == "heading":
        if blk.level >= 3:
            return para(doc, blk.spans[0], "SubHead", True)
        if role == "audit-title":
            return para(doc, blk.spans[0], "AppendixChapter", True)
        if role == "record-head" or role == "audit-head":
            return para(doc, blk.spans[0], "AppendixHead", True)
        if role == "chapter-sa-head":
            return para(doc, blk.spans[0], "SubHead", True)
        if blk.level == 2 and audit:
            p = para(doc, blk.spans[0], "AppendixHead", True)
            keep_next(p)
            return p
        if blk.level == 2:
            style = "HighYieldHead" if "HIGH-YIELD" in blk.text else "SectionHead"
            p = para(doc, blk.spans[0], style, True)
            keep_next(p)
            return p
        p = para(doc, blk.spans[0], "SubHead", True)
        keep_next(p)
        return p

    if blk.kind == "para":
        spans = [sp for ps in blk.spans for sp in ps]
        rtl = not (role == "body-en")
        style = {"lead": "LeadText", "record-note": "AppendixText",
                 "body-en": "BodyEn"}.get(role, style_txt or "BodyFa")
        if audit and role not in ("lead",):
            style = "AppendixText"
        p = para(doc, spans, style, rtl,
                 align=WD_ALIGN_PARAGRAPH.JUSTIFY if rtl else WD_ALIGN_PARAGRAPH.LEFT)
        if role == "lead":
            keep_next(p)
        return p

    if blk.kind == "list":
        counters: dict[int, int] = {}
        base = min((i for i, _, _ in blk.items), default=0)
        for indent, kind, body in blk.items:
            lvl = max(0, (indent - base) // 2)
            if kind == "ol":
                counters[lvl] = counters.get(lvl, 0) + 1
                marker = U.fa_num(counters[lvl]) + "."
                for k in list(counters):
                    if k > lvl:
                        del counters[k]
            else:
                marker = "•"
                counters.pop(lvl, None)
            txt = body[2:] if body.startswith("* ") else body
            p = doc.add_paragraph(style="ListItem")
            set_rtl(p)
            p.paragraph_format.right_indent = Cm(0.4 + 0.35 * lvl)
            p.paragraph_format.left_indent = Cm(0)
            r = p.add_run(marker + "\u2009")
            set_run_props(r, size=design.S["list"], bold=True, color=rgb(design.ACCENT))
            for s in bm.parse_inline(txt):
                add_span_run(p, s, design.S["list"])
        return None

    if blk.kind == "table":
        return add_table(doc, blk, appendix=audit or getattr(blk, "role", "") == "audit-table",
                         audit_mode=audit)

    if blk.kind == "callout":
        return add_callout(doc, blk)

    if blk.kind == "diagram":
        p = para(doc, [bm.Span(blk.text)], "AppendixText", False, WD_ALIGN_PARAGRAPH.LEFT,
                 dari_font="Consolas", latin_font="Consolas")
        return p

    if blk.kind == "rule":
        p = doc.add_paragraph(style="Normal")
        pPr = p._p.get_or_add_pPr()
        pbdr = OxmlElement("w:pBdr")
        pbdr.append(_el("w:bottom", val="single", sz=4, space=1, color="e4eaec"))
        pPr.append(pbdr)
        return p
    return None


def add_callout(doc, blk):
    table = doc.add_table(rows=1, cols=1)
    table_rtl(table)
    cell = table.rows[0].cells[0]
    cell_borders(cell, color=design.WARM_RULE, sz=8)
    shade(cell, design.WARM)
    cell.text = ""
    first = True
    buf: list[str] = []

    def flush_items():
        for body in buf:
            p = cell.add_paragraph(style="CalloutItem")
            set_rtl(p)
            p.paragraph_format.right_indent = Cm(0.6)
            for s in bm.parse_inline(body):
                add_span_run(p, s, design.S["callout"])
        buf.clear()

    for item in [i for i in blk.items if isinstance(i, str) and i.strip()]:
        if item.strip().startswith("(") and item.strip()[1:2].isdigit():
            buf.append(item.strip())
            continue
        flush_items()
        p = cell.paragraphs[0] if first else cell.add_paragraph(style="Callout")
        first = False
        set_rtl(p)
        for s in bm.parse_inline(item):
            add_span_run(p, s, design.S["callout"])
    flush_items()
    return table


def add_table(doc, blk, appendix=False, audit_mode=False):
    ncols = max(len(blk.header or []), max((len(r) for r in blk.rows), default=0))
    if not ncols:
        return None
    size = design.S["appendix"] if appendix else design.S["table"]
    table = doc.add_table(rows=1, cols=ncols)
    table.style = "Table Grid"
    table.autofit = True
    table_rtl(table)
    widths = rh_column_widths(blk, ncols)
    hdr = table.rows[0]
    for i in range(ncols):
        cell = hdr.cells[i]
        cell.text = ""
        cell.width = Cm(17.0 * widths[i] / 100.0)
        txt = blk.header[i] if blk.header and i < len(blk.header) else ""
        p = cell.paragraphs[0]
        set_rtl(p)
        for s in bm.parse_inline(txt):
            add_span_run(p, s, size)
        shade(cell, "#f2f5f6" if appendix else design.ACCENT_SOFT)
        cell_borders(cell, color=design.RULE_SOFT if appendix else design.RULE)
    repeat_header(hdr)
    for row in blk.rows:
        cells = table.add_row().cells
        for i in range(ncols):
            cell = cells[i]
            cell.text = ""
            cell.width = Cm(17.0 * widths[i] / 100.0)
            txt = row[i] if i < len(row) else ""
            p = cell.paragraphs[0]
            ltr = bm.lang_of(bm.plain_text(txt)) == "en"
            if not ltr:
                set_rtl(p)
            for s in bm.parse_inline(txt):
                add_span_run(p, s, size, rtl=not ltr)
            cell_borders(cell, color=design.RULE_SOFT if appendix else design.RULE)
    return table


def rh_column_widths(blk, ncols):
    import render_html as rh
    return rh._column_widths(blk, ncols)


# ------------------------------------------------------------------ sections

def build_header_footer(section):
    section.header.is_linked_to_previous = False
    header = section.header
    p = header.paragraphs[0]
    set_rtl(p)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(p, "STYLEREF \"ChapterTitle\" \\* CHARFORMAT ", placeholder="فصل", rtl=True,
              size=7.4, color=rgb(design.GREY))
    p2 = header.add_paragraph()
    set_rtl(p2)
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run(design.RUNNING_TITLE)
    set_run_props(r, size=7.4, color=rgb(design.GREY))

    section.footer.is_linked_to_previous = False
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_field(fp, "PAGE \\* ARABIC", placeholder="1", rtl=True, size=9,
              color=rgb(design.ACCENT))


def configure_section(section):
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.26)
    section.right_margin = Cm(1.62)
    sectPr = section._sectPr
    sectPr.append(_el("w:bidi"))
    build_header_footer(section)


# ------------------------------------------------------------------ build

def build(out_path: str, verbose: bool = True) -> dict:
    import time
    t0 = time.time()
    doc_model = bm.load_document()
    doc = Document()
    build_styles(doc)
    configure_section(doc.sections[0])

    # Word should refresh the fields (table of contents, running heads, folios) on open
    settings = doc.settings.element
    settings.append(_el("w:updateFields", val="true"))

    core = doc.core_properties
    core.title = f"{design.TITLE_FA} — {design.TITLE_EN}"
    core.author = design.AUTHOR
    core.subject = ("دوزبانه (دری + English) — مرورِ امتحان‌محورِ هستولوژی بر پایهٔ "
                    "Junqueira's Basic Histology, 17th ed.")
    core.keywords = "هیستولوژی, Histology, دری, English, bilingual, Junqueira"
    core.language = "fa-AF"

    add_title_page(doc)
    add_about_page(doc, doc_model)
    add_toc_field(doc, doc_model)
    add_preface(doc, doc_model)
    for ch in doc_model.chapters:
        add_chapter(doc, ch)
    add_appendix_a(doc, doc_model)
    add_appendix_b(doc, doc_model)
    add_glossary(doc, doc_model)

    doc.save(out_path)
    d2 = Document(out_path)
    stats = dict(
        file=os.path.basename(out_path), path=os.path.abspath(out_path),
        bytes=os.path.getsize(out_path),
        paragraphs=len(d2.paragraphs), tables=len(d2.tables),
        sections=len(d2.sections),
        styles=len([s for s in d2.styles]),
        seconds=round(time.time() - t0, 1),
    )
    if verbose:
        print(stats)
    return stats


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        design.BOOK_DIR, "dist", "histology-dari-en.docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out)
