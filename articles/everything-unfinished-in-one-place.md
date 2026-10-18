---
title: Everything unfinished in one place: the outlines, the drafts, the 2018 GitHub issues and my handwritten notes, as one inventory I can read through and decide on
date: 2026-10-18
author: Dinis Cruz
summary: The first edition left a lot unfinished, and it is scattered. In the frozen source there are 89 outlines, a title and a few bullet points each; 23 files sit in folders called draft; six chapters were written in 2018 but never published; 31 of the outlines have no newsroom article that answers them yet, and 58 do. The 2018 repository has 43 GitHub issues, 35 of them still open, most of them ideas for chapters. There is a printed copy at home with my handwritten notes in it, if I can find it. And there are the questions the newsroom's notes and the vault's board already put to me. Today, to see all of that, you have to open the map, the book pages, the drafts page, the vault, the captured GitHub data and my memory. I want it in one place, as an inventory: one row per item, whatever kind it is, with where it came from, what it says, what the map says about it, and an empty slot for my decision. The inventory is generated from the files, so it does not drift, and every row links to the page where I can read the item in full. A lot of these items are not chapters waiting to be finished; they are ideas, and some of them should become articles first, on this site or the newsroom, and only then chapters, which is the way books from articles proposes. So the inventory is the input to the loop in the next article, in which I read each item, say what I think, and the editor acts on it. This article is about building the pile, counted and in one place, so that the loop has something to work through.
version: v0.2.1
tags: inventory, outlines, drafts, issues, triage, gen-z-book, article
status: published
---

## In short {#in-short}

- **The unfinished parts are scattered.** The map, the book pages, the drafts page, the vault, the GitHub capture and my memory.
- **There is a lot of it.** 89 outlines, 23 files in draft folders, six written chapters never published, 35 open GitHub issues, my handwritten notes.
- **The map already did half the work.** 58 outlines have a newsroom article that answers them; 31 have none.
- **I want one inventory.** One row per item, whatever its kind, with its source, what it says, the map's reading, and a slot for my decision.
- **Generated from the files.** So it cannot drift, and every row links to the full item.
- **Many items are ideas, not chapters.** Some should become articles first, and chapters after.
- **The inventory feeds the loop.** The next article is how I read it, decide, and the editor acts.

## The pile, counted {#pile}

All of these numbers come from the files in this repository, the map, and the 2018 repositories.

| What | How many | Where it is now |
|---|---|---|
| Outlines: a title, "Topics to cover and ideas", a few bullets | 89 | `v1/content/`, shown on [the book pages](/v1/book/index.html) and [the map](/map/index.html) |
| of which a newsroom article answers it | 58 | the map's `articles` column |
| of which nothing answers it yet | 31 | the map says "no article yet" |
| Files in the 2018 `draft/` folders | 23 | `v1/content/2.mvp-for-gen-z-dev/draft/` (12), `3.technologies/draft/` (10), `5.concepts/draft/` (1) |
| Written in 2018 but never published | 6 | marked draft, so the Leanpub build left them out, now on [the drafts page](/v1/book/drafts.html): STEM tech stack, gamification, Leanpub, books to read, diagrams to add, Gen Z research |
| Published chapters, to review | 28 | the edition [the previous article](/articles/release-the-book-we-already-released.html) rebuilds |
| GitHub issues of the 2018 repository | 43, 35 open | `admin/content/github/`, captured by site v0.2.0; 15 labelled `new-content`, 9 `reader-feedback`, 5 `show-in-book` |
| Figures the 2018 source never generated | 3 | the STEM diagrams, the reviewer's open issue |
| My handwritten notes | unknown | a printed copy at home, not yet found |
| Questions already put to me | 7 | the vault's `board/BOARD.md` |

The 23 draft files and the 89 outlines overlap: most draft files are outlines, and one, *Wallaby and NCrunch*, was published from its draft folder. The inventory counts each file once and says which piles it is in.

## Why one place {#why}

When I sit down to make decisions about this book, I want to read, not search. Right now, to decide what happens to the outline on *Nudge*, I would open its page on the site, check the map row, see that no newsroom article answers it, remember whether I ever wrote about it anywhere else, and then decide. Multiply that by a hundred and fifty items and it does not happen.

An inventory turns that into reading down a list. Each row has what I need to decide, and a link to the rest. And because the inventory is built from the same files as the map and the board, adding an item somewhere else (a new content issue, a reader's comment, a page of my notes) adds a row here, without anyone remembering to.

## What a row carries {#row}

| Field | What it is |
|---|---|
| Item | the title, as the source has it |
| Kind | outline, draft, unpublished chapter, published chapter, GitHub issue, handwritten note, question, reader feedback |
| Source | the file and version, or the issue's link, or the page of the notes |
| What it says | one or two lines: the bullets of an outline, the ask of an issue, the gist of a note |
| The map's reading | the newsroom articles that answer it, or the gap |
| The review | the reviewer's verdict, when there is one |
| Decision | empty until I decide; then the decision, linked to its record |

The decision is the only field I fill in, and I do not fill it in here: I record it in the loop, and the inventory shows it. That keeps the inventory a view, generated, with nothing in it edited by hand.

## Many items are ideas, not chapters {#ideas}

Reading the 31 outlines that nothing answers yet, most are not chapters waiting for their text. *Nudge*, *Start with why*, *The power of habits* and *Netflix culture* are books and ideas I wanted a reader to know about. *Strings should be banned* and *Pointers* are arguments I have made in talks. *BBS and modems* is history. Some of them are still right, some are not, and some should become something other than a chapter.

That is the pattern [books from articles](https://newsroom.sgit.ai/articles/books-from-articles.html) describes, and it is how the newsroom answered 58 of these outlines without planning to: the idea is written as an article first, where it can be read, argued with and corrected on its own, and the chapter is written later, from the article. So one of the decisions an item can get is "article first". The journalist writes it, here or on the newsroom, and the item waits for the article before it becomes a chapter.

The handwritten notes are a different kind of pile. They are my reactions to the 2018 text, in the margin. If I find the copy, each page is photographed, and each note becomes a row that points at the page of the book it is written on. If I do not find it, the second-best thing is the loop itself: I read the book again and comment as I go, which is what the next article sets up.

## Where the inventory lives {#where}

The inventory is a page on this site, `inventory/index.html`, generated by the build from:

- `admin/content/map.json`, for every file of v1.0.0, its kind and the articles that answer it;
- the content issues, including the 2018 GitHub issues, which live in the vault's `board/issues/` ([decision 005](/decisions/index.html#text-issues-live-in-the-vault)): the vault board script from [one board for the book](/articles/one-board-for-the-book.html) also writes them as one JSON file, and a snapshot of it is committed here at each release, the way `map.json` is copied the other way;
- `admin/content/notes/`, a new folder for the handwritten notes, one file per page photographed, with the page of the book it refers to;
- the decision records of the next article, which also live in the vault and come in with the same snapshot, for the decision column.

And it is written as `inventory.json` too, so that an agent can read the whole pile in one file. It is grouped by part of the book, in reading order, with a filter for kind and for "no decision yet".

## The brief {#brief}

For the editor. Read `team/editor/role.md` first; the reviewer reads along.

1. **Teach the build to write the inventory**: `inventory/index.html` and `inventory.json`, one row per item, the fields above, grouped by part, filterable by kind and by "no decision yet". Done when every file of v1.0.0 has a row and the counts on the page match the table in this article, or the article is corrected.
2. **Mark the overlaps.** A draft file that is also an outline is one row, with both kinds. Done when the inventory's count of rows is the number of distinct items, and the page says how it was counted.
3. **Add the content issues** from the vault board's snapshot, once it exists, including the 2018 GitHub issues. Done when each issue is a row with its link.
4. **Create `admin/content/notes/`** with a README saying how a page of handwritten notes becomes a file, and ask me whether I have found the printed copy. Done when the answer is recorded, either way.
5. **Mark the candidates for "article first"**: the outlines with no newsroom article, as a filter, so I can read them together. Done when the filter shows the 31.
6. **Add the inventory to the navigation and `llms.txt`.**

Questions for me, kept apart:

- Have I found the printed copy with my notes?
- Should the six written but unpublished chapters be read as part of v1.0.0, or as drafts?

## What this does not claim {#limits}

- **Nothing here is built.** The inventory is a proposal; the editor builds it.
- **The counts are the map's.** "Answered" means the map names at least one newsroom article; whether the article really answers the outline is the reviewer's open issue.
- **The GitHub counts are from a capture** taken on 18 October 2026; an issue opened since is not in it.
- **My notes may not exist any more.** The copy has not been found.
- **"Most are ideas, not chapters" is my reading** of the 31 outlines without an article, not a count.

If you read the 2018 book and remember a chapter you wanted it to have, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice. The argument and the editorial responsibility are mine.

The counts: `admin/content/map.json` at site v0.2.0, rows grouped by `kind` (89 outlines, of which 58 name at least one article and 31 none) and by `status_2018` (the six written chapters whose 2018 status is not `content`); the 23 draft files by `find v1/content -path '*draft*' -name '*.md'`; the 28 published chapters as counted in the previous article. The GitHub issues are counted from `admin/content/github/issues-p1.json` by state and label, pull requests left out; the seven questions from the vault's `board/BOARD.md`. Related: [books from articles](https://newsroom.sgit.ai/articles/books-from-articles.html), [Generation Z Developers, again](/briefs/03__generation-z-developers-again.html).
