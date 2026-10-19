---
title: Your first graph, built by hand
slug: your-first-graph
part: hands-on-2026
number: 24
ideas: []
answers_2018: []
sources: [art:everything-is-connected, "graphs.sgit.ai, Fractal Semantic Graphs, 01__a-node-is-just-a-node.md", "graphs.sgit.ai, Fractal Semantic Graphs, 02__why-graphs-at-all.md", "graphs.sgit.ai, Fractal Semantic Graphs, 03__every-edge-is-a-verb.md", "graphs.sgit.ai, Fractal Semantic Graphs, 15__your-first-graph.md"]
character: zara
gravity: explorer
status: draft
---

By the end of this chapter you will have drawn a graph of something you know: a text file of forty-odd lines, an answer to a question somebody keeps getting wrong, and a list of things nobody knows. A text editor is enough for the afternoon, and you will not need a graph database; if somebody tells you otherwise in the first month, they are solving a different problem from yours. The steps are from chapter 15 of *Fractal Semantic Graphs*, the first of the graphs books on graphs.sgit.ai, and the rules behind them are from its first three chapters.

*Everything is connected* said what we mean by a graph: "a network: nodes and the edges that connect them. Never a chart, never a figure." It also said you may already think in graphs without ever having called it that. What is rare is doing it deliberately, with rules.

The most common way this fails is picking a subject instead of a question. "Let's map our architecture" is a subject: it has no stopping point, no test for correctness and no audience, so it becomes a diagram nobody reads. A good first question has three properties: somebody actually asks it, the current answer requires a person to remember something, and the answer changes when facts change. One of the book's examples is "If this service goes down, who has to be told?" Yours does not have to be about software. Anything where the answer lives in a few people's heads and is wrong twice a year will do. Write it down; you will be tempted to widen it by Wednesday.

## The afternoon, in seven steps

1. Write your question at the top of a file.
2. List the things the question touches. Not types: actual things, by name. Aim for fifteen to forty. If you have four, the question is too small. If you have three hundred, you picked a subject.
3. Write the edges as sentences, in full, one per line. The book's own first line is "the payments service is owned by the platform team". Sentences first, always: you are being forced to name the verb, and naming the verb is the whole discipline.
4. Turn each sentence into a verb and its inverse: `owned_by` and `owns`, `reads` and `read_by`, `contains` and `contained_in`. If the inverse is just the same sentence backwards, you have one relationship where you thought you had two.
5. Read your paths aloud. Start at any node and walk three or four hops. If the sentence does not survive being said out loud in front of somebody who knows the business, the edges are wrong. Fix them now.
6. Ask your question of the graph, by hand, tracing with a finger. If tracing produces an answer somebody would have got wrong from memory, you have something. If it produces nothing, look at which hop was missing: that is your first real finding.
7. Write down what you could not answer. Not in your head. As nodes, with names.

That is a complete first graph, and the book says it is more than most organisations have.

## Why the rules are what they are

Three rules from the first three chapters explain why the steps come in that order.

A node connected to nothing is meaningless. Draw a box and write Review in it: you have a word in a box, not a review. Nothing inside it says whether that review took two minutes or two weeks. Meaning, the book argues and I agree, is not declared but discovered through the connections, and confidence in it should grow with how richly, and how independently, a node is connected. That is why step two lists things and step three connects them before anybody says what anything is.

Every edge is a verb, and the generic association edge is banned. The book quotes a voice memo of mine from June 2026: "You can never have relates-to, because relates-to is meaningless, two things always relate to each other. The more granular the edge, the better the query you can write." An edge with no verb carries no constraint, so it cannot narrow a traversal. That is why step four exists, and why the inverse gets its own name: a system has one owner, an owner has forty systems, and the two directions have different fan-out.

Never render the whole graph; render the result of a query. Almost everyone who does this produces the blob, the hairball that shows everything and therefore nothing, and then prunes it. The book calls that a rendering failure mistaken for a modelling failure: rich nodes are good; solve the picture at query time, never by deleting relationships. That is why step six asks a question of the graph rather than drawing all of it, and why you show somebody one node with its neighbours.

## The first week, and the agent

Five moves pay back most, in order. Give every node a short identity that never changes, because names change. Put the file in version control, because the diff is the review surface. Add the absences you have been carrying: every "we don't know who owns that" becomes a node: the step people skip, and the one that gives the missing dots names. Point at two or three anchors, a published standard or a library at a pinned version, with a verb that says how strongly: `similar_to`, not `is_a`. And write down one rule for a type, as a required pattern of paths, then see what fails. The failures are the point.

Most readers will hand some of this to a language model, so here is the version to hand it, from the same chapter. Give it the vocabulary before the task: asked to "build a graph" with no vocabulary, it will invent one, and the book says it will invent a generic association edge within about five nodes. Ask for a proposal, not a commitment: the model proposes a graph and you validate it. Make it anchor: every node it emits carries the sentence it came from, verbatim, and you check the quotes exist. And make it emit absences: when it cannot determine something, it says so as a node; do not ask, and it will fill the gap.

*Everything is connected* ended with the line I want you to start from: "It does not matter where you start; it matters that you start." A graph has no front page. Pick the question, open the file, and write the first sentence.
