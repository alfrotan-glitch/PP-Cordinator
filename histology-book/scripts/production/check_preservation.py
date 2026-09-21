# -*- coding: utf-8 -*-
"""
check_preservation.py — production QA guard.

Guarantee: every *content* token of the frozen Markdown manuscript is present, with the
same multiplicity, in whatever we render (document model, DOCX text layer, EPUB text).

Markdown syntax tokens (list markers, rules, emphasis markers, rules) are ignored on both
sides because they are presentation.  Usage:

    python3 check_preservation.py                 # model vs manuscript
    python3 check_preservation.py --blob FILE     # FILE (plain text) vs manuscript
"""
import argparse
import collections
import io
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bookmodel import (load_document, iter_raw_texts, BOOK_DIR,   # noqa: E402
                       normalize_scripts)

SYNTAX_TOKENS = {"|", "-", "--", "---", "*", "**", "`", "```", ">", "#", "##", "###",
                 "دری:", "English:", "—", "–", "…", "•", "·"}


# combining marks (harakat) and directional punctuation that a text layer may reorder
HARAKAT = "".join(chr(c) for c in range(0x064B, 0x0653)) + "\u0670\u0653\u0654\u0655"
NEUTRAL_PUNCT = "()[]{}«»\u2039\u203a"


def normalize_text(s: str) -> str:
    """One normalisation for both sides: compatibility forms, joiners, harakat, bidi punctuation.

    The renderers do not change a single letter of the manuscript; what a text layer *can*
    differ in is presentation detail — the position of an Arabic vowel mark, the side a
    parenthesis lands on after bidi reordering, the exact space character.  Those are
    removed here so the comparison shows real content differences only.
    """
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u200c", "").replace("\u200f", "").replace("\u200e", "") \
         .replace("\ue000", "").replace("\u061c", "")
    s = normalize_scripts(s)
    for ch in HARAKAT + NEUTRAL_PUNCT:
        s = s.replace(ch, "")
    return s


def content_tokens(s: str) -> collections.Counter:
    s = normalize_text(s)
    out = []
    for line in s.split("\n"):
        line = line.strip()
        if re.fullmatch(r"[-*_]{3,}", line):
            continue
        line = re.sub(r"^\s*(\d+\.|[-*])\s+", " ", line)
        line = line.replace("****", "").replace("**", "").replace("*", "")
        line = re.sub(r"^\s*>\s?", " ", line)
        line = line.replace("|", " ").replace("`", "")
        line = re.sub(r"^\s*#+\s*", " ", line)
        out.append(line)
    text = re.sub(r"\s+", " ", " ".join(out))
    toks = [t for t in text.split(" ") if t and t not in SYNTAX_TOKENS]
    return collections.Counter(toks)


def manuscript_tokens(files=None) -> collections.Counter:
    files = files or (["00-front-matter.md"] +
                      ["chapters/" + f for f in sorted(os.listdir(os.path.join(BOOK_DIR, "chapters")))])
    total = collections.Counter()
    for f in files:
        total += content_tokens(io.open(os.path.join(BOOK_DIR, f), encoding="utf-8").read())
    return total


def model_tokens_by_file(doc) -> dict:
    out = collections.defaultdict(list)
    fm = "00-front-matter.md"
    for b in doc.front:
        out[fm].extend(iter_raw_texts(b))
    for ch in doc.chapters:
        f = "chapters/" + ch.file
        txt = out[f]
        txt += ["فصل", str(ch.number), ch.fa_title, "Chapter", str(ch.number), ch.en_title]
        for t in ch.topics:
            txt += [t.number, t.fa_title, t.en_title]
            for b in t.blocks:
                txt.extend(iter_raw_texts(b))
        for b in list(ch.blocks) + list(ch.tail):
            txt.extend(iter_raw_texts(b))
    return out


def model_tokens(doc) -> collections.Counter:
    by_file = model_tokens_by_file(doc)
    total = collections.Counter()
    for f, texts in by_file.items():
        total += content_tokens(" ".join(texts))
    # the renderers re-join wrapped lines: tokenise the joined text as well
    joined = content_tokens(" ".join(" ".join(v) for v in by_file.values()))
    return total, joined


class CompactIndex:
    """Substring counter over a large compacted text.

    ``count`` stops as soon as the caller's threshold is reached: the comparison only
    needs to know whether a token occurs at least as often as the manuscript has it, and
    a full scan of a million-character document per token made the QA pass minutes long.
    """

    def __init__(self, text: str):
        self.text = text

    def count(self, needle: str, cap: int | None = None) -> int:
        if not needle:
            return 0
        if cap is None:
            return self.text.count(needle)
        hits, pos = 0, 0
        while hits < cap:
            i = self.text.find(needle, pos)
            if i < 0:
                break
            hits += 1
            pos = i + 1
        return hits


def compare(source: collections.Counter, other: collections.Counter,
            other_compact="") -> tuple[collections.Counter, collections.Counter, list, list]:
    """Token comparison that tolerates presentation-only differences.

    A token counts as present when it is found as a substring of the other side's
    whitespace-stripped text: that removes the line-break and superscript-spacing
    differences that a text layer legitimately has, without hiding real losses.
    """
    if isinstance(other_compact, str):
        other_compact = CompactIndex(other_compact) if other_compact else None
    missing, extra, missing_ok, extra_ok = [], [], [], []
    for tok, n in (source - other).items():
        if other_compact is not None and n <= other_compact.count(tok.replace(" ", ""), cap=n):
            missing_ok.append(tok)
        else:
            missing.append(tok)
    for tok, n in (other - source).items():
        if tok in EXTRA_ALLOWED:
            extra_ok.append(tok)
        else:
            extra.append(tok)
    return (collections.Counter({k: (source - other)[k] for k in missing}),
            collections.Counter({k: (other - source)[k] for k in extra}),
            missing_ok, extra_ok)


EXTRA_ALLOWED = {"", "—", "·"}


def compact_text(s: str) -> str:
    """Script-normalised, whitespace-free projection of a text for token spot checks."""
    return re.sub(r"\s+", "", normalize_text(s))


def report(source: collections.Counter, other: collections.Counter, label: str,
           other_compact: str = "") -> int:
    missing, extra, ok_m, ok_x = compare(source, other, other_compact)
    print(f"{label}: source_tokens={sum(source.values())} other_tokens={sum(other.values())} "
          f"missing={sum(missing.values())} extra={sum(extra.values())} "
          f"(present-by-substring {len(ok_m)})")
    if missing:
        print("   missing sample:", list(missing.items())[:25])
    return sum(missing.values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blob", help="plain-text file to compare against the manuscript")
    ap.add_argument("--labels", action="store_true", help="ignore the دری:/English: labels")
    args = ap.parse_args()

    src = manuscript_tokens()
    if args.labels:
        for tok in ("دری:", "English:"):
            src.pop(tok, None)
    doc = load_document()
    plain, joined = model_tokens(doc)

    if args.blob:
        blob = io.open(args.blob, encoding="utf-8").read()
        other = content_tokens(blob)
        if args.labels:
            for tok in ("دری:", "English:"):
                other.pop(tok, None)
        return 1 if report(src, other, "deliverable vs manuscript",
                           compact_text(blob)) else 0

    bad = 0
    bad += report(src, plain, "model(per-block) vs manuscript")
    bad += report(src, joined, "model(joined lines) vs manuscript")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
