#!/usr/bin/env python3
"""The contributors to the first edition: who did what, from the 2018 repository's git history and its GitHub record.

Reads (all under admin/content/github/, captured 2026-10-18):
  git-log.txt          git log --format='%H|%an|%ae|%ad|%s' --date=short --numstat --all, from a full clone of
                       DinisCruz/Book_Generation_Z_Developer at 6188644
  issues-p*.json       GET /repos/.../issues?state=all (issues and pull requests, GitHub lists both here)
  pulls.json           GET /repos/.../pulls?state=all
  comments-p*.json     GET /repos/.../issues/comments
  contributors.json    GET /repos/.../contributors
  repo.json            GET /repos/...
Writes admin/content/contributors.json, which build.py renders at contributors/index.html.

Names: a git author and a GitHub login are joined by hand in ALIASES below, from the merge commits ("Merge pull
request #37 from clazba/master") and the emails; the join is a reading, and the raw data stays beside it.
"""
import json
import re
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
G = ROOT / "admin/content/github"
OUT = ROOT / "admin/content/contributors.json"

# git author name -> (display name, GitHub login or None)
ALIASES = {
    "Dinis Cruz": ("Dinis Cruz", "DinisCruz"),
    "Sarah Cruz": ("Sarah Cruz", "sarahallencruz"),
    "Mike Eriksson": ("Mike Eriksson", "swedishmike"),
    "Martin": ("Martin O'Brien", "mobrien-gw"),
    "clazba": ("Claudio Camerino", "clazba"),
    "Claudio Camerino": ("Claudio Camerino", "clazba"),
    "didadida5555": ("didadida5555", "didadida5555"),
    "Sam Willis": ("Sam Willis", "samwillis4216"),
    "Mark Regensberg": ("Mark Regensberg", "mregensberg"),
    "StevenJV": ("Steven Vore", "StevenJV"),
    "Mikail Tunç": ("Mikail Tunç", "emtunc"),
    "Kevin Johnson": ("Kevin Johnson", "secureideas"),
    "Kenneth Jhim Infante": ("Kenneth Jhim Infante", "kennethinfante"),
    "Michael Chadwick": ("Michael Chadwick", "Chuddington"),
}
LOGIN_NAMES = {login: name for name, login in ALIASES.values()}
LOGIN_NAMES.update({"russmiles": "Russ Miles", "francoise-cruz": "Françoise Cruz", "michaelhidalgo": "Michael Hidalgo",
                    "mooreds": "Dan Moore", "shamsul910": "shamsul910", "Immortalin": "Immortalin", "dave-theunsub": "dave-theunsub",
                    "1lastBr3ath": "1lastBr3ath"})

# the 2018 change log's own credits (content/_manuscript/change-log.md)
CHANGELOG_CREDITS = {
    "v0.60": ["Mike Eriksson", "Michael Chadwick", "Claudio Camerino"],
    "v0.50": ["Mark Regensberg", "Sarah Cruz"],
}


def load_list(name):
    d = json.loads((G / name).read_text(encoding="utf-8"))
    return d if isinstance(d, list) else []


def parse_log():
    commits, cur = [], None
    for line in (G / "git-log.txt").read_text(encoding="utf-8").split("\n"):
        if re.match(r"^[0-9a-f]{40}\|", line):
            h, an, ae, d, s = line.split("|", 4)
            cur = {"sha": h, "author": an, "email": ae, "date": d, "subject": s, "files": []}
            commits.append(cur)
        elif cur and re.match(r"^(\d+|-)\t(\d+|-)\t", line):
            a, dl, f = line.split("\t", 2)
            cur["files"].append((f, 0 if a == "-" else int(a), 0 if dl == "-" else int(dl)))
    return commits


def main():
    commits = parse_log()
    issues_all = load_list("issues-p1.json") + load_list("issues-p2.json")
    prs = [i for i in issues_all if "pull_request" in i]
    issues = [i for i in issues_all if "pull_request" not in i]
    comments = load_list("comments-p1.json") + load_list("comments-p2.json")
    repo = json.loads((G / "repo.json").read_text(encoding="utf-8"))
    pulls = {p["number"]: p for p in load_list("pulls.json")}

    people = OrderedDict()

    def person(name, login=None):
        key = login or name
        p = people.get(key)
        if p is None:
            p = people[key] = {"name": name, "login": login, "commits": 0, "merges": 0, "lines_added": 0, "lines_deleted": 0,
                               "files": set(), "chapters": set(), "first": None, "last": None, "prs_opened": 0, "prs_merged": 0,
                               "issues_opened": 0, "comments": 0, "credited_in_changelog": [], "pr_titles": []}
        return p

    for c in commits:
        name, login = ALIASES.get(c["author"], (c["author"], None))
        p = person(name, login)
        if c["subject"].startswith("Merge"):
            p["merges"] += 1
        else:
            p["commits"] += 1
        p["first"] = min(p["first"] or c["date"], c["date"])
        p["last"] = max(p["last"] or c["date"], c["date"])
        for f, a, d in c["files"]:
            p["lines_added"] += a
            p["lines_deleted"] += d
            p["files"].add(f)
            if f.startswith("content/") and f.endswith(".md"):
                p["chapters"].add(f[len("content/"):])

    for pr in prs:
        login = pr["user"]["login"]
        p = person(LOGIN_NAMES.get(login, login), login)
        p["prs_opened"] += 1
        merged = bool(pr["pull_request"].get("merged_at"))
        if merged:
            p["prs_merged"] += 1
        p["pr_titles"].append({"number": pr["number"], "title": pr["title"], "state": "merged" if merged else pr["state"],
                               "date": (pr["pull_request"].get("merged_at") or pr["created_at"])[:10], "url": pr["html_url"]})
    for i in issues:
        login = i["user"]["login"]
        person(LOGIN_NAMES.get(login, login), login)["issues_opened"] += 1
    for c in comments:
        login = c["user"]["login"]
        person(LOGIN_NAMES.get(login, login), login)["comments"] += 1
    for ver, names in CHANGELOG_CREDITS.items():
        for n in names:
            for p in people.values():
                if p["name"] == n:
                    p["credited_in_changelog"].append(ver)

    rows = []
    for p in people.values():
        rows.append({**p, "files": len(p["files"]), "chapters": sorted(p["chapters"]), "chapters_count": len(p["chapters"]),
                     "role": "author" if p["login"] == "DinisCruz" else "contributor"})
    rows.sort(key=lambda r: (r["role"] != "author", -(r["commits"] + r["prs_merged"] * 2 + r["issues_opened"] + r["comments"])))

    by_month = Counter()
    for c in commits:
        by_month[c["date"][:7]] += 1
    for i in issues_all:
        by_month[i["created_at"][:7]] += 0  # keep the month on the axis
    issues_by_month = Counter(i["created_at"][:7] for i in issues)
    prs_by_month = Counter(p["created_at"][:7] for p in prs)
    months = sorted(set(by_month) | set(issues_by_month) | set(prs_by_month))

    labels = Counter(l["name"] for i in issues for l in i["labels"])
    show_in_book = [{"number": i["number"], "title": i["title"], "state": i["state"], "url": i["html_url"], "by": i["user"]["login"], "date": i["created_at"][:10]}
                    for i in issues if any(l["name"] == "show-in-book" for l in i["labels"])]
    issue_rows = [{"number": i["number"], "title": i["title"], "state": i["state"], "by": LOGIN_NAMES.get(i["user"]["login"], i["user"]["login"]),
                   "labels": [l["name"] for l in i["labels"]], "date": i["created_at"][:10], "comments": i["comments"], "url": i["html_url"]}
                  for i in sorted(issues, key=lambda i: i["number"])]
    pr_rows = [{"number": p["number"], "title": p["title"], "by": LOGIN_NAMES.get(p["user"]["login"], p["user"]["login"]),
                "state": "merged" if p["pull_request"].get("merged_at") else p["state"], "date": p["created_at"][:10],
                "merged": (p["pull_request"].get("merged_at") or "")[:10] or None, "url": p["html_url"],
                "files_changed": pulls.get(p["number"], {}).get("changed_files")}
               for p in sorted(prs, key=lambda p: p["number"])]

    non_merge = [c for c in commits if not c["subject"].startswith("Merge")]
    doc = {
        "what": "Who contributed to the first edition, from the 2018 repository's git history and its GitHub issues, pull requests and comments, captured 2026-10-18. Names are joined to GitHub logins by hand (gen_contributors.py ALIASES); the raw data is beside this file under admin/content/github/.",
        "repository": {"url": repo["html_url"], "created": repo["created_at"][:10], "last_push": repo["pushed_at"][:10],
                       "stars": repo["stargazers_count"], "forks": repo["forks_count"], "open_issues": repo["open_issues_count"], "licence_file": repo["license"]["spdx_id"] if repo.get("license") else None},
        "totals": {"people": len(rows), "contributors": len(rows) - 1, "commits": len(non_merge), "merge_commits": len(commits) - len(non_merge),
                   "commits_by_contributors": sum(r["commits"] for r in rows if r["role"] != "author"),
                   "pull_requests": len(prs), "pull_requests_merged": sum(1 for p in prs if p["pull_request"].get("merged_at")),
                   "issues": len(issues), "issues_open": sum(1 for i in issues if i["state"] == "open"), "issues_closed": sum(1 for i in issues if i["state"] == "closed"),
                   "comments": len(comments), "first_commit": min(c["date"] for c in commits), "last_commit": max(c["date"] for c in commits),
                   "first_issue": min(i["created_at"] for i in issues_all)[:10], "last_issue": max(i["created_at"] for i in issues_all)[:10],
                   "chapters_touched_by_contributors": len({ch for r in rows if r["role"] != "author" for ch in r["chapters"]})},
        "by_year": {y: sum(1 for c in non_merge if c["date"].startswith(y)) for y in sorted({c["date"][:4] for c in commits})},
        "timeline": [{"month": m, "commits": by_month.get(m, 0), "issues": issues_by_month.get(m, 0), "prs": prs_by_month.get(m, 0)} for m in months],
        "labels": labels.most_common(),
        "show_in_book": show_in_book,
        "people": rows,
        "pull_requests": pr_rows,
        "issues": issue_rows,
        "changelog_credits": CHANGELOG_CREDITS,
    }
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    t = doc["totals"]
    print(f"gen_contributors: {t['people']} people, {t['commits']} commits ({t['commits_by_contributors']} by contributors), "
          f"{t['pull_requests_merged']}/{t['pull_requests']} PRs merged, {t['issues']} issues ({t['issues_open']} open), {t['comments']} comments -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
