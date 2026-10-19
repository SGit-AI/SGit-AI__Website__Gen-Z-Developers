#!/usr/bin/env python3
"""covers/: the cover proposals and the cover system, rendered from admin/content/covers/covers.json and the files
admin/build/covers.py drew into covers/<design>/. Called by build.py with its helpers (page, esc).

The build refuses: a word on the covers that is not in its source (the title and edition in decision 014, the cover
line and the back in article 17, the eight 2018 lines in the first edition's record), and a design whose files are
missing (run admin/build/covers.py).
"""
import json
import re
from pathlib import Path

from readers_pages import quote_in

ROOT = Path(__file__).resolve().parents[2]
FILES = ("front.svg", "kindle.svg", "wrap.svg", "wrap-guides.svg", "kindle.jpg", "leanpub.jpg", "wrap.pdf", "preview.png", "wrap-guides.png")


def check(doc, first_edition_lines):
    E = []
    b = doc["book"]
    d014 = next((ROOT / "admin/content/decisions").glob("014__*.md")).read_text(encoding="utf-8")
    if f'{b["title"]} ({b["edition"]})' not in d014:
        E.append(f"covers.json: the title and edition are not decision 014's: {b['title']} ({b['edition']})")
    a17 = (ROOT / "admin/content/articles/17__version-2-on-leanpub.md").read_text(encoding="utf-8")
    for s in [b["cover_line"], b["back_close"]] + b["back"]:
        if not quote_in(s, a17):
            E.append(f"covers.json: not word for word in article 17: {s[:70]}")
    if [l.lower() for l in b["cover_lines_2018"]] != [l.lower() for l in first_edition_lines]:
        E.append("covers.json: the eight 2018 lines are not the first edition's cover lines")
    for d in doc["designs"]:
        for f in FILES:
            if not (ROOT / "covers" / d["id"] / f).exists():
                E.append(f"covers/{d['id']}/{f} is missing: run admin/build/covers.py")
    return E


def build_covers(ctx):
    page, esc = ctx["page"], ctx["esc"]
    doc = json.loads((ROOT / "admin/content/covers/covers.json").read_text(encoding="utf-8"))
    E = check(doc, ctx["first_edition_lines"])
    if E:
        raise SystemExit("build: the covers refuse:\n  - " + "\n  - ".join(E))
    b, f, s = doc["book"], doc["formats"], doc["system"]
    pb = f["paperback"]
    spine = pb["pages"] * pb["spine_in_per_page"][pb["paper"]]
    wrap_w = 2 * pb["trim_in"][0] + spine + 2 * pb["bleed_in"]
    wrap_h = pb["trim_in"][1] + 2 * pb["bleed_in"]
    kb = lambda p: f'{(ROOT / p).stat().st_size / 1024:,.0f} KB'
    cards = ""
    for i, d in enumerate(doc["designs"], 1):
        base = f"{d['id']}/"
        dl = " ".join(f'<a class="btn" href="{base}{fn}">{lab}</a>' for fn, lab in (
            ("front.svg", "Front, SVG"), ("kindle.jpg", "Kindle JPG"), ("leanpub.jpg", "Leanpub JPG"), ("wrap.pdf", "Paperback PDF"), ("wrap.svg", "Wrap, SVG")))
        fonts = ", ".join(f"{v} ({k})" for k, v in d["font"].items())
        cards += f"""<section class="cv-design" id="{d['id']}">
<h2>{i}. {esc(d['name'])}</h2>
<div class="cv-row">
<a class="cv-front" href="{base}front.svg"><img src="{base}preview.png" alt="The front cover, design {esc(d['name'])}" width="600" height="900"></a>
<div class="cv-text">
<p>{esc(d['idea'])}</p>
<p class="small"><b>Type:</b> {esc(fonts)}.</p>
<p class="small cv-risk"><b>Risk.</b> {esc(d['risk'])}</p>
<p class="ctas">{dl}</p>
<p class="small dim">Kindle {f['kindle']['px'][0]} by {f['kindle']['px'][1]} ({kb('covers/' + base + 'kindle.jpg')}); Leanpub {f['leanpub']['px'][0]} by {f['leanpub']['px'][1]} ({kb('covers/' + base + 'leanpub.jpg')}); paperback {wrap_w:.3f} by {wrap_h:.3f} inches ({kb('covers/' + base + 'wrap.pdf')}, fonts embedded); the SVGs carry their fonts, so they open and resize anywhere.</p>
<a class="cv-kindle" href="{base}kindle.jpg"><img src="{base}kindle.jpg" alt="The Kindle cover, design {esc(d['name'])}" loading="lazy" width="160" height="256"><span class="small dim">Kindle, laid out again for its taller shape</span></a>
</div></div>
<figure class="cv-wrap"><a href="{base}wrap-guides.svg"><img src="{base}wrap-guides.png" alt="The paperback's full wrap, back, spine and front, with the print guides drawn" loading="lazy"></a>
<figcaption class="small dim">The paperback, back, spine and front, with the guides: magenta dashed is the trim, the magenta lines the spine's folds, cyan dashed the safe area, the white box the barcode area Amazon prints into. The PDF and <code>wrap.svg</code> are the same without them.</figcaption></figure>
</section>"""
    sw = "".join(f'<span class="cv-sw" style="background:{v}"></span><code>{esc(k)} {v}</code> ' for k, v in s["palette"].items())
    rules = "".join(f"<li>{esc(r)}</li>" for r in s["rules"])
    hier = "".join(f"<li>{esc(h)}</li>" for h in s["hierarchy"])
    back = "".join(f"<p>{esc(p)}</p>" for p in b["back"]) + f"<p><i>{esc(b['back_close'])}</i></p>"
    body = f"""<h1>Covers</h1>
<p class="lede">Three cover designs for <i>{esc(b['title'])} ({esc(b['edition'])})</i>, ready for Amazon and Leanpub, each drawn from data by code into SVG, so any of them can be resized, recoloured or reworded and drawn again. Proposals: the cover waits on Dinis (<a href="../decisions/index.html#the-cover-waits">decision 004</a>), and these are the options he asked for on 19 October 2026.</p>
<p class="stats"><span class="stat"><b>3</b><span>designs</span></span><span class="stat"><b>3</b><span>formats each</span></span><span class="stat"><b>{spine:.3f} in</b><span>spine, {pb['pages']} pages</span></span><span class="stat"><b>{wrap_w:.3f} &times; {wrap_h:.3f}</b><span>inches, the wrap</span></span></p>
<figure class="cv-three">{''.join(f'<a href="#{d["id"]}"><img src="{d["id"]}/preview.png" alt="{esc(d["name"])}" width="600" height="900"><span>{esc(d["name"])}</span></a>' for d in doc['designs'])}</figure>
{cards}
<h2 id="system">The system</h2>
<p>What every design shares, so that the choice between them is a choice of look, not of what the cover says or whether it prints.</p>
<div class="twocol"><div>
<h3>The words</h3>
<ul>
<li><b>Title:</b> {esc(b['title'])} ({esc(b['edition'])}), as Dinis decided it (decision 014).</li>
<li><b>Cover line:</b> {esc(b['cover_line'])}: the subtitle proposed for Leanpub in <a href="../articles/version-2-on-leanpub.html">article 17</a>; decision 014 says the two generations are said in full on the cover line.</li>
<li><b>Author:</b> {esc(b['author'])}. <b>Licence:</b> {esc(b['licence'])}. <b>Where it is built:</b> {esc(b['site'])}.</li>
</ul>
<h3>The hierarchy</h3><ol>{hier}</ol>
<h3>The back</h3><div class="cv-back small">{back}</div>
<p class="small dim">Dinis's words, from the book's description in article 17; the build checks each one is there, word for word.</p>
</div><div>
<h3>The formats</h3>
<div class="tablewrap"><table><thead><tr><th>For</th><th>What</th><th>Size</th></tr></thead><tbody>
<tr><td>KDP paperback</td><td>{esc(pb['what'])}</td><td>{pb['trim_in'][0]} &times; {pb['trim_in'][1]} in trim, {pb['bleed_in']} in bleed, spine {pb['spine_in_per_page'][pb['paper']]} in a page on {pb['paper']} paper: {wrap_w:.3f} &times; {wrap_h:.3f} in</td></tr>
<tr><td>Kindle</td><td>{esc(f['kindle']['what'])}</td><td>{f['kindle']['px'][0]} &times; {f['kindle']['px'][1]} px</td></tr>
<tr><td>Leanpub</td><td>{esc(f['leanpub']['what'])}</td><td>{f['leanpub']['px'][0]} &times; {f['leanpub']['px'][1]} px</td></tr>
</tbody></table></div>
<p class="small">{esc(pb['pages_note'])} {esc(f['check'])}</p>
<h3>The palette</h3><p class="small">{sw}</p>
<p class="small">The 2018 cover's colours, and the four-square mark that the site's infographics carry: {esc(s['mark'])}.</p>
<h3>The rules</h3><ul class="small">{rules}</ul>
</div></div>
<h2 id="change">How to change a cover</h2>
<ol>
<li>The words, the formats, the page count and the palette are in <code>admin/content/covers/covers.json</code>; the layouts are functions of width and height in <code>admin/build/covers.py</code>, one per design.</li>
<li>Run <code>python3 admin/build/covers.py</code>: every SVG, the Kindle and Leanpub images and the print PDF are drawn again, with the text fitted from the fonts' own metrics. Then the site build, which checks the words.</li>
<li>When the interior is final, set its page count and paper and run it again: the spine and the wrap follow. Then compare with KDP's cover calculator before upload.</li>
<li>The fonts are in <code>admin/content/covers/fonts/</code>, each with its SIL Open Font License; <code>admin/build/cover_fonts.py</code> fetched them from Google Fonts.</li>
</ol>"""
    page("covers/index.html", "Covers", body, "Three cover designs for Generation ZX Developers, in SVG, with the Kindle, Leanpub and KDP paperback files, and the cover system.",
         crumbs=(("Covers", "covers/index.html"),), extra_head='<link rel="stylesheet" href="../assets/covers.css">\n', wide=True)
