"""Who the book is for, drawn: the reader card and the partnership, from admin/content/positioning/reader.json.

Called by build.py; writes positioning/reader-card.svg and positioning/partnership.svg, standalone SVGs with their fonts
embedded (the drawing helpers are the paper reviews', so the two read as one hand). A change to who the book is for is
a change to the data, and both drawings follow.
"""
import json
from pathlib import Path

from paper_reviews import HAND, PEN, Pen, badge, page_frame, svg, text, wrap

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "admin/content/positioning/reader.json"
OUT = ROOT / "positioning"
Z, X, MID = "#7c3aed", "#b45309", "#1d3a8a"


def reader_card(d):
    r = d["reader"]
    pen = Pen(7)
    b = [text(500, 96, "WHO THIS BOOK IS FOR", 18, fill="#6b7280", anchor="middle", extra='letter-spacing="3"'),
         text(500, 160, r["name"], 52, weight="bold", anchor="middle"),
         text(500, 212, r["line"], 32, font=HAND, fill=PEN, anchor="middle")]
    b.append(pen.box(90, 250, 820, 260))
    b.append(text(120, 300, "Already", 24, weight="bold"))
    for i, a in enumerate(r["already"]):
        b.append(f'<circle cx="132" cy="{340 + i * 42 - 7}" r="7" fill="{MID}"/>')
        b.append(text(152, 340 + i * 42, a, 21))
    b.append(text(500, 560, r["any_generation"], 22, fill="#374151", anchor="middle"))
    for k, (col, lab) in enumerate(((Z, "Generation Z"), (X, "Generation X"))):
        x = 150 + k * 400
        b.append(f'<circle cx="{x + 150}" cy="640" r="52" fill="{col}" fill-opacity="0.15" stroke="{col}" stroke-width="4"/>')
        b.append(text(x + 150, 648, lab.split()[1], 34, weight="bold", fill=col, anchor="middle"))
        b.append(text(x + 150, 724, lab, 20, fill=col, anchor="middle"))
    b.append(pen.line(355, 640, 645, 640, MID, 4))
    b.append(text(500, 626, "ZX", 30, weight="bold", fill=MID, anchor="middle"))
    b.append(f'<rect x="90" y="780" width="400" height="230" rx="16" fill="#ecfdf5" stroke="#16a34a" stroke-width="3"/>')
    b.append(text(115, 825, "Wants from this book", 22, weight="bold", fill="#166534"))
    for i, w in enumerate(r["wants"]):
        b.append(text(115, 866 + i * 50, wrap(w, 34), 18, fill="#166534", lh=1.2))
    b.append(f'<rect x="510" y="780" width="400" height="230" rx="16" fill="#fef2f2" stroke="#dc2626" stroke-width="3"/>')
    b.append(text(535, 825, "Does not need", 22, weight="bold", fill="#991b1b"))
    b.append(text(535, 880, r["does_not_need"], 26, font=HAND, fill="#991b1b"))
    b.append(text(535, 940, ["so the book starts with the path,", "not with the pitch"], 18, fill="#991b1b", lh=1.3))
    b.append(f'<rect x="90" y="1040" width="820" height="90" rx="16" fill="#eff6ff" stroke="#2563eb" stroke-width="3"/>')
    b.append(text(500, 1095, r["turn"], 21, fill="#1e3a8a", anchor="middle"))
    b.append(f'<rect x="90" y="1160" width="820" height="90" rx="16" fill="#fff7ed" stroke="#d97706" stroke-width="3"/>')
    b.append(text(500, 1215, "The measure: " + r["measure"], 21, fill="#9a3412", anchor="middle"))
    b.append(text(500, 1320, d["title"], 26, weight="bold", fill="#374151", anchor="middle"))
    return svg(1000, 1414, "".join(page_frame(b)), "The reader card: who Generation ZX Founders is for")


def partnership(d):
    p = d["partnership"]
    W, H = 1200, 800
    pen = Pen(9)
    b = [text(600, 70, "Either could have built it", 36, weight="bold", anchor="middle"),
         text(600, 108, "the Generation Z founder and the Generation X founder, and what goes each way", 18, fill="#6b7280", anchor="middle")]
    nodes = {"z": (230, 400, Z), "x": (970, 400, X)}
    for k, (cx, cy, col) in nodes.items():
        side = p[k]
        b.append(f'<circle cx="{cx}" cy="{cy}" r="120" fill="{col}" fill-opacity="0.10" stroke="{col}" stroke-width="5"/>')
        b.append(text(cx, cy - 30, side["label"].replace(" founder", ""), 26, weight="bold", fill=col, anchor="middle"))
        b.append(text(cx, cy, "founder", 20, fill=col, anchor="middle"))
        b.append(text(cx, cy + 50, "lacks: " + side["lacks"], 17, fill="#6b7280", anchor="middle"))
        for i, h in enumerate(side["has"]):
            b.append(text(cx, 580 + i * 30, "has " + h, 19, fill=col, anchor="middle"))
    ys = [270, 340, 460, 530]
    for i, (a, bb, lab) in enumerate(p["edges"]):
        y = ys[i]
        x1, x2 = (360, 840) if a == "z" else (840, 360)
        col = nodes[a][2]
        b.append(pen.arrow(x1, y, x2, y, col, 3.5))
        b.append(text(600, y - 12, lab, 19, fill=col, anchor="middle"))
    b.append(text(600, 730, p["line"], 30, font=HAND, fill=PEN, anchor="middle"))
    return svg(W, H, "".join(page_frame(b, w=W, h=H)), "The partnership: what the Generation Z founder and the Generation X founder bring each other")


def build_positioning(ctx):
    d = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    (OUT / "reader-card.svg").write_text(reader_card(d), encoding="utf-8")
    (OUT / "partnership.svg").write_text(partnership(d), encoding="utf-8")
    return ["reader-card", "partnership"]


if __name__ == "__main__":
    print(build_positioning({}))
