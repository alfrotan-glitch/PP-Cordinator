#!/usr/bin/env python3
"""
Phase 3-5 — Normalization + automated editorial pass.

Input : project/manuscript/parts/00_extracted.md   (faithful extraction; never edited)
Output: project/manuscript/parts/10_body.md        (working body manuscript, chapters 1-10)
        project/logs/automated-change-log.csv      (rule id, classification, hits)
        project/logs/token-diff.csv                (QA: every new token a rule created)

Jobs:
  1. STRUCTURE   flat extraction -> typed block syntax the builders understand
  2. LANGUAGE    Dari copy-editing rule table (typography, ZWNJ, spacing)
  3. TERMINOLOGY Afghan-Dari terminology table (Iranian-Persian contamination audit)

English answer blocks (::: answer-en) are protected: no Dari rule is applied inside
them, so quoted English answers stay in ASCII and keep their own punctuation.
Sentence-level scientific/clinical corrections are made by hand on the output file
and recorded in project/logs/editorial-change-log.md.
"""
import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IN = ROOT / 'project/manuscript/parts/00_extracted.md'
OUT = ROOT / 'project/manuscript/parts/10_body.md'
LOG = ROOT / 'project/logs/automated-change-log.csv'
TOKDIFF = ROOT / 'project/logs/token-diff.csv'

ZWNJ = '\u200c'
DARI = '\u0600-\u06FF'
SCENARIO_RE = re.compile(r'^سناریو [۰-۹0-9]+[:：]')
SECTION_RE = re.compile(r'^بخش [الفبجد]+[:：]')


def is_dari(s: str) -> bool:
    letters = [c for c in s if c.isalpha()]
    if not letters:
        return False
    return len([c for c in letters if '\u0600' <= c <= '\u06FF']) / len(letters) > 0.6


# ------------------------------------------------------------------ structure
def structure(lines):
    out, i, open_block = [], 0, False

    def close():
        nonlocal open_block
        if open_block:
            out.append(':::')
            out.append('')
            open_block = False

    def open_b(header=''):
        nonlocal open_block
        close()
        out.append(':::' + ((' ' + header) if header else ''))
        out.append('')
        open_block = True

    while i < len(lines):
        s = lines[i].strip()

        if s.startswith(('# ', '## ', '### ')):
            close()
            out += [s, '']
            i += 1
            continue

        if SECTION_RE.match(s) and len(s) < 80:
            close()
            out += ['### ' + s, '']
            i += 1
            continue

        if SCENARIO_RE.match(s):
            open_b('scenario ' + s)
            i += 1
            continue

        if s == 'سناریو':
            open_b('scenario تمرین کوتاه')
            i += 1
            continue

        if s == 'مثال از دایکندی':
            open_b('example')
            i += 1
            continue

        if s.startswith(':::'):
            header = s[3:].strip()
            (open_b(header) if header else close())
            i += 1
            continue

        m = re.match(r'^> \*\*(.+)\*\*$', s)
        if m:
            label = m.group(1).strip()
            kind = 'key' if label.startswith('🔴') else ('tip' if label.startswith('⭐') else 'action')
            open_b(f'{kind} {label}')
            i += 1
            continue

        if s.startswith('**Sample Answer'):
            close()
            open_b('answer-en Sample Answer')
            i += 1
            continue
        if s.startswith('Sample Answer'):
            close()
            open_b('answer-en Sample Answer')
            inline = s[len('Sample Answer'):].lstrip(':： ').strip()
            if inline:
                out += [inline, '']
            i += 1
            continue
        if s.startswith('**جواب مدل') or s.startswith('جواب مدل'):
            close()
            open_b('answer-fa ' + s.strip('*').strip())
            i += 1
            continue

        if s.startswith(('- ❌', '- ✅')):
            if not open_block or '::: mistake' not in out[-4:][0]:
                open_b('mistake اشتباهات رایج')
            out += ['- ' + s[2:].strip(), '']
            i += 1
            continue

        if re.match(r'^[0-9۰-۹]{1,2}\.\s', s) and len(s) < 300:
            close()
            out += ['#### ' + s, '']
            i += 1
            continue
        if re.match(r'^[الفبجد]\)', s):
            out.append('- ' + s)
            i += 1
            continue
        if s.startswith('جواب:') and len(s) < 200:
            out += ['**' + s + '**', '']
            i += 1
            continue
        if s in ('↓', '↑'):
            out += ['`' + s + '`', '']
            i += 1
            continue

        if s:
            out += [s, '']
        i += 1

    close()
    return out


# ------------------------------------------------------- language rule table
LANGUAGE_RULES = [
    ('L01', r'\u200c{2,}', ZWNJ, 'Editorial', 'duplicate ZWNJ collapsed'),
    ('L02', r'[ \t]+(?=[،؛.؟!»٪])', '', 'Formatting', 'space before punctuation removed'),
    ('L03', r' {2,}', ' ', 'Formatting', 'double spaces collapsed'),
    ('L04', r'(?<=[\u0600-\u06FF])\.(?=[\u0600-\u06FF\u06F0-\u06F9])'
            r'(?<![\u06F0-\u06F9]\.)', '. ', 'Formatting',
     'missing space after sentence-final period'),
    ('L05', r'\s+([)])', r'\1', 'Formatting', 'space before closing bracket removed'),
    ('L06', r'\((\s+)', '(', 'Formatting', 'space after opening bracket removed'),
    ('L07', r'(?<![\u0600-\u06FF\u200c])اند(?![\u0600-\u06FF])', 'هستند', 'Editorial',
     'colloquial copula اند -> هستند (formal written Dari)'),
    ('L08', r'"([^"\n]{1,90})"', '«\1»', 'Formatting', 'straight quotes -> Dari guillemets'),
    ('L09', r'(?<!\.)\.\.\.(?!\.)', '…', 'Formatting', 'ellipsis normalised'),
    ('L10', r'\s+٪', '٪', 'Formatting', 'no space before ٪'),
    ('L11', r'(?<=[\u0600-\u06FF])[ \t]+ها(?=[\s،؛.()»«]|$)', ZWNJ + 'ها', 'Editorial',
     'ZWNJ restored before plural suffix ها'),
    ('L12', r'(?<=[\u0600-\u06FF])[ \t]+های(?=[\s،؛.()»«]|$)', ZWNJ + 'های', 'Editorial',
     'ZWNJ restored before plural suffix های'),
]

TERM_RULES = [
    ('T00', r'%', '٪', 'Formatting', 'Latin percent sign -> ٪ in Dari text'),
    ('T01', r'\bاستان\b', 'ولایت', 'Terminological',
     'Iranian administrative term استان -> Afghan ولایت'),
    ('T02', r'بیمارستان\b', 'شفاخانه', 'Terminological', 'Iranian بیمارستان -> Afghan شفاخانه'),
    ('T03', r'\bبیمار\b', 'مریض', 'Terminological', 'Iranian بیمار -> Afghan مریض'),
    ('T04', r'پزشک\b', 'داکتر', 'Terminological', 'Iranian پزشک -> Afghan داکتر'),
    ('T05', r'روستا\b', 'قریه', 'Terminological', 'Iranian روستا -> Afghan قریه'),
    ('T06', r'\bکودک\b', 'طفل', 'Terminological', 'Iranian کودک -> Afghan طفل'),
    ('T07', r'\bدرصد\b', 'فیصد', 'Terminological', 'Iranian درصد -> Afghan فیصد'),
    ('T08', r'کارکنان', 'کارمندان', 'Terminological', 'کارکنان -> Afghan کارمندان'),
    ('T09', r'کامپیوتر', 'کمپیوتر', 'Terminological', 'Afghan spelling کمپیوتر'),
    ('T10', r'\bدانشگاه\b', 'پوهنتون', 'Terminological', 'Iranian دانشگاه -> Afghan پوهنتون'),
    ('T11', r'\bمدرسه\b', 'مکتب', 'Terminological', 'Iranian مدرسه -> Afghan مکتب'),
    ('T12', r'زنگ می‌زند', 'تماس می‌گیرد', 'Editorial',
     'register: زنگ زدن -> تماس گرفتن in professional prose'),
    ('T13', r'زنگ می‌زنی', 'تماس می‌گیری', 'Editorial', 'register consistency'),
    ('T14', r'زنگ بزنی', 'تماس بگیری', 'Editorial', 'register consistency'),
    ('T15', r'زنگ بزن', 'تماس بگیر', 'Editorial', 'register consistency'),
    ('T16', r'یک بار زنگ زدن', 'یک بار تماس گرفتن', 'Editorial', 'register consistency'),
    ('T17', r'زنگ زدن', 'تماس گرفتن', 'Editorial', 'register consistency'),
    ('T18', r'مریض می‌میرد', 'جان مریض در خطر است', 'Clinical correction',
     'unsafe phrasing replaced with a clinical risk statement'),
]

DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


def split_english(lines):
    """Return list of (is_english, [lines]) segments; English answer blocks are protected."""
    segs, buf, cur = [], [], False
    for ln in lines:
        s = ln.strip()
        if s.startswith('::: answer-en'):
            if buf:
                segs.append((cur, buf))
            buf, cur = [ln], True
            continue
        if cur and s == ':::':
            buf.append(ln)
            segs.append((cur, buf))
            buf, cur = [], False
            continue
        buf.append(ln)
    if buf:
        segs.append((cur, buf))
    return segs


def apply_rules(text, rules, log_rows, tag):
    for rid, pat, repl, cls, label in rules:
        n = len(re.findall(pat, text))
        if n:
            text = re.sub(pat, repl, text)
            log_rows.append({'rule': rid, 'classification': cls, 'description': label,
                             'hits': n, 'scope': 'whole manuscript'})
    return text


def persianise(lines, log_rows):
    out, in_english, changed = [], False, 0
    for ln in lines:
        s = ln.strip()
        if s.startswith('::: answer-en'):
            in_english = True
        elif in_english and s == ':::':
            in_english = False
        latin = len([c for c in ln if c.isascii() and c.isalpha()])
        dari_l = len([c for c in ln if '\u0600' <= c <= '\u06FF' and c.isalpha()])
        if (not in_english) and dari_l and latin <= dari_l:
            new = ln.translate(DIGITS)
            if new != ln:
                changed += 1
                ln = new
        out.append(ln)
    if changed:
        log_rows.append({'rule': 'N01', 'classification': 'Formatting',
                         'description': 'ASCII digits -> Persian-Indic digits in Dari text',
                         'hits': changed, 'scope': 'whole manuscript'})
    return out


MARKER_RE = re.compile(r'^(#{2,4} |- )(\d{1,2})([.\u06F0-\u06F9]{0,3}[.)]?\s|\s)')


def persianise_markers(lines, log_rows):
    """Numbering markers (headings, list items, جواب lines) always use ۰-۹."""
    out, n = [], 0
    for ln in lines:
        new = MARKER_RE.sub(lambda m: m.group(1) + m.group(2).translate(DIGITS) + m.group(3), ln)
        new = re.sub(r'^(\*\*جواب:\s*)([الفبجد])', r'\1\2', new)
        if new != ln:
            n += 1
        out.append(new)
    if n:
        log_rows.append({'rule': 'N02', 'classification': 'Formatting',
                         'description': 'numbering markers unified to Persian-Indic digits',
                         'hits': n, 'scope': 'headings/lists/exam items'})
    return out


LEGACY_DROP = [
    '# کتاب قانون زبان',
    'برای نمایش فهرست: کلیک راست کنید ← Update Field',
    'راهنمای فایل',
    'این سند دارای قالب راست‌به‌چپ (دری) با فونت وزیرمتن است. پس از باز کردن فایل در '
    'مایکروسافت ورد، فهرست مطالب را با کلیک راست و انتخاب Update Field به‌روز کنید.',
]


def drop_legacy_frontmatter(lines, log_rows):
    """Remove version-1 production scaffolding that the new build makes obsolete:

    * the book-title line (the title page is generated by the builders),
    * the "right-click and Update Field" instructions for the old TOC.
    """
    kept, dropped = [], 0
    for ln in lines:
        if ln.strip() in LEGACY_DROP:
            dropped += 1
            continue
        kept.append(ln)
    if dropped:
        log_rows.append({'rule': 'S00', 'classification': 'Structural',
                         'description': 'version-1 title line and manual TOC-update '
                                        'instructions removed (title page and TOC are now '
                                        'generated by the build)',
                         'hits': dropped, 'scope': 'front matter'})
    return kept


def main():
    log_rows_pre = []
    raw = IN.read_text(encoding='utf-8').split('\n')
    raw = drop_legacy_frontmatter(raw, log_rows_pre)
    lines = structure([l for l in raw if l.strip() != ZWNJ and l.strip() != ''])
    before_tokens = Counter(re.findall(r'[\u0600-\u06FF]{2,}', '\n'.join(lines)))

    segs = split_english(lines)
    log_rows = list(log_rows_pre)
    processed = []
    for is_eng, seg in segs:
        txt = '\n'.join(seg)
        if is_eng:
            txt = re.sub(r' {2,}', ' ', txt)
        else:
            txt = apply_rules(txt, LANGUAGE_RULES, log_rows, 'lang')
            txt = apply_rules(txt, TERM_RULES, log_rows, 'term')
            txt = re.sub(r'\s+([،؛.؟!»])', r'\1', txt)
            txt = re.sub(r'([،؛])(?=[^\s\d])', r'\1 ', txt)
            txt = re.sub(r'\s+([)])', r'\1', txt)
        processed.append(txt)
    text = '\n'.join(processed)

    lines = persianise(text.split('\n'), log_rows)
    lines = persianise_markers(lines, log_rows)

    clean, blank = [], 0
    for ln in lines:
        if not ln.strip():
            blank += 1
            if blank > 1:
                continue
        else:
            blank = 0
        clean.append(ln.rstrip())

    body = '\n'.join(clean).strip() + '\n'
    OUT.write_text(body, encoding='utf-8')

    # QA - which Dari tokens are new (created by the rules)?
    after_tokens = Counter(re.findall(r'[\u0600-\u06FF]{2,}', body))
    new = {t: c for t, c in after_tokens.items() if t not in before_tokens}
    with TOKDIFF.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['new_token', 'count', 'note'])
        for tok, c in sorted(new.items(), key=lambda x: -x[1]):
            w.writerow([tok, c, ''])
    agg = {}
    order = []
    for r in log_rows:
        if r['rule'] not in agg:
            agg[r['rule']] = dict(r)
            order.append(r['rule'])
        else:
            agg[r['rule']]['hits'] += r['hits']
    log_rows = [agg[k] for k in order]

    with LOG.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['rule', 'classification', 'description',
                                          'hits', 'scope'])
        w.writeheader()
        for r in log_rows:
            w.writerow(r)

    print(f'body      -> {OUT}  ({len(clean)} lines)')
    print(f'changelog -> {LOG}  ({len(log_rows)} automated rules applied)')
    print(f'token QA  -> {TOKDIFF}  ({len(new)} new tokens to review)')
    for r in log_rows:
        print(f"  {r['rule']}  x{r['hits']:<4} {r['classification']:<22} {r['description']}")


if __name__ == '__main__':
    main()
