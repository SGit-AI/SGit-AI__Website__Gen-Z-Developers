# gen-z-developers.sgit.ai — the second edition of Generation Z Developers

The website for reviewing and finishing the second edition of Dinis Cruz's 2018 book
*Generation Z Developers*, built on one rule:

> **The repository holds the official versions; the vault holds the working versions.**

v1.0.0 is the first edition exactly as published: the 28 chapters the 2018 build put in the
Leanpub book and the print PDF (139 pages, 30 September 2018), in that order. It is in this
repository, frozen, and the site shows it chapter by chapter. The 2018 repository also held 5
drafts and 89 outlines the build left out; they are kept beside the book, marked, as the second
edition's raw material, and are not part of any version. Everything after it is worked on in a public, encrypted vault whose **read** key is
published, so anyone can read along. A version moves from the vault into the repository when it
is signed off, on top of the one before, and the versions page shows the delta between every two
versions, block by block and word by word.

Live site: https://gen-z-developers.sgit.ai (GitHub Pages, deployed from `dev`; address to confirm).

## Where this comes from

The six newsroom articles tagged `gen-z-book` and the two build briefs of 18 October 2026, all
captured verbatim under `admin/content/briefs/` and rendered at `/briefs/`:

1. [Hired for the workflow](https://newsroom.sgit.ai/articles/hired-for-the-workflow.html)
2. [Act as the job you want](https://newsroom.sgit.ai/articles/act-as-the-job-you-want.html)
3. [Generation Z Developers, again](https://newsroom.sgit.ai/articles/generation-z-developers-again.html) — the plan for the edition
4. [A book for one reader](https://newsroom.sgit.ai/articles/a-book-for-one-reader.html)
5. [A website to finish the book](https://newsroom.sgit.ai/articles/a-website-to-finish-the-book.html) — the plan for this site
6. [Short, punchy, and co-written with Claude](https://newsroom.sgit.ai/articles/short-punchy-and-co-written.html)

and the notes [Generation Z Developers, second edition](https://newsroom.sgit.ai/admin/notes/2026-10-18__generation-z-developers-second-edition.md)
and [a website to finish the book](https://newsroom.sgit.ai/admin/notes/2026-10-18__a-website-to-finish-the-book.md).

## Layout

```
index.html            the front page
v1/                   THE FIRST EDITION, FROZEN
  MANIFEST.json       what v1 is, where it came from, the counts
  content/            the 2018 book's content/ folder, verbatim (DinisCruz/Book_Generation_Z_Developer @ 6188644)
  images/             its figures
  generation-z-print-ready.pdf   the print edition, 139 pages (the published book)
  book/               generated: one page per chapter and draft, the table of contents (published, then drafts),
                      single.html (the published book), drafts.html and drafts.md (the rest), book.json (the book as
                      blocks, for read/), manifest.json
  versions/           generated: v1.0.0.md (the published book frozen as one markdown file) and the versions page
read/                 generated shell + assets/reader.js, reader.css: the reader and the editor's desk. Content left,
                      graph right; chapter states, comments on paragraphs, filters and folds, a reading meter after
                      the newsroom's rules, export of the review as markdown/JSON. Everything stays in the browser
                      (localStorage genz.reader.v1) until exported.
contributors/         generated: who contributed to the first edition, from git and GitHub (admin/content/contributors.json)
map/                  generated: one row per 2018 file, the newsroom articles that answer it, the gap
briefs/               generated: the articles and notes above, rendered
storyboards/          generated: the cast sheet and a swipe deck per storyboard, drawn in the browser from admin/content/storyboards/*.json
articles/             generated: this site's own articles (admin/content/articles/), each with its markdown twin; the briefs for the roles
team/                 the roles: reviewer, editor, publisher, journalist
  ISSUES.md           how the roles keep issues (the folder is the status)
  <role>/role.md      Identity, Foundation, Primary Responsibilities, Core Workflows
  <role>/issues/      open/ blocked/ done/
  <role>/briefs/      what the role was asked (the editor's first interview script is here)
  <role>/debriefs/    what the role reports back, stamped with the version reviewed
vault/                generated: how to open the working vault, read-only
admin/
  build/version.txt   the site's version (vX.Y.Z), bumped once per release
  build/gen_map.py    writes admin/content/map.json: the authored chapter-to-article reading
  build/gen_contributors.py  writes admin/content/contributors.json from admin/content/github/ (git log, issues, PRs)
  build/build.py      writes every page, the manifests, the frozen markdown, book.json, llms.txt, the sitemap
  build/page_versions.py  the newsroom's version differ (newsroom v0.12.113), copied, not rewritten
  build/validate.js   the gate
  content/            the authored data: map.json, briefs/, articles/, agent-articles/, decisions/, storyboards/, newsroom/survey.json, book/versions.json, book/print-toc.json (the print
                      PDF's table of contents, matched to the files), contributors.json, github/ (the raw record of
                      the 2018 repository), versions.json, vault.json
  index.html, versions.html   admin and the narrated release history
assets/site.css       the one stylesheet
llms.txt, sitemap.xml, robots.txt, 404.html, CNAME
.github/workflows/deploy-pages.yml   validate -> tag -> deploy, the same pipeline as the sibling sites
```

## The build

```
python3 admin/build/gen_map.py     # only when the authored reading in gen_map.py changes
python3 admin/build/build.py       # every page
node admin/build/validate.js       # the gate: version, links, canonical, key leak, freeze, map, sitemap
```

Dependencies: Python 3 with `markdown` (`pip install markdown`), Node 18+.

## The rules the gate enforces

- **`v1/` is frozen.** `build.py` stops if the assembled v1 text no longer hashes to the newest entry in
  `admin/content/book/versions.json`; `validate.js` stops if a chapter page no longer matches its markdown
  or markdown changed behind its page (`v1/book/manifest.json`).
- **Markdown is the source of truth.** Every chapter page, brief and role page is a projection of a
  markdown file.
- **No private key in the tree.** Any string carrying sgit's private-key prefix fails the build. The public
  read key on the vault page is public by design.
- **Every release is narrated** in `admin/content/versions.json` (rendered at `admin/versions.html`), and
  the version in `admin/build/version.txt` must appear in the commit subject as `site vX.Y.Z: ...`.

## The release ritual

1. `git fetch origin dev --tags` first; other agents may have shipped.
2. Bump `admin/build/version.txt` (next patch, or a deliberate `.0` minor) and add a row to
   `admin/content/versions.json` saying, in substance, what changed and why.
3. `python3 admin/build/build.py && node admin/build/validate.js`, both green.
4. Commit as `site vX.Y.Z: what changed`; push your branch; push to `dev` only as a complete release.
   CI validates, tags `vX.Y.Z` and deploys.

## The vaults

- **Public working vault** `gen-z-developers` (id `c14khrb8`, on `dev.send.sgraph.ai`): the working copy of
  v1, the map, the reviews, interviews, board, team folders. Its read key is on the vault page and in
  `admin/content/vault.json`. Its write key is not in this repository and never will be.
- **Private vault** `gen-z-developers-private` (id `z292ze46`): for the OpenRouter key, with a credit
  limit, held by Dinis. Nothing else.

## Licences

The 2018 text is the author's, under the Creative Commons licence the book itself declares (CC BY on the
cover and in the Introduction, CC BY-SA in the footer; the 2018 repository's own file says Apache 2.0, kept
as `v1/LICENSE-2018-repository.txt`). The build brief says to treat it as CC BY and confirm with Dinis;
that question is open on the reviewer's board. Everything written for this site is CC BY 4.0; code under
the repository licence (`LICENSE`, Apache 2.0).
