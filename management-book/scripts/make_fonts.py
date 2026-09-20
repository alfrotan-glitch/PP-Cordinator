#!/usr/bin/env python3
"""
Build the symbol face used for arrows, ticks and bullets that the Dari text
faces do not contain. The glyphs come from DejaVu Sans (free licence, see
assets/fonts/LICENSE-fonts.txt); the result is a small dedicated face so that a
page never falls back to an unpredictable system font.
"""
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / 'assets/fonts'
SOURCE = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

CHARS = '→←↑↓\u21e9●★✓✗×■□◆◦•§±≤≥≈↺‹›·—…»«'


def main():
    f = TTFont(SOURCE)
    options = subset.Options()
    options.layout_features = ['*']
    options.name_IDs = ['*']
    options.notdef_outline = True
    options.recalc_bounds = True
    options.drop_tables = ['GSUB', 'GPOS', 'GDEF', 'kern', 'morx', 'kerx']
    sub = subset.Subsetter(options=options)
    sub.populate(text=CHARS)
    sub.subset(f)
    for rec in f['name'].names:
        if rec.nameID in (1, 4, 6, 16):
            try:
                rec.string = 'BookSymbols'
            except Exception:                                     # noqa: BLE001
                rec.string = 'BookSymbols'.encode('utf-16-be')
    f['head'].macStyle = 0
    out_ttf = FONTS / 'BookSymbols.ttf'
    f.save(out_ttf)
    f.flavor = 'woff2'
    f.save(FONTS / 'BookSymbols.woff2')
    print('symbols ->', out_ttf, f'{out_ttf.stat().st_size / 1024:.1f} KB')
    check = TTFont(out_ttf)
    cmap = check.getBestCmap()
    missing = [c for c in CHARS if ord(c) not in cmap]
    print('  glyphs:', len(check.getGlyphOrder()), 'missing:', ''.join(missing) or 'none')


if __name__ == '__main__':
    main()
