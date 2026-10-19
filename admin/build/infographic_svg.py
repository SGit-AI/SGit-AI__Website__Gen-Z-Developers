#!/usr/bin/env python3
"""The infographics' drawing: a JSON spec in, a standalone SVG out. No browser, no library, no image model: the same
spec always gives the same file, so an infographic is corrected by changing a line of data and rebuilding.

An infographic is a printed picture, the way a storyboard panel is: it keeps its own colours in every theme of the
site (the book's cover palette on cream paper), and the SVG the site shows is the file that goes into the PDF.

    python3 admin/build/infographic_svg.py admin/content/infographics/drawn/<id>.json   # writes the SVG to stdout

Forms drawn so far (a proposal may name any form in plan.json; these are the ones the code can draw today):
  comparison  columns of items; an item can be kept, new or gone (struck through)
  flow        numbered steps, left to right, wrapping into rows
  cycle       steps around a loop, with a centre
  spectrum    a line of stops, from one end to the other
  quadrant    two axes, four cells
  stack       layers, top to bottom
  numbers     big numbers, with operators between them for worked arithmetic
  checklist   boxes to tick
  graph       nodes on a grid, labelled edges, zones that hold them (also an architecture)
  bookmap     the whole book on one page, drawn from the release candidate's data (computed, not authored)
"""
import json
import sys
from xml.sax.saxutils import escape

# ------------------------------------------------------------------ the palette: the cover's, on the storyboards' paper
PAPER = "#fbf7ee"
INK = "#23262b"
DIM = "#5c5f66"
FAINT = "#9a9ca1"
NAVY = "#0c2a3d"
CARD = "#ffffff"
COVER = {"green": "#7bc08f", "yellow": "#e8b64a", "teal": "#3b9fb0", "red": "#e5625b", "navy": NAVY}
SOFT = {"green": "#e4f2e8", "yellow": "#fbf0d6", "teal": "#dceef2", "red": "#fbe2e0", "navy": "#dfe6ec", "grey": "#eeece6"}
DEEP = {"green": "#2f6b40", "yellow": "#7a5a12", "teal": "#1d5f6b", "red": "#9c2f29", "navy": NAVY, "grey": DIM}
STROKE = dict(COVER, grey="#b9b4a6")
ORDER = ("teal", "green", "yellow", "red", "navy")
FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"

W = 1600
M = 64

# ------------------------------------------------------------------ text
_NARROW = set("ilI.,:;'|!tfj()[]{} ")
_WIDE = set("mwMW@%")


def text_width(s, size, bold=False):
    w = 0.0
    for ch in s:
        if ch in _NARROW:
            w += 0.30
        elif ch in _WIDE:
            w += 0.86
        elif ch.isupper() or ch.isdigit():
            w += 0.64
        else:
            w += 0.53
    return w * size * (1.07 if bold else 1.0) * 1.07


def wrap(s, size, width, bold=False):
    """Greedy word wrap by estimated width. A word longer than the line keeps its own line."""
    out, cur = [], ""
    for word in str(s).split():
        trial = f"{cur} {word}" if cur else word
        if cur and text_width(trial, size, bold) > width:
            out.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out or [""]


def text(x, y, lines, size, fill=INK, bold=False, anchor="start", lh=1.25, italic=False, strike=False, extra=""):
    """Lines of text whose first baseline is y. Returns (svg, height used)."""
    if isinstance(lines, str):
        lines = [lines]
    attrs = f'font-size="{size}" fill="{fill}"' + (' font-weight="700"' if bold else "") + (' font-style="italic"' if italic else "")
    attrs += f' text-anchor="{anchor}"' if anchor != "start" else ""
    attrs += ' text-decoration="line-through"' if strike else ""
    spans = "".join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * lh:.1f}">{escape(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{x:.1f}" y="{y:.1f}" {attrs}{extra}>{spans}</text>', size * lh * len(lines)


def block_height(label, detail, width, ls=26, ds=19):
    h = len(wrap(label, ls, width, True)) * ls * 1.22
    if detail:
        h += 8 + len(wrap(detail, ds, width)) * ds * 1.3
    return h


def label_detail(x, y, label, detail, width, ls=26, ds=19, colour=INK, anchor="start", strike=False):
    """A bold label and a wrapped detail under it; returns (svg, height)."""
    s1, h1 = text(x, y + ls, wrap(label, ls, width, True), ls, fill=colour, bold=True, anchor=anchor, lh=1.22, strike=strike)
    if not detail:
        return s1, h1 + ls * 0.25
    s2, h2 = text(x, y + h1 + 8 + ds, wrap(detail, ds, width), ds, fill=DIM if not strike else FAINT, anchor=anchor, lh=1.3)
    return s1 + s2, h1 + 8 + h2


def rect(x, y, w, h, fill=CARD, stroke=INK, sw=2, r=14, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def arrow(x1, y1, x2, y2, colour=INK, sw=3, dashed=False):
    d = ' stroke-dasharray="10 8"' if dashed else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{colour}" stroke-width="{sw}"{d} marker-end="url(#ah)"/>'


def colour_of(item, i):
    c = item.get("colour") if isinstance(item, dict) else None
    return c if c in COVER or c == "grey" else ORDER[i % len(ORDER)]


# ------------------------------------------------------------------ the frame every infographic shares
def header(spec):
    out = []
    x = M
    for i, c in enumerate(("green", "yellow", "teal", "red")):
        out.append(f'<rect x="{x + i * 22}" y="{M - 6}" width="16" height="16" rx="2" fill="{COVER[c]}"/>')
    k, _ = text(M + 100, M + 8, spec.get("kicker", "").upper(), 17, fill=DEEP["teal"], bold=True, extra=' letter-spacing="1.5"')
    out.append(k)
    y = M + 30
    t, h = text(M, y + 50, wrap(spec["title"], 50, W - 2 * M, True), 50, fill=NAVY, bold=True, lh=1.12)
    out.append(t)
    y += h + 14
    if spec.get("subtitle"):
        s, h = text(M, y + 25, wrap(spec["subtitle"], 25, W - 2 * M - 120), 25, fill=DIM, lh=1.32)
        out.append(s)
        y += h + 4
    return "".join(out), y + 30


def footer(spec, y):
    src = spec.get("source_line", "")
    lines = wrap(src, 17, W - 2 * M - 520)
    s1, h = text(M, y + 40, lines, 17, fill=DIM, lh=1.35)
    state = spec.get("stamp", "drafted by code, not reviewed")
    s2, _ = text(W - M, y + 40, [f"gen-z-developers.sgit.ai/infographics", f"{spec['id']} · {state}"], 17, fill=FAINT, anchor="end", lh=1.35)
    line = f'<line x1="{M}" y1="{y + 8}" x2="{W - M}" y2="{y + 8}" stroke="#d9d4c5" stroke-width="2"/>'
    return line + s1 + s2, max(h, 46) + 56


def document(spec, body, body_h, top):
    foot, fh = footer(spec, top + body_h + 20)
    hgt = int(top + body_h + 20 + fh)
    head, _ = header(spec)
    alt = escape(spec.get("alt") or spec["title"], {'"': "&quot;"})
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {hgt}" width="{W}" height="{hgt}" role="img" aria-label="{alt}" font-family="{FONT}">\n'
            f'<title>{escape(spec["title"])}</title>\n<desc>{escape(spec.get("alt", ""))}</desc>\n'
            f'<defs><marker id="ah" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
            f'<path d="M1,1 L11,6 L1,11 z" fill="{INK}"/></marker></defs>\n'
            f'<rect width="{W}" height="{hgt}" fill="{PAPER}"/>\n{head}\n{body}\n{foot}\n</svg>\n')


# ------------------------------------------------------------------ the forms
def form_comparison(spec, top):
    cols = spec["columns"]
    n = len(cols)
    gap = 64 if spec.get("arrows", True) else 28
    cw = (W - 2 * M - gap * (n - 1)) / n
    inner = cw - 44
    # the heights, so the columns line up row by row
    rows = max(len(c["items"]) for c in cols)
    ih = lambda it: block_height(it["label"], it.get("detail"), inner - 30 - (70 if it.get("state") == "new" else 0), 24, 18) + 26
    # aligned, every row as tall as its tallest cell (a before and after); or each column on its own (a stack per column)
    aligned = spec.get("align_rows", True)
    row_h = [max(ih(c["items"][r]) for c in cols if r < len(c["items"])) for r in range(rows)]
    head_h = max(block_height(c["heading"], c.get("sub"), cw - 40, 30, 19) for c in cols) + 34
    out = []
    heights = lambda c: row_h[:len(c["items"])] if aligned else [ih(it) for it in c["items"]]
    total = max(sum(heights(c)) + 14 * len(c["items"]) for c in cols) + head_h + 24
    for i, c in enumerate(cols):
        x = M + i * (cw + gap)
        col = colour_of(c, i)
        out.append(rect(x, top, cw, total, fill=SOFT[col], stroke=STROKE[col] if col != "navy" else NAVY, sw=2.5, r=18))
        s, _ = label_detail(x + 22, top + 14, c["heading"], c.get("sub"), cw - 40, 30, 19, colour=DEEP[col])
        out.append(s)
        y = top + head_h
        hs = heights(c)
        for r, it in enumerate(c["items"]):
            st = it.get("state", "kept")
            fill = CARD if st != "gone" else "#f6f4ee"
            stroke = INK if st == "new" else "#cfcabb"
            out.append(rect(x + 18, y, cw - 36, hs[r], fill=fill, stroke=stroke, sw=2.4 if st == "new" else 1.6, r=10))
            if st == "new":
                out.append(f'<rect x="{x + 18}" y="{y}" width="8" height="{hs[r]:.1f}" rx="3" fill="{STROKE[col] if col != "navy" else COVER["teal"]}"/>')
                tag_w = 58
                out.append(rect(x + cw - 18 - tag_w - 10, y + 10, tag_w, 26, fill=NAVY, stroke=NAVY, sw=1, r=13))
                out.append(text(x + cw - 18 - tag_w / 2 - 10, y + 29, "NEW", 14, fill="#ffffff", bold=True, anchor="middle")[0])
            s, _ = label_detail(x + 40, y + 6, it["label"], it.get("detail"), inner - 30 - (70 if st == "new" else 0), 24, 18,
                                colour=FAINT if st == "gone" else INK, strike=st == "gone")
            out.append(s)
            y += hs[r] + 14
        if spec.get("arrows", True) and i < n - 1:
            ay = top + head_h / 2
            out.append(arrow(x + cw + 8, ay, x + cw + gap - 8, ay, sw=4))
    h = total
    if spec.get("legend"):
        lg, lh = text(M, top + total + 40, wrap(spec["legend"], 19, W - 2 * M), 19, fill=DIM, italic=True)
        out.append(lg)
        h += lh + 24
    return "".join(out), h


def form_flow(spec, top):
    steps = spec["steps"]
    per = spec.get("per_row") or min(len(steps), 4 if len(steps) != 5 else 5)
    gap = 54
    cw = (W - 2 * M - gap * (per - 1)) / per
    out, y = [], top
    for r0 in range(0, len(steps), per):
        row = steps[r0:r0 + per]
        hh = max(block_height(s["label"], s.get("detail"), cw - 44, 25, 19) for s in row) + 92
        for j, s in enumerate(row):
            i = r0 + j
            x = M + j * (cw + gap)
            col = colour_of(s, i) if spec.get("colours", "cycle") == "cycle" else spec.get("colours")
            out.append(rect(x, y, cw, hh, fill=CARD, stroke=INK, sw=2.2, r=16))
            out.append(f'<rect x="{x}" y="{y}" width="{cw:.1f}" height="10" rx="5" fill="{STROKE[col]}"/>')
            out.append(f'<circle cx="{x + 40}" cy="{y + 48}" r="22" fill="{STROKE[col]}"/>')
            out.append(text(x + 40, y + 56, str(s.get("n", i + 1)), 22, fill="#ffffff" if col in ("navy", "teal", "red") else INK, bold=True, anchor="middle")[0])
            sv, _ = label_detail(x + 22, y + 76, s["label"], s.get("detail"), cw - 44, 25, 19)
            out.append(sv)
            if j < len(row) - 1:
                out.append(arrow(x + cw + 6, y + hh / 2, x + cw + gap - 6, y + hh / 2, sw=3.5))
        y += hh
        if r0 + per < len(steps):
            # the turn to the next row
            xr = M + (len(row) - 1) * (cw + gap) + cw / 2
            out.append(f'<path d="M{xr:.1f},{y + 4} C{xr:.1f},{y + 40} {M + cw / 2:.1f},{y + 20} {M + cw / 2:.1f},{y + 58}" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#ah)"/>')
            y += 70
    h = y - top
    if spec.get("outcome"):
        o = spec["outcome"]
        oh = block_height(o["label"], o.get("detail"), W - 2 * M - 80, 27, 20) + 36
        out.append(rect(M, y + 34, W - 2 * M, oh, fill=SOFT["navy"], stroke=NAVY, sw=2.5, r=16))
        sv, _ = label_detail(M + 40, y + 46, o["label"], o.get("detail"), W - 2 * M - 80, 27, 20, colour=NAVY)
        out.append(sv)
        h += oh + 34
    return "".join(out), h


def form_cycle(spec, top):
    import math
    steps = spec["steps"]
    n = len(steps)
    R = spec.get("radius", 300)
    cx, cy = W / 2, top + R + 110
    cw = 330
    out = []
    pos = []
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        pos.append((cx + R * 1.8 * math.cos(a), cy + R * math.sin(a)))
    # the loop's arrows, between the cards, on an ellipse
    for i in range(n):
        a1 = -math.pi / 2 + 2 * math.pi * (i + 0.30) / n
        a2 = -math.pi / 2 + 2 * math.pi * (i + 0.70) / n
        x1, y1 = cx + R * 1.8 * math.cos(a1), cy + R * math.sin(a1)
        x2, y2 = cx + R * 1.8 * math.cos(a2), cy + R * math.sin(a2)
        out.append(f'<path d="M{x1:.1f},{y1:.1f} A{R * 1.8:.1f},{R:.1f} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{INK}" stroke-width="3.5" marker-end="url(#ah)"/>')
    if spec.get("centre"):
        c = spec["centre"]
        ch = block_height(c["label"], c.get("detail"), 350, 30, 20) + 40
        out.append(rect(cx - 200, cy - ch / 2, 400, ch, fill=NAVY, stroke=NAVY, r=22))
        sv, _ = label_detail(cx, cy - ch / 2 + 14, c["label"], c.get("detail"), 350, 30, 20, colour="#ffffff", anchor="middle")
        out.append(sv.replace(f'fill="{DIM}"', 'fill="#cfe0ea"'))
    for i, (s, (x, y)) in enumerate(zip(steps, pos)):
        col = colour_of(s, i)
        hh = block_height(s["label"], s.get("detail"), cw - 40, 25, 18) + 58
        out.append(rect(x - cw / 2, y - hh / 2, cw, hh, fill=CARD, stroke=STROKE[col], sw=3.5, r=16))
        out.append(f'<circle cx="{x - cw / 2 + 4}" cy="{y - hh / 2 + 4}" r="20" fill="{STROKE[col]}"/>')
        out.append(text(x - cw / 2 + 4, y - hh / 2 + 11, str(i + 1), 20, fill="#ffffff" if col in ("navy", "teal", "red") else INK, bold=True, anchor="middle")[0])
        sv, _ = label_detail(x, y - hh / 2 + 14, s["label"], s.get("detail"), cw - 40, 25, 18, anchor="middle")
        out.append(sv)
    return "".join(out), 2 * R + 220


def form_spectrum(spec, top):
    stops = spec["stops"]
    n = len(stops)
    x0, x1 = M + 120, W - M - 120
    ly = top + 70
    out = []
    ends = spec.get("ends", ["", ""])
    out.append(text(M, ly - 34, ends[0], 20, fill=DIM, bold=True)[0])
    out.append(text(W - M, ly - 34, ends[1], 20, fill=DIM, bold=True, anchor="end")[0])
    out.append(f'<line x1="{M}" y1="{ly}" x2="{W - M}" y2="{ly}" stroke="{INK}" stroke-width="5" marker-end="url(#ah)" marker-start="url(#ah)"/>')
    cw = min(360, (x1 - x0) / max(n - 1, 1) - 24) if n > 1 else 400
    hmax = 0
    for i, s in enumerate(stops):
        x = x0 + (x1 - x0) * (s.get("at", i / max(n - 1, 1)))
        col = colour_of(s, i)
        out.append(f'<circle cx="{x:.1f}" cy="{ly}" r="26" fill="{STROKE[col]}" stroke="{INK}" stroke-width="2.5"/>')
        hh = block_height(s["label"], s.get("detail"), cw - 30, 26, 19) + 34
        hmax = max(hmax, hh)
        out.append(f'<line x1="{x:.1f}" y1="{ly + 26}" x2="{x:.1f}" y2="{ly + 62}" stroke="{INK}" stroke-width="2"/>')
        out.append(rect(x - cw / 2, ly + 62, cw, hh, fill=SOFT[col], stroke=STROKE[col], sw=2.5, r=14))
        sv, _ = label_detail(x, ly + 72, s["label"], s.get("detail"), cw - 30, 26, 19, colour=DEEP[col], anchor="middle")
        out.append(sv)
    h = 62 + hmax + 70
    if spec.get("question"):
        q, qh = text(W / 2, top + h + 20, wrap(spec["question"], 30, W - 2 * M - 200, True), 30, fill=NAVY, bold=True, anchor="middle")
        out.append(q)
        h += qh + 20
    return "".join(out), h


def form_quadrant(spec, top):
    cells = spec["cells"]  # top-left, top-right, bottom-left, bottom-right
    gx, gy = M + 70, top + 10
    gw, gh = W - 2 * M - 70, spec.get("height", 720)
    cw, chh = gw / 2, gh / 2
    out = []
    for i, c in enumerate(cells):
        x = gx + (i % 2) * cw
        y = gy + (i // 2) * chh
        col = colour_of(c, i)
        out.append(rect(x + 8, y + 8, cw - 16, chh - 16, fill=SOFT[col], stroke=STROKE[col], sw=2.5, r=18))
        sv, _ = label_detail(x + cw / 2, y + chh / 2 - block_height(c["label"], c.get("detail"), cw - 90, 32, 21) / 2 - 10, c["label"], c.get("detail"), cw - 90, 32, 21, colour=DEEP[col], anchor="middle")
        out.append(sv)
    ax = spec.get("axes", {})
    out.append(arrow(gx, gy + gh + 22, gx + gw, gy + gh + 22, sw=4))
    out.append(arrow(gx - 30, gy + gh, gx - 30, gy, sw=4))
    out.append(text(gx + gw / 2, gy + gh + 62, ax.get("x", ""), 22, fill=DIM, bold=True, anchor="middle")[0])
    out.append(f'<text x="{gx - 46}" y="{gy + gh / 2}" font-size="22" font-weight="700" fill="{DIM}" text-anchor="middle" transform="rotate(-90 {gx - 46} {gy + gh / 2})">{escape(ax.get("y", ""))}</text>')
    return "".join(out), gh + 80


def form_stack(spec, top):
    layers = spec["layers"]
    out, y = [], top
    lw = W - 2 * M - (300 if spec.get("side") else 0)
    for i, l in enumerate(layers):
        col = colour_of(l, i)
        inset = l.get("inset", 0) * 40
        hh = block_height(l["label"], l.get("detail"), lw - 80 - 2 * inset, 27, 19) + 30
        out.append(rect(M + inset, y, lw - 2 * inset, hh, fill=SOFT[col], stroke=STROKE[col], sw=2.5, r=14))
        sv, _ = label_detail(M + inset + 30, y + 8, l["label"], l.get("detail"), lw - 80 - 2 * inset, 27, 19, colour=DEEP[col])
        out.append(sv)
        y += hh + 14
    if spec.get("side"):
        sd = spec["side"]
        sx = W - M - 270
        out.append(arrow(sx + 20, y - 14, sx + 20, top, sw=4) if sd.get("up") else arrow(sx + 20, top, sx + 20, y - 14, sw=4))
        sv, _ = label_detail(sx + 50, top + (y - top) / 2 - 40, sd["label"], sd.get("detail"), 210, 22, 17, colour=NAVY)
        out.append(sv)
    return "".join(out), y - top


def form_numbers(spec, top):
    tiles = spec["tiles"]
    per = spec.get("per_row") or min(len(tiles), 4)
    opw = 64
    has_ops = any(t.get("op") for t in tiles)
    gap = opw if has_ops else 32
    cw = (W - 2 * M - gap * (per - 1)) / per
    out, y = [], top
    for r0 in range(0, len(tiles), per):
        row = tiles[r0:r0 + per]
        hh = max(70 + block_height(t["label"], t.get("detail"), cw - 40, 23, 18) for t in row) + 44
        for j, t in enumerate(row):
            x = M + j * (cw + gap)
            col = colour_of(t, r0 + j)
            total = t.get("result")
            out.append(rect(x, y, cw, hh, fill=NAVY if total else CARD, stroke=NAVY if total else STROKE[col], sw=3, r=16))
            vs = 58 if text_width(t["value"], 58, True) < cw - 40 else 42
            out.append(text(x + 20, y + 22 + vs, t["value"], vs, fill="#ffffff" if total else DEEP[col], bold=True)[0])
            sv, _ = label_detail(x + 20, y + 30 + vs, t["label"], t.get("detail"), cw - 40, 23, 18, colour="#ffffff" if total else INK)
            out.append(sv.replace(f'fill="{DIM}"', 'fill="#cfe0ea"') if total else sv)
            if t.get("op") and j > 0:
                out.append(text(x - gap / 2, y + hh / 2 + 18, t["op"], 52, fill=INK, bold=True, anchor="middle")[0])
        y += hh + 30
    h = y - top - 30
    if spec.get("note"):
        nt, nh = text(M, top + h + 44, wrap(spec["note"], 20, W - 2 * M), 20, fill=DIM, italic=True)
        out.append(nt)
        h += nh + 30
    return "".join(out), h


def form_checklist(spec, top):
    items = spec["items"]
    cols = spec.get("columns", 2 if len(items) > 4 else 1)
    gap = 40
    cw = (W - 2 * M - gap * (cols - 1)) / cols
    per = -(-len(items) // cols)
    out = []
    hmax = 0
    for c in range(cols):
        y = top
        for i, it in enumerate(items[c * per:(c + 1) * per]):
            k = c * per + i
            col = colour_of(it, k)
            hh = block_height(it["label"], it.get("detail"), cw - 110, 25, 19) + 26
            x = M + c * (cw + gap)
            out.append(rect(x, y, cw, hh, fill=CARD, stroke="#cfcabb", sw=1.6, r=12))
            out.append(rect(x + 22, y + 18, 34, 34, fill=SOFT[col], stroke=STROKE[col] if col != "navy" else NAVY, sw=3, r=6))
            if it.get("done"):
                out.append(f'<path d="M{x + 29},{y + 35} l8,9 l16,-19" fill="none" stroke="{INK}" stroke-width="4"/>')
            sv, _ = label_detail(x + 80, y + 6, it["label"], it.get("detail"), cw - 110, 25, 19)
            out.append(sv)
            y += hh + 14
        hmax = max(hmax, y - top)
    return "".join(out), hmax


def form_graph(spec, top):
    g = spec["grid"]
    cols, rows = g["cols"], g["rows"]
    rh = g.get("row_height", 190)
    cwid = (W - 2 * M) / cols
    nw = g.get("node_width", min(320, cwid - 40))
    out = []
    centre = lambda c, r: (M + cwid * (c + 0.5), top + 30 + rh * (r + 0.5))
    for z in spec.get("zones", []):
        c0, c1 = z["cols"]
        r0, r1 = z["rows"]
        col = z.get("colour", "grey")
        x, y = M + cwid * c0 + 6, top + 30 + rh * r0 - 22
        out.append(rect(x, y, cwid * (c1 - c0 + 1) - 12, rh * (r1 - r0 + 1) + 14, fill=SOFT[col], stroke=STROKE.get(col, "#cfcabb"), sw=2, r=20,
                        extra=' stroke-dasharray="8 6"' if z.get("dashed") else ""))
        if z.get("label"):
            ly = y + rh * (r1 - r0 + 1) + 4 if z.get("label_at") == "bottom" else y + 30
            out.append(text(x + cwid * (z.get("label_col", c0) - c0) + 18, ly, z["label"].upper(), 17, fill=DEEP[col], bold=True, extra=' letter-spacing="1.2"')[0])
    boxes = {}
    for i, n in enumerate(spec["nodes"]):
        x, y = centre(n["col"], n["row"])
        w = n.get("width", nw)
        hh = block_height(n["label"], n.get("detail"), w - 36, 23, 17) + 26
        boxes[n["id"]] = (x, y, w, hh)
    for e in spec.get("edges", []):
        ax, ay, aw, ahh = boxes[e["from"]]
        bx, by, bw, bh = boxes[e["to"]]
        # leave each box at its border, along the line between the centres
        def edge_pt(x, y, w, h, tx, ty):
            dx, dy = tx - x, ty - y
            if dx == 0 and dy == 0:
                return x, y
            sx = (w / 2 + 6) / abs(dx) if dx else 1e9
            sy = (h / 2 + 6) / abs(dy) if dy else 1e9
            s = min(sx, sy)
            return x + dx * s, y + dy * s
        p1 = edge_pt(ax, ay, aw, ahh, bx, by)
        p2 = edge_pt(bx, by, bw, bh, ax, ay)
        colr = DEEP["red"] if e.get("hot") else INK
        out.append(arrow(*p1, *p2, colour=colr, sw=4 if e.get("hot") else 2.8, dashed=e.get("dashed", False)))
        if e.get("label"):
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            lw = text_width(e["label"], 17) + 20
            out.append(rect(mx - lw / 2, my - 15, lw, 28, fill=PAPER, stroke="none", sw=0, r=8))
            out.append(text(mx, my + 5, e["label"], 17, fill=colr, anchor="middle", italic=True)[0])
    for i, n in enumerate(spec["nodes"]):
        x, y, w, hh = boxes[n["id"]]
        col = colour_of(n, i)
        solid = n.get("solid")
        out.append(rect(x - w / 2, y - hh / 2, w, hh, fill=NAVY if solid else CARD, stroke=STROKE[col] if col != "navy" else NAVY, sw=3, r=14))
        sv, _ = label_detail(x, y - hh / 2 + 6, n["label"], n.get("detail"), w - 36, 23, 17, colour="#ffffff" if solid else INK, anchor="middle")
        out.append(sv.replace(f'fill="{DIM}"', 'fill="#cfe0ea"') if solid else sv)
    return "".join(out), rh * rows + 40


def form_bookmap(spec, top):
    """The whole book on one page: a column per part, a tile per chapter, its height the chapter's length, its colour
    how the synthetic readers held (their mean interest, 1 to 5), and a mark where a reader put the book down."""
    parts = spec["parts"]
    n = len(parts)
    gap = 12
    cw = (W - 2 * M - gap * (n - 1)) / n
    scale = spec.get("px_per_word", 0.052)
    out = []
    ramp = [(1.0, "#e5625b"), (2.0, "#f2a07a"), (2.75, "#f3d48c"), (3.25, "#cfe3b8"), (3.75, "#8fca9e"), (5.1, "#4f9e6a")]

    def shade(v):
        if v is None:
            return "#e9e6dc"
        for lim, c in ramp:
            if v < lim:
                return c
        return ramp[-1][1]
    ymax = 0
    for i, p in enumerate(parts):
        x = M + i * (cw + gap)
        hl = wrap(p["title"], 17, cw - 14, True)
        out.append(rect(x, top, cw, 30 + 21 * len(hl), fill=NAVY, stroke=NAVY, r=10))
        out.append(text(x + 10, top + 25, hl, 17, fill="#ffffff", bold=True, lh=1.22)[0])
        y = top + 40 + 21 * len(hl)
        for c in p["chapters"]:
            hh = max(72, c["words"] * scale)
            fill = shade(c.get("interest"))
            out.append(rect(x, y, cw, hh, fill=fill, stroke=INK if c.get("placeholder") else "#ffffff", sw=2.5 if c.get("placeholder") else 1.5, r=8,
                            extra=' stroke-dasharray="6 5"' if c.get("placeholder") else ""))
            out.append(text(x + 9, y + 22, str(c["number"]), 18, fill=INK, bold=True)[0])
            tl = wrap(c["short"], 14.5, cw - 18)
            max_lines = max(1, int((hh - 30) // 17))
            if len(tl) > max_lines:
                tl = tl[:max_lines]
                tl[-1] = tl[-1].rstrip(",.;:") + "…"
            out.append(text(x + 9, y + 40, tl, 14.5, fill=INK, lh=1.18)[0])
            if c.get("put_down"):
                out.append(f'<circle cx="{x + cw - 15}" cy="{y + 16}" r="10" fill="{INK}"/>')
                out.append(text(x + cw - 15, y + 21, str(c["put_down"]), 13, fill="#ffffff", bold=True, anchor="middle")[0])
            y += hh + 6
        ymax = max(ymax, y)
    # the key
    ky = ymax + 30
    out.append(text(M, ky + 20, "How the five synthetic readers held, mean interest out of 5:", 18, fill=DIM, bold=True)[0])
    kx = M + 600
    for lab, v in (("under 2", 1.5), ("2 to 2.75", 2.4), ("2.75 to 3.25", 3.0), ("3.25 to 3.75", 3.5), ("3.75 and up", 4.2), ("not read", None)):
        out.append(rect(kx, ky, 34, 26, fill=shade(v), stroke="#ffffff", sw=1, r=5))
        out.append(text(kx + 42, ky + 20, lab, 17, fill=DIM)[0])
        kx += 60 + text_width(lab, 17)
    out.append(f'<circle cx="{M + 11}" cy="{ky + 54}" r="10" fill="{INK}"/>' + text(M + 11, ky + 59, "2", 13, fill="#ffffff", bold=True, anchor="middle")[0])
    out.append(text(M + 32, ky + 60, "readers who put the book down there", 17, fill=DIM)[0])
    out.append(rect(M + 400, ky + 40, 34, 26, fill="#e9e6dc", stroke=INK, sw=2.5, r=5, extra=' stroke-dasharray="6 5"'))
    out.append(text(M + 442, ky + 60, "a placeholder, waiting on Dinis", 17, fill=DIM)[0])
    out.append(text(M + 740, ky + 60, f"Tile height is the chapter's length: {spec['words']:,} words in all.", 17, fill=DIM)[0])
    return "".join(out), ky + 80 - top


FORMS = {"comparison": form_comparison, "flow": form_flow, "cycle": form_cycle, "spectrum": form_spectrum, "quadrant": form_quadrant,
         "stack": form_stack, "numbers": form_numbers, "checklist": form_checklist, "graph": form_graph, "bookmap": form_bookmap}


def render(spec):
    """The SVG for one spec. Raises KeyError on a form the code cannot draw."""
    _, top = header(spec)
    body, h = FORMS[spec["form"]](spec, top)
    if spec.get("footnote"):
        fn, fh = text(M, top + h + 34, wrap(spec["footnote"], 19, W - 2 * M), 19, fill=DIM, italic=True, lh=1.35)
        body += fn
        h += fh + 24
    return document(spec, body, h, top)


def strings(spec):
    """Every string a reader would see in the drawing, for the build's checks."""
    out = []

    def walk(v, key=""):
        if isinstance(v, str):
            if key in ("label", "detail", "heading", "sub", "title", "subtitle", "value", "question", "legend", "note", "short", "footnote") or key.startswith("end"):
                out.append(v)
        elif isinstance(v, dict):
            for k, x in v.items():
                walk(x, k)
        elif isinstance(v, list):
            for x in v:
                walk(x, key if key in ("ends",) else key)
    walk(spec)
    return out


if __name__ == "__main__":
    sys.stdout.write(render(json.loads(open(sys.argv[1], encoding="utf-8").read())))
