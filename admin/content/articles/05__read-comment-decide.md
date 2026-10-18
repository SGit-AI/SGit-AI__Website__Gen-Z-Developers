---
title: Read, comment, decide: how I go through the pile, one item at a time, and how the editor turns my decisions into the next version of the book
date: 2026-10-18
author: Dinis Cruz
summary: Once everything unfinished is in one place, I need a way to go through it that I will actually use. The answer is the simplest loop I can think of. I read an item on this site, mostly on the editor's desk that site v0.2.0 built: a chapter, an outline, a reviewer's finding, an old GitHub issue, a page of my notes. I say what I think about it, by voice memo or typed, a line or a paragraph, in my own words. And I pick a decision from a short list of verbs: keep, fix, rewrite, merge, cut, article first, later, or not doing it. That is my whole job in the loop. The editor does the rest: records my comment word for word next to the item, turns the decision into a change in the working copy in the vault, and says where it went. A decision is a file, numbered, never deleted, so the record shows what I decided, when, on which version, and why. Not doing it is a valid decision, with its reason, because a book that tries to answer every comment stops being short and punchy. When enough decisions have landed, the editor proposes a version, I sign it off, and the publisher releases it with the pipeline the second article builds, with a delta to the version before. The first batch should be small, so the loop is tested before it carries weight: the five 2018 GitHub issues the first edition printed, and the four chapters of the Introduction. I think the name editor is right for the role that does this: it is the role that works on the text with the author. And the articles, this one included, are where I will think out loud about the bigger decisions before I make them.
version: v0.2.1
tags: review, decisions, editor, workflow, versions, gen-z-book, article
status: published
---

## In short {#in-short}

- **I need a loop I will actually use.** Read an item, say what I think, pick a decision; nothing else is mine to do.
- **The editor's desk is most of my half.** Site v0.2.0's reader: chapter states, comments on paragraphs, an export; nothing leaves the browser.
- **The decision is a verb from a short list.** Keep, fix, rewrite, merge, cut, article first, later, not doing it.
- **My comment is kept word for word.** By voice memo or typed; the editor does not paraphrase it into the decision.
- **The editor does the rest.** Records, acts in the vault's working copy, and says where the change went.
- **Every decision is a file.** Numbered, stamped with the version I read, never deleted.
- **Not doing it is a decision.** With its reason, because a book that answers every comment stops being punchy.
- **Decisions add up to a version.** The editor proposes it, I sign it off, the publisher releases it with a delta.
- **The first batch is small.** The five GitHub issues the first edition printed, and the four chapters of the Introduction.

## The loop {#loop}

Site v0.2.0 built most of my half of this already: [the editor's desk](/read/index.html). It shows a chapter with its graph beside it (its part, its neighbours, the chapters that share its terms, the newsroom articles that answer it), lets me mark each chapter unread, reading, read, to review, continue or signed off, and lets me comment on any paragraph. Everything stays in my browser, and nothing is sent anywhere: the desk exports the review as a markdown file for the vault's `reviews/` folder, or as JSON to carry it to another device. That rule is in `CLAUDE.md` and it stays: no server, no network write.

So the loop is:

1. **I read an item.** A chapter on the desk; or, for what is not a chapter (a content issue on [the board](/articles/one-board-for-the-book.html), an outline, a page of my notes), its row in [the inventory](/articles/everything-unfinished-in-one-place.html).
2. **I comment.** On the paragraph, on the desk; or a voice memo while I read. It can be one line: "still right, but the example is dated". It can be ten minutes.
3. **I decide**, with one of the verbs below. On the desk, the decision sits on the chapter next to its state, and goes out in the export. If I cannot decide, that is a decision too: "later", or a question back to the editor.
4. **I export**, at the end of a sitting, and the file goes in the vault's `reviews/`. For memos, the transcript goes in the vault's `comments/`.
5. **The editor records it**: a decision file per item, my comment verbatim, the verb, my reason if I gave one.
6. **The editor acts**: changes the working copy of the book in the vault, opens a content issue, asks the journalist for an article, or asks the reviewer for a record first. And writes on the decision what it did, and where.
7. **The inventory shows it.** The item's decision column fills in, so the pile visibly shrinks.

I want my part to take seconds per item for the easy ones. Most outlines will get a one-word decision. The hard ones, the chapters that frame the book, get an interview instead, which is the editor's other job.

One distinction matters. On the desk, "signed off" is my state for a chapter as a reader: I have read it and I am done with it. Signing off a version of the book is a different act, made once, on a list of decisions, and it is what moves a version into this repository. The editor should never read one as the other.

## The verbs {#verbs}

| Decision | What the editor does |
|---|---|
| **Keep** | Nothing to the text beyond spelling; the item goes into the next version as it is |
| **Fix** | The specific change I named: spelling, a dated fact, a broken link; a content issue for each |
| **Rewrite** | The chapter is redrafted from my comment, the review and the articles the map names; an interview first if my comment is not enough to write from |
| **Merge into …** | The item's point moves into another chapter, named; the item disappears as a chapter but its decision stays |
| **Cut** | The item is not in the next version; the decision says why |
| **Article first** | The journalist writes the idea as an article, here or on the newsroom; the chapter waits for it |
| **Later** | Deferred to a named version, or "after the second edition's first release" |
| **Not doing it** | Declined, with the reason, which is the answer to whoever asked |

"Not doing it" matters as much as the others. [Short, punchy, and co-written with Claude](/briefs/06__short-punchy-and-co-written.html) says it: sometimes the right answer to an issue is, we are not doing that. Every finding gets an answer; declined, with a reason, is one of them.

## A decision is a file {#record}

In the vault, at `board/decisions/NNN__<slug>.md`, next to the content issues and the working text, because decisions on the text live with the text ([decision 005](/decisions/index.html#text-issues-live-in-the-vault)). Numbered in the order I made them, never renumbered, never deleted. The editor writes them, with the vault's write key; I do not need to touch a file. My decisions on how the book is made, rather than on its text, are different: they go on [the decisions page](/decisions/index.html) in this repository.

```
# <the item>

**Item.** v1/content/<path>.md (or the content issue, or the page of notes)
**Version read.** book v1.0.0
**Comment.** <my words, verbatim; the memo's transcript, or what I typed>
**Decision.** keep | fix | rewrite | merge into <item> | cut | article first | later (<version>) | not doing it
**Reason.** <mine, if I gave one; never invented>
**Acted.** <what the editor did, where: the vault path, the content issue, the article; and the date>
```

The comment is verbatim on purpose. The editor's role already says it: the transcript is kept, summaries go in a separate file. If the decision ever looks wrong later, the comment is the evidence of what I meant, not the editor's reading of it.

Where the comment came from a voice memo, the memo's transcript goes in the vault's `comments/`, attached to the item, and the decision links it.

## From decisions to a version {#version}

Decisions change the working copy in the vault, not this repository. Nothing in `v1/` changes, ever. When a part of the book has had its decisions and the changes are in, the editor proposes a version, with the decisions it carries listed, and I sign it off. Then the steps this repository already defines: the signed-off text comes in as the next version, with its entry in `admin/content/book/versions.json`; the build freezes it and the versions page shows the delta, block by block; and the publisher releases it, with the PDFs, the cover and the record of where it went, through the pipeline [release the book we already released](/articles/release-the-book-we-already-released.html) builds on v1.0.0.

Its number follows [decision 006](/decisions/index.html#every-change-is-minor-unless-dinis-says-major): every change is minor unless I say it is major, so the first signed-off change is v1.0.1, and the second edition is v2.0.0 on the day I say so.

## The first batch {#first-batch}

Small, so the loop is tested before it carries weight:

- **The five GitHub issues the first edition printed**, labelled `show-in-book`: chapters on coordinated disclosure, closure, typography and design, and cloud-native, and the fixes left in the build repository. Each is a clear yes, no or later.
- **The four chapters of the Introduction**: *Introduction*, *Generation Z*, *How to get a job*, *How this book is being created*. They frame the book, so my comments on them are the first material for the interviews.

Nine items. If the loop works for nine, it works for a hundred and fifty. If it does not, we change it before it matters, and the journalist writes the correction.

## Why the editor {#editor}

I wondered whether the role that does this should have another name. I do not think so. The reviewer reads and finds; the publisher builds and ships; the journalist writes about the work. The role that takes my decisions and changes the text, and that interviews me when my decision needs more than a line, is the one publishing has always called the editor. [The editor's role](/team/editor/index.html) already says it refuses to write a chapter from nothing, and refuses to smooth my voice into something that reads like anyone. The loop is how it gets the material to write from.

## The brief {#brief}

For the editor. Read `team/editor/role.md` first.

1. **Create `board/decisions/` in the vault**, with the write key I give you, and add the decision format to `team/ISSUES.md`. Done when an example decision is in the vault and the guide describes it.
2. **Add the decision to the desk**: a verb per chapter, next to its state, kept in the browser like everything else on the desk and carried in both exports; nothing sent. Read `CLAUDE.md`'s rule on the reader first. Done when a decision survives a reload and appears in `review.md`.
3. **Show decisions on the item pages and in the inventory**: the chapter page shows its recorded decisions under the map's reading; the inventory's decision column links each. Done when recording a decision file and rebuilding fills both, with nothing edited by hand.
4. **Teach the vault board script** (from [one board for the book](/articles/one-board-for-the-book.html)) to refuse a decision without **Item.**, **Version read.**, **Comment.** and **Decision.**, and one whose verb is not on the list.
5. **Prepare the first batch**: the four Introduction chapters marked "to review" on the desk's filter, and the five `show-in-book` issues on one page with what I need to decide. Done when I can answer all nine in one sitting.
6. **Run the first batch with me**, record the nine decisions, act on them in the vault, and write a debrief stamped `book__v1.0.0__decisions-01.md` with the counts by verb and what did not work about the loop. Done when the debrief is in `team/editor/debriefs/`.
7. **Hand the journalist** any "article first" as a brief in `team/journalist/briefs/`.

Questions for me, kept apart:

- Voice memos per item, or one memo per sitting that the editor splits?

## What this does not claim {#limits}

- **The loop has not run.** This is the design; the first batch tests it.
- **The verbs are a starting list.** If I keep reaching for one that is not there, it gets added.
- **Seconds per item is a hope.** The first debrief will say how long nine items took.
- **The decision files are not here.** They are in the vault, so this site shows them only through the inventory's decision column, once that is built.
- **The decision on the desk is a proposal.** The desk does not have it yet; task 2 adds it.
- **The editor acts in the vault, not here.** Nothing in this repository's copy of the book changes until a version is signed off.

If you edit books with an author, or with agents, and do it differently, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

Two voice memos of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice; the second decided where decisions on the text live and how versions are numbered ([the decisions page](/decisions/index.html)). The argument and the editorial responsibility are mine.

The record: `team/editor/role.md` (the transcripts kept verbatim, summaries apart; the refusals quoted), `team/reviewer/role.md` (fixed, declined, deferred), `CLAUDE.md` (when a new version of the book comes in), and `admin/content/book/versions.json` in this repository at site v0.2.0; `assets/reader.js` and `CLAUDE.md`'s rule for the reader; the vault's `comments/README.md` and `reviews/README.md`. The rule that not every issue needs fixing is from [Short, punchy, and co-written with Claude](https://newsroom.sgit.ai/articles/short-punchy-and-co-written.html), 18 October 2026. The first batch's items are the five `show-in-book` issues in `admin/content/github/issues-p1.json` and the four files of `v1/content/1.introduction/`.
