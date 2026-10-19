#!/usr/bin/env python3
"""graph/: the pages of the book as a graph, rendered from graph_model.load(). Called by build.py with its helpers
(page, write, esc, md) so every page carries the site's chrome. Writes:
  graph/index.html         the hub: the pipeline, the counts, what is next
  graph/plan.html          the plan: how an article becomes a chapter, the states, the roles, the rules
  graph/ideas/index.html   the ideas register, and graph/ideas/<id>.html for each idea with its provenance
  graph/sources.html       every source and its processing state
  graph/chapters.html      the proposed chapter map, with the ideas and the 2018 files under each chapter
  graph/tasks.html         every task the articles' briefs ask for, with its state and evidence
  graph/view.html          the graph viewer (assets/graph.js over graph/graph.json)
  graph/graph.json         the nodes and edges
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import graph_model
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]  # noqa: E402

GRAV = {"explorer": ("E", "explorer"), "villager": ("V", "villager"), "town-planner": ("T", "town planner"), "all": ("A", "all three")}


def st(s):
    return f'<span class="st {s}">{s}</span>'


def build_graph(ctx):
    page, write, esc, md = ctx["page"], ctx["write"], ctx["esc"], ctx["md"]
    m = graph_model.load()
    if m["errors"]:
        sys.exit("graph: " + "; ".join(m["errors"]))
    nodes, edges, c = m["nodes"], m["edges"], m["counts"]
    by_from, by_to = defaultdict(list), defaultdict(list)
    for e in edges:
        by_from[e["from"]].append(e)
        by_to[e["to"]].append(e)

    def href(n, up):
        if not n.get("url"):
            return esc(n["title"])
        u = n["url"] if n["url"].startswith("http") else up + n["url"]
        return f'<a href="{esc(u)}">{esc(n["title"])}</a>'

    # ---- graph.json
    write("graph/graph.json", json.dumps({"what": "The book as a graph: every node and edge graph_model.py derives from the files; drawn by assets/graph.js at graph/view.html.",
                                          "counts": c, "nodes": {k: {kk: vv for kk, vv in v.items() if kk not in ("body",)} for k, v in nodes.items()}, "edges": edges}, ensure_ascii=False) + "\n")

    # ---- the ideas register and one page per idea
    ideas = [n for n in nodes.values() if n["kind"] == "idea"]
    chapters = {n["id"][8:]: n for n in nodes.values() if n["kind"] == "chapter"}
    for i in ideas:
        up = "../../"
        prov = "".join(
            f'<li>{href(nodes[s["ref"]], up)}{(" <span class=where>" + esc(s["where"]) + "</span>") if s.get("where") else ""} <span class="small dim">({esc(nodes[s["ref"]].get("source_kind", ""))})</span></li>'
            for s in i["sources"])
        answers = "".join(f'<li>{href(nodes["book:" + f], up)} {st(nodes["book:" + f]["state"])} <span class="small dim">{esc(nodes["book:" + f]["book_kind"])}, {esc(nodes["book:" + f]["part"])}</span></li>' for f in i["answers"]) or "<li class='dim'>none named</li>"
        ch = chapters.get(i.get("chapter"))
        related = [nodes[e["to"]] for e in by_from.get(i["id"], []) if e["kind"] == "idea-in-topic"]
        siblings = [n for n in ideas if n is not i and n.get("chapter") == i.get("chapter")]
        g = GRAV.get(i.get("gravity", "all"), GRAV["all"])
        body = f"""<p class="idea-head"><span class="kind">{esc(i["idea_kind"])}</span> {st(i["state"])} <span class="dest">goes to: <b>{esc(i["destination"])}</b></span> <span class="grav" title="centre of gravity: {g[1]}">{g[0]}</span> <span class="dim">{esc(g[1])}</span></p>
<h1>{esc(i["title"])}</h1>
<p class="statement">{esc(i["statement"])}</p>
{f'<p><b>Decided by.</b> {esc(i["decided_by"])}</p>' if i.get("decided_by") else '<p class="dim"><b>Decided by.</b> Nobody yet: a candidate for Dinis to read, comment on and decide (keep, rewrite, merge, cut, article first, later, not doing it).</p>'}
{f'<p><b>Note.</b> {esc(i["notes"])}</p>' if i.get("notes") else ""}
<h2>Where it comes from</h2>
<ul class="prov">{prov}</ul>
<h2>What it answers in the 2018 book</h2>
<ul class="prov">{answers}</ul>
<h2>Where it goes</h2>
<p>{(f'Chapter <a href="../chapters.html#{esc(ch["id"][8:])}">{esc(ch["title"])}</a>, part <a href="../chapters.html#{esc(ch["part"])}">{esc(nodes["part:" + ch["part"]]["title"])}</a> ({st(ch["state"])}); topic <a href="../../map/newsroom.html#topics">{esc(nodes["topic:" + i["topic"]]["title"]) if i.get("topic") and ("topic:" + i["topic"]) in nodes else ""}</a>.' if ch else 'No chapter proposed yet.')}</p>
{('<p class="small dim">Other ideas proposed for the same chapter: ' + ", ".join(f'<a href="{esc(n["id"][5:])}.html">{esc(n["title"])}</a>' for n in siblings) + '.</p>') if siblings else ""}
<p class="small dim">Node <code>{esc(i["id"])}</code> in <a href="../graph.json">graph.json</a>; <a href="../view.html#{esc(i["id"])}">see it in the graph</a>. Source: <code>admin/content/graph/ideas.json</code>.</p>
"""
        page(f"graph/ideas/{i['id'][5:]}.html", i["title"], body, i["statement"][:160], crumbs=(("The graph", "graph/index.html"), ("Ideas", "graph/ideas/index.html"), (i["title"], f"graph/ideas/{i['id'][5:]}.html")))
    rows = []
    for i in ideas:
        ch = chapters.get(i.get("chapter"))
        srcs = ", ".join(href(nodes[s["ref"]], "../../") for s in i["sources"][:3]) + (f' and {len(i["sources"]) - 3} more' if len(i["sources"]) > 3 else "")
        rows.append(f'<tr data-state="{esc(i["state"])}" data-dest="{esc(i["destination"])}" data-kind="{esc(i["idea_kind"])}"><td><a href="{esc(i["id"][5:])}.html"><b>{esc(i["title"])}</b></a><br><span class="small dim">{esc(i["statement"][:170])}{"…" if len(i["statement"]) > 170 else ""}</span></td>'
                    f'<td><span class="kind">{esc(i["idea_kind"])}</span></td><td>{st(i["state"])}</td><td class="small">{esc(i["destination"])}</td>'
                    f'<td class="small">{(f"<a href=../chapters.html#{esc(ch["id"][8:])}>{esc(ch["title"])}</a>") if ch else "<span class=dim>none</span>"}</td><td class="small">{srcs}</td><td class="small">{len(i["answers"])}</td></tr>')
    chips = "".join(f'<button type="button" class="chip" data-k="state" data-v="{s}" aria-pressed="{str(s == "all").lower()}">{s}</button>' for s in ["all", "candidate", "accepted", "drafting", "signed-off", "declined", "deferred"])
    chips2 = "".join(f'<button type="button" class="chip" data-k="dest" data-v="{s}" aria-pressed="{str(s == "all").lower()}">{s}</button>' for s in ["all", "this-edition", "next-version", "another-book", "the-process", "undecided"])
    body = f"""<h1>The ideas register</h1>
<p class="lede">The core ideas the second edition is made of, one node each: what it says in a sentence, where it comes from (the articles, decisions and memos, with the section), which 2018 chapters it answers, which proposed chapter it goes to, and its state. {c["ideas"]} ideas today: {c["ideas_by_state"].get("accepted", 0)} Dinis has said in his own articles, {c["ideas_by_state"].get("candidate", 0)} candidates waiting on him, {c["ideas_by_state"].get("deferred", 0)} deferred.</p>
<p class="gr-stats">{"".join(f'<span class="stat"><b>{v}</b><span>{esc(k)}</span></span>' for k, v in c["ideas_by_destination"].items())} {"".join(f'<span class="stat"><b>{v}</b><span>{esc(k)}</span></span>' for k, v in c["ideas_by_kind"].items())}</p>
<div class="gr-filters" id="gr-filters"><span class="dim">State</span> {chips} <span class="dim">destination</span> {chips2}</div>
<div class="tablewrap"><table class="ideas" id="ideas"><thead><tr><th>Idea</th><th>Kind</th><th>State</th><th>Goes to</th><th>Chapter</th><th>From</th><th>Answers</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="small dim">An idea is <i>accepted</i> when Dinis said it as his own position in a co-written article; the editor still records it in the vault as a decision on the text. A <i>candidate</i> is the librarian's reading of a newsroom article; it waits for the read, comment, decide loop. Source: <code>admin/content/graph/ideas.json</code>; <a href="../graph.json">graph.json</a>; <a href="../view.html">the graph</a>.</p>
<script>(function(){{var f={{state:'all',dest:'all'}};var box=document.getElementById('gr-filters');box.addEventListener('click',function(ev){{var b=ev.target.closest('.chip');if(!b)return;f[b.dataset.k]=b.dataset.v;box.querySelectorAll('.chip[data-k='+b.dataset.k+']').forEach(function(x){{x.setAttribute('aria-pressed',String(x===b))}});document.querySelectorAll('#ideas tbody tr').forEach(function(tr){{tr.hidden=!((f.state==='all'||tr.dataset.state===f.state)&&(f.dest==='all'||tr.dataset.dest===f.dest))}})}})}})();</script>
"""
    page("graph/ideas/index.html", "The ideas register", body, "The core ideas of the second edition, each with its provenance, its 2018 chapters, its chapter and its state.",
         crumbs=(("The graph", "graph/index.html"), ("Ideas", "graph/ideas/index.html")), wide=True)

    # ---- the chapter map
    parts = m["chapters_doc"]["parts"]
    ideas_by_chapter = defaultdict(list)
    for i in ideas:
        ideas_by_chapter[i.get("chapter")].append(i)
    sections = []
    for p in parts:
        cards = []
        for ch in p["chapters"]:
            g = GRAV.get(ch["gravity"], GRAV["all"])
            ids = "".join(f'<li><a href="ideas/{esc(i["id"][5:])}.html">{esc(i["title"])}</a> {st(i["state"])}</li>' for i in ideas_by_chapter.get(ch["id"], []))
            ans = ", ".join(f'<a href="../{esc(nodes["book:" + f]["url"])}">{esc(nodes["book:" + f]["title"])}</a>' if nodes["book:" + f].get("url") else esc(nodes["book:" + f]["title"]) for f in ch.get("answers_2018", []))
            cards.append(f'<div class="chapter-card" id="{esc(ch["id"])}"><h4><span class="grav" title="{g[1]}">{g[0]}</span>{esc(ch["title"])} {st(ch["state"])}</h4><p class="punch">{esc(ch["punchline"])}</p>'
                         f'<p class="meta">Centre of gravity: {esc(g[1])} &middot; written first for <b>{esc(ch["character"])}</b> &middot; topics: {", ".join(esc(nodes["topic:" + t]["title"]) for t in ch["topics"] if ("topic:" + t) in nodes)}</p>'
                         f'<ul class="ideas">{ids or "<li class=dim>no idea placed yet</li>"}</ul>'
                         f'{("<p class=meta>Answers the 2018 files: " + ans + "</p>") if ans else ""}'
                         f'{("<p class=meta><b>Drafted:</b> <a href=\"../" + esc(ch["draft"]) + "\">read the chapter in the release candidate</a></p>") if ch.get("draft") and (ROOT / ch["draft"]).exists() else ""}</div>')
        sb = f' &middot; storyboard: <a href="../storyboards/{esc(p["storyboard"])}.html">{esc(nodes["sb:" + p["storyboard"]]["title"])}</a>' if p.get("storyboard") and ("sb:" + p["storyboard"]) in nodes else " &middot; no storyboard yet"
        sections.append(f'<h2 class="part" id="{esc(p["id"])}">{esc(p["title"])}<span class="w">{len(p["chapters"])} chapters{sb}</span></h2>{"".join(cards)}')
    left = "".join(f'<li>{esc(x.get("note", ""))}{(": " + ", ".join("<code>" + esc(f) + "</code>" for f in x["files"])) if x.get("files") else ""}</li>' for x in m["chapters_doc"].get("left_out", []))
    gcount = ", ".join(f"{v} {GRAV.get(k, (k, k))[1]}" for k, v in c["chapters_by_gravity"].items())
    body = f"""<h1>The chapter map, proposed</h1>
<p class="lede">{c["chapters"]} chapters in {c["parts"]} parts: the target nodes the ideas go to. Proposed by the librarian from the survey's 18 topics, Dinis's three storyline articles and the first storyline storyboard; it is the first answer to the editor's issue 003 and to <a href="../articles/start-from-the-storyline.html#brief">task 1 of Start from the storyline</a>. The editor's chapter map decides, and Dinis signs it off; until then every chapter is {st("proposed")} or, where a storyboard exists, {st("storyboarded")}.</p>
<p class="gr-stats"><span class="stat"><b>{c["chapters"]}</b><span>chapters</span></span><span class="stat"><b>{c["parts"]}</b><span>parts</span></span><span class="stat"><b>{c["ideas"]}</b><span>ideas placed</span></span><span class="stat"><b>{c["book_files_placed_in_chapters"]}</b><span>2018 files placed</span></span></p>
<p class="small dim">Centre of gravity, as <a href="../articles/where-do-you-land.html">Where do you land?</a> asks for every chapter: {gcount}. The letter on each chapter is its badge for now (E explorer, V villager, T town planner, A all three); the drawn badges are the editor's task 2.</p>
<div class="chapter-map">{"".join(sections)}</div>
<h2>Left out, on purpose</h2>
<ul>{left}</ul>
<p class="small dim">Source: <code>admin/content/graph/chapters.json</code>. A 2018 file can be answered by more than one chapter; the count above is distinct files.</p>
"""
    page("graph/chapters.html", "The chapter map, proposed", body, "The proposed chapters of the second edition, with the ideas and the 2018 files under each.",
         crumbs=(("The graph", "graph/index.html"), ("The chapter map", "graph/chapters.html")))

    # ---- sources
    groups = [("article", "This site's co-written articles"), ("decision", "Decisions"), ("agent-article", "Agent articles"), ("newsroom", "Newsroom articles"), ("book-2018", "The 2018 book"), ("storyboard", "Storyboards"), ("survey", "The survey"), ("memo", "Memos")]
    secs = []
    for key, label in groups:
        items = [n for n in nodes.values() if n["kind"] == "source" and n["source_kind"] == key]
        if key == "newsroom":
            items.sort(key=lambda n: ({"to-process": 0, "processed": 1, "to-mine": 2, "mined": 3, "background": 4, "skipped": 5}.get(n["state"], 9), n["title"]))
        if key == "book-2018":
            items.sort(key=lambda n: ({"unanswered": 0, "answered": 1, "apparatus": 2}.get(n["state"], 9), n["part"], n["title"]))
        trs = []
        for n in items:
            ideas_of = [nodes[e["from"]] for e in by_to.get(n["id"], []) if e["kind"] == "idea-from-source" or e["kind"] == "idea-answers-book"]
            ide = ", ".join(f'<a href="ideas/{esc(i["id"][5:])}.html">{esc(i["title"])}</a>' for i in ideas_of[:4]) + (f" and {len(ideas_of) - 4} more" if len(ideas_of) > 4 else "")
            extra = ""
            if key == "newsroom":
                extra = f'<td class="small">{esc(n["class"])}</td><td class="small dim">{esc((n.get("why") or "")[:140])}</td>'
            elif key == "book-2018":
                extra = f'<td class="small">{esc(n["book_kind"])}, {esc(n["part"])}</td><td class="small dim">{esc((n.get("gap") or "")[:140])}</td>'
            elif key == "decision":
                extra = f'<td class="small" colspan="2">“{esc(n.get("said", "")[:160])}”</td>'
            else:
                extra = '<td class="small" colspan="2"></td>'
            trs.append(f'<tr data-state="{esc(n["state"])}"><td>{href(n, "../")}</td><td>{st(n["state"])}</td>{extra}<td class="small">{ide or "<span class=dim>none</span>"}</td></tr>')
        counts = ", ".join(f"{v} {k}" for k, v in sorted(graph_model.Counter(n["state"] for n in items).items()))
        secs.append(f'<h2 id="{key}">{esc(label)} <span class="small dim">{len(items)}: {counts}</span></h2><div class="tablewrap"><table><thead><tr><th>Source</th><th>State</th><th>Class / kind</th><th>Why / gap</th><th>Ideas from it</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    nb = c["newsroom_by_state"]
    body = f"""<h1>The sources, and what has been done with each</h1>
<p class="lede">Every source the book draws on and its processing state: a newsroom article is <i>to process</i> (the survey says bring) until an idea cites it, then <i>processed</i>; a content article is <i>to mine</i> until a number, story or quote from it is attached to an idea, then <i>mined</i>; a 2018 file is <i>answered</i> when the map names an article for it. This is how "which articles have we processed" is answered: by the edges, not by a tick box.</p>
<p class="gr-stats"><span class="stat"><b>{nb.get("processed", 0)}</b><span>bring articles processed</span></span><span class="stat"><b>{nb.get("to-process", 0)}</b><span>bring still to process</span></span><span class="stat"><b>{nb.get("mined", 0)}</b><span>content mined</span></span><span class="stat"><b>{nb.get("to-mine", 0)}</b><span>content to mine</span></span><span class="stat"><b>{c["articles_by_state"].get("processed", 0)}</b><span>articles and decisions processed</span></span><span class="stat"><b>{c["book_2018_by_state"].get("unanswered", 0)}</b><span>2018 files with no article</span></span></p>
<div class="gr-filters" id="src-filters"><span class="dim">Show</span> {"".join(f'<button type="button" class="chip" data-v="{s}" aria-pressed="{str(s == "all").lower()}">{s}</button>' for s in ["all", "to-process", "processed", "to-mine", "mined", "background", "skipped", "answered", "unanswered"])}</div>
{"".join(secs)}
<p class="small dim">States come from the edges in <a href="graph.json">graph.json</a>; the overrides (a source read and found to have nothing more to give) are in <code>admin/content/graph/sources-state.json</code>. The survey's classes are <a href="../map/newsroom.html">the newsroom, surveyed</a>.</p>
<script>(function(){{var box=document.getElementById('src-filters');box.addEventListener('click',function(ev){{var b=ev.target.closest('.chip');if(!b)return;var v=b.dataset.v;box.querySelectorAll('.chip').forEach(function(x){{x.setAttribute('aria-pressed',String(x===b))}});document.querySelectorAll('tr[data-state]').forEach(function(tr){{tr.hidden=!(v==='all'||tr.dataset.state===v)}})}})}})();</script>
"""
    page("graph/sources.html", "The sources", body, "Every source the book draws on, and what has been done with each: processed, mined, answered.",
         crumbs=(("The graph", "graph/index.html"), ("Sources", "graph/sources.html")), wide=True)

    # ---- tasks
    tasks = [n for n in nodes.values() if n["kind"] == "task"]
    by_article = defaultdict(list)
    for t in tasks:
        by_article[t["article"]].append(t)
    secs = []
    for aid, ts in by_article.items():
        a = nodes[aid]
        trs = "".join(f'<tr data-state="{esc(t["state"])}"><td>{t["n"]}</td><td class="small"><b>{esc(t["role"])}</b></td><td>{esc(t["text"][:260])}{"…" if len(t["text"]) > 260 else ""}</td><td>{st(t["state"])}</td><td class="small dim">{esc(t["evidence"])}</td></tr>' for t in ts)
        done = sum(1 for t in ts if t["state"] == "done")
        secs.append(f'<h2 id="{esc(a["id"][4:])}">{href(a, "../")} <span class="small dim">{done} of {len(ts)} done</span></h2><div class="tablewrap"><table><thead><tr><th>#</th><th>Role</th><th>Task</th><th>State</th><th>Evidence</th></tr></thead><tbody>{trs}</tbody></table></div>')
    issues = [n for n in nodes.values() if n["kind"] == "issue"]
    itrs = "".join(f'<tr><td class="small"><b>{esc(i["role"])}</b></td><td><a href="../{esc(i["url"])}">{esc(i["title"])}</a></td><td>{st(i["state"])}</td></tr>' for i in issues)
    tb = c["tasks_by_state"]
    body = f"""<h1>The tasks: what the articles ask for, and what has been done</h1>
<p class="lede">Every numbered item in a co-written article's brief is a task, read from the article by the build, with the role the brief names. Its state is what the repository shows (the evidence column names the file or page), checked by the librarian; a task nobody has touched is open. {tb.get("done", 0)} done, {tb.get("in-progress", 0)} in progress, {tb.get("blocked", 0)} blocked, {tb.get("open", 0)} open, of {c["tasks"]}.</p>
<p class="gr-stats">{"".join(f'<span class="stat"><b>{v}</b><span>{esc(k)}</span></span>' for k, v in c["tasks_by_role"].items())}</p>
<div class="gr-filters" id="task-filters"><span class="dim">Show</span> {"".join(f'<button type="button" class="chip" data-v="{s}" aria-pressed="{str(s == "all").lower()}">{s}</button>' for s in ["all", "open", "in-progress", "blocked", "done"])}</div>
{"".join(secs)}
<h2>The roles' own issues</h2>
<p class="small dim">The work issues each role keeps (the folder is the status). A role opens its issues from the briefs above; these are the ones open today.</p>
<div class="tablewrap"><table><thead><tr><th>Role</th><th>Issue</th><th>State</th></tr></thead><tbody>{itrs}</tbody></table></div>
<p class="small dim">States: <code>admin/content/graph/tasks-state.json</code>. The build refuses a state for a task the articles do not have.</p>
<script>(function(){{var box=document.getElementById('task-filters');box.addEventListener('click',function(ev){{var b=ev.target.closest('.chip');if(!b)return;var v=b.dataset.v;box.querySelectorAll('.chip').forEach(function(x){{x.setAttribute('aria-pressed',String(x===b))}});document.querySelectorAll('tr[data-state]').forEach(function(tr){{tr.hidden=!(v==='all'||tr.dataset.state===v)}})}})}})();</script>
"""
    page("graph/tasks.html", "The tasks", body, "Every task the co-written articles ask for, with its state and the evidence.",
         crumbs=(("The graph", "graph/index.html"), ("Tasks", "graph/tasks.html")), wide=True)

    # ---- the viewer
    page("graph/view.html", "The graph", f"""<h1>The book as a graph</h1>
<p class="lede">{c["nodes"]} nodes and {c["edges"]} edges: the 2018 files, the sources, the ideas and the proposed chapters, with every edge the files justify. Click a node to light what it connects to. Filter the ideas by state and destination.</p>
<div class="gr-filters" id="gv-filters"></div>
<div class="gv" id="gv" data-graph="graph.json" data-up="../"><div class="gv-canvas" id="gv-canvas"></div><aside class="gv-side" id="gv-side" aria-live="polite"></aside></div>
<div class="gv-legend"><span><i style="background:#e8b64a"></i>2018 file</span><span><i style="background:#3b9fb0"></i>newsroom article</span><span><i style="background:var(--solid)"></i>co-written article</span><span><i style="background:#b45309"></i>decision</span><span><i style="background:#fb923c"></i>idea, candidate</span><span><i style="background:#0f766e"></i>idea, accepted</span><span><i style="background:#6b21a8"></i>idea, deferred</span><span><i style="background:#7c3aed"></i>chapter</span></div>
<p class="small dim">The data is <a href="graph.json">graph.json</a>, written by the build from <code>admin/content/graph/</code>, the survey, the map, the articles, the decisions and the roles' folders. Topics, concepts, tasks, issues and briefs are in the file too; the drawing shows the four columns that carry the book.</p>
""", "The book as a graph: sources, ideas and chapters, drawn.", crumbs=(("The graph", "graph/index.html"), ("The graph, drawn", "graph/view.html")),
         extra_head='<link rel="stylesheet" href="../assets/graph.css">\n<script defer src="../assets/graph.js"></script>\n', wide=True)

    # ---- the plan
    plan = (Path(__file__).resolve().parents[1] / "content/graph/plan.md").read_text(encoding="utf-8")
    page("graph/plan.html", "The plan: from articles to chapters", f'<article class="doc"><div class="body">{md(plan)}</div></article>',
         "How an article becomes a chapter: the pipeline, the states, the roles and the rules, and the order of work.", crumbs=(("The graph", "graph/index.html"), ("The plan", "graph/plan.html")))

    # ---- the hub
    nb = c["newsroom_by_state"]
    stages = [
        ("1 · Sources", f'{c["sources"]["newsroom"] + c["sources"]["article"] + c["sources"]["decision"]}', "newsroom articles, this site's articles, decisions, memos; the 2018 book beside them", "journalist writes; librarian captures", "sources.html"),
        ("2 · Ideas", f'{c["ideas"]}', f'{c["ideas_by_state"].get("accepted", 0)} accepted, {c["ideas_by_state"].get("candidate", 0)} candidates; each with its provenance', "librarian extracts; Dinis decides", "ideas/index.html"),
        ("3 · Chapters", f'{c["chapters"]}', f'in {c["parts"]} parts, proposed; {c["chapters_by_state"].get("storyboarded", 0)} storyboarded', "editor maps; Dinis signs off", "chapters.html"),
        ("4 · Text", "v1.0.0", "the working copy in the vault; decisions as files; versions signed off", "editor writes; reviewer records", "../v1/versions/index.html"),
        ("5 · Publish", "0 of 4", "print, screen, EPUB, Kindle from one source; Leanpub then Amazon", "publisher builds; Dinis uploads", "../articles/release-the-book-we-already-released.html"),
    ]
    stage_html = "".join(f'<div class="gr-stage"><span class="k">{esc(k)}</span><div class="n">{esc(n)}</div><p>{esc(p)}</p><div class="who">{esc(w)}</div><p><a href="{esc(u)}">open &rarr;</a></p></div>' for k, n, p, w, u in stages)
    todo = [n for n in nodes.values() if n["kind"] == "source" and n["source_kind"] == "newsroom" and n["state"] == "to-process"]
    unans = [n for n in nodes.values() if n["kind"] == "source" and n["source_kind"] == "book-2018" and n["state"] == "unanswered" and not any(e["kind"] == "idea-answers-book" for e in by_to.get(n["id"], []))]
    cands = [n for n in ideas if n["state"] == "candidate"]
    body = f"""<h1>The book as a graph</h1>
<p class="lede">Everything this site does to make the second edition, as one graph with a state on every node: the sources (articles, decisions, memos, the 2018 book), the ideas they carry, the chapters the ideas go to, the tasks the articles ask for, and the decisions that move them. This is the admin area of the publishing process, and the record of what has been processed, what is placed, and what waits on Dinis. <a href="plan.html">The plan</a> says how it runs.</p>
<div class="gr-pipeline">{stage_html}</div>
<p class="gr-stats"><span class="stat"><b>{c["nodes"]}</b><span>nodes</span></span><span class="stat"><b>{c["edges"]}</b><span>edges</span></span><span class="stat"><b>{nb.get("processed", 0)} of {nb.get("processed", 0) + nb.get("to-process", 0)}</b><span>bring articles processed</span></span><span class="stat"><b>{nb.get("mined", 0)} of {nb.get("mined", 0) + nb.get("to-mine", 0)}</b><span>content articles mined</span></span><span class="stat"><b>{c["book_files_answered_by_ideas"]}</b><span>2018 files an idea answers</span></span><span class="stat"><b>{c["tasks_by_state"].get("done", 0)} of {c["tasks"]}</b><span>tasks done</span></span></p>
<div class="cards">
<div class="card"><span class="k">register</span><h3><a href="ideas/index.html">The ideas</a></h3><p>{c["ideas"]} core ideas, each with its statement, provenance, the 2018 chapters it answers, its chapter and its state.</p><a class="more" href="ideas/index.html">The register &rarr;</a></div>
<div class="card"><span class="k">tracking</span><h3><a href="sources.html">The sources</a></h3><p>Every article, decision and 2018 file, and whether its ideas have been extracted, mined, answered or placed.</p><a class="more" href="sources.html">What has been processed &rarr;</a></div>
<div class="card"><span class="k">target</span><h3><a href="chapters.html">The chapter map</a></h3><p>{c["chapters"]} proposed chapters in {c["parts"]} parts, with the ideas and the 2018 files under each and a centre of gravity per chapter.</p><a class="more" href="chapters.html">The map &rarr;</a></div>
<div class="card"><span class="k">work</span><h3><a href="tasks.html">The tasks</a></h3><p>Every task the articles' briefs ask for, by role, with its state and the evidence in the repository.</p><a class="more" href="tasks.html">What is done &rarr;</a></div>
<div class="card"><span class="k">drawn</span><h3><a href="view.html">The graph</a></h3><p>{c["nodes"]} nodes and {c["edges"]} edges, in four columns; click a node to see what it connects to.</p><a class="more" href="view.html">Open it &rarr;</a></div>
<div class="card"><span class="k">rounds</span><h3><a href="../v2/book/rounds.html">The rounds</a></h3><p>Release candidate by release candidate: what each round added, changed and removed, by size, which ideas came in, and the diff Dinis reads.</p><a class="more" href="../v2/book/rounds.html">rc1 to rc2 &rarr;</a></div>
<div class="card"><span class="k">process</span><h3><a href="plan.html">The plan</a></h3><p>How an article becomes a chapter: the pipeline, the states, who does what, the rules, and the order of work from here.</p><a class="more" href="plan.html">Read it &rarr;</a></div>
</div>
<h2>What waits on Dinis</h2>
<ul>
<li><b>{len(cands)} candidate ideas</b> to read, comment on and decide, the <a href="../articles/read-comment-decide.html">read, comment, decide</a> way; the loop's first batch is the editor's task. <a href="ideas/index.html">The register</a>, filtered to candidates.</li>
<li><b>The chapter map</b>: {c["chapters"]} chapters proposed; group by centre of gravity or only mark it; accept the cast; where the storyline starts.</li>
<li><b>The open questions the articles keep apart</b>: the podcast to credit; three jobs that never scaled; the dot-com crash in the opening or later; his own three dots; a printable PDF for pen and paper; the title and the language.</li>
</ul>
<h2>What waits on the roles</h2>
<ul>
<li><b>The librarian</b>: {(str(len(todo)) + " bring articles still to process (" + ", ".join(href(n, "../") for n in todo) + ")") if todo else "no bring article left to process"}; the {nb.get("to-mine", 0)} content articles to mine as the chapters are drafted; a pass over the {len(unans)} 2018 files with neither an article nor an idea.</li>
<li><b>The editor</b>: the chapter map (this one is a proposal), the vault's decisions folder, the first interview, the first batch of the loop.</li>
<li><b>The publisher</b>: release v1.0.0 end to end, the ten tasks.</li>
<li><b>The journalist</b>: the gap articles, the fear and the job hunt first; the evidence the opening needs.</li>
</ul>
<p class="small dim">The data: <code>admin/content/graph/</code> (ideas.json, chapters.json, sources-state.json, tasks-state.json) and <a href="graph.json">graph.json</a>, derived on every build by <code>admin/build/graph_model.py</code>. The build refuses an idea that cites a source that does not exist, a chapter nothing names, or a source marked processed that no idea cites.</p>
"""
    page("graph/index.html", "The book as a graph", body, "The admin area of the publishing process: sources, ideas, chapters, tasks and decisions as one graph, with a state on every node.",
         crumbs=(("The graph", "graph/index.html"),), extra_head='<link rel="stylesheet" href="../assets/graph.css">\n')
    for rel in ("graph/ideas/index.html", "graph/sources.html", "graph/chapters.html", "graph/tasks.html", "graph/plan.html"):
        pass  # their chrome is the site's; graph.css is loaded through site.css's import below
    return m
