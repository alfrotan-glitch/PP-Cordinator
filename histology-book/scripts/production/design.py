# -*- coding: utf-8 -*-
"""
design.py — the book's design system (single source of truth for all renderers).

Page geometry, typographic scale, colour palette, font stacks and the CSS used by the
PDF renderer.  Layout values are in PDF points (1 pt = 1/72 inch).
"""
from __future__ import annotations

import os

BOOK_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT_DIR_PDF = None      # set by fonts.configure(): ZWNJ-safe copies
FONT_DIR = os.path.join(BOOK_DIR, "assets", "fonts")

# ----------------------------------------------------------------- geometry (A4)
PAGE_W, PAGE_H = 595.276, 841.890          # A4

M_INNER = 64.0      # gutter margin (binding side)
M_OUTER = 46.0      # outer margin
M_TOP = 62.0
M_BOTTOM = 58.0

HEADER_H = 30.0     # running-head band
FOOTER_H = 40.0     # folio band (the story engine may overshoot the block by one line)

BODY_TOP = M_TOP + HEADER_H
BODY_BOTTOM = PAGE_H - M_BOTTOM - FOOTER_H

# ----------------------------------------------------------------- palette
INK = "#1c1c1c"            # body text
INK_SOFT = "#33383a"       # English / secondary text
GREY = "#6d7a80"           # running heads, captions
RULE = "#c2ced2"
RULE_SOFT = "#e4eaec"
ACCENT = "#0f5d6b"         # deep teal — headings, rules, folio
ACCENT_SOFT = "#e8f1f2"    # table header tint
WARM = "#faf5e9"           # high-yield / callout background
WARM_RULE = "#c8a94b"      # muted gold
APPENDIX_INK = "#4d575b"

# ----------------------------------------------------------------- type scale
S = dict(
    chapter_kicker=10.5,
    chapter_title=23.0,
    chapter_title_en=12.5,
    topic_kicker=9.5,
    topic_title=14.5,
    topic_title_en=9.0,
    section_head=11.4,
    subhead=10.4,
    body=10.4,
    body_en=9.2,
    lead=11.0,
    list=10.2,
    table=8.3,
    table_head=8.4,
    callout=10.0,
    appendix=7.6,
    appendix_head=9.6,
    caption=8.0,
    folio=9.0,
    running=7.4,
)
LH = dict(body=1.66, body_en=1.52, list=1.60, table=1.36, callout=1.58,
          appendix=1.42, chapter_title=1.25, topic_title=1.35, section_head=1.30)

# ----------------------------------------------------------------- fonts
# Order matters: the first family that covers a glyph is used (per-glyph fallback).
FONT_STACK_DARI = "Vazirmatn, Source Serif, DejaVu Sans, Noto Emoji, Noto Sans Math"
FONT_STACK_LATIN = "Source Serif, Vazirmatn, DejaVu Sans, Noto Emoji, Noto Sans Math"
FONT_STACK_SYM = "DejaVu Sans, Noto Emoji, Noto Sans Math"

FONTS = {
    "Vazirmatn": [
        os.path.join(FONT_DIR, "Vazirmatn-Regular.ttf"),
        os.path.join(FONT_DIR, "Vazirmatn-Medium.ttf"),
        os.path.join(FONT_DIR, "Vazirmatn-SemiBold.ttf"),
        os.path.join(FONT_DIR, "Vazirmatn-Bold.ttf"),
    ],
    "Source Serif": [
        os.path.join(FONT_DIR, "SourceSerif4-Regular.ttf"),
        os.path.join(FONT_DIR, "SourceSerif4-Semibold.ttf"),
        os.path.join(FONT_DIR, "SourceSerif4-Italic.ttf"),
    ],
    "DejaVu Sans": [os.path.join(FONT_DIR, "DejaVuSans.ttf")],
    "Noto Emoji": [os.path.join(FONT_DIR, "NotoEmoji-Regular.ttf")],
    "Noto Sans Math": [os.path.join(FONT_DIR, "NotoSansMath-Regular.ttf")],
}

# ----------------------------------------------------------------- book metadata
TITLE_FA = "هیستولوژی بنیادی"
TITLE_EN = "Essential Histology"
SUBTITLE_FA = "مرورِ آموزشی، فشرده و امتحان‌محور — دری + English"
SUBTITLE_EN = "A Bilingual (Afghan Dari + English) High-Yield Review"
REFERENCE_LINE = "Junqueira's Basic Histology: Text and Atlas, 17th Edition — Anthony L. Mescher"
AUDIENCE_LINE = "برای دانشجویانِ طب، دندان‌پزشکی و علومِ صحی و داوطلبانِ امتحان‌های تخصصیِ هستولوژی"
EDITION_LINE = "نسخهٔ نهایی — ۲۰۲۶"
RUNNING_TITLE = "هیستولوژی بنیادی — دری/English"
AUTHOR = "هیستولوژی بنیادی — متنِ آموزشی دوزبانه"      # PDF metadata author field
PUBLISHER = "انتشارِ مستقل — Independent edition"       # PDF metadata publisher field


def rgb(hexstr: str) -> tuple[float, float, float]:
    """'#rrggbb' -> PyMuPDF colour tuple."""
    h = hexstr.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ----------------------------------------------------------------- CSS
def css(embed: str = "pdf") -> str:
    return f"""
/* ---------------------------------------------------------------- base */
html {{ direction: rtl; }}
body {{
  font-family: {FONT_STACK_DARI};
  font-size: {S['body']}pt; line-height: {LH['body']};
  color: {INK}; direction: rtl; text-align: justify; hyphens: none;
}}
p {{ margin: 0 0 5pt 0; }}
b, strong {{ font-weight: 700; }}
i, em {{ font-style: italic; }}
code {{ font-family: {FONT_STACK_LATIN}; font-size: 0.96em; }}

/* ---------------------------------------------------------------- headings */
h1.chapter-title {{
  font-size: {S['chapter_title']}pt; line-height: {LH['chapter_title']};
  font-weight: 700; color: {ACCENT}; text-align: right; margin: 0 0 3pt 0;
}}
p.chapter-kicker {{
  font-size: {S['chapter_kicker']}pt; letter-spacing: 0.4pt; color: {WARM_RULE};
  font-weight: 700; margin: 0 0 3pt 0; text-align: right;
}}
p.chapter-title-en {{
  font-family: {FONT_STACK_LATIN}; font-size: {S['chapter_title_en']}pt; color: {GREY};
  direction: ltr; text-align: right; margin: 0 0 8pt 0; font-weight: 400;
}}
div.chapter-rule {{ border-top: 1pt solid {ACCENT}; width: 34%; margin: 0 0 12pt 0; }}
div.chapter-open {{ margin: 0 0 10pt 0; }}
div.topic-open {{ margin: 0 0 7pt 0; }}
p.topic-kicker {{ font-size: {S['topic_kicker']}pt; color: {WARM_RULE}; font-weight: 700;
  letter-spacing: 0.3pt; margin: 0 0 1pt 0; }}
h1.topic-title {{
  font-size: {S['topic_title']}pt; line-height: {LH['topic_title']};
  font-weight: 700; color: {INK}; margin: 0 0 1pt 0; text-align: right;
}}
p.topic-title-en {{
  font-family: {FONT_STACK_LATIN}; font-size: {S['topic_title_en']}pt; color: {GREY};
  direction: ltr; text-align: right; margin: 0 0 4pt 0;
}}
h2 {{
  font-size: {S['section_head']}pt; line-height: {LH['section_head']};
  font-weight: 700; color: {ACCENT}; margin: 12pt 0 4pt 0; text-align: right;
}}
h2.hy {{
  background: {WARM}; border-right: 2.4pt solid {WARM_RULE};
  padding: 2.6pt 6pt 2.6pt 6pt; color: #7a5c12; margin: 13pt 0 5pt 0;
}}
h2.sa {{ border-top: 0.5pt solid {RULE_SOFT}; padding-top: 5pt; }}
h3 {{
  font-size: {S['subhead']}pt; font-weight: 700; color: {INK};
  margin: 8pt 0 3pt 0;
}}

/* ---------------------------------------------------------------- language blocks */
p.fa {{ direction: rtl; text-align: justify; }}
p.en {{
  font-family: {FONT_STACK_LATIN}; direction: ltr; text-align: left;
  font-size: {S['body_en']}pt; line-height: {LH['body_en']};
  color: {INK_SOFT}; margin: 1pt 0 6pt 0;
}}
p.lead {{ font-weight: 700; font-size: {S['lead']}pt; margin: 3pt 0 4pt 0; }}
p.record-note {{ font-size: {S['appendix']}pt; color: {APPENDIX_INK}; line-height: {LH['appendix']}; }}

/* ---------------------------------------------------------------- lists */
div.listbox {{ margin: 3pt 0 6pt 0; }}
p.li {{
  margin: 0 0 2.6pt 0; padding-right: 14pt; text-indent: -14pt;
  line-height: {LH['list']}; font-size: {S['list']}pt; text-align: justify;
}}
p.li b.mk {{ color: {ACCENT}; font-weight: 700; }}
div.listbox p.li span.tx {{ }}

/* ---------------------------------------------------------------- tables */
table {{ border-collapse: collapse; width: 100%; margin: 4pt 0 7pt 0; }}
th, td {{
  border: 0.4pt solid {RULE}; padding: 2.6pt 3.6pt; vertical-align: top;
  font-size: {S['table']}pt; line-height: {LH['table']}; text-align: right; direction: rtl;
}}
th {{ background: {ACCENT_SOFT}; font-weight: 700; color: {INK}; font-size: {S['table_head']}pt; }}
td.en, th.en {{ font-family: {FONT_STACK_LATIN}; direction: ltr; text-align: left; }}
table.appendix th, table.appendix td {{
  font-size: {S['appendix']}pt; line-height: {LH['appendix']}; color: {APPENDIX_INK};
  border-color: {RULE_SOFT}; padding: 2.2pt 3.2pt;
}}
table.appendix th {{ background: #f2f5f6; color: {APPENDIX_INK}; }}
table.glossary th {{ background: {ACCENT_SOFT}; }}
table.glossary td {{ font-size: 8.1pt; line-height: 1.42; }}
table.index td {{ border: none; padding: 1.6pt 0; font-size: 8.6pt; line-height: 1.5; }}
td.idx-letter {{ font-weight: 700; color: {ACCENT}; width: 24pt; }}
span.idx-term {{ color: {INK}; font-weight: 700; }}
span.idx-pages {{ color: {ACCENT}; }}

/* ---------------------------------------------------------------- tables of contents */
table.toc {{ border: none; width: 100%; margin: 8pt 0 0 0; }}
table.toc td {{ border: none; padding: 1.5pt 0; font-size: 9.4pt; color: {INK}; }}
table.toc td.toc-label {{ color: {INK}; }}
table.toc tr.ch td {{ font-weight: 700; color: {ACCENT}; padding-top: 6.5pt; font-size: 9.9pt; }}
table.toc tr.tp td {{ padding-right: 16pt; font-size: 8.9pt; color: {INK_SOFT}; }}
td.toc-label {{ text-align: right; }}
td.toc-num {{ text-align: left; direction: ltr; font-family: {FONT_STACK_LATIN};
  width: 38pt; color: {GREY}; font-size: 8.8pt; }}
h1.toc-head {{ font-size: 19pt; color: {ACCENT}; margin: 0 0 1pt 0; }}
p.toc-head-en {{ font-family: {FONT_STACK_LATIN}; font-size: 11pt; color: {GREY};
  direction: ltr; text-align: right; margin: 0 0 2pt 0; }}
p.toc-note {{ font-size: 8.4pt; color: {GREY}; margin: 0 0 6pt 0; }}

/* ---------------------------------------------------------------- callouts */
div.callout {{
  background: {WARM}; border-right: 2.4pt solid {WARM_RULE};
  border-left: 0.4pt solid {WARM_RULE};
  padding: 6pt 9pt 6pt 9pt; margin: 5pt 0 8pt 0;
}}
div.callout.aim {{ background: #eef6f7; border-right-color: {ACCENT}; border-left-color: {ACCENT}; }}
div.callout p {{ margin: 0 0 3pt 0; font-size: {S['callout']}pt; line-height: {LH['callout']}; }}
div.callout p:last-child {{ margin-bottom: 0; }}
ul.citems {{ margin: 2pt 0 2pt 0; padding: 0 14pt 0 0; }}
li.ci {{ margin: 0 0 2pt 0; font-size: {S['callout']}pt; line-height: {LH['callout']};
  list-style-type: none; text-align: right; }}

/* ---------------------------------------------------------------- rules / diagram */
hr {{ border: none; border-top: 0.5pt solid {RULE_SOFT}; margin: 7pt 0 7pt 0; }}
pre.diagram {{
  font-family: {FONT_STACK_LATIN}; font-size: {S['table']}pt; direction: ltr; text-align: left;
  background: #f5f7f8; border: 0.4pt solid {RULE_SOFT}; padding: 6pt 8pt; margin: 5pt 0 8pt 0;
  line-height: 1.45; white-space: pre;
}}

/* ---------------------------------------------------------------- front matter */
h1.book-title {{ font-size: 30pt; font-weight: 700; color: {ACCENT}; text-align: center;
  margin: 0 0 4pt 0; }}
p.book-title-en {{ font-family: {FONT_STACK_LATIN}; font-size: 17pt; color: {GREY};
  direction: ltr; text-align: center; margin: 0 0 10pt 0; }}
sup, sub {{ font-size: 0.66em; line-height: 0; }}
sup {{ vertical-align: 0.42em; }}
sub {{ vertical-align: -0.22em; }}
p.book-sub {{ font-size: 11.5pt; color: {INK}; text-align: center; margin: 0 0 3pt 0; }}
p.book-sub-en {{ font-family: {FONT_STACK_LATIN}; font-size: 10pt; color: {GREY}; direction: ltr;
  text-align: center; margin: 0 0 14pt 0; }}
div.title-rule {{ border-top: 1pt solid {ACCENT}; width: 38%; margin: 12pt auto 14pt auto; }}
p.tp-kicker {{ font-size: 8.4pt; color: {GREY}; text-align: center; margin: 0 0 1pt 0; }}
p.tp-kicker-en {{ font-family: {FONT_STACK_LATIN}; font-size: 8.4pt; color: {GREY}; direction: ltr;
  text-align: center; margin: 0 0 70pt 0; }}
p.tp-scope {{ font-size: 9.6pt; color: {INK_SOFT}; text-align: center; margin: 70pt 0 5pt 0; }}
p.tp-badges {{ font-size: 9.2pt; color: {ACCENT}; text-align: center; margin: 0 0 14pt 0; }}
p.tp-edition {{ font-size: 9.2pt; color: {GREY}; text-align: center; margin: 0; }}
div.title-page {{ margin: 0; }}
div.copyright-page {{ margin: 26pt 0 0 0; }}
h2.copyright-head {{ font-size: 13pt; color: {ACCENT}; margin: 0 0 9pt 0; }}
p.copyright-line {{ font-size: 9.2pt; line-height: 1.62; margin: 0 0 5pt 0; color: {INK_SOFT}; }}
p.copyright-note {{ font-size: 8.6pt; color: {GREY}; margin: 12pt 0 0 0; border-top: 0.5pt solid
  {RULE_SOFT}; padding-top: 6pt; }}
div.part-title {{ margin: 0 0 12pt 0; }}
h1.part-title-fa {{ font-size: 19pt; color: {ACCENT}; margin: 0 0 2pt 0; }}
p.part-title-en {{ font-family: {FONT_STACK_LATIN}; font-size: 11pt; color: {GREY}; direction: ltr;
  text-align: right; margin: 0 0 4pt 0; }}
h2.front-head {{ font-size: 12pt; color: {ACCENT}; margin: 12pt 0 4pt 0; }}

/* ---------------------------------------------------------------- back matter */
div.back-open {{ margin: 0 0 12pt 0; }}
h1.back-title {{ font-size: 19pt; color: {ACCENT}; margin: 0 0 2pt 0; }}
p.back-title-en {{ font-family: {FONT_STACK_LATIN}; font-size: 10.5pt; color: {GREY};
  direction: ltr; text-align: right; margin: 0 0 4pt 0; }}
p.back-note {{ font-size: 9pt; color: {INK_SOFT}; margin: 0 0 4pt 0; }}
p.apx-chapter-label {{ font-size: 12.5pt; font-weight: 700; color: {ACCENT};
  margin: 14pt 0 4pt 0; }}
h2.apx-head {{ font-size: 10pt; color: {INK}; margin: 2pt 0 4pt 0; font-weight: 700; }}
h2.apx-audit-title {{ font-size: 13pt; color: #7a5c12; margin: 16pt 0 3pt 0; }}
h3.apx-audit-head {{ font-size: 9.6pt; color: {INK}; margin: 0 0 5pt 0; }}
"""
