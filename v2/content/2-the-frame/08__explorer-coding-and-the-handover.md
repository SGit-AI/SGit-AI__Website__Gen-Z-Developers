---
title: Explorer coding, and the handover
slug: explorer-coding-and-the-handover
part: the-frame
number: 8
ideas: [explorer-coding, the-handover, the-villagers-craft]
answers_2018: [5.concepts/repl.md, 5.concepts/legacy-applications.md, 4.life-patterns/refactoring.md]
sources: [news:explorer-coding, news:a-browser-for-one, news:who-will-fix-your-mess, news:the-citizen-developer, news:explorer-to-villager-newsroom, art:where-the-thinking-came-from, book:5.concepts/repl.md, book:5.concepts/legacy-applications.md, book:4.life-patterns/refactoring.md]
character: zara
gravity: explorer
status: draft
---

The first edition had an outline called *REPL*, which I never wrote up. The bullets said: explain the concept, Read Execute Print Loop; say how my own O2 Platform did it well; and note that the idea was "still not very well understood and used". A REPL is the oldest fast feedback loop in programming. You type a line, it runs, you see the result, you type the next line. I thought it was a concept for programmers. It turns out to be the thing that explains what everyone is doing now.

## Why not vibe coding

The phrase people use is vibe coding. It is Andrej Karpathy's, from a post in February 2025: "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists." He was describing throwaway weekend projects.

I have never liked it, and I think the word is doing harm. It sounds as if people are just typing, going with a feeling. It is a little demeaning to the people doing it, and it hides what is happening. I am not alone in this: Andrew Ng said in May 2025 that "It's unfortunate that that's called vibe coding", and that coding with AI is "a deeply intellectual exercise".

So I would like to propose a better name: explorer coding. I considered spreadsheet coding, because of where this comes from, and brief coding, because of what it produces. But if you think in Wardley maps, as *Where do you land?* asked you to, the right word is already there. Explorers, in Simon Wardley's words, "explore never-before-discovered concepts, the uncharted land"; "They show you wonder but they fail a lot." That is exactly what someone does when they build the tool they need with an agent. The nearest existing term is *exploratory programming*, programming while the requirements are still being discovered.

> **For Dinis:** the newsroom calls explorer coding a proposal, and the ideas register still has it as a candidate. Is it the book's word, used throughout, or does the book say "what people call vibe coding" and explain it once?

## The best thing since the spreadsheet

People have always built software with whatever they controlled, and for most of them it was a spreadsheet. Spreadsheets won because of the feedback loop: change a cell and see the result, a read-evaluate-print loop for people who would never call it that. Everybody was already exploring; it was just very slow, because anything beyond a spreadsheet meant writing a document and waiting for someone else to build it. What has changed is that the loop is now fast for anything: an app, a workflow, a customisation of a product, a change to the interface of a single moment.

That is why I think it is the best thing to happen to software since the spreadsheet. I was talking to someone who works in HR, and once we started to explore what her team will be doing, the apps, the customisations and the workflows they will build, and the agents they will have to manage, her answer was that it was amazing, and when could she start. One conversation, not a survey.

I can give you my own example. The browsers on my phone had frustrated me for years: the wrong page, reloads, no offline mode, no memory of where I was. I lived with it, like everyone. Then, after weeks of building with agents, writing my own browser for one site stopped sounding unreasonable, and I wrote the brief for it. What changed was not the browsers. It was me. Patience for bad interfaces wears thin when you can do something about them, and frustration plus the power to build is where explorer coding starts.

Explorer coding is not a way to ship. It is a way to find out. And what explorers produce is the best brief there is: a working app says what its user wants better than any document, because it runs.

## Not ready to be in line

This is the part the new word makes easier to say. An explorer-coded app may look like an application and feel like an application, but it is a brief. Nobody has read the code. Nobody has validated the architecture. It does not meet any internal standard, and it is not ready to be *in line*: in the path of work that other people depend on.

The trap is that dependence comes quickly. Once something gets used, it is mission critical, even for one person, if it replaced how they work. From then on it has to be maintained, checked and kept working, and new versions cannot break it.

The first edition had an outline for this too, called *Legacy Applications*. One bullet said: "The code you are writing today will be legacy tomorrow." Explorer code becomes legacy the moment someone relies on it, and the outline's list of what makes legacy work attractive reads now like a description of the villager's job: "no new features", "very low expectations of changes", "changes are supposed to be hard", "lots of low-hanging-fruit for refactoring".

## The gap is a handover

In October 2026 Harvard Business Review published an article on turning vibe-coded prototypes into tools a company can use. Its argument, as its public summary and one author's post put it: generative AI has made building software feel almost free, so the prototype is the easy part, and turning it into a tool people rely on every day is the hard part, which they call the deployment gap. The post's opening line was: "'Build or buy in the age of AI?' Wrong question. The real one is: 'Who will fix your mess?'" I have read the summary and the post, not the full article, which is behind a paywall.

I agree with almost all of it, and I would change two things. First, I would not start from the mess. The prototype is not a mess. It is the most precise requirement the company has ever had. The mistake is to put it in line before anyone has done the work that makes software dependable.

Second, the gap is not a place to stop. It is a handover between people with different skills. Explorers are good at finding what is needed. Villagers are good at making it reliable: tests, data handling, releases that do not break it. Town planners are good at running it at scale, and they own it in production. The article's own warning story, a bank that piloted a startup's tool, built its own prototype instead, and went back to the startup a year later, is not a story of a weak team. An explorer team was asked to be villagers and town planners as well, on a regulated, data-heavy, daily-use tool, and those are different jobs.

The post also offered a test: would your team accept a bonus tied to how this tool performs in production? I like it, because it has a name in the Wardley frame: it is the moment the town planners take the code and answer for it. More of the industry already says so: the Linux kernel's rules for AI coding assistants say "Only humans can legally certify the Developer Certificate of Origin", and Fedora's proposed policy says "The contributor is always the author and is fully accountable for their contributions." We cannot make an explorer accountable for code they never read. We can make the team the work is handed to accountable, and the town planners above all. And "who will fix your mess?" should never have one answer: if the code is open, anyone can.

## What a handover looks like

I can show you one, because the newsroom went through it. Its first version had a crazy amount of features, a meter that charges by how far you read among them, and it was live and taking money. It was also, like most explorer projects, bundled in the middle of something much bigger: the application that bills sat in the same repository as 74 articles and their images.

Measured on 11 October 2026, the live reader code was about 2,700 lines. The tests that covered it were 433 lines, and the one workflow never ran them. The same code had two upstreams. No page had a Content-Security-Policy. None of that is a criticism of the explorer work; it is what explorer code looks like, and it is why it was fast. But a mistake in the meter was now a mistake with someone's money.

So the brief was to go slow to go fast, in six phases, with no behaviour change until the fifth. Map every file and every control. Move the code to its own repository as a pure refactoring, "the same behaviour and the same bugs", proved by hashing every file the live site serves before and after. Write tests, with every known bug recorded as a test that passes, so the fix later is a visible change. Review, with every finding an issue. Refactor until no change to what a reader sees or pays can slip through. And only then: the explorer returns.

The rule underneath it: explorer code is read for intent, mostly by agents; villager code is read line by line, because that is where the blast radius lives; town planner code is read by deterministic checks. The further towards commodity, the fewer agents in line, and the more deterministic code.

## The villager's craft

The handover is where the people who make things last take over, and their craft has a canon. Design, in the sense that design is how it works and not decoration, became a mandatory step in how my agents build interfaces: every change has to be simpler, and reverting it should feel worse. The wider design canon says every element must earn its place, which applies to an API or a command line as much as to a screen. And Christopher Alexander's *A Pattern Language*, from 1977, is where software design patterns came from; its lesson for the town planner is that code is a space people inhabit. The villager's second version has to be designed; the town planner has to live in the code. This book names that canon where the villager's chapters need it.

The first edition had a third outline here, *Refactoring*: what it is, and how to apply it to your life. Refactoring is the villager's verb: changing the structure of a thing without changing what it does, with a test to prove it. Applied to your life, it is the same move. Build fast to find out what you want. Then, before you depend on it, slow down and make it something you can rely on.

Even power users want that handover. When my browser for one works, it will be part of my day, and I will not want to maintain it. Not because I cannot; because it is not my focus. Being able to compile a Linux kernel does not mean I want to compile Linux kernels. I would rather hand it to someone and pay a couple of pounds a month for them to keep it working. The explorer builds the brief. The villager keeps it alive. Knowing which one you are, on which day, is most of the skill.
