#!/usr/bin/env python3
"""
Shared manuscript model for the three output builders (DOCX / EPUB / HTML).

The manuscript is a plain-text (Markdown-like) source with a small, strictly
enforced markup vocabulary, so that the same file can be rendered identically
into Word, an EPUB package and a web edition.

Markup vocabulary
-----------------
    @part شناسه :: عنوان                 part title page
    #  عنوان                             top-level document (chapter / front matter)
    ## / ### / ####                      section, subsection, sub-subsection
    :::type عنوان                        callout box, closed by a line of :::
    - item                               bullet list
    1. item                              ordered list
    | a | b |                            table (first row = header)
    > text                               quotation (consecutive lines merge)
    >> step → step → step                process strip (framework / diagram)
    **bold**   *italic*                  inline emphasis
    ---                                  ignored separator
    %% note                              production note, never rendered
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / 'manuscript' / 'parts'
MASTER = ROOT / 'manuscript' / 'master.md'
GLOSSARY_CSV = ROOT / 'glossary' / 'terminology-glossary.csv'

ZWNJ = '\u200c'
ARROW = '\u2192'

# Callout types: a small, closed set. Each one has a fixed purpose in the book,
# so the reader learns the visual language once and is not distracted later.
CALLOUTS = {
    'story':   'داستان',
    'case':    'کیس کاری',
    'decision': 'نقطه تصمیم',
    'tool':    'ابزار کار',
    'note':    'نکته',
    'reflect': 'تأمل و تمرین',
    'warn':    'کجای کار می‌شکند',
    'key':     'درس کلیدی',
    'ethics':  'آزمون اخلاقی',
    'data':    'ارقام و شواهد',
}


@dataclass
class Block:
    kind: str                       # part|h1|h2|h3|h4|para|bullet|olist|table|callout|flow|quote
    text: str = ''
    level: int = 0
    items: list = field(default_factory=list)     # table rows / bullets / callout body
    lines: list = field(default_factory=list)     # continuation lines (indented)
    markers: list = field(default_factory=list)   # printed numbers of ordered items
    ctype: str = ''
    ctitle: str = ''
    number: str = ''                # heading number extracted for display

    def plain(self) -> str:
        return strip_markup(self.text)


# ------------------------------------------------------------------ inline ----

BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
ITAL_RE = re.compile(r'(?<!\*)\*([^*]+)\*(?!\*)')


def strip_markup(text: str) -> str:
    text = BOLD_RE.sub(r'\1', text)
    text = ITAL_RE.sub(r'\1', text)
    return text.replace('  ', ' ').strip()


def inline_runs(text: str):
    """Split inline markup into (chunk, bold, italic) runs."""
    out = []
    pos = 0
    pattern = re.compile(r'\*\*(.+?)\*\*|(?<!\*)\*([^*]+)\*(?!\*)')
    for m in pattern.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False, False))
        if m.group(1) is not None:
            out.append((m.group(1), True, False))
        else:
            out.append((m.group(2), False, True))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False, False))
    return out or [(text, False, False)]


def clean_inline(s: str) -> str:
    s = s.replace('\\|', '|')
    return re.sub(r'[ \t]+', ' ', s).strip()


def parse_table_row(line: str):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [clean_inline(c) for c in line.split('|')]


# ------------------------------------------------------------------- parse ----

def parse_files(paths):
    blocks = []
    for p in paths:
        blocks.extend(parse(p))
    return blocks


def parse(path: Path):
    lines = path.read_text(encoding='utf-8').split('\n')
    blocks = []
    stack = []          # open callouts: {'type','title','body'}
    last = []           # holder for the most recent block (for continuations)
    i = 0

    def push(block):
        if stack:
            stack[-1]['body'].append(block)
        else:
            blocks.append(block)
        last[:] = [block]

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()

        if not s or s == '---':
            i += 1
            continue
        if s.startswith('%%'):                      # production note
            i += 1
            continue

        # ---- continuation line: two leading spaces bind to the previous item
        if raw[:2] == '  ' and raw.strip() and last and not s.startswith('|'):
            lines_txt = raw.strip()
            if last[0].kind in ('bullet', 'olist') and last[0].items:
                last[0].items[-1] += '\n' + clean_inline(lines_txt)
            else:
                last[0].lines.append(clean_inline(lines_txt))
            i += 1
            continue

        # ---- part title page
        m = re.match(r'^@part\s+(\S+)\s*::\s*(.+)$', s)
        if m:
            push(Block('part', text=clean_inline(m.group(2)), number=clean_inline(m.group(1))))
            i += 1
            continue

        # ---- callout open / close
        if s.startswith(':::'):
            body = s[3:].strip()
            if body:
                parts = body.split(' ', 1)
                ctype = parts[0]
                ctitle = parts[1].strip() if len(parts) > 1 else CALLOUTS.get(ctype, ctype)
                stack.append({'type': ctype, 'title': ctitle, 'body': []})
            elif stack:
                c = stack.pop()
                blk = Block('callout', items=c['body'], ctype=c['type'], ctitle=c['title'])
                if stack:
                    stack[-1]['body'].append(blk)
                else:
                    blocks.append(blk)
            i += 1
            continue

        # ---- headings
        hm = re.match(r'^(#{1,4})\s+(.*)$', s)
        if hm:
            lvl = len(hm.group(1))
            txt = clean_inline(hm.group(2))
            push(Block({1: 'h1', 2: 'h2', 3: 'h3', 4: 'h4'}[lvl], text=txt, level=lvl))
            i += 1
            continue

        # ---- tables
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = parse_table_row(lines[i])
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in row if c):
                    rows.append(row)
                i += 1
            push(Block('table', items=rows))
            continue

        # ---- process strip
        if s.startswith('>> '):
            push(Block('flow', text=clean_inline(s[3:])))
            i += 1
            continue

        # ---- quotation
        if s.startswith('> '):
            buf = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                buf.append(lines[i].strip()[2:])
                i += 1
            push(Block('quote', text=clean_inline(' '.join(buf))))
            continue

        # ---- ordered list
        if re.match(r'^\d+\.\s', s):
            items, markers = [], []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                stripped = lines[i].strip()
                markers.append(re.match(r'^(\d+)\.', stripped).group(1))
                items.append(clean_inline(re.sub(r'^\d+\.\s', '', stripped)))
                i += 1
            push(Block('olist', items=items, markers=markers))
            continue

        # ---- bullet list
        if s.startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(clean_inline(lines[i].strip()[2:]))
                i += 1
            push(Block('bullet', items=items))
            continue

        push(Block('para', text=clean_inline(s)))
        i += 1

    if stack:
        raise SystemExit(f'unclosed callout in {path}')
    return blocks


# ------------------------------------------------------------------ helpers ---

def doc_kind(title: str) -> str:
    if title.startswith(('فصل ', 'بخش ')):
        return 'chapter'
    if title.startswith('پیوست '):
        return 'appendix'
    if title.startswith('واژه'):
        return 'glossary'
    if title.startswith(('درباره نویسنده', 'درباره این نسخه', 'یادداشت سرچشمه')):
        return 'backmatter'
    return 'frontmatter'


def navigation(blocks):
    """Build the part -> chapter -> section tree used by the EPUB nav and TOC."""
    tree = []
    part = None
    chapter = None
    for b in blocks:
        if b.kind == 'part':
            part = {'title': b.text, 'number': b.number, 'chapters': []}
            tree.append(part)
            chapter = None
        elif b.kind == 'h1':
            chapter = {'title': b.text, 'kind': doc_kind(b.text), 'sections': []}
            if part is not None:
                part['chapters'].append(chapter)
            else:
                tree.append(chapter)
        elif b.kind == 'h2' and chapter is not None:
            chapter['sections'].append(b.text)
    return tree


def split_documents(blocks):
    """One document per '# ' heading; the callout bodies stay attached."""
    docs, current = [], None
    for b in blocks:
        if b.kind == 'part':
            if current:
                docs.append(current)
            current = {'title': b.text, 'kind': 'part', 'number': b.number, 'blocks': [b]}
        elif b.kind == 'h1':
            if current:
                docs.append(current)
            current = {'title': b.text, 'kind': doc_kind(b.text), 'number': '',
                       'blocks': [b]}
        elif current is None:
            current = {'title': 'سرآغاز', 'kind': 'frontmatter', 'number': '', 'blocks': []}
            current['blocks'].append(b)
        else:
            current['blocks'].append(b)
    if current:
        docs.append(current)
    return docs


if __name__ == '__main__':
    from collections import Counter
    bl = parse(MASTER)
    print(Counter(b.kind for b in bl))
    for d in split_documents(bl):
        print(f"  [{d['kind']:11}] {d['title'][:70]}  ({len(d['blocks'])} blocks)")
