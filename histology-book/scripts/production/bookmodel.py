# -*- coding: utf-8 -*-
"""
bookmodel.py — parse the frozen Markdown manuscript into a structured document model.

The manuscript is the verified source of truth. This module never rewrites content:
it only recognises structure (chapters, topics, the 13 sections, bilingual blocks,
tables, lists, callouts, diagrams) and preserves every text character for rendering.

Model
-----
Document(front: list[Block], chapters: list[Chapter], meta: dict)
Chapter(number, fa_title, en_title, blocks: list[Block], topics: list[Topic], audit: ...)
Topic(number, fa_title, en_title, blocks)
Block: Heading | Para | List | Table | Callout | Diagram | Rule
"""
from __future__ import annotations

import io
import os
import re
from dataclasses import dataclass, field
from typing import Optional

BOOK_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---------------------------------------------------------------- inline model

INLINE_RE = re.compile(
    r"(`[^`]+`)"
    r"|(\*\*[^*]+\*\*)"
    r"|(\*[^*\n]+\*)"
    r"|(~~[^~]+~~)"
    r"|(\\?\*[^*\s][^*]*\*)"
)


@dataclass
class Span:
    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False
    sup: bool = False
    sub: bool = False


SUPERSCRIPT_CHARS = "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079" \
                    "\u207a\u207b\u207c\u207d\u207e\u207f\u2071"
SUBSCRIPT_CHARS = "\u2080\u2081\u2082\u2083\u2084\u2085\u2086\u2087\u2088\u2089" \
                  "\u208a\u208b\u208c\u208d\u208e"
SUP_BASE = {"\u2070": "0", "\u00b9": "1", "\u00b2": "2", "\u00b3": "3", "\u2074": "4",
            "\u2075": "5", "\u2076": "6", "\u2077": "7", "\u2078": "8", "\u2079": "9",
            "\u207a": "+", "\u207b": "\u2212", "\u207c": "=", "\u207d": "(",
            "\u207e": ")", "\u207f": "n", "\u2071": "i"}
SUB_BASE = {"\u2080": "0", "\u2081": "1", "\u2082": "2", "\u2083": "3", "\u2084": "4",
            "\u2085": "5", "\u2086": "6", "\u2087": "7", "\u2088": "8", "\u2089": "9",
            "\u208a": "+", "\u208b": "\u2212", "\u208c": "=", "\u208d": "(",
            "\u208e": ")"}
_FA_DIGITS = "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9"
_ASCII_DIGITS = "0123456789"
_SCRIPT_RUN = re.compile(f"[{SUPERSCRIPT_CHARS}{SUBSCRIPT_CHARS}]+")


def _script_span(match: "re.Match", text: str, base: Span) -> Span:
    """One run of Unicode super/subscript characters becomes a real <sup>/<sub> span."""
    run = match.group(0)
    sup = run[0] in SUPERSCRIPT_CHARS
    table = SUP_BASE if sup else SUB_BASE
    out = [table.get(ch, ch) for ch in run]
    # Persian digits are used when the script sits on a Persian numeral (۱۰⁻³ m)
    before = text[match.start() - 1] if match.start() else ""
    after = text[match.end()] if match.end() < len(text) else ""
    if (before and before in _FA_DIGITS) or (after and after in _FA_DIGITS):
        out = [_FA_DIGITS[_ASCII_DIGITS.index(c)] if c in _ASCII_DIGITS else c for c in out]
    return Span("".join(out), bold=base.bold, italic=base.italic, code=base.code,
                sup=sup, sub=not sup)


def normalize_scripts(text: str) -> str:
    """Rewrite Unicode super/subscript characters as their base characters, script-aware.

    The digit script follows the text around it, so «۱۰⁻³ m» keeps Persian digits while
    «CO₂» and «Ca²⁺» stay Latin.  Used by the QA token comparison so both sides of it use
    one and the same convention.
    """
    out: list[str] = []
    pos = 0
    for m in _SCRIPT_RUN.finditer(text):
        run = m.group(0)
        table = SUP_BASE if run[0] in SUPERSCRIPT_CHARS else SUB_BASE
        chars = [table.get(ch, ch) for ch in run]
        before = text[m.start() - 1] if m.start() else ""
        after = text[m.end()] if m.end() < len(text) else ""
        if (before and before in _FA_DIGITS) or (after and after in _FA_DIGITS):
            chars = [_FA_DIGITS[_ASCII_DIGITS.index(c)] if c in _ASCII_DIGITS else c
                     for c in chars]
        out.append(text[pos:m.start()])
        out.append("".join(chars))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def _split_scripts(spans: list[Span], source: str) -> list[Span]:
    """Expand every span that still contains super/subscript characters."""
    out: list[Span] = []
    for span in spans:
        if not _SCRIPT_RUN.search(span.text):
            out.append(span)
            continue
        pos = 0
        for m in _SCRIPT_RUN.finditer(span.text):
            if m.start() > pos:
                out.append(Span(span.text[pos:m.start()], bold=span.bold, italic=span.italic,
                                code=span.code))
            out.append(_script_span(m, span.text, span))
            pos = m.end()
        if pos < len(span.text):
            out.append(Span(span.text[pos:], bold=span.bold, italic=span.italic, code=span.code))
    return [s for s in out if s.text]


def parse_inline(text: str) -> list[Span]:
    """Split one line of Markdown into spans (bold / italic / code)."""
    spans: list[Span] = []
    pos = 0
    for m in re.finditer(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*\n]+\*|~~[^~]+~~)", text):
        if m.start() > pos:
            spans.append(Span(text[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith("**"):
            spans.append(Span(tok[2:-2], bold=True))
        elif tok.startswith("`"):
            spans.append(Span(tok[1:-1], code=True))
        elif tok.startswith("~~"):
            spans.append(Span(tok[2:-2], italic=True))
        else:
            spans.append(Span(tok[1:-1], italic=True))
        pos = m.end()
    if pos < len(text):
        spans.append(Span(text[pos:]))
    return _split_scripts([s for s in spans if s.text], text)


def plain_text(text: str) -> str:
    """Inline Markdown -> plain text (used for TOC labels and QA)."""
    return "".join(s.text for s in parse_inline(text))


# ------------------------------------------------------------------- blocks

@dataclass
class Block:
    kind: str = "para"          # para | heading | list | table | callout | diagram | rule
    level: int = 0              # heading level (1 = topic/chapter title, 2 = 13-section head)
    html: str = ""              # rendered html fragment (set by render.py)
    spans: list[list[Span]] = field(default_factory=list)
    text: str = ""              # plain text, for TOC / QA / running heads
    items: list = field(default_factory=list)   # nested list items
    rows: list = field(default_factory=list)    # table rows
    header: list = field(default_factory=list)  # table header
    lang: str = "fa"            # fa | en | mixed
    role: str = ""              # chapter-title | topic-title | section | audit | record | …
    keep_with_next: bool = False
    gap_before: float = 0.0
    gap_after: float = 0.0


@dataclass
class Topic:
    number: str                 # "1.1"
    fa_title: str
    en_title: str
    blocks: list = field(default_factory=list)
    chapter: Optional["Chapter"] = None

    @property
    def label(self) -> str:
        return f"{self.number} {self.fa_title}"


@dataclass
class Chapter:
    number: int
    fa_title: str
    en_title: str
    blocks: list = field(default_factory=list)   # front blocks (aim callout …)
    topics: list = field(default_factory=list)
    tail: list = field(default_factory=list)     # everything after the topics
    review: list = field(default_factory=list)   # chapter master-table review (ch 1–5)
    sa: list = field(default_factory=list)       # chapter self-assessment → Appendix A
    audit: list = field(default_factory=list)    # reference-alignment audit → Appendix B
    file: str = ""

    @property
    def label_fa(self) -> str:
        return f"فصل {self.number} — {self.fa_title}"

    @property
    def label_short(self) -> str:
        return f"فصل {self.number} · {self.fa_title}"


@dataclass
class Document:
    front: list = field(default_factory=list)
    chapters: list = field(default_factory=list)
    meta: dict = field(default_factory=dict)


# ------------------------------------------------------------------- helpers

FA_RE = re.compile(r"[\u0600-\u06FF]")
EN_RE = re.compile(r"[A-Za-z]")

SECTION_RE = re.compile(r"^##\s+(\d{1,2})\.\s+(.*)$")
TOPIC_RE = re.compile(r"^#\s+(\d{1,2}\.\d{1,2})\s+(.*)$")
CH_FA_RE = re.compile(r"^#\s+فصل\s+(\d{1,2})\s*—\s*(.*)$")
CH_EN_RE = re.compile(r"^#\s+Chapter\s+(\d{1,2})\s*—\s*(.*)$")


def lang_of(text: str) -> str:
    fa = bool(FA_RE.search(text))
    en = bool(EN_RE.search(text))
    if fa and en:
        return "mixed"
    return "fa" if fa else "en"


def _split_bilingual(title: str) -> tuple[str, str]:
    """'1.1 هستولوژی چیست — What Is Histology?' -> (fa, en)"""
    if "—" not in title:
        return title.strip(), ""
    left, right = title.split("—", 1)
    return left.strip(), right.strip()


# ------------------------------------------------------------------- parsing

def _split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c.strip()) for c in cells if c.strip() != "")


SENTENCE_END_RE = re.compile(r"[.؟!:؛]\s*$")
ITEM_START_RE = re.compile(r"^\s*(\(\d+\)|[-*•]|\d+[.)])\s")


def _join_wrapped(lines: list[str]) -> list[str]:
    """Re-join paragraph lines that were wrapped mid-sentence (as in the source)."""
    out: list[str] = []
    for ln in lines:
        if out and not SENTENCE_END_RE.search(out[-1]) and not ITEM_START_RE.match(ln) \
                and out[-1].strip():
            out[-1] = out[-1].rstrip() + " " + ln.strip()
        else:
            out.append(ln)
    return out


def _flush_para(buf: list[str], out: list[Block], role: str = "") -> None:
    if not buf:
        return
    text = " ".join(x.strip() for x in buf if x.strip())
    buf.clear()
    if not text:
        return
    role2 = role
    clean = text
    if clean.startswith("**دری:**"):
        role2, clean = "fa", clean[len("**دری:**"):].strip()
    elif clean.startswith("**English:**"):
        role2, clean = "en", clean[len("**English:**"):].strip()
    if not clean:
        return
    html_only_bold = re.fullmatch(r"\*\*[^*]+\*\*", clean) is not None
    out.append(Block(
        kind="para",
        level=0,
        text=plain_text(clean),
        spans=[parse_inline(clean)],
        lang=role2 or lang_of(clean),
        role="lead" if html_only_bold else (role2 or ""),
    ))


def parse_markdown(lines: list[str]) -> list[Block]:
    blocks: list[Block] = []
    buf: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        # ---- blank
        if not stripped:
            _flush_para(buf, blocks)
            i += 1
            continue

        # ---- fenced diagram
        if stripped.startswith("```"):
            _flush_para(buf, blocks)
            j = i + 1
            code: list[str] = []
            while j < n and not lines[j].strip().startswith("```"):
                code.append(lines[j].rstrip())
                j += 1
            blocks.append(Block(kind="diagram", text="\n".join(code).strip("\n"),
                                spans=[[Span("\n".join(code).strip("\n"))]], lang="en"))
            i = j + 1
            continue

        # ---- horizontal rule
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            _flush_para(buf, blocks)
            blocks.append(Block(kind="rule"))
            i += 1
            continue

        # ---- heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            _flush_para(buf, blocks)
            blocks.append(Block(kind="heading", level=len(m.group(1)), text=plain_text(m.group(2)),
                                spans=[parse_inline(m.group(2))], lang=lang_of(m.group(2))))
            i += 1
            continue

        # ---- table
        if stripped.startswith("|"):
            _flush_para(buf, blocks)
            rows: list[list[str]] = []
            header: list[str] = []
            while i < n and lines[i].strip().startswith("|"):
                cells = _split_table_row(lines[i])
                if _is_sep_row(cells):
                    i += 1
                    continue
                if not header and not rows:
                    header = cells
                else:
                    rows.append(cells)
                i += 1
            blocks.append(Block(kind="table", header=header, rows=rows,
                                text=" | ".join(plain_text(c) for c in header),
                                lang="mixed"))
            continue

        # ---- blockquote / callout
        if stripped.startswith(">"):
            _flush_para(buf, blocks)
            q: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                q.append(re.sub(r"^\s*>\s?", "", lines[i]).rstrip())
                i += 1
            qlines = _join_wrapped([x for x in q])
            while qlines and not qlines[-1].strip():
                qlines.pop()
            blocks.append(Block(kind="callout", text=plain_text(" ".join(qlines)),
                                items=qlines, lang=lang_of(" ".join(qlines))))
            continue

        # ---- lists (bullet / numbered, possibly nested)
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            _flush_para(buf, blocks)
            items: list[tuple[int, str, str]] = []
            while i < n and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                cur = lines[i]
                indent = len(cur) - len(cur.lstrip(" "))
                mm = re.match(r"^\s*([-*]|\d+\.)\s+(.*)$", cur)
                marker = mm.group(1)
                body = [mm.group(2).rstrip()]
                kind = "ol" if marker[0].isdigit() else "ul"
                i += 1
                # a wrapped list item continues on the following indented lines
                while i < n:
                    nxt = lines[i]
                    if not nxt.strip():
                        break
                    if len(nxt) - len(nxt.lstrip(" ")) < 2:
                        break
                    if re.match(r"^\s*([-*]|\d+\.)\s+", nxt) \
                            or re.match(r"^\s*(#|>|\||```)", nxt):
                        break
                    body.append(nxt.strip())
                    i += 1
                items.append((indent, kind, " ".join(body)))
            blocks.append(Block(kind="list", items=items,
                                text=" ".join(plain_text(b) for _, _, b in items)[:120],
                                lang=lang_of(" ".join(b for _, _, b in items))))
            continue

        # ---- plain paragraph line
        buf.append(line)
        i += 1

    _flush_para(buf, blocks)
    return blocks


# --------------------------------------------------------------- classification

AUDIT_HEAD = "انطباقِ فصل با مرجع"
RECORD_HEAD = "ثبتِ تأییدِ علمی"
CHAPTER_SA_HEAD = "سؤالات مروری فصل"


def classify(doc: Document) -> None:
    """Attach roles to blocks so the renderers can style them."""
    for blk in doc.front:
        _role_block(blk, front=True)
    for ch in doc.chapters:
        for blk in ch.blocks:
            _role_block(blk, chapter=ch)
        for t in ch.topics:
            for blk in t.blocks:
                _role_block(blk, chapter=ch, topic=t)
        for blk in ch.tail:
            _role_block(blk, chapter=ch, tail=True)


def _role_block(blk: Block, chapter: Optional[Chapter] = None, topic: Optional[Topic] = None,
                tail: bool = False, front: bool = False) -> None:
    if blk.kind == "heading":
        txt = blk.text
        if blk.level == 1 and CH_FA_RE.match("# " + txt):
            blk.role = "chapter-title"
        elif blk.level == 1 and CH_EN_RE.match("# " + txt):
            blk.role = "chapter-title-en"
        elif blk.level == 1 and TOPIC_RE.match("# " + txt):
            blk.role = "topic-title"
            blk.keep_with_next = True
        elif blk.level == 1 and "Reference Alignment Audit" in txt:
            blk.role = "audit-title"
            blk.keep_with_next = True
        elif blk.level == 1:
            blk.role = "review-title"
            blk.keep_with_next = True
        elif blk.level == 2:
            if SECTION_RE.match("## " + txt):
                blk.role = "section"
                blk.keep_with_next = True
            elif txt.startswith(AUDIT_HEAD):
                blk.role = "audit-head"
            elif txt.startswith(RECORD_HEAD):
                blk.role = "record-head"
            elif txt.startswith(CHAPTER_SA_HEAD):
                blk.role = "chapter-sa-head"
            else:
                blk.role = "subhead"
                blk.keep_with_next = True
        else:
            blk.role = "subhead"
    elif blk.kind == "table":
        blk.role = "audit-table" if (tail and chapter) else "table"
    elif blk.kind == "callout":
        first = (blk.items[0] if blk.items else "")
        if "هدف فصل" in first or "اصل راهنما" in first:
            blk.role = "aim"
        elif "قانون طلایی" in first:
            blk.role = "golden"
        else:
            blk.role = "callout"
    elif blk.kind == "para":
        if tail:
            blk.role = "record-note"
        elif blk.role in ("fa", "en"):
            blk.role = "body-" + blk.role
        else:
            blk.role = "body"
        if blk.spans and blk.spans[0] and len(blk.spans[0]) == 1 and blk.spans[0][0].bold \
                and len(blk.text) < 120:
            blk.role = "lead"
            blk.keep_with_next = True
    elif blk.kind == "list":
        blk.role = "list"


# ------------------------------------------------------------------- loading

def load_document(book_dir: str = BOOK_DIR) -> Document:
    doc = Document()

    fm_path = os.path.join(book_dir, "00-front-matter.md")
    fm = io.open(fm_path, encoding="utf-8").read().split("\n")
    doc.front = parse_markdown(fm)

    chapters_dir = os.path.join(book_dir, "chapters")
    files = sorted(f for f in os.listdir(chapters_dir) if f.endswith(".md"))
    for fname in files:
        num = int(fname.split("-", 1)[0])
        lines = io.open(os.path.join(chapters_dir, fname), encoding="utf-8").read().split("\n")
        blocks = parse_markdown(lines)

        ch = Chapter(number=num, fa_title="", en_title="", file=fname)
        # chapter title = the first two H1s
        rest: list[Block] = []
        for blk in blocks:
            if blk.kind == "heading" and blk.level == 1 and not ch.fa_title and CH_FA_RE.match("# " + blk.text):
                mm = CH_FA_RE.match("# " + blk.text)
                ch.fa_title = mm.group(2).strip()
                continue
            if blk.kind == "heading" and blk.level == 1 and not ch.en_title and CH_EN_RE.match("# " + blk.text):
                mm = CH_EN_RE.match("# " + blk.text)
                ch.en_title = mm.group(2).strip()
                continue
            rest.append(blk)

        # split into: preamble (aim) / topics / review (chapter master table) /
        # self-assessment (appendix A) / reference-alignment audit (appendix B)
        topics: list[Topic] = []
        preamble: list[Block] = []
        cur: Optional[Topic] = None
        stop_at: Optional[int] = None
        for idx, blk in enumerate(rest):
            if blk.kind == "heading" and blk.level == 1 and TOPIC_RE.match("# " + blk.text):
                mm = TOPIC_RE.match("# " + blk.text)
                fa, en = _split_bilingual(mm.group(2))
                cur = Topic(number=mm.group(1), fa_title=fa, en_title=en, chapter=ch)
                topics.append(cur)
                continue
            # any other H1 (chapter review heading / audit banner) ends the topic flow,
            # and so does the chapter self-assessment heading
            if blk.kind == "heading" and blk.level == 1:
                stop_at = idx
                break
            if blk.kind == "heading" and blk.level == 2 and blk.text.startswith(CHAPTER_SA_HEAD):
                stop_at = idx
                break
            if cur is None:
                preamble.append(blk)
            else:
                cur.blocks.append(blk)
        if stop_at is not None:
            _split_tail(ch, rest[stop_at:])
        ch.blocks = preamble
        ch.topics = topics
        doc.chapters.append(ch)

    # drop trailing empty rules at the very end of a topic block list
    for ch in doc.chapters:
        for t in ch.topics:
            while t.blocks and t.blocks[-1].kind == "rule":
                t.blocks.pop()
    classify(doc)
    return doc


def _split_tail(ch: "Chapter", blocks: list) -> None:
    """Partition the chapter's closing material into review / self-assessment / audit."""
    sa_at = audit_at = None
    for i, blk in enumerate(blocks):
        if blk.kind == "heading" and blk.level == 2 and blk.text.startswith(CHAPTER_SA_HEAD) \
                and sa_at is None:
            sa_at = i
        elif blk.kind == "heading" and blk.level == 1 and "Reference Alignment Audit" in blk.text:
            audit_at = i
            break
    if audit_at is None:
        audit_at = len(blocks)
    if sa_at is None:
        sa_at = audit_at
    ch.review = blocks[:sa_at]
    ch.sa = blocks[sa_at:audit_at]
    ch.audit = blocks[audit_at:]
    ch.tail = list(ch.review) + list(ch.sa) + list(ch.audit)


def iter_raw_texts(blk: Block):
    """Yield the *source* strings of a block (no span splitting) — used by the QA checks
    so that the comparison sees exactly the characters of the manuscript."""
    if blk.kind in ("heading", "para", "diagram"):
        yield blk.text
    elif blk.kind == "list":
        for item in blk.items:
            yield item[2] if isinstance(item, tuple) else str(item)
    elif blk.kind == "callout":
        for item in blk.items:
            yield item[2] if isinstance(item, tuple) else str(item)
    elif blk.kind == "table":
        for cell in list(blk.header or []):
            yield cell
        for row in blk.rows or []:
            for cell in row:
                yield cell


def iter_texts(blk: Block):
    """Yield every text string carried by a block (for QA / preservation checks)."""
    if blk.kind == "heading" or blk.kind == "para" or blk.kind == "diagram":
        for spans in blk.spans:
            for s in spans:
                yield s.text
    elif blk.kind == "list":
        for item in blk.items:
            if isinstance(item, tuple):
                for s in parse_inline(item[2]):
                    yield s.text
            else:
                yield str(item)
    elif blk.kind == "callout":
        for item in blk.items:
            if isinstance(item, tuple):
                for s in parse_inline(item[2]):
                    yield s.text
            else:
                for s in parse_inline(str(item)):
                    yield s.text
    elif blk.kind == "table":
        for cell in list(blk.header or []):
            for s in parse_inline(cell):
                yield s.text
        for row in blk.rows or []:
            for cell in row:
                for s in parse_inline(cell):
                    yield s.text


# --------------------------------------------------------------------- stats

def stats(doc: Document) -> dict:
    topics = sum(len(c.topics) for c in doc.chapters)
    sections = 0
    for c in doc.chapters:
        for t in c.topics:
            sections += sum(1 for b in t.blocks if b.kind == "heading" and b.level == 2
                            and SECTION_RE.match("## " + b.text))
    tables = sum(1 for c in doc.chapters for t in c.topics for b in t.blocks if b.kind == "table")
    return dict(front_blocks=len(doc.front), chapters=len(doc.chapters), topics=topics,
                sections=sections, tables=tables)


if __name__ == "__main__":
    d = load_document()
    s = stats(d)
    print("stats:", s)
    for ch in d.chapters[:2]:
        print(f"\n== ch{ch.number}: {ch.fa_title} / {ch.en_title}")
        print("   preamble blocks:", len(ch.blocks), "topics:", len(ch.topics), "tail:", len(ch.tail))
        for t in ch.topics[:2]:
            kinds = {}
            for b in t.blocks:
                kinds[b.kind] = kinds.get(b.kind, 0) + 1
            print(f"   topic {t.number}: {t.fa_title} | {t.en_title} | {kinds}")
    ch = d.chapters[0]
    print("\nfirst preamble:", [b.kind + "/" + b.role for b in ch.blocks])
    print("tail:", [b.kind + "/" + b.role for b in ch.tail][:6])
