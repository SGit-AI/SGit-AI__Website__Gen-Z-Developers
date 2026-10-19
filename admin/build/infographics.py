#!/usr/bin/env python3
"""infographics/: the book's infographics, what exists, the plan, the drawn ones and the review. Called by build.py
after the release candidate is built (it reads v2/book/book.json), with its helpers (page, write, esc, md, graph).

Sources (admin/content/infographics/):
  plan.json         the proposals: one per infographic, with its altitude (book, part, chapter, idea), target, form,
                    method, priority, state, what it shows and why, the elements on it, the quotes, sources and ideas
  drawn/<id>.json   a drawn infographic's spec, rendered to SVG by infographic_svg.py
  v1-figures.json   every image of the 2018 book, what it is, whose it is, and the recommendation
  newsroom.json     the newsroom's figures in the articles the book draws on (catalogued from graphs.json)

The build refuses: a proposal with an unknown altitude, form, method or state, a target that is not the book, a part,
a chapter of the candidate or a 2018 file, a source that is not a node of the graph, an idea not in the register, a
quote not word for word in its chapter; a decided state (accepted, changes, declined, deferred) without decided_by; a
drafted proposal without a drawing, and a drawing without its proposal; a drawing whose checked lines are not word for
word in its source; and a 2018 image the text references with no row in v1-figures.json.

Writes infographics/index.html, plan.html, existing.html, how.html, drawn/<id>.html, svg/<id>.svg, and the data
beside them for agents: plan.json, drawn/<id>.json.
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import infographic_svg as svg
from readers_pages import quote_in

ROOT = Path(__file__).resolve().parents[2]
IG = ROOT / "admin/content/infographics"
DECIDED = ("accepted", "changes", "declined", "deferred")
REVIEW_KEY = "genz.infographics.v1"


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def body_of(path):
    t = Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\s*\n.*?\n---\s*\n?(.*)$", t, re.S)
    return m.group(1) if m else t


# ------------------------------------------------------------------ the candidate, as the plan needs it
def candidate():
    doc = load_json(ROOT / "v2/book/book.json")
    parts = {p["slug"]: {"slug": p["slug"], "title": p["title"], "n": i + 1, "chapters": []} for i, p in enumerate(doc["parts"])}
    chapters = {}
    for c in doc["chapters"]:
        ch = {"slug": c["slug"], "number": c["number"], "title": c["title"], "part": c["part"], "words": c["words"], "url": c["url"], "file": c["file"]}
        chapters[c["slug"]] = ch
        parts[c["part"]]["chapters"].append(ch)
    # the front matter is a target too (number 0, in no part), so a proposal can be about it
    f = doc["front"]
    fp = next((ROOT / "v2/content/0-front").glob(f"*__{f['slug']}.md"), None)
    if fp:
        chapters[f["slug"]] = {"slug": f["slug"], "number": 0, "title": f["title"], "part": "book", "words": f["words"], "url": f["url"], "file": fp.relative_to(ROOT).as_posix()}
    return doc, parts, chapters


def part_text(slug, parts):
    """A part's own words: its intro and every chapter in it, for checking a part-level proposal's quotes."""
    d = next((ROOT / "v2/content").glob(f"*-{slug}"), None)
    texts = [(d / "_index.md").read_text(encoding="utf-8")] if d and (d / "_index.md").exists() else []
    return "\n\n".join(texts + [(ROOT / c["file"]).read_text(encoding="utf-8") for c in parts[slug]["chapters"]])


def readers_by_chapter():
    """Mean interest and put-down points per chapter, from the synthetic readers' runs (the latest study)."""
    studies = sorted(p for p in (ROOT / "admin/content/readers").iterdir() if p.is_dir())
    if not studies:
        return {}, None
    study = studies[-1]
    interest, down = defaultdict(list), Counter()
    for f in sorted((study / "runs").glob("*.json")):
        run = load_json(f)
        for s in run["steps"]:
            if s["unit"].startswith("ch:") and s.get("mode") != "skip" and isinstance(s.get("interest"), int):
                interest[int(s["unit"][3:])].append(s["interest"])
        pd = run.get("put_down") or {}
        if isinstance(pd, dict) and str(pd.get("unit", "")).startswith("ch:"):
            down[int(pd["unit"][3:])] += 1
    return {n: (sum(v) / len(v), down.get(n, 0)) for n, v in interest.items()} | {n: (None, k) for n, k in down.items() if n not in interest}, study.name


# ------------------------------------------------------------------ checks
def check(plan, drawn, v1doc, parts, chapters, graph):
    E = []
    nodes = graph["nodes"]
    ideas = {i["id"] for i in graph["ideas_doc"]["ideas"]}
    ids = Counter(p["id"] for p in plan["proposals"])
    E += [f"plan.json: proposal id {i} appears {n} times" for i, n in ids.items() if n > 1]
    for p in plan["proposals"]:
        w = f"plan.json: {p['id']}"
        if p["altitude"] not in plan["altitudes"]: E.append(f"{w}: unknown altitude {p['altitude']}")
        if p["form"] not in plan["forms"]: E.append(f"{w}: unknown form {p['form']}")
        if p["method"] not in plan["methods"]: E.append(f"{w}: unknown method {p['method']}")
        if p["state"] not in plan["states"]: E.append(f"{w}: unknown state {p['state']}")
        if p.get("priority") not in (1, 2, 3): E.append(f"{w}: priority must be 1, 2 or 3")
        if not p.get("elements"): E.append(f"{w}: no elements: a proposal says what is on it")
        t = p["target"]
        if t == "book":
            pass
        elif t.startswith("part:"):
            if t[5:] not in parts: E.append(f"{w}: target {t} is not a part of the candidate")
        elif t.startswith("book:"):
            if not (ROOT / "v1/content" / t[5:]).exists(): E.append(f"{w}: target {t} is not a 2018 file")
        elif t not in chapters:
            E.append(f"{w}: target {t} is not a chapter of the candidate")
        for s in p.get("sources", []):
            if s not in nodes: E.append(f"{w}: source {s} is not a node of the graph")
        for i in p.get("ideas", []):
            if i not in ideas: E.append(f"{w}: idea {i} is not in the register")
        if p.get("quotes"):
            if t in chapters or (t.startswith("part:") and t[5:] in parts):
                text = (ROOT / chapters[t]["file"]).read_text(encoding="utf-8") if t in chapters else part_text(t[5:], parts)
                for q in p["quotes"]:
                    if not quote_in(q, text): E.append(f"{w}: quote not word for word in {t}: {q[:70]}")
            else:
                E.append(f"{w}: quotes are checked against a chapter or a part; this proposal targets {t}")
        if p["state"] in DECIDED and not p.get("decided_by"): E.append(f"{w}: state {p['state']} needs decided_by (who decided, and where)")
        if p["state"] == "drafted" and p.get("drawn") not in drawn: E.append(f"{w}: drafted, but there is no drawn/{p.get('drawn')}.json")
        if p.get("drawn") and p["drawn"] in drawn and drawn[p["drawn"]]["proposal"] != p["id"]: E.append(f"{w}: drawn/{p['drawn']}.json names proposal {drawn[p['drawn']]['proposal']}")
    by_id = {p["id"]: p for p in plan["proposals"]}
    for d in drawn.values():
        w = f"drawn/{d['id']}.json"
        p = by_id.get(d["proposal"])
        if not p: E.append(f"{w}: proposal {d['proposal']} is not in plan.json"); continue
        if p.get("drawn") != d["id"]: E.append(f"{w}: its proposal {p['id']} does not point back at it")
        if d["form"] not in svg.FORMS: E.append(f"{w}: the code cannot draw form {d['form']}")
        src = d.get("quote_source") or (chapters[p["target"]]["file"] if p["target"] in chapters else None)
        if d.get("checked"):
            if not src: E.append(f"{w}: checked lines but no quote_source"); continue
            text = (ROOT / src).read_text(encoding="utf-8")
            for q in d["checked"]:
                if not quote_in(q, text): E.append(f"{w}: checked line not word for word in {src}: {q[:70]}")
    # the 2018 figures: every reference in the text has a row, every row an image (the never-generated three excepted)
    rows = {r["image"] for r in v1doc["figures"]}
    for f in sorted((ROOT / "v1/content").rglob("*.md")):
        for ref in re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", f.read_text(encoding="utf-8")):
            if ref not in rows: E.append(f"v1-figures.json: no row for {ref}, referenced in v1/content/{f.relative_to(ROOT / 'v1/content').as_posix()}")
    for r in v1doc["figures"]:
        if r["recommendation"] not in v1doc["recommendations"]: E.append(f"v1-figures.json: {r['image']}: unknown recommendation")
        if r["kind"] != "missing" and not (ROOT / "v1" / r["image"]).exists(): E.append(f"v1-figures.json: {r['image']} is not in v1/")
        if r.get("v2") and r["v2"] not in chapters: E.append(f"v1-figures.json: {r['image']}: v2 chapter {r['v2']} does not exist")
        if r.get("proposal") and r["proposal"] not in by_id: E.append(f"v1-figures.json: {r['image']}: proposal {r['proposal']} does not exist")
    return E


# ------------------------------------------------------------------ pages
def build_infographics(ctx):
    page, write, esc, md, graph = ctx["page"], ctx["write"], ctx["esc"], ctx["md"], ctx["graph"]
    plan = load_json(IG / "plan.json")
    v1doc = load_json(IG / "v1-figures.json")
    news = load_json(IG / "newsroom.json")
    drawn = {f.stem: load_json(f) for f in sorted((IG / "drawn").glob("*.json"))}
    doc, parts, chapters = candidate()
    E = check(plan, drawn, v1doc, parts, chapters, graph)
    if E:
        raise SystemExit("build: the infographics refuse:\n  - " + "\n  - ".join(E))
    props = plan["proposals"]
    by_id = {p["id"]: p for p in props}
    nodes = graph["nodes"]
    manifest = {c["file"]: c["page"] for c in load_json(ROOT / "v1/book/manifest.json")["chapters"]}
    head = '<link rel="stylesheet" href="{up}assets/infographics.css">\n'

    # the drawings: the bookmap is filled from the candidate and the study; the rest are as authored
    interest, study = readers_by_chapter()
    for d in drawn.values():
        if d["form"] == "bookmap":
            d["parts"] = [{"title": p["title"], "chapters": [{
                "number": c["number"], "short": c["title"].split(":")[0], "words": c["words"],
                "interest": interest.get(c["number"], (None, 0))[0], "put_down": interest.get(c["number"], (None, 0))[1],
                "placeholder": c["words"] < 700} for c in p["chapters"]]} for p in parts.values()]
            d["words"] = sum(c["words"] for c in chapters.values())
        d["stamp"] = {"drafted": "drafted by code, not reviewed"}.get(by_id[d["proposal"]]["state"], by_id[d["proposal"]]["state"])
        write(f"infographics/svg/{d['id']}.svg", svg.render(d))

    # ---- helpers
    def target_link(p, up="../"):
        t = p["target"]
        if t == "book":
            return f'<a href="{up}v2/book/index.html">the whole book</a>'
        if t.startswith("part:"):
            pt = parts[t[5:]]
            return f'<a href="{up}v2/book/index.html">part {pt["n"]}, {esc(pt["title"])}</a>'
        if t.startswith("book:"):
            f = t[5:]
            return (f'<a href="{up}{manifest[f]}">the 2018 file {esc(f)}</a>' if f in manifest else f'the 2018 file <code>{esc(f)}</code>')
        c = chapters[t]
        return f'<a href="{up}{c["url"]}">ch. {c["number"]}, {esc(c["title"])}</a>'

    def part_of(p):
        t = p["target"]
        if t.startswith("part:"):
            return t[5:]
        if t in chapters:
            return chapters[t]["part"]
        return "book"

    def src_link(s, up="../"):
        n = nodes[s]
        url = n.get("url") or ""
        href = url if url.startswith("http") else (up + url if url else "")
        label = n.get("title") or s
        return f'<a href="{esc(href)}" title="{esc(s)}">{esc(label[:80])}</a>' if href else esc(label)

    news_by_article = defaultdict(list)
    for f in news["figures"]:
        news_by_article[f["article_slug"]].append(f)

    def news_for(p):
        """The newsroom figures in the articles a proposal draws on: the pinned match first."""
        out, seen = [], set()
        if p.get("newsroom"):
            m = next((f for f in news["figures"] if f["image_url"] == p["newsroom"]), None)
            if m:
                out.append(m); seen.add(m["image_url"])
        for s in p.get("sources", []):
            if s.startswith("news:"):
                for f in news_by_article.get(s[5:], []):
                    if f["image_url"] not in seen and f.get("context") != "in-pictures slide deck view":
                        out.append(f); seen.add(f["image_url"])
        return out

    def chip(cls, label):
        return f'<span class="ig-chip {cls}">{esc(label)}</span>'

    def card(p, up="../"):
        d = drawn.get(p.get("drawn"))
        figs = news_for(p)
        el = "".join(f'<li><b>{esc(e["label"])}</b>{(": " + esc(e["detail"])) if e.get("detail") else ""}</li>' for e in p["elements"])
        qs = "".join(f'<blockquote class="q">{esc(q)} <span class="ok" title="checked word for word against the chapter by the build">&#10003; in the chapter</span></blockquote>' for q in p.get("quotes", []))
        srcs = ", ".join(src_link(s, up) for s in p.get("sources", [])) or '<span class="dim">none named</span>'
        ids_ = ", ".join(f'<a href="{up}graph/ideas/{esc(i)}.html">{esc(i)}</a>' for i in p.get("ideas", [])) or '<span class="dim">none</span>'
        pic = (f'<a class="ig-thumb" href="{up}infographics/drawn/{d["id"]}.html"><img src="{up}infographics/svg/{d["id"]}.svg" alt="{esc(d.get("alt", d["title"]))}" loading="lazy"></a>' if d else "")
        nf = ""
        if figs:
            pin = figs[0] if p.get("newsroom") else None
            thumbs = "".join(f'<a href="{esc(f["image_url"])}" title="{esc((f.get("alt") or "")[:300])}"><img src="{esc(f["image_url"])}" alt="{esc((f.get("alt") or "a newsroom figure")[:300])}" loading="lazy"></a>' for f in figs[:6])
            nf = (f'<details class="ig-news"><summary>{"<b>A newsroom figure already draws this.</b> " if pin else ""}{len(figs)} newsroom figure{"s" if len(figs) != 1 else ""} in the articles it draws on</summary>'
                  f'<div class="ig-news-row">{thumbs}</div><p class="small dim">Reuse it, redraw it in the book\'s palette, or leave it to the article. The images stay on newsroom.sgit.ai.</p></details>')
        data = " ".join(f'data-{k}="{esc(v)}"' for k, v in (("id", p["id"]), ("altitude", p["altitude"]), ("part", part_of(p)), ("form", p["form"]), ("method", p["method"]), ("priority", p["priority"]), ("state", p["state"]), ("target", p["target"])))
        dec = f'<p class="small"><b>Decided by:</b> {esc(p["decided_by"])}</p>' if p.get("decided_by") else ""
        return f"""<article class="ig-card" id="{esc(p['id'])}" {data}>
<div class="ig-card-head"><h3><a href="#{esc(p['id'])}">{esc(p['title'])}</a></h3>
<p class="ig-chips">{chip('alt', p['altitude'])}{chip('form', p['form'])}{chip('m-' + p['method'], p['method'])}{chip('p' + str(p['priority']), 'priority ' + str(p['priority']))}{chip('st-' + p['state'], p['state'])}</p>
<p class="small ig-target">For {target_link(p, up)} &middot; <code>{esc(p['id'])}</code></p></div>
{pic}
<p><b>What it shows.</b> {esc(p['shows'])}</p>
<p><b>Why.</b> {esc(p['why'])}</p>
<details class="ig-el"><summary>What is on it ({len(p['elements'])})</summary><ul>{el}</ul></details>
{qs}
<p class="small"><b>Sources:</b> {srcs} &middot; <b>Ideas:</b> {ids_}</p>
{('<p class="small ig-notes"><b>Notes.</b> ' + esc(p['notes']) + '</p>') if p.get('notes') else ''}{dec}
{nf}
<div class="ig-review" data-for="{esc(p['id'])}"></div>
</article>"""

    counts = {"proposals": len(props), "drawn": len(drawn), "by_state": Counter(p["state"] for p in props), "by_altitude": Counter(p["altitude"] for p in props),
              "by_method": Counter(p["method"] for p in props), "by_priority": Counter(p["priority"] for p in props), "by_form": Counter(p["form"] for p in props),
              "chapters_covered": len({p["target"] for p in props if p["target"] in chapters and chapters[p["target"]]["number"]}), "chapters": sum(1 for c in chapters.values() if c["number"]),
              "v1": Counter(r["recommendation"] for r in v1doc["figures"]), "news": len(news["figures"]), "news_articles": len({f["article_slug"] for f in news["figures"]})}

    # ---- the plan, with the review
    per_ch = Counter(p["target"] for p in props)
    cells = []
    for pt in parts.values():
        cs = "".join(f'<button type="button" class="ig-cell n{min(per_ch.get(c["slug"], 0), 3)}" data-filter-target="{c["slug"]}" title="ch. {c["number"]}, {esc(c["title"])}: {per_ch.get(c["slug"], 0)} proposal(s)">{c["number"]}</button>' for c in pt["chapters"])
        pp = per_ch.get("part:" + pt["slug"], 0)
        cells.append(f'<div class="ig-cov-part"><button type="button" class="ig-ptitle{" has" if pp else ""}" data-filter-part="{pt["slug"]}" title="filter to this part">{pt["n"]}. {esc(pt["title"])}{" &middot; part view" if pp else ""}</button><div>{cs}</div></div>')
    sel = lambda name, opts: (f'<label>{name} <select data-filter="{name.lower()}"><option value="">all</option>' + "".join(f'<option value="{esc(v)}">{esc(l)}</option>' for v, l in opts) + "</select></label>")
    filters = (sel("Altitude", [(a, a) for a in plan["altitudes"]]) + sel("Part", [("book", "the whole book")] + [(pt["slug"], f'{pt["n"]}. {pt["title"]}') for pt in parts.values()])
               + sel("Form", [(f, f) for f in plan["forms"]]) + sel("Method", [(m, m) for m in plan["methods"]]) + sel("Priority", [("1", "1"), ("2", "2"), ("3", "3")])
               + sel("State", [(s, s) for s in plan["states"]]) + sel("Verdict", [("none", "not reviewed yet"), ("accept", "accept"), ("change", "change"), ("decline", "decline"), ("later", "later")]))
    order = sorted(props, key=lambda p: ({"book": 0, "part": 1, "idea": 2, "chapter": 3}[p["altitude"]], chapters[p["target"]]["number"] if p["target"] in chapters else (parts[p["target"][5:]]["n"] if p["target"].startswith("part:") else 0), p["priority"]))
    body = f"""<h1>The plan</h1>
<p class="lede">Every infographic proposed for the book: {counts['proposals']} of them, {counts['drawn']} drawn already as prototypes. Read a card, look at the drawing where there is one, and give your verdict: <b>accept</b>, <b>change</b> (say what), <b>decline</b> (say why) or <b>later</b>. Your verdicts stay in this browser until you export them; nothing is sent anywhere.</p>
<div class="ig-review-bar" id="ig-bar" data-store="{REVIEW_KEY}" data-site="{esc(ctx['version'])}" data-candidate="{esc(doc['version'])}"></div>
<h2 id="coverage">Where they go</h2>
<p class="small dim">Each square is a chapter of {esc(doc['version'])}, shaded by how many infographics are proposed for it; click one, or a part, to see only those. A part with its own view says so.</p>
<div class="ig-cov">{''.join(cells)}</div>
<h2 id="proposals">The proposals</h2>
<div class="ig-filters">{filters}<button type="button" class="btn" id="ig-clear">Show all</button> <span class="small dim" id="ig-shown"></span></div>
<div class="ig-cards">{''.join(card(p) for p in order)}</div>
<script src="../assets/infographics.js"></script>"""
    page("infographics/plan.html", "The infographics plan", body, f"{counts['proposals']} infographics proposed for Generation ZX Developers, by altitude and chapter, with a review: accept, change, decline or later.",
         crumbs=(("Infographics", "infographics/index.html"), ("The plan", "infographics/plan.html")), extra_head=head.format(up="../"), wide=True)

    # ---- the drawn ones, a page each
    for d in drawn.values():
        p = by_id[d["proposal"]]
        rel = f"infographics/drawn/{d['id']}.html"
        chk = "".join(f'<li>&ldquo;{esc(q)}&rdquo; <span class="ok">&#10003;</span></li>' for q in d.get("checked", []))
        src = d.get("quote_source") or (chapters[p["target"]]["file"] if p["target"] in chapters else "")
        computed = ' It is computed: the build fills it from the release candidate and the readers\' study on every run, so it cannot fall out of date.' if d["form"] == "bookmap" else ""
        body = f"""<p class="kicker">infographic &middot; {esc(p['altitude'])} &middot; {esc(d['form'])} &middot; {esc(p['state'])}</p>
<h1>{esc(d['title'])}</h1>
<p class="small">For {target_link(p, '../../')} &middot; proposal <a href="../plan.html#{esc(p['id'])}"><code>{esc(p['id'])}</code></a> in the plan</p>
<figure class="ig-figure"><img src="../svg/{d['id']}.svg" alt="{esc(d.get('alt', d['title']))}"><figcaption>{esc(d.get('alt', ''))}</figcaption></figure>
<p class="ctas"><a class="btn" href="../svg/{d['id']}.svg" download>The SVG</a> <a class="btn" href="{d['id']}.json">The data</a> <a class="btn primary" href="../plan.html#{esc(p['id'])}">Review it in the plan</a></p>
<div class="twocol"><div>
<h2>What it is for</h2><p>{esc(p['why'])}</p>
<h2>How it is made</h2><p>Drawn by <code>admin/build/infographic_svg.py</code> from <code>admin/content/infographics/drawn/{d['id']}.json</code>, as a <b>{esc(d['form'])}</b>.{computed} Change the data and rebuild; the picture follows. It keeps the book's colours in every theme of this site, because it is a printed picture: the same file goes into the PDF.</p>
{('<h2>Notes</h2><p>' + esc(p['notes']) + '</p>') if p.get('notes') else ''}
</div><div>
<h2>Checked against the source</h2>
{('<p class="small">Every line below is on the drawing or behind it, and the build found each one word for word in <code>' + esc(src) + '</code>. A line changed in the chapter and not here stops the release.</p><ul class="small">' + chk + '</ul>') if chk else '<p class="small dim">Nothing on this drawing quotes the text; its numbers and labels come from the data named under it.</p>'}
</div></div>"""
        page(rel, d["title"], body, f"Infographic, drafted by code: {d['title']}.", crumbs=(("Infographics", "infographics/index.html"), ("Drawn", "infographics/index.html#drawn"), (d["title"], rel)),
             extra_head=head.format(up="../../"), wide=True)
        write(f"infographics/drawn/{d['id']}.json", (IG / "drawn" / f"{d['id']}.json").read_text(encoding="utf-8"))
    write("infographics/plan.json", (IG / "plan.json").read_text(encoding="utf-8"))

    # ---- what exists
    rec_order = {"keep": 0, "redraw": 1, "replace": 2, "drop": 3, "history": 4}
    v1rows = ""
    for r in sorted(v1doc["figures"], key=lambda r: (rec_order[r["recommendation"]], r.get("file") or "~")):
        img = (f'<img src="../v1/{esc(r["image"])}" alt="{esc(r["what"])}" loading="lazy">' if r["kind"] != "missing" else '<span class="ig-missing">never generated</span>')
        f = r.get("file")
        where = (f'<a href="../{manifest[f]}">{esc(f)}</a>' if f in manifest else (f'<code>{esc(f)}</code>' if f else '<span class="dim">not referenced</span>'))
        v2 = f'<a href="../{chapters[r["v2"]]["url"]}">ch. {chapters[r["v2"]]["number"]}</a>' if r.get("v2") else ""
        pr = f' &middot; <a href="plan.html#{esc(r["proposal"])}">drawn</a>' if r.get("proposal") else ""
        v1rows += (f'<tr><td class="ig-tcell">{img}</td><td><b>{esc(r["kind"])}</b><br><span class="small">{where}</span></td><td>{esc(r["what"])}<br><span class="small dim">{esc(r["owner"])}</span></td>'
                   f'<td><span class="ig-chip rec-{r["recommendation"]}">{r["recommendation"]}</span><br><span class="small">{v2}{pr}</span></td><td class="small">{esc(r["why"])}</td></tr>')
    arts = defaultdict(list)
    for f in news["figures"]:
        arts[(f["article_slug"], f["article_title"], bool(f.get("gen_z_book_tag")))].append(f)
    cited = Counter()
    for p in props:
        for f in news_for(p):
            cited[f["image_url"]] += 1
    groups = ""
    for (slug, title, tagged), fs in sorted(arts.items(), key=lambda kv: (not kv[0][2], kv[0][0])):
        th = "".join(f'<figure class="ig-nf{" cited" if cited.get(f["image_url"]) else ""}"><a href="{esc(f["image_url"])}"><img src="{esc(f["image_url"])}" alt="{esc((f.get("alt") or "")[:300])}" loading="lazy"></a>'
                     f'<figcaption>{esc(f.get("kind") or "")}{" &middot; deck" if f.get("context") == "in-pictures slide deck view" else ""}{(" &middot; <b>behind " + str(cited[f["image_url"]]) + " proposal" + ("s" if cited[f["image_url"]] > 1 else "") + "</b>") if cited.get(f["image_url"]) else ""}</figcaption></figure>' for f in fs)
        groups += (f'<details class="ig-art"{" open" if tagged else ""}><summary><b>{esc(title.split(":")[0])}</b> <span class="small dim">{len(fs)} figure{"s" if len(fs) != 1 else ""}{" &middot; tagged gen-z-book" if tagged else ""}</span></summary>'
                   f'<p class="small"><a href="https://newsroom.sgit.ai/articles/{esc(slug)}.html">The article on newsroom.sgit.ai &rarr;</a></p><div class="ig-nf-row">{th}</div></details>')
    sb = []
    for f in sorted((ROOT / "admin/content/storyboards").glob("[0-9]*.json")):
        s = load_json(f)
        ev = [i for i, sc in enumerate(s.get("scenes", []), 1) if sc.get("kind") in ("evidence", "spectrum", "graph")]
        if ev:
            sb.append(f'<li><a href="../storyboards/{s["slug"]}.html">{esc(s["title"])}</a>: {len(ev)} panel{"s" if len(ev) != 1 else ""} that already work as an infographic (panels {", ".join(map(str, ev))})</li>')
    c1 = counts["v1"]
    body = f"""<h1>What exists</h1>
<p class="lede">Before proposing anything new: every picture the 2018 book has, the newsroom's figures in the articles the second edition draws on, and the storyboard panels that already work as infographics.</p>
<h2 id="v1">The 2018 book: {len(v1doc['figures'])} images</h2>
<p>Looked at one by one. Most are screenshots of 2018 tools; the few real infographics are someone else's (a Radical Candor quadrant, sixteen personality types, the Big Five, Wikipedia's licence table), and three figures the text links were never generated. The recommendation is for the working copy and the next candidate; <code>v1/</code> is frozen and does not change. <b>{c1.get('keep', 0)} keep, {c1.get('redraw', 0)} redraw, {c1.get('replace', 0)} replace, {c1.get('drop', 0)} drop, {c1.get('history', 0)} kept as the 2018 record.</b></p>
<div class="tablewrap"><table class="ig-v1"><thead><tr><th>Image</th><th>Kind, where</th><th>What it is, whose</th><th>Do</th><th>Why</th></tr></thead><tbody>{v1rows}</tbody></table></div>
<h2 id="newsroom">The newsroom: {counts['news']} figures in {counts['news_articles']} articles</h2>
<p>The six articles tagged <code>gen-z-book</code> have only eight figures between them; the rest are in the articles the startup edition draws on. Almost all are drawn by code (Mermaid, SVG, a renderer with fixed layouts, as the newsroom's <a href="https://newsroom.sgit.ai/articles/the-infographic-bake-off.html">The infographic bake-off</a> says), off-white, teal for the new way, grey for the old, red for risk. A figure marked <b>behind a proposal</b> is in an article a proposal draws on: reuse it, redraw it in the book's palette, or leave it to the article. The images stay on the newsroom and load from there.</p>
{groups}
<h2 id="storyboards">The storyboards</h2>
<p>Panels drawn by <code>assets/storyboard.js</code> from data, some of which are already infographics: evidence cards (a pinned quote or a bar chart), spectrums and graphs. A proposal that is a sequence of scenes with people is a storyboard, not an infographic, and is left to them.</p>
<ul>{''.join(sb)}</ul>
<p class="small dim">Data: <code>admin/content/infographics/v1-figures.json</code> and <code>newsroom.json</code>, catalogued on {esc(news['catalogued_on'])} from <a href="{esc(news['source'])}">the newsroom's graphs.json</a>.</p>"""
    page("infographics/existing.html", "What exists", body, f"The {len(v1doc['figures'])} images of the 2018 book with a recommendation each, and {counts['news']} newsroom figures in the articles the book draws on.",
         crumbs=(("Infographics", "infographics/index.html"), ("What exists", "infographics/existing.html")), extra_head=head.format(up="../"), wide=True)

    # ---- how they are made, and how to review
    sw = "".join(f'<span class="ig-sw" style="background:{svg.COVER[c]}"></span><code>{c} {svg.COVER[c]}</code> ' for c in ("navy", "teal", "green", "yellow", "red"))
    forms_drawn = ", ".join(f"<code>{f}</code>" for f in svg.FORMS)
    meth = "".join(f'<li><b>{esc(k)}</b>: {esc(v)} <span class="small dim">({counts["by_method"].get(k, 0)} proposed)</span></li>' for k, v in plan["methods"].items())
    states = "".join(f'<li><b>{esc(k)}</b>: {esc(v)} <span class="small dim">({counts["by_state"].get(k, 0)})</span></li>' for k, v in plan["states"].items())
    body = f"""<h1>How they are made, and how to review them</h1>
<p class="lede">The infographics follow the rules the rest of this site follows: the source of truth is data in the repository, the picture is generated from it, and the build refuses what it can check is wrong.</p>
<h2 id="altitudes">Four altitudes</h2>
<p>The brief for the second edition asked for <i>an infographic at every altitude</i>: the whole book on one page, a view per part, an infographic per chapter and how they connect, the graph of each area. Every proposal names its altitude: {', '.join(f'<b>{a}</b> ({counts["by_altitude"].get(a, 0)})' for a in plan['altitudes'])}.</p>
<h2 id="methods">Methods</h2>
<ul>{meth}</ul>
<p>Every chapter proposal came back as code, and that is the right default: an infographic in this book shows a structure (a loop, a test, a sum, who can read what), and structure drawn from data stays correct when the text changes. Image models earn their place where a mood matters more than a structure: the part openers are proposed that way, for Dinis to decide.</p>
<h2 id="drawing">The drawing</h2>
<ul>
<li><b>Data.</b> <code>admin/content/infographics/drawn/&lt;id&gt;.json</code>: a form, a kicker, a title, a subtitle, the items, a source line and the alt text. The forms the code draws today: {forms_drawn}.</li>
<li><b>Code.</b> <code>admin/build/infographic_svg.py</code> turns a spec into a standalone SVG, 1600 pixels wide, with no browser and no library; the same spec gives the same file. <code>python3 admin/build/infographic_png.py</code> makes PNGs on demand, for a slide or a post.</li>
<li><b>Palette.</b> The 2018 cover's: {sw} on the storyboards' cream paper <code>{svg.PAPER}</code>. Navy is the answer, teal the way through, green what works, yellow a caution, red a risk or a loss. Struck through is gone; a navy tag says new. A dashed box is a placeholder or something on someone else's side.</li>
<li><b>Type.</b> One sans family, bold for labels, regular for details; nothing under 17 pixels at 1600 wide, so it reads at half size on a page.</li>
<li><b>The footer</b> names the source and the state: <i>drafted by code, not reviewed</i>, until Dinis has reviewed it.</li>
<li><b>Printed pictures.</b> Like the storyboard panels, an infographic keeps its own colours in every theme of this site: it is the file that goes into the PDF.</li>
</ul>
<h2 id="rules">What the build refuses</h2>
<ul>
<li>A quote on a proposal, or a checked line on a drawing, that is not word for word in its chapter. The chapter is the authority; when it changes, the drawing has to change with it or the release stops.</li>
<li>A proposal for a chapter, part, 2018 file, source or idea that does not exist; an unknown form, method or state.</li>
<li>A decision without a name: a proposal marked accepted, changes, declined or deferred must say who decided and where.</li>
<li>A proposal marked drafted with no drawing, and a drawing with no proposal.</li>
<li>A 2018 image the text references with no row in the inventory.</li>
</ul>
<h2 id="states">States</h2>
<ul>{states}</ul>
<h2 id="review">How to review</h2>
<ol>
<li><b>Open <a href="plan.html">the plan</a></b>, on a laptop or an iPad. Start with the drawn ones (filter <i>State: drafted</i>), then priority 1.</li>
<li><b>For each card</b>, press accept, change, decline or later, and write a line if you want: what to change, why not. It is kept in your browser only.</li>
<li><b>Export</b> the review as markdown or JSON from the bar at the top of the plan, and put it in the vault's <code>reviews/</code> folder, or hand it to the agent.</li>
<li><b>The agent records it</b>: each verdict becomes the proposal's state, with <code>decided_by</code> naming you and the review file, in the next release. Accepted ones are drawn; changed ones redrawn; declined ones kept with the reason, so nobody proposes them again.</li>
</ol>
<p class="small dim">Data: <a href="plan.json">plan.json</a>. The agent that keeps it: <a href="../team/illustrator/index.html">the illustrator</a>.</p>"""
    page("infographics/how.html", "How they are made", body, "How the book's infographics are drawn from data, the palette, what the build refuses, and how to review them.",
         crumbs=(("Infographics", "infographics/index.html"), ("How they are made", "infographics/how.html")), extra_head=head.format(up="../"))

    # ---- the hub
    gal = "".join(f'<a class="ig-gal" href="drawn/{d["id"]}.html"><img src="svg/{d["id"]}.svg" alt="{esc(d.get("alt", d["title"]))}" loading="lazy"><span><b>{esc(d["title"])}</b><br><span class="small dim">{esc(d.get("kicker", ""))}</span></span></a>'
                  for d in sorted(drawn.values(), key=lambda d: (d["form"] != "bookmap", chapters[by_id[d["proposal"]]["target"]]["number"] if by_id[d["proposal"]]["target"] in chapters else 0)))
    bm = next((d for d in drawn.values() if d["form"] == "bookmap"), None)
    s = counts["by_state"]
    body = f"""<h1>Infographics</h1>
<p class="lede">The book at every altitude, as pictures: what exists, what is proposed, what is drawn, and the review that decides which go into the next candidate. Drawn from data by code, checked against the text by the build, and nothing in the book until Dinis says so.</p>
<p class="stats"><span class="stat"><b>{counts['proposals']}</b><span>proposed</span></span><span class="stat"><b>{counts['drawn']}</b><span>drawn</span></span><span class="stat"><b>{counts['chapters_covered']} of {counts['chapters']}</b><span>chapters covered</span></span><span class="stat"><b>{counts['by_priority'].get(1, 0)}</b><span>priority 1</span></span><span class="stat"><b>{s.get('accepted', 0)}</b><span>accepted</span></span></p>
{('<figure class="ig-figure ig-hero"><a href="drawn/' + bm['id'] + '.html"><img src="svg/' + bm['id'] + '.svg" alt="' + esc(bm.get('alt', '')) + '"></a><figcaption>The top altitude: the whole book on one page, coloured by how the synthetic readers held. <a href="drawn/' + bm['id'] + '.html">Open it &rarr;</a></figcaption></figure>') if bm else ''}
<div class="cards">
<a class="card" href="plan.html"><span class="k">The plan &middot; review here</span><h3>{counts['proposals']} proposals</h3><p>By altitude, part and chapter, each with what it shows, why, what is on it, its sources and the newsroom figures behind it. Accept, change, decline or later, and export.</p></a>
<a class="card" href="existing.html"><span class="k">What exists</span><h3>{len(v1doc['figures'])} images in 2018, {counts['news']} in the newsroom</h3><p>The 2018 book's pictures, looked at one by one, with what to do with each; the newsroom's figures in the articles the book draws on; the storyboard panels that already are infographics.</p></a>
<a class="card" href="how.html"><span class="k">How they are made</span><h3>Data, code, a palette, a gate</h3><p>The four altitudes, the methods, the drawing, the palette, what the build refuses, the states, and how to review.</p></a>
</div>
<h2 id="drawn">Drawn, not reviewed</h2>
<p>{counts['drawn']} prototypes, chosen where the synthetic readers said the book is slowest or most useful, and where the 2018 book has a hole: the whole book on one page; the three figures the 2018 STEM chapter never generated; the chapter the rest of the book is navigated by; the four tests and sums a founder would pin on the wall; the two pictures that explain part 7 to a reader who does not code; and the making-of in one loop.</p>
<div class="ig-gallery">{gal}</div>
<p class="small dim">Written up in <a href="../agent-articles/infographics-at-every-altitude.html">the agent article</a>. Sources: <code>admin/content/infographics/</code>.</p>"""
    page("infographics/index.html", "Infographics", body, f"The book's infographics: {counts['proposals']} proposed, {counts['drawn']} drawn by code, the 2018 figures and the newsroom's, and the review.",
         crumbs=(("Infographics", "infographics/index.html"),), extra_head=head.format(up="../"), wide=True)
    return counts
