---
title: Release the book we already released: v1.0.0 end to end, built in this repository, matched page by page to the PDF Leanpub made in 2018, and every format from the same source
date: 2026-10-18
author: Dinis Cruz
summary: The first version of Generation Z Developers was released in September 2018, on Leanpub at 60% and as a 139-page paperback on Amazon. It is in this repository now, frozen as v1.0.0, exactly the book as published: 28 chapters and the GitHub issues page, 30,893 words, with the drafts and outlines kept apart. The file the paperback was printed from is here too: 139 pages, 6 by 9 inches, typeset by Leanpub on 8 October 2018. What is not here is a way to make that book ourselves, and the second edition will need it on day one. So the first release of this project is v1.0.0 again, the same words, built here. We can do everything here. The graphs books already have a print workflow, with scripts that make well aligned 6 by 9 PDFs, and I want to use it, compare what it makes with the PDF Leanpub made in 2018, and keep going until it matches: the same chapters, in the same order, on close to the same pages. Then I upload it to Leanpub, as our own file rather than Leanpub's build, to see if that works, and then to Amazon. It will be interesting to see whether Leanpub's file needs to differ from the printed one, since Leanpub's readers read on screens. And I want every format made here from the same source: the print PDF, the screen PDF, the EPUB, and whatever Kindle needs. The licence is CC BY, as before. The cover can wait; I will decide it later, and it should not hold up anything else. The words do not change, so the book stays at v1.0.0; each file we build carries a stamp and a row in a list of publications, so we always know which file of which version went where.
version: v0.2.1
tags: release, pdf, epub, leanpub, kdp, versions, gen-z-book, article
status: published
---

## In short {#in-short}

- **v1.0.0 is in the repository, as published.** 28 chapters and the GitHub issues page, 30,893 words, frozen; the drafts and outlines apart.
- **So is the 2018 print file.** 139 pages, 6 by 9 inches, typeset by Leanpub on 8 October 2018.
- **What is missing is a way to make the book here.** The second edition will need it on day one.
- **So build v1.0.0 here, and match it to 2018.** The graphs books' print workflow, compared page by page with the Leanpub file.
- **Then upload our own file.** Leanpub first, to see if it works; then Amazon.
- **Every format from one source.** Print, screen, EPUB, and whatever Kindle needs, from the same build.
- **The licence is CC BY; the cover waits.** Neither holds up the build.
- **The words do not move, so the version does not move.** Each file gets a stamp and a row in a list of publications.

## Why v1.0.0 first {#why}

[Write it as an article](/articles/write-it-as-an-article.html) says why: everything starts with a version released, and a release process is only real once it has run end to end. The second edition will change the text, the structure, the cover and the title page. If we build the pipeline at the same time as we change all of that, every problem has two possible causes. If we build it on a version that already exists, and whose published form we have in our hands, a problem has one.

And we do have it in our hands. Site v0.2.0 re-froze v1.0.0 as exactly what the 2018 build published, and brought in the print file the paperback was made from. So there is a reference to check every page against.

## What we have, counted {#have}

| What | Where | The numbers |
|---|---|---|
| The book as published, frozen | [`v1/versions/v1.0.0.md`](/v1/versions/index.html) | 28 chapters plus the GitHub issues page, in the print order; 30,893 words; sha256 `cc0b4ced…` |
| The drafts and outlines, apart | [`v1/book/drafts.md`](/v1/book/drafts.html) | 6 drafts with text and 89 outlines, 10,841 words; not part of any version |
| The 2018 print file | `v1/generation-z-print-ready.pdf` | 139 pages, 6 by 9 inches, XeTeX through Leanpub, 8 October 2018, fonts embedded as subsets |
| Its table of contents | `admin/content/book/print-toc.json` | every printed chapter, its page, and the 2018 file it came from |
| A print workflow | graphs.sgit.ai, `admin/build/bookkit/`, `gen_book.py`, `gen_cover.py` | 6 by 9, no bleed, WeasyPrint; used for two books on Leanpub |
| Leanpub | [leanpub.com/generation-z](https://leanpub.com/generation-z) | 60% complete, 136 pages, 30,695 words, 465 readers, last updated 8 October 2018 |
| The paperback | [Amazon](https://www.amazon.co.uk/Gen-Developers-concepts-generation-developers/dp/1724194607) | 139 pages, 6 by 9 inches, 30 September 2018, ISBN-10 1724194607 |

## What we do not have {#gap}

- **No build from this repository.** The 2018 file was made by Leanpub from markdown in another repository. Nothing here can make a PDF, and the second edition cannot be typeset by a 2018 Leanpub run.
- **No EPUB, and no Kindle file**, from any source.
- **No metadata sheet**: the title, subtitle, description, categories and licence line, written once and used everywhere.
- **No upload checklist**, and **no record of publications**: `admin/content/book/versions.json` says what each version is; nothing says which file of it went where, when.
- **No cover at print size**, which can wait: the 2018 image is 975 by 1,474 pixels, and the Leanpub listing keeps its current cover until I decide.

## Build it here, and match it {#match}

The graphs books have done this twice. [graphs.sgit.ai](https://graphs.sgit.ai/v2/books/index.html) has `admin/build/bookkit/`, which renders print HTML with WeasyPrint and counts the pages it made (including the fix for counting pages in a compressed PDF), and `gen_book.py`, which sets a 6 by 9 interior with no bleed and margins above KDP's minimums. Its Leanpub release shipped two books, each with a print PDF, a screen PDF and a sample. Copy the kit, the way this site copied the newsroom's `page_versions.py`: copied, not rewritten, with a line saying where from.

Then build v1.0.0 from the same projection the frozen text uses, and compare it with the 2018 file until it matches:

- the same 28 chapters and the GitHub issues page, in the order `print-toc.json` gives;
- a page count close to 139 (the typeface and the margins differ, so not equal; the debrief says by how much and why);
- each chapter starting within a few pages of where the 2018 file starts it;
- the same figures, in the same places, at print resolution.

A side by side of the two, page for page, is the evidence: rendered as images, so I can look at it.

## Every format from one source {#formats}

All of them from the same frozen text, by the same build, with the same stamp:

1. **Print, 6 by 9.** Mirrored margins with a gutter, running heads, page numbers, fonts embedded, chapters starting on a right-hand page. The front matter as 2018 had it, the GitHub issues page, the title page, the contents, plus a copyright page that says CC BY 4.0.
2. **Screen.** The same book for reading on a screen, single margins, links live. Leanpub's readers read this one, which is why I suspect Leanpub's file may need to differ from the printed one; the publisher finds out and says.
3. **EPUB**, reflowable, from the same chapters, for Leanpub and for Kindle.
4. **Whatever Kindle needs.** I remember Leanpub wanting MOBI; that may no longer be true, for Leanpub or for Amazon. Check what each accepts today, at the source, and build that.
5. **Sample.** The front matter and the Introduction, for Leanpub's free sample.

## Version control for the files we build {#builds}

The book's version moves only when its words move, and here they do not, so this is v1.0.0. What is new is the files. I want to be able to say, for any file anyone holds: which version of the text, which build, published where, when.

- **Every file carries a stamp in its name**: `generation-z-developers__v1.0.0__print-6x9.pdf`, `__screen.pdf`, `.epub`, `__sample.pdf`, under `v1/publish/`.
- **A manifest beside them**, `v1/publish/manifest.json`, generated by the build: for each file, the text's sha256 (which must match `versions.json`), the site version that built it, the page count, the engine, the trim size, and the file's own sha256. The gate checks the text hash, the same way it checks the chapter pages.
- **A list of publications**, `admin/content/book/publications.json`: one row per upload, with the version, the file, where, the date, and the link. The publisher writes a row when I confirm an upload; the versions page shows them under the version.
- **A new cover later is a new build, not a new version.** The same words with a new cover is still v1.0.0.

Built files are generated, like the pages: never edited by hand; change the source and rebuild.

## Leanpub, then Amazon {#stores}

The Leanpub book, `generation-z`, was built in 2018 from Leanpub markdown pushed to a GitHub repository. The graphs books took the other route, and their publishing plan says why: "Our pipeline is the typesetter; Leanpub is the counter." I want to try that here: switch the listing to uploaded files, upload ours, and see if it works.

Then Amazon. The paperback already exists, with its own ISBN, and its words would not change, so the new interior is an update to an existing listing. The cover question comes back at this point, because a paperback needs a full wrap whose spine depends on the page count; until I decide, the publisher prepares the interior and the checklist, and the wrap waits.

Nothing is uploaded by an agent. The upload is account work, mine, from a checklist the publisher writes.

## The brief {#brief}

For the publisher. Read `team/publisher/role.md` and [the decisions](/decisions/index.html) first. Your open issues `001__the-leanpub-iteration-plan.md` and `002__the-6x9-pdf-and-kdp.md` are this work; fold them in.

1. **Copy the bookkit** from graphs.sgit.ai (`admin/build/bookkit/`, and what `gen_book.py` needs) into `admin/build/`, with its origin and commit. Done when `build.py` imports it and nothing in it was rewritten for style.
2. **Build the print PDF** of v1.0.0 into `v1/publish/`, with the CC BY 4.0 copyright page. Done when it renders with every font embedded.
3. **Match it to 2018**: page count against 139, chapter order against `print-toc.json`, each chapter's first page against the 2018 one, and a page-by-page side by side as images. Done when the debrief shows the comparison and the differences left are explained.
4. **Diff the text**: the 2018 GitHub issue 3 says fixes were made in the Leanpub build repository and not brought back to the source. Compare the 2018 PDF's text layer with the frozen markdown, chapter by chapter. Done when every difference is listed; each one is a text issue for the vault, not a change to `v1/`.
5. **Find out what each store accepts today**: Leanpub (PDF, EPUB, MOBI?) and Amazon KDP (the paperback interior; the Kindle ebook format). Done when the debrief quotes each store's current guidance with its date.
6. **Build the screen PDF, the EPUB, the Kindle format and the sample** from the same source. Done when each opens, and the EPUB passes a validator.
7. **Write `v1/publish/manifest.json`** from the build, and teach `validate.js` to check its text hash. Done when the gate fails on a manifest that names the wrong text.
8. **Write the metadata sheet and the upload checklist**: Leanpub on uploaded files first, then the paperback interior update. Done when the checklist is in `team/publisher/debriefs/book__v1.0.0__upload-checklist.md` and I can follow it without asking.
9. **Create `admin/content/book/publications.json`** and show its rows on the versions page. Done when, after I upload, one row says what went where.
10. **Write an agent article** when the release is done: what you built, how it compares with 2018, what you learned about the stores.

Still mine to decide, later: the cover.

## What this does not claim {#limits}

- **Nothing in this article is built.** It is the brief; the publisher builds it.
- **"Match" is close, not identical.** A different typesetter will not land every line where XeTeX did; the comparison says how close.
- **The 2018 print file's properties were read from the file**: page count, page size, producer and date from its metadata; "embedded" because its fonts are subsets, not because a preflight tool was run.
- **The 2018 interior is not proof the source is the same.** Issue 3 suggests the published text and the frozen source may differ in places; task 4 checks.
- **What the stores accept is not checked here.** Task 5 checks it; my memory of MOBI may be out of date.
- **The cover is undecided**, and the paperback's wrap waits on it.

If you have a copy of the 2018 paperback and would want this reissue, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

Two voice memos of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice; the second carries my decisions on the licence, Leanpub, the formats and the cover, recorded on [the decisions page](/decisions/index.html). The argument and the editorial responsibility are mine.

The counts: the frozen text's 30,893 words and the drafts' 10,841 are `wc -w` on `v1/versions/v1.0.0.md` and `v1/book/drafts.md` at site v0.2.0, which split the published book from the drafts and brought in the print file; the print file's 139 pages, 6 by 9 inch boxes, fonts and metadata were read with pypdf. Issue 3 is in `admin/content/github/issues-p1.json`. The Leanpub and Amazon figures are as `admin/content/book/versions.json` records them. The print workflow and the publishing plan quoted are graphs.sgit.ai's `admin/build/bookkit/pdf.py`, `admin/build/gen_book.py` and `v2/dev-packs/v0.5.18__the-leanpub-release/00__the-release.md`.
