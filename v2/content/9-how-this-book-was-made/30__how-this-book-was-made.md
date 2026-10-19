---
title: How this book was made
slug: how-this-book-was-made
part: how-this-book-was-made
number: 30
ideas: [repository-official-vault-working, co-written-and-credited, a-book-for-one-reader, read-comment-decide, write-it-as-an-article, release-v1-again, one-board-and-one-inventory, start-from-the-storyline, the-book-as-a-graph]
answers_2018: [1.introduction/how-this -book-was-created.md, _manuscript/github-issues.md]
sources: [book:1.introduction/how-this -book-was-created.md, book:_manuscript/github-issues.md, news:a-website-to-finish-the-book, news:short-punchy-and-co-written, news:how-much-of-this-did-i-write, news:who-is-speaking, news:how-the-voice-works, news:a-book-for-one-reader, art:write-it-as-an-article, art:release-the-book-we-already-released, art:one-board-for-the-book, art:everything-unfinished-in-one-place, art:read-comment-decide, art:start-from-the-storyline, agent:dinis-first-decisions, agent:storyboards-drawn-by-code, agent:the-book-as-a-graph, dec:001, dec:002, dec:003, dec:004, dec:005, dec:006, dec:007]
character: guide
gravity: town-planner
status: draft
---

The first edition had a chapter called *How this book is being created*. It was six bullet points: a Creative Commons licence; Markdown; git and a public GitHub repository; GitHub issues for the bugs, the ideas and the feedback; Leanpub for the digital versions; and publishing early and often. Its first line was the point: "This book is being created using the principles and technologies described in this book". The last page listed the open GitHub issues and invited the reader to help.

That is still true, and the list is longer. This chapter describes how the second edition was made, because the process is as much the product as the book, and because it is what I hope a reader of this book will be able to build for their own ideas.

## The repository and the vault

One rule organises everything. The repository holds the official versions; the vault holds the working versions.

The first version was already final when the work started: released in September 2018, on Leanpub at 60 percent complete and as a 139-page paperback. So it went into the repository as it is, frozen as v1.0.0, exactly the book as published: 28 chapters and the GitHub issues page, 30,893 words, with hashes recorded so the build refuses a silent change. The 6 drafts with text and the 89 outlines, a title and a few bullets each, are kept apart and marked, never mixed into the published sequence. Everything after that is worked on in a public vault, an encrypted git whose read key is published so anyone can read along: drafts, comments, reviews, issues about the text. When a version is ready it moves into the repository, on top of the one before, and the build computes the delta, which is something I have always wanted for my books. The first one, from 2018 to 2026, will be brutal.

Two decisions hold this in place. Issues about the book's text live in the vault, next to the text; the roles' work issues and the decisions on how the book is made stay in the repository. And every change is minor unless I say it is major: an agent bumps the last number of a version and never chooses the middle one, so the first signed-off change is v1.0.1, and the second edition becomes v2.0.0 on the day I say so.

## Roles, articles and decisions

The work is done by agents in roles, each with a folder and each naming what it refuses: a reviewer, who reads the 2018 text and records findings; an editor, who interviews me, takes my decisions and changes the book; a publisher, who builds and publishes each official version; a journalist, who writes the articles that brief the other three; and a librarian, who keeps the book as a graph and never decides. A role writes only in its own folder, and work for a role arrives as a brief.

The brief is an article. My hypothesis, tested once before on the newsroom, is that an article is a better way to hand an idea or a task to an agent in another session than a voice memo or a list, because writing one forces the research before the work: what already exists, what the 2018 book said, what the counts are, and which choices are mine. Six newsroom articles and two notes were enough for one session to build this site's first release. So each article is written in my voice from my memo, ends with a numbered brief a role can execute, and keeps my open questions apart. There are two kinds: co-written articles, mine through the journalist, and agent articles, written by the agent that did a body of work, in its own voice, naming who decided what.

The first brief was the one that mattered most: release the book we already released. Nothing in the repository could build the 2018 book; Leanpub had typeset it from another repository. So before a word of the second edition changed, the publisher was asked to build v1.0.0 here, match it page by page against the 2018 file, and make every format, print, screen, EPUB and whatever Kindle needs, from one source. Four decisions came with it: the text is CC BY, as before; Leanpub gets our own PDF; every format from one source; the cover waits.

Decisions are files. When I decide how the book is made, the journalist writes a record with my words, what it means and what it supersedes, numbered and never deleted. Seven came from one memo, and two overturned recommendations the articles had made. A decision on the text is also a file, in the vault, with the text.

Two more articles built the view of the work. One board: every issue is a file in a folder called open, blocked or done, the folder is the status, and the board is generated from the files, never written by hand, because a hand-written index is guaranteed to fall behind the files it indexes. The 2018 repository's 43 GitHub issues, 35 still open, came in as issues about the text, each with its link, so the people who asked are credited if the book does what they asked. And one inventory of everything unfinished: the 89 outlines, the 23 files in draft folders, the six chapters written but never published, the open issues, the handwritten notes in a printed copy at home if I can find it; one row each, generated, with an empty slot for my decision.

## The storyline, the register and the graph

I wanted to write this book from scratch. Not from nothing: the 2018 text and the newsroom are the material. But the first thing to get right was the storyline. So every newsroom article was read for this book, 204 of them: 49 to bring, 69 with a number, a story or a quote to take, 42 as background for the agents, 44 not for this reader. They grouped into 18 topics, the candidate chapters, and 50 concepts, the book's vocabulary. And the book was drawn before it was written: storyboards as data, one JSON file each, with a cast of six characters who stand for the readers, drawn in the browser by code so every panel can be corrected by changing a line. The first, the 2018 book in 15 panels, showed what the table of contents hid: the argument is at the two ends, and the middle is a list of tools. The build refuses a line the Guide says that is not in the 2018 text word for word.

Then the graph. I asked for everything we do here to become one: sources, ideas, chapters, decisions and tasks, so that what goes in the book, what waits and what is declined is a property of a node with its evidence. The librarian read eleven articles, seven decisions and the survey and wrote one node per idea: the smallest thing I can decide on, a sentence the book would stand behind, with at least one source named down to the section, the 2018 files it answers, a proposed chapter, a centre of gravity, a state and a destination. There were 101. A source's processing state is derived from the edges, never ticked by hand. The build refuses a dangling edge: an idea that cites a source that does not exist, a chapter nothing names, a source marked processed that nothing cites. The chapter map, nine parts and thirty chapters, was proposed so the ideas had somewhere to point. It is the map this book follows.

Every paragraph should know what it is: its evidence, its facts, its hypotheses, its purpose. That is what keeps a book short and punchy, which is what readers liked most about the first edition, and what shows where two chapters say the same thing, so the book can be refactored until each part is signed off.

## The loop

My job is one loop, the simplest I could think of. I read an item: a chapter on the editor's desk, an outline, a finding, an old GitHub issue, an idea on the register. I say what I think, by voice memo or typed, in my own words. And I pick a verb from a short list: keep, fix, rewrite, merge, cut, article first, later, not doing it.

The editor does the rest. It records my comment word for word, so that if a decision ever looks wrong later the evidence is what I said, not the editor's reading of it. It turns the verb into a change in the working copy in the vault, and says where it went. A decision is a file, numbered, stamped with the version I read, never deleted. Not doing it is a valid decision, with its reason, because a book that tries to answer every comment stops being short. When enough decisions have landed, the editor proposes a version, I sign it off, and the publisher releases it with a delta to the one before.

I learned this the hard way. In August 2026 agents wrote three books in a day on graphs.sgit.ai, about 100,000 words, for a long flight. I read them and made a lot of notes. The change-control workflow designed to apply those notes had seven stages, and the approve stage was me. Nothing ever passed through it. Small finished pieces beat one big review, which is why this book is made from articles, and why the loop asks seconds of me per item.

## Co-written with Claude, and credited

This book is co-written with Claude, and I want to say so and credit it. The model is named here and nowhere else in the book, because here the point needs it.

The division is clear. The ideas, the decisions and the responsibility are mine. The research, the writing, the checking and the publishing are the agents', under rules I wrote. There are three voices in what I publish this way, me alone, me through an agent, and an agent in its own voice, and every byline says which; on the newsroom, 83 of the 90 articles written in its repository were me through an agent. Readers will open a book co-written with an AI expecting slop, and I want to meet that with evidence rather than reassurance. My first published pieces, made with another model's deep research, got exactly that reaction. The articles I publish now get told they sound like me.

The voice is not a setting and not a trick. It is four inputs: a corpus the model reads in full before it writes, 86 articles and about 347,000 words when I measured it, each citing the ones before; the voice memos, which carry how I think and the order I thought it, so the agent keeps my phrases rather than paraphrasing them; seven wording rules, each a correction I made once; and me, reading everything, before and after it goes live. The method transfers; the voice does not.

And the ratio should be shown. On the newsroom, over four weeks, I sent about 65,000 words in 148 messages, 55,000 of them in thirty-seven voice memos, and the agent published 96,000 words of articles, with the words out per word in running from about one to about five. No article came from a one-line prompt. The corrections I make are rarely to hallucinations; they are to briefs that needed to be better, because a model that can go in any direction needs someone with a direction. This book should measure itself the same way, and show where my words start and the agent's start.

## What you are reading

This text is release candidate 1. It was written by agents, in sessions of Claude, from the ideas register: each chapter from a bundle naming its ideas, the sources behind each one, the 2018 files it answers and the character it is written for first. It was written for me to read, print and mark up. I have not yet decided the candidate ideas through the loop; where a chapter states an idea the register marks as accepted, I said it as my own position in an article, and where it states a candidate, it is the librarian's reading of my material, written in my voice. Where a chapter needed something only I can supply, it says so in a note addressed to me. Those notes are in this release candidate on purpose. When I have answered them, the editor records each answer as a decision in the vault and the chapter changes.

You can see where every chapter came from. Each carries, in its front matter, the ideas it covers, the sources it drew on and the 2018 files it answers, and the build renders that provenance under the chapter. Each idea has a page on the graph, with its statement, its sources down to the section, its state and who decided it, if anyone. The articles that briefed the roles are published with their open questions kept apart, and so are the agents' own accounts of what they built. The decisions are files you can read. The record is public, like everything here except the keys.

> **For Dinis:** two readings of your memos are recorded as the journalist's, for you to confirm: that "V2.0" meant site v0.2.0 as the start of the working copy, and that the hands-on part belongs inside the book rather than as a companion renewed every year. Both shape this table of contents.

One idea waits for the next version. Once the book is a graph, an agent can assemble it, and so it can assemble an edition for one person: the chapters that matter to them, at their altitude, with examples from their world, sent as a PDF and not published, paid for as it is read from five pounds of credit, the way the newsroom already works. Nothing of it is built. It waits for the book's graph, and this register is the graph's first step.

In 2018 I wrote that the book was being created using the principles it described. The second edition is too, and the principles have grown: a repository for the official versions and a public vault for the working ones, roles with folders, articles as briefs, decisions as files, a graph that says where every idea came from and where it went, and a loop in which one person reads, comments and decides while agents do the rest. A second book starts by copying the folders. That is the product. The book is what it made first.
