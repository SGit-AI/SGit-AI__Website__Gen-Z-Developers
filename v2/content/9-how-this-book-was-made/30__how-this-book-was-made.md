---
title: How this book was made
slug: how-this-book-was-made
part: how-this-book-was-made
number: 30
ideas: [the-book-in-release-mode, the-adversarial-review-board, every-verdict-is-a-precedent, a-candidate-is-read-as-a-frozen-snapshot, gen-ai-edition-name, repository-official-vault-working, co-written-and-credited, a-book-for-one-reader, read-comment-decide, write-it-as-an-article, release-v1-again, one-board-and-one-inventory, start-from-the-storyline, the-book-as-a-graph]
answers_2018: [1.introduction/how-this -book-was-created.md, _manuscript/github-issues.md]
sources: [book:1.introduction/how-this -book-was-created.md, book:_manuscript/github-issues.md, news:a-website-to-finish-the-book, news:short-punchy-and-co-written, news:how-much-of-this-did-i-write, news:who-is-speaking, news:how-the-voice-works, news:a-book-for-one-reader, art:write-it-as-an-article, art:release-the-book-we-already-released, art:one-board-for-the-book, art:everything-unfinished-in-one-place, art:read-comment-decide, art:start-from-the-storyline, agent:dinis-first-decisions, agent:storyboards-drawn-by-code, agent:the-book-as-a-graph, dec:001, dec:002, dec:003, dec:004, dec:005, dec:006, dec:007, art:the-book-in-release-mode, dec:008, dec:009, dec:010, art:generative-ai-not-ai]
character: guide
gravity: town-planner
status: draft
---

The first edition had a chapter called *How this book is being created*. It was six bullet points: a Creative Commons licence; Markdown; git and a public GitHub repository; GitHub issues for the bugs, the ideas and the feedback; Leanpub for the digital versions; and publishing early and often. Its first line was the point: "This book is being created using the principles and technologies described in this book". The last page listed the open GitHub issues and invited the reader to help.

That is still true, and the list is longer. This chapter describes how the second edition was made, because the process is as much the product as the book, and because it is what I hope a reader of this book will build for their own ideas.

## The repository and the vault

One rule organises everything. The repository holds the official versions; the vault holds the working versions.

The first version was already final: released in September 2018, on Leanpub at 60 percent complete and as a 139-page paperback. So it went into the repository as it is, frozen as v1.0.0: 28 chapters and the GitHub issues page, 30,893 words, with hashes recorded so the build refuses a silent change. The 6 drafts with text and the 89 outlines are kept apart and marked, never mixed into the published sequence. Everything after that is worked on in a public vault, whose read key is published so anyone can read along. When a version is ready it moves into the repository, on top of the one before, and the build computes the delta.

Two decisions hold it. Issues about the book's text live in the vault, next to the text; the roles' work issues and the decisions on how the book is made stay in the repository. And every change is minor unless I say it is major: an agent bumps the last number of a version, so the first signed-off change is v1.0.1, and the second edition becomes v2.0.0 on the day I say so.

## Roles, articles and decisions

The work is done by agents in roles, each with a folder and each naming what it refuses: a reviewer, who reads the 2018 text and records findings; an editor, who interviews me, takes my decisions and changes the book; a publisher, who builds and publishes each official version; a journalist, who writes the articles that brief the other three; and a librarian, who keeps the book as a graph and never decides.

The brief is an article. My hypothesis is that an article is a better way to hand a task to an agent in another session than a voice memo or a list, because writing one forces the research before the work: what exists, what the 2018 book said, and which choices are mine. Each article is written in my voice from my memo, ends with a numbered brief a role can execute, and keeps my open questions apart. There are two kinds: co-written articles, mine through the journalist, and agent articles, written by the agent that did a body of work, in its own voice, naming who decided what.

The first brief was the one that mattered most: release the book we already released. Before a word of the second edition changed, the publisher was asked to build v1.0.0 here, match it page by page against the 2018 file Leanpub made, and produce every format, print, screen, EPUB and whatever Kindle needs, from one source. Four decisions came with it: the text is CC BY, as before; Leanpub gets our own PDF; every format from one source; the cover waits.

Decisions are files. When I decide how the book is made, the journalist writes a record with my words, what it means and what it supersedes, numbered and never deleted.

Two more articles built the view of the work. One board: every issue is a file in a folder called open, blocked or done, the folder is the status, and the board is generated from the files, never written by hand. The 2018 repository's 43 GitHub issues, 35 still open, came in as issues about the text, each with its link. And one inventory of everything unfinished: the 89 outlines, the six chapters written but never published, the open issues, my handwritten notes; one row each, generated, with an empty slot for my decision.

## The storyline, the graph and the loop

I wanted to write this book from scratch, and the first thing to get right was the storyline, not a chapter. So every newsroom article was read for this book, 204 of them: 49 to bring, 69 with a number, a story or a quote to take, 42 as background for the agents, 44 not for this reader. They grouped into 18 topics, the candidate chapters, and 50 concepts, the book's vocabulary. And the book was drawn before it was written: storyboards as data, with a cast of six characters who stand for the readers, drawn in the browser by code so every panel can be corrected by changing a line.

Then the graph. I asked for everything we do here to become one: sources, ideas, chapters, decisions and tasks. The librarian read eleven articles, seven decisions and the survey and wrote one node per idea: the smallest thing I can decide on, a sentence the book would stand behind, with its sources, the 2018 files it answers and a proposed chapter. There were 101. A source's processing state is derived from the edges, never ticked by hand, and the build refuses a dangling edge: an idea that cites a source that does not exist, a chapter nothing names. The chapter map, nine parts and thirty chapters, was proposed so the ideas had somewhere to point. It is the map this book follows.

Every paragraph should know what it is: its evidence, its facts, its hypotheses, its purpose. That keeps a book short and punchy, which is what readers liked most about the first edition, and it shows where two chapters say the same thing.

My job in all of this is one loop, the simplest I could think of. I read an item: a chapter, an outline, a finding, an idea on the register. I say what I think, in my own words. And I pick a verb from a short list: keep, fix, rewrite, merge, cut, article first, later, not doing it.

The editor does the rest. It records my comment word for word, turns the verb into a change in the working copy in the vault, and says where it went. A decision is a file, numbered, stamped with the version I read, never deleted. Not doing it is a valid decision, with its reason, because a book that tries to answer every comment stops being short. When enough decisions have landed, the editor proposes a version, I sign it off, and the publisher releases it with a delta to the one before.

I learned this the hard way. In August 2026 agents wrote three books in a day on graphs.sgit.ai, about 100,000 words. The change-control workflow designed to apply my notes had seven stages, and the approve stage was me. Nothing ever passed through it. Small finished pieces beat one big review, which is why this book is made from articles.

## Release mode, and the board

The librarian's first list, the register and the proposed map, was enough to write from, so we ran with it: the book in release mode. A release candidate is a whole book, start to finish, that we could publish if we had to and are not yet publishing, because the next round will make it better. Then rounds. Each takes one pile of material and reads it against the current text: the concepts in this site's articles that the candidate does not carry; what the first edition said that this one has lost; the newsroom's articles; and anything I write next. For each thing the answer is one of a few: add it, rewrite it into something already there, merge it, sign the topic off as covered, move it to the next version or another book, or decide not to cover it and say why. Then the next candidate. My expectation is that the rounds change shape: at first we add parts and chapters, then concepts, then sentences, and when a round stops bringing anything big, we have a book.

From this first candidate on, nothing enters without a hearing. Every word, change and idea that wants to come in goes before a review board: an advocate argues for it; a cutter argues against it, always; the readers (the four people the storyboards are drawn for) say whether they would miss it; a checker asks whether it is sourced, true now, and quoted word for word; the editor says where it goes and what it displaces; and I decide. Each seat is a role in its own session, so the one arguing against has not been persuaded by what the one arguing for was shown. The cutter is the seat that matters: the first edition was liked for being short and punchy, and every book grows by things that were each a good idea on their own, so the default answer is no.

Every verdict is written down with its reason, and a general reason becomes a precedent: a rule the board applies next time without a hearing, on a list I can overturn. Tool tutorials go in the hands-on part, not in the argument; a spelling fix comes in without a hearing; a second example of the same point is cut. The first rounds are slow because everything is new; by the third, most cases should be decided by something we already said.

Release candidates are working versions, so they live in the vault, like every text decision and every text issue. To be read and printed, this one was built on the website from a frozen snapshot, marked on every page as a candidate and not a version, with its hash recorded once so that what I mark up cannot change behind me. The next candidate replaces it; nothing is published from it anywhere else.

## Co-written with Claude, and credited

This book is co-written with Claude, and I want to say so and credit it. The model is named here and nowhere else in the book, because here the point needs it.

The division is clear. The ideas, the decisions and the responsibility are mine. The research, the writing, the checking and the publishing are the agents', under rules I wrote. There are three voices in what I publish, me alone, me through an agent, and an agent in its own voice, and every byline says which. Readers will open a book co-written with an AI expecting slop, and I want to meet that with evidence rather than reassurance.

The voice is not a setting and not a trick. It is four inputs: a corpus the model reads in full before it writes, 86 articles and about 347,000 words at the time; the voice memos, which carry how I think and the order I thought it; seven wording rules, each a correction I made once; and me, reading everything, before and after it goes live. The method transfers; the voice does not.

And the ratio should be shown. On the newsroom, over four weeks, I sent about 65,000 words in 148 messages, 55,000 of them in thirty-seven voice memos, and the agent published 96,000 words of articles, with the words out per word in running from about one to about five. The corrections I make are rarely to hallucinations; they are to briefs that needed to be better, because a model that can go in any direction needs someone with a direction.

## What you are reading

This text is release candidate 1 of *Gen Z Developers (GenAI Edition)*: the first edition's name, as the paperback carried it, with the edition in brackets, which I settled on while this draft was being written; the subtitle, if there is one, is a later decision. It was written by agents, in sessions of Claude, from the ideas register: each chapter from a bundle naming its ideas, the sources behind each one and the 2018 files it answers. I have not yet decided the candidate ideas through the loop; where a chapter states an idea the register marks as accepted, I said it as my own position in an article, and where it states a candidate, it is the librarian's reading of my material, written in my voice. Where a chapter needed something only I can supply, it says so in a note addressed to me. Those notes are in this release candidate on purpose.

You can see where every chapter came from. Each carries, in its front matter, the ideas it covers, the sources it drew on and the 2018 files it answers, and the build renders that provenance under the chapter. Each idea has a page on the graph, with its sources down to the section, its state and who decided it, if anyone. The record is public, like everything here except the keys.

> **For Dinis:** two readings of your memos are recorded as the journalist's, for you to confirm: that "V2.0" meant site v0.2.0 as the start of the working copy, and that the hands-on part belongs inside the book rather than as a companion renewed every year. Both shape this table of contents.

One idea waits for the next version. Once the book is a graph, an agent can assemble it, and so it can assemble an edition for one person: the chapters that matter to them, at their altitude, sent as a PDF and not published, paid for as it is read from five pounds of credit. Nothing of it is built; it waits for the book's graph, of which this register is the first step.

The principles have grown since 2018: a repository for the official versions and a public vault for the working ones, roles with folders, articles as briefs, decisions as files, a graph that says where every idea came from and where it went, and a loop in which one person reads, comments and decides while agents do the rest. A second book starts by copying the folders. That is the product. The book is what it made first.
