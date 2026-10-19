#!/usr/bin/env python3
"""The covers: three designs for Generation ZX Developers, drawn from admin/content/covers/covers.json into covers/.

    python3 admin/build/covers.py            # every design, every format, and the exports
    python3 admin/build/covers.py --svg      # the SVGs only (no browser)

Per design, in covers/<id>/:
  front.svg            the front at 6 by 9 inches, live text with its fonts embedded: the master to resize and edit
  kindle.svg           the front at Kindle's 1600 by 2560 (a taller shape: laid out again, not stretched)
  wrap.svg             the paperback's full wrap, back, spine and front, with 0.125 inch bleed, for the page count set
  wrap-guides.svg      the same with the guides drawn: trim, bleed, safe area, spine folds, the barcode area
  kindle.jpg           1600 by 2560, for KDP's eBook upload
  leanpub.jpg          1800 by 2700, for Leanpub's 6 by 9 book
  wrap.pdf             the print-ready full wrap, fonts embedded, for KDP's paperback upload
  preview.png          the front, 600 wide, for the site

Every design is a function of its width and height, so one layout makes every format. Text is measured from the font
files themselves (fontTools), so a line is fitted, not guessed. Needs fontTools and brotli; the exports need playwright
and Chromium (the one at /opt/pw-browsers in the cloud sessions). Run admin/build/cover_fonts.py once first.
The site page, covers/index.html, is written by build.py from covers.json and these files; the build also checks that
every word on the covers is in its source, word for word.
"""
import base64
import glob
import json
import math
import os
import re
import sys
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "admin/content/covers"
OUT = ROOT / "covers"
DOC = json.loads((SRC / "covers.json").read_text(encoding="utf-8"))
BOOK, SYS, FMT = DOC["book"], DOC["system"], DOC["formats"]
P = SYS["palette"]
MARK = [P["green"], P["yellow"], P["teal"], P["red"]]
IN = 72.0  # the drawing is in points
SAFE = SYS["safe_in"] * IN


# ------------------------------------------------------------------ fonts: embedded, and measured from the files
FONTS = json.loads((SRC / "fonts/fonts.json").read_text(encoding="utf-8"))["fonts"]


def font_file(family, style="normal", weight=400):
    for f in FONTS:
        ws = [int(w) for w in f["weight"].split()]
        if f["family"] == family and f["style"] == style and min(ws) <= weight <= max(ws):
            return f
    raise KeyError(f"no font {family} {style} {weight}")


@lru_cache(maxsize=None)
def instance(family, style, weight):
    """The font at one weight, as a static font: what the SVG embeds and the PDF carries."""
    from fontTools.ttLib import TTFont
    f = TTFont(SRC / "fonts" / font_file(family, style, weight)["file"])
    if "fvar" in f:
        from fontTools.varLib import instancer
        axes = {a.axisTag: a for a in f["fvar"].axes}
        loc = {"wght": max(axes["wght"].minValue, min(axes["wght"].maxValue, weight))} if "wght" in axes else {}
        if "opsz" in axes:
            loc["opsz"] = axes["opsz"].maxValue
        if loc:
            f = instancer.instantiateVariableFont(f, loc, updateFontNames=False)
    return f


@lru_cache(maxsize=None)
def instance_woff2(family, style, weight):
    import io
    f = instance(family, style, weight)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    return buf.getvalue()


@lru_cache(maxsize=None)
def metrics(family, style, weight):
    f = instance(family, style, weight)
    cmap, hm, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    return {ch: hm[g][0] / upm for ch, g in ((chr(c), g) for c, g in cmap.items())}, upm


def width(text, family, size, weight=400, style="normal", spacing=0.0):
    m, _ = metrics(family, style, weight)
    return sum(m.get(ch, 0.55) for ch in text) * size + spacing * max(len(text) - 1, 0)


def fit(text, family, w, weight=400, style="normal", spacing_em=0.0):
    """The size at which text is exactly w wide."""
    at100 = width(text, family, 100, weight, style, spacing_em * 100)
    return 100 * w / at100


def wrap(text, family, size, w, weight=400, style="normal"):
    out, cur = [], ""
    for word in text.split():
        t = f"{cur} {word}" if cur else word
        if cur and width(t, family, size, weight, style) > w:
            out.append(cur); cur = word
        else:
            cur = t
    return out + ([cur] if cur else [])


def font_css(faces):
    rules = []
    for family, style, weight in sorted(faces):
        data = base64.b64encode(instance_woff2(family, style, weight)).decode()
        rules.append(f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
                     f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return "".join(rules)


def wrap_even(text, family, size, w, weight=400, style="normal"):
    """As few lines as wrap() gives, but as even as they can be: no word left alone on the last line."""
    n = len(wrap(text, family, size, w, weight, style))
    lo, hi = w * 0.4, w
    for _ in range(18):
        mid = (lo + hi) / 2
        if len(wrap(text, family, size, mid, weight, style)) > n:
            lo = mid
        else:
            hi = mid
    return wrap(text, family, size, hi, weight, style)


# ------------------------------------------------------------------ the drawing
class SVG:
    def __init__(self):
        self.out, self.faces, self.runs, self.n = [], set(), [], 0

    def uid(self):
        self.n += 1
        return self.n

    def add(self, s):
        self.out.append(s)

    def rect(self, x, y, w, h, fill, extra=""):
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"{extra}/>')

    def text(self, x, y, s, family, size, fill, weight=400, style="normal", anchor="start", spacing=0.0, opacity=1, extra=""):
        self.faces.add((family, style, weight))
        self.runs.append((s, family, style, weight, size))
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        ls = f' letter-spacing="{spacing:.2f}"' if spacing else ""
        op = f' fill-opacity="{opacity}"' if opacity != 1 else ""
        st = ' font-style="italic"' if style == "italic" else ""
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="\'{family}\'" font-size="{size:.2f}" font-weight="{weight}"{st} fill="{fill}"{op}{a}{ls}{extra}>{escape(s)}</text>')

    def lines(self, x, y, lines, family, size, fill, lh=1.3, **kw):
        for i, l in enumerate(lines):
            self.text(x, y + i * size * lh, l, family, size, fill, **kw)
        return len(lines) * size * lh

    def mark(self, x, y, s, gap=None, vertical=False):
        gap = s * 0.25 if gap is None else gap
        for i, c in enumerate(MARK):
            dx, dy = (0, i * (s + gap)) if vertical else (i * (s + gap), 0)
            self.rect(x + dx, y + dy, s, s, c, f' rx="{s * 0.12:.2f}"')

    def doc(self, W, H, width_attr, height_attr, title, desc, bg):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W:.2f} {H:.2f}" width="{width_attr}" height="{height_attr}" role="img" aria-label="{escape(title)}">\n'
                f'<title>{escape(title)}</title>\n<desc>{escape(desc)}</desc>\n'
                f'<style>{font_css(self.faces)}</style>\n<rect width="{W:.2f}" height="{H:.2f}" fill="{bg}"/>\n' + "\n".join(self.out) + "\n</svg>\n")


# ------------------------------------------------------------------ design 1: One letter more (the 2018 cover, one letter added)
def front_one(c, X, Y, W, H):
    navy, ivory, sky = P["navy"], P["ivory"], P["sky"]
    CD, ST, AB = "Big Shoulders Display", "Big Shoulders Stencil Display", "Archivo Black"
    m, iw = SAFE, W - 2 * SAFE
    x = X + m
    y = Y + m
    # the full title first, large enough to be read where Amazon checks it against the metadata
    c.text(x, y + 18, BOOK["title"].upper(), CD, 22, ivory, weight=800, spacing=1.5)
    y += 32
    # the blocks: G E N, the 2018 space (narrower now), Z, and the new X; tilted, but inside the safe area
    gap, inset = 5, 4
    bw = (iw - 2 * inset - 5 * gap) / 5.5
    bh = bw * 1.12
    blocks = [("G", P["green"], 1), ("E", P["yellow"], 1), ("N", P["teal"], 1), ("", P["blue"], 0.5), ("Z", P["red"], 1), ("X", ivory, 1)]
    tilt = [-1.2, 0.8, -0.5, 0.9, -0.8, 1.0]
    bx = x + inset
    for i, (ch, col, share) in enumerate(blocks):
        w = bw * share
        cx, cy = bx + w / 2, y + bh / 2
        c.add(f'<g transform="rotate({tilt[i]} {cx:.2f} {cy:.2f})">')
        c.rect(bx, y, w, bh, col, ' rx="2.5"')
        if ch:
            c.text(cx, y + bh * 0.80, ch, AB, bh * 0.86, navy, anchor="middle")
        c.add("</g>")
        bx += w + gap
    y += bh + 14
    # DEVELOPERS fitted by its size and spacing, never by stretching the glyphs
    dev_size = fit("DEVELOPERS", ST, iw, 900, spacing_em=0.06)
    c.text(x, y + dev_size * 0.74, "DEVELOPERS", ST, dev_size, sky, weight=900, spacing=dev_size * 0.06)
    y += dev_size * 0.74 + 16
    c.text(x, y + 14, BOOK["edition"].upper(), CD, 16, P["yellow"], weight=800, spacing=1.8)
    y += 24
    y += c.lines(x, y + 18, wrap_even(BOOK["cover_line"], CD, 20, iw, 700), CD, 20, ivory, lh=1.12, weight=700)
    # the author, the badge and the footer are anchored to the bottom; the eight lines of 2018 fill what is left, quieter
    bottom = Y + H - m
    c.text(x, bottom - 2, f"{BOOK['licence']} · {BOOK['site']}", CD, 10, ivory, weight=500, spacing=0.4, opacity=0.6)
    a_size = 46
    c.text(x, bottom - 18, BOOK["author"].upper(), CD, a_size, sky, weight=800, spacing=0.5)
    author_top = bottom - 18 - a_size * 0.74
    r = 31
    bx, by = X + W - m - r, bottom - 8 - r
    c.add(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="{r}" fill="none" stroke="{ivory}" stroke-width="1.2" stroke-opacity="0.75"/>')
    pid = f"badge-{c.uid()}"
    rr = r - 7
    c.add(f'<path id="{pid}" d="M{bx - rr:.2f},{by:.2f} a{rr},{rr} 0 1,1 {2 * rr},0 a{rr},{rr} 0 1,1 -{2 * rr},0" fill="none"/>')
    c.faces.add((CD, "normal", 800))
    # the ring text is set to the circle's length, so it closes the circle
    c.add(f'<text font-family="\'{CD}\'" font-size="9.5" font-weight="800" fill="{ivory}"><textPath xlink:href="#{pid}" href="#{pid}" textLength="{2 * math.pi * rr - 3:.2f}" lengthAdjust="spacing">VERSION 2 · {BOOK["year"]} · GEN ZX ·</textPath></text>')
    c.mark(bx - 13, by - 3, 5.5, 1.5)
    lines = [l.upper() for l in BOOK["cover_lines_2018"]]
    room_top, room_bot = y + 12, author_top - 14
    longest = max(lines, key=lambda l: width(l, CD, 100, 700))
    size = min(20, fit(longest, CD, iw * 0.98, 700), (room_bot - room_top) / (len(lines) * 1.12))
    lh = size * 1.12
    y0 = room_top + ((room_bot - room_top) - lh * len(lines)) / 2 + size * 0.8
    for i, l in enumerate(lines):
        c.text(x, y0 + i * lh, l, CD, size, ivory, weight=700, opacity=0.55)


def back_spine_one(c, X, Y, W, H, sx, S):
    back_text(c, X, Y, W, H, P["ivory"], P["sky"], "IBM Plex Sans", "Big Shoulders Display", body_w=400, head_w=800, body_size=11.5, lh=1.4, strong=600, head_size=16)
    spine(c, sx, Y, S, H, "Big Shoulders Display", 800, P["ivory"], P["sky"], upper=True)


# ------------------------------------------------------------------ design 2: ZX
ZX_SLOPE = 0.5          # the band rises one point for every two across
ZX_ORDER = ("green", "yellow", "teal", "red")  # the mark's order, not the Spectrum's


def stripes(c, x0, x1, y_at_x1, slope, t, gap):
    """Four bars in the mark's colours from x0 to x1, rising to the right; y_at_x1 is the first bar's top at x1."""
    for i, col in enumerate(ZX_ORDER):
        o = i * (t + gap)
        a, b = y_at_x1 + o + slope * (x1 - x0), y_at_x1 + o
        c.add(f'<polygon points="{x0:.2f},{a:.2f} {x1:.2f},{b:.2f} {x1:.2f},{b + t:.2f} {x0:.2f},{a + t:.2f}" fill="{P[col]}"/>')


def front_zx(c, X, Y, W, H, band_from=None):
    ivory = P["ivory"]
    G, MO = "Space Grotesk", "Space Mono"
    m, iw = SAFE, W - 2 * SAFE
    x, y = X + m, Y + m
    gs = fit("GENERATION", MO, iw * 0.7, 700, spacing_em=0.18)
    c.text(x, y + gs * 0.72, "GENERATION", MO, gs, ivory, weight=700, spacing=gs * 0.18)
    y += gs * 0.72 + 8
    zx = fit("ZX", G, iw * 0.92, 700, spacing_em=-0.04)
    c.text(x - zx * 0.03, y + zx * 0.72, "ZX", G, zx, ivory, weight=700, spacing=-zx * 0.04)
    y += zx * 0.72 + 12
    dv = fit("DEVELOPERS", G, iw, 700, spacing_em=0.01)
    c.text(x, y + dv * 0.72, "DEVELOPERS", G, dv, ivory, weight=700, spacing=dv * 0.01)
    y += dv * 0.72 + 24
    prompt = "> " + BOOK["edition"]
    c.text(x, y + 13, prompt, MO, 15, P["yellow"], weight=700)
    c.rect(x + width(prompt + " ", MO, 15, 700), y + 2, 8.5, 12, ivory)  # the cursor, on the baseline
    y += 30
    cl_w = iw * 0.9
    for l in wrap_even(BOOK["cover_line"], G, 16, cl_w, 500):
        c.text(x, y + 13, l, G, 16, ivory, weight=500, opacity=0.95)
        y += 16 * 1.3
    text_bottom = y
    # the author, bottom right, under the band
    a_size = 30
    c.text(X + W - m, Y + H - m - 2, BOOK["author"], G, a_size, ivory, weight=700, anchor="end")
    a_left = X + W - m - width(BOOK["author"], G, a_size, 700)
    a_top = Y + H - m - 2 - a_size * 0.72
    c.mark(X + W - m - 4 * 7.5 - 3 * 2, a_top - 16, 7.5, 2)
    # the band: placed so its last bar clears the author's mark and its first bar clears the words
    t = H * 0.028
    gap = t * 0.25
    band_h = 4 * t + 3 * gap
    xr = X + W + 20
    y_right = (a_top - 16 - 10) - band_h - ZX_SLOPE * (xr - a_left)
    clear = y_right + ZX_SLOPE * (xr - (x + cl_w))  # the band's top where the cover line ends
    if clear < text_bottom + 6:
        raise SystemExit(f"covers: zx at {W:.0f}x{H:.0f}: the band would cross the cover line ({clear:.1f} < {text_bottom + 6:.1f})")
    stripes(c, X - 20 if band_from is None else band_from, xr, y_right, ZX_SLOPE, t, gap)


def back_spine_zx(c, X, Y, W, H, sx, S):
    back_text(c, X, Y, W, H, P["ivory"], P["yellow"], "Space Grotesk", "Space Mono", body_w=400, head_w=700, body_size=12.5, lh=1.42, head_size=12)
    spine(c, sx, Y, S, H, "Space Grotesk", 700, P["ivory"], P["yellow"], upper=False, mark=False)


# ------------------------------------------------------------------ design 3: the book as a graph
def book_graph():
    """The candidate as nodes and edges: chapters (by part, sized by words), the ideas each names, the reading order,
    and the reader's route from chapter 1 to the company, chapter 22; laid out freely, then turned so the route runs
    from the top left to the bottom right. Seeded, so every run draws the same graph."""
    import numpy as np
    doc = json.loads((ROOT / "v2/book/book.json").read_text(encoding="utf-8"))
    parts = [p["slug"] for p in doc["parts"]]
    chs = doc["chapters"]
    nodes, edges = [], []
    idx = {}
    for c in chs:
        idx["ch:" + c["slug"]] = len(nodes)
        nodes.append({"kind": "chapter", "n": c["number"], "part": parts.index(c["part"]), "words": c["words"]})
    for c in chs:
        for i in c.get("ideas", []):
            k = "idea:" + i["id"]
            if k not in idx:
                idx[k] = len(nodes)
                nodes.append({"kind": "idea"})
            edges.append((idx["ch:" + c["slug"]], idx[k], "idea"))
    for a, b in zip(chs, chs[1:]):
        edges.append((idx["ch:" + a["slug"]], idx["ch:" + b["slug"]], "order"))
    byn = {c["number"]: idx["ch:" + c["slug"]] for c in chs}
    path = [byn[n] for n in range(1, 23) if n in byn]
    n = len(nodes)
    rng = np.random.default_rng(2026)
    pos = rng.random((n, 2))
    k = 0.9 / math.sqrt(n)
    A = [(a, b, 1.6 if kind == "order" else 1.0) for a, b, kind in edges]
    t = 0.12
    for _ in range(400):
        d = pos[:, None, :] - pos[None, :, :]
        dist = np.maximum(np.linalg.norm(d, axis=2), 1e-3)
        disp = ((k * k / dist ** 2)[:, :, None] * d).sum(axis=1)
        for a, b, w in A:
            v = pos[a] - pos[b]
            dd = max(np.linalg.norm(v), 1e-3)
            f = w * dd / k * v
            disp[a] -= f; disp[b] += f
        disp += (0.5 - pos) * 0.6
        ln = np.maximum(np.linalg.norm(disp, axis=1), 1e-9)
        pos += disp / ln[:, None] * np.minimum(ln, t)[:, None]
        t *= 0.99
    # turn the whole drawing, without bending it, so the route runs from the top left to the bottom right
    v = pos[path[-1]] - pos[path[0]]
    a = math.atan2(1, 1) - math.atan2(v[1], v[0])
    rot = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    pos = (pos - pos.mean(axis=0)) @ rot.T
    pos -= pos.min(axis=0); pos /= pos.max(axis=0)
    return nodes, edges, path, pos.tolist(), sum(1 for x in nodes if x["kind"] == "idea"), len(chs)


GRAPH = None


def graph_data():
    global GRAPH
    if GRAPH is None:
        GRAPH = book_graph()
    return GRAPH


def front_graph(c, X, Y, W, H):
    nodes, edges, path, pos, n_ideas, n_ch = graph_data()
    ink, paper = P["ink"], P["paper"]
    F, PX = "Fraunces", "IBM Plex Sans"
    m, iw = SAFE, W - 2 * SAFE
    # the title, above the graph: "ZX" in red, the hook, at the title's size
    x, y = X + m, Y + m
    c.mark(x, y, 7.5, 2)
    y += 22
    t1 = fit("Generation ZX", F, iw, 900)
    c.text(x, y + t1 * 0.78, "Generation", F, t1, ink, weight=900)
    c.text(x + width("Generation ", F, t1, 900), y + t1 * 0.78, "ZX", F, t1, P["red"], weight=900)
    y += t1 * 0.92
    c.text(x, y + t1 * 0.72, "Developers", F, t1, ink, weight=900)
    y += t1 * 0.72 + 20
    c.text(x, y + 16, BOOK["edition"], F, 20, ink, weight=500, style="italic")
    y += 30
    for l in wrap_even(BOOK["cover_line"], PX, 14, iw * 0.95, 400):
        c.text(x, y + 11, l, PX, 14, ink, weight=400, opacity=0.9)
        y += 14 * 1.35
    bottom = Y + H - m
    c.text(x, bottom - 2, BOOK["author"], PX, 19, ink, weight=600)
    # the graph, between the words and the author, inside the safe area
    r_max = 2.6 + math.sqrt(max(nd["words"] for nd in nodes if nd["kind"] == "chapter")) / 11
    gx, gy = X + m + r_max, y + 18 + r_max
    gw, gh = iw - 2 * r_max, (bottom - 34) - gy - r_max
    pt = lambda i: (gx + pos[i][0] * gw, gy + pos[i][1] * gh)
    cols = [P["teal"], P["green"], P["yellow"], P["red"], P["blue"]]
    for a, b, kind in edges:
        (x1, y1), (x2, y2) = pt(a), pt(b)
        c.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{ink}" stroke-opacity="{0.22 if kind == "order" else 0.12}" stroke-width="{0.7 if kind == "order" else 0.45}"/>')
    pts = [pt(p) for p in path]
    d = f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"
    for i in range(len(pts) - 1):  # Catmull-Rom through the chapters, as cubic Beziers
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}"
    c.add(f'<path d="{d}" fill="none" stroke="{P["navy"]}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, nd in enumerate(nodes):
        if nd["kind"] == "idea":
            x1, y1 = pt(i)
            c.add(f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="1.25" fill="{ink}" fill-opacity="0.55"/>')
    for i, nd in enumerate(nodes):
        if nd["kind"] == "chapter":
            x1, y1 = pt(i)
            r = 2.6 + math.sqrt(nd["words"]) / 11
            c.add(f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="{r:.2f}" fill="{cols[nd["part"] % len(cols)]}" stroke="{paper}" stroke-width="1.1"/>')
    (sx, sy), (ex, ey) = pts[0], pts[-1]
    c.add(f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="6.5" fill="{paper}" stroke="{P["navy"]}" stroke-width="2.2"/>')
    c.add(f'<rect x="{ex - 7:.2f}" y="{ey - 7:.2f}" width="14" height="14" fill="{P["navy"]}"/>')


def back_spine_graph(c, X, Y, W, H, sx, S):
    nodes, edges, path, pos, n_ideas, n_ch = graph_data()
    note = (f"The front is the book's own graph: its {n_ch} chapters, coloured by part, and the {n_ideas} ideas they were written from. "
            f"The line is the reader's route, from chapter 1 to chapter 22, the company.")
    back_text(c, X, Y, W, H, P["ink"], P["red"], "IBM Plex Sans", "Fraunces", body_w=400, head_w=900, body_size=11.5, lh=1.45, head_size=15, head_style="italic", head_weight=500, strong=600, note=note)
    spine(c, sx, Y, S, H, "Fraunces", 900, P["ink"], P["red"], upper=False)


# ------------------------------------------------------------------ the shared back and spine
def barcode_box(X, Y, W, H):
    pb = FMT["paperback"]
    bw, bh = pb["barcode_in"][0] * IN, pb["barcode_in"][1] * IN
    return X + W - 0.25 * IN - bw, Y + H - 0.25 * IN - bh, bw, bh


def back_text(c, X, Y, W, H, fg, accent_fg, body, head, body_w=400, head_w=700, body_size=12, lh=1.35, head_size=13, head_style="normal", head_weight=None, strong=700, note=None):
    """The back: the title, Dinis's description, the objective, the close; centred between the top of the safe area and
    the footer, and refused if it would reach the barcode area."""
    m, iw = SAFE, W - 2 * SAFE
    x = X + m
    bottom = Y + H - m
    footer_top = bottom - 40 - (24 if note else 0)
    _, bar_top, _, _ = barcode_box(X, Y, W, H)
    limit = min(footer_top, bar_top) - 14

    def block(cc, y):
        cc.text(x, y + head_size, BOOK["title"], head, head_size, accent_fg, weight=head_weight or head_w, style=head_style)
        y += head_size + 6
        cc.text(x, y + head_size * 0.9, BOOK["edition"], head, head_size * 0.8, fg, weight=head_weight or head_w, style=head_style, opacity=0.75)
        y += head_size + 18
        for i, para in enumerate(BOOK["back"]):
            last = i == len(BOOK["back"]) - 1
            w8, size = (strong if last else body_w), (body_size * (1.12 if last else 1))
            y += cc.lines(x, y + size, wrap(para, body, size, iw, w8), body, size, accent_fg if last else fg, lh=lh, weight=w8) + size * 0.7
        italic = "italic" if any(f["family"] == body and f["style"] == "italic" for f in FONTS) else "normal"
        y += cc.lines(x, y + body_size, wrap(BOOK["back_close"], body, body_size, iw * 0.9, body_w, italic), body, body_size, fg, lh=lh, weight=body_w, style=italic, opacity=0.9)
        cc.text(x, y + body_size + 6, BOOK["author"], body, body_size, fg, weight=strong)
        return y + body_size + 10

    h = block(SVG(), 0)
    top = Y + m + max(0, (limit - (Y + m) - h) / 2)
    end = block(c, top)
    if end > limit:
        raise SystemExit(f"covers: the back text runs to {end:.1f}pt, into the footer or the barcode area (limit {limit:.1f}pt)")
    if note:
        nl = wrap(note, body, 8.5, barcode_box(X, Y, W, H)[0] - x - 12, body_w)
        c.lines(x, bottom - 56 - 8.5 * 1.35 * (len(nl) - 1), nl, body, 8.5, fg, lh=1.35, weight=body_w, opacity=0.75)
    c.mark(x, bottom - 40, 9, 2.5)
    bar_x = barcode_box(X, Y, W, H)[0]
    fs = min([10] + [fit(line, body, bar_x - x - 12, body_w) for line in BOOK["back_footer"]])  # clear of the barcode area
    for i, line in enumerate(BOOK["back_footer"]):
        c.text(x, bottom - 14 + i * 14, line, body, fs, fg, weight=body_w, opacity=0.8)


def spine(c, sx, Y, S, H, family, weight, fg, accent, upper=True, mark=True):
    if FMT["paperback"]["pages"] < FMT["paperback"]["spine_text_min_pages"]:
        return
    size = min(S * 0.42, 15)
    cx = sx + S / 2
    t = BOOK["title"].upper() if upper else BOOK["title"]
    a = BOOK["author"].upper() if upper else BOOK["author"]
    ms = min(S * 0.32, 8)
    mark_top = Y + H - SAFE - 4 * ms - 3 * ms * 0.25
    tw = width(t, family, size, weight)
    total = tw + size * 0.9 + width(a, family, size * 0.85, weight)
    lo, hi = Y + SAFE, (mark_top - 10) if mark else (Y + H - SAFE)
    start = lo + (hi - lo - total) / 2  # centred on the spine's length, above the mark
    c.add(f'<g transform="translate({cx + size * 0.36:.2f},{start:.2f}) rotate(90)">')
    c.text(0, 0, t, family, size, fg, weight=weight)
    c.text(tw + size * 0.9, 0, a, family, size * 0.85, accent, weight=weight)
    c.add("</g>")
    if mark:
        c.mark(cx - ms / 2, mark_top, ms, vertical=True)


DESIGNS = {
    "one-letter-more": {"bg": P["navy"], "front": front_one, "back": back_spine_one},
    "zx": {"bg": P["ink"], "front": front_zx, "back": back_spine_zx},
    "the-book-as-a-graph": {"bg": P["paper"], "front": front_graph, "back": back_spine_graph},
}


# ------------------------------------------------------------------ the formats
def spine_in():
    pb = FMT["paperback"]
    return pb["pages"] * pb["spine_in_per_page"][pb["paper"]]


@lru_cache(maxsize=None)
def cap_height(family, style, weight):
    f = instance(family, style, weight)
    return f["OS/2"].sCapHeight / f["head"].unitsPerEm


def title_gate(c, did, W, H):
    """Every word of the metadata title on the front, with a cap height of at least 2.5% of the cover's height: about
    4 pixels when Amazon shows the cover 160 pixels tall. KDP checks the cover's title against the book's."""
    need = 0.025 * H
    for word in BOOK["title"].split():
        best = max((size * cap_height(fam, st, w) for s, fam, st, w, size in c.runs if re.search(rf"\b{re.escape(word)}\b", s, re.I)), default=0)
        if best < need:
            raise SystemExit(f"covers: {did} at {W:.0f}x{H:.0f}: '{word}' has a cap height of {best:.1f}pt; the title needs {need:.1f}pt to read at a thumbnail")


def make_front(did, W, H, w_attr, h_attr):
    d = DESIGNS[did]
    c = SVG()
    d["front"](c, 0, 0, W, H)
    title_gate(c, did, W, H)
    name = next(x["name"] for x in DOC["designs"] if x["id"] == did)
    return c.doc(W, H, w_attr, h_attr, f"{BOOK['title']} ({BOOK['edition']}), cover: {name}", f"Front cover, design {name}. {BOOK['cover_line']}. {BOOK['author']}.", d["bg"])


def make_wrap(did, guides=False):
    pb = FMT["paperback"]
    tw, th, b = pb["trim_in"][0] * IN, pb["trim_in"][1] * IN, pb["bleed_in"] * IN
    S = spine_in() * IN
    W, H = 2 * b + 2 * tw + S, 2 * b + th
    d = DESIGNS[did]
    c = SVG()
    d["back"](c, b, b, tw, th, b + tw, S)
    # on zx the band runs on over the spine, from its left fold; the back stays clear for the text and the barcode
    d["front"](c, b + tw + S, b, tw, th, **({"band_from": b + tw} if did == "zx" else {}))
    if guides:
        g = '<g fill="none" stroke-width="0.6">'
        g += f'<rect x="{b}" y="{b}" width="{W - 2 * b:.2f}" height="{th:.2f}" stroke="#ff00aa" stroke-dasharray="4 3"/>'  # trim
        for xx in (b + tw, b + tw + S):
            g += f'<line x1="{xx:.2f}" y1="0" x2="{xx:.2f}" y2="{H:.2f}" stroke="#ff00aa"/>'  # the folds
        for px in (b, b + tw + S):
            g += f'<rect x="{px + SAFE:.2f}" y="{b + SAFE:.2f}" width="{tw - 2 * SAFE:.2f}" height="{th - 2 * SAFE:.2f}" stroke="#00b7ff" stroke-dasharray="3 3"/>'  # safe
        bx, by, bw, bh = barcode_box(b, b, tw, th)
        g += f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bw:.2f}" height="{bh:.2f}" fill="#ffffff" fill-opacity="0.85" stroke="#ff00aa"/>'
        g += "</g>"
        c.add(g)
        c.faces.add(("IBM Plex Sans", "normal", 400))
        c.text(bx + bw / 2, by + bh / 2 + 3, "barcode area: keep clear", "IBM Plex Sans", 7, "#ff00aa", anchor="middle")
        c.text(b + tw + S / 2, b + th + b * 0.7, f"spine {S / IN:.3f} in ({pb['pages']} pages, {pb['paper']})", "IBM Plex Sans", 5.5, "#ff00aa", anchor="middle")
    name = next(x["name"] for x in DOC["designs"] if x["id"] == did)
    return c.doc(W, H, f"{W / IN:.4f}in", f"{H / IN:.4f}in", f"{BOOK['title']}, paperback full wrap: {name}",
                 f"Back, spine and front, {pb['trim_in'][0]} by {pb['trim_in'][1]} inches trim, {pb['bleed_in']} inch bleed, spine {S / IN:.3f} inches for {pb['pages']} pages.", d["bg"]), W / IN, H / IN


def write_svgs():
    out = {}
    for did in DESIGNS:
        d = OUT / did
        d.mkdir(parents=True, exist_ok=True)
        (d / "front.svg").write_text(make_front(did, 6 * IN, 9 * IN, "6in", "9in"), encoding="utf-8")
        kw, kh = FMT["kindle"]["px"]
        (d / "kindle.svg").write_text(make_front(did, 6 * IN, 6 * IN * kh / kw, str(kw), str(kh)), encoding="utf-8")
        wrap_svg, win, hin = make_wrap(did)
        (d / "wrap.svg").write_text(wrap_svg, encoding="utf-8")
        (d / "wrap-guides.svg").write_text(make_wrap(did, guides=True)[0], encoding="utf-8")
        out[did] = (win, hin)
    return out


def exact_page(path, win, hin):
    """Chromium rounds a page to whole CSS pixels (12.745 in becomes 12.75); KDP checks the size, so set the page box to
    the exact inches. The drawing starts at the page's top left, so what is cut is a sliver of bleed on the right."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject
    r = PdfReader(str(path))
    w = PdfWriter()
    pg = r.pages[0]
    top = float(pg.mediabox.top)
    box = RectangleObject([0, top - hin * 72, win * 72, top])
    pg.mediabox = box; pg.cropbox = box; pg.trimbox = box; pg.bleedbox = box
    w.add_page(pg)
    with open(path, "wb") as f:
        w.write(f)


def export(sizes):
    from playwright.sync_api import sync_playwright
    exe = os.environ.get("STORYBOARD_CHROMIUM") or next(iter(sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))), None)

    def shot(pg, svg, w, h, path, kind):
        body = re.sub(r'width="[^"]+" height="[^"]+" role', f'width="{w}" height="{h}" role', svg.read_text(encoding="utf-8"), count=1)
        pg.set_viewport_size({"width": w, "height": h})
        pg.set_content(f'<html><body style="margin:0">{body}</body></html>')
        pg.wait_for_timeout(400)
        pg.screenshot(path=str(path), type=kind, **({"quality": 92} if kind == "jpeg" else {}), clip={"x": 0, "y": 0, "width": w, "height": h})

    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = br.new_page()
        for did, (win, hin) in sizes.items():
            d = OUT / did
            shot(pg, d / "kindle.svg", *FMT["kindle"]["px"], d / "kindle.jpg", "jpeg")
            shot(pg, d / "front.svg", *FMT["leanpub"]["px"], d / "leanpub.jpg", "jpeg")
            if DESIGNS[did]["bg"] == P["paper"]:  # a light cover on Amazon's white page needs a hairline to end it
                from PIL import Image, ImageDraw
                for fn in ("kindle.jpg", "leanpub.jpg"):
                    im = Image.open(d / fn)
                    ImageDraw.Draw(im).rectangle([0, 0, im.width - 1, im.height - 1], outline="#d8d2c4", width=2)
                    im.save(d / fn, quality=92)
            shot(pg, d / "front.svg", 600, 900, d / "preview.png", "png")
            shot(pg, d / "wrap-guides.svg", 1500, round(1500 * hin / win), d / "wrap-guides.png", "png")
            # the print PDF: the SVG at its size in inches, on a page of exactly that size, fonts embedded by Chromium
            pg.set_content('<html><head><style>@page{margin:0}html,body{margin:0}svg{display:block}</style></head><body>'
                           + (d / "wrap.svg").read_text(encoding="utf-8") + "</body></html>")
            pg.wait_for_timeout(500)
            pg.pdf(path=str(d / "wrap.pdf"), width=f"{win:.4f}in", height=f"{hin:.4f}in", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}, page_ranges="1")
            exact_page(d / "wrap.pdf", win, hin)
        br.close()


if __name__ == "__main__":
    sizes = write_svgs()
    if "--svg" not in sys.argv:
        export(sizes)
    pb = FMT["paperback"]
    print(f"covers: {len(sizes)} designs in {OUT}; spine {spine_in():.3f} in for {pb['pages']} pages on {pb['paper']} paper; wrap {next(iter(sizes.values()))[0]:.3f} by {next(iter(sizes.values()))[1]:.3f} in")
