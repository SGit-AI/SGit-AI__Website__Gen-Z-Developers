#!/usr/bin/env python3
"""decks/: presentations about the book, each a PDF to post and present, with its slides and their notes. Rendered
from admin/content/decks/<slug>/ (deck.json and slides/<id>.htm); the PDF and the slide images are drawn by
admin/build/deck_pdf.py and committed, as the book's PDF is. Called by build.py with its helpers (page, esc).

The build refuses: a slide in the order with no file, a file whose <section> id is not its name, an image a slide names
that is not in the repository, and a deck whose PDF or slide images are missing or not the order's length (run
admin/build/deck_pdf.py).
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "admin/content/decks"


def check(slug, deck):
    E = []
    d = SRC / slug
    for sid in deck["order"]:
        f = d / "slides" / f"{sid}.htm"
        if not f.exists():
            E.append(f"decks/{slug}: slide {sid} is in the order but has no file"); continue
        t = f.read_text(encoding="utf-8")
        ids = re.findall(r"<section\s+id=\"([^\"]+)\"", t)
        if ids != [sid]:
            E.append(f"decks/{slug}/slides/{sid}.htm: holds sections {ids}, not one section #{sid}")
        for src in re.findall(r"<img[^>]*\ssrc=\"([^\"]+)\"", t):
            if not (ROOT / src).exists():
                E.append(f"decks/{slug}/slides/{sid}.htm: image {src} is not in the repository")
    pdf = ROOT / "decks" / f"{slug}.pdf"
    if not pdf.exists():
        E.append(f"decks/{slug}.pdf is missing: run admin/build/deck_pdf.py")
    else:
        pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
        if pages != len(deck["order"]):
            E.append(f"decks/{slug}.pdf has {pages} pages, the order has {len(deck['order'])}: run admin/build/deck_pdf.py")
    shots = sorted((ROOT / "decks" / slug).glob("slide-*.png"))
    if len(shots) != len(deck["order"]):
        E.append(f"decks/{slug}/: {len(shots)} slide images for {len(deck['order'])} slides: run admin/build/deck_pdf.py")
    return E


def notes(t):
    m = re.search(r"<aside>(.*?)</aside>", t, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def build_decks(ctx):
    page, esc = ctx["page"], ctx["esc"]
    decks = [(p.name, json.loads((p / "deck.json").read_text(encoding="utf-8"))) for p in sorted(SRC.iterdir()) if (p / "deck.json").exists()]
    E = [e for slug, deck in decks for e in check(slug, deck)]
    if E:
        raise SystemExit("build: the decks refuse:\n  - " + "\n  - ".join(E))
    parts = []
    for slug, deck in decks:
        pdf = ROOT / "decks" / f"{slug}.pdf"
        cells = ""
        for i, sid in enumerate(deck["order"], 1):
            t = (SRC / slug / "slides" / f"{sid}.htm").read_text(encoding="utf-8")
            h = re.search(r"<h[12][^>]*>(.*?)</h[12]>", t, re.S)
            title = html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip() if h else sid
            cells += (f'<figure class="dk-slide" id="{slug}-{i:02d}"><a href="{slug}/slide-{i:02d}.png"><img src="{slug}/slide-{i:02d}.png" alt="Slide {i}: {esc(title)}" loading="lazy" width="960" height="540"></a>'
                      f'<figcaption><b>{i}. {esc(title)}</b><span class="small dim">{esc(notes(t))}</span></figcaption></figure>')
        parts.append(f"""<section class="dk-deck" id="{slug}">
<h2>{esc(deck['title'])}</h2>
<p>{esc(deck['what'])}</p>
<p class="ctas"><a class="btn primary" href="{slug}.pdf" download>Download the PDF</a> <span class="small dim">{len(deck['order'])} slides, 16:9, {pdf.stat().st_size / 1048576:.1f} MB · made {esc(deck['date'])} · release candidate {esc(deck['candidate'].split('-rc')[-1])}</span></p>
<div class="dk-grid">{cells}</div>
</section>""")
    body = f"""<h1>Presentations</h1>
<p class="lede">The book, as slides to post and to present: horizontal PDFs, every slide with its speaker notes. Drawn from data like the rest of this site, so a slide is corrected by changing a line and rendering again.</p>
{''.join(parts)}
<h2 id="how">How a deck is made</h2>
<ul>
<li><b>The data.</b> <code>admin/content/decks/&lt;slug&gt;/deck.json</code> (the title, the order, the fonts) and one <code>slides/&lt;id&gt;.htm</code> per slide (a fragment, not a page of this site): one <code>&lt;section&gt;</code> on a 1920 by 1080 canvas, every style inline, the speaker notes in its <code>&lt;aside&gt;</code>. Images are named by their path here: the covers, the infographics, a storyboard panel.</li>
<li><b>The drawing.</b> <code>python3 admin/build/deck_pdf.py</code>, after the site build, renders the PDF and the slide images with Chromium; both are committed, as the book's PDF is. The build checks every slide, image and page.</li>
<li><b>The same files</b> are in the subset the Slides artifact type reads, so a deck can be published there for comments and presenting, and back.</li>
</ul>"""
    page("decks/index.html", "Presentations", body, "Presentations about Generation ZX Founders: horizontal PDFs to post and present, every slide with its speaker notes.",
         crumbs=(("Presentations", "decks/index.html"),), extra_head='<link rel="stylesheet" href="../assets/decks.css">\n', wide=True)
