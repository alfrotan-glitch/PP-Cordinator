#!/usr/bin/env python3
"""
Shared manuscript model for the three output builders (DOCX / PDF / EPUB).

Parses the single-source master manuscript (project/manuscript/master.md) into a
flat list of typed blocks:

    Chapter, Section, Subsection, ExamQuestion, Para, Bullet, Table,
    Callout(type, title, body blocks), Flow (the ↓ process diagrams)
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / 'project/manuscript/master.md'
GLOSSARY_CSV = ROOT / 'project/glossary/terminology-glossary.csv'

ZWNJ = '\u200c'

# Print-safe typographic equivalents for emoji: the embedded text fonts (Vazir,
# Samim) have no emoji glyphs, and a printed medical book should not carry
# colour emoji anyway. Applied to every output so DOCX/PDF/EPUB match.
SYMBOL_MAP = {
    '\u2b50': '\u2605',   # star      -> black star
    '\U0001f534': '\u25cf',  # red circle -> black circle
    '\u2705': '\u2713',   # check mark
    '\u274c': '\u2717',   # cross mark
}


def sanitize(text: str) -> str:
    for src, dst in SYMBOL_MAP.items():
        text = text.replace(src, dst)
    return text


@dataclass
class Block:
    kind: str                  # chapter|section|subsection|examq|para|bullet|table|callout|flow
    text: str = ''
    level: int = 0
    items: list = field(default_factory=list)   # table rows / callout body / bullets
    ctype: str = ''            # callout type
    ctitle: str = ''


def clean_inline(s: str) -> str:
    s = s.replace('\\|', '|')
    return sanitize(re.sub(r'\s+', ' ', s).strip())


def parse_table_row(line: str):
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]
    return [clean_inline(c) for c in line.split('|')]


def parse(path: Path):
    blocks = []
    lines = path.read_text(encoding='utf-8').split('\n')
    i = 0
    callout_stack = []      # list of (ctype, ctitle, body_list)

    while i < len(lines):
        raw = lines[i]
        s = raw.strip()

        if not s or s in ('<!-- table -->', '<!-- /table -->'):
            i += 1
            continue

        # ---------------- callout open / close --------------------
        m = re.match(r'^:::\s*(\S+)?\s*(.*)$', s)
        if m and not s.startswith('::::'):
            if m.group(1):
                callout_stack.append({'type': m.group(1), 'title': m.group(2).strip(),
                                      'body': [], 'lists': []})
                i += 1
                continue
            else:
                if callout_stack:
                    c = callout_stack.pop()
                    blk = Block('callout', items=c['body'], ctype=c['type'],
                                ctitle=c['title'])
                    if callout_stack:
                        callout_stack[-1]['body'].append(blk)
                    else:
                        blocks.append(blk)
                i += 1
                continue

        # ---------------- headings ---------------------------------
        hm = re.match(r'^(#{1,4})\s+(.*)$', s)
        if hm:
            lvl, txt = len(hm.group(1)), clean_inline(hm.group(2))
            kind = {1: 'chapter', 2: 'section', 3: 'subsection', 4: 'examq'}[lvl]
            blk = Block(kind, text=txt, level=lvl)
            if kind == 'examq':
                blk.kind = 'examq'
            if callout_stack:
                callout_stack[-1]['body'].append(blk)
            else:
                blocks.append(blk)
            i += 1
            continue

        # ---------------- tables -----------------------------------
        if s.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = parse_table_row(lines[i])
                if not all(re.fullmatch(r':?-{2,}:?', c) for c in row if c):
                    rows.append(row)
                i += 1
            blk = Block('table', items=rows)
            if callout_stack:
                callout_stack[-1]['body'].append(blk)
            else:
                blocks.append(blk)
            continue

        # ---------------- process diagrams -------------------------
        if re.fullmatch(r'`[↓↑]`', s):
            blk = Block('flow', text=s[1])
            if callout_stack:
                callout_stack[-1]['body'].append(blk)
            else:
                blocks.append(blk)
            i += 1
            continue

        # ---------------- bullets ----------------------------------
        if s.startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                items.append(clean_inline(lines[i].strip()[2:]))
                i += 1
            blk = Block('bullet', items=items)
            if callout_stack:
                callout_stack[-1]['body'].append(blk)
            else:
                blocks.append(blk)
            continue

        # ---------------- horizontal rule / paragraph --------------
        if s == '---':
            i += 1
            continue
        blk = Block('para', text=clean_inline(s))
        if callout_stack:
            callout_stack[-1]['body'].append(blk)
        else:
            blocks.append(blk)
        i += 1

    return blocks


def inline_runs(text: str):
    """Split inline **bold** markup into (text, bold) runs."""
    out = []
    for part in re.split(r'(\*\*[^*]+\*\*)', text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            out.append((part[2:-2], True))
        else:
            out.append((part, False))
    return out


def toc_entries(blocks):
    out = []
    for b in blocks:
        if b.kind == 'chapter':
            out.append((1, b.text))
        elif b.kind == 'section':
            out.append((2, b.text))
    return out


if __name__ == '__main__':
    bl = parse(MASTER)
    from collections import Counter
    print(Counter(b.kind for b in bl))
    print('chapters:', [b.text for b in bl if b.kind == 'chapter'])
