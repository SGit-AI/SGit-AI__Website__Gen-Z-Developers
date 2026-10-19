---
title: Where do you land?
slug: where-do-you-land
part: before-you-start
number: 3
ideas: [jobs-that-never-scaled, maps-before-names, four-stages-beyond-activities, centre-of-gravity, three-learning-paths]
answers_2018: [4.life-patterns/pionners-settlers-town-planners.md]
sources: [art:lucky-to-be-here, art:where-do-you-land, news:why-i-love-wardley-maps, sb:where-do-you-land, news:explorer-coding, news:software-vendors-as-villagers, book:4.life-patterns/pionners-settlers-town-planners.md]
character: tomas
gravity: all
status: draft
---

Take someone's first job and draw what it depends on. Put the person at the top, with the thing they need to get done. Under that, the things that serve the need: the way they work, the tools, the models those tools call, the computers the models run on. Now order it twice. Down the page, from what the person sees every day to what they never see. Across the page, from the brand new and badly understood on the left to the everyday thing everyone takes for granted on the right.

You have just drawn a map. I have not named it yet, on purpose. Look at it first.

The models are over on the right, moving further right every month: a product, being turned into a commodity. The way of working with agents is on the far left, new and rough, and moving towards something a team could build on purpose. Everything on the map is moving, and it is all moving the same way: from left to right, from rare to ordinary. Once you see that movement you cannot stop seeing it, and that is the point of this chapter.

## Maps everywhere, shown before they are named

The map you just looked at is a Wardley map, after Simon Wardley, and they run through this whole book. You will meet them in every part, sometimes with their names on and sometimes, as above, without. I want you to feel the pattern before you learn the vocabulary: the user, the need, the chain of things that serve it, and the movement. The words can come later.

The way I describe one is that it is a graph with two axes of context. *Everything is connected: graphs* gave you the graph. The first axis is vertical: a value chain, anchored at the top on a user and a need, each component drawn under the components that need it. The second is horizontal: evolution, how far each component has travelled from an idea nobody has built to something you buy by the unit without thinking. Wardley's four stages, genesis, custom built, product and commodity, are the scale on every map in this book.

Every dot is a claim: that thing exists, it sits there in the chain, and it is about that mature. The positions are judgements, and the judgements are the argument. A map you cannot be wrong about is a diagram.

Why do I care so much? In 2022 I gave a talk for the Open Security Summit on why Wardley maps changed how I think, and listed eleven shifts they caused in me. The eleventh was: "Wardley Maps gives me inner peace (allowed me to understand why things happen)". Once a thing is on a map, placed and connected, I stop carrying it in my head. When you can see the board, a bad week is a move, not a verdict. The map tells you what is moving the needle, whether you are polishing something three layers below what the user touches, what to build and what to buy, and whether a market exists at all: a layer that is already a commodity is a hard sell, and the custom building that happens on top of a commodity is where the market is.

## The four stages are not only for activities

When people start with maps, I see a lot of them stop at the four stages most examples use, and treat them as a scale for activities only. The movement is everywhere. For that talk I made a table of it. The first four rows are from Wardley's published material; the rows below the line are my own explorations.

- Activity: genesis, custom build, product, commodity.
- Practice: novel, emerging, good, best.
- Data: unmodelled, divergent, convergent, modelled.
- Knowledge: concept, hypothesis, theory, accepted.
- Openness of content: confidential, published with ordinary copyright, CC BY, CC0.
- Openness of software: proprietary, GPL, open source, public domain.
- Backup restore time: infinity (no backups), a week, a day, real time.
- Incident response time: weeks, days, hours, minutes.
- Ideas: not accepted, some value seen, accepted, obvious.
- Data, by shape: unstructured raw text, spreadsheet, graph, map.

There are more rows in the original, on security logs, risk, attacker motivation and concepts. The point for you is that evolution is in how open a piece of writing is, in how fast a team can recover, in whether an idea is accepted, in whether your data is a pile of text or a map. Once you see it, you see it in your own work and your own career, and that last row is this book's own arc: text, spreadsheet, graph, map.

## Where do you fit?

Now the question I most want this book to ask you, early, and keep asking: where are you on it?

Wardley gave the three kinds of people their names: pioneers, settlers and town planners in 2015, and since 2023 explorers, villagers and town planners. Explorers "explore never-before-discovered concepts, the uncharted land"; "They show you wonder but they fail a lot." Villagers "turn the half baked thing into something useful for a larger audience". Town planners "take something and industrialise it taking advantage of economies of scale." The 2018 book had this as an outline and never wrote it; its bullets were to explain the concept, to show how everybody is different, and to connect it to Agile, Lean and Six Sigma. This chapter writes the first two. The third can wait.

I think these are personalities, and I think Wardley nailed them. In business we keep finding the same thing over and over, in Myers-Briggs and in whatever test is in fashion, and in my experience the three do a better job of describing the people I have worked with. That is my experience, not research; the business tests have a contested evidence base of their own, and I do not want to replace one unproven test with another. What I can tell you is what I have seen.

**The explorer** is bursting with ideas. They love to experiment, to try things out. Once it works, it gets boring, and they build on top of it. They are not the person playing with the Lego; they want to invent the bricks. Failure is exciting, because failure is just an experiment. Change is natural to them, and the immediate connection with what they are making, the instant feedback, matters to them more than to anyone. What they make only works for early adopters, because it is going to break: full of wires, half-baked, a prototype. Some users love exactly that, and they live with the explorers.

**The villager** loves the user. They are emotionally attached to the user being happy, almost the user themselves; they put themselves in the middle of the problem and solve it. They thrive on packaging, releasing, going to market, taking something and refining it. They do not like failure that much, because for them the product has to work. Often it is about trimming it down, about simplicity, which is where design comes in: the first version just has to work; the second version has to be designed. Villagers can ship. They are the ones who let things scale; without them, everything would die before it reached the other side.

**The town planner** geeks out on the details. A good friend of mine says boring is good, and that is them: the nice hum of effectiveness, marginal gains, scale, bigger volumes. They like to be invisible, because they know they have done the job right when nothing goes wrong. Their work is making something a commodity, which is still ridiculously hard, and often it means removing things and going back to first principles. They are the people who pay attention to the letters, the words, the dotted i's, the grammar, the code. They can spend hours on one thing. That is craftsmanship, the obsession with getting it right, and it needs less recognition than the product people need, which is fine.

If the third one is you, and you are a little proud of doing things by hand and sceptical of shortcuts, hold on to that. The newsroom's argument in *Explorer coding* is that what people call vibe coding is explorer work, and that an explorer-coded app "is not ready to be in line": nobody has read the code or checked the architecture, and once other people depend on it, it is mission critical. Villagers make it safe to depend on; town planners own the code in production and are accountable for it. The further towards commodity a thing moves, "the fewer agents in line, and the more deterministic code". Your centre of gravity is not out of date. It is where the explorers' work has to end up.

## A centre of gravity, not a box

Everyone has a centre of gravity. Some people can play at several levels, and some are fine in more than one, but there is a centre, and knowing it helps. The test is simple. What do you care about? What makes you lose your sense of time? What is the thing that, when you do it, time just flies? That is where you are.

It moves. As your career changes, your centre can move with it. But it matters to recognise where you are now, because the skills you need as an explorer are different from the skills you need as a villager, which are different again from a town planner's. All three are brilliant. They are brilliant at different things, and they should be learning different things.

This is a lens, not a label. A software vendor, for example, has spent thirty years trying to be all three for its users, and in *Software vendors should become villagers and town planners* I argued that users are now better explorers of their own needs than the company will ever be, so the company should let them explore on top and sell them the maintenance of what they build: "What stops me is not building it; it is maintaining it." The same handover, from the person who explores to the people who maintain and own, is how a team works, and how a career moves.

## How to use this book

So here is how to read the rest of it.

Every chapter carries a badge, in black and white, because the book will be printed that way. A compass marks a chapter that leans to the explorer. A house marks one for the villager. A grid marks one for the town planner. A chapter for everyone carries all three. The badges are a first attempt, drawn for the storyboards, and whether they work is still open.

Work out your centre of gravity first, using the test above. Then read the chapters for everyone, and the chapters with your badge, before the others. There is a path through the book for each of the three, and you will see it from the badges without a table of contents telling you. An explorer will want the chapters on explorer coding and on building fast with agents early; a villager the ones on shipping and on your own newsroom; a town planner the ones on controlling your agent, on the record, and on reading code as a graph. Then come back for the rest, because you will work with the other two every day, and the handover between you is where most of the trouble in software happens.

The last part, dated 2026, is hands on: workflows you can set up this week. It will be renewed as the tools change. The argument in the rest of the book should not need to be. Whether the book should one day be grouped by centre of gravity, rather than only marked, is a question I have not settled; for now, the badges carry it.

## The jobs that never scaled

One more thing before you choose, because the map is also about where the work is.

The opportunity is not only in new jobs. It is in jobs we have been doing for a very long time, sometimes for millennia, that never really scaled and never had good technology: work done one person at a time, by hand, with the tools that person happened to have. We can now scale those jobs with agents. The map shows you where: a layer where everyone is custom building their own version of the same thing, on top of commodities, is a market, and each of those builders would rather buy.

So when you ask where you land, ask it twice. Where on the spectrum, explorer to town planner, does time fly for you? And which old job, now that it can finally have good technology, would you want to be the one to scale? The second question is the one the rest of this book keeps circling back to.

> **For Dinis:** three examples of jobs that never scaled, and now can. The article asks for them and the chapter needs them here; without them this section is a claim without a case.
