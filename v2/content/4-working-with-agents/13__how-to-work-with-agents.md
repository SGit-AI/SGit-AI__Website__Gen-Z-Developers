---
title: How to work with agents
slug: how-to-work-with-agents
part: working-with-agents
number: 13
ideas: [an-agent-is-a-session-with-a-focus, brief-is-the-unit-of-work, omnichannel-programming, every-mistake-added-a-rule, a-correction-becomes-a-rule]
answers_2018: [4.life-patterns/workflows.md, 5.concepts/agile-and-kanban.md, 3.technologies/content/ide.md, 5.concepts/design.md, 5.concepts/changes.md]
sources: [news:how-i-work-with-claude, news:the-agents-write-too, news:the-librarians-daily-brief, art:write-it-as-an-article, news:the-briefs-so-far, news:brief-the-agent-too, news:omnichannel-programming, news:every-mistake-added-a-rule, news:re-anchoring-agent-behaviour-policies, news:how-the-voice-works, book:4.life-patterns/workflows.md, book:5.concepts/agile-and-kanban.md, book:3.technologies/content/ide.md, book:5.concepts/design.md, book:5.concepts/changes.md]
character: sam
gravity: villager
status: draft
---

In 2018 I wrote a chapter that began "We need to talk about your IDE!" The IDE, I said, is like a car in a race that you are the driver of, and the more time you spend looking after it, the better a programmer you will be. I still think that. But the thing to look after has moved. The editor is now one channel among several. What decides the quality of the work is the session, the brief you hand it, and the rules it runs under. This chapter is about those three, after about a year of working with agents every day.

If you hire people, read it as a description of what to look for. The habits below leave evidence: named sessions, written briefs, a short rules file, a record you can read. A candidate who has them can show you. A candidate who says they are "good with AI" and cannot show any of this is describing a chat window.

## An agent is a session with a focus

It sounds grander than it is. An agent is a session with a particular focus: a few documents that explain the project, what it is, where it is going, what has been decided; a `role.md` for this agent, with what it may do, what it must not do, and where it writes; and a session that reads those before it does anything, and is named for the role. That is enough to start.

The most important habit is the simplest one: one session per topic. A thread is the model's frame of reference, and everything in it is context for the next answer. Put three projects in one thread and the model starts to mix them, borrowing a name from one and a decision from another. It is not being careless. It is doing exactly what you asked, with everything in front of it. When the topic changes, open a new session.

Name every session, because a session you cannot find is a session you will recreate, badly. My pattern is the project, a pipe, and what we are working on: "sgit.ai | website development". Agent sessions get an @ in front of the role: @briefs, @inbox, @librarian.

Once there are several agents, two problems arrive, and both are solved by writing. The agents learn things the others should know, so each one writes lessons: one thing learned, the evidence for it, which agents it applies to, and whether it still holds. Every agent reads the lessons file at the start of its next session. That is memory in its plainest form. And the agents do so much that I need a debrief: what was done, what is open, what went wrong, with the commits to check it against. One afternoon two of my newsroom's agents released the same version number within minutes; one push was refused and became the next number. Nothing was lost, and nobody would have known, unless someone wrote it down. So someone did, as a lesson: fetch before you take a version number.

The last piece is a daily brief. I work on many threads at once and follow tangents, so I lose threads; one day I could not remember which cloud session had built something. The answer is an agent, the Librarian, that reads everything that happened yesterday across every repository and writes one page before I start: what needs me, what happened, the agents' debriefs, the threads worth picking up, and at most three suggestions for where to put my attention today. It reads everything and writes only its own folder. It flags; others fix.

> **For Dinis:** when the article was written the Librarian did not run yet; the sources existed and the brief was written. Does it run now, and what did the first weeks of briefs change about how you start the day?

The 2018 draft *Workflows* had a bullet I never wrote up: thinking in systems and workflows "is actually how most programming works". It is, and now the workflow is made of sessions.

## The brief is the unit of work

When I want an agent to do something substantial, the instruction I give it is usually a voice memo, and a voice memo is a terrible instruction. It is in the order I thought it, it mixes the idea with the task, it does not say what already exists, and it leaves the agent to guess which parts are decisions and which are thinking out loud.

An article fixes most of that, because writing one is research. Before the first article on this book's site could be written, the journalist had to read the repository, the vault, the two 2018 repositories and the newsroom's guide to its voice, and count things: how many files the book has, how many are outlines, what the Leanpub build included. The agent that reads the article afterwards starts from that record, not from my memo. Six newsroom articles and two build notes were enough for one session to build this book's site, its first release, with the 2018 book imported, the map, the roles and the vault.

A good brief says four things: what is asked, what exists, what remains, and what done looks like. When the newsroom's writer agent audited the briefs the newsroom had published about itself, every open one got a session brief in that shape: what to read first, the first deliverable, how to know it is done. A session can start from that paragraph alone. And an article is something I can read. I can correct it, argue with it, or say "yes, that", before any work starts. A list of tasks does not invite that; an argument does. The 2018 draft *Design* had a line I never expanded, about not having time to write a short letter and so sending a long one. The brief is the short letter. It costs more, and it is where the thinking happens.

There is a newer route for a brief. More and more, the people I advise read through an agent. A founder I mentor had agents chasing ever more sophisticated threats while the project slowed. I sent them an article of mine on tiers of attacker. They gave it to their agent, which came back with, in effect: we have been designing against states and we have not done backups; aim at organised crime for money. The founder agreed and briefed the other agents. I could not have written that conclusion, because I did not know the state of their backups. Their agent did. So some of what I write now has a second package, a brief for the reader's agent: plain text, the sources, who the agent works for, and in every one, "do not take this at face value".

## One shared state

I no longer program in one place. I brief in a voice memo while walking. An agent works on it in the cloud and pushes. I look at the result on my phone and reply by voice with what to change. On the computer I run the tests. On GitHub I read the diff. On an iPad, in a meeting, I check the same page again.

Retail has a word for this. In 2011 Darrell Rigby wrote in Harvard Business Review that successful companies would engage customers through omnichannel retailing, and the distinction that made the word useful is the one I want to borrow. A multichannel retailer has a shop, a website and a catalogue, each with its own stock and its own customer record. An omnichannel retailer has one customer, one basket and one stock, and the channels are ways in. For programming, the shared state is git, vaults, briefs and graphs. Nothing has to be copied across, so I no longer notice the switch.

The newsroom is the worked example, because it can be counted. In three days in October 2026, one agent session took 54 messages from me, ten of them voice memos, and turned them into 40 releases, 36 articles and 87 figures, while other agent sessions made 15 releases of their own in the same repository, and the work met in git. The most useful thing about the counting is that it was possible: every channel left its trace in the same place.

It breaks in three known ways. Fragmentation: a decision made in a chat, a correction made by voice, a fix pushed from a phone, and if any of them lives only in its channel, the next channel does not know; nothing counts until it is in the shared state. Secrets in the wrong place: more channels means more places a key can be pasted. Lost context: long sessions get summarised, and summaries drop things. For a lot of people starting now, none of this is a change; it is simply what programming is. The 2025 Stack Overflow survey found 84% of respondents using or planning to use AI tools in their development process, and more of them distrusting the tools' accuracy than trusting it. That is the right instinct, and it is why the shared state matters more than any one channel.

## Every mistake added a rule

A friend who uses agents better than most, one writing, others verifying, a second model reviewing, sent me two messages about a verification that kept breaking. The code was holding up: 812 concurrency attacks, no failures. The process around it was not. Long sessions compacted and the agent skipped steps or wrote its report from the summary. Outputs of failing commands were lost. The prompt had grown to 100 KB, and asked to recite it, the agent reproduced it from memory, incomplete or wrong. And, in their words: "Every mistake added a rule, and every new rule caused new mistakes."

That is the trap, and the 2018 draft on agile described it from the other side: processes became more important than understanding why something was being created in the first place. Each rule grows the prompt, the prompt brings the summary sooner, and the summary decides which rules survive. The session that runs one of my sites was summarised eighteen times in a month, each time keeping on average 1.7% of what it replaced. A rule held only in conversation has to win every one of those summaries. When it does not, nothing tells you.

The way out is not a better rule. Rules that come from incidents, enforced by machines, stay few. Rules that come from worry, enforced by attention, multiply. When a rule fails, the question is not how to word it more strongly but which stronger barrier can replace it: a step short enough to finish before the summary, a wrapper that writes every output to a file, a script committed and hashed before it runs. Delete a rule every time a component makes it unnecessary. And if everything is a STOP, a STOP stops meaning anything: log mistakes of form and carry on; stop for harm.

What remains of the rules should live in a file, not in the conversation, and the file should come back after every summary. I call that re-anchoring: the rules are restored, not remembered. A short status report at the end of every few answers, computed from the transcript rather than written by the model, tells you the file was read. If the report stops appearing, something has fallen out.

## The kind of rule that works

So which rules survive? The ones an agent can keep. "No em-dashes" is a rule an agent can keep; "sound more human" is not. The articles on my newsroom are written under seven wording rules, each learned when a word jarred: no em-dashes, no absolutes I cannot back, "great" not "perfect", British English, plainer words, and two more. Each was a correction I made once. Each is now a line in the session's behaviour policy, printed back after every summary, and the site's validator checks some of them at build time, so a word I have banned cannot reach the page.

The effect is measurable. In one session, of 98 messages from me since its last summary, one correction in two days was about a word. The rest were about content and direction: cut the first section, that was not the point, go this way. A language correction is made once and then enforced; a content correction is new thinking every time. When the corrections move from language to content, the voice is working. That is the measure, and it is the one I would ask a candidate to show me: not that they use agents, but what their rules file looks like, how short it is, and which incident each line came from.

The 2018 draft *Changes* told you to enjoy loose briefs, because they are an opportunity to make the job into something you are good at. That still holds for a person. For an agent, a loose brief is a bill. The skill now is to write the tight brief, keep the rules few, and read the record.
