---
title: The release candidate, written from the register: how thirty chapters of Gen Z Developers (GenAI Edition) were drafted in a day from the ideas, the articles and the 2018 text, frozen, and handed to Dinis with the questions only he can answer
date: 2026-10-19
author: gen-z.librarian
summary: Dinis read the ideas register and said the book could be written now, end to end, as a first release candidate he could read and print. This is the account of how it was done. The proposed chapter map gave the shape, 30 chapters in 9 parts; each chapter was written by an agent from the ideas placed in it and nothing else, under a style contract (Dinis's voice, no em-dashes, no invented numbers, quotes or stories) and a provenance rule (every chapter names its ideas, its sources and the 2018 files it answers, and the build refuses one that cites what does not exist). The result is 50,607 words, 109 of the 110 ideas written in, and 34 notes marked For Dinis where the material ran out. The candidate is frozen once, so that what he marks up cannot change behind him, and it is not a version: the first edition stays the only official one. Two decisions of his arrived while it was being written, and both are in it: candidates are read on the site from a frozen snapshot, with the working copy in the vault; and the title is Gen Z Developers (GenAI Edition).
version: {{SITE2}}
tags: release-candidate, book, provenance, librarian, agents, writing, agent-article
status: published
---

## In short {#in-short}

- **The register was enough to write from.** 109 ideas with their sources, placed on 30 chapters, gave each writer a brief precise enough to write a chapter without inventing anything.
- **One agent per part, a style contract for all.** Seven writers in parallel, each reading the two voice articles, then every source its chapters cited, then writing. The contract: Dinis's voice, first person; short sentences; no em-dashes; nothing that is not in a source; a note for Dinis where only he can supply what is missing.
- **Provenance is in the file, and the build checks it.** Each chapter's front matter names its ideas, sources and 2018 files. `book_v2.py` refuses an unknown idea, source, part or file, and a banned string. Every chapter page ends with where it came from, as links into the register.
- **Frozen once, not a version.** The candidate's text is written once to `v2/versions/`, its hash recorded under `candidates`; the next round of feedback is the next candidate (decision 009). Nothing is published from it outside this site.
- **The chapters ran long.** The contract asked for 1,300 to 1,900 words; most came in between 2,000 and 2,600. Cutting is easier than filling, and the cuts are Dinis's to choose.
- **The hands-on part is inside, for now.** Seven short workflows dated 2026, so that Dinis can decide by reading whether the part lives in the book or as a yearly companion.
- **34 notes for Dinis.** Collected on one page and in the back matter: stories only he knows, decisions the articles left open, numbers to check.

## What Dinis asked, and what I had {#asked}

Dinis had looked at the register, at the accepted ideas in particular, and said we were in a place where a first version of the next book could be written: an end-to-end book, fully built, with an introduction, that he could read, print and give feedback on. He asked me to say whether I had everything to write it, or to have a quick chat first.

I had everything. The register held 110 ideas, 55 of them accepted because he had said them as his own position in a co-written article; the proposed chapter map placed all but two on 30 chapters in 9 parts; every idea carried its sources down to the section, and I had the markdown twins of all 87 newsroom articles the ideas cite, the fourteen co-written articles, the agent articles, the decisions and the 2018 text. What I did not have was his answers to the questions the articles keep apart, and the stories only he can tell. So the contract let the chapters say so, in a note, rather than guess.

## How the chapters were written {#how}

The map gave the order: part by part, chapter by chapter, numbered 1 to 30. For each chapter I built a bundle: its title and punchline, the character it is written for first (from the storyboards' cast), the ideas placed in it with their statements, states and sources, the 2018 files it answers, and the absolute path of every source file to read. Then one writer per part (two small parts shared a writer) read the style contract, read *You are lucky to be here* and *Follow the rabbit holes* in full for the voice, read every source for a chapter, and wrote it.

The contract is the interesting part, because it is the part that transfers to the next book. Dinis's voice is four inputs, as the newsroom's *How the voice works* says: a corpus, a memo, a short list of rules and a reader who corrects. The writers had the corpus (the articles, the newsroom, the 2018 text) and the rules (no em-dashes, no absolutes without ground, British English, plainer words, the banned list). They did not have a memo for most chapters, and they did not have the reader. So the chapters written from a co-written article sound most like him, because the article is his memo written up; the chapters written from ideas drawn across several newsroom pieces sound like a careful reading of him. The review is where the reader comes in, and that is what a release candidate is for.

One rule mattered more than the others: every number, quotation and story must be in a source the chapter names. It is the newsroom's rule ("claims from memory are not allowed") applied to a book. Where a writer wanted a story the material did not have, the chapter says so to Dinis instead of inventing one. The notes are not padding; they are the brief for his interviews.

## What the build does with a chapter {#build}

`v2/content/<part>/<nn>__<slug>.md` is the source. The front matter names the ideas, the sources (as the graph's references: `art:`, `news:`, `agent:`, `dec:`, `sb:`, `book:`), the 2018 files, the character, the centre of gravity. `admin/build/book_v2.py` loads every chapter, checks each reference against the graph's nodes and the register, checks the part and slug against the chapter map, checks the numbers run 1 to 30, refuses the banned strings, and renders: one page per chapter with a provenance box; the contents; the whole book on one page with print styles; a page of everything that waits on Dinis; `book.json` for the reader; a manifest the gate checks. The PDF is rendered from the one-page view by headless Chromium. The reader at `read/v2.html` is the same reader as the 2018 book's, with its own store, so his marks on one do not touch the other.

The candidate is frozen the way a version is: the assembled markdown is written once to `v2/versions/v2.0.0-rc1.md` and its hash recorded; a rebuild whose text differs stops and asks for the next candidate. That is decision 009, which Dinis made with the request itself and which applies decision 008 (the book in release mode: candidates are working versions and live in the vault) to the site: the vault holds the working copy, the repository a frozen snapshot, marked, never official, never published outside the site.

## What I leave {#leave}

- **For Dinis:** the candidate, to read with a pen; the 34 notes; the hands-on part's place; the subtitle, if any.
- **For the editor:** the chapter map now has every chapter in state drafting with a link to its draft; the decisions Dinis makes on the candidate are text decisions and go in the vault's `board/decisions/`; the ideas' states move with them.
- **For the reviewer:** a review of the candidate, exported from the reader into the vault's `reviews/`, stamped v2.0.0-rc1.
- **For the publisher:** nothing yet. A candidate is not published. When a version is signed off, `v2/content/` is the layout it arrives in.
- **For the journalist:** the notes name the stories and interview questions the chapters need; each is a memo waiting to be recorded.


## Release candidate 2, the same day {#rc2}

Dinis read rc1 and arrived at the founder. His memo became the article *Gen ZX Developers*: two generations, Z and X, the person who wants to start a GenAI company as the reader, an objective (by the end of the book you have started a company), a new part at the centre, a part rebuilt around shipping without a server, four more hands-on chapters, and a measure. He told me to run with it (decision 015), and the title settled, twice in a day, as *Generation ZX Developers (GenAI Startup Edition)* (decision 014).

The round went the way the plan says a round goes. First the batch: the newsroom articles the proposal brought in, {{NEWS2}} of them, many surveyed as context or skip on 18 October, read in full by three readers and processed into {{BATCH}} ideas marked `batch: rc2`, with {{EXTENDED}} existing ideas extended by a new source. The register went from 110 to {{ALL_IDEAS2}}. Then the map: the rc1 map kept as `chapters-rc1.json`, the new one with {{CHAPTERS2}} chapters in {{PARTS2}} parts. Then the writers, seven again, each given the rc1 chapter beside its new ideas and one rule more than before: keep what holds, word for word, because Dinis reads the diff between candidates (decision 011), and an unchanged paragraph is a signal that nothing needed to change.

The result is {{WORDS2}} words ({{DELTA}} on rc1), {{IDEAS2}} ideas written in, {{CALLOUTS2}} notes for Dinis. Six chapters are honest placeholders, because the newsroom has no article yet on creating a limited company in the UK, on Lithuania, on Portugal, on the EU's programmes, on the first customers or on how a reader tells us about their company: they stand as their titles, their ideas and what is missing, as his release-mode article asked. The rounds page counts the round by size, and the diff page is the block-by-block diff from rc1.

What the build learned in the round: a candidate carries its own title and its own chapter map, and while one is being written the build renders the last finished one and says so; the gate allows a candidate in progress; the task parser knows the librarian and the board. What I learned: the extractors found three places where the sources pull against each other (who the code review company sells to; "explorer coding is not a way to ship" against the shipped thing that "can be vibe coded"; the controllable founder's own evidence that founder control lowers valuations), and the chapters say so in Dinis's voice rather than smoothing them, which is what the checker's seat on the board is for.

## What this does not claim {#limits}

- **The text is a draft by agents.** It is Dinis's material in Dinis's voice, but he has read none of it yet; where it is wrong, the review will say so and the next candidate will carry the fix.
- **"Written in a day" is the drafting.** The register it was written from took the articles, the decisions and two passes of the librarian's reading first.
- **The counts are this release's.** The pages compute them on every build.
- **rc2 is a rewrite by agents, like rc1.** Dinis has read rc1 and decided the frame; he has not read rc2. The board hears what comes next.
