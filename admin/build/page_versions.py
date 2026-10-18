#!/usr/bin/env python3
"""A version history for a page this site writes, the way every article has one.

    from page_versions import Versions
    v = Versions("publishers", "admin/content/publishers")
    entry = v.current(source_text)       # the version the source is at; exits if the text changed and no version says so
    v.freeze(entry, md_text)             # <page>/versions/<version>.md, written once and never again
    v.ledger(state, site, today)         # <page>/changes.json: what the page's live parts did, per release
    v.index_page(...)                    # <page>/versions/index.html: the versions, the differences, the ledger

An article's versions are read from git history by publish.py. A page like For publishers is different: part of it is
the editor's text, which changes when someone decides it should, and part of it is live, rebuilt in every release from
the site's data (the features register, the newest articles). So it keeps two records:

  versions.json (beside the page's source)   one entry per version of the TEXT: the version, the date, the release,
                                              who wrote it, why, and the sha256 of the source it was built from. A
                                              build whose source no longer hashes to the newest entry stops and asks
                                              for a version, so the text cannot change without one. A change to the
                                              text is the next minor version; a rewrite is the next major, the editor's
                                              call. Each version is frozen as markdown at <page>/versions/<v>.md by the
                                              release that made it, live parts included, and never rewritten.
  <page>/changes.json                        one entry per release in which the LIVE parts changed: features added,
                                              removed or changed status, articles that came into or left the latest.
                                              Written by the build, compared with the state it last recorded, so a
                                              second run in the same release changes nothing.

The differences between two frozen versions are computed at build, block by block and then word by word, and shown on
the versions page. Nothing here is specific to For publishers; another page gets a history by calling the same four.
"""
import difflib
import hashlib
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def words(text):
    return len(re.findall(r"[\w'’£%.-]+", text))


def rebase_links(md, prefix):
    """Relative links in a page's markdown, made to work from one folder deeper (<page>/versions/)."""
    def fix(m):
        url = m.group(2)
        if re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*:|#|/)", url):
            return m.group(0)
        return m.group(1) + prefix + url + m.group(3)
    return re.sub(r"(\]\()([^)\s]+)(\))", fix, md)


def blocks(md):
    """The text of a frozen version as blocks for comparison: paragraphs, list items, rows and headings, without the
    lines every twin carries (the source line, the rule, the site-index foot)."""
    out, cur = [], []
    for line in md.splitlines():
        s = line.strip()
        if s.startswith(("*Source:", "*[Site index")) or re.fullmatch(r"-{3,}|\|[-|: ]+\|", s):
            s = ""
        if not s or re.match(r"^(#{1,4} |[-*] |\d+[.)] |\|)", s):
            if cur:
                out.append(" ".join(cur)); cur = []
            if s:
                cur.append(s)
            continue
        cur.append(s)
    if cur:
        out.append(" ".join(cur))
    return [readable(b) for b in out]


def readable(block):
    """A block as it reads: link text without its target, no emphasis markers, no quote mark. Two versions that link
    the same words to different addresses (sgit.ai's absolute links, this site's relative ones) read the same."""
    block = re.sub(r"!?\[([^\]]*)\]\([^)\s]*\)", r"\1", block)
    block = re.sub(r"\*\*|(?<![\w*])\*(?=\S)|(?<=\S)\*(?![\w*])|`", "", block)
    return re.sub(r"^>\s*", "", block).strip()


def word_diff(a, b):
    aw, bw = a.split(" "), b.split(" ")
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw, autojunk=False).get_opcodes():
        if op == "equal":
            out.append(html.escape(" ".join(aw[i1:i2])))
            continue
        if i2 > i1:
            out.append(f'<del>{html.escape(" ".join(aw[i1:i2]))}</del>')
        if j2 > j1:
            out.append(f'<ins>{html.escape(" ".join(bw[j1:j2]))}</ins>')
    return " ".join(out)


def diff(old_md, new_md):
    """(counts, html): the blocks kept, changed, removed and added between two frozen versions."""
    a, b = blocks(old_md), blocks(new_md)
    n = {"kept": 0, "changed": 0, "removed": 0, "added": 0}
    rows = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            n["kept"] += i2 - i1
            continue
        olds, news = a[i1:i2], b[j1:j2]
        # pair each old block with the most similar new one still free, when they are close enough to read as an edit
        free = list(range(len(news)))
        pairs = {}
        for i, o in enumerate(olds):
            best = max(free, key=lambda j: difflib.SequenceMatcher(None, o, news[j]).ratio(), default=None)
            if best is not None and difflib.SequenceMatcher(None, o, news[best]).ratio() >= 0.5:
                pairs[i] = best
                free.remove(best)
        paired_new = {j: i for i, j in pairs.items()}
        for i, o in enumerate(olds):
            if i not in pairs:
                n["removed"] += 1
                rows.append(f'<div class="pv-blk pv-del"><span class="pv-k">removed</span> <del>{html.escape(o)}</del></div>')
        for j, s in enumerate(news):
            if j in paired_new:
                n["changed"] += 1
                rows.append(f'<div class="pv-blk pv-chg"><span class="pv-k">changed</span> {word_diff(olds[paired_new[j]], s)}</div>')
            else:
                n["added"] += 1
                rows.append(f'<div class="pv-blk pv-add"><span class="pv-k">added</span> <ins>{html.escape(s)}</ins></div>')
    return n, "\n".join(rows)


class Versions:
    def __init__(self, page_dir, content_dir):
        self.page_dir = page_dir.strip("/")
        self.file = ROOT / content_dir / "versions.json"
        self.data = json.loads(self.file.read_text(encoding="utf-8"))
        self.entries = self.data["versions"]
        for e in self.entries:
            if not VERSION.match(e["version"]):
                sys.exit(f"page_versions: {self.file}: {e['version']!r} is not vX.Y.Z")
        keys = [tuple(map(int, VERSION.match(e["version"]).groups())) for e in self.entries]
        if keys != sorted(keys) or len(set(keys)) != len(keys):
            sys.exit(f"page_versions: {self.file}: the versions are not in order, or one is listed twice")

    def snapshot(self, e):
        return f"{self.page_dir}/versions/{e['version']}.md"

    def current(self, source_text):
        e = self.entries[-1]
        got = sha(source_text)
        if e.get("text_sha256") != got:
            major, minor, _ = map(int, VERSION.match(e["version"]).groups())
            sys.exit(f"page_versions: the source of {self.page_dir}/ changed and {self.file.relative_to(ROOT)} has no version for it.\n"
                     f"  Add an entry after {e['version']}: v{major}.{minor + 1}.0 for a change to the text (v{major + 1}.0.0 for a rewrite),\n"
                     f"  with the date, the release, who wrote it, why, and \"text_sha256\": \"{got}\".")
        return e

    def freeze(self, e, md_text):
        """The version's markdown, written by the release that made it and never again."""
        p = ROOT / self.snapshot(e)
        if p.exists():
            return False
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(rebase_links(md_text, "../"), encoding="utf-8")
        return True

    def missing(self):
        return [self.snapshot(e) for e in self.entries if not (ROOT / self.snapshot(e)).exists()]

    def ledger(self, state, site, today, what):
        """Append an entry to <page>/changes.json when the live parts differ from the state last recorded."""
        p = ROOT / self.page_dir / "changes.json"
        doc = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"what": what, "entries": [], "state": None}
        doc["what"] = what
        last = doc.get("state")
        if last == state:
            return doc, False
        entry = {"site": site, "date": today, "page": self.entries[-1]["version"]}
        if last is None:
            entry["baseline"] = True
            entry["features"] = sorted(state["features"])
            entry["latest"] = state["latest"]
        else:
            lf, nf = last["features"], state["features"]
            entry["features_added"] = sorted(set(nf) - set(lf))
            entry["features_removed"] = sorted(set(lf) - set(nf))
            entry["status_changed"] = [[k, lf[k], nf[k]] for k in sorted(set(lf) & set(nf)) if lf[k] != nf[k]]
            entry["latest_added"] = [s for s in state["latest"] if s not in last["latest"]]
            entry["latest_left"] = [s for s in last["latest"] if s not in state["latest"]]
            if last.get("start_here") != state.get("start_here"):
                entry["start_here"] = state["start_here"]
            entry = {k: v for k, v in entry.items() if v not in ([], None)}
        # one entry per release: a second change in the same release replaces that release's entry
        if doc["entries"] and doc["entries"][-1]["site"] == site and not doc["entries"][-1].get("baseline"):
            doc["entries"].pop()
        doc["entries"].append(entry)
        doc["state"] = state
        p.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        return doc, True

    def history_html(self):
        """The versions table, the differences between consecutive versions, newest first."""
        rows, diffs = [], []
        prev_md = None
        texts = {}
        for e in self.entries:
            p = ROOT / self.snapshot(e)
            texts[e["version"]] = p.read_text(encoding="utf-8") if p.exists() else ""
        for i, e in enumerate(self.entries):
            md = texts[e["version"]]
            w = words("\n".join(blocks(md)))
            if prev_md is None:
                change = "first published"
                body = ""
            else:
                n, body = diff(prev_md, md)
                change = f'{n["changed"]} changed, {n["added"]} added, {n["removed"]} removed, {n["kept"]} kept'
            rows.append(
                f'<tr><td><b>{html.escape(e["version"])}</b></td><td>{html.escape(e["date"])}</td><td>{html.escape(e["site"])}</td>'
                f'<td>{w:,}</td><td>{html.escape(change)}</td>'
                f'<td><a href="{html.escape(e["version"])}.md">the text</a>'
                + (f' &middot; <a href="#{html.escape(e["version"])}">the changes</a>' if body else "") + '</td></tr>')
            if body:
                prev = self.entries[i - 1]["version"]
                diffs.append(
                    f'<h3 id="{html.escape(e["version"])}">{html.escape(prev)} to {html.escape(e["version"])}, {html.escape(e["date"])}</h3>'
                    f'<p>{html.escape(e["why"])}</p><p class="dim">By {html.escape(e["by"])}. {html.escape(change)} (by blocks: a paragraph, '
                    f'a list item, a heading or a table row, compared as they read, without link addresses). Deleted words are struck through, added words underlined.</p>'
                    f'<details{" open" if i == len(self.entries) - 1 else ""}><summary>Every block that changed</summary>{body}</details>')
            prev_md = md
        rows.reverse(); diffs.reverse()
        table = ('<div class="tablewrap"><table><thead><tr><th>Version</th><th>Date</th><th>Release</th><th>Words</th>'
                 '<th>Change from the version before</th><th></th></tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>')
        return table, "\n".join(diffs)


def ledger_html(doc, feats, by_slug, up):
    """The live parts' changes, per release, newest first."""
    out = []
    for e in reversed(doc["entries"]):
        items = []
        if e.get("baseline"):
            items.append(f'Recording starts: {len(e["features"])} features and {len(e["latest"])} newest articles on the page.')
        for k in e.get("features_added", []):
            items.append(f'Feature added: <b>{html.escape(feats.get(k, {}).get("name", k))}</b>')
        for k in e.get("features_removed", []):
            items.append(f'Feature removed: {html.escape(feats.get(k, {}).get("name", k))}')
        for k, a, b in e.get("status_changed", []):
            items.append(f'{html.escape(feats.get(k, {}).get("name", k))}: {html.escape(a)} to {html.escape(b)}')
        for s in e.get("latest_added", []):
            t = by_slug.get(s, {}).get("title", s)
            items.append(f'Newest for publishers: <a href="{up}articles/{html.escape(s)}.html">{html.escape(t)}</a>')
        if e.get("latest_left"):
            items.append(f'{len(e["latest_left"])} older article(s) left the newest for publishers')
        if "start_here" in e:
            items.append("The five to start with changed")
        out.append(f'<li><b>{html.escape(e["site"])}</b>, {html.escape(e["date"])}, page {html.escape(e["page"])}<ul>'
                   + "".join(f"<li>{i}</li>" for i in items) + "</ul></li>")
    return '<ol class="pv-ledger" reversed>' + "".join(out) + "</ol>"
