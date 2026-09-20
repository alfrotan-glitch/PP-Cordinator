#!/usr/bin/env python3
"""
Phase 0/1 — Intake: extract the original manuscript DOCX into a structured
Markdown working file, preserving document order, headings (detected from
run size + bold), tables, callouts, lists and the multilingual answer keys.

The original DOCX is never modified. Output: project/manuscript/parts/00_extracted.md
"""
import re
import sys
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SRC = sys.argv[1] if len(sys.argv) > 1 else \
    'کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'project/manuscript/parts/00_extracted.md'


def p_text(p):
    return ''.join(n.text or '' for n in p.iter(W + 't'))


def p_runs(p):
    """Return [(text, bold, size)] preserving run order."""
    out = []
    for r in p.iter(W + 'r'):
        txt = ''.join(t.text or '' for t in r.iter(W + 't'))
        if not txt:
            continue
        rPr = r.find(W + 'rPr')
        bold = False
        size = None
        if rPr is not None:
            b = rPr.find(W + 'b')
            bold = b is not None and b.get(W + 'val', '1') not in ('0', 'false')
            sz = rPr.find(W + 'sz')
            if sz is not None:
                size = int(sz.get(W + 'val'))
        out.append((txt, bold, size))
    return out


def p_meta(p):
    runs = p_runs(p)
    sizes = {s for _, _, s in runs if s}
    bold_only = bool(runs) and all(b for _, b, _ in runs)
    return runs, sizes, bold_only


CALL = [
    (re.compile(r'^مفهوم ساده$'), 'definition', 'مفهوم ساده'),
    (re.compile(r'^مثال از دایکندی(.*)$'), 'example', None),
    (re.compile(r'^⭐'), 'tip', None),
    (re.compile(r'^🔴'), 'key', None),
    (re.compile(r'^❌'), 'wrong', None),
    (re.compile(r'^✅'), 'right', None),
    (re.compile(r'^Sample Answer'), 'answer-en', None),
    (re.compile(r'^جواب مدل'), 'answer', None),
    (re.compile(r'^جواب‌های طلایی'), 'heading', None),
    (re.compile(r'^چک‌لیست'), 'checklist', None),
    (re.compile(r'^(نمونه|فرمول طلایی|اصل طلایی|ساختار طلایی|هفت کلمه طلایی)'),
     'key', None),
]

LIST_BULLET = re.compile(r'^[•▪]\s*')
LIST_NUM = re.compile(r'^[۰-۹]+[\.\)]\s*')


def md_escape(t):
    return t.replace('|', '\\|').strip()


def emit_table(el, lines):
    rows = []
    for tr in el.findall(W + 'tr'):
        cells = []
        for tc in tr.findall(W + 'tc'):
            cells.append(' '.join(p_text(p) for p in tc.findall(W + 'p')).strip())
        rows.append(cells)
    if not rows:
        return
    ncol = max(len(r) for r in rows)
    rows = [r + [''] * (ncol - len(r)) for r in rows]
    lines.append('<!-- table -->')
    lines.append('| ' + ' | '.join(md_escape(c) for c in rows[0]) + ' |')
    lines.append('|' + '---|' * ncol)
    for r in rows[1:]:
        lines.append('| ' + ' | '.join(md_escape(c) for c in r) + ' |')
    lines.append('')
    lines.append('<!-- /table -->')


def main():
    tree = ET.parse('word/document.xml') if SRC.endswith('.docx') and False else None
    import zipfile
    with zipfile.ZipFile(SRC) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    body = root.find(W + 'body')

    lines = []
    title_done = False
    for el in body:
        tag = el.tag.replace(W, '')
        if tag == 'tbl':
            emit_table(el, lines)
            continue
        if tag != 'p':
            continue
        runs, sizes, bold_only = p_meta(el)
        txt = p_text(el).strip()
        if not txt:
            continue
        maxsz = max(sizes) if sizes else 0

        # ---- structural headings detected from run size -------------
        if maxsz >= 34:
            lines.append('')
            lines.append('# ' + txt)
            lines.append('')
            continue
        if maxsz == 27 and bold_only:
            lines.append('')
            lines.append('## ' + txt)
            lines.append('')
            continue
        if maxsz >= 30:
            lines.append('')
            lines.append('@@ ' + txt)          # front-matter / title lines
            lines.append('')
            continue
        if maxsz == 26:
            lines.append('@@ ' + txt)
            continue
        if txt == 'فهرست مطالب':
            lines.append('<!-- TOC-PLACEHOLDER -->')
            continue

        # ---- callouts / labelled blocks -----------------------------
        kind = None
        for rx, k, _ in CALL:
            if rx.match(txt):
                kind = k
                break
        if kind and len(txt) < 120:
            label = txt
            if kind == 'definition':
                lines.append('')
                lines.append('::: concept')
                lines.append('')
                continue
            if kind == 'example':
                lines.append('')
                lines.append('::: example ' + (txt if txt != 'مثال از دایکندی' else ''))
                lines.append('')
                continue
            if kind in ('tip', 'key', 'checklist'):
                lines.append('')
                lines.append('> **' + label + '**')
                continue
            if kind in ('wrong', 'right'):
                lines.append('- ' + label)
                continue
            if kind in ('answer', 'answer-en'):
                lines.append('')
                lines.append('**' + label + '**')
                continue
            if kind == 'heading':
                lines.append('')
                lines.append('### ' + label)
                lines.append('')
                continue

        # ---- lists ---------------------------------------------------
        if LIST_BULLET.match(txt):
            lines.append('- ' + LIST_BULLET.sub('', txt))
            continue
        if LIST_NUM.match(txt) and len(txt) < 400:
            lines.append(LIST_NUM.sub('- ', txt, count=1))
            continue
        if txt in ('↓', '↑'):
            lines.append('')
            lines.append('`' + txt + '`')
            lines.append('')
            continue

        lines.append(txt)
        lines.append('')

    # collapse >2 blank lines
    out = []
    blank = 0
    for ln in lines:
        if ln.strip() == '':
            blank += 1
            if blank > 2:
                continue
        else:
            blank = 0
        out.append(ln)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print(f'wrote {OUT}: {len(out)} lines')


if __name__ == '__main__':
    main()
