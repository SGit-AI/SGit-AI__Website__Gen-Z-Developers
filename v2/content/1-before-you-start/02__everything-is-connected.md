---
title: "Everything is connected: graphs"
slug: everything-is-connected
part: before-you-start
number: 2
ideas: [a-graph-is-not-a-diagram, the-whodunit-board, a-map-is-a-graph-with-positions, graphs-of-graphs, start-anywhere, the-2018-graph-chapters, code-is-already-a-graph]
answers_2018: [5.concepts/graphs.md, 2.mvp-for-gen-z-dev/content/dot-language.md, 3.technologies/content/AST.md]
sources: [art:everything-is-connected, news:the-graphs-books, book:5.concepts/graphs.md, sb:everything-is-connected, art:follow-the-rabbit-holes, art:where-do-you-land, news:introducing-fractal-semantic-graphs, art:connect-the-dots-backwards, book:2.mvp-for-gen-z-dev/content/dot-language.md, book:3.technologies/content/AST.md, news:code-review-as-a-fractal-semantic-graph]
character: zara
gravity: all
status: draft
---

Think of the board on the wall in a detective story. Photographs pinned up, notes under them, and red string running from one to another. The detective stands in front of it and asks one kind of question, every time: what connects A to B? Who knew whom, who was where, what links these two. Everything on that board is either a thing or a connection between two things.

That board is a graph. If you have followed one of those stories to the end, you already know how to read one.

I have met people for whom a graph is a picture with boxes, or a chart with bars. So let me say early what this book means by the word, because it is one of the most fundamental ideas in it, and it comes back in almost every chapter.

## A graph is a network, not a diagram

A graph is a network: nodes, and the edges that connect them. The first of the graphs books, written with agents on graphs.sgit.ai, puts it in one line: "In this book a graph is a network: nodes and the edges that connect them. Never a chart, never a figure." And its opening sentence says why the edges matter more than the nodes: "A node connected to nothing is literally meaningless."

People mean three things when they say graph. They mean networks, for analysis: who is connected to whom. They mean graph databases, for storing and fetching things fast. And they mean semantics: what something means, which in a graph comes from what it is connected to and how. That is the graphs book's way of dividing the word; others divide it differently. This book uses the first and the third senses, and almost never needs the second.

In 2018 I left an outline for a chapter called *Graphs* and never wrote it. It had four bullets: "Graphs are everywhere", "I've been thinking in graphs for years", "very hard paradigm shift to make", "requires an ability to think in nodes and edges". That is this chapter in miniature. Eight years later the shift still feels hard to explain and easy to show, which is why the storyboards in this book now draw graphs: nodes, labelled edges, a highlighted path from A to B, and a detective's board with pinned notes and red string.

> **For Dinis:** the 2018 outline's first bullet says "See my presentation on Graphs". Which presentation did you mean? If it still exists, the chapter should name it and take from it.

## The whodunit

The detective's board is the easiest way in, and it is why I think your generation will find this chapter easier than mine did. In *Follow the rabbit holes* I said that people underestimate you: you are very good at connecting the dots, very good at finding things, very good detectives. That is my experience, from my family and the young people I have worked with, not a study. But it is what thinking in graphs is: tracing what an unfamiliar thing connects to, trusting a claim because of where it came from, asking what else breaks if this one fails. The graphs book has a line for anyone who thinks this sounds exotic: "you may already think in graphs without ever having called it that."

The board is a teaching device. Real investigations are messier than red string, and so is real software. But the question stays the same, from A to B, and once you see that the question is about edges and not about the boxes, you can ask it of anything.

## A map is a graph with positions

Take the same nodes and the same edges, and now give every node a place on the page that means something. You have a map.

In my talk on why Wardley maps changed how I think, the first two shifts were exactly that: "Its a graph with context", and "When a graph becomes a Map". A Wardley map is a graph where each node has a position on two axes: how visible it is to the user at the top, and how evolved it is, from a brand-new idea to something everyone takes for granted. The positions are what make it a map and not only a graph; the edges are what make it a graph and not only a picture.

The 2018 book said the same thing from the other side, in the chapter *Dot Language*, where I complained that most diagrams in software "are usually not maps": they have components and context but no anchor, no position relative to the anchor, and no consistency of movement. That chapter was about drawing diagrams as text, so that software could draw them and a team could version them like code. Its real complaint was that we build "large interconnected and complex structures without accurate maps", and its best line is one I still believe: "What is crazy is to make decisions based on shadows of reality."

That is why this chapter and *Where do you land?* sit next to each other. One gives you the graph; the other gives it positions and asks where you are on it.

> **For Dinis:** graphs before Wardley maps, or the other way round? The chapter map puts this one first because a map is a graph with positions; the article leaves the order as your question.

## Graphs of graphs

Here is the part that took me longest to see, and that I now cannot unsee. Graphs nest. Zoom into a node and you find another graph inside it, with its own kinds of nodes and its own kinds of edges. Zoom out and the whole graph is one node in a bigger one.

The newsroom's introduction to what I call fractal semantic graphs puts the consequence in two sentences: "There is no top and no bottom. There is only the altitude you happen to be looking from, and how much definition you choose to load at it." A law is a node in a graph of laws. Open it and it is a graph of articles. Open an article and it is a graph of the terms it uses. Each level has its own vocabulary, and none of them was made to match the others. What connects them is that each one is still a graph.

In a way, you can see nature like this too: a system, the molecules in it, the particles in those, everything connected to everything else, and groups of groups forming the layers we think in. I want to be clear that this is a way of seeing, not a claim in physics. But it is how I view the world: it is made of connections. This connects to this, which connects to that. Groups of groups are the natural abstraction layers, and abstraction layers are how we think.

It is also why provenance is a graph. Where a claim came from is a chain of edges back to its source, and the newsroom's rule for a record is that it should be "not a pile of articles, but a graph whose every edge has a date and a source". A chain that ends in a rumour is a finding too. *Facts, evidence and the record* is built on that.

## Code is already a graph

The 2018 book had a second chapter that was a graph without saying so. *AST* opened by calling an abstract syntax tree "a graph representation of source code", and it told you that if you could "see code or raw data as a graph", you would have made a paradigm shift that would help you across your career. I still think so, and I now think it goes further than I said then.

Source code is the best example of a fractal graph that I know, because the layers are not an interpretation; they are a fact about the thing. At the top is a person trying to do something. Below that, the features and flows. Below that, the components people draw when you ask for the architecture. Then the classes, then the methods and the calls between them, then the syntax tree, and on down if you want to. Each layer is a graph with its own vocabulary, and you change universe when you step from one to the next.

What changed since 2018 is that naming the nodes and the edges is now cheap. A language model can read a function and say what it does, and propose the edge between two nodes faster than a person can type it. So a change to the code can be read at every layer, not only as lines. A refactor is a change that moves the bottom layers and leaves the stories at the top still. A bug is a story that stopped holding, and its fix is visible at the top as that story holding again. The blast radius of a change is the climb from the methods it touched up to the stories that can reach them, and you can read it before anyone runs anything.

This is the only honest answer I have to the characteristic failure of AI-generated code: the change made in one place that breaks something three packages away. In a text diff that is invisible. In the layered graph it is a changed node whose upward reach includes a command the author never looked at. In the newsroom I worked this through on a real tool, the sgit command line, read as layered graphs with nothing run: one commit that was 75 lines added and 7 removed in three files turned out to reach nine of the tool's 72 commands and six of its eleven user stories. The stories were hand-written, the example runs nothing, and it is published as a vault with the read key on the page, so you can check it. The technique underneath it, following the call tree from one method and writing out only that code, is one I used for code review on the O2 Platform more than a decade ago, and described in the 2018 *AST* chapter as method streams. It is back, and it is one script now.

If you are the kind of person who wants to own code in production and answer for it, this is your chapter as much as the detective's board is. If you are not, keep the shape: layers, each a graph, and a change you can read at every one.

## Start anywhere

Here is the thing about graphs that I most want you to take from this chapter, because it is about how you feel when you look at everything there is to learn.

A graph has no front page. It has no top, so there is no right place to begin. Whatever node you start from, the edges take you to the rest. It does not matter where you start; it matters that you start. It does not matter, in a way, whether you are going straight in the right direction; it matters that you get movement. You start to learn, you start to connect the dots, and the connections do the rest.

So when it feels like too much, and it will, pick a node. Any node. A tool you were shown, a problem your team keeps hitting, a question you cannot let go of. Start there and follow one edge. Then another. *Connect the dots backwards* says that your path will only make sense afterwards, and this is why: a path is a walk through a graph, and the graph does not care where the walk began.

The second half of this book has a hands-on chapter, *Your first graph, built by hand*, where you draw one of your own. You do not need it to read on. You need only to remember, when the word comes up, that a graph is nodes and the edges between them, that everything in this book connects to something else in it, and that you can start wherever you are.
