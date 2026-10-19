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
  admin/content/articles/NN__<slug>.md   articles co-written with Dinis, in Dinis's voice: ideas, tasks and reviews for the roles
  admin/content/agent-articles/NN__*.md  agent articles: one per significant body of work, in the agent's own voice
  admin/content/decisions/NNN__*.md      Dinis's decisions on how the book is made, versioned and published
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
from collections import Counter
from html.parser import HTMLParser
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import markdown  # noqa: E402
from page_versions import Versions, blocks, sha, words  # noqa: E402
from graph_pages import build_graph
from paper_reviews import build_paper_reviews
from readers_pages import build_readers  # noqa: E402
import graph_model  # noqa: E402
from book_v2 import build_v2  # noqa: E402  # noqa: E402
from infographics import build_infographics  # noqa: E402
from covers_pages import build_covers  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
VERSION = (ROOT / "admin/build/version.txt").read_text().strip()
HOST = (ROOT / "CNAME").read_text().strip()
BASE = f"https://{HOST}/"
SITE = "gen-z-developers.sgit.ai"
TODAY = date.today().isoformat()
CONTENT = ROOT / "v1/content"
SOURCE_REPO = "https://github.com/DinisCruz/Book_Generation_Z_Developer"
SOURCE_COMMIT = "61886444fe5ab118ab18726147826ab05f794edc"
PDF_SHA = hashlib.sha256((ROOT / "v1/generation-z-print-ready.pdf").read_bytes()).hexdigest()
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

# The top bar: five groups, each a link to its first page with the rest in a menu under it. It held thirteen links on
# one row, which overflowed onto two lines on a laptop and three on a tablet. The flat list is NAV, for anything that
# needs every section.
NAV_GROUPS = [
    ("The book", [("The first edition", "v1/book/index.html"), ("Second edition", "v2/book/index.html"), ("Read & review", "read/index.html"), ("Synthetic readers", "readers/index.html"), ("Covers", "covers/index.html"),
                  ("Versions", "v1/versions/index.html"), ("Contributors", "contributors/index.html")]),
    ("Storyboards", [("Storyboards", "storyboards/index.html"), ("Every panel", "storyboards/all.html"),
                     ("The model sheet", "storyboards/model-sheet.html")]),
    ("Infographics", [("Infographics", "infographics/index.html"), ("The plan, and the review", "infographics/plan.html"),
                      ("What exists", "infographics/existing.html"), ("How they are made", "infographics/how.html")]),
    ("Articles", [("Articles", "articles/index.html"), ("Decisions", "decisions/index.html"), ("The briefs", "briefs/index.html")]),
    ("The graph", [("The graph", "graph/index.html"), ("The map", "map/index.html")]),
    ("The team", [("The team", "team/index.html"), ("The vault", "vault/index.html"), ("Admin", "admin/index.html")]),
]
NAV = [item for _, items in NAV_GROUPS for item in items]

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
    ishere = lambda href: bool(here) and href.split("/")[0] == here and (here != "v1" or href.split("/")[1] == rel.split("/")[1])
    nav = "".join(
        f'<div class="ni"><a class="nl{" here" if any(ishere(h) for _, h in items) else ""}" href="{up}{items[0][1]}">{esc(group)}<span class="caret" aria-hidden="true">&#9662;</span></a>'
        f'<div class="sub">{"".join(f"""<a class="sl{' here' if h == rel else ''}" href="{up}{h}">{esc(label)}</a>""" for label, h in items)}</div></div>'
        for group, items in NAV_GROUPS)
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
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%276%27 fill=%27%230c2a3d%27/%3E%3Crect x=%274%27 y=%276%27 width=%2711%27 height=%2720%27 fill=%27%237bc08f%27/%3E%3Crect x=%2717%27 y=%276%27 width=%2711%27 height=%2720%27 fill=%27%23e5625b%27/%3E%3Ctext x=%2716%27 y=%2723%27 font-family=%27Arial Black,Arial%27 font-weight=%27900%27 font-size=%2718%27 text-anchor=%27middle%27 fill=%27%230c2a3d%27%3EZ%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{up}assets/site.css">
<link rel="stylesheet" href="{up}assets/graph.css">
{extra_head}<link rel="stylesheet" href="{up}assets/themes.css">
<script src="{up}assets/site.js"></script>
</head>
<body>
<nav class="site"><div class="row">
<a class="brand" href="{up}index.html">gen-z-developers<span>.sgit.ai</span></a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>
<div class="nav-items">{nav}</div>
<div class="nav-tools"><div class="theme-pick"></div><span class="ver">site <a href="{up}admin/versions.html" title="Site release history">{VERSION}</a></span></div>
</div></nav>
<main><div class="inner{" wide" if wide else ""}">
{crumb}
{body}
</div></main>
<footer class="site"><div class="row">
<span>Generation Z Developers, by Dinis Cruz. The 2018 text is Creative Commons BY 4.0, as Dinis decided on 18 October 2026: see <a href="{up}v1/versions/index.html#licence">the licence note</a>. Everything else on this site is CC BY 4.0; code under the repository licence.</span>
<span>Part of <a href="https://sgit.ai">sgit.ai</a> &middot; <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers">GitHub</a> &middot; <a href="{up}vault/index.html">the working vault</a> &middot; <a href="{up}admin/versions.html">release history</a> &middot; <a href="{up}llms.txt">llms.txt</a></span>
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
    """The book as parts and chapters. PUBLISHED chapters are the ones the 2018 Hugo layouts put in the Leanpub build
    and the print PDF (layouts/book/leanpub.html: `where .Pages.ByWeight ".Params.status" "==" "content"`), in that
    order: parts by weight, chapters by weight then title. Everything else is a DRAFT: a chapter with text that was
    never published (status draft or unset) or an OUTLINE (a title and "Topics to cover and ideas"). The 2018 site's
    draft/ folders and the leanpub-with-draft-chapters layout kept them apart the same way."""
    print_toc = json.loads((ROOT / "admin/content/book/print-toc.json").read_text(encoding="utf-8"))
    print_page = {e["file"]: e["page"] for e in print_toc["entries"] if e.get("file")}
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
            published = status == "content"
            weight = fm_get(fm, "weight")
            weight = int(weight) if weight.isdigit() else 999
            kind = "published" if published else ("outline" if outline else "draft")
            group = {"published": 0, "draft": 1, "outline": 2}[kind]
            chapters.append({
                "file": rel, "slug": slugify(f.stem), "title": title, "title_note": title_note, "status": status,
                "outline": outline, "published": published, "kind": kind, "print_page": print_page.get(rel),
                "weight": weight, "group": group, "body": body.strip(),
                "words": len(re.findall(r"\w+", body)), "sha": sha(f.read_text(encoding="utf-8")),
                "what": fm_get(fm, "what"), "task": fm_get(fm, "task"), "price": fm_get(fm, "price"),
            })
        chapters.sort(key=lambda c: (c["group"], c["weight"], c["title"].lower()))
        parts.append({"dir": d, "slug": pslug, "title": ptitle, "weight": pweight, "intro": pbody.strip(),
                      "print_page": print_page.get(d + "/_index.md"),
                      "chapters": chapters, "sha": sha(idx.read_text(encoding="utf-8")) if idx.exists() else None})
    parts.sort(key=lambda p: p["weight"])
    # the front matter page the print edition opened with: the GitHub issues page (content/_manuscript/github-issues.md)
    gi = CONTENT / "_manuscript/github-issues.md"
    gfm, gbody = frontmatter(gi.read_text(encoding="utf-8"))
    front = {"file": "_manuscript/github-issues.md", "slug": "github-issues", "title": "GitHub Issues", "body": gbody.strip(),
             "words": len(re.findall(r"\w+", gbody)), "sha": sha(gi.read_text(encoding="utf-8")), "print_page": print_page.get("_manuscript/github-issues.md")}
    n = 0
    for p in parts:
        for c in p["chapters"]:
            if c["published"]:
                n += 1
                c["number"] = n
            else:
                c["number"] = None
    return parts, front


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
    k = c["kind"]
    if k == "published":
        pg = f", p. {c['print_page']}" if c.get("print_page") else ""
        return f'<span class="badge written" title="In the Leanpub build and the print PDF">published{esc(pg)}</span>'
    if k == "draft":
        return '<span class="badge draft" title="Text the 2018 build left out (status draft)">draft</span>'
    return '<span class="badge outline" title="A title and &quot;Topics to cover and ideas&quot;">outline</span>'


# ---- the book as blocks, for the reader (read/) --------------------------------------------------------------
class _TopLevel(HTMLParser):
    """Splits rendered HTML into its top-level elements, each a block the reader can address, fold and comment on."""
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.depth = 0
        self.starts = []
        self.blocks = []
        self.src = ""
    def _pos(self):
        line, col = self.getpos()
        return sum(len(l) + 1 for l in self.src.split("\n")[:line - 1]) + col
    def handle_starttag(self, tag, attrs):
        if tag in ("img", "br", "hr"):
            if self.depth == 0:
                self.starts.append(self._pos()); self._close_at(self._pos() + len(self.get_starttag_text()))
            return
        if self.depth == 0:
            self.starts.append(self._pos())
        self.depth += 1
    def handle_startendtag(self, tag, attrs):
        if self.depth == 0:
            self.starts.append(self._pos()); self._close_at(self._pos() + len(self.get_starttag_text()))
    def handle_endtag(self, tag):
        if tag in ("img", "br", "hr"):
            return
        self.depth -= 1
        if self.depth == 0:
            self._close_at(self._pos() + len(tag) + 3)
    def _close_at(self, end):
        start = self.starts.pop()
        self.blocks.append(self.src[start:end])
    def split(self, html_text):
        self.src = html_text
        self.feed(html_text)
        return [b for b in self.blocks if b.strip()]


STOP = set("""the a an and or of to in on for with by from as at is are was were be been it its this that these those you your
we our they their he she his her them us i my me not no yes if then than so but can will would should could may might
have has had do does did done just also very more most some any all each every one two three about into over under out up
down what which who whom when where why how here there now then again only even still too same other another such own
into onto off per via like new old big small good bad great many much few lot lots way ways thing things make makes made
use used using get got go going come see look need needs want time year years day days part parts first last next book
chapter chapters code example examples""".split())


CAP_FORMS, LOW_FORMS = Counter(), Counter()


def _tokens(body):
    text = re.sub(r"```.*?```", " ", body, flags=re.S)
    text = re.sub(r"!\[.*?\]\(.*?\)|\(https?://[^)]*\)|`[^`]*`", " ", text)
    return re.findall(r"\b[A-Za-z][A-Za-z0-9+#.-]{2,}\b", text)


def terms_of(body):
    """The proper nouns and technical names a chapter uses: the terms it shares with other chapters. A capitalised
    word counts as a name when, across the whole book, it is written with a capital at least as often as without
    (so "Docker" survives `docker run`, and "Although" at a sentence start does not); a name with an inner capital,
    a digit or in all caps (GitHub, AWS, Web2) counts from one use, any other from two."""
    caps = Counter(w for w in _tokens(body) if (w[0].isupper() or any(ch.isupper() for ch in w[1:])) and w.lower() not in STOP)
    out = {}
    for w, n in caps.items():
        k = w.lower()
        if LOW_FORMS[k] and CAP_FORMS[k] <= 2 * LOW_FORMS[k]:
            continue  # written in lower case about as often: an ordinary word at a sentence start
        special = any(ch.isupper() for ch in w[1:]) or any(ch.isdigit() for ch in w)
        if n >= 2 or (special and len(w) >= 3):
            out[k] = out.get(k, 0) + n
    return out


def relate(chapters):
    """Chapters that share terms, as edges labelled with the terms shared; a term common to more than 40% of the
    chapters says nothing and is dropped."""
    for c in chapters:
        for w in _tokens(c["body"]):
            (CAP_FORMS if w[0].isupper() else LOW_FORMS)[w.lower()] += 1
    terms = {c["slug"]: terms_of(c["body"]) for c in chapters}
    df = Counter(t for ts in terms.values() for t in ts)
    limit = max(3, int(0.4 * len(chapters)))
    keep = {t for t, n in df.items() if n <= limit}
    rel = {}
    for a in chapters:
        ta = set(terms[a["slug"]]) & keep
        edges = []
        for b in chapters:
            if b is a:
                continue
            shared = ta & set(terms[b["slug"]])
            if shared:
                weight = sum(min(terms[a["slug"]][t], terms[b["slug"]][t]) for t in shared)
                edges.append({"slug": b["slug"], "shared": sorted(shared, key=lambda t: -(terms[a["slug"]][t] + terms[b["slug"]][t]))[:6], "n": len(shared), "w": weight})
        edges.sort(key=lambda e: (-e["n"], -e["w"]))
        rel[a["slug"]] = edges[:6]
    return rel, {s: sorted(set(t) & keep, key=lambda x: -t[x])[:12] for s, t in terms.items()}


def build_book(parts, front, map_rows):
    manifest = {"version": "v1.0.0", "site": VERSION, "source": {"repository": SOURCE_REPO, "commit": SOURCE_COMMIT},
                "what": "The hash of every chapter's markdown (v1/content/) and of the <main> it rendered; validate.js "
                        "refuses a page that no longer matches its markdown, or markdown that was edited behind its page.",
                "chapters": []}
    flat = [(p, c) for p in parts for c in p["chapters"]]
    pub = [(p, c) for p, c in flat if c["published"]]
    drafts = [(p, c) for p, c in flat if not c["published"]]
    by_file = {r["file"]: r for r in map_rows}
    n_draft = sum(1 for _, c in drafts if c["kind"] == "draft")
    n_outline = sum(1 for _, c in drafts if c["kind"] == "outline")
    pub_words = sum(c["words"] for _, c in pub)

    def nav_for(seq, i):
        prev = seq[i - 1] if i > 0 else None
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        pn = '<div class="prevnext">'
        pn += (f'<a href="../{prev[0]["slug"]}/{prev[1]["slug"]}.html">&larr; {esc(prev[1]["title"])}</a>' if prev else "<span></span>")
        pn += (f'<a href="../{nxt[0]["slug"]}/{nxt[1]["slug"]}.html">{esc(nxt[1]["title"])} &rarr;</a>' if nxt else "<span></span>")
        return pn + "</div>"

    # one page per chapter: the published ones walk the published sequence, the drafts walk the drafts
    for seq, label in ((pub, "published"), (drafts, "drafts")):
        for i, (p, c) in enumerate(seq):
            rel = chapter_url(c, p)
            up = up_for(rel)
            body_html = md(rebase_images(c["body"], "../../"))
            row = by_file.get(c["file"])
            answers = ""
            if row and row["articles"]:
                answers = ('<p class="small dim">Answered since, on the newsroom: ' + ", ".join(
                    f'<a href="{a["url"]}">{esc(a["title"])}</a>' for a in row["articles"]) + f'. <a href="{up}map/index.html#{slugify(c["file"])}">The map row</a>.</p>')
            elif row:
                answers = f'<p class="small dim">No newsroom article answers it yet. <a href="{up}map/index.html#{slugify(c["file"])}">The map row</a>.</p>'
            note = ""
            if c["kind"] == "outline":
                note = ('<div class="outline-note">In 2018 this was an outline: a title and "Topics to cover and ideas". It was never in the published book, '
                        'and it is shown exactly as it was left. The second edition fills it from the articles the map names.</div>')
            elif c["kind"] == "draft":
                note = ('<div class="outline-note">A draft: text that was in the repository but not in the published book (the 2018 build took only '
                        'chapters marked <code>status: content</code>). Shown exactly as it was left.</div>')
            if c["title_note"]:
                note += f'<p class="small dim">{esc(c["title_note"])}</p>'
            mvp = ""
            if c["what"] or c["task"]:
                mvp = '<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{esc(v)}</dd>" for k, v in (("What", c["what"]), ("Task", c["task"]), ("Price", c["price"])) if v) + "</dl>"
            where = (f'chapter {c["number"]} of {len(pub)} in the published book' if c["published"] else f'draft {i + 1} of {len(drafts)}, not in the published book')
            main = (f'<article class="chapter"><p class="small dim">{esc(p["title"])} &middot; {where} &middot; {badge(c)} '
                    f'<span class="badge frozen">v1.0.0, 2018, frozen</span> &middot; {c["words"]:,} words &middot; '
                    f'<a href="{SOURCE_REPO}/blob/{SOURCE_COMMIT}/content/{c["file"]}">the 2018 file</a> &middot; <a href="{up}read/index.html#{c["slug"]}">read and review</a></p>'
                    f'<h1>{esc(c["title"])}</h1>{note}{mvp}<div class="body">{body_html}</div>{answers}{nav_for(seq, i)}</article>')
            page(rel, c["title"], main, f"{c['title']}, {'a chapter' if c['published'] else 'a draft'} of Generation Z Developers (2018), as released.",
                 crumbs=(("The book", "v1/book/index.html"), (p["title"], f"v1/book/index.html#{p['slug']}"), (c["title"], rel)))
            manifest["chapters"].append({"file": c["file"], "page": rel, "title": c["title"], "part": p["title"], "kind": c["kind"],
                                         "number": c["number"], "print_page": c["print_page"], "words": c["words"],
                                         "markdown_sha256": c["sha"], "main_sha256": sha(main)})

    # the front matter page: GitHub Issues, as the print edition opened
    fmain = (f'<article class="chapter"><p class="small dim">Front matter &middot; <span class="badge written">published, p. {front["print_page"]}</span> '
             f'<span class="badge frozen">v1.0.0, 2018, frozen</span> &middot; {front["words"]} words &middot; <a href="{SOURCE_REPO}/blob/{SOURCE_COMMIT}/content/{front["file"]}">the 2018 file</a></p>'
             f'<h1>{esc(front["title"])}</h1><div class="body">{md(front["body"])}</div>'
             f'<p class="small dim">In the print edition this page listed the five issues labelled <code>show-in-book</code> as of 8 October 2018 (#2 to #6). '
             f'<a href="../../contributors/index.html">The contributors page</a> has every issue, pull request and commit of the first edition.</p>'
             f'<div class="prevnext"><span></span><a href="{pub[0][0]["slug"]}/{pub[0][1]["slug"]}.html">{esc(pub[0][1]["title"])} &rarr;</a></div></article>')
    page("v1/book/github-issues.html", front["title"], fmain, "The front-matter page of the 2018 print edition: the GitHub issues a reader could help with.",
         crumbs=(("The book", "v1/book/index.html"), (front["title"], "v1/book/github-issues.html")))
    manifest["chapters"].append({"file": front["file"], "page": "v1/book/github-issues.html", "title": front["title"], "part": "Front matter", "kind": "published",
                                 "number": 0, "print_page": front["print_page"], "words": front["words"], "markdown_sha256": front["sha"], "main_sha256": sha(fmain)})

    # the table of contents: the book as published, then the drafts
    toc_pub, toc_dr = [], []
    for pi, p in enumerate(parts):
        pc = [c for c in p["chapters"] if c["published"]]
        dc = [c for c in p["chapters"] if not c["published"]]
        plain = re.sub(r"\s+", " ", re.sub(r"!\[.*?\]\(.*?\)", "", re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", p["intro"]))).strip()
        intro = f'<p class="small dim">{esc(plain[:220])}&hellip;</p>' if len(plain) > 40 else ""
        if pc:
            items = "".join(f'<li><a href="{p["slug"]}/{c["slug"]}.html">{esc(c["title"])}</a> <span class="w">p. {c["print_page"]} &middot; {c["words"]:,} words</span></li>' for c in pc)
            toc_pub.append(f'<li id="{p["slug"]}"><div class="part"><span class="n">{pi + 1}</span>{esc(p["title"])} '
                           f'<span class="w">{len(pc)} chapters{", from p. " + str(p["print_page"]) if p["print_page"] else ""}</span></div>{intro}<ol>{items}</ol></li>')
        if dc:
            items = "".join(f'<li><a href="{p["slug"]}/{c["slug"]}.html">{esc(c["title"])}</a> {badge(c)}<span class="w">{c["words"]:,} words</span></li>' for c in dc)
            toc_dr.append(f'<li id="drafts-{p["slug"]}"><div class="part">{esc(p["title"])} <span class="w">{sum(1 for c in dc if c["kind"] == "draft")} drafts, {sum(1 for c in dc if c["kind"] == "outline")} outlines</span></div>'
                          + (intro if not pc else "") + f'<ol>{items}</ol></li>')
    fe = FIRST_EDITION
    body = f"""<div class="toc-head"><a href="../generation-z-print-ready.pdf"><img class="thumb" src="../images/title_page.png" alt="The cover of Gen Z Developers, early release, September 2018" width="150" height="227"></a><div>
<h1>Generation Z Developers <span class="badge frozen">v1.0.0 &middot; 2018 &middot; frozen</span></h1>
<p class="lede">Key concepts and ideas for the next generation of developers. The first edition as published: the {len(pub)} chapters of the print edition (139 pages, 30 September 2018) and the Leanpub build of 8 October 2018. This is the official version this repository holds; nothing in it changes. <a href="../versions/index.html">The versions page</a> records it, and will show the delta to the next one.</p>
<p><span class="stat"><b>{len(pub)}</b><span>published chapters</span></span> <span class="stat"><b>{pub_words:,}</b><span>words published</span></span> <span class="stat"><b>139</b><span>print pages</span></span> <span class="stat"><b>{n_draft}</b><span>drafts</span></span> <span class="stat"><b>{n_outline}</b><span>outlines</span></span></p>
<p><a href="../../read/index.html">Read and review it</a> &middot; <a href="single.html">on one page</a> &middot; <a href="../generation-z-print-ready.pdf">the print PDF</a> &middot; <a href="../versions/v1.0.0.md">the frozen markdown</a> &middot; <a href="drafts.html">the drafts on one page</a> &middot; <a href="../../map/index.html">the map to the newsroom articles</a></p>
<p class="small">Where the first edition lives: <a href="{fe["amazon"]["url"]}">the paperback on Amazon</a> ({fe["amazon"]["pages"]} pages, published {fe["amazon"]["published"]}, ISBN-10 {fe["amazon"]["isbn10"]}) &middot; <a href="{fe["leanpub"]["url"]}">Leanpub</a> ({fe["leanpub"]["price"]}; {fe["leanpub"]["complete"]} complete, {fe["leanpub"]["readers"]} readers, {fe["leanpub"]["words"]:,} words) &middot; <a href="{SOURCE_REPO}">the source on GitHub</a>.</p>
</div></div>
<h2 id="published">The book as published</h2>
<div class="note">What the 2018 build published is a rule in the repository's Hugo layouts: a chapter went into the Leanpub book and the print PDF only if its front matter said <code>status: content</code>, parts by weight, chapters by weight then title. These {len(pub)} chapters, in this order, are the print edition's table of contents, with its page numbers. The front matter was <a href="github-issues.html">a page of GitHub issues to help with</a>.</div>
<ul class="toc">{"".join(toc_pub)}</ul>
<h2 id="drafts">The drafts: what was in the repository but not in the book</h2>
<div class="note warn">{n_draft} draft chapters with text and {n_outline} outlines (a title and "Topics to cover and ideas") never reached the published book. They are kept exactly as they were left, because the second edition starts from them, and <a href="../../map/index.html">the map</a> says which newsroom article has since answered each. Nothing here is the author's finished word: it is the ideas he meant to come back to.</div>
<ul class="toc">{"".join(toc_dr)}</ul>
"""
    page("v1/book/index.html", "The book, v1.0.0 (2018)", body,
         "Generation Z Developers, the 2018 first edition as published, chapter by chapter, and the drafts it left out.", crumbs=(("The book", "v1/book/index.html"),))

    # the published book on one page, and the frozen markdown it is a projection of; the drafts on their own page
    frozen = [f"# Generation Z Developers\n\n*Key concepts and ideas for the next generation of developers. Dinis Cruz, 2018. "
              f"Version v1.0.0: the first edition as published, the {len(pub)} chapters of the print edition and the Leanpub build, "
              f"frozen from {SOURCE_REPO} at {SOURCE_COMMIT[:9]}. The drafts the build left out are not part of this version; they are in v1/book/drafts.md.*\n",
              f"\n# Front matter\n\n## {front['title']}\n\n*Published, p. {front['print_page']}, {front['file']}.*\n\n" + front["body"] + "\n"]
    single = ['<h1>Generation Z Developers <span class="badge frozen">v1.0.0 &middot; 2018 &middot; frozen</span></h1>'
              f'<p class="lede">The book as published, on one page, in the print edition\'s order. <a href="index.html">The table of contents</a> &middot; <a href="drafts.html">the drafts</a>.</p>'
              f'<h3 class="ch" id="github-issues">{esc(front["title"])}</h3><p class="meta">front matter, p. {front["print_page"]}</p><div class="body">{md(front["body"])}</div>']
    draft_md = [f"# Generation Z Developers: the drafts\n\n*What the 2018 repository held but the published book left out: {n_draft} draft chapters and {n_outline} outlines, "
                f"as they were left, from {SOURCE_REPO} at {SOURCE_COMMIT[:9]}. Not part of v1.0.0; the second edition's raw material.*\n"]
    dsingle = [f'<h1>The drafts <span class="badge draft">not in the published book</span></h1><p class="lede">{n_draft} draft chapters and {n_outline} outlines, as they were left in the 2018 repository, part by part. <a href="index.html">The table of contents</a> &middot; <a href="single.html">the published book</a>.</p>']
    pn = 0
    for p in parts:
        pc = [c for c in p["chapters"] if c["published"]]
        dc = [c for c in p["chapters"] if not c["published"]]
        if pc:
            pn += 1
            single.append(f'<h2 class="part" id="{p["slug"]}">Part {pn}: {esc(p["title"])}</h2>')
            frozen.append(f"\n# Part {pn}: {p['title']}\n")
            if p["intro"]:
                single.append(f'<div class="body">{md(rebase_images(p["intro"], "../"))}</div>')
                frozen.append(rebase_images(p["intro"], "") + "\n")
            for c in pc:
                single.append(f'<h3 class="ch" id="{c["slug"]}">{esc(c["title"])}</h3><p class="meta">chapter {c["number"]} &middot; p. {c["print_page"]} &middot; {c["words"]:,} words &middot; '
                              f'<a href="{p["slug"]}/{c["slug"]}.html">its own page</a></p><div class="body">{md(rebase_images(c["body"], "../"))}</div>')
                frozen.append(f"\n## {c['title']}\n\n*Chapter {c['number']}, p. {c['print_page']}, {c['words']} words, {c['file']}.*\n\n" + rebase_images(c["body"], "") + "\n")
        if dc:
            dsingle.append(f'<h2 class="part" id="{p["slug"]}">{esc(p["title"])}</h2>')
            draft_md.append(f"\n# {p['title']}\n")
            if not pc and p["intro"]:
                dsingle.append(f'<div class="body">{md(rebase_images(p["intro"], "../"))}</div>')
                draft_md.append(rebase_images(p["intro"], "") + "\n")
            for c in dc:
                dsingle.append(f'<h3 class="ch" id="{c["slug"]}">{esc(c["title"])}</h3><p class="meta">{badge(c)} {c["words"]:,} words &middot; '
                               f'<a href="{p["slug"]}/{c["slug"]}.html">its own page</a></p><div class="body">{md(rebase_images(c["body"], "../"))}</div>')
                draft_md.append(f"\n## {c['title']}\n\n*{c['kind'].capitalize()}, {c['words']} words, {c['file']}.*\n\n" + rebase_images(c["body"], "") + "\n")
    page("v1/book/single.html", "The book on one page, v1.0.0 (2018)", '<div class="single">' + "".join(single) + "</div>",
         "Generation Z Developers (2018), the first edition as published, on one page.", crumbs=(("The book", "v1/book/index.html"), ("On one page", "v1/book/single.html")))
    page("v1/book/drafts.html", "The drafts, v1 (2018)", '<div class="single">' + "".join(dsingle) + "</div>",
         "The drafts and outlines the 2018 build left out of Generation Z Developers, on one page.", crumbs=(("The book", "v1/book/index.html"), ("The drafts", "v1/book/drafts.html")))
    write("v1/book/drafts.md", rebase_links_md("\n".join(draft_md)))
    write("v1/book/manifest.json", json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    return "\n".join(frozen), flat, pub, drafts


def rebase_links_md(text):
    """Image links in an assembled markdown file under v1/book/, one folder below v1/."""
    return text.replace("](images/", "](../images/")


def build_bookjson(parts, front, flat, map_rows):
    """v1/book/book.json: the book as data for the reader (read/): parts, chapters, each chapter as blocks the reader
    can fold and comment on, the newsroom articles that answer it, and the chapters it shares terms with."""
    by_file = {r["file"]: r for r in map_rows}
    chapters = []
    allc = [c for _, c in flat]
    rel, terms = relate(allc)
    for p, c in flat:
        html_text = md(rebase_images(c["body"], "../v1/"))
        blocks_ = _TopLevel().split(html_text)
        chapters.append({
            "slug": c["slug"], "part": p["slug"], "title": c["title"], "kind": c["kind"], "published": c["published"], "number": c["number"],
            "print_page": c["print_page"], "words": c["words"], "url": chapter_url(c, p), "file": c["file"],
            "articles": [{"title": a["title"], "url": a["url"]} for a in (by_file.get(c["file"], {}).get("articles") or [])],
            "gap": by_file.get(c["file"], {}).get("gap", ""),
            "terms": terms.get(c["slug"], []), "related": rel.get(c["slug"], []),
            "blocks": [{"id": f"{c['slug']}-{i + 1}", "html": b, "words": len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", b)))} for i, b in enumerate(blocks_)],
        })
    fb = _TopLevel().split(md(front["body"]))
    doc = {
        "what": "Generation Z Developers v1.0.0 as data for the reader at read/: parts, chapters (published, draft, outline) as blocks, "
                "the newsroom articles that answer each (from the map) and the chapters that share terms (computed). Generated by build.py.",
        "version": "v1.0.0", "site": VERSION, "title": "Generation Z Developers", "subtitle": "Key concepts and ideas for the next generation of developers",
        "print_pdf": "../v1/generation-z-print-ready.pdf", "cover": "../v1/images/title_page.png",
        "parts": [{"slug": p["slug"], "title": p["title"], "print_page": p["print_page"], "intro_html": md(rebase_images(p["intro"], "../v1/")) if p["intro"] else ""} for p in parts],
        "front": {"slug": "github-issues", "title": front["title"], "print_page": front["print_page"], "words": front["words"], "url": "v1/book/github-issues.html",
                  "blocks": [{"id": f"github-issues-{i + 1}", "html": b, "words": len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", b)))} for i, b in enumerate(fb)]},
        "chapters": chapters,
        "meter": {"start": 500, "symbol": "£", "pence_per_words": 250, "min_share": 0.1,
                  "rule": "A penny per 250 words, charged for the share of the chapter read (never less than 10% once opened); credit starts at £5 and can go below zero; nothing leaves the browser."},
    }
    write("v1/book/book.json", json.dumps(doc, ensure_ascii=False) + "\n")
    return doc


def build_read_v2(doc):
    """read/v2.html: the same reader over the release candidate (v2/book/book.json), its own store (genz.reader.v2)."""
    body = f"""<div id="reader" class="reader" data-book="../v2/book/book.json" data-store="genz.reader.v2">
<noscript><p class="note warn">The reader needs JavaScript. The candidate itself does not: <a href="../v2/book/index.html">the contents</a>, <a href="../v2/book/single.html">on one page</a>.</p></noscript>
<div class="rd-strip" id="rd-strip">
  <div class="rd-strip-left">
    <a class="rd-brand" href="../v2/book/index.html" title="The contents">{esc(doc["title"])} <span class="badge draft">{esc(doc["version"])}</span></a>
    <span class="rd-progress" id="rd-progress" title="Chapters read, of the candidate"></span>
  </div>
  <div class="rd-strip-right">
    <span class="rd-meter" id="rd-meter" title="The reading meter: a penny per 250 words read, from £5 of credit, kept in this browser"></span>
    <button class="rd-btn" id="rd-mode" type="button" aria-pressed="false" title="Review mode: states, comments, folds and the export, for Dinis and the editor">Review mode</button>
    <button class="rd-btn" id="rd-help" type="button" aria-expanded="false" aria-controls="rd-helpbox">?</button>
  </div>
</div>
<div class="rd-helpbox" id="rd-helpbox" hidden>
  <p><b>What this is.</b> Release candidate {esc(doc["version"])} of the second edition: {doc["chapters"]} chapters written from the ideas register, for Dinis to read and mark up. Not an official version. Keys: <kbd>j</kbd>/<kbd>k</kbd> next and previous chapter, <kbd>g</kbd> the graph, <kbd>f</kbd> focus.</p>
  <p><b>Review mode.</b> Each chapter has a state: unread, reading, read, to review, continue, signed off. Comment on any paragraph. Export the review as markdown or JSON for the vault's <code>reviews/</code> folder. Nothing here is sent anywhere unless you export it; this reader keeps its own store (<code>genz.reader.v2</code>), apart from the 2018 book's.</p>
  <p><b>The graph.</b> The open chapter in the middle, its part and neighbours, and the articles it was written from; the ideas it carries are listed under it, each a link to the register.</p>
</div>
<div class="rd-filters" id="rd-filters" hidden></div>
<div class="rd-main">
  <aside class="rd-toc" id="rd-toc" aria-label="Chapters"></aside>
  <section class="rd-content" id="rd-content" aria-live="polite"></section>
  <aside class="rd-graph" id="rd-graph" aria-label="The graph"></aside>
</div>
<div class="rd-export" id="rd-export" hidden></div>
</div>
"""
    page("read/v2.html", f"Read and review the second edition, {doc['version']}", body,
         f"Read release candidate {doc['version']} of {doc["title"]}, with the editor's desk: states, comments, folds, export.",
         crumbs=(("Read and review", "read/index.html"), ("The second edition", "read/v2.html")),
         extra_head='<link rel="stylesheet" href="../assets/reader.css">\n<script defer src="../assets/reader.js"></script>\n', wide=True)


def build_read(bookdoc):
    """read/: the reader and the editor's review desk. Content on the left, the graph on the right, the state of every
    chapter and comment kept in this browser, the reading meter after the newsroom's rules."""
    n_pub = sum(1 for c in bookdoc["chapters"] if c["published"])
    body = f"""<div id="reader" class="reader" data-book="../v1/book/book.json">
<noscript><p class="note warn">The reader needs JavaScript. The book itself does not: <a href="../v1/book/index.html">the table of contents</a>, <a href="../v1/book/single.html">on one page</a>, <a href="../v1/generation-z-print-ready.pdf">the print PDF</a>.</p></noscript>
<div class="rd-strip" id="rd-strip">
  <div class="rd-strip-left">
    <a class="rd-brand" href="../v1/book/index.html" title="The table of contents">Generation Z Developers <span class="badge frozen">v1.0.0</span></a>
    <span class="rd-progress" id="rd-progress" title="Chapters read, of the published book"></span>
  </div>
  <div class="rd-strip-right">
    <span class="rd-meter" id="rd-meter" title="The reading meter: a penny per 250 words read, from £5 of credit, kept in this browser"></span>
    <button class="rd-btn" id="rd-mode" type="button" aria-pressed="false" title="Review mode: states, comments, folds and the export, for the editor">Review mode</button>
    <button class="rd-btn" id="rd-help" type="button" aria-expanded="false" aria-controls="rd-helpbox">?</button>
  </div>
</div>
<div class="rd-helpbox" id="rd-helpbox" hidden>
  <p><b>Reading.</b> The {n_pub} published chapters in the print edition's order; the drafts and outlines after them, marked. Keys: <kbd>j</kbd>/<kbd>k</kbd> next and previous chapter, <kbd>g</kbd> the graph, <kbd>f</kbd> focus (folds everything but the open chapter).</p>
  <p><b>The meter.</b> A penny per 250 words, charged for the share of a chapter you actually scrolled through, never less than a tenth once opened; £5 of credit to start, allowed below zero, nothing blocked, nothing sent anywhere. The newsroom's rules, kept in this browser (<code>genz.reader.v1</code>).</p>
  <p><b>Review mode</b> (the editor's desk). Each chapter has a state: unread, reading, read, to review, continue, signed off. Comment on any paragraph. Filter the book to one state and fold the rest. Export your review as markdown or JSON for the vault's <code>reviews/</code> folder, or import one. Nothing here is sent anywhere unless you export it.</p>
  <p><b>The graph.</b> The open chapter in the middle; its part, the chapters before and after, the chapters it shares terms with (the terms on the edge), and the newsroom articles that have since answered it. Your paragraphs run along the bottom, one bar each: comments and reading colour them. Click a node to go there; the whole-book view shows every chapter by part.</p>
</div>
<div class="rd-filters" id="rd-filters" hidden></div>
<div class="rd-main">
  <aside class="rd-toc" id="rd-toc" aria-label="Chapters"></aside>
  <section class="rd-content" id="rd-content" aria-live="polite"></section>
  <aside class="rd-graph" id="rd-graph" aria-label="The graph"></aside>
</div>
<div class="rd-export" id="rd-export" hidden></div>
</div>
"""
    page("read/index.html", "Read and review", body,
         "Read Generation Z Developers (2018) with the graph beside it; the editor's desk to mark, comment, fold and export a review.",
         crumbs=(("Read and review", "read/index.html"),),
         extra_head='<link rel="stylesheet" href="../assets/reader.css">\n<script defer src="../assets/reader.js"></script>\n', wide=True)


def build_contributors():
    d = json.loads((ROOT / "admin/content/contributors.json").read_text(encoding="utf-8"))
    t = d["totals"]
    rows = []
    for p in d["people"]:
        login = f'<a href="https://github.com/{esc(p["login"])}">@{esc(p["login"])}</a>' if p["login"] else ""
        chapters = ", ".join(esc(ch.rsplit("/", 1)[-1][:-3]) for ch in p["chapters"][:8]) + (f" and {len(p['chapters']) - 8} more" if len(p["chapters"]) > 8 else "")
        prs = "; ".join(f'<a href="{esc(x["url"])}">#{x["number"]}</a> {esc(x["title"])} ({x["state"]})' for x in p["pr_titles"]) or ""
        credit = ", ".join(p["credited_in_changelog"])
        rows.append(f'<tr><td><b>{esc(p["name"])}</b><br>{login}{" &middot; <span class=small>" + esc(p["role"]) + "</span>" if p["role"] == "author" else ""}</td>'
                    f'<td>{p["commits"]}{" (+" + str(p["merges"]) + " merges)" if p["merges"] else ""}<br><span class="small dim">{p["first"] or ""}{" to " + p["last"] if p["last"] and p["last"] != p["first"] else ""}</span></td>'
                    f'<td>+{p["lines_added"]:,} / &minus;{p["lines_deleted"]:,}<br><span class="small dim">{p["chapters_count"]} chapter files</span></td>'
                    f'<td>{p["prs_merged"]} of {p["prs_opened"]}<br><span class="small dim">{prs}</span></td><td>{p["issues_opened"]}</td><td>{p["comments"]}</td>'
                    f'<td class="small">{chapters}{"<br><span class=dim>credited in " + esc(credit) + "</span>" if credit else ""}</td></tr>')
    # the timeline: one series (commits a month), one hue, thin bars, a table beside it
    have = {m["month"]: m for m in d["timeline"]}
    months = sorted(have)
    y0, m0 = map(int, months[0].split("-")); y1, m1 = map(int, months[-1].split("-"))
    tl = []
    while (y0, m0) <= (y1, m1):
        k = f"{y0:04d}-{m0:02d}"; tl.append(have.get(k, {"month": k, "commits": 0, "issues": 0, "prs": 0}))
        m0 += 1
        if m0 > 12: m0 = 1; y0 += 1
    mx = max(m["commits"] for m in tl) or 1
    W, H, bw = 760, 160, max(4, min(18, 740 // max(1, len(tl)) - 2))
    every = max(1, -(-len(tl) // 9))
    bars = "".join(
        f'<rect x="{10 + i * (bw + 2)}" y="{H - 24 - round((H - 40) * m["commits"] / mx)}" width="{bw}" height="{round((H - 40) * m["commits"] / mx)}" rx="2" fill="#0f766e"><title>{m["month"]}: {m["commits"]} commits, {m["issues"]} issues, {m["prs"]} pull requests</title></rect>'
        + (f'<text x="{10 + i * (bw + 2) + bw / 2}" y="{H - 8}" font-size="9" text-anchor="middle" fill="#5c5f66">{m["month"][2:]}</text>' if (i % every == 0) else "")
        for i, m in enumerate(tl))
    svg = (f'<svg class="tl" viewBox="0 0 {W} {H}" role="img" aria-label="Commits a month, {tl[0]["month"]} to {tl[-1]["month"]}"><text x="10" y="14" font-size="11" fill="#5c5f66">Commits a month (the tallest bar is {mx})</text>{bars}</svg>')
    tl_rows = "".join(f'<tr><td>{m["month"]}</td><td>{m["commits"]}</td><td>{m["issues"]}</td><td>{m["prs"]}</td></tr>' for m in tl)
    labels = ", ".join(f'<code>{esc(n)}</code> {k}' for n, k in d["labels"])
    sib = "".join(f'<li><a href="{esc(i["url"])}">#{i["number"]}</a> {esc(i["title"])} <span class="small dim">({i["state"]})</span></li>' for i in d["show_in_book"])
    prs = "".join(f'<tr><td><a href="{esc(p["url"])}">#{p["number"]}</a></td><td>{esc(p["title"])}</td><td>{esc(p["by"])}</td><td>{p["state"]}</td><td>{p["merged"] or p["date"]}</td></tr>' for p in d["pull_requests"])
    iss = "".join(f'<tr><td><a href="{esc(i["url"])}">#{i["number"]}</a></td><td>{esc(i["title"])}</td><td>{esc(i["by"])}</td><td>{", ".join(esc(l) for l in i["labels"])}</td><td>{i["state"]}</td><td>{i["date"]}</td><td>{i["comments"]}</td></tr>' for i in d["issues"])
    r = d["repository"]
    body = f"""<h1>The contributors to the first edition</h1>
<p class="lede">The first edition asked for help through GitHub issues and pull requests, and got it: before any second edition, {t["contributors"]} people besides the author had committed fixes, opened pull requests, raised issues or commented, on a repository that {r["stars"]} people starred and {r["forks"]} forked. This page is the record, from the repository's git history and its GitHub issues, read on 18 October 2026. The second edition credits them, with their permission.</p>
<p><span class="stat"><b>{t["contributors"]}</b><span>contributors</span></span> <span class="stat"><b>{t["commits"]}</b><span>commits</span></span> <span class="stat"><b>{t["commits_by_contributors"]}</b><span>by contributors</span></span> <span class="stat"><b>{t["pull_requests_merged"]}</b><span>of {t["pull_requests"]} PRs merged</span></span> <span class="stat"><b>{t["issues"]}</b><span>issues ({t["issues_open"]} open)</span></span> <span class="stat"><b>{t["comments"]}</b><span>comments</span></span> <span class="stat"><b>{t["chapters_touched_by_contributors"]}</b><span>chapter files touched by others</span></span></p>
<h2>When</h2>
<p class="small dim">Commits from {t["first_commit"]} to {t["last_commit"]}; issues and pull requests from {t["first_issue"]} to {t["last_issue"]}. By year: {", ".join(f"{y}: {n}" for y, n in d["by_year"].items())}. The book was written in 2018; the contributions came in from September 2018, the month it was released early, through 2020.</p>
{svg}
<details><summary>The same, as a table</summary><div class="tablewrap"><table><thead><tr><th>Month</th><th>Commits</th><th>Issues opened</th><th>Pull requests opened</th></tr></thead><tbody>{tl_rows}</tbody></table></div></details>
<h2>Who did what</h2>
<div class="tablewrap"><table class="people"><thead><tr><th>Person</th><th>Commits</th><th>Lines</th><th>Pull requests merged</th><th>Issues</th><th>Comments</th><th>Chapter files touched</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="small dim">Lines are git's count across every file, including the generated ones the author committed. A pull request's commits are counted under the person who made them, so a contributor's commits and merged pull requests are the same work seen twice. Git author names were joined to GitHub logins by hand (<code>admin/build/gen_contributors.py</code>); the raw data is under <code>admin/content/github/</code>.</p>
<h2>What the issues asked for</h2>
<p>Labels, as the author used them: {labels}. The print edition's front page listed the five labelled <code>show-in-book</code> as of 8 October 2018:</p>
<ul>{sib}</ul>
<h2>The pull requests</h2>
<div class="tablewrap"><table><thead><tr><th>#</th><th>Title</th><th>By</th><th>State</th><th>Date</th></tr></thead><tbody>{prs}</tbody></table></div>
<h2>The issues</h2>
<div class="tablewrap"><table><thead><tr><th>#</th><th>Title</th><th>By</th><th>Labels</th><th>State</th><th>Opened</th><th>Comments</th></tr></thead><tbody>{iss}</tbody></table></div>
<p class="small dim">The 2018 change log credits Mike Eriksson, Michael Chadwick and Claudio Camerino (v0.60) and Mark Regensberg and Sarah Cruz (v0.50) for content fixes and contributions. Repository: <a href="{esc(r["url"])}">{esc(r["url"].replace("https://github.com/", ""))}</a>, created {r["created"]}, last push {r["last_push"]}, licence file {esc(r["licence_file"] or "none")}.</p>
"""
    page("contributors/index.html", "The contributors", body, "Who contributed to the first edition of Generation Z Developers: commits, pull requests, issues and comments, from the 2018 repository.",
         crumbs=(("The contributors", "contributors/index.html"),), wide=True)
    return d


# ------------------------------------------------------------------ versions
def build_versions(frozen_md, parts, pub):
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
    cands = v.data.get("candidates") or []
    cand_html = ("</p><ul>" + "".join(f'<li><a href="../../v2/book/index.html"><b>{esc(c["version"])}</b></a>, {esc(c["date"])}, {esc(c.get("title", ""))}: {esc(c["what"])} '
                                        + (f'Frozen at <a href="../../{esc(c["frozen"])}">{esc(c["frozen"])}</a>, sha256 {c["text_sha256"][:12]}&hellip;' if c.get("text_sha256") else '<span class="st in-progress">being written</span>') + "</li>" for c in cands) + "</ul><p class=\"small\">") if cands else "None yet."
    body = f"""<h1>The versions of the book</h1>
<p class="lede">The rule this site is built on: <b>the repository holds the official versions; the vault holds the working versions.</b> A version moves from <a href="../../vault/index.html">the vault</a> into the repository when it is signed off, on top of the one before, and this page shows the delta between every two versions, block by block and word by word. There is one version so far.</p>
{table}
<p class="small dim">The table and the deltas are computed by the newsroom's <code>page_versions.py</code> (newsroom v0.12.113), copied into <code>admin/build/</code> as the brief asked rather than rewritten. Each version is frozen as one markdown file by the release that made it and never rewritten; the frozen file for v1.0.0 is <a href="v1.0.0.md">v1.0.0.md</a>, {words(chr(10).join(blocks(frozen_md))):,} words in {len(blocks(frozen_md)):,} blocks: the book as published, the {len(pub)} chapters of <a href="../generation-z-print-ready.pdf">the print PDF</a> (139 pages, sha256 {PDF_SHA[:12]}…) and the Leanpub build. The drafts the build left out are not part of any version; they are kept as <a href="../book/drafts.md">v1/book/drafts.md</a> and shown <a href="../book/drafts.html">on their own page</a>.</p>
{diffs}
<h2 id="candidates">Release candidates of the second edition</h2>
<p class="small">A candidate is a draft of the next edition written in this repository for Dinis to read and mark up (<a href="../../decisions/index.html#a-candidate-is-read-on-the-site-from-a-frozen-snapshot">decision 009</a>). It is frozen once, like a version, so that what was read cannot change; it is not official and nothing is published from it outside this site. {cand_html}</p>
<h2 id="record">The record</h2>
<div class="tablewrap"><table><thead><tr><th>Version</th><th>Date</th><th>Where</th><th>What it is</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2 id="source">Where v1.0.0 comes from</h2>
<ul>
<li>The repository <a href="{SOURCE_REPO}">DinisCruz/Book_Generation_Z_Developer</a> at commit <code>{SOURCE_COMMIT[:12]}</code> (1 March 2024, a README change; the content was last changed in October 2018). Its <code>content/</code> folder is copied verbatim to <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers/tree/dev/v1/content">v1/content/</a> and its <code>static/images/</code> to <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers/tree/dev/v1/images">v1/images/</a>: 138 markdown files, of which the Hugo layouts published the 28 marked <code>status: content</code>; 90 are outlines and the rest drafts.</li>
<li>The print-ready PDF, <a href="../generation-z-print-ready.pdf">v1/generation-z-print-ready.pdf</a>: 139 pages, the Leanpub build of 8 October 2018 made print-ready for the paperback, supplied by Dinis on 18 October 2026. Its table of contents is the published book's, and is kept as data in <code>admin/content/book/print-toc.json</code>.</li>
<li><a href="https://leanpub.com/generation-z">Leanpub</a>: "Key concepts and ideas for the next generation of developers", 60% complete, 136 pages, 30,695 words, last updated 8 October 2018, 465 readers (read 18 October 2026). The Leanpub build left the drafts and outlines out, as the print edition did; this site shows them apart from the book, because the second edition starts from them.</li>
<li>Amazon: <a href="{FIRST_EDITION["amazon"]["url"]}">Gen Z Developers</a>, the paperback: {FIRST_EDITION["amazon"]["pages"]} pages, published {FIRST_EDITION["amazon"]["published"]}, ISBN-10 {FIRST_EDITION["amazon"]["isbn10"]}, the early-release cover of September 2018 with its eight lines. That publication date is the date of v1.0.0; 8 October 2018 is the last change to the text, on Leanpub and in the repository.</li>
</ul>
<h2 id="leanpub">The 2018 change log, v0.30 to v0.60</h2>
<p class="small dim">As the book's own <code>_manuscript/change-log.md</code> records it. The contributors it names are to be credited in the second edition, with their permission.</p>
<div class="body">{changelog_html}</div>
<h2 id="licence">The licence</h2>
<p>The repository's licence file is Apache 2.0 (kept as <a href="../LICENSE-2018-repository.txt">v1/LICENSE-2018-repository.txt</a>). The book's Introduction says Creative Commons Attribution 4.0; its footer says Attribution-ShareAlike 4.0; the printed cover carries the CC BY mark. On 18 October 2026 Dinis decided the text is CC BY 4.0, as the cover and the Introduction say (<a href="../../decisions/index.html#the-2018-text-is-cc-by">decision 001</a>): the BY-SA line in the footer and the Apache 2.0 file in the 2018 repository are the exceptions, recorded here, not followed.</p>
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


# ------------------------------------------------------------------ articles
def render_articles(src, outdir, agent):
    """One stream of articles: admin/content/<src>/NN__<slug>.md to <outdir>/<slug>.html, plus the markdown twin
    <outdir>/<slug>.md an agent is pointed at. NN is the reading order and never changes; the slug is the address."""
    out = []
    for f in sorted((ROOT / "admin/content" / src).glob("[0-9][0-9]__*.md")):
        fm, text = frontmatter(f.read_text(encoding="utf-8"))
        slug = f.stem.split("__", 1)[1]
        a = {k: fm_get(fm, k) for k in ("title", "date", "author", "summary", "version", "tags", "status")}
        if a["status"] != "published":
            continue
        rel = f"{outdir}/{slug}.html"
        hook = a["title"].split(":")[0]
        if agent:
            kicker = "agent article"
            byline = (f'By <code>{esc(a["author"])}</code>, an agent of this site, in its own voice, about work it did. '
                      f'Decisions it quotes are attributed to Dinis by name; the editorial responsibility is Dinis&rsquo;s.')
        else:
            kicker = "article"
            byline = (f'By {esc(a["author"])}, co-written with this site&rsquo;s journalist, <code>gen-z.journalist</code>, in {esc(a["author"])}&rsquo;s voice; '
                      f'the editorial responsibility is {esc(a["author"])}&rsquo;s.')
        body = (f'<article class="doc"><p class="kicker">{kicker} &middot; {esc(a["date"])} &middot; site {esc(a["version"])} &middot; '
                f'<a href="{slug}.md">markdown</a></p><h1>{esc(a["title"])}</h1><p class="byline">{byline}</p>'
                f'<div class="src"><b>Abstract.</b> {esc(a["summary"])}</div>'
                f'<div class="body">{md(text)}</div></article>')
        page(rel, hook, body, a["summary"][:300], crumbs=(("Articles", "articles/index.html"), (hook, rel)))
        write(f"{outdir}/{slug}.md", f.read_text(encoding="utf-8"))
        out.append((rel, a))
    return out


def build_articles():
    """The two streams (decided by Dinis on 18 October 2026): articles co-written with Dinis, in Dinis's voice
    (admin/content/articles/ to articles/), and agent articles, one per significant body of work, written by the agent
    that did it, in its own voice (admin/content/agent-articles/ to agent-articles/). One index for both."""
    co = render_articles("articles", "articles", agent=False)
    ag = render_articles("agent-articles", "agent-articles", agent=True)

    def li(rel, a):
        title = a["title"].split(":", 1)
        by = f' &middot; <code>{esc(a["author"])}</code>' if rel.startswith("agent-articles/") else ""
        return (f'<li><a href="../{rel}"><b>{esc(title[0])}</b></a>: {esc(title[1].strip() if len(title) > 1 else "")}'
                f' <span class="small dim">({esc(a["date"])}, site {esc(a["version"])}{by})</span></li>')
    body = f"""<h1>Articles</h1>
<p class="lede">How the work on this book is communicated: as articles, in two streams. Each page links its markdown twin, which is the file to hand to an agent.</p>
<h2 id="co-written">Co-written with Dinis</h2>
<p class="small dim">In Dinis&rsquo;s voice, from Dinis&rsquo;s memos, written up with this site&rsquo;s journalist. They are the briefs: an idea, a task or a review researched, counted and written up before any role acts on it, ending with a brief a role can execute. The shape is the newsroom&rsquo;s (<a href="https://newsroom.sgit.ai/articles/how-the-voice-works.html">how the voice works</a>). Sources in <code>admin/content/articles/</code>.</p>
<ol class="articles">{"".join(li(r, a) for r, a in co)}</ol>
<h2 id="agents">By the agents</h2>
<p class="small dim">In the agent&rsquo;s own voice: every agent writes one when it has finished a significant body of work, a bigger version of a release note, with what it did, the flows, the changes, and what it leaves for the other roles. When it refers to a human decision it names who made it. Sources in <code>admin/content/agent-articles/</code>; the decisions they record are on <a href="../decisions/index.html">the decisions page</a>.</p>
<ol class="articles">{"".join(li(r, a) for r, a in ag) or "<li class='dim'>none yet</li>"}</ol>
<p class="small dim">The journalist&rsquo;s mandate is <a href="../team/journalist/index.html">its role</a>.</p>
"""
    page("articles/index.html", "Articles", body, "This site's articles: co-written with Dinis, and by the agents about their work.", crumbs=(("Articles", "articles/index.html"),))
    build_decisions()
    return co + ag


def build_decisions():
    """Dinis's decisions on how the book is made and published, one file each: admin/content/decisions/NNN__<slug>.md,
    numbered in the order made, never renumbered or deleted. Decisions on the book's text live in the vault with the
    text issues. Each file: '# title', then **Decided.**, **By.**, **Said.**, **Means.**, **Supersedes.**, **Recorded in.**"""
    rows, secs = [], []
    for f in sorted((ROOT / "admin/content/decisions").glob("[0-9][0-9][0-9]__*.md")):
        text = f.read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.M).group(1).strip()
        num, slug = f.stem.split("__", 1)
        decided = re.search(r"^\*\*Decided\.\*\*\s*(.+)$", text, re.M)
        rows.append(f'<tr><td><a href="#{slug}">{num}</a></td><td>{esc(decided.group(1) if decided else "")}</td><td>{esc(title)}</td></tr>')
        secs.append(f'<section id="{slug}"><h2>{num} &middot; {esc(title)}</h2>{md(text.split(chr(10), 1)[1])}</section>')
    body = f"""<h1>Decisions</h1>
<p class="lede">Dinis&rsquo;s decisions on how this book is made, versioned and published, one record each, in the order made. A decision is never deleted; a later one supersedes it and says so. Decisions on the book&rsquo;s text are kept in the vault, with the text issues.</p>
<div class="tablewrap"><table><thead><tr><th>#</th><th>Decided</th><th>Decision</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<div class="doc"><div class="body">{"".join(secs)}</div></div>
<p class="small dim">The sources are in <code>admin/content/decisions/</code>. The agent article that recorded each one is linked from it.</p>
"""
    page("decisions/index.html", "Decisions", body, "Dinis's decisions on how the book is made, versioned and published.", crumbs=(("Decisions", "decisions/index.html"),))


# ------------------------------------------------------------------ the newsroom, surveyed
def build_newsroom_survey():
    """admin/content/newsroom/survey.json: every newsroom article read and classified for the book (bring, content,
    context, skip) with the reason, the topics the book should cover and the articles that feed each, the concepts with
    the article that defines each, and the gaps. Written by the journalist's survey; rendered at map/newsroom.html for
    Dinis to read and decide. A decision on an article is his; the class is a proposal."""
    f = ROOT / "admin/content/newsroom/survey.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text(encoding="utf-8"))
    arts = d["articles"]
    by = {}
    for a in arts:
        by.setdefault(a["class"], []).append(a)
    url = lambda slug: f"https://newsroom.sgit.ai/articles/{slug}.html"
    title_of = {a["slug"]: a["title"].split(":")[0] for a in arts}
    link = lambda slug: f'<a href="{url(slug)}">{esc(title_of.get(slug, slug))}</a>'
    order = [("bring", "Bring: becomes, or seeds, material in the book"), ("content", "Content: a specific example, number, story or quote to take"),
             ("context", "Context: background for the agents writing the book"), ("skip", "Skip: not for this reader")]
    counts = " ".join(f'<span class="stat"><b>{len(by.get(k, []))}</b><span>{k}</span></span>' for k, _ in order)
    topics = "".join(f'<tr><td><b>{esc(t["title"])}</b><br><span class="small dim">{esc(t.get("why", ""))}</span></td>'
                     f'<td class="small">{", ".join(link(s) for s in t["articles"])}</td>'
                     f'<td class="small">{esc("; ".join(t.get("answers_2018", [])))}</td></tr>' for t in d["topics"])
    concepts = "".join(f'<tr><td><b>{esc(c["term"])}</b></td><td class="small">{esc(c["definition"])}</td><td class="small">{link(c["defined_in"])}</td></tr>' for c in d["concepts"])
    gaps = "".join(f"<li>{esc(g)}</li>" for g in d["gaps"])
    groups = ""
    for k, label in order:
        rows = "".join(f'<tr id="{esc(a["slug"])}"><td><a href="{url(a["slug"])}">{esc(a["title"].split(":")[0])}</a><br><span class="small dim">{esc(a.get("date", ""))}{" &middot; in the map" if a.get("in_map") else ""}</span></td>'
                       f'<td class="small">{esc(a.get("serves", ""))}</td><td class="small">{esc(a.get("why", ""))}</td></tr>'
                       for a in sorted(by.get(k, []), key=lambda a: a.get("rank", 999)))
        groups += (f'<h3 id="{k}">{esc(label)} ({len(by.get(k, []))})</h3><div class="tablewrap"><table class="map"><thead><tr><th>Article</th><th>Serves</th><th>Why</th></tr></thead>'
                   f'<tbody>{rows}</tbody></table></div>')
    body = f"""<h1>The newsroom, surveyed</h1>
<p class="lede">Every article on newsroom.sgit.ai, read for this book and given a proposed class, with the reason: what to bring, what content to take, what is background for the agents, and what to skip. Then the topics the second edition should cover, the concepts it should introduce, and the gaps no article covers yet. The classes are proposals; the decisions are Dinis's.</p>
<p>{counts} <span class="stat"><b>{len(arts)}</b><span>articles</span></span></p>
<p class="small dim">{esc(d.get("note", ""))} Counted on {esc(d.get("counted_on", ""))}. The data is <a href="../admin/content/newsroom/survey.json">admin/content/newsroom/survey.json</a>; the argument is in <a href="../articles/start-from-the-storyline.html">start from the storyline</a>.</p>
<h2 id="topics">The topics ({len(d["topics"])})</h2>
<div class="tablewrap"><table class="map"><thead><tr><th>Topic</th><th>Articles that feed it</th><th>2018 chapters it answers</th></tr></thead><tbody>{topics}</tbody></table></div>
<h2 id="concepts">The concepts ({len(d["concepts"])})</h2>
<div class="tablewrap"><table class="map"><thead><tr><th>Term</th><th>As the newsroom uses it</th><th>Defined in</th></tr></thead><tbody>{concepts}</tbody></table></div>
<h2 id="gaps">The gaps ({len(d["gaps"])})</h2>
<p class="small dim">What a newcomer needs that no article covers yet: each is a candidate for a new article first, then a chapter.</p>
<ul>{gaps}</ul>
<p class="small dim">What the second pass, over the articles imported from sgit.ai, found that fills some of them:</p>
<ul class="small">{"".join(f"<li>{esc(g)}</li>" for g in d.get("gaps_filled_by_imported", []))}</ul>
<h2 id="articles">Every article, by class</h2>
{groups}
"""
    page("map/newsroom.html", "The newsroom, surveyed", body, "Every newsroom article read for the book: bring, content, context or skip, the topics, the concepts and the gaps.",
         crumbs=(("The map", "map/index.html"), ("The newsroom, surveyed", "map/newsroom.html")), wide=True)
    return d


# ------------------------------------------------------------------ storyboards
SB_KINDS = {"cover", "scene", "evidence", "punchline", "spectrum", "map", "graph"}
SB_POSES = {"stand", "point", "wave", "arms-up", "shrug", "think", "sit"}
SB_MOODS = {"neutral", "happy", "excited", "calm", "worried", "sad", "surprised", "thinking", "confused", "determined"}
SB_SETTINGS = {"none", "office", "interview", "street", "night", "classroom"}
SB_PROPS = {"laptop", "desk", "book", "board", "phone", "sign"}
SB_HEAD = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Patrick+Hand&display=swap">\n')


def sb_tools(views):
    """The storyboard toolbar: the views (on a board's page), panels per row, animation, text under the panels, play in
    order, the filter and the keys. assets/storyboard.js wires it; what a viewer picks is kept in their browser only."""
    v = ('<span class="sb-views" role="group" aria-label="View">'
         '<button type="button" data-view="deck" title="One panel at a time (d)">Deck</button>'
         '<button type="button" data-view="grid" title="Every panel on one page (g)">Grid</button>'
         '<button type="button" data-view="script" title="The storyboard as text (t)">Script</button></span>') if views else ""
    cols = "".join(f'<option value="{n}">{n}</option>' for n in range(1, 7))
    keys = ("<kbd>d</kbd> <kbd>g</kbd> <kbd>t</kbd> views &middot; " if views else "") + \
        "<kbd>a</kbd> animation &middot; <kbd>x</kbd> text &middot; <kbd>+</kbd><kbd>&minus;</kbd> per row &middot; <kbd>/</kbd> filter &middot; <kbd>p</kbd> play" + \
        (" &middot; <kbd>&larr;</kbd><kbd>&rarr;</kbd> <kbd>n</kbd> notes <kbd>f</kbd> full screen" if views else "")
    return (f'<div class="sb-tools" role="toolbar" aria-label="How to view the panels">{v}'
            f'<label class="sb-for-grid">Per row <select class="sb-cols">{cols}</select></label>'
            '<label title="Panels play as they arrive (a)"><input type="checkbox" class="sb-anim"> Animation</label>'
            '<label class="sb-for-grid" title="Each panel\'s script under it (x)"><input type="checkbox" class="sb-showtext"> Text</label>'
            '<button type="button" class="sb-playall sb-for-grid" title="Play the panels one after another (p)">Play in order</button>'
            '<input type="search" class="sb-filter sb-for-list" placeholder="Filter: a word, a name, a mood, a kind" aria-label="Filter the panels">'
            f'<span class="sb-keys">{keys}</span></div>')


def build_storyboards():
    """Storyboards are data, drawn by assets/storyboard.js with Rough.js (vendored, MIT): admin/content/storyboards/cast.json
    and NN__<slug>.json, one storyboard each. The build checks every scene against the cast and the vocabulary the renderer
    knows, writes a swipe deck per storyboard and the cast sheet, and copies the JSON beside them for agents."""
    src = ROOT / "admin/content/storyboards"
    cast = json.loads((src / "cast.json").read_text(encoding="utf-8"))
    ids = {c["id"] for c in cast["characters"]}
    head = SB_HEAD + '<link rel="stylesheet" href="../assets/storyboard.css">\n'
    scripts = '<script src="../assets/vendor/rough-4.6.6.js"></script><script src="../assets/storyboard.js"></script>'
    boards = []
    for f in sorted(src.glob("[0-9][0-9]__*.json")):
        sb = json.loads(f.read_text(encoding="utf-8"))
        for i, sc in enumerate(sb["scenes"], 1):
            where = f"{f.name} scene {i}"
            if sc.get("kind", "scene") not in SB_KINDS:
                sys.exit(f"build: {where}: unknown kind {sc.get('kind')}")
            if sc.get("setting", "none") not in SB_SETTINGS:
                sys.exit(f"build: {where}: unknown setting {sc.get('setting')} (the renderer knows {', '.join(sorted(SB_SETTINGS))})")
            for pr in sc.get("props", []):
                if pr.get("kind") not in SB_PROPS:
                    sys.exit(f"build: {where}: unknown prop {pr.get('kind')} (the renderer knows {', '.join(sorted(SB_PROPS))})")
            for c in sc.get("cast", []):
                if c["who"] not in ids:
                    sys.exit(f"build: {where}: {c['who']} is not in the cast")
                if c.get("pose", "stand") not in SB_POSES or c.get("mood", "neutral") not in SB_MOODS:
                    sys.exit(f"build: {where}: unknown pose or mood for {c['who']}")
            if sc.get("kind") == "evidence" and not (sc.get("evidence", {}).get("quote") or sc.get("evidence", {}).get("bars")):
                sys.exit(f"build: {where}: evidence needs a quote or bars")
            if sb.get("quote_source") and not sc.get("not_a_quote"):
                # the Guide speaks the book's words: every quote card and Guide line must be in the source, word for word
                norm = lambda t: re.sub(r"\s+", " ", t.replace("**", "").replace("\u2019", "'").replace("\u2018", "'")).strip()
                text = norm((ROOT / sb["quote_source"]).read_text(encoding="utf-8"))
                said = [sc.get("evidence", {}).get("quote")] + [c.get("says") for c in sc.get("cast", []) if c["who"] == "guide"]
                for q in filter(None, said):
                    if norm(q) not in text:
                        sys.exit(f"build: {where}: \"{q[:60]}\" is not in {sb['quote_source']} word for word (mark the scene not_a_quote if it is not meant to be)")
        slug = sb["slug"]
        rel = f"storyboards/{slug}.html"
        payload = json.dumps({"storyboard": sb, "cast": cast}, ensure_ascii=False).replace("</", "<\\/")
        rows = "".join(f'<li><a href="#scene-{i}">{i}</a>. {esc(sc.get("caption") or sc.get("punchline") or sc.get("title") or "")}'
                       f' <span class="small dim">({esc(sc.get("kind", "scene"))}; {esc(sc.get("source", ""))})</span></li>' for i, sc in enumerate(sb["scenes"], 1))
        body = f"""<h1>{esc(sb["title"])}</h1>
<p class="lede">{esc(sb["subtitle"])}</p>
<p class="small dim">Status: {esc(sb["status"])} &middot; book {esc(sb["book_version"])} &middot; {esc(sb["by"])}. {esc(sb.get("rule", ""))}</p>
<div class="sb-viewer">{sb_tools(views=True)}
<div class="sb-deck" hidden><div class="sb-track"></div>
<div class="sb-bar"><button type="button" class="sb-prev" aria-label="Previous panel">&larr;</button><span class="sb-count"></span><button type="button" class="sb-next" aria-label="Next panel">&rarr;</button><button type="button" class="sb-replay" title="Play this panel (p)">&#9654; Play</button><button type="button" class="sb-notes-toggle" title="Notes (n)">Notes</button><button type="button" class="sb-full" title="Full screen (f)">Full screen</button></div>
<div class="sb-notes"></div></div>
<div class="sb-grid" hidden></div>
<div class="sb-script" hidden></div>
<script type="application/json" class="sb-data">{payload}</script></div>
<h2 id="panels">The panels</h2>
<ol class="small">{rows}</ol>
<p class="small dim">The data is <a href="{slug}.json">{slug}.json</a> and <a href="cast.json">cast.json</a>; the panels are drawn in your browser from it, by <code>assets/storyboard.js</code> with Rough.js. Nothing is an image file: change the JSON, rebuild, and every panel is redrawn.</p>
{scripts}
"""
        page(rel, sb["title"], body, sb["subtitle"], crumbs=(("Storyboards", "storyboards/index.html"), (sb["title"], rel)), extra_head=head, wide=True)
        write(f"storyboards/{slug}.json", f.read_text(encoding="utf-8"))
        boards.append((rel, sb))
    write("storyboards/cast.json", (src / "cast.json").read_text(encoding="utf-8"))
    sb_head = SB_HEAD + '<link rel="stylesheet" href="../assets/storyboard.css">\n'
    total = sum(len(sb["scenes"]) for _, sb in boards)
    payload = json.dumps({"boards": [{"href": rel[12:], "storyboard": sb} for rel, sb in boards], "cast": cast}, ensure_ascii=False).replace("</", "<\\/")
    body = f"""<h1>Every panel</h1>
<p class="lede">All {len(boards)} storyboards, {total} panels, on one page, in order: to see the book as a flow rather than one panel at a time. A click on a panel plays it; its number opens it in that storyboard's deck.</p>
<div class="sb-contact" data-view="grid">{sb_tools(views=False)}<script type="application/json" class="sb-data">{payload}</script></div>
{scripts}
"""
    page("storyboards/all.html", "Every panel", body, f"All {total} storyboard panels on one page, as a grid: filter, play, open in the deck.",
         crumbs=(("Storyboards", "storyboards/index.html"), ("Every panel", "storyboards/all.html")), extra_head=sb_head, wide=True)
    payload = json.dumps({"cast": cast}, ensure_ascii=False).replace("</", "<\\/")
    body = f"""<h1>The model sheet</h1>
<p class="lede">Every character in every mood and every pose, side by side, the way animators check a character is on model: a face that reads wrong here reads wrong in every panel it is in. Correct the drawing in <code>assets/storyboard.js</code> or the look in <code>cast.json</code>, rebuild, and every panel changes with it.</p>
<p class="small dim">Moods: {", ".join(sorted(SB_MOODS))}. Poses: {", ".join(sorted(SB_POSES))}.</p>
<div class="sb-sheet"><script type="application/json" class="sb-data">{payload}</script></div>
{scripts}
"""
    page("storyboards/model-sheet.html", "The model sheet", body, "Every storyboard character in every mood and pose, to check the drawing.",
         crumbs=(("Storyboards", "storyboards/index.html"), ("The model sheet", "storyboards/model-sheet.html")), extra_head=sb_head, wide=True)
    # ---- the index: the comic shelf. Text is written here; every panel, face and figure on it is drawn in the browser
    # from the same data as the decks (assets/storyboard.js, shelf()), so nothing on it is an image file and a corrected
    # panel corrects its thumbnail too. The grouping is data: admin/content/storyboards/shelves.json.
    shelves = json.loads((src / "shelves.json").read_text(encoding="utf-8"))
    by_slug = {sb["slug"]: (rel, sb) for rel, sb in boards}
    placed = [slug for sh in shelves["shelves"] for slug in sh["boards"]]
    for slug in placed:
        if slug not in by_slug:
            sys.exit(f"build: shelves.json names {slug}, which is not a storyboard")
    for slug in by_slug:
        if placed.count(slug) != 1:
            sys.exit(f"build: storyboard {slug} is on {placed.count(slug)} shelves in shelves.json; it must be on exactly one")
    if shelves["start"] not in by_slug:
        sys.exit(f"build: shelves.json starts with {shelves['start']}, which is not a storyboard")
    names = {c["id"]: c["name"] for c in cast["characters"]}
    number = {sb["slug"]: f.name[:2] for f in sorted(src.glob("[0-9][0-9]__*.json")) for sb in [json.loads(f.read_text(encoding="utf-8"))]}

    def faces_of(sb, k=4):
        count = {}
        for sc in sb["scenes"]:
            for c in sc.get("cast", []):
                count[c["who"]] = count.get(c["who"], 0) + 1
        return [w for w, _ in sorted(count.items(), key=lambda x: (-x[1], x[0]))[:k]]

    def faces_html(sb, cls="sbx-face"):
        return "".join(f'<svg class="{cls}" data-who="{esc(w)}" role="img" aria-label="{esc(names[w])}"><title>{esc(names[w])}</title></svg>' for w in faces_of(sb))

    def thumb(slug, i, cls="sbx-thumb"):
        return f'<svg class="{cls}" data-board="{esc(slug)}" data-scene="{i}" viewBox="0 0 1600 1000" role="img" aria-label="Panel {i + 1}"></svg>'

    def source_title(sb):
        q = sb.get("quote_source") or ""
        if q.startswith("admin/content/articles/") and (ROOT / q).exists():
            return fm_get(frontmatter((ROOT / q).read_text(encoding="utf-8"))[0], "title").split(":")[0]
        return ""

    def card(slug):
        rel, sb = by_slug[slug]
        href = rel[12:]
        strip = "".join(thumb(slug, i) for i in range(1, min(4, len(sb["scenes"]))))
        return (f'<article class="sbx-card"><a class="sbx-cover" href="{href}" aria-label="{esc(sb["title"])}: open the deck">{thumb(slug, 0)}'
                f'<span class="sbx-tag">{number[slug]}</span></a>'
                f'<a class="sbx-strip" href="{href}?view=grid" aria-label="{esc(sb["title"])}: every panel">{strip}</a>'
                f'<div class="sbx-body"><h3><a href="{href}">{esc(sb["title"])}</a></h3><p>{esc(sb["subtitle"])}</p>'
                f'<div class="sbx-meta"><span class="sbx-faces">{faces_html(sb)}</span><span>{len(sb["scenes"])} panels</span>'
                f'<span class="sbx-status sbx-{esc(sb["status"])}">{esc(sb["status"])}</span></div></div></article>')

    srel, ssb = by_slug[shelves["start"]]
    shref, sn = srel[12:], len(ssb["scenes"])
    st = source_title(ssb)
    start = (f'<section class="sbx-start" aria-labelledby="sbx-start-h"><p class="sbx-kicker">Start here</p><div class="sbx-start-grid">'
             f'<div><a class="sbx-cover sbx-big" href="{shref}" aria-label="{esc(ssb["title"])}: open the deck">{thumb(ssb["slug"], 0)}</a>'
             f'<div class="sbx-start-strip">{"".join(thumb(ssb["slug"], i) for i in range(1, min(4, sn)))}'
             f'<a class="sbx-more" href="{shref}?view=grid">+{max(0, sn - 4)} more</a></div></div>'
             f'<div class="sbx-start-text"><span class="sbx-tag sbx-tag-big">{number[ssb["slug"]]}</span>'
             f'<h2 id="sbx-start-h">{esc(ssb["title"])}</h2><p>{esc(ssb["subtitle"])}</p>'
             f'<div class="sbx-meta"><span class="sbx-faces">{faces_html(ssb, "sbx-face sbx-face-big")}</span>'
             f'<span>{sn} panels &middot; {esc(ssb["status"])}{" &middot; from the article &ldquo;" + esc(st) + "&rdquo;" if st else ""}</span></div>'
             f'<div class="sbx-actions"><a class="sbx-btn sbx-btn-go" href="{shref}?view=deck">&#9654; Play the deck</a>'
             f'<a class="sbx-btn" href="{shref}?view=grid">See all {sn}</a><a class="sbx-btn" href="{shref}?view=script">Read the script</a></div>'
             f'</div></div></section>')
    shelf_html = "".join(
        f'<section class="sbx-shelf" aria-labelledby="sbx-shelf-{k}"><div class="sbx-head"><h2 id="sbx-shelf-{k}">{esc(sh["title"])}</h2><p>{esc(sh["note"])}</p></div>'
        f'<div class="sbx-cards">{"".join(card(slug) for slug in sh["boards"])}</div></section>'
        for k, sh in enumerate(shelves["shelves"], 1))
    # how each character stands on the page: presentation only, the cast file says who they are
    stance = {"zara": ("wave", "happy"), "tomas": ("stand", "happy"), "priya": ("point", "happy"), "sam": ("stand", "calm"),
              "marta": ("arms-up", "excited"), "guide": ("wave", "happy"), "agent": ("wave", "happy")}
    cast_html = "".join(
        f'<figure class="sbx-person"><div class="sbx-bubble">&ldquo;{esc(c["line"])}&rdquo;</div>'
        f'<svg class="sbx-figure" data-who="{esc(c["id"])}" data-pose="{stance.get(c["id"], ("stand", "happy"))[0]}" data-mood="{stance.get(c["id"], ("stand", "happy"))[1]}" role="img" aria-label="{esc(c["name"])}"></svg>'
        f'<figcaption><b>{esc(c["name"])}</b><span>{esc(c["role"])}</span>'
        f'<details><summary>More</summary><dl><dt>Stands for</dt><dd>{esc(c["stands_for"])}</dd><dt>Personality</dt><dd>{esc(c["personality"])}</dd>'
        f'<dt>Wants</dt><dd>{esc(c["wants"])}</dd><dt>Fears</dt><dd>{esc(c["fears"])}</dd></dl></details></figcaption></figure>'
        for c in cast["characters"])
    total = sum(len(sb["scenes"]) for _, sb in boards)
    lineup_names = "".join(f"<span>{esc(c['name'])}</span>" for c in cast["characters"])
    payload = json.dumps({"cast": cast, "boards": {sb["slug"]: {"title": sb["title"], "scenes": sb["scenes"][:4]} for _, sb in boards},
                          "stance": stance}, ensure_ascii=False).replace("</", "<\\/")
    body = f"""<div class="sbx">
<section class="sbx-hero" aria-labelledby="sbx-h1">
<p class="sbx-count">{len(boards)} storyboards &middot; {total} panels &middot; {len(cast["characters"])} characters &middot; all drawn from data</p>
<h1 id="sbx-h1">The book, one panel at a time</h1>
<svg class="sbx-underline" aria-hidden="true" viewBox="0 0 620 22" preserveAspectRatio="none"><path d="M4 14 Q 160 4 310 12 T 616 8"></path></svg>
<p class="sbx-lede">Before a chapter is written, it is a storyboard: the punchline, the idea, the evidence and the people it is for. Flick through them on a tablet, see them all at once, or read them as a script.</p>
<div class="sbx-actions"><a class="sbx-btn sbx-btn-ink" href="{shref}">Start with {esc(ssb["title"].split(":")[0])} &rarr;</a><a class="sbx-btn sbx-btn-marker" href="all.html">Every panel on one page</a><a class="sbx-btn sbx-btn-line" href="#cast">Meet the cast</a></div>
<svg class="sbx-lineup" role="img" aria-label="The cast in a row: {esc(", ".join(names.values()))}"></svg>
<div class="sbx-names" style="--n:{len(cast["characters"])}">{lineup_names}</div>
</section>
{start}
{shelf_html}
<section class="sbx-cast" id="cast" aria-labelledby="sbx-cast-h"><div class="sbx-head"><h2 id="sbx-cast-h">The cast</h2><p>Each one stands for a reader the book is for, or a role in the story. All drawn by code; none of it is settled.</p><a href="model-sheet.html">The model sheet: every mood and pose &rarr;</a></div>
<div class="sbx-people">{cast_html}</div></section>
<section class="sbx-how" aria-labelledby="sbx-how-h"><div class="sbx-how-head"><h2 id="sbx-how-h">No picture to redraw</h2><p>A panel is corrected by changing a line, not by drawing it again.</p></div>
<div><b>1. Write it as data</b><span>Each storyboard is one JSON file, <code>admin/content/storyboards/NN__&lt;slug&gt;.json</code>: who is in each panel, their pose and mood, what they say, the evidence and its source. The cast is <code>cast.json</code>; these shelves are <code>shelves.json</code>.</span></div>
<div><b>2. The build checks it</b><span>An unknown character, pose, mood, setting or prop stops the release, and so does a Guide line or quote card that is not in its source word for word.</span></div>
<div><b>3. Your browser draws it</b><span>Sketched with <a href="https://roughjs.com">Rough.js</a> (MIT, vendored), the same wobble on every load; as a deck, a grid or a script, animated or still. No image model draws any of it.</span></div>
</section>
<script type="application/json" class="sb-data">{payload}</script>
</div>
<script src="../assets/vendor/rough-4.6.6.js"></script><script src="../assets/storyboard.js"></script>
"""
    page("storyboards/index.html", "Storyboards", body, "The book as storyboards, drawn from data: every storyboard on its shelf, with a preview of its panels, and the cast.",
         crumbs=(("Storyboards", "storyboards/index.html"),), extra_head=SB_HEAD + '<link rel="stylesheet" href="../assets/storyboard.css">\n', wide=True)
    return boards


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
def build_home(parts, flat, pub, drafts, map_doc, briefs, roles, vault, contrib, articles, v2=None):
    v2card = ""
    if v2:
        v2card = (f'<div class="card big v2"><span class="k">The second edition &middot; {esc(v2["version"])} &middot; release candidate, not a version</span>'
                  f'<h3><a href="v2/book/index.html">{esc(v2["title"])}: the end-to-end draft, {esc(v2["version"])}</a></h3>'
                  f'<p>{v2["chapters"]} chapters in {v2["parts"]} parts, {v2["words"]:,} words, written by the book\'s agents from {v2["ideas"]} ideas in the register and the articles behind them, for Dinis to read, print and mark up. Every chapter ends with where it came from; {v2["callouts"]} notes say what only Dinis can fill in.</p>'
                  f'<p class="stats"><span class="stat"><b>{v2["chapters"]}</b><span>chapters</span></span><span class="stat"><b>{v2["words"]:,}</b><span>words</span></span><span class="stat"><b>{v2["ideas"]}</b><span>ideas written in</span></span><span class="stat"><b>{v2["callouts"]}</b><span>for Dinis</span></span></p>'
                  f'<span class="more"><a href="v2/book/index.html">The contents &rarr;</a> &nbsp; <a href="read/v2.html">Read and review &rarr;</a> &nbsp; <a href="v2/book/single.html">On one page &rarr;</a>'
                  + (f' &nbsp; <a href="{esc(v2["pdf"])}">The PDF &rarr;</a>' if v2.get("pdf") else "") + '</span></div>')
    c = map_doc["counts"]
    n_pub = len(pub); n_draft = sum(1 for _, ch in drafts if ch["kind"] == "draft"); n_outline = sum(1 for _, ch in drafts if ch["kind"] == "outline"); pub_words = sum(ch["words"] for _, ch in pub)
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
<p class="ctas">{("<a class=\"btn primary\" href=\"v2/book/index.html\">Read the second edition, " + esc(v2["version"]) + "</a> " if v2 else "")}<a class="btn" href="v1/book/index.html">Read the first edition here</a> <a class="btn" href="{fe["amazon"]["url"]}">Paperback on Amazon</a> <a class="btn" href="{fe["leanpub"]["url"]}">Free to read on Leanpub</a></p>
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
<div class="card big"><span class="k">The book &middot; v1.0.0 &middot; 2018 &middot; frozen</span><h3><a href="v1/book/index.html">The book as published, and the drafts kept apart</a></h3><p>The {n_pub} chapters the 2018 build published, in the print edition's order with its page numbers; and, kept apart, the {n_draft} drafts and {n_outline} outlines it left out, which the second edition starts from.</p>
<p class="stats"><span class="stat"><b>{n_pub}</b><span>published chapters</span></span><span class="stat"><b>{pub_words:,}</b><span>words published</span></span><span class="stat"><b>139</b><span>print pages</span></span><span class="stat"><b>{n_draft + n_outline}</b><span>drafts and outlines</span></span></p>
<span class="more"><a href="v1/book/index.html">The table of contents &rarr;</a> &nbsp; <a href="read/index.html">Read and review &rarr;</a> &nbsp; <a href="v1/generation-z-print-ready.pdf">The print PDF &rarr;</a></span></div>
{v2card}<a class="card" href="v1/versions/index.html"><span class="k">Versions</span><h3>One version so far</h3><p>Where v1.0.0 comes from, the 2018 change log, and the page that will carry the block-by-block delta to v2.</p></a>
<a class="card" href="map/index.html"><span class="k">The map</span><h3>{c["files"]} files, {c["answered_by_articles"]} answered</h3><p>Every 2018 chapter and outline, the newsroom articles that have since answered it, and the gap.</p></a>
<a class="card" href="team/index.html"><span class="k">The team</span><h3>Reviewer, editor, publisher</h3><p>Each reads, challenges, interviews Dinis and signs off. The first interview script is written.</p></a>
<a class="card" href="vault/index.html"><span class="k">The vault</span><h3>Read along</h3><p>The public working vault, its read key published: the working copy of v1, the board, the reviews, the roles.</p></a>
<a class="card" href="read/index.html"><span class="k">Read &amp; review</span><h3>The reader, and the editor's desk</h3><p>The book with its graph beside it; mark, comment, fold and export a review; a reading meter after the newsroom's rules.</p></a>
<a class="card" href="contributors/index.html"><span class="k">Contributors</span><h3>{contrib["totals"]["contributors"]} people, {contrib["totals"]["pull_requests_merged"]} pull requests</h3><p>Who fixed, asked and commented on the first edition, from its git history and GitHub issues: {contrib["totals"]["commits_by_contributors"]} commits by others, {contrib["totals"]["issues"]} issues.</p></a>
<a class="card" href="infographics/index.html"><span class="k">Infographics</span><h3>The book at every altitude, as pictures</h3><p>What the 2018 book and the newsroom already have, the proposals for the second edition by part and chapter, the first ones drawn by code, and the review that decides.</p></a>
<a class="card" href="graph/index.html"><span class="k">The graph</span><h3>The book as a graph: ideas, sources, chapters, tasks</h3><p>The admin area of the publishing process: which articles are processed, which ideas Dinis has accepted, where each goes, and what the briefs asked for.</p></a>
</div>
<h2 id="articles">This site's articles</h2>
<p class="lede">How the work is briefed: each idea, task or review is written up as an article first, then a role is pointed at it.</p>
<ol>
{"".join(f'<li><a href="{rel}">{esc(a["title"].split(":")[0])}</a>: {esc(a["title"].split(":", 1)[1].strip())}</li>' for rel, a in articles)}
</ol>
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
<li><b>The licence of the 2018 text is CC BY 4.0</b>, decided by Dinis on 18 October 2026 (<a href="decisions/index.html#the-2018-text-is-cc-by">decision 001</a>); the 2018 footer's BY-SA and the 2018 repository's Apache 2.0 file are the exceptions.</li>
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
<pre>python3 admin/build/gen_map.py           # admin/content/map.json from v1/content/ and the authored reading
python3 admin/build/gen_contributors.py  # admin/content/contributors.json from admin/content/github/
python3 admin/build/graph_model.py       # checks the graph (ideas, chapters, sources, tasks) and prints its counts
node admin/build/print_pdf.js v2/book/single.html v2/generation-z-developers-<candidate>.pdf   # the candidate as a PDF, after build.py (Playwright)
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
    chapters = "\n".join(f"- [{c['title']}]({BASE}{chapter_url(c, p)}): {c['kind']}{', p. ' + str(c['print_page']) if c.get('print_page') else ''}, {c['words']} words, part {p['title']}" for p in parts for c in p["chapters"])
    write("llms.txt", f"""# gen-z-developers.sgit.ai

> The website for finishing the second edition of Generation Z Developers (Dinis Cruz, 2018). The repository holds the official versions of the book; a public vault holds the working versions. Site {VERSION}.

## The rule
The repository holds the official versions; the vault holds the working versions. v1.0.0 is the 2018 first edition as released, frozen. A version moves from the vault to the repository when signed off, and the versions page shows the delta block by block.

## Sections
- [The book, v1.0.0]({BASE}v1/book/index.html): the 2018 first edition as published, 28 chapters in the print edition's order, then the drafts and outlines it left out; [on one page]({BASE}v1/book/single.html); [the drafts]({BASE}v1/book/drafts.html); [frozen markdown]({BASE}v1/versions/v1.0.0.md); [the print PDF, 139 pages]({BASE}v1/generation-z-print-ready.pdf)
- [The second edition, release candidate]({BASE}v2/book/index.html): the first end-to-end draft of the second edition, written from the ideas register, not an official version; [on one page]({BASE}v2/book/single.html); [read and review]({BASE}read/v2.html); [what waits on Dinis]({BASE}v2/book/for-dinis.html); data at [book.json]({BASE}v2/book/book.json); source v2/content/, one markdown file per chapter naming its ideas and sources
- [Read and review]({BASE}read/index.html): the reader with the graph beside it and the editor's desk (states, comments, folds, export); the book as data at [book.json]({BASE}v1/book/book.json)
- [Synthetic readers]({BASE}readers/index.html): invented readers who read a release candidate the way they would, say where they would put it down and whether they would buy it, and are interviewed; the newsroom's synthetic-users method adapted to a book ([the protocol]({BASE}readers/protocol.html)); data under admin/content/readers/
- [The graph]({BASE}graph/index.html): the admin area of the publishing process: [the ideas register]({BASE}graph/ideas/index.html), [the sources and their states]({BASE}graph/sources.html), [the chapter map, proposed]({BASE}graph/chapters.html), [the tasks]({BASE}graph/tasks.html), [the plan]({BASE}graph/plan.html), [the graph drawn]({BASE}graph/view.html); data at [graph.json]({BASE}graph/graph.json)
- [Infographics]({BASE}infographics/index.html): the book at every altitude as pictures: [the plan, with a review]({BASE}infographics/plan.html) (data at [plan.json]({BASE}infographics/plan.json)), [what exists]({BASE}infographics/existing.html) (the 2018 images and the newsroom's figures), [how they are made]({BASE}infographics/how.html); drawn by code from admin/content/infographics/drawn/*.json into infographics/svg/*.svg
- [Covers]({BASE}covers/index.html): three cover designs for the second edition, proposals (decision 004), each as SVG (the master, fonts embedded), Kindle and Leanpub JPG and a KDP paperback PDF; drawn by admin/build/covers.py from admin/content/covers/covers.json
- [The contributors]({BASE}contributors/index.html): who contributed to the first edition, from git and GitHub; data at [contributors.json]({BASE}admin/content/contributors.json)
- [Versions]({BASE}v1/versions/index.html): the official versions and their deltas (page_versions.py from the newsroom)
- [The map]({BASE}map/index.html): one row per 2018 file, the newsroom articles that answer it, the gap; data at [map.json]({BASE}admin/content/map.json)
- [Articles]({BASE}articles/index.html): this site's own articles, the briefs for the roles; each has a markdown twin at articles/<slug>.md
- [The briefs]({BASE}briefs/index.html): the six newsroom articles tagged gen-z-book and the two build briefs, verbatim
- [The team]({BASE}team/index.html): reviewer, editor, publisher; role.md, issues, briefs, debriefs, the first interview script
- [The vault]({BASE}vault/index.html): the public working vault, read key published; the private vault for the OpenRouter key
- [Admin]({BASE}admin/index.html): the build chain and rules; [release history]({BASE}admin/versions.html)

## The articles
{chr(10).join(f"- [{a['title']}]({BASE}{rel[:-5]}.md)" for rel, a in articles)}

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
        "print_pdf": {"path": "v1/generation-z-print-ready.pdf", "pages": 139, "sha256": PDF_SHA, "what": "the Leanpub build of 2018-10-08 made print-ready for the paperback; its table of contents is the published book's"},
        "counts": {"markdown_files": 138, "published_chapters": 28, "outlines": 90},
    }, indent=1) + "\n", encoding="utf-8")
    parts, front = load_book()
    map_doc = json.loads((ROOT / "admin/content/map.json").read_text(encoding="utf-8"))
    files_in_map = {r["file"] for r in map_doc["rows"]}
    files_on_disk = {p.relative_to(CONTENT).as_posix() for p in CONTENT.rglob("*.md")}
    if files_in_map != files_on_disk:
        sys.exit(f"build: map.json and v1/content disagree: {sorted(files_in_map ^ files_on_disk)}; run gen_map.py")
    frozen_md, flat, pub, drafts = build_book(parts, front, map_doc["rows"])
    build_versions(frozen_md, parts, pub)
    bookdoc = build_bookjson(parts, front, flat, map_doc["rows"])
    build_read(bookdoc)
    contrib = build_contributors()
    build_map(parts, map_doc)
    briefs = build_briefs()
    roles = build_team()
    vault = build_vault()
    articles = build_articles()
    build_storyboards()
    build_newsroom_survey()
    build_graph({"page": page, "write": write, "esc": esc, "md": md})
    build_readers({"page": page, "write": write, "esc": esc, "md": md})
    v2 = build_v2({"page": page, "write": write, "esc": esc, "md": md, "sha": sha, "split_blocks": lambda h: _TopLevel().split(h), "graph": graph_model.load(), "version": VERSION})
    if v2:
        build_read_v2(v2)
    build_infographics({"page": page, "write": write, "esc": esc, "md": md, "graph": graph_model.load(), "version": VERSION})
    build_covers({"page": page, "esc": esc, "first_edition_lines": FIRST_EDITION["cover_lines"]})
    build_paper_reviews({})
    build_home(parts, flat, pub, drafts, map_doc, briefs, roles, vault, contrib, articles, v2)
    print(f"build: {VERSION}, {len(flat)} chapters, {len([w for w in written if w.endswith('.html')])} pages, {len(written)} files written")


if __name__ == "__main__":
    main()
