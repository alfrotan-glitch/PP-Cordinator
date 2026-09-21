# -*- coding: utf-8 -*-
"""
epub.py — EPUB 3 (reflowable) production renderer.

Layout decisions specific to the digital edition:
  * right-to-left page progression (an RTL book opens from the right)
  * embedded Dari/Latin fonts with per-glyph fallback, no fixed line breaks
  * semantic navigation (nav.xhtml) + NCX for older readers
  * one XHTML document per chapter (fast, memory-friendly reading)
  * a typeset cover image produced from the print title page
The text itself is the same frozen manuscript as the print editions.
"""
from __future__ import annotations

import datetime as _dt
import html as _html
import os
import re
import sys
import uuid
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bookmodel as bm
import design
import render_html as rh
import units as U

EPUB_FONTS = [
    ("Vazirmatn", "Vazirmatn-Regular.ttf", "400", "normal"),
    ("Vazirmatn", "Vazirmatn-Bold.ttf", "700", "normal"),
    ("Source Serif 4", "SourceSerif4-Regular.ttf", "400", "normal"),
    ("Source Serif 4", "SourceSerif4-Semibold.ttf", "600", "normal"),
    ("Source Serif 4", "SourceSerif4-Italic.ttf", "400", "italic"),
    ("DejaVu Sans", "DejaVuSans.ttf", "400", "normal"),
    ("Noto Emoji", "NotoEmoji-Regular.ttf", "400", "normal"),
    ("Noto Sans Math", "NotoSansMath-Regular.ttf", "400", "normal"),
]

CSS_EXTRA = """
body { padding: 0 4%; }
h1.chapter-title { margin-top: 1.2em; }
div.chapter-open { border-bottom: 0.6pt solid #0f5d6b; padding-bottom: 0.6em; margin-bottom: 1em; }
div.topic-open { margin-top: 1.6em; border-top: 0.4pt solid #e4eaec; padding-top: 0.8em; }
table { font-size: 0.82em; }
div.callout { break-inside: avoid; }
h2, h3 { break-after: avoid; }
p.li { break-inside: avoid; }
"""


def xhtml_page(title: str, body: str, extra_class: str = "") -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"
      xml:lang="fa-AF" lang="fa-AF" dir="rtl">
<head>
  <meta charset="utf-8"/>
  <title>{_html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="../css/style.css"/>
</head>
<body class="{extra_class}" dir="rtl">
{body}
</body>
</html>
"""


def span_xhtml(spans) -> str:
    out = []
    for s in spans:
        t = _html.escape(s.text, quote=False)
        if s.code:
            out.append(f"<code>{t}</code>")
            continue
        if s.bold:
            t = f"<strong>{t}</strong>"
        if s.italic:
            t = f"<em>{t}</em>"
        if getattr(s, "sup", False):
            t = f"<sup>{t}</sup>"
        elif getattr(s, "sub", False):
            t = f"<sub>{t}</sub>"
        out.append(t)
    return "".join(out)


def list_xhtml(blk) -> str:
    items = [it for it in blk.items if isinstance(it, tuple)]
    if not items:
        return ""
    base = min(i for i, _, _ in items)
    out = ['<div class="listbox">']
    counters: dict[int, int] = {}
    for indent, kind, body in items:
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
        out.append(f'<p class="li" style="margin-right:{lvl}em">'
                   f'<b class="mk" style="color:#0f5d6b">{marker}</b> '
                   f'<span class="tx">{span_xhtml(bm.parse_inline(txt))}</span></p>')
    out.append("</div>")
    return "".join(out)


def callout_xhtml(blk) -> str:
    inner = []
    buf: list[str] = []

    def flush():
        if buf:
            inner.append("<ul class='citems' style='list-style:none;padding-right:1em'>")
            for body in buf:
                inner.append(f"<li>{span_xhtml(bm.parse_inline(body))}</li>")
            inner.append("</ul>")
            buf.clear()

    for item in [i for i in blk.items if isinstance(i, str) and i.strip()]:
        if re.match(r"^\(\d+\)\s*", item.strip()):
            buf.append(item.strip())
            continue
        flush()
        inner.append(f"<p>{span_xhtml(bm.parse_inline(item))}</p>")
    flush()
    cls = "callout " + (getattr(blk, "role", "") or "")
    return f'<div class="{cls.strip()}">' + "".join(inner) + "</div>"


def table_xhtml(blk) -> str:
    ncols = max(len(blk.header or []), max((len(r) for r in blk.rows), default=0))
    if not ncols:
        return ""
    widths = rh._column_widths(blk, ncols)
    out = ['<table class="data">', "<colgroup>",
           "".join(f'<col style="width:{w:.1f}%"/>' for w in widths), "</colgroup>"]
    if blk.header:
        out.append("<thead><tr>")
        for i in range(ncols):
            cell = blk.header[i] if i < len(blk.header) else ""
            txt = bm.plain_text(cell)
            d = ' dir="ltr"' if bm.lang_of(txt) == "en" else ""
            out.append(f"<th{d}>{span_xhtml(bm.parse_inline(cell)) or '&#160;'}</th>")
        out.append("</tr></thead>")
    out.append("<tbody>")
    for row in blk.rows:
        out.append("<tr>")
        for i in range(ncols):
            cell = row[i] if i < len(row) else ""
            txt = bm.plain_text(cell)
            d = ' dir="ltr"' if bm.lang_of(txt) == "en" else ""
            out.append(f"<td{d}>{span_xhtml(bm.parse_inline(cell)) or '&#160;'}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def block_xhtml(blk) -> str:
    role = getattr(blk, "role", "")
    if blk.kind == "heading":
        if blk.level >= 3:
            return f"<h3>{span_xhtml(blk.spans[0])}</h3>"
        if role in ("audit-title", "review-title"):
            return f'<h2 class="apx-audit-title">{span_xhtml(blk.spans[0])}</h2>'
        if role in ("record-head", "audit-head"):
            return f'<h3 class="apx-audit-head">{span_xhtml(blk.spans[0])}</h3>'
        cls = "hy" if "HIGH-YIELD" in blk.text else ("sa" if role == "chapter-sa-head" else "")
        return f'<h2 class="{cls}">{span_xhtml(blk.spans[0])}</h2>'
    if blk.kind == "para":
        spans = [sp for ps in blk.spans for sp in ps]
        if role == "body-en":
            return f'<p class="en" dir="ltr">{span_xhtml(spans)}</p>'
        cls = {"lead": "lead", "record-note": "record-note"}.get(role, "fa")
        return f'<p class="{cls}">{span_xhtml(spans)}</p>'
    if blk.kind == "list":
        return list_xhtml(blk)
    if blk.kind == "table":
        return table_xhtml(blk)
    if blk.kind == "callout":
        return callout_xhtml(blk)
    if blk.kind == "diagram":
        return f'<pre class="diagram" dir="ltr">{_html.escape(blk.text)}</pre>'
    if blk.kind == "rule":
        return '<hr/>'
    return ""


def render_nav(items) -> str:
    lis = []
    for level, label, href in items:
        lis.append(f'<li><a href="{href}">{_html.escape(label)}</a></li>')
    return ("<nav epub:type='toc' id='toc' dir='rtl'><h1>فهرست مطالب</h1><ol>"
            + "".join(lis) + "</ol></nav>")


def build(out_path: str, cover_pdf: str | None = None, verbose: bool = True) -> dict:
    import time
    t0 = time.time()
    doc = bm.load_document()
    book_id = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "pp-cordinator/histology-book"))
    today = _dt.date.today().isoformat()

    files: dict[str, bytes] = {}
    nav_items = []

    # ---- cover image from the print title page
    cover_name = None
    if cover_pdf and os.path.exists(cover_pdf):
        try:
            import pymupdf
            src = pymupdf.open(cover_pdf)
            pix = src[0].get_pixmap(dpi=150)
            pix.save("/tmp/_cover.jpg", jpg_quality=88)
            data = open("/tmp/_cover.jpg", "rb").read()
            files["OEBPS/images/cover.jpg"] = data
            cover_name = "images/cover.jpg"
            src.close()
        except Exception as exc:                             # pragma: no cover
            if verbose:
                print("  cover generation skipped:", exc)

    # ---- fonts
    for _fam, fname, _w, _s in EPUB_FONTS:
        path = os.path.join(design.FONT_DIR, fname)
        if os.path.exists(path):
            files[f"OEBPS/fonts/{fname}"] = open(path, "rb").read()

    # ---- css
    files["OEBPS/css/style.css"] = rh.css_for_measure().replace(
        "url(", "url(../fonts/").encode("utf-8") + CSS_EXTRA.encode("utf-8")

    # ---- front matter
    title_body = f"""
<section epub:type="titlepage" class="title-page" dir="rtl">
  <p class="tp-kicker">مرجعِ معیار — Reference standard</p>
  <p class="tp-kicker-en" dir="ltr">{_html.escape(design.REFERENCE_LINE)}</p>
  <h1 class="book-title">{design.TITLE_FA}</h1>
  <p class="book-title-en" dir="ltr">{design.TITLE_EN}</p>
  <hr/>
  <p class="book-sub">{design.SUBTITLE_FA}</p>
  <p class="book-sub-en" dir="ltr">{design.SUBTITLE_EN}</p>
  <p class="tp-scope">{design.AUDIENCE_LINE}</p>
  <p class="tp-badges">۲۳ فصل · ۱۰۸ مبحث · ۱۳ بخشِ ثابت در هر مبحث · واژه‌نامهٔ ۶۹۰ اصطلاح</p>
  <p class="tp-edition">{design.EDITION_LINE}</p>
</section>"""
    if cover_name:
        title_body = ('<div style="text-align:center;margin-bottom:1.5em">'
                      f'<img src="../{cover_name}" alt="{design.TITLE_FA}" '
                      'style="max-width:100%;height:auto"/></div>') + title_body
    files["OEBPS/text/titlepage.xhtml"] = xhtml_page("هیستولوژی بنیادی", title_body).encode("utf-8")

    about_lines = [
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
                         "نامِ بین‌المللی (Tight junction، Adherens junction، Gap junction) و "
                         "کاربوهایدریت به همین شکل ثبت شده‌اند."),
        ("واژه‌نامه", "پیوستِ ج واژه‌نامهٔ ۶۹۰ اصطلاحِ کتاب را بر پایهٔ الفبای دری دارد."),
    ]
    about_body = ['<section epub:type="copyright-page" class="copyright-page" dir="rtl">',
                  "<h2>دربارهٔ این نسخه — About this edition</h2>"]
    for head, body in about_lines:
        about_body.append(f'<p class="copyright-line"><b>{head}:</b> {body}</p>')
    about_body.append('<p class="copyright-note">این کتاب برای آموزش و مرورِ امتحانی تهیه شده '
                      "است و جایگزینِ مرجعِ اصلی یا تصمیمِ بالینی نیست.</p></section>")
    files["OEBPS/text/about.xhtml"] = xhtml_page("دربارهٔ این نسخه", "".join(about_body)).encode("utf-8")

    # ---- preface
    pre = ['<section class="preface" dir="rtl">']
    head_done = 0
    for blk in doc.front:
        if blk.kind == "heading" and blk.level == 1 and head_done < 2:
            head_done += 1
            cls = "part-title-fa" if head_done == 1 else "part-title-en"
            d = "" if head_done == 1 else ' dir="ltr"'
            pre.append(f'<{ "h1" if head_done==1 else "p" } class="{cls}"{d}>'
                       f'{_html.escape(blk.text)}</{"h1" if head_done==1 else "p"}>')
            continue
        if blk.kind == "heading" and blk.level == 2:
            pre.append(f'<h2 class="front-head">{_html.escape(blk.text)}</h2>')
            continue
        pre.append(block_xhtml(blk))
    pre.append("</section>")
    files["OEBPS/text/preface.xhtml"] = xhtml_page("پیش‌گفتار", "".join(pre)).encode("utf-8")
    nav_items.append((0, "پیش‌گفتار و راهنمای مطالعه", "preface.xhtml"))

    # ---- chapters
    for ch in doc.chapters:
        body = ['<section class="chapter" dir="rtl">',
                f'<div class="chapter-open" id="{U.ch_id(ch.number)}">',
                f'<p class="chapter-kicker">فصل {U.fa_num(ch.number)}</p>',
                f'<h1 class="chapter-title">{_html.escape(ch.fa_title)}</h1>',
                f'<p class="chapter-title-en" dir="ltr">Chapter {ch.number} — '
                f'{_html.escape(ch.en_title)}</p></div>']
        for blk in ch.blocks:
            body.append(block_xhtml(blk))
        for t in ch.topics:
            body.append(f'<div class="topic-open" id="{U.tp_id(t.number)}">')
            body.append(f'<p class="topic-kicker">مبحث {_html.escape(t.number)}</p>')
            body.append(f'<h1 class="topic-title">{_html.escape(t.fa_title)}</h1>')
            if t.en_title:
                body.append(f'<p class="topic-title-en" dir="ltr">{_html.escape(t.en_title)}</p>')
            body.append("</div>")
            for blk in t.blocks:
                body.append(block_xhtml(blk))
        for blk in ch.review:
            body.append(block_xhtml(blk))
        body.append("</section>")
        fname = f"ch{ch.number:02d}.xhtml"
        files[f"OEBPS/text/{fname}"] = xhtml_page(
            f"فصل {ch.number} — {ch.fa_title}", "".join(body)).encode("utf-8")
        nav_items.append((0, f"فصل {U.fa_num(ch.number)} — {ch.fa_title}", fname))
        for t in ch.topics:
            nav_items.append((1, f"{t.number} {t.fa_title}", fname))

    # ---- appendix A (self-assessment)
    sa = ['<section class="appendix" dir="rtl"><h1 class="back-title">پیوستِ الف — پرسش‌های '
          "مروریِ فصل‌ها</h1>",
          '<p class="back-title-en" dir="ltr">Appendix A — Chapter Self-Assessment</p>',
          '<p class="back-note">برای هر فصل، پرسش‌های مروری و پاسخ‌های کوتاهِ آن.</p>']
    for ch in doc.chapters:
        sa.append(f'<h2 class="apx-chapter-label">فصل {U.fa_num(ch.number)} — '
                  f'{_html.escape(ch.fa_title)}</h2>')
        for blk in ch.sa:
            sa.append(block_xhtml(blk))
    sa.append("</section>")
    files["OEBPS/text/appendix-a.xhtml"] = xhtml_page("پیوستِ الف", "".join(sa)).encode("utf-8")
    nav_items.append((0, "پیوستِ الف — پرسش‌های مروریِ فصل‌ها", "appendix-a.xhtml"))

    # ---- appendix B (reference alignment records)
    ab = ['<section class="appendix" dir="rtl"><h1 class="back-title">پیوستِ ب — ممیزیِ انطباق با '
          "مرجع</h1>",
          '<p class="back-title-en" dir="ltr">Appendix B — Reference Alignment Records</p>',
          '<p class="back-note">دوازده بررسیِ انطباقِ محتوا با مرجعِ معیار برای هر فصل؛ سندِ '
          "کیفیتِ کتاب، نه متنِ درسی.</p>"]
    for ch in doc.chapters:
        for blk in ch.audit:
            ab.append(block_xhtml(blk))
    ab.append("</section>")
    files["OEBPS/text/appendix-b.xhtml"] = xhtml_page("پیوستِ ب", "".join(ab)).encode("utf-8")
    nav_items.append((0, "پیوستِ ب — ممیزیِ انطباق با مرجع", "appendix-b.xhtml"))

    # ---- appendix C (glossary)
    gl = ['<section class="appendix" dir="rtl"><h1 class="back-title">پیوستِ ج — واژه‌نامهٔ '
          "اصطلاح‌ها</h1>",
          '<p class="back-title-en" dir="ltr">Appendix C — Terminology Glossary</p>',
          '<p class="back-note">شکلِ معیاریِ هر اصطلاح، برابرِ انگلیسی/لاتین و نخستین فصلِ '
          "کاربرد.</p>",
          '<table class="glossary"><thead><tr><th>اصطلاح (دری)</th><th>English</th>'
          "<th>Latin / مخفف</th><th>فصل</th></tr></thead><tbody>"]
    for dari, eng, lat, chp in U.glossary_rows():
        gl.append(f'<tr><td>{_html.escape(dari)}</td><td dir="ltr">{_html.escape(eng)}</td>'
                  f'<td dir="ltr">{_html.escape(lat)}</td><td dir="ltr">{_html.escape(chp)}</td></tr>')
    gl.append("</tbody></table></section>")
    files["OEBPS/text/appendix-c.xhtml"] = xhtml_page("پیوستِ ج", "".join(gl)).encode("utf-8")
    nav_items.append((0, "پیوستِ ج — واژه‌نامهٔ اصطلاح‌ها", "appendix-c.xhtml"))

    # ---- nav + ncx
    nav = ("<?xml version='1.0' encoding='utf-8'?>\n"
           '<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" '
           'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="fa-AF" dir="rtl">\n'
           "<head><meta charset='utf-8'/><title>فهرست مطالب</title>"
           "<link rel='stylesheet' type='text/css' href='css/style.css'/></head><body>"
           + render_nav([(lvl, label, f"text/{href}") for lvl, label, href in nav_items])
           + "</body></html>")
    files["OEBPS/nav.xhtml"] = nav.encode("utf-8")

    ncx_points = []
    for i, (lvl, label, href) in enumerate(nav_items, 1):
        ncx_points.append(f'<navPoint id="np{i}" playOrder="{i}"><navLabel><text>'
                          f"{_html.escape(label)}</text></navLabel>"
                          f'<content src="text/{href}"/></navPoint>')
    files["OEBPS/toc.ncx"] = ("<?xml version='1.0' encoding='utf-8'?>\n"
                              '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" '
                              'xml:lang="fa-AF"><head>'
                              f'<meta name="dtb:uid" content="{book_id}"/></head>'
                              f"<docTitle><text>{design.TITLE_FA}</text></docTitle>"
                              f"<navMap>{''.join(ncx_points)}</navMap></ncx>").encode("utf-8")

    # ---- package documents
    manifest = []
    for path in sorted(files):
        if path.startswith("OEBPS/fonts/"):
            props = ""
            media = "font/ttf"
        elif path.endswith(".css"):
            props, media = "", "text/css"
        elif path.endswith(".xhtml"):
            props = ' properties="nav"' if path.endswith("nav.xhtml") else ""
            media = "application/xhtml+xml"
        elif path.endswith(".ncx"):
            props, media = "", "application/x-dtbncx+xml"
        elif path.endswith(".jpg"):
            props, media = ' properties="cover-image"', "image/jpeg"
        else:
            props, media = "", "application/octet-stream"
        mid = path.split("/")[-1].replace(".", "_")
        manifest.append(f'<item id="{mid}" href="{path[6:]}" media-type="{media}"{props}/>')
    spine = ['<itemref idref="titlepage_xhtml"/>', '<itemref idref="about_xhtml"/>',
             '<itemref idref="nav_xhtml"/>', '<itemref idref="preface_xhtml"/>']
    for ch in doc.chapters:
        spine.append(f'<itemref idref="ch{ch.number:02d}_xhtml"/>')
    spine += ['<itemref idref="appendix-a_xhtml"/>', '<itemref idref="appendix-b_xhtml"/>',
              '<itemref idref="appendix-c_xhtml"/>']

    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid"
         xml:lang="fa-AF" dir="rtl">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_id}</dc:identifier>
    <dc:title>{design.TITLE_FA} — {design.TITLE_EN}</dc:title>
    <dc:creator>{design.AUTHOR}</dc:creator>
    <dc:language>fa-AF</dc:language>
    <dc:language>en</dc:language>
    <dc:date>{today}</dc:date>
    <dc:publisher>{design.PUBLISHER}</dc:publisher>
    <dc:description>دوزبانه (دری + English) — مرورِ امتحان‌محورِ هستولوژی بر پایهٔ Junqueira's Basic Histology, 17th ed.</dc:description>
    <dc:subject>Histology</dc:subject>
    <dc:subject>Medical education</dc:subject>
    <meta property="dcterms:modified">{_dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}</meta>
    <meta name="cover" content="cover_jpg"/>
  </metadata>
  <manifest>
    {chr(10).join(manifest)}
  </manifest>
  <spine toc="toc_ncx" page-progression-direction="rtl">
    {chr(10).join(spine)}
  </spine>
</package>"""
    files["OEBPS/content.opf"] = opf.encode("utf-8")

    # ---- write the container
    if os.path.exists(out_path):
        os.remove(out_path)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip",
                   compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0" encoding="utf-8"?>\n'
                   '<container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" '
                   'media-type="application/oebps-package+xml"/></rootfiles></container>')
        for path, data in sorted(files.items()):
            z.writestr(path, data)

    stats = dict(file=os.path.basename(out_path), path=os.path.abspath(out_path),
                 bytes=os.path.getsize(out_path), documents=len(files) + 1,
                 nav_items=len(nav_items), fonts=len([f for f in files if "/fonts/" in f]),
                 cover=bool(cover_name), seconds=round(time.time() - t0, 1))
    if verbose:
        print(stats)
    return stats


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        design.BOOK_DIR, "dist", "histology-dari-en.epub")
    cover = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        design.BOOK_DIR, "dist", "histology-dari-en.pdf")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build(out, cover)
