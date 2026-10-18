---
title: Write it as an article: how I brief the agents that finish this book, and why their first job is to ship the book we already shipped
date: 2026-10-18
author: Dinis Cruz
summary: This is the first article on this site, and it is about the articles themselves. My hypothesis is that an article is a better way to hand an idea, a task or a review to an agent working in another session than a voice memo or a list of tasks. On the newsroom it worked: six articles and two notes, written on 18 October, were enough for one session to build this whole site, v0.1.0, with the book imported, the map, the roles and the vault. Writing an article forces the research before the work: what already exists, what the 2018 book said, what the numbers are, and which choices are mine. So this site now has a journalist, the same role that writes the newsroom's articles, and a section for its articles. The roles keep their names: the reviewer reviews the 2018 text, the editor edits the book, the publisher publishes it, and the journalist writes the articles that brief them. Each article ends with a brief, a numbered list a role can execute, and a short file in that role's briefs folder points at it. The first brief is the one that matters most. Everything we do starts with a version released, and the first version of this book was released in 2018: it is in this repository, frozen as the book was published, 28 chapters and 30,893 words, and so is the 139-page file the paperback was printed from. What is not here is a cover at print size, a way to build the book from this repository, and a record of what went where. So the first job is to release v1.0.0 again, end to end, before a word of the second edition changes. Four more articles follow: that release, one board for the book, everything unfinished in one place, and the loop in which I read, comment and decide, and the editor turns my decisions into the next version.
version: v0.2.1
tags: articles, roles, workflow, release, gen-z-book, article
status: published
---

## In short {#in-short}

- **An article is how I brief an agent.** One page with the idea, the evidence and the task, which another session can read and act on.
- **It worked once already.** Six newsroom articles and two notes of 18 October 2026 were enough to build this site's first release, v0.1.0.
- **Writing it forces the research.** What exists, what the 2018 book said, what the counts are, and what is a decision for me.
- **This site now has a journalist.** The role that writes the newsroom's articles, here writing the briefs for the roles that finish the book.
- **The roles keep their names.** Reviewer, editor, publisher; and the journalist, who writes about the work but does not do it.
- **Every article ends with a brief.** A numbered list, each item with what "done" looks like, and my questions kept apart.
- **The first job is to ship the book we already shipped.** v1.0.0, end to end: a new cover, Leanpub, the paperback, then the same book built here.
- **Four articles follow.** The release, one board, everything unfinished in one place, and how I decide and the editor acts.

## Why an article {#why}

When I want an agent to do something substantial, the instruction I give it is usually a voice memo, and a voice memo is a terrible instruction. It is in the order I thought it, it mixes the idea with the task, it does not say what already exists, and it leaves the agent to guess which parts are decisions and which are thinking out loud.

An article fixes most of that, because writing one is research. Before this one could be written, the journalist had to read this repository, the vault, the two 2018 repositories and the newsroom's guide to its own voice, and count things: how many files the book has, how many are outlines, what the Leanpub build actually included, what is missing for a print run. The agent that reads the article afterwards starts from that record, not from my memo.

There is evidence that it works. The newsroom's six articles tagged `gen-z-book` and its two build notes, all written on 18 October 2026, were handed to one session, and that session built [this site's first release](/admin/versions.html): the 2018 book imported and frozen, the versions page, [the map](/map/index.html) of 138 files to the newsroom articles that answer them, three roles with their first issues, and the public vault. Those eight pages are kept here as [the briefs](/briefs/index.html). One session, from articles, to a working site.

And an article is something I can read. I can correct it, argue with it, or say "yes, that", before any work starts. A list of tasks does not invite that; an argument does.

## A journalist, here as on the newsroom {#journalist}

So this site now has [a journalist](/team/journalist/index.html), the role that writes the newsroom's articles, and a place for its articles at [/articles/](/articles/index.html). It writes in the same voice and the same shape as the newsroom: my voice, in the first person, from my memo; plain words; a title that is a hook and an argument; *In short*, the argument in sections, *What this does not claim*, *Where this comes from*. The newsroom's guide to that, *Writing here: the voice, the shape, the contract and the run*, holds here too.

Each article has a markdown twin next to its page, `articles/<slug>.md`. That is the file to hand to an agent.

There is a second stream, for the agents' own voice. When an agent finishes a significant body of work, it writes an [agent article](/articles/index.html#agents): what it did, the flows, the changes, what it leaves for the other roles, and who decided what. These articles are co-written with me, in my voice; those are written by the agents, in theirs, and they name me where a decision was mine.

## The roles, and their names {#roles}

I wondered whether "editor" was the right name for the role that changes the book. I think it is: in publishing, the editor is the person who works on the text with the author, and that is exactly the job. So the names stay, with one added:

| Role | What it does | What it does not do |
|---|---|---|
| [Reviewer](/team/reviewer/index.html) | Reads the 2018 text and records findings, one record per chapter, each with its evidence and a verdict | Write the new text, or fix anything in `v1/` |
| [Editor](/team/editor/index.html) | Interviews me, takes my decisions, and changes the book: the chapter map, the drafts, the next version | Publish, or decide for me |
| [Publisher](/team/publisher/index.html) | Builds and publishes each official version: the PDFs, the cover, Leanpub, Amazon, the record of what went where | Change the text, or publish anything that is not in this repository |
| [Journalist](/team/journalist/index.html) | Writes the articles that brief the other three: researched, counted, ending with a brief | Do the work the article asks for |

The rule from [the issues guide](/team/index.html) stays: a role writes only in its own folder, and work for a role arrives as a brief in its `briefs/`. So the journalist never opens an issue for the editor. It writes the article, and a short brief in the editor's folder that says "read this article; its last section is your brief".

## How an article becomes work {#flow}

1. I record a memo, or say it in a session like this one.
2. The journalist reads the record, does the research and the counting, and writes the article, ending with a section called *The brief*.
3. The journalist writes a short file in each role's `briefs/` that points at the article.
4. I read the article, and correct it if it is wrong.
5. I open a session for the role and say: read this article, and take it from there.
6. That session opens its own issues from the brief, does the work, and reports back in a debrief stamped with the version it worked on.
7. If the work shows the article was wrong, the article is corrected; if it raises something new, that is the next article.

The role that receives the article can be any session. What matters is that it reads the role's `role.md` first, and holds to what that role refuses.

## The first job: ship the book we already shipped {#first-job}

Everything I do starts with getting a version out. A version that is not released is not finished, and the release process is only real once it has run end to end.

This book has a released version already. The 2018 first edition is [in this repository](/v1/book/index.html), frozen as v1.0.0 and, since site v0.2.0, exactly as it was published: 28 chapters and the GitHub issues page, [30,893 words](/v1/versions/index.html), with the 6 drafts and 89 outlines kept apart. The 139-page, 6 by 9 inch file the paperback was printed from, typeset by Leanpub on 8 October 2018, is here too.

What is not here is a way to make that book ourselves. Nothing in this repository can build it: the 2018 file was made by Leanpub from another repository, and the second edition cannot be. There is no EPUB, no metadata sheet, no upload checklist, no record of which file went where. So the first thing to do, before any word of the second edition changes, is to release v1.0.0 again: built here, in every format from the same source, matched page by page against the file Leanpub made in 2018, and uploaded as our own file, to Leanpub first and then Amazon. When the second edition's first version arrives, releasing it is a rebuild, not a project.

## The series {#series}

| | Article | For | Done when |
|---|---|---|---|
| 2 | [Release the book we already released](/articles/release-the-book-we-already-released.html) | Publisher | v1.0.0 is built here, matches the 2018 file, and is uploaded to Leanpub and then Amazon, in every format from one source |
| 3 | [One board for the book](/articles/one-board-for-the-book.html) | Editor, with every role | Every issue is a file, the board on the site is built from the files, and content issues name the version and the sentence |
| 4 | [Everything unfinished in one place](/articles/everything-unfinished-in-one-place.html) | Editor | The outlines, the drafts, the 2018 GitHub issues and my notes are in one inventory, each item with a decision slot |
| 5 | [Read, comment, decide](/articles/read-comment-decide.html) | Editor, and me | On [the editor's desk](/read/index.html), the first batch of my decisions is recorded and acted on, and the loop has run once |

They are in that order on purpose. Release first; then the board, because everything after it needs somewhere to be tracked; then the pile; then the loop that works through it.

## The brief {#brief}

For the journalist, which is how this article checks itself:

1. Publish this article and the four that follow at `/articles/`, each with a markdown twin. Done when the site's gate passes with all five.
2. Put a brief in `team/publisher/briefs/` for article 2, and in `team/editor/briefs/` for articles 3, 4 and 5. Done when each role's page lists its brief.
3. When a role's debrief comes back, read it against the article, and correct the article if the work found it wrong.

For me:

1. Read the five articles and correct what is wrong.
2. Open a session as the publisher and point it at article 2; open one as the editor and point it at article 3.

## What this does not claim {#limits}

- **The hypothesis is one data point.** One site built from eight newsroom pages in one session; whether articles beat lists as instructions in general is not measured.
- **The journalist is new here.** The voice and the shape are the newsroom's, used for the first time on this site.
- **"Editor" is my choice of name.** The role could be split later, if editing the text and running the interviews turn out to be different jobs.
- **These articles have no figures.** The newsroom's articles carry drawn figures; these use tables, and figures can follow.
- **Nothing in the series is built yet.** Each article is a brief; the work is the roles'.

If you are running a role on this book, or want to see how this works for your own project, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, in the session that wrote this article, written up by this site's journalist, `gen-z.journalist`, in my voice. The argument and the editorial responsibility are mine.

The record read for it: this repository at site v0.2.0 (`README.md`, `CLAUDE.md`, `team/`, `admin/content/`, `read/`); the public vault `c14khrb8`, cloned read-only; [DinisCruz/Book_Generation_Z_Developer](https://github.com/DinisCruz/Book_Generation_Z_Developer) and [DinisCruz/Book_Generation_Z_Developer_Build](https://github.com/DinisCruz/Book_Generation_Z_Developer_Build), cloned; the newsroom's `admin/content/articles/README.md`, the guide to its voice and shape. The counts: 30,893 words from `wc -w v1/versions/v1.0.0.md`; the print file's pages and size from `v1/generation-z-print-ready.pdf`, read with pypdf; the cover's size from `v1/images/title_page.png`; the paperback and Leanpub figures from `admin/content/book/versions.json`. Site v0.2.0 is where the published book was split from the drafts and the print file came in.
