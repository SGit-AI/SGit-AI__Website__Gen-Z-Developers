#!/usr/bin/env python3
"""Export a storyboard's panels as PNG slides, for an iPad's photos, a LinkedIn carousel or a review by eye.

    python3 admin/build/storyboard_png.py the-2018-book [out_dir] [--width 1600]

It opens the built deck (storyboards/<slug>.html, run build.py first) in headless Chromium, turns the animation off,
and screenshots each panel as out_dir/<slug>__NN.png (default out_dir: a temporary folder, printed at the end). The
PNGs are not part of the site: the deck is the storyboard, and the images are copies of it, made on demand. Needs
Python's playwright; it uses STORYBOARD_CHROMIUM if set, else the Chromium preinstalled at /opt/pw-browsers in the cloud sessions, else playwright's own."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    slug = args[0]
    out = Path(args[1]) if len(args) > 1 else Path(tempfile.mkdtemp(prefix=f"storyboard-{slug}-"))
    width = int(sys.argv[sys.argv.index("--width") + 1]) if "--width" in sys.argv else 1600
    deck = ROOT / "storyboards" / f"{slug}.html"
    if not deck.exists():
        sys.exit(f"storyboard_png: {deck} does not exist; run admin/build/build.py first")
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        import glob, os
        exe = os.environ.get("STORYBOARD_CHROMIUM") or next(iter(sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))), None)
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": int(width * 0.625)})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(deck.as_uri())
        page.wait_for_timeout(1500)
        page.add_style_tag(content=".sb-slide *{animation:none!important}")
        svgs = page.query_selector_all(".sb-slide svg")
        for i, svg in enumerate(svgs, 1):
            svg.screenshot(path=str(out / f"{slug}__{i:02d}.png"))
        browser.close()
    if errors:
        sys.exit(f"storyboard_png: the page reported errors: {errors[:3]}")
    print(f"storyboard_png: {len(svgs)} panels written to {out}")


if __name__ == "__main__":
    main()
