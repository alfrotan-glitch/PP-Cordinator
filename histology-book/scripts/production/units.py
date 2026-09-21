# -*- coding: utf-8 -*-
"""
units.py — the professional book structure: title page, copyright page, table of
contents, preface, chapters (with front-of-chapter treatment and chapter review) and
the four appendices.

Every unit is a *page block group*: an optional opener plus a list of (block id, html)
chunks, so the layout engine can control page breaks, keep-with-next and table chunking.
Only layout is decided here; all wording comes from the frozen manuscript, except the
publishing details on the title/copyright pages and the navigational labels (chapter /
topic / appendix labels and the table of contents), which describe the edition itself.
"""
from __future__ import annotations

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmodel as bm
import design
import render_html as rh

BOOK_DIR = design.BOOK_DIR
BODY_H = design.BODY_BOTTOM - design.BODY_TOP
BODY_W = design.PAGE_W - design.M_INNER - design.M_OUTER

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa_num(n) -> str:
    return str(n).translate(FA_DIGITS)


def ch_id(n: int) -> str:
    return f"ch-{n:02d}"


def tp_id(number: str) -> str:
    return "tp-" + number.replace(".", "-")


class Unit:
    """A sequence of blocks that flow into pages, optionally with an opener."""

    def __init__(self, key: str, meta: dict | None = None, head: str = ""):
        self.key = key
        self.meta = meta or {}
        self.head = head
        self.chunks: list[tuple[str, str]] = []
        self.pages: list[int] = []

    # ---- construction helpers
    def add_blocks(self, blocks: list, prefix: str | None = None) -> None:
        prefix = prefix or self.key
        for i, blk in enumerate(blocks):
            bid = f"{prefix}-b{i}"
            html = rh.block_html(blk, bid=bid)
            if html:
                self.chunks.append((bid, html))

    def add_html(self, bid: str, html: str) -> None:
        self.chunks.append((bid, html))

    def measure_ok(self, html: str) -> float:
        return rh.measure_height(html)


# ------------------------------------------------------------ title & imprint

def title_unit() -> Unit:
    u = Unit("title", meta=dict(furniture=False, fixed=True))
    u.head = f"""
<div class="title-page">
  <p class="tp-kicker">مرجعِ معیار — Reference standard</p>
  <p class="tp-kicker-en" dir="ltr">{rh.esc(design.REFERENCE_LINE)}</p>
  <h1 class="book-title">{design.TITLE_FA}</h1>
  <p class="book-title-en" dir="ltr">{design.TITLE_EN}</p>
  <div class="title-rule"></div>
  <p class="book-sub">{design.SUBTITLE_FA}</p>
  <p class="book-sub-en" dir="ltr">{design.SUBTITLE_EN}</p>
  <p class="tp-scope">{design.AUDIENCE_LINE}</p>
  <p class="tp-badges">۲۳ فصل · ۱۰۸ مبحث · ۱۳ بخشِ ثابت در هر مبحث · واژه‌نامهٔ ۶۹۰ اصطلاح</p>
  <p class="tp-edition">{design.EDITION_LINE}</p>
</div>
"""
    return u


def copyright_unit() -> Unit:
    u = Unit("copyright", meta=dict(furniture=False, fixed=True))
    u.head = f"""
<div class="copyright-page">
  <h2 class="copyright-head">دربارهٔ این نسخه — About this edition</h2>
  <p class="copyright-line"><b>کتاب:</b> {design.TITLE_FA} — {design.TITLE_EN}</p>
  <p class="copyright-line"><b>زبان:</b> دوزبانه — دری (افغانستان) + English</p>
  <p class="copyright-line"><b>مرجعِ معیار:</b> {design.REFERENCE_LINE}</p>
  <p class="copyright-line"><b>سطح:</b> {design.AUDIENCE_LINE}</p>
  <p class="copyright-line"><b>ساختار:</b> ۲۳ فصل · ۱۰۸ مبحث · هر مبحث در ۱۳ بخشِ ثابت
     (تعریف، طبقه‌بندی، ساختمان، حجرات، وظیفه، رابطهٔ ساختمان–وظیفه، نمای هستولوژیک، تشخیص،
     مقایسه، همبستگی بالینی، نکاتِ امتحانی، جدولِ خلاصه، پرسش و پاسخ).</p>
  <p class="copyright-line"><b>ماهیتِ اثر:</b> این کتاب یک اثرِ آموزشیِ مستقل است؛ نه ترجمه، نه
     نقلِ متنِ مرجع و نه بازنویسیِ نزدیک به آن. مبنای محتوا تجزیه و تحلیلِ مستقلِ مطالبِ
     مرجعِ معیار و مقادیرِ متعارفِ هستولوژی است.</p>
  <p class="copyright-line"><b>اصطلاح‌شناسی:</b> نام‌های بین‌المللیِ طبی (اندوتلیوم، ساینوسویید،
     ترومبوسیت، کیموتراپی) به شکلِ رایجِ بین‌المللی و نام‌های تثبیت‌شدهٔ دری (کبد، کلیه) به شکلِ
     معیارِ آموزشیِ افغانستان آمده‌اند؛ اتصالاتِ حجروی به نامِ بین‌المللی
     (Tight junction / Zonula occludens، Adherens junction / Zonula adherens، Gap junction)
     و کاربوهایدریت به همین شکل ثبت شده‌اند. واژه‌نامهٔ کامل در پیوستِ ج آمده است.</p>
  <p class="copyright-line"><b>واحدها:</b> اندازه‌ها به میکرومتر (µm)، نانومتر (nm)، میلی‌متر (mm)
     و میلی‌لیتر (mL) و دما به درجهٔ سلسیوس (°C) است، مگر خلافش گفته شود.</p>
  <p class="copyright-note">این کتاب برای آموزش و مرورِ امتحانی تهیه شده است و جایگزینِ مرجعِ
     اصلی یا تصمیمِ بالینی نیست.</p>
</div>
"""
    return u


# --------------------------------------------------------------------- TOC

def toc_unit(page_map: dict, back_entries: list[tuple[str, str]], doc) -> Unit:
    u = Unit("toc", meta=dict(furniture=True, running="toc"))
    rows = ['<div class="toc-page">',
            '<h1 class="toc-head" id="toc-head">فهرست مطالب</h1>',
            '<p class="toc-head-en" dir="ltr">Contents</p>',
            '<p class="toc-note">شماره‌های این فهرست، شمارهٔ صفحهٔ همین چاپ‌اند.</p>',
            '<table class="toc"><tbody>']
    for ch in doc.chapters:
        page = page_map.get(ch_id(ch.number), "")
        rows.append(f'<tr class="ch" id="toc-{ch_id(ch.number)}">'
                    f'<td class="toc-label">{rh.esc(ch.label_fa)}</td>'
                    f'<td class="toc-num" dir="ltr">{page}</td></tr>')
        for t in ch.topics:
            tp = page_map.get(tp_id(t.number), "")
            rows.append('<tr class="tp">'
                        f'<td class="toc-label"><a href="#{tp_id(t.number)}" id="toc-{tp_id(t.number)}">'
                        f'{rh.esc(t.number)} {rh.esc(t.fa_title)}</a></td>'
                        f'<td class="toc-num">{tp}</td></tr>')
    for label, key in back_entries:
        page = page_map.get(key, "")
        rows.append(f'<tr class="ch" id="toc-{key}">'
                    f'<td class="toc-label">{rh.esc(label)}</td>'
                    f'<td class="toc-num" dir="ltr">{page}</td></tr>')
    rows.append("</tbody></table></div>")
    u.add_html("toc-body", "".join(rows))
    return u


# ----------------------------------------------------------------- preface

def preface_unit(doc) -> Unit:
    """The preface / study guide (00-front-matter.md): part title + flowing sections."""
    u = Unit("preface", meta=dict(furniture=True, running="front"))
    blocks = list(doc.front)
    head_done = 0
    idx = 0
    for blk in blocks:
        if blk.kind == "heading" and blk.level == 1 and head_done < 2:
            head_done += 1
            if head_done == 1:
                u.head = ('<div class="part-title">'
                          f'<h1 class="part-title-fa" id="preface">{rh.esc(blk.text)}</h1>')
            else:
                u.head += f'<p class="part-title-en" dir="ltr">{rh.esc(blk.text)}</p></div>'
            continue
        idx += 1
        if blk.kind == "heading" and blk.level == 2:
            bid = f"preface-h-{idx}"
            u.chunks.append((bid, f'<h2 class="front-head" id="{bid}">'
                                  f'{rh.spans_html(blk.spans[0])}</h2>'))
            continue
        bid = f"preface-b-{idx}"
        html = rh.block_html(blk, bid=bid)
        if html:
            u.chunks.append((bid, html))
    return u


# ----------------------------------------------------------------- chapters

def chapter_unit(ch: "bm.Chapter") -> Unit:
    u = Unit(ch_id(ch.number), meta=dict(furniture=True, chapter=ch.number,
                                         chapter_title=ch.fa_title))
    u.head = (f'<div class="chapter-open" id="{ch_id(ch.number)}">'
              f'<p class="chapter-kicker">فصل {fa_num(ch.number)}</p>'
              f'<h1 class="chapter-title">{rh.esc(ch.fa_title)}</h1>'
              f'<p class="chapter-title-en" dir="ltr">Chapter {ch.number} — {rh.esc(ch.en_title)}</p>'
              '<div class="chapter-rule"></div></div>')
    u.add_blocks(ch.blocks, f"{ch_id(ch.number)}-front")
    for t in ch.topics:
        opener = (f'<div class="topic-open" id="{tp_id(t.number)}">'
                  f'<p class="topic-kicker">مبحث {rh.esc(t.number)}</p>'
                  f'<h1 class="topic-title">{rh.esc(t.fa_title)}</h1>'
                  + (f'<p class="topic-title-en" dir="ltr">{rh.esc(t.en_title)}</p>' if t.en_title else "")
                  + "</div>")
        u.add_html(tp_id(t.number), opener)
        u.add_blocks(t.blocks, tp_id(t.number))
    u.add_blocks(ch.review, f"{ch_id(ch.number)}-review")
    return u


# --------------------------------------------------------------- appendices

def appendix_a_unit(doc) -> Unit:
    u = Unit("bk-sa", meta=dict(furniture=True, running="appendix-a",
                                running_text="پیوستِ الف — پرسش‌های مروریِ فصل‌ها"))
    u.head = ('<div class="back-open" id="bk-sa">'
              '<h1 class="back-title">پیوستِ الف — پرسش‌های مروریِ فصل‌ها</h1>'
              '<p class="back-title-en" dir="ltr">Appendix A — Chapter Self-Assessment '
              '(Questions &amp; Answers)</p>'
              '<p class="back-note">برای هر فصل، پرسش‌های مروری و پاسخ‌های کوتاهِ آن. پاسخ‌ها را '
              'پس از حلِ پرسش‌ها ببینید.</p></div>')
    for ch in doc.chapters:
        label = (f'<p class="apx-chapter-label" id="apx-a-{ch.number}">فصل {fa_num(ch.number)} — '
                 f'{rh.esc(ch.fa_title)}</p>')
        u.add_html(f"apx-a-{ch.number}", label)
        for i, blk in enumerate(ch.sa):
            bid = f"apx-a-{ch.number}-{i}"
            if blk.kind == "heading" and blk.level == 2 and blk.text.startswith(bm.CHAPTER_SA_HEAD):
                u.add_html(bid, f'<h2 class="apx-head" id="{bid}">'
                                f'{rh.spans_html(blk.spans[0])}</h2>')
                continue
            html = rh.block_html(blk, bid=bid)
            if html:
                u.add_html(bid, html)
    return u


def appendix_b_unit(doc) -> Unit:
    u = Unit("bk-audit", meta=dict(furniture=True, running="appendix-b",
                                   running_text="پیوستِ ب — ممیزیِ انطباق با مرجع"))
    u.head = ('<div class="back-open" id="bk-audit">'
              '<h1 class="back-title">پیوستِ ب — ممیزیِ انطباق با مرجع</h1>'
              '<p class="back-title-en" dir="ltr">Appendix B — Reference Alignment Records '
              '(Junqueira’s Basic Histology, 17th ed.)</p>'
              '<p class="back-note">برای هر فصل، دوازده بررسیِ انطباقِ محتوا با مرجعِ معیار و '
              'موردهای مقدارِ معیارِ آن ثبت شده است. این پیوست سندِ کیفیتِ کتاب است و بخشی از '
              'متنِ درسی نیست.</p></div>')
    for ch in doc.chapters:
        for i, blk in enumerate(ch.audit):
            bid = f"apx-b-{ch.number}-{i}"
            if blk.kind == "heading" and blk.level == 1:
                u.add_html(bid, f'<h2 class="apx-audit-title" id="audit-{ch.number}">'
                                f'{rh.spans_html(blk.spans[0])}</h2>')
                continue
            if blk.kind == "heading" and blk.level == 2 and blk.text.startswith(bm.AUDIT_HEAD):
                u.add_html(bid, f'<h3 class="apx-audit-head" id="{bid}">'
                                f'{rh.spans_html(blk.spans[0])}</h3>')
                continue
            html = rh.block_html(blk, bid=bid)
            if html:
                u.add_html(bid, html)
    return u


# ---------------------------------------------------------------- glossary

def glossary_unit(row_limit: int | None = None, max_rows: int | None = None) -> Unit:
    u = Unit("bk-glossary", meta=dict(furniture=True, running="appendix-c",
                                      running_text="پیوستِ ج — واژه‌نامهٔ اصطلاح‌ها"))
    u.head = ('<div class="back-open" id="bk-glossary">'
              '<h1 class="back-title">پیوستِ ج — واژه‌نامهٔ اصطلاح‌ها</h1>'
              '<p class="back-title-en" dir="ltr">Appendix C — Terminology Glossary '
              '(Afghan Dari · English · Latin)</p>'
              '<p class="back-note">شکلِ معیاریِ هر اصطلاح در کتاب و برابرِ انگلیسی/لاتینِ آن؛ '
              'ستونِ آخر نخستین فصلی است که اصطلاح در آن آمده است. اصطلاح‌ها بر پایهٔ الفبای '
              'دری چیده شده‌اند.</p></div>')
    data = glossary_rows()
    if max_rows:
        data = data[:max_rows]
    per_chunk = row_limit or 30

    def table(chunk, first: bool) -> str:
        head = ('<table class="glossary">'
                '<colgroup><col style="width:30%"><col style="width:39%">'
                '<col style="width:22%"><col style="width:9%"></colgroup>'
                '<thead><tr><th>اصطلاح (دری)</th><th>English</th><th>Latin / مخفف</th>'
                '<th>فصل</th></tr></thead><tbody>')
        rows = []
        for dari, eng, lat, chp in chunk:
            rows.append(f'<tr><td class="fa">{rh.esc(dari)}</td><td class="en">{rh.esc(eng)}</td>'
                        f'<td class="en">{rh.esc(lat)}</td><td class="en">{rh.esc(chp)}</td></tr>')
        return head + "".join(rows) + "</tbody></table>"

    chunks = [data[i:i + per_chunk] for i in range(0, len(data), per_chunk)]
    for i, chunk in enumerate(chunks):
        u.add_html(f"glossary-{i}", table(chunk, i == 0))
    return u


def glossary_rows() -> list[tuple[str, str, str, str]]:
    path = os.path.join(BOOK_DIR, "glossary", "terminology-glossary.csv")
    rows = list(csv.reader(open(path, encoding="utf-8")))
    I = {h: i for i, h in enumerate(rows[0])}
    data, seen = [], set()
    for r in rows[1:]:
        dari, eng = r[I["dari_term"]].strip(), r[I["english_term"]].strip()
        lat, abbr = r[I["latin_term"]].strip(), r[I["abbreviation"]].strip()
        chp = r[I["first_appearance"]].strip()
        if not dari or dari in seen:
            continue
        seen.add(dari)
        data.append((dari, eng, lat or abbr, chp))
    data.sort(key=lambda x: x[0])
    return data


# ------------------------------------------------------------------- index

def index_unit(entries) -> Unit:
    u = Unit("bk-index", meta=dict(furniture=True, running="appendix-d",
                                   running_text="پیوستِ د — نمایهٔ اصطلاح‌ها"))
    u.head = ('<div class="back-open" id="bk-index">'
              '<h1 class="back-title">پیوستِ د — نمایهٔ اصطلاح‌ها</h1>'
              '<p class="back-title-en" dir="ltr">Appendix D — Index</p>'
              '<p class="back-note">شماره‌ها، شمارهٔ صفحهٔ همین چاپ‌اند؛ اصطلاح‌های انگلیسی '
              'برای جست‌وجوی نامِ بین‌المللی آمده‌اند.</p></div>')
    rows = ['<table class="index"><colgroup><col style="width:5%"><col style="width:95%">'
            '</colgroup><tbody>']
    for letter, items in entries:
        rows.append(f'<tr><td class="idx-letter">{rh.esc(letter)}</td><td class="idx-body">')
        rows.append(" · ".join(f'<span class="idx-term">{rh.esc(t)}</span> '
                               f'<span class="idx-pages">{rh.esc(p)}</span>' for t, p in items))
        rows.append("</td></tr>")
    rows.append("</tbody></table>")
    u.add_html("index-table", "".join(rows))
    return u
