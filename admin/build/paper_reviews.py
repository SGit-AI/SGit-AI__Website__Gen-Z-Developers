"""Paper reviews: Dinis's pen on a printed release candidate, drawn so that anyone can read it.

A paper review is data (admin/content/reviews/paper/<id>.json): the photographs of the marked pages, each handwritten
note with where it sits on the photograph, what it says word for word, what it means and the theme it belongs to, and
the candidate's contents with the page each chapter starts on. Called by build.py; it writes, per review, into
reviews/paper/<id>/:

  page-N-callouts.svg   the photograph with each note boxed and numbered, and the notes typed beside it
  page-N-redrawn.svg    the page redrawn clean, with the marks in the same places, in a hand anyone can read
  after-title-page.svg  a sketch of the title page after the change
  after-contents-map.svg, after-contents-line.svg   two ways to show the contents as a picture, as note 6 asks

Every SVG embeds its photograph and its fonts (Caveat for the pen, IBM Plex Sans for type, both under the SIL Open Font
Licence), so it can be opened, printed or sent on its own. The drawing is deterministic: the wobble of the pen is a
seeded random, so a rebuild changes nothing unless the data changes.
"""
import base64
import json
import random
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "admin/content/reviews/paper"
FONTS = {"Caveat": ROOT / "admin/content/reviews/fonts/caveat/caveat-400-700.woff2",
         "Plex": ROOT / "admin/content/covers/fonts/ibm-plex-sans/ibm-plex-sans-normal-400.woff2"}
INK, DIM, PAPER, PEN = "#1f2937", "#9ca3af", "#ffffff", "#1d3a8a"
THEME = {"first-page": "#dc2626", "show": "#2563eb", "doing": "#16a34a", "altitude": "#9333ea", "process-out": "#d97706",
         "voice": "#0891b2", "reader-context": "#db2777", "release": "#4f46e5",
         "evidence": "#0f766e", "links": "#c026d3", "works": "#15803d", "answers": "#475569", "visual": "#ea580c"}
HAND, TYPE = "Caveat, cursive", "Plex, 'IBM Plex Sans', Arial, sans-serif"
# which part each hands-on chapter would sit beside, if the hands-on part is spread across the book (note 11): a proposal
SPREAD = {30: "working-with-agents", 31: "before-you-start", 32: "the-frame", 33: "the-frame", 34: "getting-the-job",
          35: "judgement", 36: "getting-the-job", 37: "start-the-company", 38: "build-it-without-a-server",
          39: "start-the-company", 40: "build-it-without-a-server"}
MILESTONE = {"before-you-start": "name your problem, and where you stand", "the-frame": "brief your first agent",
             "getting-the-job": "show your work in public", "working-with-agents": "run your first workspace",
             "judgement": "name the stop; check a claim", "start-the-company": "ship, test, price, register",
             "build-it-without-a-server": "a product with no server of yours", "the-long-game": "keep a memory; give back",
             "how-this-book-was-made": "tell us what you made"}


def esc(s):
    return escape(str(s), quote=True)


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def fontface():
    return "".join(f"@font-face{{font-family:{k};src:url(data:font/woff2;base64,{b64(p)}) format('woff2');}}" for k, p in FONTS.items())


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<style>{fontface()}</style><rect width="{w}" height="{h}" fill="#f8fafc"/>{body}</svg>\n')


def wrap(s, n):
    out, line = [], ""
    for word in str(s).split():
        if line and len(line) + 1 + len(word) > n:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    return out + ([line] if line else [])


def text(x, y, lines, size, font=TYPE, fill=INK, weight="normal", anchor="start", lh=1.25, extra=""):
    if isinstance(lines, str):
        lines = [lines]
    spans = "".join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * lh:.1f}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{spans}</text>')


class Pen:
    """Seeded wobble, so the marks look drawn and stay the same on every build."""

    def __init__(self, seed):
        self.r = random.Random(seed)

    def j(self, a=3.0):
        return self.r.uniform(-a, a)

    def line(self, x1, y1, x2, y2, colour=PEN, w=3.2, a=2.5, extra=""):
        mx, my = (x1 + x2) / 2 + self.j(a), (y1 + y2) / 2 + self.j(a)
        return (f'<path d="M{x1 + self.j(1):.1f},{y1 + self.j(1):.1f} Q{mx:.1f},{my:.1f} {x2 + self.j(1):.1f},{y2 + self.j(1):.1f}" '
                f'fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round" {extra}/>')

    def box(self, x, y, w, h, colour=PEN, sw=3.2, fill="none"):
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
        d = "M" + " L".join(f"{px + self.j(2.5):.1f},{py + self.j(2.5):.1f}" for px, py in pts)
        return f'<path d="{d}" fill="{fill}" stroke="{colour}" stroke-width="{sw}" stroke-linejoin="round"/>'

    def curve(self, pts, colour=PEN, w=3.2, head=True):
        (x1, y1), (cx, cy), (x2, y2) = pts
        out = f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round"/>'
        return out + (self.head(cx, cy, x2, y2, colour, w) if head else "")

    def arrow(self, x1, y1, x2, y2, colour=PEN, w=3.2):
        return self.line(x1, y1, x2, y2, colour, w, 1.5) + self.head(x1, y1, x2, y2, colour, w)

    def head(self, fx, fy, x, y, colour, w):
        import math
        a = math.atan2(y - fy, x - fx)
        p1 = (x - 18 * math.cos(a - 0.45), y - 18 * math.sin(a - 0.45))
        p2 = (x - 18 * math.cos(a + 0.45), y - 18 * math.sin(a + 0.45))
        return (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{x:.1f},{y:.1f} L{p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{colour}" '
                f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

    def brace(self, x, y1, y2, side=1, colour=PEN, w=3.2):
        """A curly bracket from y1 to y2 at x, its point towards side (+1 right, -1 left)."""
        m, d = (y1 + y2) / 2, 16 * side
        return (f'<path d="M{x:.1f},{y1:.1f} q{d:.1f},0 {d:.1f},14 L{x + d:.1f},{m - 14:.1f} q0,14 {d:.1f},14 q{-d:.1f},0 {-d:.1f},14 '
                f'L{x + d:.1f},{y2 - 14:.1f} q0,14 {-d:.1f},14" fill="none" stroke="{colour}" stroke-width="{w}" stroke-linecap="round"/>')

    def ring(self, cx, cy, rx, ry, colour=PEN, w=3.2):
        return (f'<ellipse cx="{cx + self.j(1):.1f}" cy="{cy + self.j(1):.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" '
                f'stroke="{colour}" stroke-width="{w}" transform="rotate({self.j(4):.1f} {cx} {cy})"/>')

    def strike(self, x1, x2, y, colour="#dc2626"):
        return self.line(x1, y, x2, y + self.j(2), colour, 3, 1.2)


def badge(x, y, n, colour, r=20):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{colour}" stroke="#fff" stroke-width="3"/>'
            + text(x, y + r * 0.36, str(n), int(r * 1.05), weight="bold", fill="#fff", anchor="middle"))


# ------------------------------------------------------------------ 1. the photograph, with callouts
def callouts(rv, page, out):
    pw, ph = 1000, 1333
    panel_x, panel_w = pw + 40, 720
    photo = out / page["photo"]
    cards, y = [], 120
    for note in page["notes"]:
        col = THEME[note["theme"]]
        written = wrap("“" + note["written"] + "”", 44)
        means = wrap(note["means"], 58)
        h = 34 + len(written) * 36 + len(means) * 26 + 40
        cards.append((note, y, h, written, means, col))
        y += h + 18
    H = max(ph, y + 40)
    body = [f'<image x="0" y="0" width="{pw}" height="{ph}" href="data:image/jpeg;base64,{b64(photo)}" xlink:href="data:image/jpeg;base64,{b64(photo)}"/>']
    for note, cy, h, written, means, col in cards:
        x, yy, w, hh = (note["region"][0] * pw, note["region"][1] * ph, note["region"][2] * pw, note["region"][3] * ph)
        body.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{w:.1f}" height="{hh:.1f}" rx="14" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-width="5"/>')
        bx, by = max(24, x), max(24, yy)
        body.append(f'<path d="M{x + w:.1f},{yy + hh / 2:.1f} L{panel_x - 4},{cy + 30}" stroke="{col}" stroke-width="2.5" stroke-opacity="0.55" fill="none" stroke-dasharray="6 6"/>')
        body.append(badge(bx, by, note["n"], col))
    body.append(f'<rect x="{pw + 20}" y="0" width="{panel_w + 40}" height="{H}" fill="#ffffff"/>')
    body.append(text(panel_x, 52, page["name"], 30, weight="bold"))
    body.append(text(panel_x, 88, "What the pen says, word for word, and what it means", 19, fill="#6b7280"))
    for note, cy, h, written, means, col in cards:
        body.append(f'<rect x="{panel_x}" y="{cy}" width="{panel_w}" height="{h}" rx="14" fill="#fff" stroke="{col}" stroke-width="2.5"/>')
        body.append(f'<rect x="{panel_x}" y="{cy}" width="10" height="{h}" rx="5" fill="{col}"/>')
        body.append(badge(panel_x + 40, cy + 34, note["n"], col, 18))
        body.append(text(panel_x + 72, cy + 40, rv["themes"][note["theme"]]["name"].upper(), 15, weight="bold", fill=col, extra='letter-spacing="1.5"'))
        body.append(text(panel_x + 30, cy + 80, written, 31, font=HAND, fill=PEN, lh=1.16))
        body.append(text(panel_x + 30, cy + 80 + len(written) * 36 + 4, means, 20, lh=1.3))
    return svg(panel_x + panel_w + 30, H, "".join(body), f"{page['name']}: the photograph, with Dinis's notes numbered and typed")


# ------------------------------------------------------------------ 2. the page redrawn, marks in place
def page_frame(body, w=1000, h=1414, foot=""):
    out = [f'<rect x="14" y="18" width="{w - 20}" height="{h - 24}" fill="#e5e7eb"/>',
           f'<rect x="6" y="8" width="{w - 20}" height="{h - 24}" fill="{PAPER}" stroke="#d1d5db"/>']
    out += body
    if foot:
        out.append(text(w / 2, h - 46, foot, 17, fill="#6b7280", anchor="middle"))
    return out


def note_mark(pen, x, y, lines, n, col, size=34, anchor="start", at=None):
    lines = lines if isinstance(lines, list) else [lines]
    bx, by = at or (x - 30, y - 12)
    return text(x, y, lines, size, font=HAND, fill=PEN, anchor=anchor, lh=1.05) + badge(bx, by, n, col, 15)


def tw(s, size):
    """An estimate of a sans-serif string's width, glyph class by glyph class, calibrated on Plex at 17px."""
    narrow, wide = set("il.,:;'()[]!|1 tfrjI"), set("mwMW@")
    units = sum(0.28 if c in narrow else 0.86 if c in wide else 0.66 if c.isupper() or c.isdigit() else 0.54 for c in s)
    return units * size * 0.998


def strikes(pen, lines, x0, y0, lh, cuts, size=17):
    """Strike the given substrings: cuts are (line index, first words, last words) in the typed lines."""
    out = []
    for i, start, end in cuts:
        s = lines[i]
        a = s.index(start)
        b = s.index(end, a) + len(end)
        out.append(pen.strike(x0 + tw(s[:a], size), x0 + tw(s[:b], size), y0 + i * lh - 6))
    return out


def redraw_title(rv):
    pen, t = Pen(11), THEME
    b = []
    b.append(text(500, 520, "SECOND EDITION · RELEASE CANDIDATE V2.0.0-RC2 · 2026-10-19", 16, fill="#4b5563", anchor="middle", extra='letter-spacing="2"'))
    b.append(text(500, 590, "Generation ZX Developers", 54, weight="bold", anchor="middle"))
    b.append(text(500, 640, "GenAI Startup Edition", 26, font="Georgia, serif", anchor="middle"))
    b.append(text(500, 690, "Dinis Cruz", 19, weight="bold", anchor="middle"))
    b.append('<rect x="150" y="725" width="700" height="170" rx="10" fill="#fafafa" stroke="#d1d5db"/>')
    lines = ["Release candidate 2 of the second edition: not signed off, not an official",
             "version. The first edition (2018) is the only official version. This candidate",
             "was written by the book's agents from the ideas register and is for reading and",
             "marking up. Its text is frozen as v2/versions/v2.0.0-rc2.md; the title is",
             "Dinis's decision of 19 October 2026 (decision 014). Text: CC BY 4.0."]
    b.append(text(175, 765, lines, 17, fill="#374151", lh=1.55))
    # what Dinis struck: from "The first edition" to "marking up.", and the title clause
    b += strikes(pen, lines, 175, 765, 17 * 1.55, [(1, "The first", "This candidate"), (2, "was", "reading and"),
                                                  (3, "marking", "up."), (3, "the title", "is"), (4, "Dinis", "014).")])
    b.append(pen.box(250, 90, 520, 250))
    b.append(note_mark(pen, 510, 200, ["Graph representation", "of book"], 1, t["show"], 44, "middle", at=(250, 90)))
    b.append(pen.curve([(250, 270), (110, 520), (120, 1080)]))
    b.append(note_mark(pen, 70, 1140, ["can also", "go here"], 2, t["show"], 38))
    b.append(badge(132, 742, 3, t["process-out"], 15))
    b.append(pen.curve([(856, 860), (900, 905), (880, 950)], head=False))
    b.append(note_mark(pen, 760, 985, ["should be", "what is the", "book all about"], 4, t["first-page"], 34))
    b.append(pen.arrow(700, 1010, 610, 905))
    b.append(note_mark(pen, 455, 1060, ["this paragraph", "buys more time", "from the reader to", "continue reading"], 5, t["first-page"], 34))
    return svg(1000, 1414, "".join(page_frame(b, foot="Generation ZX Developers (GenAI Startup Edition), release candidate · page 1 of 168")),
               "Page 1 redrawn, with Dinis's marks in place")


def contents_lines(rv, parts_ids, start_n, end_n, y0, lh=31):
    """The contents as the candidate prints them; returns the drawn lines and the y of each part and chapter."""
    ch = {c["n"]: c for c in rv["contents"]["chapters"]}
    title = {p["id"]: p["title"] for p in rv["contents"]["parts"]}
    out, ys, y = [], {}, y0
    for pid in parts_ids:
        nums = [n for n in range(start_n, end_n + 1) if ch[n]["part"] == pid]
        if not nums:
            continue
        out.append(text(110, y, title[pid], 20, weight="bold"))
        ys[pid] = y
        y += lh
        for n in nums:
            out.append(text(140, y, f"{n}. {ch[n]['title']}", 18))
            ys[n] = y
            y += lh
        y += 8
    return out, ys, y


ORDER = ["before-you-start", "the-frame", "getting-the-job", "working-with-agents", "judgement", "start-the-company",
         "build-it-without-a-server", "the-long-game", "hands-on-2026", "how-this-book-was-made"]


def redraw_contents1(rv):
    pen, t = Pen(22), THEME
    b = [text(110, 150, "Contents", 36, weight="bold")]
    lines, ys, _ = contents_lines(rv, ORDER, 1, 25, 200)
    b += lines
    b.append(note_mark(pen, 520, 82, "try a couple visualisations of this contents (first)", 6, t["show"], 34, "middle", at=(215, 70)))
    b.append(note_mark(pen, 880, 128, ["page", "number"], 7, t["altitude"], 30))
    b.append(pen.arrow(905, 160, 905, 215))
    y1, y2 = ys["before-you-start"] - 20, ys[5] + 8
    b.append(pen.brace(88, y1, y2, -1))
    b.append(pen.box(14, ys[5] + 20, 70, 38))
    b.append(text(49, ys[5] + 48, "start", 28, font=HAND, fill=PEN, anchor="middle"))
    b.append(badge(20, ys[5] + 18, 8, t["doing"], 13))
    b.append(pen.arrow(49, ys[5] + 64, 49, ys[5] + 108))
    b.append(text(49, ys[5] + 134, ["hands-on", "section"], 26, font=HAND, fill=PEN, anchor="middle", lh=1.0))
    b.append(note_mark(pen, 640, ys["the-frame"] - 18, "what about using this space", 9, t["show"], 30))
    for i, lab in enumerate((["for infographics", "explaining this chapter"], ["or graphs"], ["or storyboards"])):
        yy = ys["the-frame"] + i * 120
        b.append(pen.box(640, yy, 330, 96 if i == 0 else 70))
        b.append(text(805, yy + 42, lab, 30, font=HAND, fill=PEN, anchor="middle", lh=1.0))
    y1, y2 = ys[17] - 18, ys[25] + 8
    b.append(pen.brace(878, y1, y2, 1))
    b.append(note_mark(pen, 700, y2 + 62, ["ok but these are", "the details of the topics"], 10, t["altitude"], 32))
    b.append(pen.arrow(890, y2 + 36, 905, y2 - 20))
    return svg(1000, 1414, "".join(page_frame(b, foot="Generation ZX Developers (GenAI Startup Edition), release candidate · page 2 of 168")),
               "Page 2 redrawn, with Dinis's marks in place")


def redraw_contents2(rv):
    pen, t = Pen(33), THEME
    lines, ys, y = contents_lines(rv, ORDER, 26, 41, 110)
    b = list(lines)
    b.append(text(110, y + 50, "About this release candidate", 30, weight="bold", fill="#cbd5e1"))
    for i in range(5):
        b.append(f'<rect x="110" y="{y + 80 + i * 30}" width="{760 - (i % 3) * 90}" height="10" rx="5" fill="#e5e7eb"/>')
    y1, y2 = ys[30] - 20, ys[40] + 8
    b.append(pen.brace(760, y1, y2, 1))
    b.append(note_mark(pen, 815, (y1 + y2) / 2 - 60, ["these need", "to be spread", "across the", "book"], 11, t["doing"], 34))
    b.append(note_mark(pen, 590, 1150, ["By now the reader should", "be very curious and", "excited to continue reading"], 12, t["first-page"], 34))
    b.append(pen.ring(760, 1362, 66, 22))
    b.append(pen.arrow(765, 1334, 745, 1240))
    b.append(note_mark(pen, 140, 1170, ["with this current", "version I'm not"], 13, t["process-out"], 34))
    b.append(pen.line(130, 1214, 330, 1214))
    b.append(pen.arrow(430, 1185, 560, 1170))
    return svg(1000, 1414, "".join(page_frame(b, foot="Generation ZX Developers (GenAI Startup Edition), release candidate · page 3 of 168")),
               "Page 3 redrawn, with Dinis's marks in place")


# ------------------------------------------------------------------ 3. after: the title page and the contents
def after_title_page(rv):
    b = []
    names = [("you", "You"), ("before-you-start", "Start"), ("the-frame", "The frame"), ("working-with-agents", "Agents"),
             ("judgement", "Judgement"), ("start-the-company", "The company"), ("build-it-without-a-server", "No server"),
             ("company", "A company")]
    xs = [90 + i * 117 for i in range(len(names))]
    ys = [250 + (60 if i % 2 else -40) for i in range(len(names))]
    for i in range(len(names) - 1):
        b.append(f'<line x1="{xs[i]}" y1="{ys[i]}" x2="{xs[i + 1]}" y2="{ys[i + 1]}" stroke="#94a3b8" stroke-width="4"/>')
    for i, (k, lab) in enumerate(names):
        end = k in ("you", "company")
        col = "#16a34a" if k == "company" else ("#1d3a8a" if k == "you" else "#2563eb")
        b.append(f'<circle cx="{xs[i]}" cy="{ys[i]}" r="{30 if end else 20}" fill="{col if end else "#fff"}" stroke="{col}" stroke-width="5"/>')
        b.append(text(xs[i], ys[i] + (66 if i % 2 else -48), lab, 20, weight="bold", fill=col, anchor="middle"))
    b.append(text(500, 120, "THE BOOK AS A GRAPH: FROM YOU TO A COMPANY", 15, fill="#6b7280", anchor="middle", extra='letter-spacing="2"'))
    b.append(text(500, 520, "Generation ZX Developers", 54, weight="bold", anchor="middle"))
    b.append(text(500, 570, "GenAI Startup Edition", 26, font="Georgia, serif", anchor="middle"))
    b.append(text(500, 615, "Dinis Cruz", 19, weight="bold", anchor="middle"))
    para = ["Two generations, one objective: by the end of this book, you have",
            "started a GenAI company. You will brief agents the way a developer",
            "does, ship something a stranger can use, find out whether they miss",
            "it, put a price on it, and build it without a server of your own.",
            "Each part ends with something you can now do. Start on the next page."]
    b.append('<rect x="120" y="660" width="760" height="210" rx="12" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>')
    b.append(text(150, 705, para, 20, lh=1.55))
    b.append(text(500, 920, "draft wording, to be written by the editor", 22, font=HAND, fill="#2563eb", anchor="middle"))
    b.append(text(500, 1300, "Release candidate 2 · not signed off · frozen as v2.0.0-rc2 · CC BY 4.0", 16, fill="#9ca3af", anchor="middle"))
    b.append(text(500, 1340, "(the graph can also go here, at the bottom)", 20, font=HAND, fill="#9ca3af", anchor="middle"))
    return svg(1000, 1414, "".join(page_frame(b)), "Sketch: the title page after the change")


def after_contents_map(rv):
    ch = rv["contents"]["chapters"]
    title = {p["id"]: p["title"] for p in rv["contents"]["parts"]}
    intro = {p["id"]: p["intro"] for p in rv["contents"]["parts"]}
    order = [p for p in ORDER if p != "hands-on-2026"]
    b = [text(70, 90, "Contents, as topics first", 34, weight="bold"),
         text(70, 124, ["Each part is a topic with its point and what you can do after it; chapters are the detail;", "the hands-on chapters (green) sit beside the part they practise."], 15, fill="#6b7280")]
    y = 186
    glyph = ["graph", "map", "strip"]
    for i, pid in enumerate(order):
        nums = [c for c in ch if c["part"] == pid] + [c for c in ch if SPREAD.get(c["n"]) == pid]
        nums.sort(key=lambda c: (c["part"] == "hands-on-2026", c["n"]))
        first = min(c["page"] for c in nums)
        point = wrap(intro[pid].split(". ")[0].rstrip(".") + ".", 70)[:2]
        h = 64 + len(point) * 20 + ((len(nums) + 1) // 2) * 22
        b.append(f'<rect x="60" y="{y}" width="880" height="{h}" rx="12" fill="#fff" stroke="#e5e7eb"/>')
        b.append(text(84, y + 32, title[pid], 21, weight="bold"))
        b.append(text(716, y + 32, f"p. {first}", 19, fill="#6b7280", anchor="end"))
        b.append(text(84, y + 56, point, 15, fill="#374151", lh=1.3))
        b.append(text(84, y + 58 + len(point) * 20, "you can: " + MILESTONE[pid], 16, font=HAND, fill="#16a34a"))
        cy = y + 82 + len(point) * 20
        for k, c in enumerate(nums):
            cx = 90 + (k % 2) * 315
            yy = cy + (k // 2) * 22
            ho = c["part"] == "hands-on-2026"
            lab = (c["title"][:34] + "…") if len(c["title"]) > 35 else c["title"]
            b.append(text(cx, yy, f"{c['n']}. {lab}  {c['page']}", 13, fill="#16a34a" if ho else "#4b5563", weight="bold" if ho else "normal"))
        g = glyph[i % 3]
        gx, gy = 760, y + 14
        b.append(f'<rect x="{gx}" y="{gy}" width="160" height="{h - 28}" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-dasharray="5 5"/>')
        if g == "graph":
            pts = [(gx + 40, gy + 30), (gx + 110, gy + 24), (gx + 80, gy + 60), (gx + 130, gy + 70)]
            b += [f'<line x1="{a[0]}" y1="{a[1]}" x2="{c2[0]}" y2="{c2[1]}" stroke="#94a3b8" stroke-width="3"/>' for a, c2 in zip(pts, pts[1:])]
            b += [f'<circle cx="{px}" cy="{py}" r="8" fill="#2563eb"/>' for px, py in pts]
        elif g == "map":
            b += [f'<rect x="{gx + 20 + k * 40}" y="{gy + 70 - k * 14}" width="28" height="{14 + k * 14}" fill="#93c5fd"/>' for k in range(3)]
        else:
            b += [f'<rect x="{gx + 16 + k * 46}" y="{gy + 22}" width="40" height="48" rx="4" fill="#fff" stroke="#64748b" stroke-width="2"/>' for k in range(3)]
        b.append(text(gx + 80, gy + h - 40, "infographic, graph or strip", 12, fill="#64748b", anchor="middle"))
        y += h + 12
    return svg(1000, y + 40, "".join(page_frame(b, h=y + 40)), "Sketch: the contents as topics first, with page numbers, milestones and a picture beside each part")


def after_contents_line(rv):
    ch = rv["contents"]["chapters"]
    title = {p["id"]: p["title"] for p in rv["contents"]["parts"]}
    order = [p for p in ORDER if p != "hands-on-2026"]
    W, H = 1000, 1414
    b = [text(70, 90, "Contents, as a line from you to a company", 34, weight="bold"),
         text(70, 124, ["One stop per part, with the page it starts on; the green branches are the hands-on", "chapters, spread across the book, with the page each starts on today."], 15, fill="#6b7280")]
    x0, y0, step = 200, 232, 126
    b.append(f'<line x1="{x0}" y1="{y0 - 40}" x2="{x0}" y2="{y0 + step * (len(order) - 1) + 40}" stroke="#1d3a8a" stroke-width="12" stroke-linecap="round"/>')
    for i, pid in enumerate(order):
        y = y0 + i * step
        own = [c for c in ch if c["part"] == pid]
        first = min(c["page"] for c in own)
        b.append(f'<circle cx="{x0}" cy="{y}" r="22" fill="#fff" stroke="#1d3a8a" stroke-width="7"/>')
        b.append(text(x0 - 40, y + 8, f"p. {first}", 20, fill="#6b7280", anchor="end"))
        b.append(text(x0 + 44, y - 6, title[pid], 22, weight="bold"))
        b.append(text(x0 + 44, y + 20, f"{len(own)} chapter{'s' if len(own) > 1 else ''} · you can: {MILESTONE[pid]}", 16, fill="#374151"))
        ho = [c for c in ch if SPREAD.get(c["n"]) == pid]
        for k, c in enumerate(ho):
            bx, by, ly = 735, y - 14 + k * 30, y + 36 + k * 6
            b.append(f'<path d="M{x0 + 16},{y + 16} Q{x0 + 30},{ly} {x0 + 60},{ly} L{bx - 50},{ly} Q{bx - 25},{ly} {bx - 25},{(ly + by) / 2} '
                     f'Q{bx - 25},{by} {bx - 11},{by}" fill="none" stroke="#16a34a" stroke-width="3"/>')
            b.append(f'<circle cx="{bx}" cy="{by}" r="9" fill="#16a34a"/>')
            lab = (c["title"][:24] + "…") if len(c["title"]) > 25 else c["title"]
            b.append(text(bx + 16, by + 5, f"{lab} {c['page']}", 15, fill="#166534", weight="bold"))
    b.append(text(x0, y0 - 64, "you", 26, font=HAND, fill="#1d3a8a", anchor="middle"))
    b.append(text(x0, y0 + step * (len(order) - 1) + 80, "a company", 30, font=HAND, fill="#16a34a", anchor="middle"))
    return svg(W, H, "".join(page_frame(b)), "Sketch: the contents as a line from you to a company, with the hands-on chapters as branches")


def contents_of(candidate):
    """The candidate's contents and page numbers, from whichever review of that candidate records them."""
    for f in sorted(SRC.glob("*.json")):
        rv = json.loads(f.read_text(encoding="utf-8"))
        if rv.get("candidate") == candidate and rv.get("contents"):
            return rv["contents"]
    raise SystemExit(f"paper reviews: no review of {candidate} records its contents")


def after_before_you_read(rv):
    """Notes 22 to 26: the page before chapter 1, for the reader, not for the author."""
    b = [text(500, 120, "Before you read", 44, weight="bold", anchor="middle"),
         text(500, 160, "a sketch of the page after About this release candidate moves to the end", 20, font=HAND, fill="#2563eb", anchor="middle")]
    b.append('<rect x="90" y="200" width="820" height="150" rx="16" fill="#fef3c7" stroke="#d97706" stroke-width="3"/>')
    b.append(text(130, 255, "Reading this on a screen? Stop, and print it.", 30, weight="bold"))
    b.append(text(130, 300, ["This book is made to be read on paper, with a pen. Every chapter", "is a PDF on the website, ready to print."], 19, fill="#374151", lh=1.4))
    b.append(text(90, 410, "The book's website", 28, weight="bold"))
    items = [("The tools and visualisations", "the graph of the book, the storyboards, the infographics, the reader"),
             ("The chapter PDFs, for print", "one per chapter, or the whole book"),
             ("Everything else, in public", "the articles, the decisions, the reviews: every material, open")]
    for i, (h, d) in enumerate(items):
        y = 460 + i * 92
        b.append(f'<rect x="90" y="{y - 30}" width="820" height="76" rx="12" fill="#fff" stroke="#cbd5e1"/>')
        b.append(f'<circle cx="130" cy="{y + 8}" r="14" fill="#2563eb"/>')
        b.append(text(160, y, h, 21, weight="bold"))
        b.append(text(160, y + 28, d, 17, fill="#4b5563"))
    b.append(text(90, 790, "Yours to copy, share, sell and remix", 28, weight="bold"))
    b.append(text(90, 826, "The whole text is under Creative Commons Attribution (CC BY 4.0), a copyright licence that gives you rights:", 17, fill="#374151"))
    verbs = ["copy it", "distribute it", "sell it", "remix it"]
    for i, v in enumerate(verbs):
        x = 90 + i * 210
        b.append(f'<rect x="{x}" y="850" width="190" height="90" rx="14" fill="#ecfdf5" stroke="#16a34a" stroke-width="3"/>')
        b.append(text(x + 95, 905, v, 24, weight="bold", fill="#166534", anchor="middle"))
    b.append(text(90, 985, "All you need to do is give a small credit for where the text came from.", 19, fill="#374151"))
    b.append('<rect x="90" y="1030" width="820" height="210" rx="16" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>')
    b.append(text(130, 1085, "Why read this book, and why keep going", 26, weight="bold"))
    b.append(text(130, 1125, ["By the end, you have started a GenAI company. Every part ends with", "something you can now do. The first thing to do is on the next page."], 19, fill="#374151", lh=1.45))
    b.append(text(500, 1215, "(note 26: answer these by page 5)", 22, font=HAND, fill="#2563eb", anchor="middle"))
    return svg(1000, 1414, "".join(page_frame(b)), "Sketch: the page before chapter 1, after the review")


def after_part_opener(rv):
    """Note 27: the part opener with a picture of the part, drawn from the candidate's contents."""
    cont = contents_of(rv["candidate"])
    chs = [c for c in cont["chapters"] if c["part"] == "before-you-start"]
    b = [text(110, 150, "PART 1", 22, fill="#4b5563", extra='letter-spacing="3"'),
         text(110, 215, "Before you start", 54, weight="bold"),
         text(110, 265, ["Who this book is for and what it is for, why you are lucky to be here,", "why everything is a graph, where you land, and why the path only", "makes sense afterwards."], 21, fill="#374151", lh=1.45)]
    xs = [170, 330, 500, 670, 830]
    ys = [620, 500, 640, 500, 620]
    names = ["Gen ZX", "Lucky to be here", "Everything is connected", "Where do you land?", "Connect the dots"]
    for i in range(len(xs) - 1):
        b.append(f'<line x1="{xs[i]}" y1="{ys[i]}" x2="{xs[i + 1]}" y2="{ys[i + 1]}" stroke="#94a3b8" stroke-width="5"/>')
    b.append(f'<path d="M{xs[-1]},{ys[-1] + 110} C{xs[-1]},800 700,860 600,878" fill="none" stroke="#16a34a" stroke-width="5" stroke-dasharray="10 8"/>')
    for i, c in enumerate(chs):
        b.append(f'<circle cx="{xs[i]}" cy="{ys[i]}" r="38" fill="#fff" stroke="#2563eb" stroke-width="6"/>')
        b.append(text(xs[i], ys[i] + 11, str(c["n"]), 30, weight="bold", fill="#2563eb", anchor="middle"))
        lab = wrap(names[i], 12)
        b.append(text(xs[i], ys[i] + (70 if ys[i] > 560 else -80 - 22 * (len(lab) - 1)), lab, 19, weight="bold", anchor="middle", lh=1.15))
        b.append(text(xs[i], ys[i] + (70 if ys[i] > 560 else -80 - 22 * (len(lab) - 1)) + 22 * len(lab), f"p. {c['page']}", 16, fill="#6b7280", anchor="middle"))
    b.append('<rect x="250" y="880" width="500" height="120" rx="18" fill="#ecfdf5" stroke="#16a34a" stroke-width="3"/>')
    b.append(text(500, 930, "After this part, you can:", 22, weight="bold", fill="#166534", anchor="middle"))
    b.append(text(500, 968, "name your problem, and where you stand", 22, fill="#166534", anchor="middle"))
    b.append(text(500, 1100, ["a sketch for note 27: the part as a graph, its chapters", "as the stops, and the milestone it ends on"], 24, font=HAND, fill="#2563eb", anchor="middle", lh=1.1))
    return svg(1000, 1414, "".join(page_frame(b)), "Sketch: the opener of Part 1 with a graph of the part")


FATE_COLOUR = {"keep": "#16a34a", "fix": "#65a30d", "rewrite": "#2563eb", "forward": "#9333ea", "end": "#d97706", "cut": "#dc2626"}


def after_chapter_one(rv):
    """Notes 28 to 51 on chapter 1, as a map of its paragraphs and what happens to each."""
    data = rv["chapter_one"]
    blocks = data["blocks"]
    W, top, bh, gap = 1000, 190, 46, 10
    H = top + len(blocks) * (bh + gap) + 330
    b = [text(70, 90, "Chapter 1, paragraph by paragraph", 34, weight="bold"),
         text(70, 126, "What the pen asks for each paragraph of Gen ZX: who this book is for, and what it is for (rc2, pages 7 to 9)", 16, fill="#6b7280")]
    lx = 70
    for i, (k, lab) in enumerate(data["fates"].items()):
        x = lx + i * 150
        b.append(f'<rect x="{x}" y="146" width="20" height="20" rx="4" fill="{FATE_COLOUR[k]}"/>')
        b.append(text(x + 28, 162, lab, 14, fill="#374151"))
    y, section = top, None
    end_ys, fwd_ys = [], []
    for blk in blocks:
        if blk["section"] != section:
            section = blk["section"]
        col = FATE_COLOUR[blk["fate"]]
        cut = blk["fate"] == "cut"
        b.append(f'<rect x="150" y="{y}" width="560" height="{bh}" rx="10" fill="{col}" fill-opacity="{0.10 if cut else 0.16}" stroke="{col}" stroke-width="2.5"{" stroke-dasharray=\"7 6\"" if cut else ""}/>')
        b.append(text(165, y + 29, blk["first"], 16, fill="#9ca3af" if cut else INK, extra='text-decoration="line-through"' if cut else ""))
        if blk["notes"]:
            b.append(text(700, y + 29, "notes " + ", ".join(str(n) for n in blk["notes"]), 13, fill=col, anchor="end"))
        b.append(text(140, y + 29, blk["section"] if blocks.index(blk) == 0 or blocks[blocks.index(blk) - 1]["section"] != blk["section"] else "", 13, fill="#6b7280", anchor="end"))
        if blk["fate"] == "end":
            end_ys.append(y + bh / 2)
        if blk["fate"] == "forward":
            fwd_ys.append(y + bh / 2)
        y += bh + gap
    ey = y + 60
    b.append(f'<rect x="150" y="{ey}" width="560" height="110" rx="14" fill="#fff7ed" stroke="#d97706" stroke-width="3"/>')
    b.append(text(430, ey + 45, "At the end of the book", 22, weight="bold", fill="#9a3412", anchor="middle"))
    b.append(text(430, ey + 78, "how this book was written, and evolved", 19, fill="#9a3412", anchor="middle"))
    for k, yy in enumerate(end_ys):
        x = 740 + k * 22
        b.append(f'<path d="M710,{yy} L{x},{yy} L{x},{ey + 55} L712,{ey + 55}" fill="none" stroke="#d97706" stroke-width="2.5"/>')
    for yy in fwd_ys:
        b.append(f'<path d="M150,{yy} L95,{yy} L95,{top + 4} L148,{top + 4}" fill="none" stroke="#9333ea" stroke-width="3"/>')
        b.append(text(88, (yy + top) / 2, "the reason to read it, first", 15, font=HAND, fill="#9333ea", anchor="middle", extra=f'transform="rotate(-90 88 {(yy + top) / 2})"'))
    return svg(W, H, "".join(page_frame(b, h=H)), "Sketch: chapter 1 of rc2, paragraph by paragraph, with what happens to each")


def after_reviewer_page(rv):
    """Note 51 and decision 018: a page of the reviewer edition, with boxes the reviewer answers in pen."""
    pen = Pen(51)
    b = ['<rect x="6" y="8" width="980" height="64" fill="#4f46e5"/>',
         text(40, 50, "REVIEWER EDITION \u00b7 release candidate 3 \u00b7 not the edition for sale", 20, weight="bold", fill="#fff", extra='letter-spacing="1.5"'),
         text(40, 130, "1  Gen ZX: who this book is for", 32, weight="bold")]
    y = 180
    for i in range(22):
        if i in (6, 7, 8):
            if i == 6:
                b.append(f'<rect x="34" y="{y - 22}" width="590" height="96" rx="6" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>')
                b.append(badge(30, y - 20, "R8", "#4f46e5", 17))
        w = 560 - (i * 37 % 120)
        b.append(f'<rect x="50" y="{y - 12}" width="{w}" height="11" rx="5" fill="#d1d5db"/>')
        y += 32
        if i == 13:
            y += 20
    # the margin: review boxes
    bx, bw = 660, 310
    boxes = [
        ("R7", "Page 7 named the author's daughters. Here it says:", ["keep 'kids'", "'children'", "cut the line"], 0),
        ("R8", "Which story is this paragraph telling?", ["Gen X builds it for Gen Z", "Gen Z builds it for Gen X", "both ways (note 36)"], 0),
        ("R9", "Too much detail for chapter 1?", ["yes, cut", "no, keep", "move to part 7"], 3),
    ]
    by = 110
    for rid, q, opts, lines in boxes:
        h = 64 + len(wrap(q, 30)) * 22 + len(opts) * 34 + 70
        b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{h}" rx="12" fill="#fff" stroke="#4f46e5" stroke-width="2.5"/>')
        b.append(badge(bx + 26, by + 26, rid, "#4f46e5", 17))
        b.append(text(bx + 54, by + 32, "for reviewers", 14, weight="bold", fill="#4f46e5", extra='letter-spacing="1"'))
        qy = by + 62
        b.append(text(bx + 18, qy, wrap(q, 30), 17, lh=1.3))
        oy = qy + len(wrap(q, 30)) * 22 + 12
        for k, o in enumerate(opts):
            b.append(f'<rect x="{bx + 18}" y="{oy + k * 34 - 16}" width="20" height="20" rx="3" fill="#fff" stroke="#374151" stroke-width="2"/>')
            b.append(text(bx + 48, oy + k * 34, o, 16, fill="#374151"))
        ly = oy + len(opts) * 34 + 6
        if rid == "R8":
            tick_x, tick_y, ans_y = bx + 22, oy + 2 * 34 - 8, ly - 4
        for k in range(2):
            b.append(f'<line x1="{bx + 18}" y1="{ly + k * 26}" x2="{bx + bw - 18}" y2="{ly + k * 26}" stroke="#cbd5e1" stroke-width="1.5"/>')
        by += h + 22
    # a space to draw
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{1150 - by}" rx="12" fill="#fafafa" stroke="#4f46e5" stroke-width="2.5" stroke-dasharray="9 7"/>')
    b.append(badge(bx + 26, by + 26, "R10", "#4f46e5", 19))
    b.append(text(bx + 56, by + 32, "draw it here", 14, weight="bold", fill="#4f46e5"))
    b.append(text(bx + 18, by + 62, ["The graph of this part, as you", "see it: the chapters, and how", "they connect."], 16, fill="#6b7280", lh=1.3))
    # a reviewer's pen, answering
    b.append(pen.line(tick_x, tick_y, tick_x + 9, tick_y + 10, PEN, 3.5) + pen.line(tick_x + 9, tick_y + 10, tick_x + 26, tick_y - 14, PEN, 3.5))
    b.append(text(bx + 22, ans_y, "it goes both ways!", 26, font=HAND, fill=PEN))
    b.append(f'<rect x="34" y="{1180}" width="930" height="120" rx="12" fill="#eef2ff" stroke="#4f46e5"/>')
    b.append(text(60, 1222, "How to answer", 20, weight="bold", fill="#3730a3"))
    b.append(text(60, 1254, ["Tick, write or draw in the boxes, then photograph the page. Every box has an id (R7, R8 ...),", "so each answer is read back to the question it answers, and recorded with the review."], 16, fill="#3730a3", lh=1.4))
    return svg(1000, 1414, "".join(page_frame(b, foot="Generation ZX Developers, reviewer edition \u00b7 page 7")), "Sketch: a page of the reviewer edition, with boxes to tick, write and draw in")


def qr_image(qid, x, y, size):
    """A drawn QR code (q/<id>/qr.svg, made by qr_codes.py), embedded so the sketch stands alone."""
    return (f'<image x="{x}" y="{y}" width="{size}" height="{size}" '
            f'href="data:image/svg+xml;base64,{b64(ROOT / "q" / qid / "qr.svg")}"/>')


def after_margin_system(rv):
    """Notes 64 to 75: facts and opinions marked, concepts explained in a line, and QR codes where the page needs room."""
    links = json.loads((ROOT / "admin/content/qr/links.json").read_text(encoding="utf-8"))["links"]
    FACT, OPIN, STORY, CONC = "#0f766e", "#b45309", "#7c3aed", "#db2777"
    b = [text(60, 90, "Technology that finally works for you", 30, weight="bold"),
         text(60, 122, "a sketch of chapter 2 with the margin system: what is fact, what is opinion, and where the site takes over", 16, fill="#6b7280")]
    paras = [
        ("story", ["Two years in, I have never felt happier at work, or more", "empowered. That is my own account, and there are others", "like it, and others that are not."], "two-years"),
        ("opinion", ["This is the biggest opportunity of your career, whether it", "is starting or twenty years in: the moment when you can", "still be a player, before things stabilise."], None),
        ("fact", ["People learn more from text read on paper than on a", "screen, in study after study; so print this book and", "read it with a pen."], None),
        ("concept", ["A UI, a user interface, is the part of software you see and", "touch: the screen, the buttons, the form. Think of a car's", "dashboard: the engine is the program, the dashboard is the UI."], "custom-ui"),
        ("opinion", ["When an interface costs an afternoon, you stop asking", "whether it is worth building, and start asking which", "moment it is for."], "victor"),
    ]
    mark = {"fact": (FACT, "FACT", "backed by data, with its source"), "opinion": (OPIN, "OPINION", "mine; no data yet"),
            "story": (STORY, "STORY", "my own account"), "concept": (CONC, "CONCEPT", "explained in a line")}
    y = 190
    for kind, lines, qid in paras:
        col, lab, sub = mark[kind]
        h = len(lines) * 30 + 20
        if kind == "concept":
            b.append(f'<rect x="52" y="{y - 30}" width="590" height="{h + 8}" rx="10" fill="#fdf2f8" stroke="{col}" stroke-width="2"/>')
        b.append(text(80, y, lines, 19, lh=1.5))
        if kind == "fact":
            b.append(f'<circle cx="62" cy="{y - 7}" r="8" fill="{col}"/>')
        elif kind == "opinion":
            b.append(f'<circle cx="62" cy="{y - 7}" r="8" fill="#fff" stroke="{col}" stroke-width="3"/>')
        elif kind == "story":
            b.append(f'<rect x="55" y="{y - 14}" width="14" height="14" fill="{col}" transform="rotate(45 62 {y - 7})"/>')
        b.append(text(670, y - 2, lab, 14, weight="bold", fill=col, extra='letter-spacing="1.5"'))
        b.append(text(670, y + 18, sub, 14, fill="#6b7280"))
        if kind == "fact":
            b.append(text(670, y + 40, "ref: the reading studies (to find, note 76)", 13, fill=col))
        if qid:
            b.append(qr_image(qid, 870, y - 26, 92))
            b.append(text(916, y + 82, "/q/" + qid, 12, fill="#374151", anchor="middle"))
        y += h + 70
    b.append(f'<rect x="52" y="{y - 10}" width="908" height="230" rx="14" fill="#f8fafc" stroke="#cbd5e1"/>')
    b.append(text(80, y + 26, "The margin, in four marks", 20, weight="bold"))
    for i, k in enumerate(("fact", "opinion", "story", "concept")):
        col, lab, sub = mark[k]
        yy = y + 66 + i * 34
        if k == "fact":
            b.append(f'<circle cx="92" cy="{yy - 6}" r="8" fill="{col}"/>')
        elif k == "opinion":
            b.append(f'<circle cx="92" cy="{yy - 6}" r="8" fill="#fff" stroke="{col}" stroke-width="3"/>')
        elif k == "story":
            b.append(f'<rect x="85" y="{yy - 13}" width="14" height="14" fill="{col}" transform="rotate(45 92 {yy - 6})"/>')
        else:
            b.append(f'<rect x="84" y="{yy - 14}" width="16" height="16" rx="3" fill="#fdf2f8" stroke="{col}" stroke-width="2"/>')
        b.append(text(116, yy, f"{lab.lower()}: {sub}", 17, fill="#374151"))
    b.append(text(560, y + 66, ["and a QR code where the page needs", "more room: the source, the explainer,", "the talk, the visualisation; each one a", "short address on the book's site, so it", "never goes out of date"], 16, fill="#374151", lh=1.35))
    b.append(text(500, 1330, "a sketch for notes 64 to 75, and Dinis's memo on QR codes; the marks and the wording are proposals", 18, font=HAND, fill=PEN, anchor="middle"))
    return svg(1000, 1414, "".join(page_frame(b)), "Sketch: a page with facts and opinions marked, a concept explained in a line, and QR codes to the site")


DRAW = {"redraw_title": redraw_title, "redraw_contents1": redraw_contents1, "redraw_contents2": redraw_contents2,
        "after_title_page": None, "after_contents_map": None, "after_contents_line": None,
        "after_before_you_read": after_before_you_read, "after_part_opener": after_part_opener, "after_chapter_one": after_chapter_one,
        "after_reviewer_page": after_reviewer_page,
        "after_margin_system": after_margin_system}


def build_paper_reviews(ctx):
    """Draw every review: the callouts for each photographed page, then the drawings the review names. A drawing named
    with a page ("redraw_title:page-1") is written as <page>-redrawn.svg; one without, as after-<name>.svg."""
    DRAW.update({"after_title_page": after_title_page, "after_contents_map": after_contents_map, "after_contents_line": after_contents_line})
    written = []
    for f in sorted(SRC.glob("*.json")):
        rv = json.loads(f.read_text(encoding="utf-8"))
        out = ROOT / "reviews/paper" / rv["id"]
        for page in rv["pages"]:
            for n in page["notes"]:
                if n["theme"] not in rv["themes"]:
                    raise SystemExit(f"paper review {f.name}: note {n['n']} has an unknown theme {n['theme']}")
            (out / f"{page['id']}-callouts.svg").write_text(callouts(rv, page, out), encoding="utf-8")
        for spec in rv.get("drawings", []):
            name, _, page = spec.partition(":")
            if name not in DRAW:
                raise SystemExit(f"paper review {f.name}: unknown drawing {name}")
            target = f"{page}-redrawn.svg" if page else "after-" + name.replace("after_", "").replace("_", "-") + ".svg"
            (out / target).write_text(DRAW[name](rv), encoding="utf-8")
        written.append(rv["id"])
    if "page" in ctx:
        build_hub(ctx)
    return written


# ------------------------------------------------------------------ the hub: every page, every note, in one place
def build_hub(ctx):
    """reviews/paper/index.html and reviews/paper/notes.json: every page reviewed, mapped to its chapter, and every
    note in one table, filterable by theme, chapter and batch. The chapter is the last one starting on or before the
    page, from the contents in rc2-01; a page before chapter 1 is front matter."""
    page, esc_, write = ctx["page"], ctx["esc"], ctx["write"]
    reviews = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(SRC.glob("*.json"))]
    chapters = next(rv["contents"]["chapters"] for rv in reviews if "contents" in rv)
    themes = {}
    for rv in reviews:
        themes.update(rv["themes"])

    def chapter_of(num):
        ch = [c for c in chapters if c["page"] <= num]
        return (f'{ch[-1]["n"]}. {ch[-1]["title"]}', f'ch{ch[-1]["n"]}') if ch else ("Front matter", "front")

    pages, notes = [], []
    for rv in reviews:
        if not rv.get("article"):
            raise SystemExit(f"paper review {rv['id']}: no article")
        for pg in rv["pages"]:
            num = int(pg["id"].split("-")[1])
            chap, ckey = chapter_of(num)
            pages.append({"batch": rv["id"], "part": rv["part"], "page": num, "id": pg["id"], "name": pg["name"], "chapter": chap,
                          "ckey": ckey, "article": rv["article"], "photo": f'{rv["id"]}/{pg["photo"]}',
                          "callouts": f'{rv["id"]}/{pg["id"]}-callouts.svg', "notes": [n["n"] for n in pg["notes"]]})
            for n in pg["notes"]:
                notes.append({"n": n["n"], "batch": rv["id"], "page": num, "chapter": chap, "ckey": ckey, "theme": n["theme"],
                              "theme_name": themes[n["theme"]]["name"], "written": n["written"], "means": n["means"],
                              "article": rv["article"], "callouts": f'{rv["id"]}/{pg["id"]}-callouts.svg'})
    nums = [n["n"] for n in notes]
    if nums != list(range(1, len(nums) + 1)):
        raise SystemExit("paper reviews: the notes are not numbered 1 to N in order across the batches")
    count = lambda key, v: sum(1 for n in notes if n[key] == v)
    used = [t for t in themes if count("theme", t)]
    ckeys = list(dict.fromkeys(n["ckey"] for n in notes))
    cname = {n["ckey"]: n["chapter"] for n in notes}
    dot = lambda t: f'<span style="display:inline-block;width:.7em;height:.7em;border-radius:50%;background:{THEME[t]};margin-right:.35em"></span>'
    art = lambda a, pid: f'../../agent-articles/{a}.html#{pid}'

    cards = "".join(
        f'<a class="pr-card" href="{esc_(p["callouts"])}" title="{esc_(p["name"])}: the photograph with the notes typed">'
        f'<img src="{esc_(p["photo"])}" alt="Page {p["page"]} of the printed candidate, marked" loading="lazy" width="150" height="200">'
        f'<b>Page {p["page"]}</b><span class="small">{esc_(p["chapter"])}</span>'
        f'<span class="small dim">{f"notes {p['notes'][0]} to {p['notes'][-1]}" if len(p["notes"]) > 1 else f"note {p['notes'][0]}"} &middot; part {p["part"]}</span></a>'
        for p in pages)
    matrix_head = "".join(f'<th title="{esc_(themes[t]["name"])}">{dot(t)}</th>' for t in used)
    matrix = "".join(
        f'<tr><td class="small">{esc_(cname[k])}</td>' + "".join(
            f'<td class="small">{sum(1 for n in notes if n["ckey"] == k and n["theme"] == t) or ""}</td>' for t in used)
        + f'<td class="small"><b>{count("ckey", k)}</b></td></tr>' for k in ckeys)
    legend = "".join(f'<li>{dot(t)}<b>{esc_(themes[t]["name"])}</b> ({count("theme", t)}): {esc_(themes[t]["principle"])}</li>' for t in used)
    chips_t = '<button type="button" class="chip" data-k="theme" data-v="all" aria-pressed="true">all themes</button>' + "".join(
        f'<button type="button" class="chip" data-k="theme" data-v="{t}" aria-pressed="false">{dot(t)}{esc_(themes[t]["name"])} {count("theme", t)}</button>' for t in used)
    chips_c = '<button type="button" class="chip" data-k="ch" data-v="all" aria-pressed="true">all pages</button>' + "".join(
        f'<button type="button" class="chip" data-k="ch" data-v="{k}" aria-pressed="false">{esc_(cname[k])} {count("ckey", k)}</button>' for k in ckeys)
    rows = "".join(
        f'<tr id="n{n["n"]}" data-theme="{n["theme"]}" data-ch="{n["ckey"]}"><td><a href="#n{n["n"]}"><b>{n["n"]}</b></a></td>'
        f'<td class="small"><a href="{esc_(n["callouts"])}">p. {n["page"]}</a><br><span class="dim">{esc_(n["chapter"])}</span></td>'
        f'<td class="small">{dot(n["theme"])}{esc_(n["theme_name"])}</td>'
        f'<td><span class="pr-pen">{esc_(n["written"])}</span></td><td class="small">{esc_(n["means"])}</td>'
        f'<td class="small"><a href="{art(n["article"], "page-" + str(n["page"]))}">article</a></td></tr>'
        for n in notes)
    style = ('<style>.pr-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:.8rem;margin:1rem 0}'
             '.pr-card{display:flex;flex-direction:column;gap:.15rem;text-decoration:none;color:inherit;border:1px solid var(--line2);border-radius:10px;padding:.5rem;background:var(--panel)}'
             '.pr-card img{width:100%;height:auto;border-radius:6px}.pr-pen{font-family:Caveat,cursive;font-size:1.25rem;line-height:1.15;color:#1d3a8a}'
             '#pr-notes td{vertical-align:top}#pr-search{font:inherit;padding:.3rem .6rem;border:1px solid var(--line2);border-radius:8px;min-width:16rem;max-width:100%}'
             ':root[data-theme="dark"] .pr-pen{color:#93c5fd}@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .pr-pen{color:#93c5fd}}</style>\n'
             '<style>@font-face{font-family:Caveat;src:url(../../admin/content/reviews/fonts/caveat/caveat-400-700.woff2) format("woff2")}</style>\n')
    script = ('<script>(function(){var f={theme:"all",ch:"all",q:""};function go(){document.querySelectorAll("#pr-notes tbody tr").forEach(function(tr){'
              'tr.hidden=!((f.theme==="all"||tr.dataset.theme===f.theme)&&(f.ch==="all"||tr.dataset.ch===f.ch)&&(!f.q||tr.textContent.toLowerCase().indexOf(f.q)>=0))});'
              'var v=document.querySelectorAll("#pr-notes tbody tr:not([hidden])").length;document.getElementById("pr-shown").textContent=v}'
              'document.getElementById("pr-filters").addEventListener("click",function(ev){var b=ev.target.closest(".chip");if(!b)return;f[b.dataset.k]=b.dataset.v;'
              'document.querySelectorAll("#pr-filters .chip[data-k="+b.dataset.k+"]").forEach(function(x){x.setAttribute("aria-pressed",String(x===b))});go()});'
              'document.getElementById("pr-search").addEventListener("input",function(e){f.q=e.target.value.toLowerCase();go()})})();</script>')
    body = f"""<h1>RC2 on paper: every page, every note</h1>
<p class="lede">Dinis is reading the printed release candidate 2 with a pen. Each batch of photographs is a record and an article; this page puts them together: {len(pages)} pages, {len(notes)} notes, {len(used)} themes, mapped to the chapter each page is in. Every note has its own address (<code>#n52</code>), the photograph it is on, its words as written and what they mean.</p>
<h2 id="pages">The pages</h2>
<p class="small dim">Each card opens the photograph with the notes boxed, numbered and typed.</p>
<div class="pr-cards">{cards}</div>
<h2 id="map">Chapters by theme</h2>
<div class="tablewrap"><table><thead><tr><th>Chapter</th>{matrix_head}<th>Notes</th></tr></thead><tbody>{matrix}</tbody></table></div>
<ul class="small">{legend}</ul>
<h2 id="notes">Every note</h2>
<div class="gr-filters" id="pr-filters"><p><span class="dim">Theme</span> {chips_t}</p><p><span class="dim">Chapter</span> {chips_c}</p>
<p><input id="pr-search" type="search" placeholder="Search the notes" aria-label="Search the notes"> <span class="small dim"><span id="pr-shown">{len(notes)}</span> shown</span></p></div>
<div class="tablewrap"><table id="pr-notes"><thead><tr><th>#</th><th>Page</th><th>Theme</th><th>Written</th><th>What it means</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small dim">Source: <code>admin/content/reviews/paper/rc2-*.json</code>, drawn by <code>admin/build/paper_reviews.py</code>; the same notes as data in <a href="notes.json">notes.json</a>. The articles: {" &middot; ".join(f'<a href="{art(rv["article"], "in-short")}">part {rv["part"]}</a>' for rv in reviews)}.</p>
{script}"""
    page("reviews/paper/index.html", "RC2 on paper: every page, every note", body,
         f"Every page of Dinis's paper review of release candidate 2, and all {len(notes)} notes, mapped to chapter and theme.",
         crumbs=(("RC2 on paper", "reviews/paper/index.html"),), extra_head=style, wide=True)
    write("reviews/paper/notes.json", json.dumps({"what": "Every note of Dinis's paper review of release candidate 2, in order.",
                                                  "themes": {t: themes[t] for t in used}, "pages": pages, "notes": notes},
                                                 indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    print(build_paper_reviews({}))
