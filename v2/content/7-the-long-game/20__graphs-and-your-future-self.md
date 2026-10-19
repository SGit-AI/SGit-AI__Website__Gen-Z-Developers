---
title: Graphs, memory and your future self
slug: graphs-and-your-future-self
part: the-long-game
number: 20
ideas: [think-in-graphs, memory-is-context-management, the-site-becomes-the-memory]
answers_2018: [7.your-cv/future-self.md, 4.life-patterns/content/backup-your-life.md, 2.mvp-for-gen-z-dev/content/dot-language.md, 5.concepts/recursive-functions.md]
sources: [news:memory-is-not-a-spectator-sport, news:knowledge-that-maintains-itself, news:bringing-my-past-work-back, news:the-graphs-books, news:introducing-fractal-semantic-graphs, art:connect-the-dots-backwards, book:4.life-patterns/content/backup-your-life.md, book:7.your-cv/future-self.md, book:2.mvp-for-gen-z-dev/content/dot-language.md, book:5.concepts/recursive-functions.md]
character: priya
gravity: all
status: draft
---

In 2018 I wrote a chapter called *Backup your life*. It asked one question: if you lost your laptop right now, how painful would it be? My own answer, at the moment of writing, was that I would lose the text of that chapter and nothing else, and in half an hour not even that, because it would be committed to git and pushed to GitHub. The chapter ended with a line I still stand by: "You basically need to backup your life!"

Eight years later the question is the same and the answer has grown. It is no longer only your files you have to keep. It is your ideas, the connections between them, and now the memory your agents work from. This chapter is about all three, and about the person you are keeping them for: your future self.

## I think in graphs

My thinking is very hyperlinked. I connect things; I follow this and then that, and it all works itself out in the end. *Everything is connected: graphs* introduced the graph as a thing to draw. Here I want to say it as a way of thinking, because it is the way I keep what I know.

The first edition had a chapter on DOT, a text language for diagrams. The argument was not about the tool. It was that a diagram stored as text can be put in git, committed on every change, and diffed, so that you can see what changed since the last time you looked. I wrote then that our brains struggle to review a diagram a second or third time unless we are shown "what changed since the last review", and that we were making decisions "based on shadows of reality". I also said that most diagrams are not maps, and that the next step was maps. The second edition's answer is the graph, and the graph is the step after the map.

Think of what your team already has. A spreadsheet of who owns which system. A folder of policies nobody opens. A shared drive of decisions that made sense at the time. Each of those is already a graph: a spreadsheet is a graph of sheets, rows, cells and formulas; a policy document is a graph of sections; a team is a graph of people and what they are responsible for. Nothing has to be converted. The edges only need to be named. A policy is owned by a team and implemented by a control; a decision supersedes an older one. Once the edges have names, a question can cross the formats, and a correction in one place can show you everything that rested on it.

Two rules from *Fractal Semantic Graphs* matter more than the rest. Every edge is a verb that reads both ways, and "relates to" is banned, because two things always relate and an edge with no verb tells you nothing. And supersede, never delete: an idea that turned out wrong stays, marked, with what replaced it, because the path from wrong to right is itself knowledge. The 2018 book had an outline called *Recursive Functions* that I never wrote up; it is, in a way, this: open any node and you find the same shape again, a graph inside the graph, as far down as your question needs to go.

Then the part that matters most for someone who has never written code. You do not have to get the graph right. You have to maintain it. The projects that try to get the ontology right first spend a year on it and never ship. Agents are very good at maintaining graphs: they read a new document and propose its nodes and edges, they notice a policy changed and mark what rested on it, and code checks that they kept the rules. When something in the graph looks wrong, you ask why, and the answer is a fix at the right altitude. I measured this on the newsroom: the graphs of its 112 articles hold about an eighth of the articles' text, and that eighth is enough to decide what to read.

A graph is also not a search box. Similarity search is useful for finding a starting point when you do not know the words an organisation uses, but it gives you similarity, not a reason, and the neighbours move when the index changes. A graph gives the same answer to the same question, with the path that led to it. For the question your team actually asks, "why are we required to do this, and by whom?", the path is the answer.

## Memory is context management

People ask how my agents remember. The picture most people have is one memory system, somewhere behind the agent, into which everything it sees is deposited and from which it retrieves by similarity whatever seems relevant. Mine is the opposite, and the newsroom article *Memory is not a spectator sport* says why.

An agent works inside a window of text. Everything in that window costs money, because it is billed by the token, and it costs attention, because a model's recall gets worse as the window fills. So the question is never "what do we remember". It is "what does this agent need in its window right now, and no more". Memory is context management. The industry's name for the same thing is context engineering, and it arrived there too.

It is many memories, not one. The rules of my inbox agent are not the rules of the news graph, and the vocabulary of a code review is not the vocabulary of a risk register. Each is a memory with its own words, and by now, across twenty-seven sibling sites and forty published vaults, they disagree with each other in places. I used to think that was a problem to solve. I now think it is the point: each is correct for its context, and a memory forced to agree with all the others would be wrong for every one of them.

It is fractal. Principles at the top in a few kilobytes, arguments and worked examples below, code at the bottom. An agent loads the altitude its question lives at and follows a link down only when it has to. The fractal is the budget.

And it is files. This is where the field and I agree, and where you should take heart. In August 2025 Letta ran a memory benchmark, and a plain filesystem, with the agent reading and writing files, scored 74.0 percent against 68.5 percent for a graph-based memory product. Their explanation was that simpler tools are more likely to be in the model's training and so more likely to be used well. Files won. Manus said it from the other side: "we treat the file system as the ultimate context". A folder of well-named plain files, kept in git, is already a memory an agent can use. You do not need a product for this.

It is shared. A session ends, and the next one, or a different agent, or a person, picks up from the same files. The article that argued this was written that way: one session, across several context resets, revised an article, wrote two more, published a vault and shipped six releases in a day, "remembering nothing between resets except what the files remembered for it". Nothing is remembered by the model between sessions. Everything is remembered by the files.

I should say where this falls short, because the article does. The thesis calls itself untested and falsifiable. Stale pages become false memories: the session that wrote it found four and fixed two. It is one person's estate, with one person's vocabulary at the top of every ladder, and it has not yet been tested against a second person's. Hold it as my position, and watch for the evidence.

## Publish, and the site becomes the memory

In 2018, under *Backup your life*, I said that the fewer secrets you have, the easier everything else is to back up, and that the more you publish, the more you can use the web itself as your backup. I said that Google and the Web Archive would eventually index what you put on a public, hyperlinked page, and that I had used their caches to recover ideas I published on sites that have since disappeared. And I said why I share at all: one day in the future my future self will need it. Open sourcing my work meant that when I moved jobs I did not start from scratch; the O2 Platform research and a maturity model tool came with me because they were already public.

The same reasoning now has a second beneficiary. Open source and Creative Commons are not a licensing preference here. They are what makes a memory usable by an agent: a public page can be fetched, a public quote can be cited with its URL, a public graph can be loaded by anyone's model, and a public vault can be cloned with a read key that is itself public. The more I publish, the more there is for the next session to stand on, and the less it has to be told. One article said it in passing, and it is the right description: the site is becoming the memory.

The 2018 book had an outline called *Future Self* that I never wrote. Its notes said: create assets that will be useful for them; the power of open sourcing your ideas; letters to a younger self are not that useful, unless you have a time machine; and that is why you want to share. I am writing it now. A letter to your younger self reaches nobody. A letter to your future self reaches them, but only if they can find it.

I know this because I failed at it. I have been creating content for a long time, and most of it is not linkable from what I write now. For years I used Google as the search engine for my own work: I would search for a phrase I remembered and find my old post. That is not a memory, it is luck. Twitter went south, and much of what I wrote there is hard to reach. The inventory, taken in October 2026 from the public pages, is 103 essays, 1,289 blog posts, 65 decks, 10 books, 29 tools, 2,038 files of NotebookLM material and 221 videos. A back catalogue I cannot link to is a conversation with no reply. So the newsroom now has a brief for a worker: an agent that runs every day, takes one item from that catalogue, and writes it back as an article that says what it was, what it said, what changed since, and how it connects. Each article is a node the next one can link to. It compounds.

> **For Dinis:** the 2018 *Future Self* outline promised a Twitter case study, "a perfect example that happened with me when writing this book", with two screenshots and no text. What did they show? The story would make this section concrete.

Every team has a back catalogue like this: design documents, talks, incident reviews, old wikis, decisions that made sense at the time. Most of it is not linkable from what the team writes today, so the same arguments get made again and the same mistakes repeated. A worker like that one does not need everything ready. It starts with the source that is easiest to read, writes a few items a day, and retrofits the history backwards while the team keeps working.

There is one more thing a shared memory needs, and a vector store cannot give it: a source for every item. On my sites that is a set of habits rather than a feature. Every quote has a URL. Every release has a commit. Every vault has a read key on its page. Every file inside a vault has a hash. Every page has a byline naming the person responsible, the model that drafted it and the date. Provenance is what lets memory be shared without being trusted. *Facts, evidence and the record* said why that matters for you; here it is what makes the memory safe for an agent to use.

So the advice to you is the 2018 advice, extended. Keep your work in plain text, in git, committed often. Name the links between things, in words a person in your team would say. Publish what you can, under a licence that lets it be quoted. Keep what you cannot publish in a vault, with a key that reads and does not write. And when you brief an agent, hand it the altitude its question lives at, not everything you have. *Your first graph, built by hand* and *Your own newsroom and inbox* show both ends of this done small.

The lesson of *Backup your life* was that you will lose data, so build the habits before it happens. The lesson now is that you will forget, your agents will forget, and the people who come after you on the team will never have known. The only memory that survives all three is the one that was written down, linked and left where the next reader will find it. Write for that reader. One day it will be you.
