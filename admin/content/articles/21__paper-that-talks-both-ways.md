---
title: Paper that talks both ways: QR codes take the reader from the page to the website, where the sources, the graphs and the visualisations live, and a pen and a photograph take the reader's notes back, which changes how I want to read every book
date: 2026-10-19
author: Dinis Cruz
summary: Two things came out of reading the printed release candidate with a pen. The first is QR codes. From a provenance and explainability point of view the medium of the book is not good enough, but we have a whole website and a whole graph behind it, so whenever the page needs more room, more evidence, a source, a visualisation, a bigger storyboard, a repository or the newest version of something, a small QR code can send the reader there. The code prints a short address on the book's site, so the paper never goes out of date. It also opens a commercial angle: the website will have its own billing, pay per page, and a book could come with credits. The second is the review itself. I write on the page, I take a photograph, and the agent reads my handwriting, captures every note, and turns it into articles and drawings. I always loved reading but never scaled the capture of what I learned, the comments I wanted to send to the author, the passages I wanted to find again. Now I can: read with a pen, photograph, and let it become something. That changes my reading habits, and it should be in the book, in How to read this book and as a workflow the reader can copy.
version: v0.2.39
tags: qr-codes, reading, workflow, provenance, website, paper, gen-z-book, article
status: published
---

## In short {#in-short}

- **The page is not enough for provenance and explainability.** The website and the graph behind the book are.
- **QR codes join the two.** Small, in the margin, wherever the page needs more room.
- **They point to a short address on the book's site.** So a printed code never goes out of date.
- **They point to anything.** Sources, the graph, visualisations, bigger storyboards, repositories, newer versions, other chapters, the 2018 book.
- **And there is a business in it.** The site will charge per page; a book could come with credits.
- **The pen works the other way.** I write on the page, photograph it, and the agent captures every note.
- **That changes how I read.** Every book I love can now leave something behind: comments for the author, nuggets for my influences.
- **It belongs in the book.** How to read this book recommends it; the hands-on part shows how.

## The page needs more room {#room}

I think we can use QR codes quite creatively here. If you look at the book from a provenance point of view, and from an explainability point of view, the medium of the book is not good enough. A page cannot hold the source of every claim, the data behind it, the graph it sits in, the visualisation that explains it. But we have a whole website. We have the whole graph. We have everything we would want the reader to be able to follow.

So the book becomes the way in, and anyone who wants to learn more, to get more evidence, to follow a topic or to see a visualisation, can. Any time we want to link, any time we need more real estate, we can point to the website. That solves a lot of the problems I was having with the review, which are really one problem: how to balance the medium of the book with the interactivity of the website.

## Small codes, stable addresses {#codes}

The codes do not have to be big. As long as they are small enough to fit the margin and have enough granularity for a phone to read, they work, and they only point to public pages. Each one prints a short address on the book's own site, `gen-z-developers.sgit.ai/q/` and a name, and that page sends the reader on. Those are pages we can maintain. When something moves, or there is a newer version, or I update a repository, the page behind the code changes and the paper does not.

<figure><a href="../reviews/paper/rc2-03/after-margin-system.svg"><img src="../reviews/paper/rc2-03/after-margin-system.svg" alt="Sketch: a page of the book with facts and opinions marked in the margin, a concept explained in one line, and QR codes to the site" loading="lazy" style="max-width:560px"></a><figcaption>The journalist's sketch of the margin, with the first codes; they scan, and <a href="../q/index.html">the list of codes</a> says where each goes.</figcaption></figure>

And they can point at anything: the source of a claim, the newsroom article behind a chapter, a talk, the book's graph, a bigger version of a storyboard, a repository, the 2018 book, another chapter, the evolution of an idea since the book was printed.

## A commercial angle {#commercial}

It also introduces some interesting commercialisation angles. The website is going to have its own billing model, charging per page or per thing you see, the way the newsroom's reading meter works. So somebody who buys the book could get an amount of credits for the site. The book stays the book; the site becomes the place where it keeps going. That is for later. In the short term, the codes just solve a lot of linking.

## The pen works the other way {#pen}

The other thing I realised is something you can only realise after you experience it, which is exactly what I talk about in this book. I write on the printed page, in my handwriting, I take a photograph, and the journalist agent reads it, captures it, draws it, and turns it into articles. Yes, I am trying to write a bit more legibly. But it is capturing it, and that creates a very powerful feedback loop.

Then I realised: I am going to use this myself. One of the problems I always had with books is that I love reading, but I never scaled the capture of the knowledge. Sometimes I want to make a comment, or send something to the author, or just capture what I learned, and I lose it. I think I will go back and write it up, and I cannot find the page, or the chapter is not where I thought. Sometimes I took the time to highlight things, but it never made sense to do it properly, because nothing would happen from it.

Now I can read a book, make comments, highlight, tag, take a photograph, and have that transformed into an article, or into notes, or into something. That is a ridiculously powerful workflow. It completely changes my reading habit and makes reading a lot more interesting. It means I can go back to the books I love, find those nuggets and those comments, and leave them, for example, in [my influences](https://influences.sgit.ai/).

## In the book {#in-the-book}

That is why the page called *How to read this book* should not only say read it on paper with a pen. It should recommend this workflow, the one I am using right now to review the book: read on paper, write on it, photograph the pages, and let an agent read your handwriting and capture what you thought. And the hands-on part should show how to set it up, so the reader can do it with this book and with every book after it.

## The brief {#brief}

For the publisher. Read `team/publisher/role.md`, decisions 016 and 018, and this article first.

1. **Put QR codes in the release edition** wherever a chapter links: small, in the margin, each a short address from `admin/content/qr/links.json`, with the page behind it. Done when the release edition's links are codes, and every code has its page.
2. **Look at the credits idea**: what a book buyer would get on the site, and how it would work with the site's billing. Done when it is a note in your `briefs/`, for later.

For the editor:

3. **Mark facts and opinions, and explain concepts in a line**, as the margin sketch proposes; every link becomes a code with a line of text saying what it is. Done when chapter 2 of the next candidate does it.
4. **Rewrite How to read this book** to recommend reading with a pen and photographing the pages for an agent. Done when the next candidate has it.

For the journalist:

5. **Write the reading workflow as a hands-on chapter**: read on paper, mark, photograph, let an agent capture, publish what you learned. Done when the article for it exists, from this review as the worked example.

For the librarian:

6. **Process this article** into the register, and the QR codes as a source of links. Done when both are cited.

## What this does not claim {#limits}

- **The codes are the first seven.** The rest come as the editor places links.
- **The credits are an idea, not a plan.** The site's billing does not exist yet.
- **The reading workflow is mine, and a few days old.** It works for me; the hands-on chapter will say what it needs.
- **A code is only as good as the page behind it.** The build refuses a code without one.

## Where this comes from {#sources}

A voice memo of mine on 19 October 2026, sent with the third batch of photographs of my review of the printed release candidate, written up by this site's journalist, `gen-z.journalist`, in my voice, keeping the memo's order and phrases. The argument and the editorial responsibility are mine. The review is in [RC2 on paper, part 3](/agent-articles/rc2-on-paper-pages-10-to-13.html); the codes and the pages behind them are built from `admin/content/qr/links.json`.
