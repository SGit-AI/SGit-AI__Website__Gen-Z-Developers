---
title: "Publish, publish, publish: your own newsroom"
slug: your-own-newsroom
part: getting-the-job
number: 12
ideas: [publish-publish-publish, every-part-buys-the-next, the-voice-is-four-inputs, the-memo-is-the-thinking, your-newsroom-is-your-demo-and-your-crm]
answers_2018: [4.life-patterns/publish-publish-publish.md, 2.mvp-for-gen-z-dev/content/hugo.md, 7.your-cv/leanpub.md, 5.concepts/amazon-press-releases.md]
sources: [news:your-own-newsroom, news:books-from-articles, news:nineteen-sites, news:the-man-behind-the-curtain, news:the-question-is-whether-they-miss-it, news:how-the-voice-works, news:how-much-of-this-did-i-write, news:not-a-straight-line, art:gen-zx-developers, book:4.life-patterns/publish-publish-publish.md, book:2.mvp-for-gen-z-dev/content/hugo.md, book:7.your-cv/leanpub.md, book:5.concepts/amazon-press-releases.md, book:7.your-cv/blogs.md]
character: tomas
gravity: explorer
status: draft
---

The first edition had a draft called *Publish, Publish Publish*. It never got past its notes. One of them was the story of how that book was being written: as soon as I had some content, about 20% done, I published it on Leanpub. Another promised a graph showing that great minds and artists publish a lot, because the frequency of publishing is one of the best indications of talent. The outline on Leanpub next to it said "publish early and often", and, two lines down, "all the other leanpub books that I have not completed".

Those two notes, side by side, are the honest version of this chapter. I believe in publishing constantly, and my books stall. My Leanpub page lists ten: *Hacking Portugal* at 95%, last updated in December 2016; *Generation Z Developers*, the book whose second edition you are reading, at 60%; and seven more, most between 60% and 95%. The reason is the same every time, and I said it in a memo once: "you almost start to be locked by the first version of the content, because making changes becomes quite painful." A book is one big batch: every change touches everything, the review piles up on one person, me, and when my energy moves to the next thing the book stays where it was.

> **For Dinis:** the 2018 outline promised a graph of how much great minds and artists publish, as evidence that frequency is a sign of talent. Did you have a source in mind, or should that claim be cut?

## Why the articles do not stall

The articles I publish now work the other way. Each one starts from a voice memo, is researched and checked, gets its figures and its sources, and is live the same day. Each one is finished: nothing waits on the next one. And there is a feedback loop: an article is read, corrected and linked within days, and the next memo builds on what is published. A good feedback loop is shipping, often and early. The books never had one.

So here is my hypothesis, untested until a first book proves it: a book is a curated, ordered set of finished articles, plus the editorial thread that connects them. The thread is my part: choosing, connecting, adding the nugget. This edition is one test of it, and *How this book was made, and what you made* says how it went.

The lesson for you is smaller. Small finished pieces beat big batches. Shipping does not mean a proof of concept or a demo; it means a thing somebody else can go and use, on their own, and get value from. Ship that, often, and each piece buys you the position you need to do the next.

## The loop you can copy on day one

The founders I most want to see succeed are the authentic ones, who come from the field they are building for. Their brand is themselves, and it needs a medium that keeps their story. I wrote the recipe below for them; it works just as well when the company, for now, is you.

In 2018 the chapter on Hugo made the case for static sites: a generator builds every page in advance, and the result is a folder of files with no back end and no moving parts. I asked you to ask yourself "Why do you need a database?" and to notice how often the answer is that you do not. The file system was the database, git was the deployment, and GitHub was the content management system. All of that still holds. What is new is who edits the files.

The loop is short. You speak a memo. An agent researches it, writes it in your voice, checks it against sources, builds the site, runs the checks, and publishes. Everything it needs exists today: a GitHub account and one public repository (GitHub Pages is free, and on a free plan the repository must be public, so nothing confidential goes in it); an agent plan with cloud sessions connected to that repository; and any app that turns a voice memo into text, because the order you said things in, and the words you reached for, are the raw material.

The steps, as I give them to founders:

1. Create the repository and turn on Pages. Add a workflow that validates before it publishes; the rule that matters is that a failed check stops the release.
2. Write the house rules: one file at the root that the agent reads at the start of every session. Who you are, your voice, what to check, what never to publish. It grows by one line every time you correct the agent.
3. Connect a cloud session to the repository and give it the first brief: the folders, an article template, a small build script, a validator, and a first page about you.
4. Record, paste, review. Correct by voice. The agent changes it, rebuilds, validates, pushes, and checks the live page.
5. Keep the record. Every article says what it does not claim and where it comes from; a correction is a new version, not a note about the old one; every release gets a version and a one-line note.

What it is like to run: on the newsroom, in three days, 54 messages from me, ten of them voice memos, became 40 releases. The memo is a draft of a thought; the article is the thought, checked. And once the pattern exists it repeats cheaply: in fifteen days in August one site became twenty repositories, because publishing had been reduced to adding one file.

Two honest limits. The writing pipeline is a pattern to copy, not yet a kit. And a rule in a prompt is a hope: only the rules a hook or the build keeps are enforced, so mark which is which. A site like this is also pure client side, the way *Serverless, for real* asks your product to be.

## An article behind every answer

The 2018 outline on blogs had one idea I still use every week: answer questions made to you with a blog post. When somebody asks you a question, write the answer as a post and send them the link. It scales your time, especially when several people ask the same thing.

My rule now is stronger. If I am sending an email that answers a real question, there should almost always be an article behind it. Someone once pointed out that they sent me about two hundred words and got back closer to two thousand. Fair; but I only write it once. The next person who asks gets a link. The article can be read later, forwarded, checked against its sources and corrected as a new version, none of which an email can do.

Who writes it matters. The agents draft; I read every draft, often change it a lot, and I send it. It is the Wizard of Oz in reverse: the program is visible and the person is behind the curtain, and the person stays, because an article can be corrected tomorrow and an email cannot be unsent.

Each part of an email buys the next. The subject, a few seconds of attention, buys the first line. The first line buys the paragraph. The first paragraph buys the decision to read the email, and the email buys the article. Nothing further down gets read if something higher up did not earn it. The 2018 book had a note on Amazon's habit of writing the press release first, with the definition of success in it. It is the same discipline: the first line has to carry the whole thing, for a page, a pull request or a CV.

For you, in a job hunt, this is the whole method in one habit. Every time a colleague, a lecturer or an interviewer asks you something you know, the answer becomes a page. A year of that is a body of linked, dated, checked work, and when the hiring manager asks why they should hire you, you do not make a claim. You send a link.

## Your newsroom is your demo, and your CRM

My company sells behaviour policies and licences to operate for agents. The hardest part of selling them is showing them in action, because the examples are customer work and cannot be shared. The ecosystem around the newsroom, its agents, their behaviour policy, the status report every few answers, the leak scan before every commit, the releases with their logs, is the best public example I have of a policy running under real load every day.

And a very effective newsroom is, underneath, a very effective CRM and publishing workflow: agents that follow up people and threads, draft, publish and keep a record. The company had reasons to follow people up, but not at volumes that would push the workflow to mature; its traction is something I describe rather than measure. The newsroom had readers every day, and readers mature a workflow. The rule runs through this book: always follow the users, even when the user is you, and follow the feedback loops. A problem solved before anybody needs it is solved in the abstract, and that is where complexity creeps in.

So your newsroom is not a side project. It is the demo of how you work, the record a customer or a hiring manager can check, and the first version of the machinery that will follow up your first ten customers.

## The voice is not a setting

There is no setting that makes an agent write in my voice. The voice comes from four inputs, and if you take any one away it stops working.

The corpus: everything already published. When the agent writes for me it has the articles the new one links to in front of it, read in full, so the vocabulary is defined on the page. On the newsroom that was 86 articles, about 347,000 words, 51 of them from voice memos, and under those years of my earlier writing. The memo: me talking, in the order I thought it. The rules: seven of them, each a correction I made once. No em-dashes. No absolutes I cannot back. "Great", not "perfect". British English. Plainer words. They live in a file the agent reads back after every summary, and the build checks some of them, so a banned word cannot reach the page. The reader: I read every article, before it goes live and after. A wrong word becomes a rule; a wrong point becomes a new version. The model never decides whether something sounds like me. I do.

Nothing is trained. The agent is the same model anyone uses; what is different is one session's context: one rules file, one corpus, one set of memos, one reader. That is why the method transfers and the voice does not. The agent that runs the newsroom, asked to speak for itself in *How the voice works*, put it better than I have: "the person has to do most of the work, by thinking out loud, by reading, and by saying no."

For you this is good news. The corpus can start today, at one article. The rules file starts at one line, the first thing the agent gets wrong. The 2018 outline on blogs said the hard part is the first fifty posts, and to write for your future self; the corpus is exactly that.

## Speak it, do not type it

The input I think matters most is the memo, and I want to call it what it is: my hypothesis, from one author's experience, with one session's counts behind it. A typed brief is already edited into someone else's register. A memo is how I think, in the order I think it, with the phrases I would actually use, and the agent keeps those phrases rather than paraphrasing them. The transcript is not tidy, with "right?" every third sentence and a tangent in the middle of the point, and that is exactly why it works. The tangent is not noise; it is the connection I made, and keeping it in its place is what makes the article mine rather than a summary of my instructions. An article from a memo sounds like its author. One from a typed brief sounds like a careful assistant.

The counts, for what they are worth. Over twenty-seven days I sent 148 messages and 65,323 words, 55,473 of them in thirty-seven voice memos, and the agent published twenty-two articles of 96,451 words across 123 releases. No article came from a one-line prompt. The real input is not the memo. Behind one of those articles the agent found and quoted thirty-three pieces of my earlier writing, none written for it. The agent is fast because the record exists.

That is why I would start your record now, this week, before you have anything you think is worth saying. A model that can go in every direction needs someone with a direction. The direction is yours, and the record is how you show you have one.
