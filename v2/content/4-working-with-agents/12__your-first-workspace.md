---
title: Your first workspace
slug: your-first-workspace
part: working-with-agents
number: 12
ideas: [first-workspace, not-on-your-laptop]
answers_2018: [2.mvp-for-gen-z-dev/_index.md, 2.mvp-for-gen-z-dev/content/slack-and-chatops.md, 4.life-patterns/automate-your-workflows.md, 6.security/dont-touch-production.md]
sources: [news:from-a-spreadsheet-to-a-folder-per-person, news:replicating-the-agentic-inbox, news:how-i-work-with-claude, news:short-punchy-and-co-written, news:why-my-agents-do-not-run-on-my-laptop, book:2.mvp-for-gen-z-dev/_index.md, book:2.mvp-for-gen-z-dev/content/slack-and-chatops.md, book:4.life-patterns/automate-your-workflows.md, book:6.security/dont-touch-production.md]
character: priya
gravity: all
status: draft
---

Not long ago I sat with someone who runs their customer relationships in a spreadsheet. A good one, shaped over years to how they work: one row per person, a stage, a date, a next step, and a notes column that holds whatever fits. It does what a spreadsheet does well. What it cannot hold is what happened: the emails, word for word, the call last Tuesday, what was promised, what they care about. That lives in Gmail, in a notebook and in one person's head, and only that person can read it in context.

If you have run a team, a project or a department, you have a spreadsheet like it. This chapter is about the afternoon that turns it into your first workspace, with an agent working inside it, using nothing more than a Google Workspace account and a Claude seat. No developer, no new tool, no code. It is the practical chapter I promised in *Short, punchy, and co-written with Claude*, for the people I will send this book to who do not yet work the way I do. The 2018 book had a draft called *Automate your workflows* that never got past its bullets; one of them tied the topic to "thinking in graphs" and to moving away from spreadsheets. It took a different kind of software for me to write it up.

## The row becomes a folder

The difference between a spreadsheet and a workspace is not the tool. It is what counts as the record. In a spreadsheet the record is the row, and the row is a summary you typed. In a folder the record is everything that happened, kept as it happened, and the summary is derived from it. That reversal is what gives an agent something to work with.

So make a folder in Google Drive called Contacts. Inside it, one folder per person. Inside each, five documents, with these names so that you and the agent mean the same thing:

- **Record.** Role, company, how you met, stage, the next step and its date, what they care about. Every fact says where it came from, in brackets: "(email, 3 Oct)". This is the row, promoted.
- **Ledger.** A sheet with one line per event: the date, in or out, the channel, one sentence. Only ever added to; a correction is a new line.
- **Messages.** Every email and note exchanged with the person, pasted word for word.
- **Notes.** Calls and meetings, dated, including what you said into your phone afterwards.
- **Summary.** Written by the agent from the four above, rewritten whenever you ask, never edited by hand. If it is wrong, the fix goes in the Record or the Ledger, and the Summary is regenerated.

That is the whole structure. It is the one my agents run in encrypted vaults, minus the hashes and the graph. A person with no interest in software can keep it, and a person who leaves can hand it over. The 2018 chapter on Slack had a smaller version of the same habit, which I called talking to yourself: write down what you are about to try, do it, paste the screenshot, repeat, because the raw record of your own thinking is useful to your future self. The Ledger is that habit, kept for every person you work with.

## The agent, and six lines

In the Claude app, connect Google Drive and Gmail. Make one Project, call it Contacts, and put the agent's behaviour policy in its instructions. Mine is six lines:

1. You work for me. Every email you write is a draft that I read and send. You never send.
2. You read the Contacts folder in my Drive and my Gmail. You write only into a person's folder, and only into their Ledger, Messages, Notes and Summary. You never change the Record without showing me the change first.
3. You add to the Ledger and the Messages. You never rewrite or delete a line. A correction is a new line.
4. Every fact you put in a Record or a Summary names where it came from.
5. If a person has no folder, you ask before making one. If a request would reach outside the folder, you ask.
6. At the end of every task you say, in one line, what you read and what you wrote.

The first three are the ones my team learned the hard way: draft and never send; append and never rewrite; stay in the folder. The sixth exists because most of the policy is told, not enforced. In the Claude app today, "draft, never send" holds as far as Gmail drafting goes; the rest is a rule the agent is asked to keep, and the one-line report is how you check that it did.

Draft, never send is the rule that never changes. It is why the agentic email workflow I run is the first one that made me feel more in control, not less: every reply lands in Drafts, I read it, change what I want changed, and press send. When the day comes to let an agent send, it will be one agent, one kind of message, with a policy row that says so.

## One afternoon, then five exercises

The migration is one afternoon, in four steps. Export the sheet as a CSV and drop it in the folder; ask the agent what folders and Records it would make, and do not let it make anything yet. Make the folders, from a template you made once. Then, person by person: read everything in my Gmail with this person from the last year, write the Record and the first Ledger lines from it, each fact with its source. Read the Record and correct it once; that is the only retyping you will ever do. Last, ask for the Summaries.

Then five exercises over the first week, each one message to the agent, each using the folder in a way the one before did not:

1. **Ask.** Who have I not spoken to in more than a month, grouped by stage, with the last Ledger line for each?
2. **Prepare.** I am meeting this person on Thursday. Brief me from the folder: what we last agreed, the last three emails, what we promised and have not done.
3. **Draft.** Draft my follow-up, in my voice, from Notes. Do not send. Add a Ledger line that says a draft exists.
4. **Debrief.** Here is my voice note after the meeting. Put it in Notes, update the next step in the Record and show me the change, add the Ledger line, regenerate the Summary.
5. **Campaign.** Find everyone whose Record says they care about X. Show me the list with the reason for each. Then draft one note to each, and do not send any.

The fourth is the one that changes the habit, because the record is now kept at the moment the thing happens.

It will get two things wrong at first. It will put a fact in the Record without a source, or infer a stage from tone; the fix is a stricter line 4. And it will rewrite the Summary in a way that drops something you cared about; the fix is not to edit the Summary but to put the thing in the Record, where it is a fact with a source. The Summary is a view; the Record is the truth. One thing that is not a mistake: it will sometimes ask when you did not expect it to. That is line 5 working.

> **For Dinis:** the beginner's checklist of accounts and what they cost (the Workspace seat, the Claude plan, the agent's own mailbox) is still a gap in the material; the only figure the articles give is "a few pounds a month" for a Workspace mailbox.

## Habits that make it last

Three habits turn a week's exercise into a way of working.

One session per topic. A thread is the model's frame of reference, and everything in it is context for the next answer. Put three projects in one thread and the model starts to borrow a name from one and a decision from another. It is not being careless; it is doing exactly what you asked. When the topic changes, open a new session.

Name every session, with the project and the job in the name: Contacts, this week's follow-ups. An agent session gets an @ in front: @contacts. An agent, in the end, is a session with a focus: a few documents that say what the project is, a short file that says what the agent does and does not do, and a session that reads them before anything else. *How to work with agents* takes this further.

Give the agent a mailbox of its own. When you want it to handle mail rather than read yours, buy it a Workspace seat on a domain you own and a Claude seat of its own, and connect Gmail and Drive from that account, not yours. Your inbox has years of secrets in it. The agent's is empty on day one, so what it can leak is nothing, and what it can reach is exactly what you forward to it. That isolation is not a limitation. It is what lets you give the agent more as you learn to trust it.

## Why your agents should not run on your laptop

People ask me most weeks why I do not run a model on my Mac. The reason is not the models. It is a fact about operating systems: they have two hard walls, the kernel and the user account, and inside the user account there is no third wall. A process you start runs as you. The file system does not know the difference between you opening your SSH key and a process you started opening it. An agent on your laptop can read everything you can read: your cloud credentials, the password manager while it is unlocked, every site your browser is signed into.

The 2018 book had a draft on this, *Don't touch production*, written for developers: teams and individuals should be "allergic to being given access to data and systems", because the more you can reach, the more a compromise of your machine costs. The same rule now applies to the agent you have just set up, and to you as its operator. A mistake inside a boundary is a bad afternoon. The same mistake inside your account is an incident.

So pick the surface by reach. My agents run in places that are not my laptop: a chat with nothing connected, for thinking; Cowork in the cloud, with no repositories, for most of the agentic work; Claude Code on the web, with one repository per session, when code has to change. The surface with the repositories has no mailbox, the surface with the mailbox has no repositories, and the surface with neither does the thinking. Your Contacts Project is the first of these: it reaches one folder and one mailbox, and nothing else of yours.

In 2018 I wrote that Slack was "a massive agent for change" because it put humans, bots, servers and events in one asynchronous place, and I asked whether you were going to take an active role in making it work for an organisation. The question is the same now, with an agent in the room. The first task in the 2018 book was to write a blog post about your experiments. Write the one about this afternoon.
