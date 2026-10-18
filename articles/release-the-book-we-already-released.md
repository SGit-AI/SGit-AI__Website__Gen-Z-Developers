---
title: Release the book we already released: v1.0.0 end to end, first with the 2018 print file and a new cover, then built from this repository, before a word of it changes
date: 2026-10-18
author: Dinis Cruz
summary: The first version of Generation Z Developers was released in September 2018, on Leanpub at 60% and as a 139-page paperback on Amazon. It is in this repository now, frozen as v1.0.0: since site v0.2.0, exactly the book as published, 28 chapters and the GitHub issues page, 30,893 words, with the drafts and outlines kept apart. And the file the paperback was printed from is here too: a 139-page, 6 by 9 inch PDF, typeset by Leanpub on 8 October 2018, fonts embedded. So half of the pipeline exists as an artefact. What does not exist is everything around it: a cover at print size (the only one is a 975 by 1,474 pixel image), a metadata sheet, an upload checklist, a record of which file went where, and above all a way to build the book from this repository. The second edition will need that last one on day one. So I want v1.0.0 released twice, end to end, before a word of it changes. The first release uses the 2018 interior exactly as it is, with a new cover, which proves the publishing half this week: cover, Leanpub, the paperback, the record. The second builds the same book from this repository with the tools the graphs books used, and checks it against the 2018 file: the same 28 chapters in the same order, close to the same 139 pages, every chapter near the page it was on. That proves the build half, so that the second edition's first release is a rebuild, not a project. The words do not change, so the book stays at v1.0.0; each built file carries a stamp and a row in a list of publications. The new cover keeps the 2018 design's four colour blocks and its eight lines, and says first edition. And the uploads are mine, from a checklist.
version: v0.2.1
tags: release, pdf, leanpub, kdp, cover, versions, gen-z-book, article
status: published
---

## In short {#in-short}

- **v1.0.0 is in the repository, as published.** 28 chapters and the GitHub issues page, 30,893 words, frozen; the drafts and outlines kept apart.
- **So is the 2018 print file.** 139 pages, 6 by 9 inches, typeset on 8 October 2018, fonts embedded.
- **What is missing is everything around it.** A cover at print size, a metadata sheet, an upload checklist, a record of publications, and a build from this repository.
- **Release v1.0.0 twice, before the text changes.** First the 2018 interior with a new cover; then the same book built here.
- **The first release proves the publishing half.** Cover, Leanpub, the paperback, the record, this week.
- **The second proves the build half.** Built from `v1/content/`, checked against the 2018 file page by page.
- **The words do not move, so the version does not move.** Each built file gets a stamp and a row in a list of publications.
- **A new cover, recognisably the old one.** The four colour blocks and the eight lines, marked first edition. The uploads are mine.

## Why v1.0.0 first {#why}

[Write it as an article](/articles/write-it-as-an-article.html) says why: everything starts with a version released, and a release process is only real once it has run end to end. The second edition will change the text, the structure, the cover and the title page. If we build the pipeline at the same time as we change all of that, every problem has two possible causes. If we build it on a version that already exists, and whose published form we have in our hands, a problem has one.

And we do have it in our hands. Site v0.2.0 did two things this pipeline depends on: it re-froze v1.0.0 as exactly what the 2018 build published, and it brought in the print-ready PDF the paperback was made from. So there is a reference to check every step against.

## What we have, counted {#have}

| What | Where | The numbers |
|---|---|---|
| The book as published, frozen | [`v1/versions/v1.0.0.md`](/v1/versions/index.html) | 28 chapters plus the GitHub issues page, in the print order; 30,893 words; sha256 `cc0b4ced…` |
| The drafts and outlines, apart | [`v1/book/drafts.md`](/v1/book/drafts.html) | 6 drafts with text and 89 outlines, 10,841 words; not part of any version |
| The 2018 print file | `v1/generation-z-print-ready.pdf` | 139 pages, 6 by 9 inches, XeTeX through Leanpub, 8 October 2018, fonts embedded as subsets |
| Its table of contents | `admin/content/book/print-toc.json` | every printed chapter, its page, and the 2018 file it came from |
| The rule that made it | the 2018 Hugo layout `layouts/book/leanpub.html` | parts by weight; only pages with `status: content` |
| Leanpub | [leanpub.com/generation-z](https://leanpub.com/generation-z) | 60% complete, 136 pages, 30,695 words, 465 readers, last updated 8 October 2018 |
| The paperback | [Amazon](https://www.amazon.co.uk/Gen-Developers-concepts-generation-developers/dp/1724194607) | 139 pages, 6 by 9 inches, 30 September 2018, ISBN-10 1724194607 |
| The cover | `v1/images/title_page.png` | 975 by 1,474 pixels at 300 dpi: 3.25 by 4.9 inches |

## What we do not have {#gap}

- **No cover at print size.** A 6x9 front at 300 dpi needs 1,800 by 2,700 pixels before bleed; Leanpub's cover wants at least 1,600 by 2,400. The 2018 image is about half of that in each direction, and the 2018 PDF has no cover in it: its first page is the GitHub issues page.
- **No full cover wrap** for the paperback: back, spine and front, with bleed.
- **No build from this repository.** The 2018 file was made by Leanpub from markdown in another repository. Nothing here can make a PDF, and the second edition cannot be typeset by a 2018 Leanpub run.
- **No metadata sheet**: the title, subtitle, description, categories and licence line, written once and used everywhere.
- **No upload checklist**, and **no record of publications**: `admin/content/book/versions.json` says what each version is; nothing says which file of it went where, when.

## Two releases of the same version {#two}

**Release one: the 2018 interior, a new cover.** The print file is the published book, as published. Use it as it is, untouched, with its sha256 recorded, and add what it lacks: the new cover, front and wrap; the metadata sheet; the checklist; the record. This is a release we can make in days, and it tests everything after the PDF: the cover's geometry against KDP's calculator, the Leanpub upload, the paperback update, the row in the record. If something goes wrong here, it is not the typesetting.

**Release two: the same book, built here.** Then the build half. The graphs books have done this twice: [graphs.sgit.ai](https://graphs.sgit.ai/v2/books/index.html) has `admin/build/bookkit/`, which renders print HTML with WeasyPrint and counts the pages it made (including the fix for counting pages in a compressed PDF), and its Leanpub release shipped two books, each with a print PDF, a screen PDF, a cover and a sample. Copy the kit, the way this site copied the newsroom's `page_versions.py`: copied, not rewritten, with a line saying where from. Build v1.0.0 from the same projection the frozen text uses, and check it against the 2018 file:

- the same 28 chapters and the GitHub issues page, in the order `print-toc.json` gives;
- a page count close to 139 (the typeface and the margins will differ, so not equal; the debrief says by how much and why);
- each chapter starting within a few pages of where the 2018 file starts it.

When release two matches, it replaces the 2018 interior on Leanpub and, if I decide, on the paperback. From then on every version, the second edition's included, is built here.

## Version control for the files we build {#builds}

The book's version moves only when its words move, and here they do not, so both releases are v1.0.0. What is new is the files. I want to be able to say, for any PDF anyone holds: which version of the text, which build, which cover, published where, when.

- **Every file carries a stamp in its name**: `generation-z-developers__v1.0.0__print-6x9.pdf`, `__screen.pdf`, `__sample.pdf`, `__cover-wrap.pdf`, `__cover-front.png`, under `v1/publish/`. Release one's interior is the 2018 file, copied under the stamped name, byte for byte.
- **A manifest beside them**, `v1/publish/manifest.json`, generated by the build: for each file, the text's sha256 (which must match `versions.json`), the build (`2018-leanpub` or the site version that built it), the page count, the engine, the trim size, and the file's own sha256. The gate checks the text hash, the same way it checks the chapter pages.
- **A list of publications**, `admin/content/book/publications.json`: one row per upload, with the version, the file, where (Leanpub, KDP), the date, and the link. The publisher writes a row when I confirm an upload; the versions page shows them under the version.
- **A cover change is a new build, not a new version.** The same words with a new cover is v1.0.0, build two.

Built files are generated, like the pages: never edited by hand; change the source and rebuild.

## The PDFs, when we build them {#pdfs}

1. **Print, 6x9.** Mirrored margins with a gutter on the inside, running heads, page numbers, fonts embedded, images at print resolution, chapters starting on a right-hand page. The front matter as 2018 had it: the GitHub issues page, the title page, the contents; plus a copyright and licence page, which 2018 did not have.
2. **Screen.** The same book for reading on a screen, single margins, links live. This is what Leanpub readers get, so it is the book.
3. **Sample.** The front matter and the Introduction, for Leanpub's free sample, cut by the same builder.

The licence page cannot be finished yet: the reviewer's issue on the licence (CC BY on the cover and in the Introduction, CC BY-SA in the footer, Apache 2.0 on the 2018 repository) waits on me. Build it with a placeholder the gate refuses to publish, so the question cannot be forgotten.

## The cover {#cover}

The 2018 cover is navy, with four colour blocks spelling GEN Z and eight lines: question everything, make fact based decisions, understand the history of tech, learn how to learn, understand what game is being played, develop intellectual curiosity, look under the hood, shake things up. I would keep all of it. What it needs is to be redrawn, at print size, as a file we can correct, and to say which book it is.

- **Drawn, not photographed.** An SVG or HTML page in the cover's colours, rendered to PNG and PDF, the way the graphs books' `gen_cover.py` made theirs. Text that can be corrected, rather than a picture that has to be redrawn.
- **The front**, at 1,800 by 2,700 pixels or more, for Leanpub and the site.
- **The full wrap** for the paperback: back, spine and front, with 0.125 inches of bleed on every outer edge. The spine width comes from the page count and the paper, so it is computed from the PDF's page count, not typed in, and checked against KDP's cover calculator before upload.
- **It says first edition.** "First edition, 2018" on the front, so that when the second edition's cover arrives the two cannot be confused.
- **The back** carries the two reader quotes from the Amazon listing that the home page already uses, the eight lines or a short description, and the address of this site.
- **Three options for me to choose from**, as images on one page, rather than one finished design.

## Leanpub and Amazon {#stores}

The Leanpub book, `generation-z`, was built in 2018 from Leanpub markdown pushed to a GitHub repository. The graphs books took the other route, and their publishing plan says why: "Our pipeline is the typesetter; Leanpub is the counter." Upload our own PDF, use the screen PDF as the book, leave the EPUB slot empty until there is a reflowable edition. I think this book should do the same, so that the file on Leanpub is exactly a file in this repository.

The paperback already exists, with its own ISBN, and its text would not change. Refreshing it with the new cover is an update to an existing listing; leaving it is also fine, because the second edition will be a new book with a new ISBN either way. That is my call, and the publisher should prepare both and let me choose.

Nothing is uploaded by an agent. The upload is account work, mine, from a checklist the publisher writes.

## The brief {#brief}

For the publisher. Read `team/publisher/role.md` first. Your open issues `001__the-leanpub-iteration-plan.md` and `002__the-6x9-pdf-and-kdp.md` are this work; fold them in.

Release one:

1. **Draw three cover options**, front and full wrap, the spine computed from 139 pages; reuse graphs.sgit.ai's `gen_cover.py`, copied with its origin noted. Done when one page shows the three at print size, and I have picked one.
2. **Write the metadata sheet** for v1.0.0 (title, subtitle, description, categories, keywords, licence line, author line), once, used by the site and the stores. Done when the site's book page and the sheet cannot disagree because one is built from the other.
3. **Stamp the files**: the 2018 interior copied byte for byte into `v1/publish/` under its stamped name, the cover files beside it, and `v1/publish/manifest.json` generated. Done when the gate checks the manifest's text hash and fails on a wrong one.
4. **Write the upload checklist**: Leanpub (switching to our own PDF), and the paperback in both versions, refresh or leave. Done when it is in `team/publisher/debriefs/book__v1.0.0__upload-checklist.md` and I can follow it without asking.
5. **Create `admin/content/book/publications.json`** and show its rows on the versions page. Done when, after I upload, one row says what went where.

Release two:

6. **Copy the bookkit** from graphs.sgit.ai (`admin/build/bookkit/`) into `admin/build/`, with its origin and commit. Done when `build.py` imports it and nothing in it was rewritten for style.
7. **Build print, screen and sample** from the frozen projection, into `v1/publish/` with the build's stamp. Done when the debrief records the page count against 139, the chapter order against `print-toc.json`, and how far each chapter's first page moved.
8. **Diff the text**: the 2018 GitHub issue 3 says fixes were made in the Leanpub build repository and not brought back to the source. Compare the 2018 PDF's text layer with the frozen markdown, chapter by chapter. Done when the debrief lists every difference, each one a content issue for the editor, not a change to `v1/`.

Questions for me, kept apart:

- The licence of the 2018 text, which the copyright page needs.
- Leanpub: switch to uploading our own PDF?
- Amazon: refresh the 2018 paperback with the new cover, or leave it?
- Which of the three covers.

## What this does not claim {#limits}

- **Nothing in this article is built.** It is the brief; the publisher builds it.
- **The 2018 print file's properties were read from the file**: page count, page size, producer and date from its metadata; "embedded" because its fonts are subsets, not because a preflight tool was run.
- **The 2018 interior is not proof the source is the same.** Issue 3 suggests the published text and the frozen source may differ in places; task 8 checks.
- **The cover sizes are from Leanpub's and KDP's published guidance as the graphs books used it**, not re-checked for this article; the spine width must come from KDP's own calculator.
- **Whether to refresh the paperback is undecided.** Both paths are prepared; I choose.
- **The licence is open.** The copyright page waits on it.

If you have a copy of the 2018 paperback and would want this reissue, or have opinions on the cover, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice. The argument and the editorial responsibility are mine.

The counts: the frozen text's 30,893 words and the drafts' 10,841 are `wc -w` on `v1/versions/v1.0.0.md` and `v1/book/drafts.md` at site v0.2.0, which split the published book from the drafts and brought in the print file; the print file's 139 pages, 6 by 9 inch boxes, fonts and metadata (XeTeX, 8 October 2018) were read with pypdf; the cover's size is from the image file. The selection rule is `layouts/book/leanpub.html` in [DinisCruz/Book_Generation_Z_Developer](https://github.com/DinisCruz/Book_Generation_Z_Developer); issue 3 is in `admin/content/github/issues-p1.json`. The Leanpub and Amazon figures are as `admin/content/book/versions.json` records them. The PDF and cover tooling, and the Leanpub publishing plan quoted, are graphs.sgit.ai's `admin/build/bookkit/pdf.py`, `admin/build/gen_cover.py` and `v2/dev-packs/v0.5.18__the-leanpub-release/00__the-release.md`.
