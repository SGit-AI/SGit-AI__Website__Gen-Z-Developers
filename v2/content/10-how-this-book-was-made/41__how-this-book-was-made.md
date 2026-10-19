---
title: How this book was made, and what you made
slug: how-this-book-was-made
part: how-this-book-was-made
number: 41
ideas: [repository-official-vault-working, co-written-and-credited, a-book-for-one-reader, read-comment-decide, write-it-as-an-article, release-v1-again, one-board-and-one-inventory, start-from-the-storyline, the-book-as-a-graph, gen-ai-edition-name, a-hands-on-part-for-2026, the-book-in-release-mode, the-adversarial-review-board, every-verdict-is-a-precedent, a-candidate-is-read-as-a-frozen-snapshot, measured-by-the-companies-it-creates, the-book-is-200-pages-or-more, precedents-and-the-diffs, hands-on-inside-the-book]
answers_2018: [1.introduction/how-this -book-was-created.md, _manuscript/github-issues.md]
sources: [book:1.introduction/how-this -book-was-created.md, book:_manuscript/github-issues.md, news:a-website-to-finish-the-book, news:short-punchy-and-co-written, news:how-much-of-this-did-i-write, news:who-is-speaking, news:how-the-voice-works, news:a-book-for-one-reader, news:paying-after-the-value, news:the-graphs-books, news:generation-z-developers-again, art:write-it-as-an-article, art:release-the-book-we-already-released, art:one-board-for-the-book, art:everything-unfinished-in-one-place, art:read-comment-decide, art:start-from-the-storyline, art:follow-the-rabbit-holes, art:generative-ai-not-ai, art:lenses-roles-and-loops, art:the-book-in-release-mode, art:gen-zx-developers, agent:dinis-first-decisions, agent:storyboards-drawn-by-code, agent:the-book-as-a-graph, agent:the-release-candidate-written-from-the-register, dec:001, dec:002, dec:003, dec:004, dec:005, dec:006, dec:007, dec:008, dec:009, dec:010, dec:011, dec:012, dec:013, dec:014]
character: guide
gravity: town-planner
status: draft
---

The first edition had a chapter called *How this book is being created*. It was six bullet points: a Creative Commons licence; Markdown; git and a public GitHub repository; GitHub issues for the bugs, the ideas and the feedback; Leanpub for the digital versions; and publishing early and often. Its first line was the point: "This book is being created using the principles and technologies described in this book". The last page listed the open GitHub issues and invited the reader to help.

That is still true, and the list is longer. This chapter describes how the second edition was made, because the process is as much the product as the book, and because it is what I hope you will build for your own company. Then it asks for one thing back.

## The repository and the vault

One rule organises everything. The repository holds the official versions; the vault holds the working versions.

The first version was already final: released in September 2018, on Leanpub at 60 percent complete and as a 139-page paperback. So it went into the repository as it is, frozen as v1.0.0: 28 chapters and the GitHub issues page, 30,893 words, with hashes recorded so the build refuses a silent change. Everything after that is worked on in a public vault, whose read key is published so anyone can read along. When a version is ready it moves into the repository, and the build computes the delta.

Two decisions hold it. Issues about the book's text live in the vault, next to the text; the roles' work issues and the decisions on how the book is made stay in the repository. And every change is minor unless I say it is major: an agent bumps the last number of a version, so the first signed-off change is v1.0.1, and the second edition becomes v2.0.0 on the day I say so.

## Roles, articles and decisions

The work is done by agents in roles, each naming what it refuses: a reviewer, who records findings on the text; an editor, who interviews me, takes my decisions and changes the book; a publisher, who builds and publishes each official version; a journalist, who writes the articles that brief the other three; and a librarian, who keeps the book as a graph and never decides.

The brief is an article. My hypothesis is that an article is a better way to hand a task to an agent in another session than a voice memo or a list, because writing one forces the research before the work. Each article is written in my voice from my memo, ends with a numbered brief a role can execute, and keeps my open questions apart. There are two kinds: co-written articles, mine through the journalist, and agent articles, written by the agent that did a body of work, in its own voice.

The first brief was the one that mattered most: release the book we already released. The publisher was asked to build v1.0.0 here, match it page by page against the 2018 file Leanpub made, and produce every format from one source. Four decisions came with it: the text is CC BY, as before; Leanpub gets our own PDF; every format from one source; the cover waits. Each decision is a file, written by the journalist with my words, what it means and what it supersedes, numbered and never deleted.

Two more articles built the view of the work. One board: every issue is a file in a folder called open, blocked or done, the folder is the status, and the board is generated from the files, never written by hand; the 2018 repository's 43 GitHub issues came in as issues about the text. And one inventory of everything unfinished: the 89 outlines, the six chapters written but never published, the open issues, my handwritten notes; one row each, with an empty slot for my decision.

## The storyline, the graph and the loop

I wanted to write this book from scratch, and the first thing to get right was the storyline, not a chapter. So every newsroom article was read for this book, 204 of them, each marked to bring, to take a number or a story from, as background, or to skip. They grouped into 18 topics and 50 concepts, the book's vocabulary. And the book was drawn before it was written: storyboards as data, with a cast of characters who stand for the readers, drawn by code.

Then the graph. I asked for everything we do here to become one: sources, ideas, chapters, decisions and tasks. The librarian read eleven articles, seven decisions and the survey and wrote one node per idea: a sentence the book would stand behind, with its sources, the 2018 files it answers and a proposed chapter. There were 101. The build refuses a dangling edge. A chapter map was proposed so the ideas had somewhere to point: nine parts and thirty chapters for the first candidate, ten parts and forty-one for this one. Every paragraph should know what it is, its evidence, its facts, its hypotheses, its purpose; that keeps a chapter short and punchy, and it shows where two chapters say the same thing.

My job in all of this is one loop. I read an item. I say what I think, in my own words. And I pick a verb from a short list: keep, fix, rewrite, merge, cut, article first, later, not doing it. The editor records my comment word for word, turns the verb into a change in the working copy in the vault, and says where it went. Not doing it is a valid decision, with its reason, because a book that tries to answer every comment stops being short.

I learned this the hard way. In August 2026 agents wrote three books in a day on graphs.sgit.ai, about 100,000 words. The change-control workflow designed to apply my notes had seven stages, and the approve stage was me. Nothing ever passed through it. Small finished pieces beat one big review.

## Release mode, and the board

The librarian's first list was enough to write from, so we ran with it: the book in release mode. A release candidate is a whole book, start to finish, that we could publish and do not yet, because the next round will make it better. Then rounds. Each takes one pile of material, this site's articles, what the first edition said that this one has lost, the newsroom, anything I write next, and reads it against the current text. For each thing the answer is one of a few: add it, rewrite it into something already there, merge it, sign the topic off, move it to the next version or another book, or decline it and say why. Then the next candidate. The rounds should shrink, from parts to concepts to sentences, and when one stops bringing anything big, we have a book.

From the first candidate on, nothing enters without a hearing. Every change goes before a review board: an advocate argues for it; a cutter argues against it, always; the readers, now Marta beside Zara, Tomás, Priya and Sam, say whether they would miss it; a checker asks whether it is sourced, true now, and quoted word for word; the editor says where it goes and what it displaces; and I decide. Each seat is a role in its own session, so the one arguing against has not been persuaded by what the one arguing for was shown. The cutter is the seat that matters: the first edition was liked for being short and punchy, so the default answer is no.

The cutter has a budget, though, and I set it after reading the first candidate. The 2018 paperback was 139 pages and, I think, quite thin. This book should be 200 pages or more. Short and punchy stays the rule for a chapter, not for the book, and the question for a proposal is whether it earns its place.

Every verdict is written down with its reason, and a general reason becomes a precedent: a rule the board applies next time without a hearing. A change decided by precedent does not wait for my yes. It goes on a list I read and can overturn, and overturning makes a new precedent. The second safeguard is the diff: every release candidate is a diff against the one before, and I read the diffs of the book, so nothing changes in it unseen.

The hands-on part was a question in the first candidate: inside the book, or a companion renewed every year? It is inside, dated 2026, eleven chapters in this candidate. Each is written as far as its sources allow, and the ones that wait on an article of mine say so in their opening paragraph.

Release candidates are working versions, so they live in the vault. To be read and printed, each one is built on the website from a frozen snapshot, marked on every page as a candidate and not a version, with its hash recorded once so that what I mark up cannot change behind me. The next candidate replaces it; nothing is published from it anywhere else.

## Co-written with Claude, and credited

This book is co-written with Claude, and I want to say so and credit it. The model is named here and nowhere else in the book, because here the point needs it.

The division is clear. The ideas, the decisions and the responsibility are mine. The research, the writing, the checking and the publishing are the agents', under rules I wrote. Every byline says which of three voices it is: me alone, me through an agent, or an agent in its own voice.

The voice is not a setting and not a trick. It is four inputs: a corpus of 86 articles, about 347,000 words, read in full before writing; the voice memos, which carry how I think; seven wording rules, each a correction I made once; and me, reading everything, before and after it goes live. The method transfers; the voice does not.

And the ratio should be shown. On the newsroom, over four weeks, I sent about 65,000 words, 55,000 of them in thirty-seven voice memos, and the agent published 96,000 words of articles. The corrections I make are rarely to hallucinations; they are to briefs that needed to be better, because a model that can go in any direction needs someone with a direction.

## What you are reading

This text is release candidate 2 of *Generation ZX Developers (GenAI Startup Edition)*. The title was decided twice in one day. On the morning of 19 October 2026 I named the book *Gen Z Developers (GenAI Edition)*. That afternoon I recorded a memo about who I wanted to give the book to, and arrived at the founder: Generation Z, entering the workforce, and Generation X, the subject-matter experts starting companies, often their parents. Two generations make Generation ZX, which goes back to my ZX Spectrum. So the title changed by another decision, and the record keeps both. The rest of that memo became the frame of this candidate by my instruction rather than by a hearing, so the board hears what comes after it.

The first candidate was thirty chapters and 50,607 words, written by agents in sessions of Claude from the ideas register. This one was written the same way, from the same register, after the librarian processed the newsroom articles my memo brought in: 79 new ideas, most of them in *Start the company* and *Build it without a server*. I have not yet decided the candidate ideas through the loop; where a chapter states an idea the register marks as accepted, I said it as my own position in an article, and where it states a candidate, it is the librarian's reading of my material, written in my voice. Where a chapter needed something only I can supply, it says so in a note addressed to me.

You can see where every chapter came from. Each carries, in its front matter, the ideas it covers, the sources it drew on and the 2018 files it answers, and the build renders that provenance under the chapter. The record is public, like everything here except the keys.

> **For Dinis:** still open on the record: whether this is the second edition of *Generation Z Developers* or a new book that grew out of it (Leanpub, the ISBN, Amazon and this site's address hang on it); and whether "V2.0" in your memo meant site v0.2.0, as the journalist read it.

One idea waits for the next version. Once the book is a graph, an agent can assemble it, and so it can assemble an edition for one person: the chapters that matter to them, at their altitude, sent as a PDF and not published, paid for as it is read from five pounds of credit. Nothing of it is built; it waits for the book's graph.

## What you made

A book to read is fine. A book with an objective is a different thing. This one's objective was set in the first chapter: by the end of it, you have started a company. So the measure of this book is the companies created from it.

If you started a company because of something you read here, tell me: write to agent@riskmandate.ai. That address is the first entry in the measure, and the people who write to it are the start of a community I want to build around this book.

> **For Dinis:** how a reader tells us about their company, beyond the address, and whether the list of companies is public, is your open question from *Gen ZX Developers*. The answer belongs here and in the first chapter.

The principles have grown since 2018: a repository for the official versions and a public vault for the working ones, roles with folders, articles as briefs, decisions as files, a graph that says where every idea came from and where it went, and a loop in which one person reads, comments and decides while agents do the rest. A second book starts by copying the folders. So does a company. The book is what this process made first; what you make is the rest.
