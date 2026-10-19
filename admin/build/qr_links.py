"""The pages behind the book's QR codes: q/<id>/index.html for every id in admin/content/qr/links.json.

Each page says what the code points to and sends the reader on to it. The code itself is drawn once by qr_codes.py
into q/<id>/qr.svg and committed; the build refuses an id whose code has not been drawn, so a printed code always has
a page behind it. Called by build.py with its page() and esc().
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build_qr_links(ctx):
    page, esc = ctx["page"], ctx["esc"]
    doc = json.loads((ROOT / "admin/content/qr/links.json").read_text(encoding="utf-8"))
    rows = []
    for qid, ln in doc["links"].items():
        if not (ROOT / "q" / qid / "qr.svg").exists():
            raise SystemExit(f"build: QR code {qid} has no q/{qid}/qr.svg: run admin/build/qr_codes.py")
        to = ln["to"] if ln["to"].startswith("http") else "../../" + ln["to"]
        rel = f"q/{qid}/index.html"
        body = (f'<h1>{esc(ln["label"])}</h1><p class="lede">You scanned a code in <i>Generation ZX Founders (GenAI Edition)</i> '
                f'({esc(ln["for"])}). It goes to: <a href="{esc(to)}">{esc(ln["label"])}</a>.</p>'
                f'<p><img src="qr.svg" alt="The QR code for this page" width="120" height="120"></p>'
                f'<p class="small dim">Every code in the book prints a short address on this site, so it never goes out of date: '
                f'when the target moves, this page changes, and the paper does not. <a href="../index.html">All the codes</a>.</p>')
        page(rel, ln["label"], body, f"Where the book's code {qid} points: {ln['label']}.",
             crumbs=(("QR codes", "q/index.html"), (ln["label"], rel)),
             extra_head=f'<meta http-equiv="refresh" content="2; url={esc(to)}">\n')
        rows.append(f'<tr><td><img src="{qid}/qr.svg" alt="" width="56" height="56"></td><td><code>/q/{esc(qid)}/</code></td>'
                    f'<td><a href="{esc(to if to.startswith("http") else to[3:])}">{esc(ln["label"])}</a></td><td>{esc(ln["kind"])}</td><td class="small">{esc(ln["for"])}</td></tr>')
    body = (f'<h1>QR codes</h1><p class="lede">{esc(doc["what"])}</p>'
            f'<table><thead><tr><th></th><th>Address</th><th>Goes to</th><th>Kind</th><th>Where in the book</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')
    page("q/index.html", "QR codes", body, "Every QR code in the book, the short address it prints and where it goes.", crumbs=(("QR codes", "q/index.html"),))
    return list(doc["links"])
