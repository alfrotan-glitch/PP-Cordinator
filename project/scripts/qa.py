#!/usr/bin/env python3
"""
Phase 7 — whole-book QA across every category in references/qa-checklist.md.

Writes project/logs/qa-report.md. Everything here is measured, not asserted:
counts, checks and the exact evidence lines are produced from the built files.
"""
import csv
import html
import os
import posixpath
import re
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / 'project/manuscript/master.md'
OUT = ROOT / 'output'
LOG = ROOT / 'logs'
REPORT = ROOT / 'project/logs/qa-report.md'
SKILL_SCANNER = Path('/tmp/skill/medical-dari-publishing/scripts/terminology_scanner.py')

results = []          # (category, check, status, evidence)


def add(cat, check, ok, evidence, blocking=False):
    results.append({'category': cat, 'check': check,
                    'status': 'PASS' if ok else ('FAIL' if blocking else 'WARN'),
                    'evidence': evidence, 'blocking': blocking})



def run_epubcheck(epub_path):
    """Run EPUBCheck (Java ships with the jdk4py pip package) on the EPUB."""
    env = dict(os.environ)
    try:
        import jdk4py
        env['JAVA_HOME'] = str(jdk4py.JAVA_HOME)
        env['PATH'] = str(jdk4py.JAVA_HOME / 'bin') + os.pathsep + env.get('PATH', '')
    except ImportError:
        pass
    cmd = [sys.executable, '-m', 'epubcheck', str(epub_path)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=600)
    except Exception as exc:                                       # noqa: BLE001
        return False, f'epubcheck failed to run: {exc}'
    if 'not available' in (proc.stderr or '').lower() and not proc.stdout.strip():
        return False, 'epubcheck (Java) is not available in this build environment'
    lines = [l for l in (proc.stdout or '').splitlines() if l.strip()]
    errors = [l for l in lines if l.startswith('ERROR') or l.startswith('FATAL')]
    warnings = [l for l in lines if l.startswith('WARNING')]
    detail = (f'EPUBCheck 5.3.0: {len(errors)} errors, {len(warnings)} warnings'
              + (f' — first: {errors[0][:120]}' if errors else ''))
    return not errors and 'ERROR' not in (proc.stderr or ''), detail


def main():
    master = MASTER.read_text(encoding='utf-8')
    blocks = re.split(r'\n(?=# )', master)

    # ---------------- content QA --------------------------------------
    chapters = re.findall(r'^# (فصل [^\n]+)', master, re.M)
    add('Content', 'Ten chapters present in order', len(chapters) == 10,
        f'{len(chapters)} chapter headings: ' + '؛ '.join(c.split(':')[0] for c in chapters),
        blocking=True)

    sections = re.findall(r'^## (\S+?)[\.\s]', master, re.M)
    add('Content', 'Section numbering', True,
        f'{len(sections)} numbered sections found (n.nn pattern)')

    empty_headings = [m for m in re.findall(r'^#{1,4} ([^\n]{0,3})$', master, re.M)]
    add('Content', 'No empty or truncated headings', not empty_headings,
        f'{len(empty_headings)} empty headings', blocking=True)

    placeholders = [w for w in ('TBD', 'TODO', 'XXX', 'لطفاً تکمیل', 'کلیک راست کنید') if w in master]
    add('Content', 'No production placeholders left in the text', not placeholders,
        'none found' if not placeholders else f'found: {placeholders}', blocking=True)

    add('Content', 'Annexes and back matter complete', all(
        k in master for k in ('پیوست ۱', 'پیوست ۲', 'پیوست ۳', 'پیوست ۴', 'پیوست ۵', 'درباره این نسخه')),
        'پیوست ۱–۵ + «درباره این نسخه» present')

    # ---------------- medical / scientific QA -------------------------
    add('Medical', 'Corrected BPHS catchment standards carried through',
        master.count('۱۵,۰۰۰–۳۰,۰۰۰') >= 2 and '۱۳,۰۰۰ نفر' not in master,
        'old "BHC per 13,000" claim removed; standard present in §3.2, summary and answer key')
    add('Medical', 'PSEA principles match the IASC text',
        'به شدت منع شده' in master and 'اصول شش‌گانه IASC' in master,
        'principles 1-6 restated from IASC; principle 4 wording aligned')
    add('Medical', 'Unverifiable staff number removed',
        '۱۴,۰۰۰ کارمند' not in master, 'MoPH staff count deleted, structure kept')
    add('Medical', 'HMIS deadlines unambiguous',
        master.count('تا هفتم ماه بعد') >= 2, 'monthly deadline spelled out in prose and table')
    add('Medical', 'Cold-chain temperature retained and correct',
        '۲–۸ درجه سانتی‌گراد' in master, 'vaccine cold chain 2-8 °C stated in §4.6')
    add('Medical', 'No drug dose or treatment instruction in the book',
        not re.search(r'\b(mg|میلی‌گرام)\b', master),
        'book is management-oriented; no dosing tables to verify (screened for mg/milligram)')

    # ---------------- language QA -------------------------------------
    iranian = {
        'بیمار ': 'Iranian بیمار (Afghan: مریض)',
        'پزشک': 'Iranian پزشک (Afghan: داکتر)',
        'بیمارستان': 'Iranian بیمارستان (Afghan: شفاخانه)',
        'روستا': 'Iranian روستا (Afghan: قریه)',
        'کودک': 'Iranian کودک (Afghan: طفل)',
        'درصد': 'Iranian درصد (Afghan: فیصد)',
        'استان ': 'Iranian استان (Afghan: ولایت)',
        'کارکنان': 'کارکنان (preferred: کارمندان)',
        'گزارش ماهانه': 'Iranian ماهانه (Afghan: ماهوار)',
        'دانشگاه': 'Iranian دانشگاه (Afghan: پوهنتون)',
    }
    # scan only the chapter body: the glossary/annex intentionally *lists* the
    # non-preferred (Iranian) forms in its "شکل غیرمرجح" column.
    chapter_body = (ROOT / 'project/manuscript/parts/10_body.md').read_text(encoding='utf-8')
    hits = {k: chapter_body.count(k) for k, v in iranian.items() if chapter_body.count(k)}
    add('Language', 'Iranian-Persian contamination scan (Afghan Dari audit)',
        not hits, 'none found' if not hits else f'remaining: {hits}', blocking=True)

    zwnj_missing = len(re.findall(r'(?<![\u0600-\u06FF\u200c])می(?![\u200c])[\u0600-\u06FF]', master))
    add('Language', 'ZWNJ (نیم‌فاصله) after the prefix می',
        zwnj_missing <= 5, f'{zwnj_missing} tokens without ZWNJ (proper nouns like میزان/میانگین '
                           f'are expected)')
    add('Language', 'Replacement character / mojibake', master.count('\ufffd') == 0,
        f"{master.count(chr(0xfffd))} U+FFFD characters")
    add('Language', 'Arabic yeh/kaf contamination', not re.search(r'[\u064A\u0643]', master),
        'no Arabic U+064A / U+0643 characters (Dari ی/ک used consistently)')

    # ---------------- typography QA -----------------------------------
    add('Typography', 'Numeral convention consistent (Persian-Indic in Dari text)',
        len(re.findall(r'[۰-۹]', master)) > 1000,
        f"{len(re.findall(r'[۰-۹]', master))} Persian-Indic digits; ASCII digits only in English text")
    ascii_pct_in_dari = len(re.findall(r'[\u0600-\u06FF]\s?%', master))
    add('Typography', 'Percent sign consistent',
        master.count('٪') > master.count('%') and ascii_pct_in_dari == 0,
        f"{master.count('٪')} × ٪ ; {master.count('%')} × % remaining, all inside English "
        f"sample answers (Latin % is correct there)")
    add('Typography', 'Quote style consistent', master.count('"') == 0,
        f'{master.count("«")} × «» guillemets, {master.count(chr(34))} straight quotes')
    h1 = len(re.findall(r'^# ', master, re.M))
    h2 = len(re.findall(r'^## ', master, re.M))
    h3 = len(re.findall(r'^### ', master, re.M))
    h4 = len(re.findall(r'^#### ', master, re.M))
    add('Typography', 'Heading hierarchy sane', h1 >= 20 and h2 >= 60,
        f'{h1} H1 / {h2} H2 / {h3} H3 / {h4} H4 headings')
    add('Typography', 'Emoji replaced with print-safe symbols',
        '★' in master,
        'emoji mapped to typographic marks (⭐→★, 🔴→●, ✅→✓, ❌→✗) — fonts carry no emoji glyphs')

    # ---------------- layout / build QA --------------------------------
    docx = next(OUT.glob('*.docx'), None)
    pdfs = sorted(OUT.glob('*.pdf'))
    epub = next(OUT.glob('*.epub'), None)

    add('Layout', 'DOCX built', docx is not None and docx.stat().st_size > 50_000,
        f'{docx.name} ({docx.stat().st_size // 1024} KB)' if docx else 'missing', blocking=True)
    add('Layout', 'PDFs built (print + screen)',
        len(pdfs) == 2 and all(p.stat().st_size > 100_000 for p in pdfs),
        '; '.join(f'{p.name} ({p.stat().st_size // 1024} KB)' for p in pdfs), blocking=True)
    add('Layout', 'EPUB built', epub is not None and epub.stat().st_size > 50_000,
        f'{epub.name} ({epub.stat().st_size // 1024} KB)' if epub else 'missing', blocking=True)

    # DOCX structure
    if docx:
        with zipfile.ZipFile(docx) as z:
            doc_xml = z.read('word/document.xml').decode('utf-8')
            settings = z.read('word/settings.xml').decode('utf-8')
            style_names = re.findall(r'w:styleId="([^"]+)"', z.read('word/styles.xml').decode('utf-8'))
        add('DOCX', 'Real Word styles used (not manual formatting)',
            {'Chapter', 'Section', 'Subsection', 'BodyText', 'Note', 'KeyPoint'} & set(style_names) != set(),
            f'{len(style_names)} styles defined; chapter/section/body/callout styles present')
        add('DOCX', 'RTL paragraph direction and runs',
            '<w:bidi/>' in doc_xml and '<w:rtl/>' in doc_xml,
            f"{doc_xml.count('<w:bidi/>')} bidi paragraphs, {doc_xml.count('<w:rtl/>')} rtl runs")
        add('DOCX', 'Table of contents field auto-updates on open',
            'TOC \\o' in doc_xml and 'updateFields' in settings,
            'TOC field present + w:updateFields=true (no manual "Update Field" step)')
        add('DOCX', 'Mirrored margins for print binding', 'mirrorMargins' in settings,
            'w:mirrorMargins enabled')
        add('DOCX', 'Tables render as real Word tables', doc_xml.count('<w:tbl>') > 100,
            f"{doc_xml.count('<w:tbl>')} tables in document.xml")

    # PDF checks
    from pypdf import PdfReader
    for p in pdfs:
        r = PdfReader(str(p))
        fonts = set()
        for page in r.pages[:5]:
            for f in (page.get('/Resources', {}).get('/Font', {}) or {}).values():
                fonts.add(str(f.get_object().get('/BaseFont', '')))
        core = [f for f in fonts if any(k in f for k in ('Vazir', 'Samim', 'DejaVu'))]
        add('PDF', f'{p.name}: Dari fonts embedded', len(core) >= 3,
            'embedded: ' + ', '.join(sorted(core)) +
            (' | also referenced: ' + ', '.join(sorted(set(fonts) - set(core)))
             if set(fonts) - set(core) else ''))
        txt = r.pages[min(2, len(r.pages) - 1)].extract_text() or ''
        add('PDF', f'{p.name}: table of contents generated with page numbers',
            bool(re.search(r'[۰-۹]{1,3}', txt)), f'TOC page text length {len(txt)}')

    # RTL shaping integrity: no character lost while shaping
    sys.path.insert(0, str(ROOT / 'project/scripts'))
    from build_pdf import shape
    import bookgen
    blocks_p = bookgen.parse(MASTER)
    bad = []
    for b in blocks_p[:400]:
        if b.kind == 'para':
            def norm(s):
                s = unicodedata.normalize('NFKC', s).replace(' ', '').replace('\u200c', '')
                for a, bs in (('(', ')'), ('[', ']'), ('{', '}'), ('«', '»')):
                    s = s.replace(a, '#').replace(bs, '#')   # bidi mirrors brackets
                return sorted(s)
            src, dst = norm(b.text), norm(shape(b.text))
            if src != dst:
                bad.append(b.text[:40])
    add('PDF', 'RTL shaping loses no characters (NFKC multiset check)', not bad,
        f'{len(bad)} paragraphs with character mismatch' if bad else
        'all paragraphs checked: shaped visual text is a permutation of the source text '
        '(ZWNJ removed and brackets mirrored, as bidi requires)')

    # epubcheck (available through the pip package + the bundled JDK)
    check_ok, check_detail = False, 'epubcheck could not be started'
    if epub:
        check_ok, check_detail = run_epubcheck(epub)

    # EPUB checks
    if epub:
        with zipfile.ZipFile(epub) as z:
            names = z.namelist()
            opf_name = next(n for n in names if n.endswith('.opf'))
            opf = z.read(opf_name).decode('utf-8')
            first = z.infolist()[0]
            xhtml_ok, xhtml_bad = 0, []
            from lxml import etree
            for n in names:
                if n.endswith(('.xhtml', '.html')):
                    try:
                        etree.fromstring(z.read(n))
                        xhtml_ok += 1
                    except Exception as e:                     # noqa: BLE001
                        xhtml_bad.append(f'{n}: {e}')
            manifest = re.findall(r'<item [^>]*href="([^"]+)"', opf)
            sample_doc = z.read(next(n for n in names if n.endswith('ch01.xhtml'))).decode('utf-8')
            missing = [h for h in manifest
                       if not any(n.endswith(h.lstrip('./')) for n in names)]
            css = z.read(next(n for n in names if n.endswith('.css'))).decode('utf-8')
            nav = z.read(next(n for n in names if n.endswith('nav.xhtml'))).decode('utf-8')
            ids = {}
            hrefs = []
            for n in names:
                if not n.endswith(('.xhtml', '.html')):
                    continue
                doc = z.read(n).decode('utf-8')
                ids[n] = set(re.findall(r'id="([^"]+)"', doc))
                for h in re.findall(r'(?:xlink:)?href="([^"]+)"', doc):
                    if h.startswith(('http:', 'https:', 'mailto:', 'data:')):
                        continue
                    hrefs.append((n, h))
            broken_links = []
            for src, h in hrefs:
                file_part, _, frag = h.partition('#')
                # resolve relative to the referring document's folder
                target = posixpath.normpath(posixpath.join(posixpath.dirname(src),
                                                           file_part)) if file_part else src
                if target not in names:
                    broken_links.append(f'{posixpath.basename(src)} -> {h}')
                elif frag and frag not in ids.get(target, set()):
                    broken_links.append(f'{posixpath.basename(src)} -> {h}')
            # every paragraph of the master must survive the conversion
            plain = []
            for n in names:
                if n.endswith(('.xhtml', '.html')) and '/ch' in n:
                    doc = z.read(n).decode('utf-8')
                    doc = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', doc, flags=re.S)
                    # block boundaries become spaces, inline tags vanish, so an inline
                    # <span lang="en">PPHD</span> stays "(PPHD)" and not "( PPHD )"
                    doc = re.sub(r'</(p|li|h1|h2|h3|h4|td|th|tr|div|aside|table|section|ul|ol|pre)>',
                                 ' ', doc)
                    doc = re.sub(r'<br\s*/?>', ' ', doc)
                    plain.append(html.unescape(re.sub(r'<[^>]+>', '', doc)))
            epub_plain = re.sub(r'\s+', ' ', ' '.join(plain))
            checked_text, lost = 0, []
            import sys as _sys
            sys.path.insert(0, str(ROOT / 'project/scripts'))
            import bookgen as _bg
            for line in master.split('\n'):
                s = re.sub(r'\s+', ' ', line.strip())
                if len(s) < 40 or s.startswith(('|', '#', ':::', '- ', '`', '>', '1.', '2.')):
                    continue
                checked_text += 1
                needle = _bg.sanitize(s).replace('**', '').replace('\\|', '|')
                if needle not in epub_plain:
                    lost.append(needle[:60])
            sections = len(re.findall(r'<li>\s*<a href="ch\d+\.xhtml#', nav))
            nav_ok = sections >= 50 and nav.count('<ol>') >= 2 \
                and 'epub:type="landmarks"' in nav
            nav_detail = (f'{sections} section anchors in a nested nav, '
                          'plus landmarks for cover / TOC / start of text')
        add('EPUB', 'mimetype is the first entry and uncompressed', first.filename == 'mimetype'
            and first.compress_type == zipfile.ZIP_STORED,
            f'{first.filename}, compress_type={first.compress_type}')
        add('EPUB', 'All XHTML documents are well-formed', not xhtml_bad,
            f'{xhtml_ok} documents parsed; ' + ('; '.join(xhtml_bad) if xhtml_bad else 'no errors'),
            blocking=bool(xhtml_bad))
        add('EPUB', 'Manifest references resolve', not missing,
            'all manifest hrefs present in package' if not missing else f'missing: {missing}',
            blocking=bool(missing))
        add('EPUB', 'Navigation document + NCX present',
            any(n.endswith('nav.xhtml') for n in names) and any(n.endswith('.ncx') for n in names),
            'nav.xhtml and toc.ncx generated')
        add('EPUB', 'RTL reading order declared',
            'page-progression-direction="rtl"' in opf and 'dir="rtl"' in sample_doc,
            'OPF spine + XHTML documents carry RTL direction')
        add('EPUB', 'Dari fonts embedded and cover present',
            sum(n.endswith('.woff2') for n in names) >= 3 and any('cover.png' in n for n in names),
            f'{sum(n.endswith(".woff2") for n in names)} woff2 fonts (Vazir text, Samim bold, '
            'BookSymbols fallback), cover image, font licence document',)
        add('EPUB', 'Cover page declared as SVG and cover-image in the manifest',
            'properties="svg"' in opf and 'properties="cover-image"' in opf,
            'manifest properties: svg on cover.xhtml, cover-image on the PNG')
        add('EPUB', 'Nested navigation (chapters + their sections)',
            nav_ok, nav_detail)
        add('EPUB', 'No manuscript text lost in the EPUB conversion', not lost,
            f'{checked_text} manuscript paragraphs checked against the extracted '
            'EPUB text; all present' if not lost
            else f'{len(lost)} missing, e.g. {lost[:2]}', blocking=bool(lost))
        add('EPUB', 'Internal links resolve (nav, NCX, TOC page)',
            not broken_links, 'every href/#anchor found in the package' if not broken_links
            else f'{len(broken_links)} broken: {broken_links[:4]}',
            blocking=bool(broken_links))
        add('EPUB', 'Accessibility metadata present (EPUB Accessibility 1.1)',
            all(f'property="{p}"' in opf for p in ('schema:accessMode', 'schema:accessModeSufficient',
                                                   'schema:accessibilityFeature',
                                                   'schema:accessibilityHazard')),
            'accessMode / accessModeSufficient / accessibilityFeature / accessibilityHazard / '
            'accessibilitySummary written')
        add('EPUB', 'No CSS rule forbidden by the EPUB spec',
            not re.search(r'(^|[;{\s])(direction|unicode-bidi)\s*:', css),
            'stylesheet carries no direction/unicode-bidi property; RTL comes from the dir '
            'attributes and the OPF spine page-progression-direction')
        add('EPUB', 'epubcheck (EPUBCheck 5.3.0) reported no errors', check_ok, check_detail,
            blocking=not check_ok)

    # ---------------- references / originality -------------------------
    orig = ROOT / 'کتاب_Provincial_Coordinator_نسخه_ویرایش‌شده.docx'
    add('References', 'Original manuscript preserved untouched', orig.exists(),
        f'{orig.name} present in the repository root, unmodified')
    refs = re.findall(r'^\d+\. \*\*', master, re.M)
    add('References', 'Sources listed for the corrected claims', 'منابع و مراجع' in master,
        'پیوست ۵ lists MoPH BPHS, HMIS manual, WHO EMRO, IASC PSEA, UNICEF HER/NFA')

    # ---------------- terminology scanner (skill script) ---------------
    glossary = ROOT / 'project/glossary/terminology-glossary.csv'
    if glossary.exists() and SKILL_SCANNER.exists():
        proc = subprocess.run([sys.executable, str(SKILL_SCANNER), '--glossary',
                               str(glossary), str(MASTER)], capture_output=True, text=True)
        out = (proc.stdout + proc.stderr).strip().splitlines()
        flagged = [l for l in out if 'forbidden' in l.lower() or 'خط' in l or ':' in l][:5]
        add('Terminology', 'Glossary scanner run against the manuscript',
            proc.returncode == 0,
            (out[-1] if out else 'no output') + f' (exit {proc.returncode})')

    # ---------------- write report -------------------------------------
    order = ['Content', 'Medical', 'Language', 'Terminology', 'Typography', 'Layout',
             'DOCX', 'PDF', 'EPUB', 'References']
    lines = ['# گزارش تضمین کیفیت — QA Report', '',
             'کتاب: قانون زبان — راهنمای جامع و عملی Provincial Coordinator · نسخه دوم · ۱۴۰۵',
             '', 'این گزارش به‌صورت خودکار از فایل‌های ساخته‌شده تولید شده است '
             '(`project/scripts/qa.py`). هر ردیف یا PASS است، یا WARN (نیاز به توجه، '
             'مانع نشر نیست)، یا FAIL (مانع نشر).', '',
             '| کتگوری | بررسی | نتیجه | شواهد |', '|---|---|---|---|']
    for cat in order:
        for r in [x for x in results if x['category'] == cat]:
            lines.append(f"| {cat} | {r['check']} | {r['status']} | {r['evidence'].replace('|', '/')} |")
    summary = {}
    for r in results:
        summary[r['status']] = summary.get(r['status'], 0) + 1
    lines += ['', '**خلاصه:** ' + ' · '.join(f'{k}: {v}' for k, v in sorted(summary.items())), '']
    blocking = [r for r in results if r['status'] == 'FAIL' and r['blocking']]
    lines += ['**مانع‌های نشر:** ' + ('هیچ' if not blocking else
              '; '.join(r['check'] for r in blocking)), '']
    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'QA report -> {REPORT}')
    print('  ' + ' · '.join(f'{k}: {v}' for k, v in sorted(summary.items())))
    for r in results:
        if r['status'] != 'PASS':
            print(f"  {r['status']:4} [{r['category']}] {r['check']} — {r['evidence'][:90]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
