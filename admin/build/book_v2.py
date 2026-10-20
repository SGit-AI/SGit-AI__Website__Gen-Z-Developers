"""The book as a release candidate (Generation ZX Founders, a new book that grew out of the 2018 one): v2/content/ -> v2/book/ (one page per chapter, the contents, the whole
book on one page for print, book.json for the reader), v2/versions/<candidate>.md frozen once, and the manifest the
gate checks.

v2/content/<n>-<part>/<nn>__<slug>.md is a chapter drafted from the ideas register: its front matter names the
ideas it is written from, the sources it drew on and the 2018 files it answers, and the build refuses a chapter
whose ideas, sources, part or 2018 files do not exist. A candidate is not an official version: it is frozen like
one (text_sha256 recorded once in admin/content/book/versions.json under "candidates", the text written once to
v2/versions/), so that what Dinis read and marked up cannot change behind him, but it is not in "versions", it is
not published outside this site, and the publisher's rule holds (decision 009).

Called from build.py as build_v2(ctx) with the page/write/esc/md/sha helpers; pdf rendering is admin/build/print_pdf.js.
"""
import hashlib
import json
import os
import re
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "v2/content"
OUT = "v2/book/"

CALLOUT = re.compile(r"^> \*\*For Dinis:\*\*\s*(.*?)$(?:\n^>\s?(.*?)$)*", re.M)
# the strings the build refuses outright; the writers' style check is wider (STYLE.md), but "perfect" in a quoted 2018 line and
# "leverage" as Dinis's own noun ("places of highest leverage") are legitimate, so the gate leaves those to the editor
BANNED = ["—", "–", " prose ", "massively", "get rid of", "delve", "tapestry", "utilis", "worth noting", "In this chapter", "dive in"]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        sys.exit("book_v2: a chapter has no front matter")
    fm = {}
    for line in m.group(1).split("\n"):
        if not line.strip() or line.startswith("#"):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
        elif v.isdigit():
            v = int(v)
        else:
            v = v.strip("'\"")
        fm[k.strip()] = v
    return fm, m.group(2).strip()


def load(graph_nodes, chapters_doc, ideas_doc):
    """Every chapter under v2/content/, checked against the register, the chapter map and the graph's nodes."""
    if not SRC.exists():
        return None
    ideas = {i["id"]: i for i in ideas_doc["ideas"]}
    parts = OrderedDict()
    for p in chapters_doc["parts"]:
        parts[p["id"]] = {"id": p["id"], "title": p["title"], "note": p.get("note"), "chapters": [], "intro": "", "map": p}
    errors, chapters, front = [], [], None
    for f in sorted(SRC.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(ROOT).as_posix()
        if f.name == "_index.md":
            fm, body = frontmatter(text)
            if fm.get("part") in parts:
                parts[fm["part"]]["intro"] = body
            else:
                errors.append(f"{rel}: part intro for unknown part {fm.get('part')}")
            continue
        fm, body = frontmatter(text)
        for k in ("title", "slug", "part", "number", "ideas", "answers_2018", "sources", "character", "gravity", "status"):
            if k not in fm:
                errors.append(f"{rel}: front matter lacks {k}")
        for b in BANNED:
            if b in body:
                errors.append(f"{rel}: contains the banned string {b!r}")
        for i in fm.get("ideas") or []:
            if i not in ideas:
                errors.append(f"{rel}: written from unknown idea {i}")
        for s in fm.get("sources") or []:
            if ":" in s and s.split(":", 1)[0] in ("art", "news", "agent", "dec", "sb", "book", "survey") and s not in graph_nodes:
                errors.append(f"{rel}: cites unknown source {s}")
        for a in fm.get("answers_2018") or []:
            if not (ROOT / "v1/content" / a).exists():
                errors.append(f"{rel}: answers unknown 2018 file {a}")
        callouts = [re.sub(r"\n>\s?", " ", m.group(0)[len("> **For Dinis:** "):]).strip() for m in CALLOUT.finditer(body)]
        ch = {"file": rel, "fm": fm, "body": body, "title": fm.get("title", f.stem), "slug": fm.get("slug", f.stem), "part": fm.get("part"),
              "number": fm.get("number", 0), "ideas": fm.get("ideas") or [], "sources": fm.get("sources") or [], "answers": fm.get("answers_2018") or [],
              "character": fm.get("character"), "gravity": fm.get("gravity"), "words": len(re.findall(r"\w+", re.sub(CALLOUT, "", body))), "callouts": callouts, "sha": None}
        ch["sha"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if fm.get("part") == "front":
            front = ch
            continue
        if fm.get("part") not in parts:
            errors.append(f"{rel}: unknown part {fm.get('part')}")
            continue
        if fm.get("slug") not in {c["id"] for c in parts[fm["part"]]["map"]["chapters"]}:
            errors.append(f"{rel}: slug {fm.get('slug')} is not a chapter of part {fm['part']} in chapters.json")
        parts[fm["part"]]["chapters"].append(ch)
        chapters.append(ch)
    for p in parts.values():
        p["chapters"].sort(key=lambda c: c["number"])
    chapters.sort(key=lambda c: c["number"])
    nums = [c["number"] for c in chapters]
    if nums != list(range(1, len(nums) + 1)):
        errors.append(f"chapter numbers are not 1..{len(nums)}: {nums}")
    if errors:
        sys.exit("book_v2:\n  " + "\n  ".join(errors))
    return {"parts": [p for p in parts.values() if p["chapters"]], "chapters": chapters, "front": front,
            "words": sum(c["words"] for c in chapters) + (front["words"] if front else 0)}


def current_title():
    """The book's title now (admin/content/book/title.json), checked against the decision it names. A candidate's frozen
    text keeps the title it was written under; the pages show this one, and say so when the two differ."""
    doc = json.loads((ROOT / "admin/content/book/title.json").read_text(encoding="utf-8"))
    full = f'{doc["title"]} ({doc["edition"]})'
    if full not in (ROOT / doc["decision"]).read_text(encoding="utf-8"):
        sys.exit(f"book_v2: the title in admin/content/book/title.json, {full}, is not in {doc['decision']}")
    return dict(doc, full=full)


def frozen_markdown(book, cand):
    out = [f"# {cand.get('title', 'Generation ZX Developers (GenAI Startup Edition)')}\n\n*{cand['version']}, {cand['date']}. {cand['status']}*\n"]
    if book["front"]:
        out.append(f"## {book['front']['title']}\n\n{book['front']['body']}\n")
    for p in book["parts"]:
        out.append(f"# Part: {p['title']}\n")
        if p["intro"]:
            out.append(p["intro"] + "\n")
        for c in p["chapters"]:
            out.append(f"## {c['number']}. {c['title']}\n\n{c['body']}\n")
    return "\n".join(out)


def build_v2(ctx):
    page, write, esc, md, sha, split_blocks, graph = (ctx[k] for k in ("page", "write", "esc", "md", "sha", "split_blocks", "graph"))
    nodes = graph["nodes"]
    vfile = ROOT / "admin/content/book/versions.json"
    vdoc = json.loads(vfile.read_text(encoding="utf-8"))
    cands = vdoc.get("candidates") or []
    if not SRC.exists():
        return None
    if not cands:
        sys.exit("book_v2: v2/content exists but admin/content/book/versions.json has no candidates entry")
    finished = [x for x in cands if not x.get("in_progress")]
    map_file = (finished[-1] if finished else cands[-1]).get("map", "admin/content/graph/chapters.json")
    chapters_doc = json.loads((ROOT / map_file).read_text(encoding="utf-8"))
    ideas_doc = json.loads((ROOT / "admin/content/graph/ideas.json").read_text(encoding="utf-8"))
    ideas = {i["id"]: i for i in ideas_doc["ideas"]}
    book = load(nodes, chapters_doc, ideas_doc)
    if not book:
        return None
    finished = [x for x in cands if not x.get("in_progress")]
    if not finished:
        sys.exit("book_v2: every candidate is in progress; nothing to render")
    cand = finished[-1]
    if cands[-1] is not cand:
        print(f"build: candidate {cands[-1]['version']} is in progress; rendering {cand['version']}")
    written_as = cand.get("title", "Generation ZX Developers (GenAI Startup Edition)")  # what the frozen text says
    cur = current_title()
    title, name, sub, short = cur["full"], cur["title"], cur["edition"] + ")", cur["short"]
    retitled = ("" if written_as == title else
                f'<p class="small dim">Release candidate {esc(cand["version"])} was written and frozen as <i>{esc(written_as)}</i>. '
                f'The book is now <i>{esc(title)}</i> (<a href="{{up}}decisions/index.html#{esc(cur["anchor"])}">decision 019</a>), a new book that grew out of '
                f'{esc(cur["grew_out_of"])} (decision 017); the next candidate carries the title.</p>')
    text = frozen_markdown(book, cand)
    got = sha(text)
    snap = ROOT / "v2/versions" / (cand["version"] + ".md")
    if os.environ.get("GENZ_NO_FREEZE"):
        print(f"build: candidate {cand['version']} not frozen (GENZ_NO_FREEZE set); text sha {got[:12]}")
    elif cand.get("text_sha256") is None:
        cand["text_sha256"] = got
        vfile.write_text(json.dumps(vdoc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_text(text, encoding="utf-8")
        print(f"build: recorded text_sha256 for candidate {cand['version']} and froze {snap.relative_to(ROOT)}")
    elif cand["text_sha256"] != got:
        sys.exit(f"book_v2: the text of candidate {cand['version']} changed after it was frozen (sha {got[:12]} vs {cand['text_sha256'][:12]}). "
                 f"A candidate is read and marked up as frozen: add the next candidate to admin/content/book/versions.json (text_sha256 null) and rebuild.")
    elif not snap.exists():
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_text(text, encoding="utf-8")
    ver = cand["version"]
    pdf_rel = f"v2/generation-z-developers-{ver}.pdf"
    pdf_exists = (ROOT / pdf_rel).exists()
    n = len(book["chapters"])
    flat = [(p, c) for p in book["parts"] for c in p["chapters"]]
    manifest = {"version": ver, "site": ctx["version"], "what": "The hash of every chapter's markdown (v2/content/) and of the <main> it rendered; validate.js "
                "refuses a page that no longer matches its markdown. A candidate's text is frozen once at v2/versions/<version>.md.", "chapters": []}

    def badge():
        return f'<span class="badge draft">release candidate {esc(ver)}</span>'

    def callout_html(body_html):
        # the For Dinis callouts: blockquotes whose first words are the marker
        return re.sub(r"<blockquote>\s*<p><strong>For Dinis:</strong>(.*?)</p>\s*</blockquote>",
                      lambda m: f'<aside class="for-dinis"><b>For Dinis</b>{m.group(1)}</aside>', body_html, flags=re.S)

    def provenance(c, up):
        items = []
        for i in c["ideas"]:
            idea = ideas[i]
            items.append(f'<li><a href="{up}graph/ideas/{esc(i)}.html">{esc(idea["title"])}</a> <span class="st {esc(idea["state"])}">{esc(idea["state"])}</span></li>')
        srcs = []
        for s in c["sources"]:
            nd = nodes.get(s)
            if nd:
                url = nd.get("url", "")
                srcs.append(f'<a href="{esc(url if url.startswith("http") else up + url)}">{esc(nd["title"])}</a>' if url else esc(nd["title"]))
            else:
                srcs.append(esc(s))
        ans = []
        for a in c["answers"]:
            nd = nodes.get("book:" + a)
            ans.append(f'<a href="{up}{esc(nd["url"])}">{esc(nd["title"])}</a>' if nd and nd.get("url") else esc(a))
        return (f'<div class="prov-box"><h3>Where this chapter comes from</h3>'
                f'<p class="small">Written from {len(c["ideas"])} idea{"s" if len(c["ideas"]) != 1 else ""} in <a href="{up}graph/ideas/index.html">the register</a>'
                + (":" if c["ideas"] else ". The hands-on part has no ideas placed yet; its sources are the articles below.") + f'</p>'
                + (f'<ul class="prov">{"".join(items)}</ul>' if items else "")
                + (f'<p class="small">Sources drawn on: {"; ".join(srcs)}.</p>' if srcs else "")
                + (f'<p class="small">Answers the 2018 files: {"; ".join(ans)}.</p>' if ans else "")
                + f'<p class="small dim">Centre of gravity: {esc(c["gravity"] or "all")} &middot; written first for {esc(c["character"] or "the reader")} &middot; {c["words"]:,} words &middot; '
                  f'<a href="{up}graph/chapters.html#{esc(c["slug"])}">the chapter on the map</a> &middot; <a href="https://github.com/SGit-AI/SGit-AI__Website__Gen-Z-Developers/blob/dev/{esc(c["file"])}">the markdown</a></p></div>')

    def nav(i):
        prev = flat[i - 1][1] if i > 0 else None
        nxt = flat[i + 1][1] if i + 1 < len(flat) else None
        return ('<div class="prevnext">' + (f'<a href="{prev["slug"]}.html">&larr; {esc(prev["title"])}</a>' if prev else (f'<a href="{book["front"]["slug"]}.html">&larr; {esc(book["front"]["title"])}</a>' if book["front"] else "<span></span>"))
                + (f'<a href="{nxt["slug"]}.html">{esc(nxt["title"])} &rarr;</a>' if nxt else '<a href="index.html">The contents &rarr;</a>') + "</div>")

    notice = (f'<div class="rc-note"><b>A release candidate.</b> This is {esc(ver)} of {esc(name)}: every chapter written by the book\'s agents '
              f'from <a href="../../graph/ideas/index.html">the ideas register</a>, for Dinis to read, print and mark up. Nothing in it is signed off. '
              f'The first edition, <a href="../../v1/book/index.html">v1.0.0</a>, is the only official version; the candidate\'s text is frozen at '
              f'<a href="../versions/{esc(ver)}.md">v2/versions/{esc(ver)}.md</a> so that what was read cannot change behind the reader (<a href="../../decisions/index.html#a-candidate-is-read-on-the-site-from-a-frozen-snapshot">decision 009</a>).</div>')
    # one page per chapter
    for i, (p, c) in enumerate(flat):
        rel = f"{OUT}{c['slug']}.html"
        up = "../../"
        body_html = callout_html(md(c["body"]))
        main = (f'<article class="chapter v2"><p class="small dim">{esc(p["title"])} &middot; chapter {c["number"]} of {n} &middot; {badge()} &middot; {c["words"]:,} words &middot; '
                f'<a href="{up}read/v2.html#{esc(c["slug"])}">read and review</a></p><h1>{esc(c["title"])}</h1><div class="body">{body_html}</div>{provenance(c, up)}{nav(i)}</article>')
        page(rel, c["title"], main, f"{c['title']}: chapter {c['number']} of {title}, release candidate {ver}.",
             crumbs=((short, OUT + "index.html"), (p["title"], f"{OUT}index.html#{p['id']}"), (c["title"], rel)))
        manifest["chapters"].append({"file": c["file"], "page": rel, "title": c["title"], "part": p["title"], "number": c["number"], "words": c["words"],
                                     "ideas": c["ideas"], "markdown_sha256": c["sha"], "main_sha256": sha(main)})
    if book["front"]:
        f = book["front"]
        rel = f"{OUT}{f['slug']}.html"
        main = (f'<article class="chapter v2"><p class="small dim">Front matter &middot; {badge()} &middot; {f["words"]:,} words</p><h1>{esc(f["title"])}</h1>'
                f'<div class="body">{callout_html(md(f["body"]))}</div><div class="prevnext"><a href="index.html">&larr; The contents</a><a href="{flat[0][1]["slug"]}.html">{esc(flat[0][1]["title"])} &rarr;</a></div></article>')
        page(rel, f["title"], main, f"{f['title']}: the front matter of {title}, release candidate {ver}.",
             crumbs=((short, OUT + "index.html"), (f["title"], rel)))
        manifest["chapters"].append({"file": f["file"], "page": rel, "title": f["title"], "part": "Front matter", "number": 0, "words": f["words"], "ideas": [],
                                     "markdown_sha256": f["sha"], "main_sha256": sha(main)})
    write(f"{OUT}manifest.json", json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    # the contents
    all_callouts = [(c, x) for c in book["chapters"] for x in c["callouts"]] + ([(book["front"], x) for x in book["front"]["callouts"]] if book["front"] else [])
    toc = []
    for pi, p in enumerate(book["parts"], 1):
        intro = f'<p class="small">{md(p["intro"]).replace("<p>", "").replace("</p>", " ")}</p>' if p["intro"] else ""
        items = "".join(f'<li><a href="{c["slug"]}.html">{esc(c["title"])}</a> <span class="w">{c["words"]:,} words &middot; {len(c["ideas"])} ideas{" &middot; " + str(len(c["callouts"])) + " for Dinis" if c["callouts"] else ""}</span></li>' for c in p["chapters"])
        toc.append(f'<li id="{esc(p["id"])}"><div class="part"><span class="n">{pi}</span>{esc(p["title"])} <span class="w">{len(p["chapters"])} chapters</span></div>{intro}<ol start="{p["chapters"][0]["number"]}">{items}</ol></li>')
    front_li = f'<li><a href="{book["front"]["slug"]}.html">{esc(book["front"]["title"])}</a> <span class="w">front matter</span></li>' if book["front"] else ""
    n_ideas = len({i for c in book["chapters"] for i in c["ideas"]})
    body = f"""<h1>{esc(title)}</h1>
{retitled.replace("{up}", "../../")}
<p class="lede">Release candidate {esc(ver)}, {esc(cand["date"])}: {n} chapters in {len(book["parts"])} parts, {book["words"]:,} words, written from {n_ideas} of the {len(ideas)} ideas in the register, with {len(all_callouts)} places where only Dinis can fill in what is missing. {esc(cand.get("what", ""))}</p>
{notice}
<p class="stats"><span class="stat"><b>{n}</b><span>chapters</span></span><span class="stat"><b>{book["words"]:,}</b><span>words</span></span><span class="stat"><b>{n_ideas}</b><span>ideas written in</span></span><span class="stat"><b>{len(all_callouts)}</b><span>for Dinis</span></span></p>
<p><a href="../../read/v2.html">Read and review it</a> &middot; <a href="single.html">on one page, for print</a> &middot; {'<a href="../' + esc(pdf_rel.split('/', 1)[1]) + '">the PDF</a> &middot; ' if pdf_exists else ''}<a href="../versions/{esc(ver)}.md">the frozen markdown</a> &middot; <a href="book.json">book.json</a> &middot; <a href="../../graph/chapters.html">the chapter map</a> &middot; <a href="for-dinis.html">everything that waits on Dinis</a> &middot; <a href="../../readers/index.html">what synthetic readers made of it</a></p>
<h2>How to read it, and how to answer</h2>
<p>Read it as a reader first: <a href="../../read/v2.html">the reader</a> keeps your place, lets you mark each chapter (read, to review, continue, signed off), comment on any paragraph, and export the review as a file for the vault's <code>reviews/</code> folder. Or print <a href="single.html">the one-page version</a>{' or <a href="../' + esc(pdf_rel.split('/', 1)[1]) + '">the PDF</a>' if pdf_exists else ''} and write on it. Every chapter ends with where it came from: the ideas, the articles and the 2018 files, each a link. A verb on an idea (keep, rewrite, merge, cut, article first, later, not doing it) is a decision; the editor records it in the vault and the idea's state moves on <a href="../../graph/ideas/index.html">the register</a>.</p>
<ol class="toc v2">{front_li}{"".join(toc)}</ol>
<p class="small dim">Source: <code>v2/content/</code>, one markdown file per chapter with the ideas, sources and 2018 files it was written from in its front matter; <code>admin/build/book_v2.py</code> renders these pages and refuses a chapter that cites an idea, source, part or file that does not exist. Manifest: <a href="manifest.json">manifest.json</a>.</p>
"""
    page(OUT + "index.html", f"{name}, release candidate {ver}", body,
         f"{title}, release candidate {ver}: {n} chapters written from the ideas register, for Dinis to read and mark up.",
         crumbs=((short, OUT + "index.html"),))
    # what waits on Dinis
    rows = "".join(f'<li><a href="{esc(c["slug"])}.html">{esc(c["title"])}</a>: {esc(x)}</li>' for c, x in all_callouts)
    unplaced = [i for i in ideas.values() if not i.get("chapter")]
    qs = "".join(f'<li><a href="../../graph/ideas/{esc(i["id"])}.html">{esc(i["title"])}</a> <span class="dim small">{esc(i.get("notes") or i["statement"])}</span></li>' for i in unplaced)
    body = f"""<h1>Everything that waits on Dinis</h1>
<p class="lede">The release candidate was written from the register, and the register was written from the articles; where the articles stop, the chapters stop and say so. This page collects every <b>For Dinis</b> note in the {n} chapters, and the ideas the map has not placed.</p>
{notice}
<h2>The notes in the chapters ({len(all_callouts)})</h2>
<ul class="prov">{rows or "<li class=dim>none</li>"}</ul>
<h2>Ideas with no chapter ({len(unplaced)})</h2>
<ul class="prov">{qs or "<li class=dim>none</li>"}</ul>
<h2>The questions the articles keep apart</h2>
<p class="small">Each co-written article ends with questions for Dinis; <a href="../../graph/index.html">the graph's hub</a> lists them, and the chapters that depend on an answer carry a note above.</p>
"""
    page(OUT + "for-dinis.html", "Everything that waits on Dinis", body, f"Every note for Dinis in release candidate {ver} of {name}, and the ideas with no chapter.",
         crumbs=((short, OUT + "index.html"), ("For Dinis", OUT + "for-dinis.html")))
    # the whole book on one page, for print
    parts_html = []
    for pi, p in enumerate(book["parts"], 1):
        chs = "".join(f'<section class="pr-chapter" id="{esc(c["slug"])}"><h2><span class="num">{c["number"]}</span>{esc(c["title"])}</h2><div class="body">{callout_html(md(c["body"]))}</div>'
                      f'<p class="pr-prov">From the register: {", ".join(esc(ideas[i]["title"]) for i in c["ideas"]) or "the articles of the hands-on part"}. Answers: {", ".join(esc(nodes["book:" + a]["title"]) for a in c["answers"] if ("book:" + a) in nodes) or "no 2018 file"}.</p></section>' for c in p["chapters"])
        parts_html.append(f'<section class="pr-part" id="{esc(p["id"])}"><p class="pr-partn">Part {pi}</p><h1>{esc(p["title"])}</h1>{md(p["intro"]) if p["intro"] else ""}</section>{chs}')
    toc_print = "".join(f'<li class="pr-tocpart">{esc(p["title"])}<ol>' + "".join(f'<li>{c["number"]}. {esc(c["title"])}</li>' for c in p["chapters"]) + "</ol></li>" for p in book["parts"])
    front_html = f'<section class="pr-chapter front" id="{esc(book["front"]["slug"])}"><h2>{esc(book["front"]["title"])}</h2><div class="body">{callout_html(md(book["front"]["body"]))}</div></section>' if book["front"] else ""
    back = "".join(f'<li><b>{esc(c["title"])}:</b> {esc(x)}</li>' for c, x in all_callouts)
    single = f"""<article class="printbook">
<section class="pr-title"><p class="pr-k">Release candidate {esc(ver)} &middot; {esc(cand["date"])}</p><h1>{esc(name)}</h1><p class="pr-sub">{esc(sub.rstrip(")"))}</p><p class="pr-by">Dinis Cruz</p>{retitled.replace("{up}", "../../")}
<p class="pr-note">{esc(cand["status"])} The first edition (2018) is the only official version. This candidate was written by the book's agents from the ideas register and is for reading and marking up. Its text is frozen as v2/versions/{esc(ver)}.md; the title is Dinis's decision of 19 October 2026 (decision 014). Text: CC BY 4.0.</p></section>
<section class="pr-toc"><h1>Contents</h1><ol>{toc_print}</ol></section>
{front_html}
{"".join(parts_html)}
<section class="pr-part back" id="for-dinis"><p class="pr-partn">Back matter</p><h1>What only Dinis can fill in</h1><p>The {len(all_callouts)} notes left in the chapters, collected.</p><ul>{back}</ul></section>
</article>"""
    page(OUT + "single.html", f"{title}, {ver}, on one page", single,
         f"The whole release candidate {ver} of {name} on one page, for reading and printing.",
         crumbs=((short, OUT + "index.html"), ("On one page", OUT + "single.html")),
         extra_head='<link rel="stylesheet" href="../../assets/print-book.css">\n')
    # book.json for the reader
    chapters = []
    for p, c in flat:
        blocks_ = split_blocks(callout_html(md(c["body"])))
        chapters.append({"slug": c["slug"], "part": p["id"], "title": c["title"], "kind": "candidate", "published": True, "number": c["number"], "print_page": None,
                         "words": c["words"], "url": f"{OUT}{c['slug']}.html", "file": c["file"],
                         "articles": [{"title": nodes[s]["title"], "url": ("" if nodes[s].get("url", "").startswith("http") else "../") + nodes[s].get("url", "")} for s in c["sources"] if s in nodes and nodes[s].get("url") and s.split(":")[0] in ("art", "news")][:6],
                         "ideas": [{"id": i, "title": ideas[i]["title"], "state": ideas[i]["state"], "url": f"../graph/ideas/{i}.html"} for i in c["ideas"]],
                         "gap": "", "terms": [], "related": [],
                         "blocks": [{"id": f"{c['slug']}-{k + 1}", "html": b, "words": len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", b)))} for k, b in enumerate(blocks_)]})
    fb = split_blocks(callout_html(md(book["front"]["body"]))) if book["front"] else []
    doc = {"what": f"{title}, release candidate {ver}, as data for the reader at read/v2.html. Generated by book_v2.py from v2/content/.",
           "version": ver, "candidate": f"release candidate {ver}", "site": ctx["version"], "title": title, "subtitle": "Release candidate " + ver,
           "print_pdf": ("../" + pdf_rel) if pdf_exists else None, "cover": None,
           "parts": [{"slug": p["id"], "title": p["title"], "print_page": None, "intro_html": md(p["intro"]) if p["intro"] else ""} for p in book["parts"]],
           "front": {"slug": book["front"]["slug"] if book["front"] else "about", "title": book["front"]["title"] if book["front"] else "About", "print_page": None,
                     "words": book["front"]["words"] if book["front"] else 0, "url": f"{OUT}{book['front']['slug']}.html" if book["front"] else OUT + "index.html",
                     "blocks": [{"id": f"front-{k + 1}", "html": b, "words": len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", b)))} for k, b in enumerate(fb)]},
           "chapters": chapters,
           "meter": {"start": 500, "symbol": "£", "pence_per_words": 250, "min_share": 0.1,
                     "rule": "A penny per 250 words, charged for the share of the chapter read (never less than 10% once opened); credit starts at £5 and can go below zero; nothing leaves the browser."}}
    write(f"{OUT}book.json", json.dumps(doc, ensure_ascii=False) + "\n")
    build_rounds(ctx, book, cands, cand, text, ideas, notice)
    return {"version": ver, "title": title, "candidate": cand, "in_progress": cands[-1]["version"] if cands[-1] is not cand else None, "chapters": n, "parts": len(book["parts"]), "words": book["words"], "ideas": n_ideas, "callouts": len(all_callouts),
            "pdf": pdf_rel if pdf_exists else None, "book": book}


def _chapters_of_frozen(md_text):
    """The chapters of a frozen candidate: (number, title, words) from its '## N. Title' headings."""
    out, cur, words = [], None, 0
    for line in md_text.splitlines():
        m = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            if cur:
                out.append((cur[0], cur[1], words))
            cur, words = (int(m.group(1)), m.group(2).strip()), 0
            continue
        if cur:
            words += len(re.findall(r"\w+", line))
    if cur:
        out.append((cur[0], cur[1], words))
    return out


def build_rounds(ctx, book, cands, cand, text, ideas, notice):
    """v2/book/rounds.html and diff.html: what each round changed, by size, and the block diff Dinis reads (decision 011);
    the librarian's count of the rounds converging (The book in release mode, task 5). The differ is the newsroom's
    page_versions.diff, not a second one."""
    page, write, esc, md = (ctx[k] for k in ("page", "write", "esc", "md"))
    short = current_title()["short"]
    sys.path.insert(0, str(ROOT / "admin/build"))
    from page_versions import diff as pv_diff  # noqa: E402
    finished = [x for x in cands if not x.get("in_progress")]
    prev = finished[-2] if len(finished) > 1 else None
    rc_map_prev = ROOT / "admin/content/graph/chapters-rc1.json"
    rows = []
    sizes = None
    diff_html = ""
    if prev:
        old_text = (ROOT / prev["frozen"]).read_text(encoding="utf-8") if (ROOT / prev["frozen"]).exists() else ""
        old_ch = {t: w for _, t, w in _chapters_of_frozen(old_text)}
        cur_ch = {c["title"]: c["words"] for c in book["chapters"]}
        prev_map = json.loads(rc_map_prev.read_text(encoding="utf-8")) if rc_map_prev.exists() else {"parts": []}
        cur_map = json.loads((ROOT / "admin/content/graph/chapters.json").read_text(encoding="utf-8"))
        pm = {c["id"]: (p["id"], c["title"]) for p in prev_map["parts"] for c in p["chapters"]}
        cm = {c["id"]: (p["id"], c["title"]) for p in cur_map["parts"] for c in p["chapters"]}
        parts_added = [p["title"] for p in cur_map["parts"] if p["id"] not in {q["id"] for q in prev_map["parts"]}]
        parts_removed = [p["title"] for p in prev_map["parts"] if p["id"] not in {q["id"] for q in cur_map["parts"]}]
        added = [cm[i][1] for i in cm if i not in pm]
        removed = [pm[i][1] for i in pm if i not in cm]
        moved = [(pm[i][1], pm[i][0], cm[i][0]) for i in cm if i in pm and pm[i][0] != cm[i][0]]
        retitled = [(pm[i][1], cm[i][1]) for i in cm if i in pm and pm[i][1] != cm[i][1]]
        n, diff_html = pv_diff(old_text, text)
        sizes = {"parts added": len(parts_added), "parts removed": len(parts_removed), "chapters added": len(added), "chapters removed": len(removed),
                 "chapters moved": len(moved), "chapters retitled": len(retitled), "blocks changed": n["changed"], "blocks added": n["added"], "blocks removed": n["removed"], "blocks kept": n["kept"]}
        batch = [i for i in ideas.values() if i.get("batch") == cand["version"].split("-")[-1]]
        by_kind = {}
        for i in batch:
            by_kind[i["kind"]] = by_kind.get(i["kind"], 0) + 1
        ch_rows = []
        for c in book["chapters"]:
            before = old_ch.get(c["title"])
            if c["slug"] not in pm:
                ch_rows.append(f'<tr><td><a href="{esc(c["slug"])}.html">{esc(c["title"])}</a></td><td><span class="st open">new</span></td><td></td><td>{c["words"]:,}</td></tr>')
            else:
                old_title = pm[c["slug"]][1]
                before = old_ch.get(old_title, old_ch.get(c["title"]))
                delta = (c["words"] - before) if before is not None else None
                ch_rows.append(f'<tr><td><a href="{esc(c["slug"])}.html">{esc(c["title"])}</a>{(" <span class=dim>was " + esc(old_title) + "</span>") if old_title != c["title"] else ""}</td>'
                               f'<td>{"moved to " + esc(cm[c["slug"]][0]) if pm[c["slug"]][0] != cm[c["slug"]][0] else "kept"}</td><td>{(f"{before:,}" if before is not None else "")}</td><td>{c["words"]:,}{(f" ({delta:+,})" if delta is not None else "")}</td></tr>')
        for i in pm:
            if i not in cm:
                ch_rows.append(f'<tr><td>{esc(pm[i][1])}</td><td><span class="st declined">removed</span></td><td>{old_ch.get(pm[i][1], 0):,}</td><td></td></tr>')
        rows.append(f"""<h2>Round 1: {esc(prev["version"])} to {esc(cand["version"])}</h2>
<p>{esc(cand.get("what", ""))}</p>
<p class="gr-stats">{"".join(f'<span class="stat"><b>{v}</b><span>{esc(k)}</span></span>' for k, v in sizes.items())}</p>
<p class="small">The sizes are the round's shape (decision 008: parts, chapters, sections, paragraphs): this round added {len(parts_added)} part{"s" if len(parts_added) != 1 else ""} ({", ".join(esc(x) for x in parts_added) or "none"}){(", removed " + ", ".join(esc(x) for x in parts_removed)) if parts_removed else ""}, added {len(added)} chapters, moved {len(moved)} and retitled {len(retitled)}; at the paragraph level {n["changed"]:,} blocks changed, {n["added"]:,} were added and {n["removed"]:,} removed against {n["kept"]:,} kept. <a href="diff.html">The diff</a>, block by block, is what Dinis reads (decision 011).</p>
<h3>The ideas that came in</h3>
<p>{len(batch)} ideas in the batch <code>{esc(cand["version"].split("-")[-1])}</code>{(": " + ", ".join(f"{v} {esc(k)}" for k, v in sorted(by_kind.items()))) if batch else ""}. Each is on <a href="../../graph/ideas/index.html">the register</a> with its sources; none has been through a hearing: Dinis brought the pile in himself (decision 014).</p>
<ul class="prov">{"".join(f'<li><a href="../../graph/ideas/{esc(i["id"])}.html">{esc(i["title"])}</a> <span class="dim small">{esc(i["kind"])} &middot; {esc(i.get("chapter") or "no chapter")}</span></li>' for i in batch)}</ul>
<h3>Chapter by chapter</h3>
<div class="tablewrap"><table><thead><tr><th>Chapter</th><th>What happened</th><th>Words in {esc(prev["version"])}</th><th>Words in {esc(cand["version"])}</th></tr></thead><tbody>{"".join(ch_rows)}</tbody></table></div>""")
    def cand_row(c):
        fz = ROOT / c["frozen"]
        if c.get("in_progress") and not fz.exists():
            return f'<tr><td><b>{esc(c["version"])}</b></td><td>{esc(c["date"])}</td><td>{esc(c.get("title", ""))}</td><td colspan="3"><span class="st in-progress">being written</span> {esc(c.get("what", ""))}</td></tr>'
        chs = _chapters_of_frozen(fz.read_text(encoding="utf-8")) if fz.exists() else [(0, c["title"], c["words"]) for c in book["chapters"]]
        return (f'<tr><td><b>{esc(c["version"])}</b></td><td>{esc(c["date"])}</td><td>{esc(c.get("title", ""))}</td><td>{len(chs)}</td><td>{sum(w for _, _, w in chs):,}</td>'
                f'<td>{("<a href=\"../../" + esc(c["frozen"]) + "\">frozen</a>") if fz.exists() else "this build"}</td></tr>')
    cand_rows = "".join(cand_row(c) for c in cands)
    body = f"""<h1>The rounds</h1>
<p class="lede">The book in release mode (decision 008): a release candidate, then a round that takes one pile of material and ends in the next candidate, until the rounds shrink from parts to sentences. This page is the librarian's count of each round by size, the ideas that came in, and the diff Dinis reads.</p>
{notice}
<h2>The candidates</h2>
<div class="tablewrap"><table><thead><tr><th>Candidate</th><th>Date</th><th>Title</th><th>Chapters</th><th>Words</th><th>Text</th></tr></thead><tbody>{cand_rows}</tbody></table></div>
{"".join(rows) or "<p class=dim>The first candidate; no round yet.</p>"}
<p class="small dim">Chapter maps: the current one is <code>admin/content/graph/chapters.json</code>, the rc1 one is kept as <code>chapters-rc1.json</code>. The block diff uses the newsroom's <code>page_versions.diff</code>, the same differ as the versions page.</p>
"""
    page(OUT + "rounds.html", "The rounds", body, "Release candidate by release candidate: what each round added, changed and removed, by size, the ideas that came in, and the diff.",
         crumbs=((short, OUT + "index.html"), ("The rounds", OUT + "rounds.html")))
    if prev:
        dbody = f"""<h1>The diff: {esc(prev["version"])} to {esc(cand["version"])}</h1>
<p class="lede">Every block of the candidate that changed, was added or was removed since the one before, as the newsroom's differ reads it. {"".join(f"{v:,} {esc(k)}; " for k, v in sizes.items() if k.startswith("blocks"))}</p>
{notice}
<div class="pv-diff">{diff_html}</div>
"""
        page(OUT + "diff.html", f"The diff, {prev['version']} to {cand['version']}", dbody, "The block-by-block diff between the last two release candidates, for Dinis to read.",
             crumbs=((short, OUT + "index.html"), ("The rounds", OUT + "rounds.html"), ("The diff", OUT + "diff.html")))
