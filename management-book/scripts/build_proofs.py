#!/usr/bin/env python3
"""
Page proofs - the real book text, laid out on 17x24 cm print pages.

Instead of sample filler, this engine renders the actual manuscript (heads,
body, tables with many columns, callout boxes, flow strips, exam items, the
glossary, the quick review and the cover) at the interior's real type sizes and
colours, so the layout can be inspected page by page on 150 dpi proofs and in a
single PDF. A dark-mode page shows the night palette of the same design.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

import bookkit as bk
import mgmtgen
from mgmtgen import ROOT, split_documents

OUT = ROOT / 'qa' / 'proof'
DPI = 150
CM = DPI / 2.54
W, H = int(17 * CM), int(24 * CM)
MARGIN_SIDE = int(1.7 * CM)
MARGIN_TOP = int(1.75 * CM)
MARGIN_BOTTOM = int(1.9 * CM)
TEXT_W = W - 2 * MARGIN_SIDE

LIGHT = dict(
    paper=(255, 255, 255, 255), ink=(27, 36, 48, 255), soft=(74, 83, 97, 255),
    rule=(219, 221, 214, 255), accent=(19, 84, 76, 255), navy=(29, 51, 88, 255),
    panel=(247, 246, 242, 255), table_head=(232, 240, 239, 255),
    table_alt=(249, 249, 247, 255), warn=(163, 66, 56, 255), gold=(118, 93, 22, 255),
)
DARK = dict(
    paper=(19, 21, 25, 255), ink=(233, 231, 226, 255), soft=(178, 183, 191, 255),
    rule=(54, 59, 67, 255), accent=(119, 201, 180, 255), navy=(200, 218, 240, 255),
    panel=(27, 30, 36, 255), table_head=(31, 42, 44, 255), table_alt=(23, 26, 31, 255),
    warn=(214, 136, 122, 255), gold=(212, 185, 104, 255),
)

def plain(text: str) -> str:
    """Proof pages show emphasis through the typeface, not through markers."""
    return text.replace('**', '').replace('*', '')


BODY = 21.9          # 10.5 pt at 150 dpi
H1, H2, H3, CAP = 34.0, 26.5, 23.0, 17.0
TITLES = mgmtgen.CALLOUTS


class Page:
    def __init__(self, colours, footer=''):
        self.c = colours
        self.img = Image.new('RGBA', (W, H), colours['paper'])
        self.y = MARGIN_TOP
        self.footer = footer
        self.inset = 0
        self.frozen = False        # while a panel is being drawn, never break the page
        self.on_break = None       # called before a new page is started

    @property
    def right(self):
        return W - MARGIN_SIDE - self.inset

    @property
    def tw(self):
        return TEXT_W - 2 * self.inset

    def space(self, px):
        self.y += px

    def new_page(self):
        self.finish()
        if self.on_break:
            self.on_break()
        self.img = Image.new('RGBA', (W, H), self.c['paper'])
        self.y = MARGIN_TOP

    def finish(self):
        if not self.footer:
            return
        f = bk.font(CAP, 'body')
        bk.draw_line(self.img, W - MARGIN_SIDE, H - 34, self.footer, f, self.c['soft'], 'rtl')

    def room(self, needed):
        if self.frozen:
            return False
        if self.y + needed > H - MARGIN_BOTTOM:
            self.new_page()
            return True
        return False

    # ------------------------------------------------------------------ text
    def heading(self, text, level=1):
        f = bk.font({1: H1, 2: H2, 3: H3}[level], 'display')
        colour = {1: self.c['navy'], 2: self.c['accent'], 3: self.c['soft']}[level]
        lines = bk.wrap(text, f, self.tw, 'rtl')
        self.room(len(lines) * f.line_height * 1.5 + (34 if level == 1 else 20))
        if level == 1:
            self.space(16)
        for ln in lines:
            self.y += f.line_height * 1.16
            bk.draw_line(self.img, self.right, self.y, ln, f, colour, 'rtl')
            self.y += f.line_height * 0.34
        if level == 1:
            draw = ImageDraw.Draw(self.img)
            draw.line([MARGIN_SIDE, self.y + 9, W - MARGIN_SIDE, self.y + 9],
                      fill=self.c['accent'], width=2)
            self.space(18)
        self.space(6)

    def para(self, text):
        text = plain(text)
        f = bk.font(BODY, 'body')
        lines = bk.wrap(text, f, self.tw, 'rtl')
        self.room(len(lines) * f.line_height * 1.62 + 8)
        self.y = bk.draw_block(self.img, self.right, self.y, self.tw, text, f,
                               self.c['ink'], 'rtl', line_height=f.line_height * 1.62)
        self.space(7)

    def items(self, values, ordered=False, markers=None):
        f = bk.font(BODY, 'body')
        for n, item in enumerate(values, 0):
            prefix = f'{markers[n]}. ' if markers else f'{n + 1}. '
            if not ordered:
                prefix = '•  '
            parts = [plain(x) for x in item.split('\n')]
            first = bk.wrap(prefix + parts[0], f, self.tw - 26, 'rtl')
            rest = [ln for part in parts[1:]
                    for ln in bk.wrap(part, f, self.tw - 40, 'rtl')]
            self.room((len(first) + len(rest)) * f.line_height * 1.5 + 6)
            for i, ln in enumerate(first):
                self.y += f.line_height * 1.12
                bk.draw_line(self.img, self.right - 14, self.y, ln, f, self.c['ink'], 'rtl')
                self.y += f.line_height * 0.44
            for ln in rest:
                self.y += f.line_height * 1.08
                bk.draw_line(self.img, self.right - 40, self.y, ln, f, self.c['ink'], 'rtl')
                self.y += f.line_height * 0.42
            self.space(4)

    def flow(self, text):
        text = plain(text)
        f = bk.font(BODY, 'body')
        lines = bk.wrap(text, f, self.tw, 'rtl')
        self.room(len(lines) * f.line_height * 1.6 + 16)
        self.space(8)
        for ln in lines:
            self.y += f.line_height * 1.2
            x = self.right - (self.tw - bk.measure(ln, 'rtl', f)) / 2
            bk.draw_line(self.img, x, self.y, ln, f, self.c['accent'], 'rtl')
            self.y += f.line_height * 0.42
        self.space(12)

    def quote(self, text):
        text = plain(text)
        f = bk.font(BODY * 0.97, 'body')
        lines = bk.wrap(text, f, self.tw - 30, 'rtl')
        self.room(len(lines) * f.line_height * 1.6 + 18)
        top = self.y
        self.space(8)
        for ln in lines:
            self.y += f.line_height * 1.2
            bk.draw_line(self.img, self.right - 16, self.y, ln, f, self.c['soft'], 'rtl')
            self.y += f.line_height * 0.42
        draw = ImageDraw.Draw(self.img)
        draw.line([self.right, top, self.right, self.y], fill=self.c['rule'], width=3)
        self.space(12)

    def table(self, rows, split=False):
        f = bk.font(BODY * 0.95, 'body')
        rows = [r for r in rows if r]
        if not rows:
            return
        head, rest = rows[0], rows[1:]
        while True:
            batch, used = [], 0
            for r in rest:
                est = bk.row_height(r, f, self.tw, 'rtl') + 12
                if self.y + used + est > H - MARGIN_BOTTOM and batch:
                    break
                batch.append(r)
                used += est
            self.y = bk.table(self.img, self.right, self.y, self.tw, [head] + batch, f,
                              self.c, 'rtl')
            rest = rest[len(batch):]
            if not rest or not split:
                break
            self.new_page()
            self.space(6)
        self.space(14)

    def measure(self, kind, payload, width=None):
        """Height a block would take, measured on a throwaway page."""
        scratch = Page(self.c, '')
        scratch.inset = self.inset
        scratch.frozen = True
        scratch.on_break = None
        scratch.y = MARGIN_TOP
        drawer = {'para': lambda pg: pg.para(payload),
                  'bullet': lambda pg: pg.items(payload[0], markers=payload[1]),
                  'olist': lambda pg: pg.items(payload[0], ordered=True,
                                               markers=payload[1]),
                  'table': lambda pg: pg.table(payload),
                  'h3': lambda pg: pg.heading(payload, 3),
                  'flow': lambda pg: pg.flow(payload)}[kind]
        drawer(scratch)
        return scratch.y - MARGIN_TOP

    def callout(self, ctype, title, blocks):
        """A callout box; long boxes continue on the next page in a fresh panel."""
        pad = 20
        accent = {'warn': self.c['warn'], 'decision': self.c['gold'],
                  'case': self.c['navy']}.get(ctype, self.c['accent'])
        head_f = bk.font(BODY * 1.02, 'display')
        total = sum(self.measure(*b) for b in blocks)
        remaining = list(blocks)
        first = True
        while remaining:
            start = self.y + 14
            layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            real, self.img, self.inset = self.img, layer, pad
            self.frozen = True
            self.y = start + pad
            label = title if first else title + ' — ادامه'
            bk.draw_line(layer, self.right, self.y + head_f.ascender, label, head_f,
                         accent, 'rtl')
            self.y += head_f.line_height * 1.25 + 8
            drew = []
            while remaining:
                b = remaining[0]
                h = self.measure(*b)
                if self.y + h > H - MARGIN_BOTTOM - pad and drew:
                    break
                kind, payload = b
                if kind == 'para':
                    self.para(payload)
                elif kind == 'bullet':
                    self.items(payload[0], markers=payload[1])
                elif kind == 'olist':
                    self.items(payload[0], ordered=True, markers=payload[1])
                elif kind == 'table':
                    self.table(payload)
                elif kind == 'h3':
                    self.heading(payload, 3)
                elif kind == 'flow':
                    self.flow(payload)
                drew.append(b)
                remaining = remaining[1:]
                if self.y > H - MARGIN_BOTTOM - pad:
                    break
            self.y += pad
            self.img, self.inset, self.frozen = real, 0, False
            draw = ImageDraw.Draw(real)
            draw.rounded_rectangle([MARGIN_SIDE, start, W - MARGIN_SIDE, self.y],
                                   radius=10, fill=self.c['panel'], outline=self.c['rule'])
            draw.rectangle([W - MARGIN_SIDE - 6, start + 2, W - MARGIN_SIDE - 1, self.y - 2],
                           fill=accent)
            real.alpha_composite(layer)
            self.space(18)
            first = False
            if remaining:
                self.new_page()


def render(blocks, footer, colours, limit_pages=1):
    pages = []
    page = Page(colours, footer)

    def flush():
        page.finish()
        pages.append(page.img)

    page.on_break = flush

    for b in blocks:
        if len(pages) >= limit_pages:
            break
        if b.kind == 'h1':
            if page.y > MARGIN_TOP + 10:
                page.new_page()
            page.heading(b.text, 1)
        elif b.kind == 'h2':
            page.heading(b.text, 2)
        elif b.kind == 'h3':
            page.heading(b.text, 3)
        elif b.kind == 'para':
            page.para(b.text + ''.join(' ' + x for x in b.lines))
        elif b.kind == 'bullet':
            page.items(b.items, markers=None)
        elif b.kind == 'olist':
            page.items(b.items, ordered=True, markers=b.markers or None)
        elif b.kind == 'table':
            page.table(b.items, split=True)
        elif b.kind == 'flow':
            page.flow(b.text)
        elif b.kind == 'quote':
            page.quote(b.text)
        elif b.kind == 'callout':
            def wrap_block(x):
                if x.kind == 'para':
                    return (x.kind, x.text + ''.join(' ' + y for y in x.lines))
                if x.kind in ('bullet', 'olist'):
                    return (x.kind, (x.items, x.markers or None))
                if x.kind == 'table':
                    return (x.kind, x.items)
                return (x.kind, x.text)

            body = [wrap_block(x) for x in b.items]
            label = TITLES.get(b.ctype, b.ctype)
            title = f'{label} — {b.ctitle}' if b.ctitle else label
            page.callout(b.ctype, title, body)
        if page.y > H - MARGIN_BOTTOM:
            page.new_page()
    if len(pages) < limit_pages:
        flush()
    return pages


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    docs = split_documents(mgmtgen.parse(mgmtgen.MASTER))
    by_title = {d['title']: d for d in docs}

    all_blocks = mgmtgen.parse(mgmtgen.MASTER)

    def pick(prefix, limit=60):
        """Blocks of one chapter, case or tool section, starting at the heading."""
        begin = None
        for i, b in enumerate(all_blocks):
            if b.kind in ('h1', 'h2') and b.text.startswith(prefix):
                begin = i
                break
        if begin is None:
            raise SystemExit(f'proof target not found: {prefix}')
        level = all_blocks[begin].kind
        out = []
        for b in all_blocks[begin:begin + limit]:
            if out and b.kind in ('h1', 'h2') and not (level == 'h2' and b.kind == 'h1'):
                break
            out.append(b)
        return out

    pages = []          # (name, PIL image, footer)

    # 1. cover
    cover = Image.open(ROOT / 'assets' / 'cover.jpg').convert('RGB')
    cw, ch = int(W * 0.8), int(H * 0.8)
    canvas = Image.new('RGB', (W, H), (243, 242, 238))
    canvas.paste(cover.resize((cw, ch), Image.LANCZOS), ((W - cw) // 2, (H - ch) // 2))
    pages.append(('01_cover', canvas, ''))

    specs = [
        ('02_chapter', 'فصل 4', 'فصل 4 — تصمیم‌گیری'),
        ('03_structure', 'فصل 7', 'فصل 7 — ساختار سازمانی'),
        ('04_case', 'کیس 1 —', 'کیس‌های مدیریتی'),
        ('05_tools', 'ابزار 1', 'بستهٔ ابزارها'),
        ('06_exam', 'بخش یکم —', 'کارگاه تمرین'),
        ('07_glossary', 'پیوست 1', 'پیوست 1 — واژه‌نامه'),
        ('08_review', 'پیوست 3', 'پیوست 3 — مرور سریع'),
    ]
    for name, start, footer in specs:
        blocks = pick(start)
        imgs = render(blocks, footer, LIGHT, limit_pages=1)
        pages.append((name, imgs[0].convert('RGB'), footer))

    # dark mode: the same design in the night palette, on the chapter-4 opening
    dark_imgs = render(pick('فصل 4'), 'حالت شبانه', DARK, limit_pages=1)
    pages.append(('09_dark_mode', dark_imgs[0].convert('RGB'), ''))

    for name, img, _ in pages:
        img.save(OUT / f'{name}.png')

    pdf = OUT / 'صفحه‌آرایی_نمونه.pdf'
    imgs = [p[1] for p in pages]
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=DPI, quality=88)
    print(f'proofs -> {OUT} ({len(pages)} pages) · {pdf.name}')
    for name, img, _ in pages:
        print(f'    {name}.png  {img.width}x{img.height}')


if __name__ == '__main__':
    main()
