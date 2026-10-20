#!/usr/bin/env python3
"""Render a deck to its PDF and its slide images: admin/content/decks/<slug>/ into decks/<slug>.pdf and
decks/<slug>/slide-NN.png.

    python3 admin/build/deck_pdf.py [slug ...]        # every deck when none is named

A deck is data, like a storyboard or an infographic: deck.json (the title, the order, the fonts) and one
slides/<id>.htm per slide (.htm, not .html: a fragment, not a page of this site, so the gate does not take it for one),
a single <section> on a 1920 by 1080 canvas with every style inline, in the subset the
Slides artifact type uses, so the same files can be published there. Images are named by their path in this
repository (covers/zx/leanpub.jpg, infographics/svg/<id>.svg) and resolve against its root. Speaker notes are the
slide's <aside>; they are not drawn, and the site's page shows them under each slide.

Run after build.py (the covers and the infographics it draws are on the slides); the build then writes decks/index.html
from deck.json and these files. Needs playwright and Chromium (the one at /opt/pw-browsers in the cloud sessions).
"""
import glob
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "admin/content/decks"
OUT = ROOT / "decks"

# What the Slides runtime does before it draws a slide, and what a browser does not: no default margins, a fixed
# canvas per slide, notes kept out of the picture.
RESET = """@page{size:1920px 1080px;margin:0}
html,body{margin:0;padding:0;background:#121417}
section{position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden;page-break-after:always;break-after:page}
section *{margin:0;box-sizing:border-box}
section ul,section ol{padding-left:1.2em}
aside{display:none}"""


def html_of(deck, d):
    slides = "\n".join((d / "slides" / f"{sid}.htm").read_text(encoding="utf-8") for sid in deck["order"])
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><base href="{ROOT.as_uri()}/">'
            f'<title>{deck["title"]}</title><link rel="stylesheet" href="{deck["fonts"]}"><style>{RESET}</style></head>'
            f"<body>{slides}</body></html>")


def render(slug):
    from playwright.sync_api import sync_playwright
    d = SRC / slug
    deck = json.loads((d / "deck.json").read_text(encoding="utf-8"))
    out = OUT / slug
    out.mkdir(parents=True, exist_ok=True)
    tmp = out / ".deck.html"  # a file, so the <base> resolves images from the repository; removed after
    tmp.write_text(html_of(deck, d), encoding="utf-8")
    exe = os.environ.get("STORYBOARD_CHROMIUM") or next(iter(sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))), None)
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            pg = br.new_page(viewport={"width": 1920, "height": 1080})
            pg.goto(tmp.as_uri())
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            for i, sid in enumerate(deck["order"], 1):
                pg.locator(f"section#{sid}").screenshot(path=str(out / f"slide-{i:02d}.png"))
            pg.pdf(path=str(OUT / f"{slug}.pdf"), width="1920px", height="1080px", print_background=True,
                   margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            br.close()
    finally:
        tmp.unlink(missing_ok=True)
    # the slide images are kept small for the page; the PDF is the deck
    from PIL import Image
    for f in sorted(out.glob("slide-*.png")):
        im = Image.open(f)
        im.thumbnail((960, 540))
        im.save(f, optimize=True)
    print(f"deck_pdf: {slug}: {len(deck['order'])} slides, {OUT / (slug + '.pdf')}")


if __name__ == "__main__":
    for slug in (sys.argv[1:] or sorted(p.name for p in SRC.iterdir() if (p / "deck.json").exists())):
        render(slug)
