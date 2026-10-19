#!/usr/bin/env python3
"""Fetch the covers' fonts once, with their licences, into admin/content/covers/fonts/. Run again only to change them.

    python3 admin/build/cover_fonts.py

Every family is from Google Fonts and under the SIL Open Font License 1.1, which allows embedding in a book cover and
redistribution with the licence beside the font; the licence is fetched from the google/fonts repository and saved next
to each family. Only the latin subset is kept (the covers are in English and Portuguese names fit in it). The covers
embed these files in the SVG (so it renders anywhere) and Chromium embeds them in the print PDF.
Writes fonts/<family-slug>/<file>.woff2, fonts/<family-slug>/OFL.txt and fonts/fonts.json (family, style, weights, file).
"""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "admin/content/covers/fonts"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
FAMILIES = {  # Google Fonts family -> (css2 axis spec, google/fonts repo folder)
    "Archivo Black": ("", "archivoblack"),
    "Big Shoulders Display": (":wght@500..900", "bigshouldersdisplay"),
    "Big Shoulders Stencil Display": (":wght@700..900", "bigshouldersstencildisplay"),
    "Space Grotesk": (":wght@400..700", "spacegrotesk"),
    "Space Mono": (":ital,wght@0,400;0,700", "spacemono"),
    "Fraunces": (":ital,opsz,wght@0,9..144,300..900;1,9..144,300..900", "fraunces"),
    "IBM Plex Sans": (":ital,wght@0,400;0,600;1,400", None),  # Plex is OFL in its own repository folder name
}
PLEX_LICENCE = "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexsans/OFL.txt"


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


def main():
    manifest = []
    for family, (axes, repo) in FAMILIES.items():
        slug = re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        css = get("https://fonts.googleapis.com/css2?family=" + family.replace(" ", "+") + axes + "&display=swap")
        seen = {}
        for block in re.findall(r"/\* latin \*/\s*@font-face\s*{(.*?)}", css, re.S):
            style = re.search(r"font-style:\s*(\w+)", block).group(1)
            weight = re.search(r"font-weight:\s*([\d ]+);", block).group(1).strip()
            url = re.search(r"url\((.*?)\)", block).group(1)
            key = (style, url)
            if key in seen:
                # one variable file serves several weights: record the range it covers
                m = next(f for f in manifest if f["file"].endswith(seen[key]))
                ws = [int(w) for w in (m["weight"] + " " + weight).split()]
                m["weight"] = f"{min(ws)} {max(ws)}"
                continue
            name = f"{slug}-{style}-{weight.replace(' ', '-')}.woff2"
            (d / name).write_bytes(get(url, binary=True))
            seen[key] = name
            manifest.append({"family": family, "style": style, "weight": weight, "file": f"{slug}/{name}", "source": url})
        lic = get(PLEX_LICENCE if repo is None else f"https://raw.githubusercontent.com/google/fonts/main/ofl/{repo}/OFL.txt")
        (d / "OFL.txt").write_text(lic, encoding="utf-8")
    (OUT / "fonts.json").write_text(json.dumps({"what": "The covers' fonts: Google Fonts, SIL Open Font License 1.1, latin subset; fetched by admin/build/cover_fonts.py.", "fonts": manifest}, indent=1) + "\n", encoding="utf-8")
    print(f"cover_fonts: {len(manifest)} font files in {OUT}")


if __name__ == "__main__":
    main()
