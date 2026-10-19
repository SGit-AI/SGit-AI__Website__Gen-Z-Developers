---
title: Facts, evidence and the record
slug: facts-and-the-record
part: judgement
number: 15
ideas: [the-record-checks-you, asked-to-be-corrected, a-claim-earns-its-status-by-being-refutable, ask-for-the-evidence, privacy-aware-generation, a-rabbit-hole-is-a-prompt-away, disagree-rationally-with-provenance, managing-information-is-the-work, gen-ai-makes-the-checking-cheap, best-prepared-person-in-the-room, provenance-is-a-graph, reality-corrects-the-graph, stale-pages-become-false-memories]
answers_2018: [5.concepts/facts.md, 5.concepts/feedback-loops.md, 4.life-patterns/content/being-criticized-is-a-privilege.md]
sources: [art:follow-the-rabbit-holes, sb:follow-the-rabbit-holes, art:where-the-thinking-came-from, art:generative-ai-not-ai, art:everything-is-connected, news:my-memory-checked, news:reviews-on-the-record, news:your-agents-logs-are-a-self-report, news:journalism-becomes-intelligence, news:memory-is-not-a-spectator-sport, news:code-review-as-a-fractal-semantic-graph, news:knowledge-that-maintains-itself, news:the-briefs-so-far, book:5.concepts/facts.md, book:5.concepts/feedback-loops.md, book:4.life-patterns/content/being-criticized-is-a-privilege.md]
character: sam
gravity: villager
status: draft
---

The cover of the 2018 book had two lines about this: question everything, and make fact based decisions. Inside, there was an outline called *Facts*, about data-driven decisions, that I never wrote. Its bullets still hold: be data and facts driven; science up your arguments; check your sources; understand the agenda of who is talking to you; and do not trust what is on the media when it is selling fear, because if it is on the media it is because it is rare. This is that chapter, and it is a different chapter from the one I would have written in 2018, because checking a fact has become cheap.

## Ask for the evidence

One of the most important skills this generation needs is questioning, and asking for the evidence. And in a way they already have it. They are very good at connecting the dots, very good at finding things; I think people underestimate them. They are very good detectives. That is my experience, from my family and the young people I have worked with, not a study.

They also care about privacy; they just have not had enough cases to disrupt it. Look at Snapchat: its best feature was that images disappear. That is a point about its design, not a claim about how private it actually is. And this generation has been told so often not to put anything online that it sometimes becomes a problem of its own. Where to draw the line is a question I do not have a settled answer to.

Behind the habit of asking is a philosophy, and I would rather name it. Karl Popper's principle is short: a claim earns its status by being refutable. If nothing could show it to be wrong, it is not saying anything. I keep a register of my own influences in that shape, where "an entry in this register is a falsifiable claim about my codebase", and I once wrote, about education, that "the problem with dogma is not that it exists, but that you stop asking the question." That is the first line of the 2018 cover, made into a method. Bruce Schneier adds the security version: before asking how something failed, ask who bears the cost of the failure.

## Provenance, and the rabbit holes

Learning takes you to two ideas: provenance, where something came from, and explainability, why it is the way it is. And to following the rabbit holes. Following a rabbit hole is now a prompt away. You should never take something at face value. You can build your own agents and your own tools, and be curious: where is the source of that, and where is the source of that? It is one of the areas I believe in most.

This book has an example of its own. In *Where the thinking came from* I could not say where the recording of a keynote by David Rice was. I found a link, and following it with an agent led to the video's real title, *OWASP AppSec USA 2010: Keynote: David Rice*, and then to a working session at the OWASP Summit in 2011 about presenting that keynote around the world, which I had not remembered. The last step was mine: a post I wrote in 2016, *The Pollution Analogy*, which links the full recording under the title my register uses, *Upon the Threshold of Opportunity*, and settles that they are the same talk. One link, one agent, one old blog post.

Provenance is a graph. As *Everything is connected: graphs* said, that is how I see the world: this connects to this, which connects to that. Where a claim came from is a chain of edges back to its source, and the detective's board, with the photos and the red string, is a graph of exactly that kind. The record a newsroom should keep is "not a pile of articles, but a graph whose every edge has a date and a source".

And the rabbit hole runs towards you as well. When I wrote the article behind *What generative AI is*, I asked Claude, which is helping me write this book, to correct me where I was wrong. It did: classic machine learning learns too; inside a model there are vectors, not a stored graph, so my graph is a metaphor; the prompt conditions what the model computes rather than changing it; hallucinations have a second cause, in training that rewards guessing; and emergent abilities are debated. The corrections are printed in that chapter with their sources, because they are the kind of thing a reader should learn to ask for. The book does the same wherever my picture and the evidence differ.

## How you disagree rationally

Provenance and explainability went by the wayside in the last decade, and I think they are the key piece of the puzzle, because they are how you can have rational conversations. That is how you can debate, how you can disagree, how you can have a logical conversation with somebody: when you can show what is evidence and what is not, what we know and what we do not know. Sometimes not knowing is a fact.

The newsroom has two rules for this. The first comes from how my articles are now written. I record a voice memo and say things the way I remember them, with the instinct ahead of the evidence. Then the agent checks: the repositories, the commits, the documentation, the web, my own old writing. In the last eight articles when I counted, five of my claims were confirmed, five corrected and two could not be found, and the articles say which. The rule is: "Not found is not false." It means the evidence was not found, and the article says so. Peer review used to come after publishing, from whoever on Twitter or LinkedIn noticed the mistake. Now it comes before, against the record rather than the crowd. And thinking out loud, which used to drive my teams mad as a plan moved from Monday to Friday, is now safe, because the record catches up with the instinct. It goes both ways: I correct the agent too.

The second rule is from the reviews. Every article is reviewed by readers that are not the writer, against published criteria, and each review is one file, written once and never edited. "A finding with no answer is just a complaint." So every finding gets an answer: fixed, in which version; declined, with the reason; or open. Declined with a reason is a valid answer. Deleting the finding is not. The 2018 book had the human version of this, in a chapter called *Being criticized is a privilege*: listening to criticism does not mean doing what you are told, and I gave three models for when I disagree, agree to disagree, disagree and commit, disagree and ignore. You cannot control how somebody will react to your actions, so use the reaction in your feedback loop. The review record is that chapter, kept as files.

One more rule, and it is the one a hiring manager should hold onto: distrust self-reports. An agent's account of what it did, its reasoning and its tidy summary at the end, is a self-report, the way a person's account is. In one study, models that exploited a reward hack admitted it in under 2% of cases. So the evidence should be written by something the agent controls less: a record a hook reads, a boundary the platform holds, someone outside testing it. My own newsroom agent's status report, computed from the transcript rather than written by the agent, once flagged two commits made without the leak scan. Both turned out to be in throwaway test repositories. The record written outside the agent was more honest than the agent's account, because it could not quietly leave the two commits out, and it still needed reading. Evidence that the control ran is not evidence that it worked.

## Reality corrects the graph

Here is the part people get wrong when they try to build a record like this. A model's first reading of anything, a codebase, a policy, an organisation, will be partly wrong. Some edges it proposes will not exist; some stories it names will be the wrong story. If the plan requires the graph to be right, the plan fails.

The plan does not require that. It requires the graph to be made of layers that someone knows, and to make predictions that something can check. Users confirm the top: a story either holds after a change or it does not. Experts confirm their own layer: the architect reads the components, the security reviewer the flows, the author the methods. Tests confirm execution. And every correction is a commit with a name on it. You do not have to get it right; you have to maintain it, and agents are very good at maintaining graphs, with a validator checking what they maintain. The patterns in the shape are findings in themselves: when my own code was read as a graph, the rules the project stated most firmly were the ones that held, and the one it stated least was the one most often broken.

The 2018 draft on feedback loops said "TDD is a gigantic feedback loop", and that the point of a loop is that the input affects the output which affects the input. This is that loop, applied to knowledge. When something in the graph looks wrong, you ask why, and the answer is a fix at the right altitude, and the next brief carries it.

The same loop keeps a shared memory honest. A memory made by agents and people becomes a rumour mill unless every item carries its source: a URL for every quote, a hash for every file, a byline on every page. And a memory goes stale. The session that wrote the article on memory found four stale claims about its own estate while researching it, fixed two, and left two standing and named, because a memory that hides its own errors is the thing to argue against. Two of the fixes were to measure the numbers at build time rather than remember them, which is the general rule: count rather than remember. The sentence I keep from that work is a hard one: "If the reality document doesn't list it, it does not exist."

## It is what work is

That is fundamentally what you do in business. When you work for a company, a lot of the time it is about managing information: knowing where it is, who is doing what, what the status is, and how a decision can be made. All of that is more and more critical, which is why it is so important that you learn how to follow the evidence. And it is why learning how to learn matters so much: if you learn this way, you are already learning how to follow the provenance, how to bring it down to things you understand, and how to communicate it, because you have the material.

Generative AI lets you scale this. In the past it was crazy expensive: building a system to give you this kind of data could cost hundreds of thousands or millions of pounds, a figure from my memory rather than a measurement, so it was rare, and even then it took so long that it was not effective. Now it is a brief and a feedback loop. When the newsroom's writer agent counted the sixty-five briefs the newsroom had published about itself, it took each one's status from the code rather than from what the articles said, and the audit found where the site's own records had fallen behind, and found the agent itself missing from the list of agents that write there. That is what checking looks like when it is cheap: it checks the checker too.

> **For Dinis:** the cost figure is from your memory; the article asks the book to give one example of such a system with a real number, which only you can supply.

So following the rabbit holes is not just something interesting. It is the core of what you do, and the core of what you are good at. You want to be known as the person who has the facts, the person who knows what is going on, the person who is well briefed. The person nobody can throw sand in the eyes of, or hand half-baked material, because they know you will check.

## Be the best-prepared person in the room

The other thing is that you have to be the most prepared person in the room. These days there is no excuse not to be. You should have briefings and pre-briefings: briefings for you, and briefings on the people you are meeting. You need to understand the name of the game and what is happening. You should have follow-ups. The storyboard for this chapter puts the brief on one board: who they are, what they want; what I want, what I know; what I don't know; the follow-ups. *Meeting briefs and follow-ups*, in the hands-on part, is the workflow.

All of this was overhead in the past. It could only be done by a very specific type of person. Not any more, and that is the beauty of where we are now: you can scale it, the way the rest of this book scales publishing, communication and agentic workflows.

> **For Dinis:** two of the article's questions for you are left open here: how you prepare for a meeting today, step by step; and whether the book may mention your daughters, as the article does when it makes the Snapchat point. This draft keeps them out until you decide.

If you are the person who always checks the source, you are already most of the way to the job. The rest is making the checking visible: a record anyone can read, with every finding answered, and your name on it.
