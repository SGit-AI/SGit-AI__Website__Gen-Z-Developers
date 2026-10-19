#!/usr/bin/env python3
"""Draw each QR code once, into q/<id>/qr.svg, from admin/content/qr/links.json. Run by hand when an id is added:

    pip install segno && python3 admin/build/qr_codes.py

A code encodes only the short address (base + id + '/'), never the target, so it never needs redrawing when a target
moves; the build (qr_links.py) writes the page behind it and refuses an id with no drawn code. Error correction M,
a two-module quiet zone, no fixed size: the SVG scales to whatever the page prints it at (about 15 mm is enough).
"""
import json
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parents[2]
doc = json.loads((ROOT / "admin/content/qr/links.json").read_text(encoding="utf-8"))
for qid in doc["links"]:
    out = ROOT / "q" / qid
    out.mkdir(parents=True, exist_ok=True)
    qr = segno.make(doc["base"] + qid + "/", error="m", micro=False)
    qr.save(str(out / "qr.svg"), scale=4, border=2, dark="#111827", xmldecl=False, svgns=True, title=f"QR code for {doc['base']}{qid}/")
    print(qid, qr.version, qr.designator)
