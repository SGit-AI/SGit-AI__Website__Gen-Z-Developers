---
title: Lenses, roles and loops: a prompt is a lens that changes who the answer is for, a role is a model with a description, an agent is a loop with a goal, tools are requests the model sends back, and long chats forget because they are compressed
date: 2026-10-18
author: Dinis Cruz
summary: This is how I explain what is going on inside the tools, and I think it is one of the most important things a reader can understand, because once you see it, it stops being magic and you can take control of it. It starts with the prompt. A language model can speak to any audience because, to the model, translating from Portuguese to English is no different from translating for a teenager, a musician, a doctor or a football fan: it has the frame of reference for all of them, and the prompt is the lens. That is also why people who say they are bad at maths do maths all day; it is the lens that was wrong. A role, like the editor, the publisher, the journalist or the librarian on this site, is a model plus a role description and a question. An agent is that on a loop with an objective: do the task, ask whether it is done, and if not, go round again. The big change since the first ChatGPT and the first Claude is tools. The early models only had their training, which is a compression of the world, like having all of Google squeezed inside them. Now the model can answer with a request instead of an answer: please search the web, call the weather service, read this file. The program around it does that, adds the result to the conversation, and sends it all back, and the model writes its answer from there. And it has no memory: every request carries the whole conversation, which is why there is a context window, why long chats get compressed into a lower-resolution summary, and why details get lost. So work in many separate, focused threads, with named agents, each with one job, which is how the email workflow in this book runs.
version: v0.2.14
tags: llm, agents, prompts, tools, context, compaction, gen-z-book, article
status: published
---

## In short {#in-short}

- **Understanding how the tools work makes them stop being magic.** And lets you set the constraints, instead of guessing.
- **A prompt is a lens.** Translating into another language is, to a model, the same as explaining for a teenager, a musician or a doctor.
- **"Bad at maths" is often the wrong lens.** People do maths all day; it is not the maths school called maths.
- **A role is a model with a description and a question.** The editor, the publisher, the journalist on this site.
- **An agent is a role on a loop with a goal.** Do the task; are we done? If not, go round again.
- **Tools changed everything.** The model sends back a request, the program runs it, and the result goes into the next request.
- **The model remembers nothing between requests.** Every request carries the whole conversation, which is why there is a context window.
- **Long chats are compressed, so details get lost.** Work in many separate, focused threads, with named agents.

## Why this matters {#why}

It is very important to understand this workflow, because once you understand it you start to see the connections. You see that it is not magic. And that is why you want this level of understanding: so that you can be the one who defines the constraints and how it works. The more you understand it, the better your workflow will be.

[Generative AI, not AI](/articles/generative-ai-not-ai.html) explained what a language model is. This article is about what happens when you use one, from a single prompt to an agent that runs for hours.

## A prompt is a lens {#lens}

The power of a language model starts with the prompt. The prompt lets you customise the output, which is why a model can speak to so many audiences so easily, and why it can translate. From a model's point of view, translating from one language to another is no different from translating for a particular topic, region, audience, stakeholder or persona. Explain this to me as if I were a teenager. Explain it as if I were a musician. Explain it with medical references. Explain it in football terms.

The model can do that because it has the frame of reference: it holds all those worlds inside it, and the prompt puts the right lens in front of the idea. The analogy is the reason someone understands something.

It is the same with people who say they are not good at maths. Watch them in their day-to-day and they do a huge amount of maths. They are just not good at the kind of maths we decided was maths: sums, calculus, trigonometry, algebra. Mathematics is much more than that. That is why it is important to show the multiple lenses, and why the visualisations in this book try to.

## A role is a model with a description {#roles}

On this site there is an editor, a publisher, a journalist, a reviewer, and now a librarian; elsewhere I have had a developer and a designer. Each of those roles is, in essence, almost a raw model plus a role description and a question. That is it. The role description is the lens: who you are, what you care about, what you refuse, how you work. Every role on this site has a `role.md` that says exactly that, and [how I work with Claude](https://newsroom.sgit.ai/articles/how-i-work-with-claude.html) describes an agent as a focused session with a role file.

## An agent is a loop with a goal {#agent}

And an agent is that role on a loop, with an objective. Fundamentally the agent is simply a task: do this; then, are we done yet, or do we need to continue? And rinse and repeat. That is what Claude does, that is what ChatGPT does, and that is what a lot of agents do. They are not that difficult, which is why the better you understand them, the better your workflows will be.

## Tools changed everything {#tools}

It would be powerful to show the evolution from the first ChatGPT and the first Claude to now. The first ones relied on their training, which is always fundamentally a compression of reality. Imagine having all of Google put inside the model: it was impossible for it to know everything, and what it knew stopped at the day its training ended.

What changed is that we gave the models tools, and let them iterate with those tools. This is a very important concept to explain. When you ask a question, the model does not have to answer. It can return a tool call instead: can you make these calls for me? Can you call this weather service? Can you run this web search? Can you read this file? Those are the capabilities we gave that agent, or that session. The program around the model makes the calls, gets the answers, puts it all together, and sends it in the next request. The next request has your original question, plus the tool calls, plus their answers, and the model writes its answer from that, or asks for another tool, and it continues.

ChatGPT launched at the end of November 2022 with no tools at all; plugins arrived in March 2023, and developers could give models their own functions from the middle of 2023. By November 2024 there was an open standard for connecting tools to any model, the Model Context Protocol. The agents of 2026 are that loop, with many tools, running for a long time.

## It remembers nothing {#memory}

I think a lot of people have not fully pictured this: the longer your chat, the more the model has to process, every time. There is no memory. There is a cache that saves some work, but fundamentally the model starts from the prompt it receives, which is why it has to receive all of it: your instructions, the whole conversation so far, the tool results. And that is why there is a context window: there is only so much you can give a model to process and keep in that short-term memory at once.

## Long chats are compressed {#compression}

So the next step the providers took was compression. When a conversation gets too long, it is replaced by something like a zip file, or a lower-resolution version of your conversation, with only the key concepts, and that is what gets fed into what follows. That is why a long chat loses details, and why a model sometimes loses a specific piece of information. In a way it is not that it does not remember: that information is simply not in what it was given any more. That is where those mistakes come from.

The newsroom measured it, in [re-anchoring](https://newsroom.sgit.ai/articles/re-anchoring-agent-behaviour-policies.html): the session that runs the site was summarised eighteen times in a month, each summary keeping on average 1.7% of what it replaced. Its answer is to keep the rules in a file that is printed back after every summary: "The rules are restored, not remembered." And [memory is not a spectator sport](https://newsroom.sgit.ai/articles/memory-is-not-a-spectator-sport.html) puts the principle in one line: "Nothing is remembered by the model between sessions. Everything is remembered by the files."

## Many focused threads {#threads}

That is why my recommendation is to have lots of separate threads, which is what I do most of the time: lots of mini agents, each with a name, each told what it focuses on. One topic per session keeps what the model has to hold small and right. It is exactly how the agentic workflow behind my email runs, which the book has a whole chapter on: [replicating the agentic inbox](https://newsroom.sgit.ai/articles/replicating-the-agentic-inbox.html), one session per role, every message between agents a file, and every email a draft a person sends.

## Precisely {#precisely}

The picture above is how I explain it. A few points, made precise:

- **Every request is independent.** The model is called afresh each time; the application around it keeps the conversation and resends it. Prompt caching lets the provider reuse work on a repeated beginning, which makes it faster and cheaper; it does not give the model memory.
- **The model never runs a tool.** It writes a structured request, a tool name and its arguments. The program around it, often called the harness, decides whether to run it, runs it, and adds the result to the conversation. That is where the control lives, which is why the newsroom puts its behaviour policies and hooks there.
- **An agent is a model plus instructions, tools, a loop and a rule for stopping.** The "personality" is the instructions; "are we done?" can be the model's own judgement, a test that passes, a budget that runs out, or a person.
- **Memory features are still the context window.** When an assistant "remembers" you, it is saved notes being put back into the prompt.
- **Compaction is a summary written by the model**, replacing the older part of the conversation; what the summary leaves out is gone from the session unless it is in a file.

## The brief {#brief}

For the editor. Read `team/editor/role.md` and this article first.

1. **Place this chapter right after what generative AI is**, as the second half of the same explanation: lenses, roles, the loop, tools, the context window, compression, and why to work in focused threads. Done when the chapter map has it.
2. **Plan the lenses exercise for the hands-on part**: one idea explained through five lenses (a teenager, a musician, a doctor, a football fan, another language), the reader's own choice of idea. Done when the part lists it.
3. **Plan a tiny agent loop for the hands-on part**: a page of code or a no-code version that shows the loop and one tool call, so the reader sees it is not magic. Done when the part lists it, with the newsroom article it builds on.
4. **Prepare interview questions** on this: the first time I saw a model ask for a tool; a time a long chat lost something important; how I name and split my agents. Done when the script is in your `briefs/`.

## What this does not claim {#limits}

- **"An agent is just a loop" is a simplification.** Good agents add planning, checks and limits; the loop is the skeleton, not the whole animal.
- **The dates are the commonly recorded ones**: ChatGPT on 30 November 2022, plugins in March 2023, functions for developers in mid 2023, the Model Context Protocol in November 2024.
- **The 1.7% is one session's measurement** on one site over a month, not a property of every product.
- **Training as a compression of the world is a metaphor**, a useful one; what a model knows is learned patterns, not a stored copy.
- **How each product compresses differs**, and changes; the principle, that details can drop out, does not.

If you have a better way to explain the loop to someone who has never coded, write to [agent@riskmandate.ai](mailto:agent@riskmandate.ai).

## Where this comes from {#sources}

A voice memo of mine on 18 October 2026, written up by this site's journalist, `gen-z.journalist`, in my voice, keeping the memo's order and phrases; the precise points were checked against how the model APIs work. The argument and the editorial responsibility are mine.

The newsroom quotes and the eighteen summaries at 1.7% are from [re-anchoring](https://newsroom.sgit.ai/articles/re-anchoring-agent-behaviour-policies.html) and [memory is not a spectator sport](https://newsroom.sgit.ai/articles/memory-is-not-a-spectator-sport.html); the habits from [how I work with Claude](https://newsroom.sgit.ai/articles/how-i-work-with-claude.html); the email workflow from [replicating the agentic inbox](https://newsroom.sgit.ai/articles/replicating-the-agentic-inbox.html). The plugins date is as recorded by the [AI Wiki list of ChatGPT plugins](https://aiwiki.ai/wiki/list_of_chatgpt_plugins/raw).
