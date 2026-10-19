#!/usr/bin/env python3
"""Export a storyboard's panels as PNG slides, for an iPad's photos, a LinkedIn carousel or a review by eye.

    python3 admin/build/storyboard_png.py the-2018-book [out_dir] [--width 1600] [--grid [--cols 4] [--text]]

It opens the built deck (storyboards/<slug>.html, run build.py first) in headless Chromium, turns the animation off,
hides the site's navigation, and screenshots each panel as out_dir/<slug>__NN.png (default out_dir: a temporary folder,
printed at the end). With --grid it writes one image instead, out_dir/<slug>__grid.png: every panel on one sheet,
--cols per row (default 4), with each panel's text under it if --text is given. The
PNGs are not part of the site: the deck is the storyboard, and the images are copies of it, made on demand. Needs
Python's playwright; it uses STORYBOARD_CHROMIUM if set, else the Chromium preinstalled at /opt/pw-browsers in the cloud sessions, else playwright's own."""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] not in ("--width", "--cols")]
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
    grid = "--grid" in sys.argv
    cols = int(sys.argv[sys.argv.index("--cols") + 1]) if "--cols" in sys.argv else 4
    # the viewer reads its settings from the browser: still panels, the view asked for; nothing here is kept
    prefs = json.dumps({"anim": False, "view": "grid" if grid else "deck", "cols": cols, "text": "--text" in sys.argv})
    with sync_playwright() as p:
        import glob, os
        exe = os.environ.get("STORYBOARD_CHROMIUM") or next(iter(sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))), None)
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": int(width * 0.625)})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.add_init_script(f"try {{ localStorage.setItem('genz.storyboards.v1', {json.dumps(prefs)}); }} catch (e) {{}}")
        page.goto(deck.as_uri() + ("?view=grid" if grid else "?view=deck"))
        page.add_style_tag(content="nav.site{display:none!important}.sb-panel *{animation:none!important}")
        page.wait_for_timeout(1500)
        if grid:
            # draw every panel (the grid draws lazily, as panels near the screen)
            page.evaluate("document.querySelectorAll('.sb-cell').forEach(c => c._draw && c._draw())")
            page.wait_for_timeout(500)
            page.query_selector(".sb-grid").screenshot(path=str(out / f"{slug}__grid.png"))
            n = 1
        else:
            svgs = page.query_selector_all(".sb-deck .sb-slide svg")
            for i, svg in enumerate(svgs, 1):
                svg.screenshot(path=str(out / f"{slug}__{i:02d}.png"))
            n = len(svgs)
        browser.close()
    if errors:
        sys.exit(f"storyboard_png: the page reported errors: {errors[:3]}")
    print(f"storyboard_png: {'a grid of every panel' if grid else f'{n} panels'} written to {out}")


if __name__ == "__main__":
    main()
