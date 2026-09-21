# -*- coding: utf-8 -*-
"""
fonts.py — font preparation for the print/digital PDF.

Why this exists
---------------
Typographic correctness in Dari requires the zero-width non-joiner (U+200C, نیم‌فاصله).
MuPDF's shaper replaces the ZWNJ glyph with the *space* glyph of the font, so a PDF text
layer cannot tell «می‌شود» (ZWNJ) from «می شود» (space): searching a ZWNJ word would fail.

Fix: before rendering we derive a copy of the Dari fonts in which an unused private-use
code point (U+E000) carries a blank, zero-advance glyph that behaves exactly like the ZWNJ
for the Arabic shaper.  The renderer then writes U+E000 instead of U+200C, and the PDF
ToUnicode maps that glyph back to U+200C.  The rendered glyphs (and therefore the visual
output) are unchanged; only the text layer becomes exact.

Derived files live in `assets/fonts/zwnj/` and are generated deterministically.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import design

ZWNJ = "\u200c"          # the real character used by the manuscript / DOCX / EPUB
ZWNJ_RENDER = "\ue000"   # the private-use stand-in used inside the PDF engine
DARI_FILES = ("Vazirmatn-Regular.ttf", "Vazirmatn-Medium.ttf",
              "Vazirmatn-SemiBold.ttf", "Vazirmatn-Bold.ttf")
DERIVED_DIR = os.path.join(design.FONT_DIR, "zwnj")

_configured = False


def _patch(src: str, dst: str, pua: int = 0xE000) -> str:
    from fontTools.ttLib import TTFont
    from fontTools.ttLib.tables._g_l_y_f import Glyph

    f = TTFont(src)
    name = f"uni{pua:04X}"
    if name not in f.getGlyphOrder():
        glyf = f["glyf"]
        glyf.glyphs[name] = Glyph()
        glyf.glyphs[name].numberOfContours = 0
        order = list(f.getGlyphOrder()) + [name]
        f.setGlyphOrder(order)
        f["hmtx"].metrics[name] = (0, 0)
        loca = getattr(glyf, "loca", None)
        if loca is not None:
            try:
                glyf.compile(f)
            except Exception:
                pass
        for t in f["cmap"].tables:
            if t.isUnicode():
                t.cmap[pua] = name
        if "post" in f and hasattr(f["post"], "glyphOrder"):
            f["post"].glyphOrder = f.getGlyphOrder()
    f.save(dst)
    return dst


def configure(verbose: bool = False) -> str:
    """Create (once) and return the directory holding the derived Dari fonts."""
    global _configured
    if _configured and os.path.isdir(DERIVED_DIR):
        return DERIVED_DIR
    os.makedirs(DERIVED_DIR, exist_ok=True)
    for fname in DARI_FILES:
        src = os.path.join(design.FONT_DIR, fname)
        dst = os.path.join(DERIVED_DIR, fname)
        if not os.path.exists(src):
            continue
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            _patch(src, dst)
            if verbose:
                print("  derived ZWNJ-safe font:", fname)
    # the PDF archive must see one directory holding every font: copy the rest in
    import shutil
    for files in design.FONTS.values():
        for path in files:
            base = os.path.basename(path)
            dst = os.path.join(DERIVED_DIR, base)
            if not os.path.exists(dst):
                shutil.copy2(path, dst)
    # renderers and the shaping map must use the derived copies
    for anchor, files in design.FONTS.items():
        design.FONTS[anchor] = [os.path.join(DERIVED_DIR, os.path.basename(p))
                                if os.path.exists(os.path.join(DERIVED_DIR, os.path.basename(p)))
                                else p for p in files]
    design.FONT_DIR_PDF = DERIVED_DIR
    _configured = True
    return DERIVED_DIR


if __name__ == "__main__":
    print(configure(verbose=True))
