---
title: One board for the book: every issue a file, a Kanban page built from the files, and every content issue pinned to a version and a sentence
date: 2026-10-18
author: Dinis Cruz
summary: To finish a book with agents in several roles, I need to see, in one place, what is open, what is blocked, what is done, and what is waiting on me. This site already has the pieces: each role keeps its issues as files, in folders called open, blocked and done, where the folder is the status, which is the pattern graphs.sgit.ai calls Issues-FS-lite. There are ten of them today, across three roles. What it does not have is the view across them. The vault's board is a markdown file that someone rewrites by hand whenever an issue moves, which means it will drift. And there is a second kind of issue that has nowhere to live yet: the content issue, a finding about a sentence of the book, from the reviewer, a reader, an old GitHub issue or me. A content issue is not a task for a role; it is a question about the text, and it needs the file, the version, the sentence quoted, and in the end an answer: fixed, declined with its reason, or deferred to a later version. So the proposal is one board, built from files. Work issues stay where they are, in each role's folder. Content issues get a folder of their own, with the same three statuses and a fixed set of fields. The build reads all of them and writes a Kanban page on this site, with a column per status, a card per issue, and a filter by role, by kind and by the version an issue is meant for. The board in the vault becomes a copy of that page, never written by hand. The 2018 book's own GitHub issues, 43 of them, 35 still open, come in as content issues, each with its link. And the gate checks the fields, so an issue without a "done when", or a finding without its sentence, does not get in.
version: v0.2.1
tags: issues, board, kanban, workflow, versions, gen-z-book, article
status: published
---

## In short {#in-short}

- **I need one view of the work.** What is open, blocked and done, across the roles, and what waits on me.
- **The pieces exist.** Each role keeps issues as files in open, blocked and done; the folder is the status; ten issues today.
- **The view across them is written by hand.** The vault's board is rewritten whenever an issue moves, so it will drift.
- **A second kind of issue has nowhere to live.** The content issue: a finding about a sentence of the book, which needs the version, the quote and an answer.
- **Work issues stay with the roles; content issues get a folder of their own.** Same three statuses, fixed fields.
- **The build writes the board.** A Kanban page on this site, a column per status, filters by role, kind and target version.
- **The vault's board becomes a copy.** Never edited by hand again.
- **The 2018 GitHub issues come in as content issues.** 43 of them, 35 still open, each with its number and link.

## What we have {#have}

[The issues guide](/team/index.html) this site started with is short, and it is right: each role owns `team/<role>/issues/open|blocked|done/`, the folder is the status, a status change is a `git mv`, a file is `NNN__slug.md` and is never renumbered, and only the owning role writes into its folder. There is no tool, and that is a feature: an agent in any session can read and move a file.

Today there are ten issues:

| Role | Open | Blocked | Done |
|---|---|---|---|
| Reviewer | 3 | 1 (the licence, waiting on me) | 0 |
| Editor | 2 | 1 (the chapter map, waiting on the review and the first interview) | 0 |
| Publisher | 2 | 1 (the Web Summit launch, waiting on a signed-off version) | 0 |

The view across them is `board/BOARD.md` in the vault: a markdown list of the ten, plus seven questions for me. Its own first line says it is "rewritten by whoever moves an issue". That will work for ten issues and one session. It will not work for a hundred issues and four sessions, because the one thing a hand-written index is guaranteed to do is fall behind the files it indexes.

## Two kinds of issue {#kinds}

Most of what will happen to this book is not a task. It is a question about the text.

- **A work issue** is a task for a role: build the PDF, run the first interview, check the map. It has a "what", a "done when", where it came from, and, when blocked, what it waits on. It belongs to one role and lives in that role's folder. This is what exists.
- **A content issue** is a finding about the book: a spelling mistake in a chapter, a 2018 claim that dated, a broken link, a reader saying a chapter lost them, a 2018 GitHub issue asking for a chapter on coordinated disclosure, or me saying a paragraph is wrong. It belongs to the book, not to a role. It needs the file, the version read, the sentence quoted, the kind, who raised it, and in the end an answer.

The reviewer's role already describes content issues without naming them: findings, numbered, each with its evidence and severity, and an answer recorded next to it, "fixed (where), declined (why), or deferred (to which version)". The proposal is to give them a home that every role and the board can see, rather than leaving them inside review records.

## Where content issues live {#where}

In this repository, at `board/content/open|blocked|done/`, with the same rules as the roles' folders: the folder is the status, `NNN__slug.md`, never renumbered, never deleted.

I know that bends the rule that the vault holds the working versions. My reasoning: an issue is not a version of the book, it is a record about one, and the board on the site can only be built from files the build can read. And the repository gives every issue a history for free. The drafts of the text stay in the vault; the record of what we found and decided lives here. If the editor sees a reason this is wrong, that is a question for me, not a decision to make quietly.

Who writes: any role may create a content issue, and records itself as the one who raised it. Only the editor moves one to done, because only the editor changes the text; a content issue is done when its answer is recorded, whether that answer is "fixed in v1.1.0" or "declined, because the book is not doing that". A content issue waiting on my decision is blocked, with **Waits on.** Dinis.

The fields, in the same style as the work issues:

```
# <the finding, as a sentence>

**File.** v1/content/<path>.md
**Version.** book v1.0.0
**Quote.** "<the sentence, word for word>"
**Kind.** spelling | dated | wrong | missing | broken link | structure | reader | idea
**Raised by.** reviewer | editor | publisher | journalist | Dinis | reader (source) | 2018 GitHub issue #N
**For.** the book version this should land in, or "undecided"
**Answer.** fixed (where, which version) | declined (why) | deferred (to which version)
```

The **Quote** is checked: the gate finds the quoted sentence in the named file at the named version, and fails if it is not there, which is the newsroom's rule that a quote is word for word, applied to findings.

## The board {#board}

The build reads every work issue and every content issue and writes `board/index.html`, a Kanban page:

- **Three columns**, open, blocked and done, because those are the statuses the folders have. No "in progress" column: a role that is working on an issue says so in its debrief, and a fourth folder would be a fourth thing to keep in step.
- **A card per issue**: the title, the role or "content", the kind, the version it is for, and for a blocked card, what it waits on.
- **Filters** by role, by kind, and by target version, so "everything that has to land in v1.1.0" is one click.
- **A "waits on Dinis" strip** at the top: every blocked issue whose **Waits on.** names me, and the open questions. This is the part I will read every day.
- **Counts per column and per role**, which the publisher's and the editor's debriefs can quote.

It is generated, like every page here, so it is never edited by hand. At each release, the build also writes `board/BOARD.md` for the vault, the same content as markdown, and that replaces the hand-written one.

## The 2018 GitHub issues {#github}

The first edition took feedback through GitHub issues, and showed some of them in the book: the 2018 Leanpub build has a page listing the issues labelled `show-in-book`. Site v0.2.0 captured the whole of the 2018 repository's issues, pull requests and comments under `admin/content/github/`, for [the contributors page](/contributors/index.html). Counted from that capture:

| | Issues | Open | Closed |
|---|---|---|---|
| All | 43 | 35 | 8 |
| labelled `new-content` | 15 | | |
| labelled `improvement` | 10 | | |
| labelled `reader-feedback` | 9 | | |
| labelled `show-in-book` | 5 | | |

And 24 pull requests, 21 of them merged. The eight closed issues are a typo on the cover and seven notes from one reader on the chaos engineering chapter; the 35 open ones run from 22 February 2018 to 3 October 2019, and most are ideas for chapters: coordinated disclosure, closure, typography and design, cloud-native, the C4 model, "understand what game is being played", summits versus conferences, HTTP from the basics, "is this book just for Gen Z".

Each comes in as a content issue, raised by "2018 GitHub issue #N", with its link, its date, its labels and its author, so the people who asked are credited if the book does what they asked. The 35 open ones go in `open/`; the 8 closed ones go straight to `done/`, with the answer the 2018 repository records. Issue 3 deserves attention of its own: it says fixes were made in the Leanpub build repository and never brought back to the source, which means the published text and the frozen source may differ in places, and [the previous article](/articles/release-the-book-we-already-released.html) asks the publisher to check.

## The gate {#gate}

What `validate.js` should refuse, so the board stays honest:

- A work issue without **What.**, **Done when.** and **From.**; a blocked one without **Waits on.**
- A content issue without **File.**, **Version.**, **Quote.** and **Kind.**, or a quote that is not in the file at that version.
- A content issue in `done/` without an **Answer.**
- A number used twice in the same folder.
- A status written inside a file, since the folder is the status.

## The brief {#brief}

For the editor, with the other roles reading along. Read `team/editor/role.md` and `team/ISSUES.md` first.

1. **Create `board/content/open|blocked|done/`** and add the content issue format to `team/ISSUES.md`. Done when the guide describes both kinds and an example content issue passes the gate.
2. **Teach the build to write the board**: `board/index.html` from every role's issues and the content issues, with the three columns, the filters, the counts and the "waits on Dinis" strip; and `board/BOARD.md` for the vault. Done when moving an issue with `git mv` and rebuilding moves its card, with nothing else edited.
3. **Teach the gate the checks above.** Done when each check has a failing example that it refuses.
4. **Bring in the 43 GitHub issues of the 2018 repository** from `admin/content/github/` as content issues, generated rather than typed, open ones in `open/` and closed ones in `done/`. Done when every issue has a file, and the board's count matches the capture's.
5. **Move the seven open questions from the vault's board** into blocked issues that wait on me, each in the role that needs the answer. Done when the "waits on Dinis" strip shows them and the hand-written board is gone.
6. **Add the board to the navigation and to `llms.txt`.**

Questions for me, kept apart:

- Content issues in the repository rather than the vault: agreed?
- Only the editor closes a content issue: agreed?

## What this does not claim {#limits}

- **Nothing here is built.** The board is a proposal; the editor builds it.
- **The GitHub counts are from a capture.** `admin/content/github/` as site v0.2.0 took it on 18 October 2026; an issue opened since is not in it.
- **No "in progress" column is a choice.** If the roles find they need one, it is a fourth folder and a change to the guide.
- **Content issues in the repository bends a rule.** The reasoning is above; I have not decided it yet.
- **A Kanban page is a view, not a tool.** There is no drag and drop; a card moves when its file moves.

If you keep a board like this for your own writing, or have opinions on what it should show, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice. The argument and the editorial responsibility are mine.

The record: `team/ISSUES.md` and the ten issue files under `team/*/issues/` in this repository at site v0.2.0, counted by folder; `board/BOARD.md` in the public vault `c14khrb8`, cloned read-only on 18 October 2026, quoted from its first line; `team/reviewer/role.md` for the finding format and its answers. The 2018 issues are counted from `admin/content/github/issues-p1.json` and `pulls.json`, captured by site v0.2.0, by state and label, with pull requests left out of the issue count; the `show-in-book` page is `manuscript/github-issues.md` in [DinisCruz/Book_Generation_Z_Developer_Build](https://github.com/DinisCruz/Book_Generation_Z_Developer_Build), 8 October 2018. The pattern is graphs.sgit.ai's Issues-FS-lite, as `team/ISSUES.md` describes it.
