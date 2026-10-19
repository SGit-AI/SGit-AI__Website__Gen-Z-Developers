#!/usr/bin/env python3
"""Export drawn infographics as PNG, for a slide, a LinkedIn post or a review by eye.

    python3 admin/build/infographic_png.py [id ...] [--out dir] [--scale 1]

It opens each built SVG (infographics/svg/<id>.svg, run build.py first) in headless Chromium and screenshots it at its
own size as <out>/<id>.png (default out: a temporary folder, printed at the end). With no id, every drawn infographic.
The PNGs are not part of the site: the SVG is the infographic, and the images are copies of it, made on demand. Needs
Python's playwright; it uses STORYBOARD_CHROMIUM if set, else the Chromium preinstalled at /opt/pw-browsers in the
cloud sessions, else playwright's own."""
import glob
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    argv = sys.argv[1:]
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else Path(tempfile.mkdtemp(prefix="infographics-"))
    scale = float(argv[argv.index("--scale") + 1]) if "--scale" in argv else 1.0
    ids = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] not in ("--out", "--scale"))]
    svgs = [ROOT / "infographics/svg" / f"{i}.svg" for i in ids] if ids else sorted((ROOT / "infographics/svg").glob("*.svg"))
    missing = [s for s in svgs if not s.exists()]
    if missing or not svgs:
        sys.exit(f"infographic_png: no SVG at {', '.join(map(str, missing)) or 'infographics/svg/'}; run admin/build/build.py first")
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        exe = os.environ.get("STORYBOARD_CHROMIUM") or next(iter(sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))), None)
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        for svg in svgs:
            w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', svg.read_text(encoding="utf-8")).groups())
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            page.set_content('<html><body style="margin:0">' + svg.read_text(encoding="utf-8") + '</body></html>')
            page.wait_for_timeout(300)
            page.screenshot(path=str(out / f"{svg.stem}.png"), clip={"x": 0, "y": 0, "width": w, "height": h})
            page.close()
        browser.close()
    print(f"infographic_png: {len(svgs)} PNG(s) in {out}")


if __name__ == "__main__":
    main()
