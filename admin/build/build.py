#!/usr/bin/env python3
"""gen-z-developers.sgit.ai — the whole site, generated from the files that are the source of truth.

    python3 admin/build/gen_map.py      # the chapter-to-article map (admin/content/map.json)
    python3 admin/build/build.py        # everything else
    node admin/build/validate.js        # the gate

Sources (never edited by this script, except the two bootstraps noted):
  v1/content/**/*.md                     the 2018 book, as released. FROZEN.
  v1/images/                             its figures
  admin/content/book/versions.json       the book's official versions; text_sha256 is filled in ONCE by this build
  admin/content/map.json                 the chapter-to-article map (gen_map.py)
  admin/content/briefs/*.md              the newsroom articles and notes that brief this site, captured verbatim
  admin/content/vault.json               the public working vault's read key and address (the write key is never here)
  admin/content/versions.json            the site's release history, narrated
  team/<role>/role.md, issues/, briefs/  the roles
  admin/build/version.txt                the site's version

Outputs (every .html on the site, plus):
  v1/book/**                             one page per chapter, the table of contents, the whole book on one page
  v1/book/manifest.json                  the hash of every chapter's markdown and of the page it rendered (validate.js checks)
  v1/versions/v1.0.0.md                  the book frozen as one markdown file, written once by page_versions.freeze
  v1/versions/index.html                 the versions page: the table and the block-by-block deltas (page_versions.py)
  llms.txt, sitemap.xml, robots.txt, 404.html

page_versions.py is the newsroom's (admin/build/page_versions.py at newsroom v0.12.113), copied as the brief asked,
not rewritten: a version of the book is frozen as markdown, and the delta between two versions is computed from the
frozen files, block by block and word by word.
"""
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import markdown  # noqa: E402
from page_versions import Versions, blocks, sha, words  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / "admin/build/version.txt").read_text().strip()
HOST = (ROOT / "CNAME").read_text().strip()
BASE = f"https://{HOST}/"
SITE = "gen-z-developers.sgit.ai"
TODAY = date.today().isoformat()
CONTENT = ROOT / "v1/content"
SOURCE_REPO = "https://github.com/DinisCruz/Book_Generation_Z_Developer"
SOURCE_COMMIT = "61886444fe5ab118ab18726147826ab05f794edc"
# The first edition's public record, read on 18 October 2026. The cover (v1/images/title_page.png) carries EIGHT
# lines, not the seven the newsroom article counted: "Look under the hood" is the one it missed.
FIRST_EDITION = {
    "amazon": {"url": "https://www.amazon.co.uk/Gen-Developers-concepts-generation-developers/dp/1724194607",
               "title": "Gen Z Developers", "pages": 139, "published": "30 September 2018", "isbn10": "1724194607",
               "size": "15.24 × 22.86 cm", "rating": "one five-star review"},
    "leanpub": {"url": "https://leanpub.com/generation-z", "title": "Generation Z Developers", "price": "free to read online, suggested price $10",
                "complete": "60%", "updated": "8 October 2018", "readers": 465, "pages": 136, "words": 30695, "formats": "PDF and EPUB"},
    "github": {"url": SOURCE_REPO, "files": 138, "outlines": 90},
    "cover_lines": ["Question everything", "Make fact based decisions", "Understand the history of tech", "Learn how to learn",
                    "Understand what game is being played", "Develop intellectual curiosity", "Look under the hood", "Shake things up"],
    "quotes": [("Amazing read for anyone new to, or wanting to get into programming. Brilliant background primer, not just for Gen Z.", "Kevin Fielder, on the Amazon listing"),
               ("This book teaches young developers how to become a developer. I wish I had this type of book when I started my career.", "Matt Parsons, on the Amazon listing")],
}

PARTS = [  # directory, slug, title, the Hugo weight that ordered it
    ("1.introduction", "introduction", "Introduction"),
    ("2.mvp-for-gen-z-dev", "mvp-for-gen-z-dev", "MVP for Gen Z Dev"),
    ("3.technologies", "technologies", "Technologies"),
    ("4.life-patterns", "life-patterns", "Life Patterns"),
    ("5.concepts", "concepts", "Concepts"),
    ("6.security", "security", "Security"),
    ("7.your-cv", "your-cv", "Your CV"),
    ("10.misc", "misc", "Misc"),
]

NAV = [
    ("The book", "v1/book/index.html"),
    ("Versions", "v1/versions/index.html"),
    ("The map", "map/index.html"),
    ("The briefs", "briefs/index.html"),
    ("The team", "team/index.html"),
    ("The vault", "vault/index.html"),
    ("Admin", "admin/index.html"),
]

written = []


# ------------------------------------------------------------------ helpers
def md(text, up=""):
    """Markdown to HTML. Image paths are rebased by the caller. One 2018 link is a bare domain (wallabyjs.com); it is
    rendered with its scheme, and left as written in the frozen markdown."""
    # The 2018 markdown often starts a list straight after a paragraph line, which Leanpub rendered as a list and
    # python-markdown renders as the paragraph's text. A blank line before the first item restores the list.
    out, prev = [], ""
    for line in text.splitlines():
        if re.match(r"^\s*([-*+]|\d+[.)])\s+\S", line) and prev.strip() and not re.match(r"^\s*([-*+]|\d+[.)])\s+", prev) and not prev.startswith(("    ", "\t")):
            out.append("")
        out.append(line); prev = line
    text = "\n".join(out)
    h = markdown.markdown(text, extensions=["extra", "sane_lists", "toc"], output_format="html5")
    return h.replace('href="wallabyjs.com"', 'href="https://wallabyjs.com"')


def esc(s):
    return html.escape(str(s), quote=True)


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    written.append(rel)


def up_for(rel):
    return "../" * (len(rel.split("/")) - 1)


def page(rel, title, body, description, crumbs=(), extra_head="", wide=False):
    up = up_for(rel)
    here = rel.split("/")[0] if "/" in rel else ""
    nav = "".join(
        f'<a class="nl{" here" if (href.split("/")[0] == here and here) else ""}" href="{up}{href}">{esc(label)}</a>'
        for label, href in NAV)
    crumb = ""
    if crumbs:
        items = [f'<a href="{up}index.html">{SITE}</a>']
        for label, href in crumbs[:-1]:
            items.append(f'<a href="{up}{href}">{esc(label)}</a>')
        items.append(f"<b>{esc(crumbs[-1][0])}</b>")
        crumb = '<div class="crumbs">' + " &rarr; ".join(items) + "</div>"
    canonical = BASE + ("" if rel == "index.html" else rel)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} &mdash; {SITE}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<link rel="stylesheet" href="{up}assets/site.css">
{extra_head}</head>
<body>
<nav class="site"><div class="row">
<a class="brand" href="{up}index.html">gen-z-developers<span>.sgit.ai</span></a>
<a class="parent" href="https://sgit.ai" title="sgit.ai, the parent project">&#8599; part of <b>sgit.ai</b></a>
{nav}
<span class="ver">site <a href="{up}admin/versions.html" title="Release history">{VERSION}</a></span>
</div></nav>
<main><div class="inner{" wide" if wide else ""}">
{crumb}
{body}
</div></main>
<footer class="site"><div class="row">
<span>Generation Z Developers, by Dinis Cruz. The 2018 text is Creative Commons BY (the cover) or BY-SA (the footer): see <a href="{up}v1/versions/index.html#licence">the licence note</a>. Everything else on this site is CC BY 4.0; code under the repository licence.</span>
<span><a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers">GitHub</a> &middot; <a href="{up}vault/index.html">the working vault</a> &middot; <a href="{up}admin/versions.html">release history</a> &middot; <a href="{up}llms.txt">llms.txt</a></span>
</div></footer>
</body>
</html>
"""
    write(rel, doc)


# ------------------------------------------------------------------ the book
def frontmatter(text):
    m = re.match(r"---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def fm_get(fm, key):
    m = re.search(rf"^{key}\s*[.]?\s*:\s*(.*)$", fm, re.M)
    return m.group(1).strip().strip('"') if m else ""


def slugify(stem):
    return re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")


def load_book():
    """The book as parts and chapters, in the order the 2018 Hugo site showed them: parts by their weight (the
    directory number), written chapters before outlines (the 2018 site split them into content/ and draft/), then by
    weight, then by title. Files under _manuscript/ and the Hugo apparatus are not chapters."""
    parts = []
    for d, pslug, ptitle in PARTS:
        pdir = CONTENT / d
        idx = pdir / "_index.md"
        pfm, pbody = frontmatter(idx.read_text(encoding="utf-8")) if idx.exists() else ("", "")
        pweight = int(fm_get(pfm, "weight") or 999)
        chapters = []
        for f in sorted(pdir.rglob("*.md")):
            if f.name == "_index.md":
                continue
            rel = f.relative_to(CONTENT).as_posix()
            fm, body = frontmatter(f.read_text(encoding="utf-8"))
            title = fm_get(fm, "title")
            if not title or title.startswith("status"):
                title = f.stem.replace("-", " ").strip().capitalize()
                title_note = "The 2018 file has no title; this one is from its file name."
            else:
                title_note = ""
            outline = "Topics to cover" in body
            status = fm_get(fm, "status") or "unset"
            weight = fm_get(fm, "weight")
            weight = int(weight) if weight.isdigit() else 999
            group = 1 if (outline or f.parent.name == "draft") else 0
            chapters.append({
                "file": rel, "slug": slugify(f.stem), "title": title, "title_note": title_note, "status": status,
                "outline": outline, "weight": weight, "group": group, "body": body.strip(),
                "words": len(re.findall(r"\w+", body)), "sha": sha(f.read_text(encoding="utf-8")),
                "what": fm_get(fm, "what"), "task": fm_get(fm, "task"), "price": fm_get(fm, "price"),
            })
        chapters.sort(key=lambda c: (c["group"], c["weight"], c["title"].lower()))
        parts.append({"dir": d, "slug": pslug, "title": ptitle, "weight": pweight, "intro": pbody.strip(),
                      "chapters": chapters, "sha": sha(idx.read_text(encoding="utf-8")) if idx.exists() else None})
    parts.sort(key=lambda p: p["weight"])
    return parts


def rebase_images(body, up):
    """Image links in the 2018 markdown are Hugo-root relative (images/...). Point them at v1/images/ from a page
    `up` levels down; a figure the 2018 repository never generated (the STEM PlantUML diagrams) becomes a note."""
    def fix(m):
        alt, url = m.group(1), m.group(2)
        if url.startswith("images/"):
            return f"![{alt}]({up}images/{url[7:]})"
        if url.startswith("../../puml-graphs/"):
            return f"*[Figure missing from the 2018 repository: `{url.rsplit('/', 1)[-1]}` was never generated from its PlantUML source.]*"
        return m.group(0)
    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", fix, body)


def chapter_url(c, part):
    return f"v1/book/{part['slug']}/{c['slug']}.html"


def badge(c):
    return ('<span class="badge outline">outline</span>' if c["outline"] else '<span class="badge written">written</span>')


def build_book(parts, map_rows):
    manifest = {"version": "v1.0.0", "site": VERSION, "source": {"repository": SOURCE_REPO, "commit": SOURCE_COMMIT},
                "what": "The hash of every chapter's markdown (v1/content/) and of the <main> it rendered; validate.js "
                        "refuses a page that no longer matches its markdown, or markdown that was edited behind its page.",
                "chapters": []}
    flat = [(p, c) for p in parts for c in p["chapters"]]
    by_file = {r["file"]: r for r in map_rows}
    n_written = sum(1 for _, c in flat if not c["outline"])
    n_outline = len(flat) - n_written
    total_words = sum(c["words"] for _, c in flat)

    # one page per chapter
    for i, (p, c) in enumerate(flat):
        rel = chapter_url(c, p)
        up = up_for(rel)
        body_html = md(rebase_images(c["body"], "../../"))
        prev = flat[i - 1] if i > 0 else None
        nxt = flat[i + 1] if i + 1 < len(flat) else None
        pn = '<div class="prevnext">'
        pn += (f'<a href="../{prev[0]["slug"]}/{prev[1]["slug"]}.html">&larr; {esc(prev[1]["title"])}</a>' if prev else "<span></span>")
        pn += (f'<a href="../{nxt[0]["slug"]}/{nxt[1]["slug"]}.html">{esc(nxt[1]["title"])} &rarr;</a>' if nxt else "<span></span>")
        pn += "</div>"
        row = by_file.get(c["file"])
        answers = ""
        if row and row["articles"]:
            answers = ('<p class="small dim">Answered since, on the newsroom: ' + ", ".join(
                f'<a href="{a["url"]}">{esc(a["title"])}</a>' for a in row["articles"]) + f'. <a href="{up}map/index.html#{slugify(c["file"])}">The map row</a>.</p>')
        elif row:
            answers = f'<p class="small dim">No newsroom article answers it yet. <a href="{up}map/index.html#{slugify(c["file"])}">The map row</a>.</p>'
        note = ""
        if c["outline"]:
            note = ('<div class="outline-note">In the 2018 edition this chapter was an outline: a title and "Topics to cover and ideas". '
                    'It is shown exactly as released. The second edition fills it from the articles the map names.</div>')
        if c["title_note"]:
            note += f'<p class="small dim">{esc(c["title_note"])}</p>'
        mvp = ""
        if c["what"] or c["task"]:
            mvp = '<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{esc(v)}</dd>" for k, v in (("What", c["what"]), ("Task", c["task"]), ("Price", c["price"])) if v) + "</dl>"
        main = (f'<article class="chapter"><p class="small dim">{esc(p["title"])} &middot; chapter {i + 1} of {len(flat)} &middot; {badge(c)} '
                f'<span class="badge frozen">v1.0.0, 2018, frozen</span> &middot; {c["words"]:,} words &middot; '
                f'<a href="{SOURCE_REPO}/blob/{SOURCE_COMMIT}/content/{c["file"]}">the 2018 file</a></p>'
                f'<h1>{esc(c["title"])}</h1>{note}{mvp}<div class="body">{body_html}</div>{answers}{pn}</article>')
        page(rel, c["title"], main, f"{c['title']}, a chapter of Generation Z Developers (2018), as released.",
             crumbs=(("The book", "v1/book/index.html"), (p["title"], f"v1/book/index.html#{p['slug']}"), (c["title"], rel)))
        manifest["chapters"].append({"file": c["file"], "page": rel, "title": c["title"], "part": p["title"],
                                     "kind": "outline" if c["outline"] else "written", "words": c["words"],
                                     "markdown_sha256": c["sha"], "main_sha256": sha(main)})

    # the table of contents
    toc = []
    for pi, p in enumerate(parts):
        items = "".join(
            f'<li><a href="{p["slug"]}/{c["slug"]}.html">{esc(c["title"])}</a> {badge(c)}<span class="w">{c["words"]:,} words</span></li>'
            for c in p["chapters"])
        plain = re.sub(r"\s+", " ", re.sub(r"!\[.*?\]\(.*?\)", "", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", p["intro"]))).strip()
        intro = f'<p class="small dim">{esc(plain[:220])}&hellip;</p>' if len(plain) > 40 else ""
        toc.append(f'<li id="{p["slug"]}"><div class="part"><span class="n">{pi + 1}</span>{esc(p["title"])} '
                   f'<span class="w">{len(p["chapters"])} chapters, {sum(1 for c in p["chapters"] if not c["outline"])} written</span></div>{intro}<ol>{items}</ol></li>')
    fe = FIRST_EDITION
    body = f"""<div class="toc-head"><a href="../images/title_page.png"><img class="thumb" src="../images/title_page.png" alt="The cover of Gen Z Developers, early release, September 2018" width="150" height="227"></a><div>
<h1>Generation Z Developers <span class="badge frozen">v1.0.0 &middot; 2018 &middot; frozen</span></h1>
<p class="lede">Key concepts and ideas for the next generation of developers. The first edition, as released: September 2018 on Leanpub at 60% complete, last updated 8 October 2018, and the same text on Amazon. This is the official version this repository holds; nothing in it changes. <a href="../versions/index.html">The versions page</a> records it, and will show the delta to the next one.</p>
<p><span class="stat"><b>{len(flat)}</b><span>chapters</span></span> <span class="stat"><b>{n_written}</b><span>written</span></span> <span class="stat"><b>{n_outline}</b><span>outlines</span></span> <span class="stat"><b>{total_words:,}</b><span>words in the source</span></span> <span class="stat"><b>8</b><span>parts</span></span></p>
<p><a href="single.html">Read it on one page</a> &middot; <a href="../versions/v1.0.0.md">the frozen markdown</a> &middot; <a href="../../map/index.html">the map to the newsroom articles</a></p>
<p class="small">Where the first edition lives: <a href="{fe["amazon"]["url"]}">the paperback on Amazon</a> ({fe["amazon"]["pages"]} pages, published {fe["amazon"]["published"]}, ISBN-10 {fe["amazon"]["isbn10"]}) &middot; <a href="{fe["leanpub"]["url"]}">Leanpub</a> ({fe["leanpub"]["price"]}; {fe["leanpub"]["complete"]} complete, {fe["leanpub"]["readers"]} readers, {fe["leanpub"]["words"]:,} words) &middot; <a href="{SOURCE_REPO}">the source on GitHub</a>.</p>
</div></div>
<div class="note">The 2018 site showed, in each part, the chapters with text first and the outlines after, and this table keeps that order. An <span class="badge outline">outline</span> is a title and "Topics to cover and ideas": {n_outline} of the {len(flat)} chapters, and with the outline template itself, 90 of the 138 files. The second edition fills them from the newsroom's articles; <a href="../../map/index.html">the map</a> says which.</div>
<ul class="toc">{"".join(toc)}</ul>
"""
    page("v1/book/index.html", "The book, v1.0.0 (2018)", body,
         "Generation Z Developers, the 2018 first edition as released, chapter by chapter.", crumbs=(("The book", "v1/book/index.html"),))

    # the whole book on one page, and the frozen markdown it is a projection of
    single, frozen = [], [f"# Generation Z Developers\n\n*Key concepts and ideas for the next generation of developers. Dinis Cruz, 2018. "
                          f"Version v1.0.0: the first edition as released, frozen from {SOURCE_REPO} at {SOURCE_COMMIT[:9]}.*\n"]
    single.append('<h1>Generation Z Developers <span class="badge frozen">v1.0.0 &middot; 2018 &middot; frozen</span></h1>'
                  '<p class="lede">The whole first edition on one page, in reading order. <a href="index.html">The table of contents</a>.</p>')
    for pi, p in enumerate(parts):
        single.append(f'<h2 class="part" id="{p["slug"]}">Part {pi + 1}: {esc(p["title"])}</h2>')
        frozen.append(f"\n# Part {pi + 1}: {p['title']}\n")
        if p["intro"]:
            single.append(f'<div class="body">{md(rebase_images(p["intro"], "../"))}</div>')
            frozen.append(rebase_images(p["intro"], "") + "\n")
        for c in p["chapters"]:
            single.append(f'<h3 class="ch" id="{c["slug"]}">{esc(c["title"])}</h3><p class="meta">{badge(c)} {c["words"]:,} words &middot; '
                          f'<a href="{p["slug"]}/{c["slug"]}.html">its own page</a></p><div class="body">{md(rebase_images(c["body"], "../"))}</div>')
            frozen.append(f"\n## {c['title']}\n\n*{'Outline' if c['outline'] else 'Written'}, {c['words']} words, {c['file']}.*\n\n" + rebase_images(c["body"], "") + "\n")
    page("v1/book/single.html", "The book on one page, v1.0.0 (2018)", '<div class="single">' + "".join(single) + "</div>",
         "Generation Z Developers (2018), the whole first edition on one page.", crumbs=(("The book", "v1/book/index.html"), ("On one page", "v1/book/single.html")))
    write("v1/book/manifest.json", json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    return "\n".join(frozen), flat


# ------------------------------------------------------------------ versions
def build_versions(frozen_md, parts):
    v = Versions("v1", "admin/content/book")
    e = v.entries[-1]
    got = sha(frozen_md)
    if e.get("text_sha256") is None:  # the one bootstrap: the first version's hash, recorded once
        e["text_sha256"] = got
        v.file.write_text(json.dumps(v.data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"build: recorded text_sha256 for {e['version']} in {v.file.relative_to(ROOT)}")
    e = v.current(frozen_md)  # exits if the frozen text changed with no new version: v1 is frozen
    if v.freeze(e, frozen_md):
        print(f"build: froze {v.snapshot(e)}")
    table, diffs = v.history_html()
    changelog = (CONTENT / "_manuscript/change-log.md").read_text(encoding="utf-8")
    changelog_html = md(frontmatter(changelog)[1])
    rows = "".join(f"<tr><td>{esc(e['version'])}</td><td>{esc(e['date'])}</td><td>{esc(e.get('where', ''))}</td><td>{esc(e['why'])}</td></tr>" for e in reversed(v.entries))
    body = f"""<h1>The versions of the book</h1>
<p class="lede">The rule this site is built on: <b>the repository holds the official versions; the vault holds the working versions.</b> A version moves from <a href="../../vault/index.html">the vault</a> into the repository when it is signed off, on top of the one before, and this page shows the delta between every two versions, block by block and word by word. There is one version so far.</p>
{table}
<p class="small dim">The table and the deltas are computed by the newsroom's <code>page_versions.py</code> (newsroom v0.12.113), copied into <code>admin/build/</code> as the brief asked rather than rewritten. Each version is frozen as one markdown file by the release that made it and never rewritten; the frozen file for v1.0.0 is <a href="v1.0.0.md">v1.0.0.md</a>, {words(chr(10).join(blocks(frozen_md))):,} words in {len(blocks(frozen_md)):,} blocks.</p>
{diffs}
<h2 id="record">The record</h2>
<div class="tablewrap"><table><thead><tr><th>Version</th><th>Date</th><th>Where</th><th>What it is</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2 id="source">Where v1.0.0 comes from</h2>
<ul>
<li>The repository <a href="{SOURCE_REPO}">DinisCruz/Book_Generation_Z_Developer</a> at commit <code>{SOURCE_COMMIT[:12]}</code> (1 March 2024, a README change; the content was last changed in October 2018). Its <code>content/</code> folder is copied verbatim to <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers/tree/dev/v1/content">v1/content/</a> and its <code>static/images/</code> to <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers/tree/dev/v1/images">v1/images/</a>: 138 markdown files, 90 of them outlines.</li>
<li><a href="https://leanpub.com/generation-z">Leanpub</a>: "Key concepts and ideas for the next generation of developers", 60% complete, 136 pages, 30,695 words, last updated 8 October 2018, 465 readers (read 18 October 2026). The Leanpub build left the outlines out; this site shows them, because the second edition starts from them.</li>
<li>Amazon: <a href="{FIRST_EDITION["amazon"]["url"]}">Gen Z Developers</a>, the paperback: {FIRST_EDITION["amazon"]["pages"]} pages, published {FIRST_EDITION["amazon"]["published"]}, ISBN-10 {FIRST_EDITION["amazon"]["isbn10"]}, the early-release cover of September 2018 with its eight lines. That publication date is the date of v1.0.0; 8 October 2018 is the last change to the text, on Leanpub and in the repository.</li>
</ul>
<h2 id="leanpub">The 2018 change log, v0.30 to v0.60</h2>
<p class="small dim">As the book's own <code>_manuscript/change-log.md</code> records it. The contributors it names are to be credited in the second edition, with their permission.</p>
<div class="body">{changelog_html}</div>
<h2 id="licence">The licence</h2>
<p>The repository's licence file is Apache 2.0 (kept as <a href="../LICENSE-2018-repository.txt">v1/LICENSE-2018-repository.txt</a>). The book's Introduction says Creative Commons Attribution 4.0; its footer says Attribution-ShareAlike 4.0; the printed cover carries the CC BY mark. The build brief says to treat the text as CC BY and confirm with Dinis. Until that is settled, the 2018 text on this site is shown under the licence the book itself declares, and the question is open on <a href="../../team/index.html">the team's board</a>.</p>
"""
    page("v1/versions/index.html", "The versions of the book", body,
         "Every official version of Generation Z Developers, and the delta between them, block by block.",
         crumbs=(("The book", "v1/book/index.html"), ("Versions", "v1/versions/index.html")))


# ------------------------------------------------------------------ the map
def build_map(parts, map_doc):
    rows = map_doc["rows"]
    url_of = {c["file"]: chapter_url(c, p) for p in parts for c in p["chapters"]}
    groups = {}
    for r in rows:
        groups.setdefault(r["part"], []).append(r)
    order = [p["title"] for p in parts] + [k for k in groups if k not in [p["title"] for p in parts]]
    sections = []
    for part in order:
        rs = groups.get(part, [])
        if not rs:
            continue
        trs = []
        for r in rs:
            link = f'<a href="../{url_of[r["file"]]}">{esc(r["title"])}</a>' if r["file"] in url_of else esc(r["title"])
            arts = ", ".join(f'<a href="{a["url"]}">{esc(a["title"])}</a>' for a in r["articles"]) or '<span class="dim">none yet</span>'
            kind = {"written": '<span class="badge written">written</span>', "outline": '<span class="badge outline">outline</span>'}.get(r["kind"], '<span class="badge">apparatus</span>')
            gap = r["gap"]
            gap_html = {"": '<span class="dim">answered</span>', "none": '<span class="dim">no article yet</span>'}.get(gap, esc(gap))
            trs.append(f'<tr id="{slugify(r["file"])}"><td>{link}<br><code class="small">{esc(r["file"])}</code></td><td>{kind}<br><span class="small dim">2018 status: {esc(r["status_2018"])}, {r["words"]} words</span></td><td>{arts}</td><td class="gap">{gap_html}</td></tr>')
        sections.append(f'<h2 id="{slugify(part)}">{esc(part)} <span class="small dim">{len(rs)} files, {sum(1 for r in rs if r["articles"])} answered</span></h2>'
                        f'<div class="tablewrap"><table class="map"><thead><tr><th>Chapter</th><th>Kind</th><th>Newsroom articles that answer it</th><th>The gap, or what to do</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    c = map_doc["counts"]
    body = f"""<h1>The map: every 2018 file, and the article that answers it</h1>
<p class="lede">The second edition's first deliverable, as the build brief asked: one row per file of the 2018 book, whether it was written or an outline, the newsroom articles that have since answered it, and the gap. The reading is a first one; the reviewer's records and the editor's interviews decide what each chapter becomes.</p>
<p><span class="stat"><b>{c["files"]}</b><span>files</span></span> <span class="stat"><b>{c["written"]}</b><span>written</span></span> <span class="stat"><b>{c["outline"]}</b><span>outlines</span></span> <span class="stat"><b>{c["apparatus"]}</b><span>apparatus</span></span> <span class="stat"><b>{c["answered_by_articles"]}</b><span>answered</span></span> <span class="stat"><b>{c["articles_cited"]}</b><span>articles cited</span></span></p>
<div class="legend"><span><span class="badge written">written</span> a chapter with text in 2018</span><span><span class="badge outline">outline</span> a title and "Topics to cover and ideas"</span><span><span class="badge">apparatus</span> a Hugo file, not a chapter</span></div>
<p class="small dim">The data is <a href="../admin/content/map.json">admin/content/map.json</a>, written by <code>admin/build/gen_map.py</code>, where the reading is authored file by file. A row says "answered" when the articles cover the outline; "no article yet" when none does; otherwise what is missing, or a then-and-now note for a written chapter whose 2018 claims dated. Source: {esc(map_doc["source"])}.</p>
{"".join(sections)}
"""
    page("map/index.html", "The map", body, "One row per file of the 2018 book, the newsroom articles that answer it, and the gap.",
         crumbs=(("The map", "map/index.html"),), wide=True)


# ------------------------------------------------------------------ briefs
def build_briefs():
    files = sorted((ROOT / "admin/content/briefs").glob("*.md"))
    cards, llms = [], []
    for f in files:
        text = f.read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
        src = re.search(r"^\*Source: (.*?)\*$", text, re.M)
        rest = text.split("\n", 1)[1]
        rel = f"briefs/{f.stem}.html"
        short = title.split(":")[0]
        body = f'<article class="doc"><h1>{esc(title)}</h1><div class="body">{md(rest)}</div></article>'
        page(rel, short, body, f"{short}: a brief for this site, captured from the newsroom.", crumbs=(("The briefs", "briefs/index.html"), (short, rel)))
        kind = "note" if "__note-" in f.stem else "article"
        cards.append(f'<div class="card"><span class="k">{kind} {f.stem[:2]}</span><h3><a href="{f.stem}.html">{esc(short)}</a></h3><p>{esc(title.split(":", 1)[1].strip() if ":" in title else "")}</p>'
                     f'<a class="more" href="{f.stem}.html">Read it &rarr;</a></div>')
        llms.append((rel, short))
    body = f"""<h1>The briefs</h1>
<p class="lede">The six newsroom articles tagged <code>gen-z-book</code>, in the order they were published, and the two build briefs written for the agents that make the book and its website. They are the source of everything this site does; captured verbatim on 18 October 2026, with the newsroom's chrome left out.</p>
<div class="cards">{"".join(cards)}</div>
<div class="note">Every article says what it does not claim, and so does this site: on 18 October 2026, after this first release, the second edition is still unwritten. What exists is the first edition as released, the map, the roles, the working vault, and the versions page that will carry the delta when a second version is signed off.</div>
<p class="small dim">The captured markdown is in <code>admin/content/briefs/</code>; the newsroom's series page is <a href="https://newsroom.sgit.ai/articles/generation-z-developers-again.html">on each article</a>, and the briefs map is at <a href="https://newsroom.sgit.ai/briefs/index.html#gen-z-book-website">newsroom.sgit.ai/briefs</a>.</p>
"""
    page("briefs/index.html", "The briefs", body, "The newsroom articles and build briefs this site is made from.", crumbs=(("The briefs", "briefs/index.html"),))
    return llms


# ------------------------------------------------------------------ team
def build_team():
    roles = []
    for d in sorted((ROOT / "team").iterdir()):
        if not d.is_dir() or not (d / "role.md").exists():
            continue
        text = (d / "role.md").read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
        claim = re.search(r"\*\*Central claim\.\*\*\s*(.+)", text)
        claim = claim.group(1).strip() if claim else ""
        issues = {}
        for st in ("open", "blocked", "done"):
            issues[st] = sorted(p.name for p in (d / "issues" / st).glob("*.md"))
        briefs = sorted(p.name for p in (d / "briefs").glob("*.md")) if (d / "briefs").exists() else []
        debriefs = sorted(p.name for p in (d / "debriefs").glob("*.md")) if (d / "debriefs").exists() else []
        rel = f"team/{d.name}/index.html"
        lists = ""
        for st in ("open", "blocked", "done"):
            items = "".join(f'<li><a href="issues/{st}/{esc(n)}">{esc(n[:-3])}</a></li>' for n in issues[st]) or "<li class='dim'>none</li>"
            lists += f"<h3>Issues: {st} ({len(issues[st])})</h3><ul>{items}</ul>"
        bl = "".join(f'<li><a href="briefs/{esc(n)}">{esc(n[:-3])}</a></li>' for n in briefs) or "<li class='dim'>none yet</li>"
        dl = "".join(f'<li><a href="debriefs/{esc(n)}">{esc(n[:-3])}</a></li>' for n in debriefs) or "<li class='dim'>none yet</li>"
        body = (f'<article class="doc"><div class="body">{md(text)}</div>'
                f'<h2 id="work">The work environment</h2><p class="small dim">The folder is the status: an issue moves between open/, blocked/ and done/ with a <code>git mv</code>. '
                f'Another role may read this folder; only this role writes into it. Briefs arrive here; debriefs are what the role reports back, stamped with the version they reviewed.</p>'
                f'{lists}<h3>Briefs</h3><ul>{bl}</ul><h3>Debriefs</h3><ul>{dl}</ul></article>')
        page(rel, title, body, f"{title}: its mandate, what it refuses, and its work.", crumbs=(("The team", "team/index.html"), (title, rel)))
        roles.append((d.name, title, claim, sum(len(v) for v in issues.values()), len(issues["open"])))
    cards = "".join(f'<div class="card"><span class="k">role</span><h3><a href="{n}/index.html">{esc(t)}</a></h3><p>{esc(c)}</p><p class="small">{o} open of {k} issues</p><a class="more" href="{n}/index.html">The role &rarr;</a></div>' for n, t, c, k, o in roles)
    body = f"""<h1>The team</h1>
<p class="lede">The roles that finish the book, one folder each, after <a href="https://graphs.sgit.ai/v2/team/index.html">the seven roles of graphs.sgit.ai</a> and <a href="https://newsroom.sgit.ai/articles/the-agent-team-as-it-runs.html">the agent team as it runs</a>. The book's plan asks for a reviewer, an editor and a publisher at least; each reads the book, gives feedback, challenges it, writes interview scripts for Dinis, and signs off its part. Their briefs, debriefs, issues and interview transcripts are kept here, in the repository, so the workflow is mapped as it runs.</p>
<div class="cards role-grid">{cards}</div>
<div class="note">Every role names what it refuses. A role definition that would read the same in any other repository has failed its brief. The roles' working copies, the board and the reviews-in-progress live in <a href="../vault/index.html">the public vault</a>; what is signed off comes back here.</div>
<p class="small dim">The shape is the one <code>graphs.sgit.ai</code> uses: <code>role.md</code> with Identity, Foundation, Primary Responsibilities and Core Workflows; <code>issues/open|blocked|done/</code> where the folder is the status; <code>briefs/</code> and <code>debriefs/</code>. Stamps carry the version reviewed: <code>book__v1.0.0__&lt;slug&gt;.md</code> for the book, <code>v0.1.0__&lt;slug&gt;.md</code> for the site.</p>
"""
    page("team/index.html", "The team", body, "The roles that finish the book: reviewer, editor, publisher.", crumbs=(("The team", "team/index.html"),))
    return roles


# ------------------------------------------------------------------ vault
def build_vault():
    v = json.loads((ROOT / "admin/content/vault.json").read_text(encoding="utf-8"))
    pub = v["public"]
    body = f"""<h1>The working vault</h1>
<p class="lede">All work after v1 happens in a public, zero-knowledge encrypted vault, with its <b>read</b> key published here so that anyone can read along: drafts, comments, reviews, the board. Its write key is never published. When a version is signed off it moves from the vault into the repository, on top of the one before, and <a href="../v1/versions/index.html">the versions page</a> shows the delta.</p>
<h2>Open it</h2>
<dl class="kv">
<dt>In the browser</dt><dd><a href="{esc(pub["web"])}">{esc(pub["web"])}</a></dd>
<dt>With sgit</dt><dd><code>pip3 install sgit-ai</code> then <code>sgit clone {esc(pub["read_key"])}</code> (read-only)</dd>
<dt>Vault id</dt><dd><code>{esc(pub["id"])}</code> on <code>{esc(pub["remote"])}</code></dd>
<dt>Read key</dt><dd><code style="overflow-wrap:anywhere">{esc(pub["read_key"])}</code> <span class="small dim">(deliberately public; it opens the vault read-only)</span></dd>
<dt>Created</dt><dd>{esc(pub["created"])}, by the session that built this site, from the build brief</dd>
</dl>
<h2>What is in it</h2>
<ul>
{"".join(f"<li><code>{esc(k)}</code>: {esc(w)}</li>" for k, w in pub["layout"].items())}
</ul>
<p class="small dim">The vault opens on its own page (<code>_page.json</code>), with the same sections. Every file in it is encrypted on the device before it leaves; the server never sees plaintext, and the read key published above is what decrypts it in your browser.</p>
<h2 id="private">The private vault</h2>
<p>The OpenRouter key the agents use to reach a model <b>never goes in the public vault</b>: anything in a vault whose read key is published is readable by everyone. It goes in a second vault, <code>{esc(v["private"]["id"])}</code>, whose key is held only by Dinis and is not in this repository or on this site; the key itself carries a credit limit set at OpenRouter, so a mistake costs a little. The vault holds a <code>README.md</code> and an <code>openrouter.env.example</code> and nothing else until Dinis puts the key in. The newsroom's reader-vault pattern, a passkey opening the vault, is the intended door; see <a href="https://newsroom.sgit.ai/articles/the-passkey-opens-the-vault.html">the passkey opens the vault</a>.</p>
<h2>The rule, and the gate</h2>
<p>The repository's release gate (<code>admin/build/validate.js</code>) refuses any file carrying a private sgit key (any string with sgit's private-key prefix), the same rule sgit's own scanner uses; the public read key passes because public and private differ by a word, not a character. The vault's write key and the private vault's key were delivered to Dinis in the session that created them and exist nowhere in this tree.</p>
"""
    page("vault/index.html", "The working vault", body, "The public vault where the book is worked on, and how to open it read-only.", crumbs=(("The vault", "vault/index.html"),))
    return v


# ------------------------------------------------------------------ home, admin, agent surface
def build_home(parts, flat, map_doc, briefs, roles, vault):
    c = map_doc["counts"]
    six = [b for b in briefs if "__note-" not in b[0]]
    fe = FIRST_EDITION
    lines = "".join(f"<li>{esc(l)}</li>" for l in fe["cover_lines"])
    quotes = "".join(f'<blockquote class="quote">&ldquo;{esc(q)}&rdquo;<span>{esc(w)}</span></blockquote>' for q, w in fe["quotes"])
    body = f"""<section class="hero">
<a class="cover" href="v1/book/index.html"><img src="v1/images/title_page.png" alt="The cover of Gen Z Developers, early release, September 2018: navy, four colour blocks spelling GEN Z, and eight lines from Question everything to Shake things up" width="300" height="454"></a>
<div class="hero-text">
<p class="kicker"><span class="sw g"></span><span class="sw y"></span><span class="sw t"></span><span class="sw r"></span> a book by Dinis Cruz &middot; first edition September 2018 &middot; second edition in the making, dated October 2026</p>
<h1>Generation Z Developers</h1>
<p class="sub">Key concepts and ideas for the next generation of developers.</p>
<ul class="cover-lines">{lines}</ul>
<p>The eight lines on the cover are what the book was for. They read more urgently now than in 2018, and the second edition keeps all eight: the manual for getting into development, and getting a job, now that everyone who can brief an agent is a developer.</p>
<p class="ctas"><a class="btn primary" href="v1/book/index.html">Read the first edition here</a> <a class="btn" href="{fe["amazon"]["url"]}">Paperback on Amazon</a> <a class="btn" href="{fe["leanpub"]["url"]}">Free to read on Leanpub</a></p>
</div>
</section>
<h2 id="first-edition">The first edition, where it lives</h2>
<p class="lede">Released early and in public, the way the book told its readers to work: on Leanpub at 60% complete, as a paperback, and as Markdown in a Git repository. Those three are the record of v1.0.0, and this site shows that text exactly as released.</p>
<div class="cards editions">
<a class="card amazon" href="{fe["amazon"]["url"]}"><span class="k">Paperback &middot; Amazon</span><h3>{esc(fe["amazon"]["title"])}</h3><p>{fe["amazon"]["pages"]} pages &middot; published {fe["amazon"]["published"]} &middot; ISBN-10 {fe["amazon"]["isbn10"]} &middot; {fe["amazon"]["size"]} &middot; {fe["amazon"]["rating"]}</p><span class="more">amazon.co.uk &rarr;</span></a>
<a class="card leanpub" href="{fe["leanpub"]["url"]}"><span class="k">{fe["leanpub"]["formats"]} &middot; Leanpub</span><h3>{esc(fe["leanpub"]["title"])}</h3><p>{fe["leanpub"]["price"]} &middot; {fe["leanpub"]["complete"]} complete, last updated {fe["leanpub"]["updated"]} &middot; {fe["leanpub"]["readers"]} readers &middot; {fe["leanpub"]["pages"]} pages, {fe["leanpub"]["words"]:,} words</p><span class="more">leanpub.com/generation-z &rarr;</span></a>
<a class="card github" href="{fe["github"]["url"]}"><span class="k">The source &middot; GitHub</span><h3>Book_Generation_Z_Developer</h3><p>{fe["github"]["files"]} Markdown files, {fe["github"]["outlines"]} of them outlines &middot; Creative Commons BY on the cover &middot; feedback by GitHub issues &middot; imported here as v1.0.0, frozen</p><span class="more">github.com/DinisCruz &rarr;</span></a>
</div>
<div class="quotes">{quotes}</div>
<h2 id="second-edition">The second edition, in the making</h2>
<p class="lede"><b>The repository holds the official versions; the vault holds the working versions.</b> The first edition is here exactly as released. Everything after it is worked on in a public vault and moves here when signed off, with a delta between every two versions.</p>
<div class="making">
<div class="card big"><span class="k">The book &middot; v1.0.0 &middot; 2018 &middot; frozen</span><h3><a href="v1/book/index.html">Read it chapter by chapter, outlines included</a></h3><p>{len(flat)} chapters in 8 parts: {c["written"]} written, {c["outline"]} outlines. The Leanpub build left the outlines out; this site shows them, because the second edition starts from them.</p>
<p class="stats"><span class="stat"><b>{len(flat)}</b><span>chapters</span></span><span class="stat"><b>{c["written"]}</b><span>written</span></span><span class="stat"><b>{c["outline"]}</b><span>outlines</span></span><span class="stat"><b>{sum(ch["words"] for _, ch in flat):,}</b><span>words in the source</span></span></p>
<span class="more"><a href="v1/book/index.html">The table of contents &rarr;</a> &nbsp; <a href="v1/book/single.html">On one page &rarr;</a></span></div>
<a class="card" href="v1/versions/index.html"><span class="k">Versions</span><h3>One version so far</h3><p>Where v1.0.0 comes from, the 2018 change log, and the page that will carry the block-by-block delta to v2.</p></a>
<a class="card" href="map/index.html"><span class="k">The map</span><h3>{c["files"]} files, {c["answered_by_articles"]} answered</h3><p>Every 2018 chapter and outline, the newsroom articles that have since answered it, and the gap.</p></a>
<a class="card" href="team/index.html"><span class="k">The team</span><h3>Reviewer, editor, publisher</h3><p>Each reads, challenges, interviews Dinis and signs off. The first interview script is written.</p></a>
<a class="card" href="vault/index.html"><span class="k">The vault</span><h3>Read along</h3><p>The public working vault, its read key published: the working copy of v1, the board, the reviews, the roles.</p></a>
</div>
<div class="twocol">
<div><h2>The articles behind it</h2><p class="small dim">The newsroom series tagged gen-z-book, in the order published, and <a href="briefs/index.html">the two build briefs</a>: captured verbatim.</p>
<ol>
{"".join(f'<li><a href="{rel}">{esc(t)}</a></li>' for rel, t in six)}
</ol></div>
<div><h2>What this site does not claim</h2>
<ul>
<li><b>The second edition is not written.</b> This release has the first edition, the map, the roles, the vault and the versions machinery.</li>
<li><b>The map is a first reading.</b> Not every outline has an article, and not every article fits; the reviewer and the editor decide.</li>
<li><b>The address is the one proposed</b>, matching the printed cover's <i>Gen Z Developers</i>; to confirm.</li>
<li><b>The licence of the 2018 text is to confirm</b> with Dinis: CC BY on the cover, CC BY-SA in the footer, Apache 2.0 on the repository.</li>
</ul></div>
</div>
<p class="small dim">Built as the build brief <a href="briefs/08__note-a-website-to-finish-the-book.html">a website to finish the book</a> asked: the new repository with v1 imported as released, a static site showing it chapter by chapter, and a versions page reusing the newsroom's <code>page_versions.py</code>. The agent surface is <a href="llms.txt">llms.txt</a>.</p>
"""
    page("index.html", "Generation Z Developers, the second edition", body,
         "The website for finishing the second edition of Generation Z Developers: the 2018 book as released, the map to the newsroom's articles, the roles, and the working vault.", wide=True)

    # admin
    vs = json.loads((ROOT / "admin/content/versions.json").read_text(encoding="utf-8"))
    rows = "".join(f'<tr><td><b>{esc(r["version"])}</b></td><td>{esc(r["date"])}</td><td>{esc(r["what"])}</td></tr>' for r in reversed(vs["releases"]))
    if vs["releases"][-1]["version"] != VERSION:
        sys.exit(f"build: version.txt says {VERSION} but the newest row in admin/content/versions.json is {vs['releases'][-1]['version']}; add a row")
    page("admin/versions.html", "Release history", f'<h1>Release history</h1><p class="lede">Every release of this site, narrated: a reader should understand the change without opening the diff. Every push to <code>dev</code> is a release, tagged <code>vX.Y.Z</code> by CI, which refuses a release whose <code>version.txt</code> disagrees with the commit subject.</p><div class="tablewrap"><table><thead><tr><th>Site</th><th>Date</th><th>What changed, and why</th></tr></thead><tbody>{rows}</tbody></table></div>',
         "Every release of gen-z-developers.sgit.ai, narrated.", crumbs=(("Admin", "admin/index.html"), ("Release history", "admin/versions.html")))
    page("admin/index.html", "Admin and engineering", f"""<h1>Admin and engineering</h1>
<p class="lede">How this site is built, and the rules it keeps.</p>
<h2>The chain</h2>
<pre>python3 admin/build/gen_map.py     # admin/content/map.json from v1/content/ and the authored reading
python3 admin/build/build.py       # every page, the manifest, the frozen markdown, llms.txt, the sitemap
node admin/build/validate.js       # the gate: version, links, canonical, key leak, manifest, sitemap, map</pre>
<h2>The rules</h2>
<ul>
<li><b>v1/ is frozen.</b> <code>v1/content/</code> is the 2018 book as released; <code>build.py</code> stops if the frozen text changes without a new entry in <code>admin/content/book/versions.json</code>, and <code>validate.js</code> stops if a page no longer matches its markdown.</li>
<li><b>Markdown is the source of truth.</b> Every chapter page, brief and role page is a projection of a markdown file; <code>v1/book/manifest.json</code> records the hashes.</li>
<li><b>Every release is narrated</b> in <a href="versions.html">the release history</a>, and the version in <code>admin/build/version.txt</code> must match the commit subject <code>site vX.Y.Z: ...</code>.</li>
<li><b>No private key in the tree.</b> The gate refuses any string with sgit's private-key prefix. The public read key on <a href="../vault/index.html">the vault page</a> is public by design.</li>
<li><b>The repository holds the official versions; the vault holds the working versions.</b></li>
</ul>
<h2>Where things are</h2>
<ul>
<li><code>v1/content/</code>, <code>v1/images/</code>: the 2018 book. <code>v1/book/</code>: its pages. <code>v1/versions/</code>: the frozen markdown and the versions page.</li>
<li><code>admin/content/</code>: the authored data (map, briefs, versions, vault). <code>admin/build/</code>: the generators, <code>page_versions.py</code> from the newsroom, <code>validate.js</code>.</li>
<li><code>team/</code>: the roles, their issues, briefs and debriefs. <code>vault/</code>: how to open the working vault.</li>
<li><code>.github/workflows/deploy-pages.yml</code>: validate, tag, deploy to GitHub Pages, the same pipeline as the sibling sites.</li>
</ul>
<p><a href="versions.html">Release history</a> &middot; <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers">the repository</a></p>
""", "How gen-z-developers.sgit.ai is built.", crumbs=(("Admin", "admin/index.html"),))

    # 404, robots, sitemap, llms.txt
    page("404.html", "Not here", '<h1>Not here</h1><p>That page is not on this site. <a href="index.html">The front page</a>, <a href="v1/book/index.html">the book</a>, <a href="map/index.html">the map</a>.</p>', "Page not found.",
         extra_head='<meta name="robots" content="noindex">\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    pages = [w for w in written if w.endswith(".html") and w != "404.html"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{BASE}{'' if p == 'index.html' else p}</loc></url>\n" for p in sorted(pages)) + "</urlset>\n")
    chapters = "\n".join(f"- [{c['title']}]({BASE}{chapter_url(c, p)}): {'outline' if c['outline'] else 'written'}, {c['words']} words, part {p['title']}" for p in parts for c in p["chapters"])
    write("llms.txt", f"""# gen-z-developers.sgit.ai

> The website for finishing the second edition of Generation Z Developers (Dinis Cruz, 2018). The repository holds the official versions of the book; a public vault holds the working versions. Site {VERSION}.

## The rule
The repository holds the official versions; the vault holds the working versions. v1.0.0 is the 2018 first edition as released, frozen. A version moves from the vault to the repository when signed off, and the versions page shows the delta block by block.

## Sections
- [The book, v1.0.0]({BASE}v1/book/index.html): the 2018 first edition chapter by chapter; [on one page]({BASE}v1/book/single.html); [frozen markdown]({BASE}v1/versions/v1.0.0.md)
- [Versions]({BASE}v1/versions/index.html): the official versions and their deltas (page_versions.py from the newsroom)
- [The map]({BASE}map/index.html): one row per 2018 file, the newsroom articles that answer it, the gap; data at [map.json]({BASE}admin/content/map.json)
- [The briefs]({BASE}briefs/index.html): the six newsroom articles tagged gen-z-book and the two build briefs, verbatim
- [The team]({BASE}team/index.html): reviewer, editor, publisher; role.md, issues, briefs, debriefs, the first interview script
- [The vault]({BASE}vault/index.html): the public working vault, read key published; the private vault for the OpenRouter key
- [Admin]({BASE}admin/index.html): the build chain and rules; [release history]({BASE}admin/versions.html)

## The briefs
{chr(10).join(f"- [{t}]({BASE}{rel})" for rel, t in briefs)}

## The chapters of v1.0.0
{chapters}

## The first edition, where it lives
- Paperback on Amazon: {FIRST_EDITION["amazon"]["url"]} ({FIRST_EDITION["amazon"]["pages"]} pages, published {FIRST_EDITION["amazon"]["published"]}, ISBN-10 {FIRST_EDITION["amazon"]["isbn10"]})
- Leanpub, free to read online: {FIRST_EDITION["leanpub"]["url"]} ({FIRST_EDITION["leanpub"]["complete"]} complete, {FIRST_EDITION["leanpub"]["readers"]} readers, {FIRST_EDITION["leanpub"]["words"]} words)
- The cover's eight lines: {"; ".join(FIRST_EDITION["cover_lines"])}

## The source
- 2018 repository: {SOURCE_REPO} at {SOURCE_COMMIT}
- Leanpub: https://leanpub.com/generation-z (60% complete, last updated 2018-10-08)
- The newsroom series: https://newsroom.sgit.ai/articles/generation-z-developers-again.html
- The vault, read-only: {vault["public"]["web"]}
""")


def main():
    (ROOT / "v1/MANIFEST.json").write_text(json.dumps({
        "what": "v1 is the first edition of Generation Z Developers as released in 2018, frozen. Nothing under v1/content/ or v1/images/ changes except to fix a copy error; v1/book/ and v1/versions/ are generated from them.",
        "version": "v1.0.0", "released": "2018-09-30", "last_content_change": "2018-10-08", "frozen_on": "2026-10-18",
        "source": {"repository": SOURCE_REPO, "commit": SOURCE_COMMIT, "paths": ["content/", "static/images/", "LICENSE"]},
        "leanpub": {"url": "https://leanpub.com/generation-z", "complete": "60%", "pages": 136, "words": 30695, "readers": 465, "read_on": "2026-10-18"},
        "counts": {"markdown_files": 138, "outlines": 90},
    }, indent=1) + "\n", encoding="utf-8")
    parts = load_book()
    map_doc = json.loads((ROOT / "admin/content/map.json").read_text(encoding="utf-8"))
    files_in_map = {r["file"] for r in map_doc["rows"]}
    files_on_disk = {p.relative_to(CONTENT).as_posix() for p in CONTENT.rglob("*.md")}
    if files_in_map != files_on_disk:
        sys.exit(f"build: map.json and v1/content disagree: {sorted(files_in_map ^ files_on_disk)}; run gen_map.py")
    frozen_md, flat = build_book(parts, map_doc["rows"])
    build_versions(frozen_md, parts)
    build_map(parts, map_doc)
    briefs = build_briefs()
    roles = build_team()
    vault = build_vault()
    build_home(parts, flat, map_doc, briefs, roles, vault)
    print(f"build: {VERSION}, {len(flat)} chapters, {len([w for w in written if w.endswith('.html')])} pages, {len(written)} files written")


if __name__ == "__main__":
    main()
