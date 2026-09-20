#!/usr/bin/env python3
"""
HTML builder - one self-contained reading edition.

Everything (fonts, cover, styles, the reading script) is embedded in a single
file so it can be opened from a disk, a memory stick or a web server without any
supporting folder. Layout: a slim navigation column on wide screens, a plain
single column on phones; dark mode follows the reader's system setting.
"""
from __future__ import annotations

import base64
import html
import re
from pathlib import Path

import mgmtgen
from mgmtgen import ROOT, inline_runs, split_documents

OUT = ROOT / 'output' / 'مدیریت_نسخهٔ_وب.html'
FONTS = ROOT / 'assets/fonts'
COVER = ROOT / 'assets/cover-web.jpg'

LANG = 'fa-AF'
TITLE = 'مدیریت؛ مبانی و مهارت‌های اساسی مدیریت'
SUBTITLE = 'Management: The Essentials — Afghan Dari Professional Edition'
PUBLISHER = 'نشر سرچشمه'
STRAP = ('بیست فصل · سی کیس کاری · بستهٔ چهارده‌گانهٔ ابزارها · صد و پنجاه پرسش تمرینی · '
         'واژه‌نامهٔ کامل اصطلاحات')

CALLOUT_TITLE = {
    'story': 'داستان', 'case': 'کیس کاری', 'decision': 'نقطهٔ تصمیم', 'tool': 'ابزار کار',
    'note': 'نکته', 'reflect': 'تأمل و تمرین', 'warn': 'کجای کار می‌شکند',
    'key': 'درس کلیدی', 'ethics': 'آزمون اخلاقی', 'data': 'ارقام و شواهد',
}

LATIN = re.compile(r'[A-Za-z][A-Za-z0-9\.\-\+/#:]*')


def esc(t: str) -> str:
    return html.escape(t, quote=False)


def with_latin(text: str) -> str:
    out, last = [], 0
    for m in LATIN.finditer(text):
        out.append(esc(text[last:m.start()]))
        out.append(f'<span lang="en" dir="ltr">{esc(m.group(0))}</span>')
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


def slug(i: int) -> str:
    return f'sec-{i}'


def css() -> str:
    def b64(name):
        return base64.b64encode((FONTS / name).read_bytes()).decode()

    return f'''
@font-face {{ font-family: "DariBook"; font-weight: 400; font-display: swap;
  src: url(data:font/woff2;base64,{b64('Vazir.woff2')}) format("woff2"); }}
@font-face {{ font-family: "DariBook"; font-weight: 700; font-display: swap;
  src: url(data:font/woff2;base64,{b64('Samim.woff2')}) format("woff2"); }}
@font-face {{ font-family: "DariDisplay"; font-weight: 700; font-display: swap;
  src: url(data:font/woff2;base64,{b64('Samim.woff2')}) format("woff2"); }}
@font-face {{ font-family: "BookSymbols"; font-display: swap;
  src: url(data:font/woff2;base64,{b64('BookSymbols.woff2')}) format("woff2"); }}

:root {{
  --ink: #1b2430; --ink-soft: #4a5361; --paper: #ffffff; --paper-soft: #f7f6f2;
  --rule: #e0dfd7; --accent: #14584f; --accent-soft: #eaf2f0; --navy: #1d3358;
  --measure: 40rem; --sidebar: 21rem;
}}
@media (prefers-color-scheme: dark) {{
  :root {{ --ink: #e9e7e2; --ink-soft: #b6bac2; --paper: #14161a; --paper-soft: #1c1f25;
           --rule: #363b43; --accent: #77c9b4; --accent-soft: #1e2a2c; --navy: #cfdff2; }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0; background: var(--paper); color: var(--ink);
  font-family: "DariBook", "BookSymbols", "Vazirmatn", "Noto Naskh Arabic", Tahoma, serif;
  font-size: clamp(16.5px, 1.02vw + 12px, 18.5px); line-height: 2.02;
  text-align: justify; text-justify: inter-word; hyphens: none;
  -webkit-text-size-adjust: 100%;
}}
.layout {{ display: grid; grid-template-columns: var(--sidebar) minmax(0, 1fr);
  gap: 3.2rem; max-width: 1180px; margin: 0 auto; padding: 0 1.6rem; }}
nav.toc {{
  position: sticky; top: 0; align-self: start; max-height: 100vh; overflow-y: auto;
  padding: 1.6rem 0 3rem; font-size: 0.86rem; line-height: 1.75; border-left: 1px solid
  var(--rule); padding-left: 1.4rem;
}}
nav.toc h2 {{ font-size: 0.95rem; color: var(--ink-soft); font-weight: 700; margin: 0 0 0.6rem; }}
nav.toc ol {{ list-style: none; margin: 0; padding: 0; }}
nav.toc li {{ margin: 0.16rem 0; }}
nav.toc a {{ color: var(--ink); text-decoration: none; }}
nav.toc a:hover {{ color: var(--accent); }}
nav.toc li.part > a {{ color: var(--accent); font-weight: 700; display: block;
  margin-top: 0.9rem; }}
nav.toc li.lvl2 {{ padding-right: 1.1rem; color: var(--ink-soft); font-size: 0.97em; }}
nav.toc li.part > ol {{ margin: 0.2rem 0 0.5rem; padding-right: 1.1rem; }}
nav.toc li.part > ol > li {{ margin: 0.12rem 0; }}
nav.toc .mcq {{ margin: 0 0 1.1em; }}
nav.toc .mcq p.q {{ font-weight: 700; margin: 0 0 0.25em; }}
.toc-tree .qnum, .qnum {{ color: var(--accent); }}
.mcq ol.choices {{ list-style: none; margin: 0; padding: 0 1.1rem 0 0; }}
.mcq ol.choices li {{ margin: 0.18em 0; line-height: 1.5; }}
.mcq .opt-letter {{ font-weight: 700; color: var(--ink-soft); }}
aside.box h3 {{ font-size: 0.95rem; margin: 0 0 0.4rem; color: var(--accent); }}
main {{ padding: 2.4rem 0 5rem; max-width: var(--measure); }}
.cover {{ display: block; width: min(100%, 22rem); margin: 0 auto 2.4rem;
  border-radius: 6px; box-shadow: 0 12px 40px rgba(0,0,0,.22); }}
h1, h2, h3, h4 {{ font-family: "DariDisplay", "DariBook", serif; line-height: 1.55;
  text-align: right; break-after: avoid; }}
h1 {{ font-size: 1.72rem; color: var(--navy); margin: 3.2rem 0 1.1rem;
  border-bottom: 2px solid var(--accent); padding-bottom: 0.45rem; }}
h1:first-of-type {{ margin-top: 0.6rem; }}
h2 {{ font-size: 1.24rem; color: var(--accent); margin: 2.1rem 0 0.6rem; }}
h3 {{ font-size: 1.06rem; color: var(--ink-soft); margin: 1.6rem 0 0.4rem; }}
h4 {{ font-size: 1rem; color: var(--navy); margin: 1.2rem 0 0.3rem; }}
p {{ margin: 0.62em 0; }}
a {{ color: var(--accent); }}
ul, ol {{ margin: 0.6em 1.5em 0.8em 0; padding: 0; }}
li {{ margin: 0.3em 0; }}
blockquote {{ margin: 1em 0; padding: 0.2em 1.1em 0.2em 0; border-right: 3px solid var(--rule);
  color: var(--ink-soft); }}
table {{ width: 100%; border-collapse: collapse; margin: 1.2em 0; font-size: 0.88rem;
  display: block; overflow-x: auto; }}
th, td {{ border: 1px solid var(--rule); padding: 0.42em 0.6em; text-align: right;
  vertical-align: top; }}
th {{ background: var(--accent-soft); color: var(--navy); }}
tbody tr:nth-child(even) {{ background: var(--paper-soft); }}
.keytable {{ font-size: 0.82rem; }}
aside.box {{ margin: 1.4em 0; padding: 0.95em 1.15em 1.05em; background: var(--paper-soft);
  border: 1px solid var(--rule); border-right: 4px solid var(--accent); border-radius: 4px; }}
aside.box > h4 {{ margin: 0 0 0.5em; color: var(--accent); font-size: 1.02rem; }}
aside.box.case {{ border-right-color: var(--navy); }}
aside.box.warn {{ border-right-color: #a8443a; }}
aside.box.warn > h4 {{ color: #a8443a; }}
aside.box.decision {{ border-right-color: #8a6d1f; }}
aside.box.decision > h4 {{ color: #7a6018; }}
aside.box.tool {{ background: color-mix(in srgb, var(--accent-soft) 60%, var(--paper)); }}
p.flow {{ text-align: center; font-weight: 700; color: var(--accent); line-height: 2.1;
  margin: 1.4em 0; }}
.footer {{ color: var(--ink-soft); font-size: 0.86rem; border-top: 1px solid var(--rule);
  margin-top: 3rem; padding-top: 1rem; }}
.titlepage {{ text-align: center; margin-bottom: 3rem; }}
.titlepage h1 {{ text-align: center; border: none; margin-bottom: 0.3rem; }}
.titlepage p {{ text-align: center; }}
.progress {{ position: fixed; top: 0; right: 0; height: 3px; background: var(--accent);
  width: 0; z-index: 10; }}
@media (max-width: 900px) {{
  .layout {{ grid-template-columns: minmax(0, 1fr); gap: 0; }}
  nav.toc {{ position: static; max-height: none; border-left: none; padding: 1.2rem 0 0;
    border-bottom: 1px solid var(--rule); }}
  main {{ padding-top: 1.4rem; }}
}}
@media print {{
  nav.toc, .progress {{ display: none; }}
  .layout {{ display: block; max-width: none; }}
  body {{ font-size: 10.5pt; }}
  h1 {{ page-break-before: always; }}
  aside.box, table, tr {{ page-break-inside: avoid; }}
}}
'''


CHOICE_RE = re.compile(r'^(الف|ب|ج|د)\)\s?(.*)$')


def is_mcq_item(item: str) -> bool:
    lines = item.split('\n')
    return len([ln for ln in lines if CHOICE_RE.match(ln.strip())]) == 4 and len(lines) >= 5


def mcq_html(item: str, marker: str) -> str:
    lines = [ln.strip() for ln in item.split('\n')]
    choices = ''.join(
        f'<li><span class="opt-letter">{esc(m.group(1))})</span> {inline(m.group(2))}</li>'
        for m in (CHOICE_RE.match(ln) for ln in lines[1:]) if m)
    num = f'<span class="qnum">{esc(marker)}.</span> ' if marker else ''
    return (f'<div class="mcq" role="group"><p class="q">{num}{inline(lines[0])}</p>'
            f'<ol class="choices">{choices}</ol></div>')


def render_blocks(blocks, counter, nested=False, out=None):
    if out is None:
        out = []
    for b in blocks:
        if b.kind == 'h1':
            counter[0] += 1
            out.append(f'<h1 id="{slug(counter[0])}">{inline(b.text)}</h1>')
        elif b.kind == 'h2':
            out.append(f'<h2>{inline(b.text)}</h2>')
        elif b.kind == 'h3':
            out.append(f'<h3>{inline(b.text)}</h3>')
        elif b.kind == 'h4':
            out.append(f'<h4>{inline(b.text)}</h4>')
        elif b.kind == 'para':
            extra = ''.join(' ' + inline(x) for x in b.lines)
            out.append(f'<p>{inline(b.text)}{extra}</p>')
        elif b.kind == 'bullet':
            items = ''.join('<li>' + '<br/>'.join(inline(x) for x in i.split('\n')) + '</li>'
                            for i in b.items)
            out.append(f'<ul>{items}</ul>')
        elif b.kind == 'olist':
            if len(b.items) == 1 and is_mcq_item(b.items[0]):
                out.append(mcq_html(b.items[0], b.markers[0] if b.markers else ''))
                continue
            items = ''
            for n, i in enumerate(b.items):
                marker = b.markers[n] if n < len(b.markers) else str(n + 1)
                body = '<br/>'.join(inline(x) for x in i.split('\n'))
                items += f'<li value="{esc(marker)}">{body}</li>'
            out.append(f'<ol>{items}</ol>')
        elif b.kind == 'quote':
            out.append(f'<blockquote><p>{inline(b.text)}</p></blockquote>')
        elif b.kind == 'flow':
            out.append(f'<p class="flow">{inline(b.text)}</p>')
        elif b.kind == 'table':
            rows = [r for r in b.items if r]
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            cls = ' class="keytable"' if (ncols == 2 and rows[0][0] == 'پرسش') else ''
            head = ''.join(f'<th scope="col">{inline(c)}</th>' for c in rows[0])
            body = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>'
                           for r in rows[1:])
            out.append(f'<table{cls}><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>')
        elif b.kind == 'callout':
            label = CALLOUT_TITLE.get(b.ctype, b.ctype)
            title = f'{label} — {b.ctitle}' if b.ctitle else label
            out.append(f'<aside class="box {esc(b.ctype)}"><h3>{inline(title)}</h3>')
            render_blocks(b.items, counter, nested=True, out=out)
            out.append('</aside>')
    return out


def main():
    blocks = mgmtgen.parse(mgmtgen.MASTER)
    docs = split_documents(blocks)

    counter = [0]
    body_parts = []
    toc_items = []
    toc_groups = []          # two-level sidebar: part -> its chapters
    current = None
    for doc in docs:
        if doc['kind'] == 'part':
            counter[0] += 1
            if current:
                toc_groups.append(current)
            current = {'part': f'<li class="part"><a href="#{slug(counter[0])}">'
                               f'{esc(doc["title"])}</a>', 'chapters': []}
            body_parts.append(f'<h1 id="{slug(counter[0])}">{esc(doc["title"])}</h1>')
            continue
        start = counter[0] + 1
        if doc['kind'] == 'appendix' and current:
            toc_groups.append(current)
            current = {'part': None, 'chapters': []}
        body_parts.extend(render_blocks(doc['blocks'], counter))
        entry = f'<li class="lvl2"><a href="#{slug(start)}">{esc(doc["title"])}</a></li>'
        if current is None:
            current = {'part': None, 'chapters': []}
        current['chapters'].append(entry)
    if current:
        toc_groups.append(current)
    for g in toc_groups:
        inner = f'<ol>{"".join(g["chapters"])}</ol>' if g['chapters'] else ''
        if g['part']:
            toc_items.append(g['part'] + inner + '</li>')
        else:
            toc_items.extend(g['chapters'])

    cover_b64 = base64.b64encode(COVER.read_bytes()).decode()
    head_html = f'''<div class="titlepage">
<img class="cover" src="data:image/jpeg;base64,{cover_b64}" alt="جلد کتاب {esc(TITLE)}"/>
<h1>{esc(TITLE)}</h1>
<p style="color:var(--accent)">{esc(SUBTITLE)}</p>
<p>{esc(STRAP)}</p>
<p>{esc(PUBLISHER)} — 1405 / 2026</p>
</div>'''

    doc = f'''<!DOCTYPE html>
<html lang="{LANG}" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(STRAP)}"/>
<meta name="author" content="{esc(PUBLISHER)}"/>
<style>{css()}</style>
</head>
<body>
<div class="progress" id="progress"></div>
<div class="layout">
<nav class="toc" aria-label="فهرست مطالب">
<h2>فهرست مطالب</h2>
<ol class="toc-tree">{''.join(toc_items)}</ol>
</nav>
<main>
{head_html}
{''.join(body_parts)}
<p class="footer">{esc(PUBLISHER)} — {esc(TITLE)} — نسخهٔ وب. متن این نسخه با نسخهٔ ورقی
و نسخهٔ الکترونیکی یکی است.</p>
</main>
</div>
<script>
(function () {{
  var bar = document.getElementById('progress');
  function update() {{
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  }}
  document.addEventListener('scroll', update, {{passive: true}});
  update();
}})();
</script>
</body>
</html>'''
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(doc, encoding='utf-8')
    print(f'HTML -> {OUT}  ({OUT.stat().st_size / 1024:.0f} KB, '
          f'{len(blocks)} blocks, {counter[0]} top-level sections)')


if __name__ == '__main__':
    main()
