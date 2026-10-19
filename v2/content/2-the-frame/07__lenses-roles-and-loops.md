---
title: Lenses, roles and loops
slug: lenses-roles-and-loops
part: the-frame
number: 7
ideas: [a-prompt-is-a-lens, a-role-is-a-model-with-a-description, tools-changed-everything, the-model-remembers-nothing, long-chats-are-compressed]
answers_2018: [3.technologies/content/ml-ai.md]
sources: [art:lenses-roles-and-loops, sb:lenses-roles-and-loops, news:how-i-work-with-claude, news:memory-is-not-a-spectator-sport, news:re-anchoring-agent-behaviour-policies, news:replicating-the-agentic-inbox, art:gen-zx-developers, book:3.technologies/content/ml-ai.md]
character: zara
gravity: all
status: draft
---

*What generative AI is* explained what a language model is. This chapter is about what happens when you use one, from a single prompt to an agent that runs for hours. It is very important to understand this workflow, because once you understand it you see that it is not magic. And that is why you want this level of understanding: so that you can be the one who defines the constraints and how it works. Whether you are leaving university or leaving twenty-five years of a profession to start a company, this is the chapter to understand before you build anything on these tools.

## A prompt is a lens

The power of a language model starts with the prompt. The prompt lets you customise the output, which is why a model can speak to so many audiences so easily, and why it can translate. From a model's point of view, translating from one language to another is no different from translating for a particular topic, region, audience, stakeholder or persona. Explain this to me as if I were a teenager. Explain it as if I were a musician. Explain it with medical references. Explain it in football terms.

The model can do that because it has the frame of reference. It holds all those worlds inside it, and the prompt puts the right lens in front of the idea. The analogy is the reason someone understands something.

Take one idea, recursion, and put it through five lenses. For a teenager, a meme of a meme. For a musician, a round, sung over itself. For a doctor, cells dividing into cells. For a football fan, the replay of the replay. In Portuguese, *recursividade*. Same idea, five ways in, and to the model the fifth is no different from the other four.

It is the same with people who say they are not good at maths. Watch them in their day-to-day and they do a huge amount of maths: rotas, budgets, stock levels. They are just not good at the kind of maths we decided was maths: sums, calculus, trigonometry, algebra. Mathematics is much more than that. It was the lens that was wrong, not the person, and that is why this book keeps showing multiple lenses. *One idea, five lenses* in the hands-on part lets you try it on an idea of your own.

## A role is a model with a description

On the site that made this book there is an editor, a publisher, a journalist, a reviewer, and now a librarian; elsewhere I have had a developer and a designer. Each of those roles is, in essence, almost a raw model plus a role description and a question. That is it.

The role description is the lens: who you are, what you care about, what you refuse, how you work. Every role on the site has a `role.md` that says exactly that. In the newsroom, in *How I work with Claude*, I put it this way: an agent is a session with a particular focus, and in practice it is three things: a few documents that explain the project, a `role.md` for this agent, and a session that reads those before it does anything, named for the role. That is enough to start. The same model sits behind every role; what changes is the description and the question. If your company's first team is a set of agents, this is what each of them is, and *Controlling your agent: RiskMandate* is about what each of them is allowed to do.

## An agent is a loop with a goal

And an agent is that role on a loop, with an objective. Fundamentally the agent is simply a task: do this; then, are we done yet, or do we need to continue? And rinse and repeat. They are not that difficult, which is why the better you understand them, the better your workflows will be.

"An agent is just a loop" is a simplification, and I want to be straight about that. Good agents add planning, checks and limits; the loop is the skeleton, not the whole animal. Made precise: an agent is a model plus instructions, tools, a loop and a rule for stopping. The "personality" is the instructions. "Are we done?" can be the model's own judgement, a test that passes, a budget that runs out, or a person. *A tiny agent loop*, in the hands-on part, is a page of that, so you can see the skeleton move.

## Tools changed everything

In 2018 I told you that as a developer you would soon be asked to write code that integrates with machine learning services: voice, image recognition, domain-specific analysis. The direction was right and the picture was backwards. Today the model asks for the service.

The first chat assistants relied on their training, which is always fundamentally a compression of reality. Imagine having all of Google put inside the model: it was impossible for it to know everything, and what it knew stopped at the day its training ended. Compression is a metaphor, a useful one; what a model knows is learned patterns, not a stored copy. But the limit was real.

What changed is that we gave the models tools, and let them iterate with those tools. This is a very important concept to understand. When you ask a question, the model does not have to answer. It can return a tool call instead: can you make these calls for me? Can you call this weather service? Can you run this web search? Can you read this file? Those are the capabilities we gave that agent, or that session. The program around the model makes the calls, gets the answers, puts it all together, and sends it in the next request. The next request has your original question, plus the tool calls, plus their answers, and the model writes its answer from that, or asks for another tool, and it continues.

Picture it with a made-up question: is it raining in Lisbon? The model answers with a request: call the weather service. The program calls it and gets "light rain". It sends everything back: the question, the call, the result. Now the model answers: take an umbrella. Two requests for one answer, and the second holds everything the first did, plus the tool's result.

The point that matters most is this: the model never runs a tool. It writes a structured request, a tool name and its arguments. The program around it, often called the harness, decides whether to run it, runs it, and adds the result to the conversation. That is where the control lives, and it is why *Controlling your agent: RiskMandate* puts the rules there and not in the model's good intentions.

The dates, as commonly recorded, show how fast this moved. ChatGPT launched on 30 November 2022 with no tools at all. Plugins arrived in March 2023, and developers could give models their own functions from the middle of 2023. By November 2024 there was an open standard for connecting tools to any model, the Model Context Protocol. The agents of 2026 are that loop, with many tools, running for a long time.

> **For Dinis:** the first time you saw a model ask for a tool instead of answering. The article's interview script asks for it, and it would open this section better than the dates do.

## It remembers nothing

I think a lot of people have not fully pictured this: the longer your chat, the more the model has to process, every time. There is no memory. There is a cache that saves some work, but fundamentally the model starts from the prompt it receives, which is why it has to receive all of it: your instructions, the whole conversation so far, the tool results. That is why there is a context window. There is only so much you can give a model to process and keep in that short-term memory at once.

Made precise: every request is independent. The model is called afresh each time; the application around it keeps the conversation and resends it. Prompt caching makes a repeated beginning faster and cheaper; it does not give the model memory. And when an assistant "remembers" you, it is saved notes being put back into the prompt.

## Long chats are compressed

So the next step the providers took was compression. When a conversation gets too long, it is replaced by something like a zip file, or a lower-resolution version of your conversation, with only the key concepts, and that is what gets fed into what follows. That is why a long chat loses details, and why a model sometimes loses a specific piece of information. In a way it is not that it does not remember: that information is simply not in what it was given any more. What the summary leaves out is gone from the session unless it is in a file.

The newsroom measured it. The session that runs the sgit.ai site was summarised eighteen times in a month, all automatically. Each time it started from about 780,000 to 800,000 tokens of context and kept 9,000 to 19,000: on average 1.7% of what it replaced. That is one session's measurement, on one site, over one month; how each product compresses differs and changes. The principle, that details can drop out, does not.

The newsroom's answer, in *Re-anchoring: keeping an agent's rules alive through every summary*, is to keep the rules in a file that is printed back after every summary: "The rules are restored, not remembered." And *Memory is not a spectator sport* puts the whole principle in one line: "Nothing is remembered by the model between sessions. Everything is remembered by the files."

## Many focused threads

That is why my recommendation is to have lots of separate threads, which is what I do most of the time: lots of mini agents, each with a name, each told what it focuses on. A thread is the model's frame of reference: everything in it is context for the next answer. Put three projects in one thread and the model starts to mix them, borrowing a name from one, a decision from another, an assumption from a third. It is not being careless. It is doing exactly what you asked, using everything in front of it. One topic per session keeps the frame of reference small and right. When the topic changes, open a new session.

Name them, too. A session you cannot find is a session you will recreate, badly. My pattern is the project, a pipe, and what we are working on; agent sessions get an @ in front of the role: `@briefs`, `@inbox`, `@drafts`. The @ tells me at a glance that I am talking to an agent with a defined job.

It is exactly how the agentic workflow behind my email runs, which *Your own newsroom and inbox* walks through. One session per role: one reads the mailbox, one writes drafts, one keeps the contacts, one researches a person before a first email. Every message between the agents is a file in a vault, so the conversation between them is a record from the first message. And every outgoing email is a draft that a person reads and sends. That rule never changes: nothing is sent by an agent. The sessions talk through files, never through memory, and each one holds only what its one job needs.

Not magic: a lens, a role, a loop. Understand that, and you are the one who sets the constraints.
