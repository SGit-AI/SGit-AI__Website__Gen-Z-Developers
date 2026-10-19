---
title: Version 2 on Leanpub: why Generation ZX Developers should update the 2018 book in place rather than start a new one, what to change on the page, a price anyone can set to zero, and the listing ready to paste
date: 2026-10-19
author: Dinis Cruz
summary: Generation ZX Developers is, fundamentally, a new book, and Leanpub has a word for that: a new edition, which Leanpub treats as a new, different book that past readers buy again. But the 2018 book has 465 readers on Leanpub, and this is version 2 of it. So I think the right move is to update the existing book: change the title, the subtitle, the address and the description, and publish the new text as a new version, which every one of those readers gets for free, with a release note to the ones who opted in. The old address redirects, because the book has had sales, and the 2018 text stays where it is: frozen on this site, on GitHub and in the paperback. On price, I want what the first edition never quite had: anyone can choose to pay nothing. Today the page asks non-members for at least $7.99 and only members get it free; the fix is two settings. Above zero, a suggested price of $20 says what the book is worth, and Leanpub pays 80% of anything from $7.99 up. The one thing that does not change is the rule that only a signed-off version is published, so the page is ready now and the upload waits for v2.0.0, unless I decide to publish it in progress the way Leanpub was made for. Everything to paste is at the end.
version: v0.2.31
tags: leanpub, publishing, pricing, version-2, listing, gen-z-book, article
status: published
---

## In short {#in-short}

- **It is a new book, and it is version 2 of the old one.** Both are true; Leanpub makes me pick.
- **Update the 2018 book in place.** New title, subtitle, address and description; the new text as a new version.
- **The 465 readers get it for free.** That is what a Leanpub version means, and they are the first audience.
- **The old address redirects.** Because the book has had sales; the 2018 text stays frozen here, on GitHub and in print.
- **Anyone can pay zero.** Today only members get it free and everyone else pays at least $7.99; two settings fix that.
- **Suggest $20.** Leanpub pays 80% of anything from $7.99 up, and the suggested price is what most people see.
- **The page is ready now; the upload waits for v2.0.0.** Unless I decide to publish it in progress.
- **The listing is below, ready to paste.**

## A new book, or version 2? {#version-or-edition}

This is fundamentally a new book: a new title, two generations instead of one, an objective the first one did not have, and most of it written since. Leanpub's help centre has a word for that. "A new "edition" of a book is a new, different book", and "the main reason to create a new "edition" of a book is when the author has essentially written a new book". A new version, on the other hand, is an update, and "when a new version of a Leanpub book is published, it is immediately made available for free" to everyone who bought it.

So by Leanpub's definition this is an edition. But we had 465 readers on Leanpub, and this is version 2 of that book. In this repository it already is: the book's own version stream goes from v1.0.0, the 2018 edition, to v2.0.0, and every chapter names the 2018 files it answers. I think it is worth updating that book, and Leanpub lets me: the title, the subtitle and the address of a published book can all be changed, and the new text goes up as a new version.

What each choice gives:

| | Update the 2018 book (a new version) | A new book (a new edition) |
|---|---|---|
| The 465 readers | Get it free, automatically; a release note reaches the ones who opted in | Must buy it; I can send them a coupon, which Leanpub says to do "very rarely" |
| The page | Keeps its readers, its history and its licence; the old address redirects | Starts at zero readers, on a new address |
| The 2018 book on Leanpub | Replaced by version 2 for new buyers | Stays on sale beside the new one |
| The 2018 text | Frozen on this site at `/v1/`, on GitHub and in the paperback | The same |
| Money | Nothing lost: the book is pay what you want, with zero allowed | A second price to explain |

The only real cost of updating is that the 2018 book stops being on sale on Leanpub as itself. I can live with that, because it is not lost: it is CC BY, it is frozen as v1.0.0 on this site, its source is on GitHub, and the paperback is still on Amazon. And the gain is the one this book is for. Its measure is the companies created from it, so reach matters more than a fresh page, and 465 people who once chose this book are the best first readers it could have.

The address should change with the title. Leanpub says that for a published book that has had at least one sale, the old address redirects to the new one, and current readers are not affected. `leanpub.com/generation-zx` is free as I write.

## When {#when}

The rule of this repository does not change: only a signed-off version is published, and a release candidate is not a version. So the page is ready now, and the upload of the new text, with the new title, waits for v2.0.0. Changing the title of a published book on Leanpub also needs a new version to be published, so the two happen together.

There is another way, and it is the one Leanpub was built for: publish while writing, and say how complete it is. The 2018 book has said "60% complete" since 8 October 2018. Publishing a release candidate on Leanpub, marked in progress, would get the book to the 465 readers in weeks instead of months, and their feedback into the rounds. That would change the publisher's rule, so it is my decision, and I keep it apart below.

## The price {#price}

On Leanpub I still want the mode where you can choose zero: you can choose not to pay anything. The 2018 page does not quite do that today. Its settings, as Leanpub shows them: free purchases are allowed, but only with a Reader Membership; everyone else pays at least $7.99; the suggested price is $10, and the most anyone can pay is $20. So a reader without a membership cannot pick zero.

The fix is on the book's pricing page:

- **Allow Free Purchases:** on.
- **Free purchases require a Reader, Standard or Pro membership:** off. This is the one that matters.
- **Minimum price:** free, $0.
- **Suggested price:** $20.
- **Maximum price:** $100, so a company or a reader who wants to pay more can.

Why $20 suggested. Leanpub pays the author 80% of anything from $7.99 up, and 80% minus 50 cents between $0.99 and $7.98, as its help centre says. The suggested price is what the slider starts at, so it is what most people who pay will pay; at $20 the book earns $16 a copy, and at $10 it earns $8. The book is now well over 200 pages at the paperback's size, and its promise is a company; $10 undersells that. And zero stays for anyone who wants it, which is the point: Leanpub's own advice is that free is usually not the right idea for an author, and for most authors it is not, but this book is measured by the companies it creates, not by what it earns, and it is CC BY anyway. Leanpub also notes that people often pay even when they could pay nothing.

## The listing, ready to paste {#listing}

Everything below is for the book's settings on Leanpub, in the order the settings pages ask for it. Change them together, with the upload of v2.0.0.

### Title {#title}

```
Generation ZX Developers (GenAI Startup Edition)
```

### Subtitle {#subtitle}

```
For Generation Z and Generation X: start a GenAI company by the end of the book
```

### Address {#url}

```
leanpub.com/generation-zx
```

The old address, `leanpub.com/generation-z`, redirects.

### Short description {#short}

For the line under the title and for links shared on social media:

```
Two generations, one objective: by the end of this book, you have started a GenAI company. Ship it, see if they miss it, and build it without a server.
```

### About the book {#about}

```
In 2018 I wrote Generation Z Developers for one reader: the generation entering the job market. Eight years later that generation is not only looking for jobs. They are starting companies. And so is mine.

This is version 2, and it is written for two generations. Generation Z, entering the workforce and becoming the new entrepreneurs. And Generation X: the subject-matter experts, twenty years inside a problem, who can now build the first version of the answer themselves, with agents, instead of explaining it to a team they could never afford. Often they are in the same family. Put the two letters together and you get Generation ZX, which takes me back to where I started: the ZX Spectrum.

The book has one objective: that by the end of it, you have started a company.

So it covers what you need for that, for real:

- What generative AI is, and how a model becomes a role and a role becomes an agent
- Why everyone who can brief an agent is now a developer, and explorer coding instead of vibe coding
- Your first workspace with agents, and how to work with them without losing control
- Direction and judgement: the skills that stay scarce
- Start the company: be a founder, ship it and see if they miss it, price it then give it away, sell, and fund it or do not
- Build it without a server: no servers of yours, no database of yours, privacy by design, and control of the agents your company runs on
- Hands on, 2026: dated, practical workflows, from an agentic workflow on day one to your first price, your first ten customers and a serverless product in a weekend

It is co-written with Claude, and every claim in it can be traced to a source: the book is built in public at gen-z-developers.sgit.ai, where every chapter shows the ideas and sources it was written from.

I measure this book by how many companies are created from it. If you start one, tell me.

The first edition is still available, free, at gen-z-developers.sgit.ai/v1/book/ and on GitHub. Everything is Creative Commons (CC BY 4.0). Pay what you want, including nothing.
```

### Table of contents {#toc}

Leanpub builds the contents from the uploaded files. For the page, the parts:

```
Before you start
The frame
Getting the job, or making it
Working with agents
Direction and judgement
Start the company
Build it without a server
The long game
Hands on, 2026
How this book was made, and what you made
```

### Categories {#categories}

Keep *Computers and Programming*. Replace *Engineering* and *Education* with the closest Leanpub has to **Startups** and **Artificial Intelligence**; the publisher checks the list.

### The rest of the settings {#settings}

| Setting | Value |
|---|---|
| Language | English |
| Licence | Creative Commons Attribution 4.0 International (unchanged) |
| Suggested hashtag | `GenZX_Dev` (was `GenZ_Dev`) |
| Completeness | Honest: 100% only for v2.0.0; if published in progress, the share of chapters written |
| Cover | 1,800 by 2,700 pixels for 6 by 9 inches, as Leanpub's help says; the cover waits ([decision 004](/decisions/index.html#the-cover-waits)), so the 2018 one stays until then |
| Files | Uploaded, not generated by Leanpub: a screen PDF at 6 by 9 inches and an EPUB, from the same source as every other format ([decision 003](/decisions/index.html#every-format-from-one-source)) |
| About the author | Unchanged: it is set on my Leanpub profile and shared by all my books |
| Links | The book's site, gen-z-developers.sgit.ai; the source on GitHub |

### The release note, for the 465 {#release-note}

Leanpub sends it only to readers who opted in to messages, with the new version:

```
Subject: Generation Z Developers is now Generation ZX Developers, version 2, free for you

Hi,

In 2018 you picked up Generation Z Developers. Thank you. Eight years later, here is version 2, and as with every Leanpub update, it is free for you: it is already in your library.

It has a new title, Generation ZX Developers (GenAI Startup Edition), because it is now for two generations, Generation Z and Generation X, and because it has an objective the first one did not have: that by the end of it, you have started a company.

Most of it is new: what generative AI is, working with agents, starting the company, building it without a server, and a hands-on part for 2026. The 2018 text is still free at gen-z-developers.sgit.ai/v1/book/.

I measure this book by the companies created from it. If you start one, or you are already building one, I would like to hear about it.

Dinis
```

## The brief {#brief}

For the publisher. Read `team/publisher/role.md`, decisions 002, 003, 004 and 014, and this article first.

1. **Build the Leanpub files from v2.0.0 when it is signed off**: a screen PDF at 6 by 9 inches and an EPUB, from the one source, and the sample Leanpub offers. Done when both open cleanly and the page count is recorded.
2. **Check the settings against Leanpub as it is on the day**: the categories that exist, that the old address redirects after the change, and that a reader with no membership can choose zero. Done when a test at $0 works, from an account with no membership.
3. **Record the listing** as published: what was pasted, the date, the version. Done when it is in your `debriefs/`.

Questions for me, kept apart:

- Version 2 of the 2018 book, updated in place, rather than a new edition? (My recommendation: yes.)
- Publish when v2.0.0 is signed off, or now, in progress, as the 2018 book was?
- A suggested price of $20, minimum $0, maximum $100?
- The new address, `generation-zx`?

## What this does not claim {#limits}

- **Leanpub's rules are as its help centre stated them on 19 October 2026.** The royalty rates, the minimum prices and the membership settings have changed before; the publisher checks them on the day.
- **The 2018 settings are as Leanpub's page showed them** that day: free with a membership, a minimum of $7.99 otherwise, $10 suggested, $20 at most.
- **"Well over 200 pages" is an estimate.** The rc2 PDF built here is 168 A4 pages; at 6 by 9 inches the same text runs to many more, and the publisher's build will count them.
- **The release note reaches only readers who opted in.** Leanpub does not email every buyer.
- **The address was free on the day.** It can be taken before the change.

## Where this comes from {#sources}

A voice memo of mine on 19 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice. The argument and the editorial responsibility are mine.

Leanpub's rules are from its help centre, read that day: [a new version and a new edition](https://help.leanpub.com/en/articles/2936877-what-s-the-difference-between-a-new-version-of-a-book-and-a-new-edition-of-a-book), [offering past readers a discount](https://help.leanpub.com/en/articles/4914213-i-m-publishing-a-new-book-and-i-would-like-to-offer-readers-of-my-other-books-a-discount-on-the-new-book-how-can-i-do-that), [pricing flexibility](https://help.leanpub.com/en/articles/10549058-leanpub-product-pricing-flexibility-to-enhance-your-book-marketing-opportunities-for-authors) (13 February 2025), [free with membership](https://help.leanpub.com/en/articles/9333803-should-i-opt-my-book-in-to-the-free-with-membership-feature-on-leanpub-i-m-concerned-my-royalties-will-go-down-what-should-i-do), [changing the address](https://help.leanpub.com/en/articles/478705-how-do-i-change-the-url-for-my-book), [changing the title](https://help.leanpub.com/en/articles/3076419-how-can-i-change-the-title-of-my-book), [the cover size](https://help.leanpub.com/en/articles/110542-what-size-should-my-book-cover-image-be) and [a totally free book](https://help.leanpub.com/en/articles/4981358-is-there-a-way-to-make-a-book-totally-free). The 2018 settings and numbers are from [the book's Leanpub page](https://leanpub.com/generation-z), read the same day.
