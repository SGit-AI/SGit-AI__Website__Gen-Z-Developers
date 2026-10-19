---
title: Images, infographics and storyboards, drawn by code
slug: images-infographics-and-storyboards
part: hands-on-2026
number: 27
ideas: []
answers_2018: []
sources: [agent:storyboards-drawn-by-code, art:everything-is-connected, sb:everything-is-connected]
character: zara
gravity: explorer
status: draft
---

By the end of this chapter you will know how to make a storyboard that is data, not a picture: a cast file, one file per story, panels drawn in the browser every time, and every quoted line checked against its source before anything is released. It is how the storyboards on this book's site are made, and the method is the one the site's journalist, an agent, set out in *Storyboards drawn by code*. There is no image file to edit. Change the data and the picture changes.

I asked for two things in one memo: a survey of the newsroom for this book, and a way to see the book as a storyboard, with characters, that was not boring boxes and not a round of image generation, and that I could flick through on an iPad. The journalist went to look at how another site of mine had done its storyboards. There, each story ends in a prompt for an image model: good pictures, and every change costs a new image. The lessons it brought back were the ones to keep: draw the cast first, keep storyboards as data, and write the model's mistakes down.

So here the panel is drawn from the data, in the browser, every time. People are drawn from a look (skin, hair, shirt, trousers, an accessory) in a pose (stand, point, wave, arms up, shrug, think, sit) with a mood (neutral, happy, worried, surprised, thinking, determined) that sets the eyebrows and the mouth. Rough.js, an open-source drawing library, gives every stroke its hand-drawn wobble, and a seed per panel keeps it identical between loads. The deck swipes natively on a tablet; when a panel arrives its strokes draw themselves, the people walk in and the bubbles pop, in order. Export is a script that screenshots each panel to a PNG.

This is also this part's answer to infographics and presentations: a deck you can swipe is a presentation, an evidence card with a pinned quote or a bar chart is an infographic, same data, same renderer.

## The workflow

1. **Write the cast first.** One file, with each character's role, what they stand for, a personality, what they want and fear, a line, and a look. Their pronouns are part of the file. This book's cast has six: Zara, Tomás, Priya, Sam, the Guide and the Agent, and the Agent is drawn differently, with a screen for a head and a prompt on its chest. One lesson from the other site: avoid a character called "Dev".
2. **One file per story.** A slug, a title, a punchline, the cast it uses, and the panels. Five kinds of panel to start: a cover; a scene, with a setting, props and people; an evidence card; a punchline; and a spectrum, a line of labelled stops with people placed along it. Since the article was written the storyboards can draw graphs too: nodes and labelled edges, groups that hold groups, a highlighted path from A to B, and a detective's board with pinned notes and red string.
3. **Name the source of every quote.** A storyboard that quotes names a `quote_source`, and every line the Guide says and every quote card has to be in it word for word. A line that is not meant as a quote says so, with `not_a_quote` and a note.
4. **Render, then look.** Review by rendering the panels to images and reading them as a reader would. The first version here had quote cards too small to read on a tablet, bubbles too wide, heads too small for a cartoon, and a punchline underline that ran into the characters.
5. **Let the build refuse.** Before the first release the journalist checked every quote against its source with a script, and four failed: one was a slip ("anyone who can brief an agent is one", where the article says "anyone who can brief an agent to build something is one"), and three were lines never meant as quotes, which now say so. For the 2018 storyboard the check then moved into the build: a Guide line or quote card not found in the frozen text, word for word, stops the release. It was tested by changing one line and watching the build refuse it.

That last step is the one to copy even if you never draw a panel. A citation that is not in the source should fail by machine, before a person reads it.

## A worked example

The storyboard for *Everything is connected* uses all of it, and its third panel is the one to study. The caption is "The whodunit: who broke the build?" The nodes are "the build broke at 9:14", "commit a3f", "the agent's pull request", "tests skipped", "Tomás, on holiday", "a library updated" and "approved in 40 seconds". The edges carry verbs: after, merged from, skipped, includes, approved, "pinned it, once". And a path is highlighted, from the break to the commit to the pull request to the skipped tests. The panel's note says what it is: the detective's board is a graph, the highlighted path is the answer from A to B, and the case is made up.

The file's own rule, written at the top, is that every line the Guide says and every quote card is from the article word for word, and the build checks it; the whodunit, the forest and the provenance chain are the storyboard's own illustrations, and they say so. That panel has no picture anywhere on disk. It is a list of nodes and edges with positions, and a renderer. Nothing is redrawn by hand, because nothing was drawn by hand.

## What it does not do yet

The renderer is a prototype: when the article was written, five panel kinds, seven poses, six moods; enough to see a storyline, not to illustrate a printed book. No image model was used, and none is ruled out: a storyboard is a brief an image model could also draw from, and the data is the same either way. The deck was tested in a headless browser, not on an iPad, and my iPad is the real test. And when the cast and the first storyline were made, every content choice in them was a proposal for me; I had decided none of them.

> **For Dinis:** the Guide's pronouns are they/them in the cast file until you decide how the author appears. Is the Guide drawn as you?
