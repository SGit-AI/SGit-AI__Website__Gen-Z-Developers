#!/usr/bin/env python3
"""readers/: synthetic readers of a release candidate, rendered from admin/content/readers/. Called by build.py with its
helpers (page, write, esc, md) so every page carries the site's chrome; also runs on its own to check one run record:

    python3 admin/build/readers_pages.py check admin/content/readers/01-rc2/runs/aisha.json

Sources (admin/content/readers/):
  protocol.json                  the method, adapted from the newsroom's synthetic users to a book; shared by every study
  <study>/study.json             which candidate, pinned by its sha256, who asked, the disclosure
  <study>/personas.json          the invented readers
  <study>/journeys.json          what each was expected to do, written before any run
  <study>/runs/<persona>.json    the run as the reader wrote it: steps, put-down point, buy decision, interview, findings
  <study>/checks.json            what was checked after the runs, and whether each finding held
  <study>/synthesis.json         will they buy, and the recommendations, ordered by cost
  <study>/answers.json           the editor's answer to each finding (declined, with a reason, is an answer)

The build refuses a run whose persona, unit, mode, phase, pace or cost is unknown, whose interview does not answer every
question, or which quotes the candidate anywhere other than word for word in the unit it cites; and a study whose
candidate no longer hashes to the sha256 it was read at.
Writes readers/index.html, readers/protocol.html, and per study readers/<study>/index.html, findings.html,
interviews.html and <persona>.html.
"""
import hashlib
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "admin/content/readers"
MODES = ("read", "skim", "skip", "stop")
PHASES = ("natural", "asked")
PACES = ("too slow", "right", "too fast")
BUY = ("yes", "maybe", "no")
COMMISSION = ("yes", "yes-with-conditions", "no")
VERDICTS = ("holds", "partly", "does-not-hold", "not-about-the-book")


def load_json(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# ------------------------------------------------------------------ the candidate, as units
def units_of(text):
    """The candidate as the reader meets it: about (everything before the first part), part:N, ch:N, in order."""
    out, cur, part = OrderedDict(), "about", 0
    out[cur] = {"id": cur, "kind": "about", "title": "About this release candidate", "lines": []}
    for line in text.splitlines():
        m = re.match(r"^# Part: (.+)$", line)
        c = re.match(r"^## (\d+)\. (.+)$", line)
        if m:
            part += 1
            cur = f"part:{part}"
            out[cur] = {"id": cur, "kind": "part", "n": part, "title": m.group(1).strip(), "lines": []}
        elif c:
            cur = f"ch:{int(c.group(1))}"
            out[cur] = {"id": cur, "kind": "chapter", "n": int(c.group(1)), "part": part, "title": c.group(2).strip(), "lines": []}
        out[cur]["lines"].append(line)
    for u in out.values():
        u["text"] = "\n".join(u.pop("lines"))
        u["words"] = len(u["text"].split())
    return out


def norm(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-"}))
    s = re.sub(r"[*_`>]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def quote_in(quote, text):
    """Word for word, ignoring emphasis, links and curly quotes; an ellipsis may join fragments that appear in order."""
    hay, at = norm(text), 0
    for frag in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", quote):
        f = norm(frag).strip(" '\"")
        if not f:
            continue
        i = hay.find(f, at)
        if i < 0:
            return False
        at = i + len(f)
    return True


# ------------------------------------------------------------------ the checks
def check_run(run, units, personas, protocol, name="run"):
    errs = []
    E = lambda m: errs.append(f"{name}: {m}")
    p = personas.get(run.get("persona"))
    if not p:
        return [f"{name}: persona {run.get('persona')!r} is not in personas.json"]
    steps = run.get("steps") or []
    if not steps:
        E("no steps")
    seen_asked = False
    for i, s in enumerate(steps, 1):
        w = f"step {s.get('n')}"
        if s.get("n") != i:
            E(f"{w}: steps are numbered 1, 2, 3 in order (expected {i})")
        if s.get("unit") not in units:
            E(f"{w}: unit {s.get('unit')!r} is not in the candidate (about, part:N, ch:N)")
        if s.get("phase") not in PHASES:
            E(f"{w}: phase {s.get('phase')!r} is not one of {PHASES}")
        if s.get("phase") == "asked":
            seen_asked = True
        elif seen_asked:
            E(f"{w}: a natural step after an asked one; the natural phase comes first")
        if s.get("mode") not in MODES:
            E(f"{w}: mode {s.get('mode')!r} is not one of {MODES}")
        if s.get("mode") != "skip" and s.get("pace") not in PACES:
            E(f"{w}: pace {s.get('pace')!r} is not one of {PACES}")
        if s.get("mode") != "skip" and not (isinstance(s.get("interest"), int) and 1 <= s["interest"] <= 5):
            E(f"{w}: interest must be 1 to 5")
        if s.get("quote") and s.get("unit") in units and not quote_in(s["quote"], units[s["unit"]]["text"]):
            E(f"{w}: the quote is not word for word in {s['unit']}: {s['quote'][:90]!r}")
        for k in ("read", "thought", "next"):
            if not s.get(k):
                E(f"{w}: no {k}")
    pd = run.get("put_down")
    if pd:
        st = next((s for s in steps if s.get("n") == pd.get("after_step")), None)
        if not st or st.get("phase") != "natural":
            E("put_down.after_step must name a natural step")
        elif st.get("unit") != pd.get("unit"):
            E(f"put_down.unit {pd.get('unit')!r} is not the unit of step {pd.get('after_step')} ({st.get('unit')})")
    b = run.get("buy_at_put_down") or {}
    if b.get("decision") not in (COMMISSION if p.get("role") == "publisher" else BUY):
        E(f"buy_at_put_down.decision {b.get('decision')!r} is not allowed for this reader")
    qs = protocol["interview"] + (protocol["publisher_interview"] if p.get("role") == "publisher" else [])
    iv = run.get("interview") or []
    if len(iv) != len(qs) or not all(isinstance(a, str) and a.strip() for a in iv):
        E(f"interview: {len(iv)} answers for {len(qs)} questions; every question gets an answer, in order")
    if not (isinstance(run.get("rating"), int) and 1 <= run["rating"] <= 5) or not run.get("rating_why"):
        E("rating must be 1 to 5, with rating_why")
    d = run.get("decision") or {}
    if d.get("buy") not in BUY:
        E(f"decision.buy {d.get('buy')!r} is not one of {BUY}")
    if p.get("role") == "publisher" and d.get("commission") not in COMMISSION:
        E(f"decision.commission {d.get('commission')!r} is not one of {COMMISSION}")
    costs = {c["id"] for c in protocol["costs"]}
    ids = set()
    for f in run.get("findings") or []:
        fid = f.get("id", "?")
        if not re.match(rf"^{run['persona']}-\d+$", fid) or fid in ids:
            E(f"finding {fid}: ids are <persona>-<n>, unique")
        ids.add(fid)
        if f.get("cost") not in costs:
            E(f"finding {fid}: cost {f.get('cost')!r} is not one of {sorted(costs)}")
        if f.get("unit") not in units:
            E(f"finding {fid}: unit {f.get('unit')!r} is not in the candidate")
        elif f.get("quote") and not quote_in(f["quote"], units[f["unit"]]["text"]):
            E(f"finding {fid}: the quote is not word for word in {f['unit']}: {f['quote'][:90]!r}")
        if not f.get("what"):
            E(f"finding {fid}: no what")
    if not 3 <= len(ids) <= 8:
        E(f"{len(ids)} findings; a run ends with 3 to 8")
    return errs


def load_study(sdir, protocol):
    study = load_json(sdir / "study.json")
    raw = (ROOT / study["candidate_file"]).read_text(encoding="utf-8")
    errs = []
    if hashlib.sha256(raw.encode("utf-8")).hexdigest() != study["candidate_sha256"]:
        errs.append(f"{sdir.name}: {study['candidate_file']} no longer hashes to the candidate the readers read")
    units = units_of(raw)
    personas = OrderedDict((p["id"], p) for p in load_json(sdir / "personas.json")["personas"])
    journeys = {j["persona"]: j for j in load_json(sdir / "journeys.json")["journeys"]}
    for pid in personas:
        if pid not in journeys:
            errs.append(f"{sdir.name}: {pid} has no journey; the journey is written before the run")
    runs = OrderedDict()
    for pid in personas:
        f = sdir / "runs" / f"{pid}.json"
        if f.exists():
            run = load_json(f)
            errs += check_run(run, units, personas, protocol, f"{sdir.name}/runs/{pid}.json")
            runs[pid] = run
    for f in (sdir / "runs").glob("*.json"):
        if f.stem not in personas:
            errs.append(f"{sdir.name}/runs/{f.name}: no such persona")
    opt = lambda n, d: load_json(sdir / n) if (sdir / n).exists() else d
    checks, synthesis, answers = opt("checks.json", {"checks": []}), opt("synthesis.json", None), opt("answers.json", {"answers": {}})
    fids = {f["id"] for r in runs.values() for f in r.get("findings", [])}
    for c in checks["checks"]:
        if c.get("finding") not in fids:
            errs.append(f"{sdir.name}/checks.json: finding {c.get('finding')!r} does not exist")
        if c.get("verdict") not in VERDICTS:
            errs.append(f"{sdir.name}/checks.json: verdict {c.get('verdict')!r} is not one of {VERDICTS}")
    for k in answers["answers"]:
        if k not in fids:
            errs.append(f"{sdir.name}/answers.json: finding {k!r} does not exist")
    for r in (synthesis or {}).get("recommendations", []):
        for k in r.get("from", []):
            if k not in fids:
                errs.append(f"{sdir.name}/synthesis.json: recommendation {r.get('id')} cites {k!r}, which does not exist")
    return {"id": sdir.name, "study": study, "units": units, "personas": personas, "journeys": journeys, "runs": runs,
            "checks": {c["finding"]: c for c in checks["checks"]}, "synthesis": synthesis, "answers": answers["answers"], "errors": errs}


# ------------------------------------------------------------------ the pages
def build_readers(ctx):
    page, esc, md = ctx["page"], ctx["esc"], ctx["md"]
    protocol = load_json(R / "protocol.json")
    studies = [load_study(d, protocol) for d in sorted(R.iterdir()) if d.is_dir() and (d / "study.json").exists()]
    errs = [e for s in studies for e in s["errors"]]
    if errs:
        sys.exit("readers: " + "; ".join(errs))
    head = '<link rel="stylesheet" href="{up}assets/readers.css">\n'
    costs = OrderedDict((c["id"], c) for c in protocol["costs"])
    manifest = load_json(ROOT / "v2/book/manifest.json") if (ROOT / "v2/book/manifest.json").exists() else {"chapters": []}

    def chip(cls, label=None):
        return f'<span class="st {esc(cls)}">{esc(label or cls)}</span>'

    def cost_chip(c):
        return f'<span class="cost {esc(c)}">{esc(costs[c]["label"])}</span>'

    def decision_chip(d):
        cls = {"yes": "buy-yes", "maybe": "buy-maybe", "no": "buy-no", "yes-with-conditions": "buy-maybe"}[d]
        return f'<span class="dec {cls}">{esc(d.replace("-", " "))}</span>'

    page("readers/protocol.html", "The protocol for synthetic readers", f"""<h1>The protocol for synthetic readers</h1>
<p class="lede">{esc(protocol['what'])}</p>
<p class="small dim">Protocol {esc(protocol['version'])}, adapted from <a href="{esc(protocol['adapted_from'])}">How to run synthetic users on your own site</a>. Source: <code>admin/content/readers/protocol.json</code>.</p>
<h2>What changes from a website to a book</h2><ul>{''.join(f'<li>{esc(x)}</li>' for x in protocol['changes_from_the_site_method'])}</ul>
<h2>Two phases</h2><dl class="kv">{''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k, v in protocol['phases'].items())}</dl>
<h2>The loop, for every unit</h2><ol>{''.join(f'<li><b>{esc(s["step"])}.</b> {esc(s["what"])}</li>' for s in protocol['loop'])}</ol>
<h2>The rules</h2><ul>{''.join(f'<li>{esc(x)}</li>' for x in protocol['rules'])}</ul>
<h2>The offer the buy question answers</h2><p>{esc(protocol['the_offer'])}</p>
<h2>The interview, the same for everyone</h2><ol>{''.join(f'<li>{esc(q)}</li>' for q in protocol['interview'])}</ol>
<h3>And for a publisher</h3><ol>{''.join(f'<li>{esc(q)}</li>' for q in protocol['publisher_interview'])}</ol>
<h2>What a finding costs, in order</h2><ul>{''.join(f'<li>{cost_chip(c["id"])} {esc(c["what"])}</li>' for c in protocol['costs'])}</ul>
<h2>The units and the record</h2><p>{esc(protocol['units'])}</p>
<dl class="kv">{''.join(f'<dt><code>{esc(k)}</code></dt><dd>{esc(v)}</dd>' for k, v in protocol['record']['fields'].items())}</dl>
<p>{esc(protocol['models'])}</p>""", "The protocol for synthetic readers of the book: the newsroom's method, adapted from a website to a book.",
         crumbs=(("Synthetic readers", "readers/index.html"), ("Protocol", "readers/protocol.html")), extra_head=head.format(up="../"))

    cards = ""
    for s in studies:
        st, n = s["study"], len(s["runs"])
        cards += (f'<a class="card" href="{esc(s["id"])}/index.html"><span class="k">{esc(st["candidate"])} &middot; {esc(st["date"])}</span>'
                  f'<h3>{esc(st["title"])}</h3><p>{len(s["personas"])} readers, {n} run{"s" if n != 1 else ""}. '
                  f'{esc((s["synthesis"] or {}).get("headline", "The readers and their journeys are set; the runs follow."))}</p><span class="more">Open the study &rarr;</span></a>')
    page("readers/index.html", "Synthetic readers", f"""<h1>Synthetic readers</h1>
<p class="lede">Invented readers, played by a model, who read a release candidate of the book from the first page the way they would, say where they would put it down and whether they would buy it there, finish it as beta readers, and are interviewed. The method is the newsroom's <a href="https://newsroom.sgit.ai/articles/how-to-run-synthetic-users.html">synthetic users</a>, which has run on three sites, adapted to a book: <a href="protocol.html">the protocol</a>.</p>
<div class="disclose"><b>Everybody in these studies is invented.</b> It is not reader research. What is evidence is the candidate's text: every quote a reader cites is checked by the build against the chapter it cites.</div>
<div class="cards">{cards}</div>
<p class="small dim">Why here, and not in a vault: Dinis asked for the pages to be on this site, so the studies are kept with the candidates they read and compared across them. The editor owns them (<a href="../team/editor/index.html">team/editor</a>, primary responsibility 4); the brief is <a href="../team/editor/briefs/book__v2.0.0-rc2__synthetic-readers.md">synthetic readers of release candidate 2</a>.</p>""",
         "Synthetic readers of the book: invented readers who read a release candidate and say whether they would buy it.",
         crumbs=(("Synthetic readers", "readers/index.html"),), extra_head=head.format(up="../"))

    for s in studies:
        build_study(s, protocol, page, esc, md, head, costs, manifest, chip, cost_chip, decision_chip)
    return studies


def build_study(s, protocol, page, esc, md, head, costs, manifest, chip, cost_chip, decision_chip):
    # a chapter links to its page only while the site renders the candidate the readers read
    pages_by_n = {c["number"]: c["page"] for c in manifest["chapters"]} if manifest.get("version") == s["study"]["candidate"] else {}
    sid, st, units, personas, journeys, runs = s["id"], s["study"], s["units"], s["personas"], s["journeys"], s["runs"]
    base = f"readers/{sid}/"
    up = "../../"
    H = head.format(up=up)
    crumbs = (("Synthetic readers", "readers/index.html"), (st["candidate"], base + "index.html"))

    def ulink(uid):
        u = units[uid]
        label = {"about": "About", "part": f"Part {u.get('n')}", "chapter": f"Ch. {u.get('n')}"}[u["kind"]]
        href = pages_by_n.get(u.get("n")) if u["kind"] == "chapter" else None
        t = f'{label}: {esc(u["title"])}'
        return f'<a href="{up}{esc(href)}">{t}</a>' if href else t

    def short(uid):
        u = units[uid]
        return {"about": "About", "part": f"P{u.get('n')}", "chapter": f"{u.get('n')}"}[u["kind"]]

    def name(pid, link=True):
        p = personas[pid]
        return f'<a href="{esc(pid)}.html">{esc(p["name"])}</a>' if link else esc(p["name"])

    def counts(run):
        steps = run["steps"]
        nat = [x for x in steps if x["phase"] == "natural"]
        return {"steps": len(steps), "natural": len(nat), "questions": sum(1 for x in steps if x.get("question")),
                "confusions": sum(1 for x in steps if x.get("confusion")), "quotes": sum(1 for x in steps if x.get("quote")),
                "read_natural": sum(units[x["unit"]]["words"] for x in nat if x["mode"] in ("read", "skim")),
                "findings": len(run.get("findings", []))}

    total_words = sum(u["words"] for u in units.values())
    allf = sorted(((pid, f) for pid, r in runs.items() for f in r.get("findings", [])), key=lambda t: (list(costs).index(t[1]["cost"]), t[0]))
    fcount = Counter(f["cost"] for _, f in allf)

    # ---- one page per reader
    for pid, p in personas.items():
        j, run = journeys[pid], runs.get(pid)
        prof = "".join(f'<dt>{esc(k.replace("_", " "))}</dt><dd>{esc(p[k])}</dd>' for k in
                       ("situation", "arrives_with", "knows", "does_not_know", "decides_on", "leaves_when", "patience", "format", "reads_like") if p.get(k))
        neg = ' class="neg"'
        prof = prof.replace("<dt>does not know</dt>", f"<dt{neg}>does not know</dt>").replace("<dt>leaves when</dt>", f"<dt{neg}>leaves when</dt>")
        jour = "".join(f'<dt>{esc(k.replace("_", " "))}</dt><dd>{esc(j[k])}</dd>' for k in ("hypothesis", "expected_path", "expected_put_down", "expected_buy", "watch_for"))
        body = f"""<h1>{esc(p['name'])} <span class="small dim">(invented)</span></h1>
<p class="lede">Generation {esc(p['generation'])}, {esc(p['age'])}{', publisher' if p.get('role') == 'publisher' else ''}. <i>&ldquo;{esc(p['arrives_with'])}&rdquo;</i></p>
<div class="disclose small">{esc(st['disclosure'])}</div>"""
        if run:
            c = counts(run)
            pd = run.get("put_down")
            b = run["buy_at_put_down"]
            body += f"""<div class="verdict">
<div><span class="k">Put it down</span><b>{ulink(pd['unit']) if pd else 'finished the natural read'}</b>{f'<p>{esc(pd["why"])}</p>' if pd else ''}</div>
<div><span class="k">{'Commission' if p.get('role') == 'publisher' else 'Buy'}, at that point</span><b>{decision_chip(b['decision'])}</b><p>{esc(b.get('why', ''))}{(' Format: ' + esc(b['format']) + '.') if b.get('format') else ''}{(' Would pay: ' + esc(b['would_pay']) + '.') if b.get('would_pay') else ''}</p></div>
<div><span class="k">At the end</span><b>{decision_chip(run['decision'].get('commission') or run['decision']['buy'])} &middot; {run['rating']}/5</b><p>{esc(run['decision'].get('why', ''))} <i>{esc(run['rating_why'])}</i></p></div>
</div>
<p>{''.join(f'<span class="stat"><b>{v:,}</b><span>{esc(k.replace("_", " "))}</span></span>' for k, v in c.items())}</p>"""
        body += f"""<div class="twocol"><div><h2>Who they are</h2><dl class="kv">{prof}</dl>{f'<p class="small dim">Nearest in the storyboard cast: {esc(p["nearest_in_cast"])}.</p>' if p.get('nearest_in_cast') else ''}</div>
<div><h2>What we expected, before the run</h2><dl class="kv">{jour}</dl></div></div>"""
        if not run:
            body += '<p class="note">The run has not happened yet. The journey above was written first, on purpose.</p>'
        else:
            rows = ""
            for x in run["steps"]:
                if x["phase"] == "asked" and (x["n"] == 1 or run["steps"][x["n"] - 2]["phase"] == "natural"):
                    rows += '<tr class="phase"><td colspan="3">The asked phase: from here the reader is going on as a paid beta reader. Nothing below changes where they put it down or what they decided there.</td></tr>'
                q = f'<blockquote class="q">{esc(x["quote"])} <span class="ok" title="Checked by the build: word for word in this unit">&#10003; verbatim</span></blockquote>' if x.get("quote") else ""
                extra = (f'<p class="qn"><b>Question:</b> {esc(x["question"])}</p>' if x.get("question") else "") + \
                        (f'<p class="cf"><b>Confusion:</b> {esc(x["confusion"])}</p>' if x.get("confusion") else "")
                meta = "" if x["mode"] == "skip" else f'<br><span class="small dim">pace: {esc(x["pace"])} &middot; interest {x["interest"]}/5</span>'
                stop = ' class="putdown"' if run.get("put_down") and run["put_down"]["after_step"] == x["n"] else ""
                rows += (f'<tr{stop}><td class="n">{x["n"]}</td><td class="u">{ulink(x["unit"])}<br><span class="mode {esc(x["mode"])}">{esc(x["mode"])}</span>{meta}</td>'
                         f'<td><p>{esc(x["read"])}</p><p class="th">{esc(x["thought"])}</p>{q}{extra}<p class="nx"><b>Next:</b> {esc(x["next"])}</p></td></tr>')
            body += f'<h2 id="run">The run, unit by unit</h2><div class="tablewrap"><table class="run"><thead><tr><th>#</th><th>Unit</th><th>What they read, thought and did</th></tr></thead><tbody>{rows}</tbody></table></div>'
            qs = protocol["interview"] + (protocol["publisher_interview"] if p.get("role") == "publisher" else [])
            body += '<h2 id="interview">The interview</h2><dl class="iv">' + "".join(f'<dt>{i}. {esc(q)}</dt><dd>{esc(a)}</dd>' for i, (q, a) in enumerate(zip(qs, run["interview"]), 1)) + "</dl>"
            body += f'<p><b>Rating: {run["rating"]}/5.</b> {esc(run["rating_why"])}</p>'
            body += '<h2 id="findings">What they found</h2><ol class="findings">' + "".join(
                f'<li id="{esc(f["id"])}">{cost_chip(f["cost"])} <span class="small dim">{ulink(f["unit"])}{", step " + str(f["step"]) if f.get("step") else ""}</span><br>{esc(f["what"])}'
                + (f'<blockquote class="q">{esc(f["quote"])} <span class="ok">&#10003; verbatim</span></blockquote>' if f.get("quote") else "")
                + (f'<p class="small chk"><b>Checked:</b> {chip(s["checks"][f["id"]]["verdict"])} {esc(s["checks"][f["id"]]["how"])}</p>' if f["id"] in s["checks"] else "") + "</li>"
                for f in run["findings"]) + "</ol>"
            if run.get("recommendations"):
                body += '<h2>What they would change, most important first</h2><ol>' + "".join(f"<li>{esc(r)}</li>" for r in run["recommendations"]) + "</ol>"
        page(f"{base}{pid}.html", f"{p['name']}, synthetic reader of {st['candidate']}", body,
             f"{p['name']} (invented), Generation {p['generation']}, reading {st['candidate']}: the run, the interview, what they found.",
             crumbs=crumbs + ((p["name"], f"{base}{pid}.html"),), extra_head=H)

    # ---- the findings page
    def answer_cell(fid):
        a = s["answers"].get(fid)
        return f'{chip(a["answer"])} {esc(a.get("why", ""))}' if a else '<span class="dim small">awaiting the editor</span>'
    frows = "".join(
        f'<tr><td>{cost_chip(f["cost"])}</td><td><a href="{esc(pid)}.html#{esc(f["id"])}">{esc(f["id"])}</a><br><span class="small dim">{name(pid, False)}</span></td>'
        f'<td>{ulink(f["unit"])}</td><td>{esc(f["what"])}</td><td>{(chip(s["checks"][f["id"]]["verdict"]) + " " + esc(s["checks"][f["id"]]["how"])) if f["id"] in s["checks"] else "<span class=\'dim small\'>not checked</span>"}</td><td>{answer_cell(f["id"])}</td></tr>'
        for pid, f in allf)
    page(f"{base}findings.html", f"What the readers found in {st['candidate']}", f"""<h1>What the readers found in {esc(st['candidate'])}</h1>
<p class="lede">{len(allf)} findings from {len(runs)} readers, ordered by what they cost, not by who found them. Each points at a unit of the candidate, so anybody can check it. Every finding gets an answer; declined, with a reason, is one of them, and none is deleted.</p>
<p>{''.join(f'<span class="stat"><b>{fcount.get(c, 0)}</b><span>{esc(costs[c]["label"])}</span></span>' for c in costs)}</p>
<div class="tablewrap"><table class="findings-t"><thead><tr><th>Cost</th><th>Finding</th><th>Unit</th><th>What</th><th>Checked</th><th>Answer</th></tr></thead><tbody>{frows or '<tr><td colspan="6" class="dim">No runs yet.</td></tr>'}</tbody></table></div>""",
         f"Every finding of the synthetic readers of {st['candidate']}, by cost, with its check and its answer.", crumbs=crumbs + (("Findings", base + "findings.html"),), extra_head=H, wide=True)

    # ---- the interviews, question by question
    iv = ""
    qs = protocol["interview"]
    for i, q in enumerate(qs):
        iv += f'<h2 id="q{i + 1}">{i + 1}. {esc(q)}</h2><dl class="iv">' + "".join(f'<dt>{name(pid)}</dt><dd>{esc(r["interview"][i])}</dd>' for pid, r in runs.items()) + "</dl>"
    pubs = [(pid, r) for pid, r in runs.items() if personas[pid].get("role") == "publisher"]
    for k, q in enumerate(protocol["publisher_interview"]):
        iv += f'<h2 id="p{k + 1}">Publisher {k + 1}. {esc(q)}</h2><dl class="iv">' + "".join(f'<dt>{name(pid)}</dt><dd>{esc(r["interview"][len(qs) + k])}</dd>' for pid, r in pubs) + "</dl>"
    page(f"{base}interviews.html", f"The interviews, {st['candidate']}", f"""<h1>The interviews, question by question</h1>
<p class="lede">The same questions for every reader, so the answers read down a column as well as across a run.</p>
{iv or '<p class="note">No runs yet.</p>'}""", f"The synthetic readers' interviews on {st['candidate']}, question by question.",
         crumbs=crumbs + (("Interviews", base + "interviews.html"),), extra_head=H)

    # ---- the study page
    syn = s["synthesis"] or {}
    rows = ""
    for pid, p in personas.items():
        r = runs.get(pid)
        if r:
            c = counts(r)
            pd = r.get("put_down")
            rows += (f'<tr><td>{name(pid)}<br><span class="small dim">{esc(p["situation"].split(".")[0])}</span></td><td>{esc(p["generation"])}{" &middot; publisher" if p.get("role") == "publisher" else ""}</td>'
                     f'<td><i>{esc(p["arrives_with"])}</i></td><td>{ulink(pd["unit"]) if pd else "the end"}<br><span class="small dim">{c["read_natural"]:,} of {total_words:,} words</span></td>'
                     f'<td>{decision_chip(r["buy_at_put_down"]["decision"])}</td><td>{decision_chip(r["decision"].get("commission") or r["decision"]["buy"])}</td>'
                     f'<td>{r["rating"]}/5</td><td>{c["questions"]}</td><td>{c["confusions"]}</td><td>{c["findings"]}</td></tr>')
        else:
            rows += f'<tr><td>{name(pid)}</td><td>{esc(p["generation"])}</td><td><i>{esc(p["arrives_with"])}</i></td><td colspan="7" class="dim">not run yet; expected: {esc(journeys[pid]["expected_put_down"])}; buy: {esc(journeys[pid]["expected_buy"])}</td></tr>'
    # the book, unit by unit: who read, skimmed, skipped or stopped where, interest and pace
    grid = ""
    for uid, u in units.items():
        cells, ints, paces = "", [], Counter()
        for pid in personas:
            r = runs.get(pid)
            xs = [x for x in (r["steps"] if r else []) if x["unit"] == uid]
            x = next((y for y in xs if y["phase"] == "natural"), xs[0] if xs else None)
            if x:
                cls = f'{x["mode"]}{" asked" if x["phase"] == "asked" else ""}'
                tip = f'{personas[pid]["name"]}: {x["mode"]}{" (asked)" if x["phase"] == "asked" else ""}' + ("" if x["mode"] == "skip" else f', interest {x["interest"]}/5, {x["pace"]}')
                cells += f'<td class="cell {cls}" title="{esc(tip)}">{"" if x["mode"] == "skip" else x["interest"]}</td>'
                for y in xs:
                    if y["mode"] != "skip":
                        ints.append(y["interest"]); paces[y["pace"]] += 1
            else:
                cells += '<td class="cell none" title="not opened"></td>'
        avg = f"{sum(ints) / len(ints):.1f}" if ints else ""
        pc = " ".join(f'{n}&times; {esc(k)}' for k, n in paces.most_common()) or ""
        rowcls = ' class="partrow"' if u["kind"] != "chapter" else ""
        grid += f'<tr{rowcls}><td class="u">{ulink(uid)}</td><td class="small dim">{u["words"]:,}</td>{cells}<td>{avg}</td><td class="small">{pc}</td></tr>'
    heads = "".join(f'<th class="rot"><a href="{esc(pid)}.html">{esc(p["name"].split()[0])}</a></th>' for pid, p in personas.items())
    recs = "".join(
        f'<li>{cost_chip(r["cost"])} <b>{esc(r["what"])}</b><br>{esc(r["why"])} <span class="small dim">From {", ".join(f"""<a href="findings.html">{esc(k)}</a>""" for k in r.get("from", []))}.</span></li>'
        for r in syn.get("recommendations", []))
    body = f"""<h1>{esc(st['title'])}</h1>
<p class="lede">{esc(syn.get('summary') or st['asked_by'])}</p>
<div class="disclose">{esc(st["disclosure"])} <span class="small">Candidate <a href="{up}{esc(st['candidate_file'])}">{esc(st['candidate'])}</a>, sha256 <code>{esc(st['candidate_sha256'][:16])}&hellip;</code>, read on {esc(st['date'])}.</span></div>
<p><a href="{up}readers/protocol.html">The protocol</a> &middot; <a href="findings.html">every finding</a> &middot; <a href="interviews.html">the interviews, question by question</a> &middot; <a href="{up}team/editor/briefs/book__v2.0.0-rc2__synthetic-readers.md">the brief</a></p>"""
    if syn.get("will_they_buy"):
        body += f'<h2 id="buy">Will they buy it?</h2><div class="answer">{md(syn["will_they_buy"])}</div>'
    body += f"""<h2 id="readers">The five readers</h2>
<div class="tablewrap"><table class="readers-t"><thead><tr><th>Reader (invented)</th><th>Gen</th><th>Arrives with</th><th>Put it down at</th><th>Buy, there</th><th>At the end</th><th>Rating</th><th>Questions</th><th>Confusions</th><th>Findings</th></tr></thead><tbody>{rows}</tbody></table></div>"""
    if syn.get("expected_vs_actual"):
        body += '<h2 id="expected">What we expected, and what happened</h2>' + md(syn["expected_vs_actual"])
    if recs:
        body += f'<h2 id="recommendations">What would make it better, by what it costs</h2><ol class="recs">{recs}</ol>'
    if syn.get("strengths"):
        body += '<h2 id="strengths">What is strong</h2><ul>' + "".join(f"<li>{esc(x)}</li>" for x in syn["strengths"]) + "</ul>"
    body += f"""<h2 id="map">The book, unit by unit</h2>
<p class="small">Each column is a reader; each cell is what they did with that unit in the natural phase (or, faded, in the asked phase), and the number is their interest out of 5. Where the cells go pale is where the book loses people. <span class="cell read key">read</span> <span class="cell skim key">skim</span> <span class="cell skip key">skip</span> <span class="cell stop key">put down</span> <span class="cell read asked key">asked</span> <span class="cell none key">not opened</span></p>
<div class="tablewrap"><table class="grid"><thead><tr><th>Unit</th><th>Words</th>{heads}<th>Interest</th><th>Pace</th></tr></thead><tbody>{grid}</tbody></table></div>"""
    if syn.get("method_notes"):
        body += '<h2 id="notes">How it was run, and what went wrong</h2>' + md(syn["method_notes"])
    page(f"{base}index.html", st["title"], body, f"{st['title']}: whether they would buy it, where they put it down, and what they found.",
         crumbs=crumbs, extra_head=H, wide=True)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "check":
        f = Path(sys.argv[2]).resolve()
        sdir = f.parent.parent
        protocol = load_json(R / "protocol.json")
        study = load_json(sdir / "study.json")
        units = units_of((ROOT / study["candidate_file"]).read_text(encoding="utf-8"))
        personas = {p["id"]: p for p in load_json(sdir / "personas.json")["personas"]}
        errs = check_run(load_json(f), units, personas, protocol, f.name)
        print("\n".join(errs) if errs else f"{f.name}: ok")
        sys.exit(1 if errs else 0)
    print(__doc__)
