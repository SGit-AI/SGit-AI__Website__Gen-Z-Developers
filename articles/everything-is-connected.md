---
title: Everything is connected: a graph is a network of nodes and edges, not a diagram; a map is a graph with positions, provenance is a graph, the world is groups of groups, and you can start anywhere
date: 2026-10-18
author: Dinis Cruz
summary: Graphs are one of the most fundamental ideas in this book, and one to introduce sooner rather than later. I have met people for whom a graph is just a diagram, so the book has to show what we mean: a network graph, nodes and the edges between them. The easiest way in is the whodunit, the detective's board with the connections from A to B. A map is a graph with positions; a Wardley map is a graph with context. Graphs nest: there are graphs of graphs, fractal graphs, and even nature is a gigantic graph, from systems down to molecules and photons, where groups of groups form natural abstraction layers, which is how we think. That is how I see the world: it is made of connections, which is why provenance is a graph, and why so many of the relationships in this book are graphs. And because a graph has no top and no bottom, you can start anywhere: it does not matter where you start, it matters that you start, and get movement. The 2018 book already had this as an outline, which says I had been thinking in graphs for years and that it is a very hard paradigm shift to make, and two of its published chapters, on the DOT language and on syntax trees, were graphs without saying so. Since then the newsroom and graphs.sgit.ai have written a lot about graphs, with figures and visualisations, and this article says what the book should bring from them. The storyboards can now draw graphs too, including the detective's board.
version: v0.2.13
tags: graphs, fractal-graphs, provenance, maps, connections, starting, gen-z-book, article
status: published
---

## In short {#in-short}

- **Graphs belong early in the book.** They are one of its most fundamental ideas.
- **A graph is a network, not a diagram.** Nodes and the edges between them; some people think a graph is just a picture.
- **The whodunit is the easiest way in.** The detective's board: the connections from A to B.
- **A map is a graph with positions.** A Wardley map is a graph with context.
- **Graphs nest, and so does the world.** Groups of groups form natural abstraction layers, from systems to molecules to photons.
- **Provenance is a graph.** Where something came from is a chain of edges.
- **You can start anywhere.** It does not matter where you start; it matters that you start.
- **There is already a lot to bring.** The 2018 outline, the newsroom's articles, graphs.sgit.ai's books and figures.

## A graph is not a diagram {#not-a-diagram}

I have met people for whom a graph is just a diagram, a picture with boxes. So the book needs to show what we mean, and the visualisations are the way to do it. What we mean is a network graph: nodes, and the edges that connect them.

The first of the graphs books on graphs.sgit.ai, *Fractal Semantic Graphs*, says it in its second chapter: "In this book a graph is a network: nodes and the edges that connect them. Never a chart, never a figure." It separates three things people mean by the word: networks, for analysis (who is connected to whom); storage, graph databases, for speed; and semantics, for what something means. This book uses graphs in the first and third senses, and almost never needs the second.

## The whodunit {#whodunit}

The way I sometimes explain it is the whodunit, the detective story: the board on the wall with the photos, the notes and the red string between them. The question is always a connection, from A to B: who knew whom, who was where, what links the two. That board is a graph. And as [follow the rabbit holes](/articles/follow-the-rabbit-holes.html) says, this generation are very good detectives already.

## A map is a graph with positions {#map}

In a way, a map is a graph with positioning. In my talk on why Wardley maps changed how I think, the first two shifts were exactly that: "Its a graph with context", and "When a graph becomes a Map". A Wardley map is a graph where each node has a place on two axes, how visible it is and how evolved it is, which is what makes it a map and not only a graph. That is why [where do you land](/articles/where-do-you-land.html) and this article belong next to each other.

## Graphs of graphs {#fractal}

It is very important to talk about fractal graphs, and graphs of graphs, and how everything connects. In a way, even nature is a gigantic graph: from the system, down to the molecules, down to the photons; everything is connected to everything else. And it is groups of groups that form natural abstraction layers, which is how we think.

The newsroom's [introducing fractal semantic graphs](https://newsroom.sgit.ai/articles/introducing-fractal-semantic-graphs.html) puts the consequence in two sentences: "There is no top and no bottom. There is only the altitude you happen to be looking from, and how much definition you choose to load at it." And one line from the graphs books says why the edges matter more than the nodes: "A node connected to nothing is literally meaningless."

## How I see the world {#world}

Fundamentally, that is how I view the world: it is all made of connections. This connects to this, which connects to that, which connects to that. That is why provenance is a graph: where a claim came from is a chain of edges back to its source. As the newsroom's [journalism becomes intelligence](https://newsroom.sgit.ai/articles/journalism-becomes-intelligence.html) puts it, the record should be "not a pile of articles, but a graph whose every edge has a date and a source". And it is why so many of the relationships in this book are graphs: the influences, the paths, the evidence, the people in a team.

The graphs book has a line for the reader who thinks this sounds exotic: "you may already think in graphs without ever having called it that." Tracing what an unfamiliar system connects to, trusting a claim because of where it came from, asking what else breaks if this fails: that is thinking in graphs.

## Start anywhere {#start}

And for me the other thing about graphs is the ability to start anywhere. It is very important that you never feel overwhelmed. It does not matter where you start; it matters that you start. It does not matter, in a way, whether you are going straight in the right direction; it matters that you get movement. You start to learn, you start to think about these things, you start to connect the dots, and you make movement. So start from a place, and then start connecting.

A graph has no front page. Whatever node you start from, the edges take you to the rest, which is why [connect the dots backwards](/articles/connect-the-dots-backwards.html) can say that a path only makes sense afterwards.

## The 2018 book was already there {#2018}

The 2018 book had an outline called *Graphs*, never written, and its four bullets are this article in miniature: "Graphs are everywhere", "I've been thinking in graphs for years", "very hard paradigm shift to make", "requires an ability to think in nodes and edges". And two of its published chapters were graphs without saying so: *Dot Language*, about drawing the diagrams that software never has, and *AST*, which opens by calling an abstract syntax tree "a graph representation of source code".

## What to bring {#bring}

We already have a lot of material that connects these dots, with good explanations and visualisations:

| From | What it brings | Where in the book |
|---|---|---|
| *Fractal Semantic Graphs*, ch. 2, *Why graphs at all* (graphs.sgit.ai) | The definition, and the three meanings of "graph" | This chapter's opening |
| *Fractal Semantic Graphs*, ch. 1, *A node is just a node*, and ch. 3, *Every edge is a verb* | Meaning comes from the edges; edges are verbs with inverses | The chapter, for readers who want more |
| *Fractal Semantic Graphs*, ch. 15, *Your first graph* | A first graph, built by hand | The hands-on part |
| [Introducing fractal semantic graphs](https://newsroom.sgit.ai/articles/introducing-fractal-semantic-graphs.html) | Graphs of graphs; no top and no bottom | Graphs of graphs |
| [The graphs books](https://newsroom.sgit.ai/articles/the-graphs-books.html) | Three books written over a graph, and the altitude ladder | How this book was made |
| [Search as navigation](https://newsroom.sgit.ai/articles/search-as-navigation.html) | A graph per article makes search into navigation | Graphs, memory and your future self |
| [Knowledge that maintains itself](https://newsroom.sgit.ai/articles/knowledge-that-maintains-itself.html) | Knowledge kept as a graph, maintained by agents, checked by code | Working with agents |
| [The agent is the reader](https://newsroom.sgit.ai/articles/the-agent-is-the-reader.html) | A graph answers in 90% fewer tokens than the text it was made from | Why graphs matter to agents |
| [Code review as a fractal semantic graph](https://newsroom.sgit.ai/articles/code-review-as-a-fractal-semantic-graph.html) | Source code is already a graph, from stories down to syntax | Next to the 2018 AST chapter |
| [Journalism becomes intelligence](https://newsroom.sgit.ai/articles/journalism-becomes-intelligence.html) | Provenance as a graph with dated, sourced edges | Follow the rabbit holes |
| The figures of the graphs books: *the edge set*, *the core graph*, *the evidence trail*, *the altitude ladder* | Existing visualisations, mine, under the same licence | Figures in the chapter |
| Every newsroom article's own graph | A live example of a graph per piece of writing | The chapter's worked example |

## Drawn, not described {#drawn}

The storyboards can now draw graphs: nodes and labelled edges, groups that hold groups, a highlighted path from A to B, and a detective's board with pinned notes and red string. [The storyboard for this article](/storyboards/everything-is-connected.html) uses all of it.

## The brief {#brief}

For the editor. Read `team/editor/role.md`, this article and its storyboard first.

1. **Place the graphs chapter early**, before or with Wardley maps, since a map is a graph with positions. Done when the chapter map orders the two and says why.
2. **Choose the figures** from the list above, and the worked example: one newsroom article's graph, shown and read. Done when the chapter map names them.
3. **Place the 2018 material**: the outline *Graphs*, and the chapters *Dot Language* and *AST* as examples inside this one. Done when the chapter map says where.
4. **Put *Your first graph* in the hands-on part.** Done when the part lists it.
5. **Prepare interview questions** on this: where graphs first entered my thinking (the influences register asks the same); a graph I drew that changed a decision; how to explain "start anywhere" to someone who feels lost. Done when the script is in your `briefs/`.

Questions for me, kept apart:

- Graphs before Wardley maps, or the other way round?
- Which of my graph presentations is the one the 2018 outline meant by "see my presentation on Graphs"?

## What this does not claim {#limits}

- **"Nature is a graph" is a way of seeing**, not a claim in physics; the book should say so.
- **The three meanings of "graph" are the graphs book's classification.** Others classify them differently.
- **The 90% figure is the newsroom's measurement on five articles.** It is not a general law.
- **The figures listed are candidates.** Which ones are in the book is the editor's choice.
- **The detective board is a teaching device.** Real investigations are messier than red string.

If you think in graphs and never called it that, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice, keeping the memo's order and phrases. The argument and the editorial responsibility are mine.

The graphs book quotes are from *Fractal Semantic Graphs* on graphs.sgit.ai, chapter 2, *Why graphs at all* (`v2/books/fsg/content/02__why-graphs-at-all.md` in the graphs repository); "A node connected to nothing is literally meaningless" is from the newsroom's [the graphs books](https://newsroom.sgit.ai/articles/the-graphs-books.html). The Wardley shifts are slides 17 and 18 of [Why Wardley Maps changed how I think](https://docs.google.com/presentation/d/1Rj-EnQaKwt0d9A1zq2pVxi1fLttmsi6spN1MgEBnfPk/). The 2018 quotations are from `5.concepts/graphs.md` in `v1/content/` and from the chapters *Dot Language* and *AST* of book v1.0.0. The other newsroom quotes are from the articles linked, as recorded in their graphs.
