---
title: A tiny agent loop
slug: a-tiny-agent-loop
part: hands-on-2026
number: 26
ideas: []
answers_2018: []
sources: [art:lenses-roles-and-loops, news:how-i-work-with-claude, news:re-anchoring-agent-behaviour-policies]
character: zara
gravity: explorer
status: draft
---

By the end of this chapter you will have run an agent loop by hand, with yourself as the program around the model, and you will know why a long chat forgets. The loop is the one *Lenses, roles and loops* described, and the habits at the end are the newsroom's, from *How I work with Claude* and *Re-anchoring*.

An agent is a role on a loop with a goal. Fundamentally it is a task: do this; then, are we done yet, or do we need to continue? And rinse and repeat. Made precise, an agent is a model plus instructions, tools, a loop and a rule for stopping. The "personality" is the instructions. "Are we done?" can be the model's own judgement, a test that passes, a budget that runs out, or a person.

When you ask a question, the model does not have to answer. It can return a request instead: run this web search, call this weather service, read this file. The model never runs the tool. It writes a structured request, a tool name and its arguments, and the program around it, often called the harness, decides whether to run it, runs it, and adds the result to the conversation. The next request carries your question, the tool call and its answer, and the model writes from that, or asks for another tool. That is where the control lives.

## Run it by hand

The simplest way to see this is to be the harness yourself, with a chat window and a text file. A role, the article says, is almost a raw model plus a role description and a question, so that is what you build.

1. **Write the role.** A short file, `role.md`, as *How I work with Claude* describes it: its role, its responsibilities, what it may do, what it must not do, and where it writes. Give it one tool, in words: it may ask you to read a file for it, and when it asks, it stops and waits.
2. **Set the goal and the stopping rule.** One task the role can finish in a few rounds, and one sentence that says what done looks like.
3. **Start the session with the role.** Use the newsroom's starter prompt for an agent session: read the role file and the policy, then "Reply with: your role in three lines, what you may do, what you must not do, and where you write your output. Then wait for the first task."
4. **Give the task, and play the program.** When the model asks for the file, you open it and paste the contents back. That is the tool call and its result. Then it answers, or asks for another.
5. **Stop when the rule says.** Not when the model sounds finished. Then ask the newsroom's ending question: list what you changed, what you checked and against which source, and what you are not sure of.

After a few rounds you have watched the request instead of an answer, the result going back in, the loop going round, and the moment it decides it is done. It is not magic, and once you see the loop you can set its constraints.

> **For Dinis:** the article asks for "a page of code or a no-code version". This is the no-code version. The page of code needs your choice of language and tool, and whether it lives on the page or on the site, where it can be kept current.

## Why it forgets

The model remembers nothing between requests. Every request carries the whole conversation: your instructions, everything said so far, every tool result. That is why there is a context window, and why your hand-run loop got longer every round. When a conversation gets too long, the providers compress it: the older part is replaced by a summary the model writes, a lower-resolution version with only the key concepts. What the summary leaves out is gone from the session unless it is in a file.

The newsroom measured this on itself. The session that runs its site was summarised eighteen times in a month, each time keeping on average 1.7% of what it replaced. One session on one site, not a law; enough to change how you work. On 9 October two emails drafted by one of my agents went out in my voice, against a rule that had been written down four times, and one of the reasons was that the rule fell out of the agent's context when the conversation was summarised.

## The habits

Three habits follow, and they are the ones the newsroom runs under.

**One session per topic, with a name.** A thread is the model's frame of reference. Put three projects in one and it will borrow a name from one and a decision from another, because it is using everything in front of it. So: one topic per session, named "project | what we are working on", with an @ in front of an agent's name so you can see you are talking to a role with a job.

**Rules in a file, not in the chat.** A rule given only in conversation has to win every summary, and nothing tells you when it does not. Put the rules in a file and have the harness print it back after every summary. "The rules are restored, not remembered." The cheapest version is a line in the file your tool reads at every start, telling the agent to read its policy; the bluntest is typing "read your instructions again". The newsroom's recipe has six steps: write the rules as a short policy file, each with what enforces it; re-anchor after every compaction; add a canary, a short report every few answers computed from the transcript, so you notice when it stops appearing; give the person two commands, status and reload; measure one rule in the report; and move the rules that matter most from an expectation to a reader or a gate. Re-anchoring enforces nothing. A rule in view is still an expectation.

**Memory is what the session reads, so curate it.** When something comes back wrong, fix the brief or the file it came from, not only the text in front of you, so the next session does not repeat it. "Nothing is remembered by the model between sessions. Everything is remembered by the files." The line is the newsroom's, as *Lenses, roles and loops* quotes it, and your hand-run loop is where you will first believe it.
