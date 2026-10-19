#!/usr/bin/env python3
"""The book as a graph: the model behind graph/ (the ideas register, the sources, the chapter map, the tasks, the
process), derived from the files that are the source of truth and never edited by hand.

Nodes (each with an id, a kind, a title, a url where one exists, and a state):
  source    a newsroom article (news:<slug>, with its survey class), a co-written article (art:<slug>), an agent
            article (agent:<slug>), a decision (dec:<nnn>), a 2018 file (book:<path>), a storyboard (sb:<slug>),
            a memo (memo:<id>), the survey's gaps (survey:gaps)
  idea      a node of admin/content/graph/ideas.json
  chapter   a chapter of the proposed map, admin/content/graph/chapters.json; part:<id> for its part
  topic     one of the survey's 18 topics
  concept   one of the survey's 50 concepts
  task      a numbered item of a co-written article's brief, read from the article; its state from tasks-state.json
  issue     a role's work issue, team/<role>/issues/<open|blocked|done>/
Edges (from, to, kind): idea-from-source, idea-answers-book, idea-goes-to-chapter, idea-in-topic, chapter-in-part,
  chapter-covers-topic, chapter-answers-book, topic-has-article, concept-defined-in, task-from-article,
  task-for-role, issue-of-role, decision-recorded-in, brief-points-at, storyboard-quotes.

Everything is computed by load(); build.py renders the pages and writes graph/graph.json. The checks (an idea that
cites a source that does not exist, a chapter the ideas name that is not on the map, a 'processed' source nothing
cites) stop the build, because a graph with dangling edges is the drift this site argues against.
"""
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / "admin/content/graph"
NEWSROOM = "https://newsroom.sgit.ai/articles/"

TASK_ROLES = ("editor", "publisher", "reviewer", "journalist", "librarian", "board", "dinis")


def _fm(text):
    m = re.match(r"---\n(.*?)\n---\n?(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def _fm_get(fm, key):
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    return m.group(1).strip() if m else ""


def read_articles(folder, prefix):
    out = OrderedDict()
    for f in sorted((ROOT / folder).glob("*.md")):
        fm, body = _fm(f.read_text(encoding="utf-8"))
        slug = f.stem.split("__", 1)[1]
        out[f"{prefix}:{slug}"] = {"id": f"{prefix}:{slug}", "slug": slug, "file": f.relative_to(ROOT).as_posix(), "title": _fm_get(fm, "title"),
                                   "date": _fm_get(fm, "date"), "version": _fm_get(fm, "version"), "author": _fm_get(fm, "author"),
                                   "url": f"{folder.split('/')[-1]}/{slug}.html", "body": body}
    return out


def read_decisions():
    out = OrderedDict()
    for f in sorted((ROOT / "admin/content/decisions").glob("*.md")):
        t = f.read_text(encoding="utf-8")
        n, slug = f.stem.split("__", 1)
        title = re.search(r"^# (.+)$", t, re.M).group(1)
        said = re.search(r"\*\*Said\.\*\*\s*(.+)", t)
        out[f"dec:{n}"] = {"id": f"dec:{n}", "n": n, "slug": slug, "title": title, "said": said.group(1).strip() if said else "",
                           "url": f"decisions/index.html#{slug}", "file": f.relative_to(ROOT).as_posix()}
    return out


def read_tasks(articles, state_doc):
    """One task per numbered item of each co-written article's 'The brief' section. A line 'For the editor.' (or
    'For me:') before a list names the role of the items that follow."""
    tasks = []
    for a in articles.values():
        m = re.search(r"^## The brief.*?\n(.*?)(?=^## )", a["body"], re.S | re.M)
        if not m:
            continue
        role = None
        for line in m.group(1).splitlines():
            r = re.match(r"^\s*(?:\*\*)?For (the )?(\w+)", line)
            if r:
                w = r.group(2).lower()
                role = "dinis" if w == "me" else (w if w in TASK_ROLES else role)
                continue
            t = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
            if t and role:
                n, text = int(t.group(1)), t.group(2).strip()
                tid = f"{a['slug']}:{role}:{n}"
                st = state_doc["tasks"].get(tid, {"state": "open", "evidence": ""})
                title = re.sub(r"\*\*", "", text.split(". ")[0])[:110]
                tasks.append({"id": "task:" + tid, "article": a["id"], "role": role, "n": n, "text": re.sub(r"\*\*", "", text), "title": title,
                              "state": st["state"], "evidence": st.get("evidence", ""), "url": a["url"] + "#brief"})
    return tasks


def read_issues():
    out = []
    for role_dir in sorted((ROOT / "team").iterdir()):
        if not (role_dir / "issues").exists():
            continue
        for st in ("open", "blocked", "done"):
            for f in sorted((role_dir / "issues" / st).glob("*.md")):
                title = re.search(r"^# (.+)$", f.read_text(encoding="utf-8"), re.M)
                out.append({"id": f"issue:{role_dir.name}:{f.stem}", "role": role_dir.name, "state": st, "title": title.group(1) if title else f.stem,
                            "url": f"team/{role_dir.name}/issues/{st}/{f.name}", "file": f.relative_to(ROOT).as_posix()})
    return out


def read_briefs():
    out = []
    for role_dir in sorted((ROOT / "team").iterdir()):
        for f in sorted((role_dir / "briefs").glob("*.md")) if (role_dir / "briefs").exists() else []:
            t = f.read_text(encoding="utf-8")
            title = re.search(r"^# (.+)$", t, re.M)
            arts = re.findall(r"articles/([a-z0-9-]+)\.md", t)
            out.append({"id": f"brief:{role_dir.name}:{f.stem}", "role": role_dir.name, "title": title.group(1) if title else f.stem,
                        "url": f"team/{role_dir.name}/briefs/{f.name}", "articles": sorted(set(arts))})
    return out


def load():
    ideas_doc = json.loads((G / "ideas.json").read_text(encoding="utf-8"))
    chapters_doc = json.loads((G / "chapters.json").read_text(encoding="utf-8"))
    sources_state = json.loads((G / "sources-state.json").read_text(encoding="utf-8"))
    tasks_state = json.loads((G / "tasks-state.json").read_text(encoding="utf-8"))
    survey = json.loads((ROOT / "admin/content/newsroom/survey.json").read_text(encoding="utf-8"))
    map_doc = json.loads((ROOT / "admin/content/map.json").read_text(encoding="utf-8"))
    articles = read_articles("admin/content/articles", "art")
    agent_articles = read_articles("admin/content/agent-articles", "agent")
    decisions = read_decisions()
    storyboards = OrderedDict()
    for f in sorted((ROOT / "admin/content/storyboards").glob("[0-9]*.json")):
        s = json.loads(f.read_text(encoding="utf-8"))
        storyboards["sb:" + s["slug"]] = {"id": "sb:" + s["slug"], "slug": s["slug"], "title": s["title"], "url": f"storyboards/{s['slug']}.html",
                                         "quote_source": s.get("quote_source"), "panels": len(s.get("scenes", []))}
    errors = []
    nodes, edges = OrderedDict(), []

    def add(n):
        nodes[n["id"]] = n
        return n

    def edge(a, b, kind, label=None):
        edges.append({"from": a, "to": b, "kind": kind, **({"label": label} if label else {})})

    # sources: newsroom articles
    for a in survey["articles"]:
        nid = "news:" + a["slug"]
        add({"id": nid, "kind": "source", "source_kind": "newsroom", "title": a["title"].split(":")[0], "full_title": a["title"], "url": NEWSROOM + a["slug"] + ".html",
             "class": a["class"], "serves": a.get("serves"), "why": a.get("why", ""), "date": a.get("date"),
             "state": {"bring": "to-process", "content": "to-mine", "context": "background", "skip": "skipped"}[a["class"]]})
    for a in articles.values():
        add({"id": a["id"], "kind": "source", "source_kind": "article", "title": a["title"].split(":")[0], "full_title": a["title"], "url": a["url"], "date": a["date"], "version": a["version"], "state": "to-process"})
    for a in agent_articles.values():
        add({"id": a["id"], "kind": "source", "source_kind": "agent-article", "title": a["title"].split(":")[0], "full_title": a["title"], "url": a["url"], "date": a["date"], "version": a["version"], "state": "to-process"})
    for d in decisions.values():
        add({"id": d["id"], "kind": "source", "source_kind": "decision", "title": f"Decision {d['n']}: {d['title']}", "url": d["url"], "said": d["said"], "state": "to-process"})
    for s in storyboards.values():
        add({"id": s["id"], "kind": "source", "source_kind": "storyboard", "title": s["title"], "url": s["url"], "panels": s["panels"], "state": "background"})
        if s.get("quote_source"):
            q = s["quote_source"]
            m = re.search(r"articles/\d+__([a-z0-9-]+)\.md", q)
            if m and ("art:" + m.group(1)) in nodes:
                edge(s["id"], "art:" + m.group(1), "storyboard-quotes")
    add({"id": "survey:gaps", "kind": "source", "source_kind": "survey", "title": "The survey's gaps", "url": "map/newsroom.html#gaps", "state": "to-process"})
    add({"id": "memo:2026-10-18-graphs", "kind": "source", "source_kind": "memo", "title": "Dinis's message of 18 October 2026 asking for the graph", "url": "graph/plan.html", "state": "processed"})
    # sources: the 2018 files, with the map's reading
    answered = Counter()
    for r in map_doc["rows"]:
        nid = "book:" + r["file"]
        add({"id": nid, "kind": "source", "source_kind": "book-2018", "title": r["title"], "file": r["file"], "book_kind": r["kind"], "part": r["part"],
             "url": None, "map_articles": [a["slug"] for a in r["articles"]], "gap": r["gap"], "state": "answered" if r["articles"] else ("apparatus" if r["kind"] == "apparatus" else "unanswered")})
        for a in r["articles"]:
            if ("news:" + a["slug"]) in nodes:
                edge(nid, "news:" + a["slug"], "answered-by")
                answered["news:" + a["slug"]] += 1
    # chapter pages for the 2018 files
    manifest = json.loads((ROOT / "v1/book/manifest.json").read_text(encoding="utf-8")) if (ROOT / "v1/book/manifest.json").exists() else {"chapters": []}
    for ch in manifest["chapters"]:
        if ("book:" + ch["file"]) in nodes:
            nodes["book:" + ch["file"]]["url"] = ch["page"]
    # topics and concepts
    for t in survey["topics"]:
        add({"id": "topic:" + t["id"], "kind": "topic", "title": t["title"], "why": t.get("why", ""), "url": "map/newsroom.html#topics", "articles": t.get("articles", []), "state": "surveyed"})
        for s in t.get("articles", []):
            if ("news:" + s) in nodes:
                edge("topic:" + t["id"], "news:" + s, "topic-has-article")
    for c in survey["concepts"]:
        cid = "concept:" + re.sub(r"[^a-z0-9]+", "-", c["term"].lower()).strip("-")
        add({"id": cid, "kind": "concept", "title": c["term"], "definition": c["definition"], "url": "map/newsroom.html#concepts", "state": "surveyed"})
        if c.get("defined_in") and ("news:" + c["defined_in"]) in nodes:
            edge(cid, "news:" + c["defined_in"], "concept-defined-in")
    # the chapter map
    for p in chapters_doc["parts"]:
        add({"id": "part:" + p["id"], "kind": "part", "title": p["title"], "storyboard": p.get("storyboard"), "url": "graph/chapters.html#" + p["id"], "state": "proposed"})
        if p.get("storyboard") and ("sb:" + p["storyboard"]) in nodes:
            edge("part:" + p["id"], "sb:" + p["storyboard"], "part-storyboarded-by")
        for c in p["chapters"]:
            add({"id": "chapter:" + c["id"], "kind": "chapter", "title": c["title"], "punchline": c["punchline"], "part": p["id"], "gravity": c["gravity"], "character": c["character"],
                 "topics": c["topics"], "url": "graph/chapters.html#" + c["id"], "state": c["state"], "answers_2018": c.get("answers_2018", [])})
            edge("chapter:" + c["id"], "part:" + p["id"], "chapter-in-part")
            for t in c["topics"]:
                if ("topic:" + t) in nodes:
                    edge("chapter:" + c["id"], "topic:" + t, "chapter-covers-topic")
                else:
                    errors.append(f"chapter {c['id']} covers unknown topic {t}")
            for f in c.get("answers_2018", []):
                if ("book:" + f) in nodes:
                    edge("chapter:" + c["id"], "book:" + f, "chapter-answers-book")
                else:
                    errors.append(f"chapter {c['id']} answers unknown 2018 file {f}")
    # ideas
    cited = Counter()
    for i in ideas_doc["ideas"]:
        nid = "idea:" + i["id"]
        add({"id": nid, "kind": "idea", "title": i["title"], "statement": i["statement"], "idea_kind": i["kind"], "state": i["state"], "destination": i["destination"],
             "decided_by": i.get("decided_by"), "notes": i.get("notes"), "gravity": i.get("gravity", "all"), "topic": i.get("topic"), "chapter": i.get("chapter"),
             "url": f"graph/ideas/{i['id']}.html", "sources": i["sources"], "answers": i.get("answers", [])})
        for s in i["sources"]:
            if s["ref"] not in nodes:
                errors.append(f"idea {i['id']} cites unknown source {s['ref']}")
                continue
            edge(nid, s["ref"], "idea-from-source", s.get("where"))
            cited[s["ref"]] += 1
        for f in i.get("answers", []):
            if ("book:" + f) in nodes:
                edge(nid, "book:" + f, "idea-answers-book")
            else:
                errors.append(f"idea {i['id']} answers unknown 2018 file {f}")
        if i.get("chapter"):
            if ("chapter:" + i["chapter"]) in nodes:
                edge(nid, "chapter:" + i["chapter"], "idea-goes-to-chapter")
            else:
                errors.append(f"idea {i['id']} goes to unknown chapter {i['chapter']}")
        if i.get("topic"):
            if ("topic:" + i["topic"]) in nodes:
                edge(nid, "topic:" + i["topic"], "idea-in-topic")
            else:
                errors.append(f"idea {i['id']} names unknown topic {i['topic']}")
    # source states: citations move them; overrides say the rest
    for sid, n in cited.items():
        s = nodes[sid]
        if s["kind"] != "source":
            continue
        if s["source_kind"] == "newsroom":
            s["state"] = {"bring": "processed", "content": "mined", "context": "mined", "skip": "mined"}[s["class"]]
        elif s["source_kind"] != "book-2018":  # a 2018 file keeps the map's reading (answered / unanswered) and gains its idea count
            s["state"] = "processed"
        s["ideas"] = n
    for sid, st in sources_state["overrides"].items():
        if sid not in nodes:
            errors.append(f"sources-state overrides unknown source {sid}")
            continue
        if st == "processed" and not cited.get(sid):
            errors.append(f"sources-state says {sid} is processed but no idea cites it")
            continue
        nodes[sid]["state"] = st
    # tasks, issues, briefs
    tasks = read_tasks(articles, tasks_state)
    for t in tasks:
        add({**t, "kind": "task"})
        edge(t["id"], t["article"], "task-from-article")
    for tid in tasks_state["tasks"]:
        if ("task:" + tid) not in nodes:
            errors.append(f"tasks-state names a task the articles do not have: {tid}")
    for i in read_issues():
        add({**i, "kind": "issue"})
    for b in read_briefs():
        add({**b, "kind": "brief", "state": "sent"})
        for a in b["articles"]:
            if ("art:" + a) in nodes:
                edge(b["id"], "art:" + a, "brief-points-at")
    for d in decisions.values():
        edge(d["id"], "agent:dinis-first-decisions", "decision-recorded-in") if "agent:dinis-first-decisions" in nodes else None

    # counts
    def count(kind, key="state"):
        return Counter(n.get(key) for n in nodes.values() if n["kind"] == kind)
    counts = {
        "nodes": len(nodes), "edges": len(edges),
        "sources": Counter(n["source_kind"] for n in nodes.values() if n["kind"] == "source"),
        "newsroom_by_state": Counter(n["state"] for n in nodes.values() if n["kind"] == "source" and n["source_kind"] == "newsroom"),
        "articles_by_state": Counter(n["state"] for n in nodes.values() if n["kind"] == "source" and n["source_kind"] in ("article", "agent-article", "decision")),
        "book_2018_by_state": Counter(n["state"] for n in nodes.values() if n["kind"] == "source" and n["source_kind"] == "book-2018"),
        "ideas": len(ideas_doc["ideas"]), "ideas_by_state": count("idea"), "ideas_by_destination": count("idea", "destination"), "ideas_by_kind": count("idea", "idea_kind"),
        "chapters": sum(1 for n in nodes.values() if n["kind"] == "chapter"), "parts": sum(1 for n in nodes.values() if n["kind"] == "part"),
        "chapters_by_state": count("chapter"), "chapters_by_gravity": count("chapter", "gravity"),
        "tasks": len(tasks), "tasks_by_state": count("task"), "tasks_by_role": count("task", "role"),
        "issues_by_state": count("issue"), "briefs": sum(1 for n in nodes.values() if n["kind"] == "brief"),
        "topics": len(survey["topics"]), "concepts": len(survey["concepts"]),
        "book_files_answered_by_ideas": len({e["to"] for e in edges if e["kind"] == "idea-answers-book"}),
        "book_files_placed_in_chapters": len({e["to"] for e in edges if e["kind"] == "chapter-answers-book"}),
    }
    counts = json.loads(json.dumps(counts))  # Counters to plain dicts
    return {"nodes": nodes, "edges": edges, "counts": counts, "errors": errors, "ideas_doc": ideas_doc, "chapters_doc": chapters_doc,
            "sources_state": sources_state, "tasks_state": tasks_state, "survey": survey, "articles": articles, "decisions": decisions, "tasks": tasks}


def neighbours(model, nid):
    out = []
    for e in model["edges"]:
        if e["from"] == nid:
            out.append((e["to"], e["kind"], e.get("label"), "out"))
        elif e["to"] == nid:
            out.append((e["from"], e["kind"], e.get("label"), "in"))
    return out


if __name__ == "__main__":
    m = load()
    if m["errors"]:
        print("graph: " + "; ".join(m["errors"]))
        sys.exit(1)
    print(json.dumps(m["counts"], indent=1))
