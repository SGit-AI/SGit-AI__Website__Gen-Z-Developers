---
title: An agentic workflow from zero
slug: an-agentic-workflow-from-zero
part: hands-on-2026
number: 23
ideas: []
answers_2018: []
sources: [news:from-a-spreadsheet-to-a-folder-per-person, news:how-i-work-with-claude, art:follow-the-rabbit-holes, art:lenses-roles-and-loops]
character: zara
gravity: explorer
status: draft
---

By the end of this chapter you will have a folder for every person you deal with, an agent that reads those folders and drafts for you, and six lines of rules that make it safe. One afternoon, no developer, no vault, no new tool: a Google Workspace account and a Claude seat are enough. The steps are the newsroom's, from *From a spreadsheet to a folder per person*. The tools move, and the article dates its description of the Claude app to October 2026; the shape is what to learn.

## What a spreadsheet cannot hold

If you are in touch with people, you probably have a spreadsheet: one row per person, a stage, a date, a next step, and a notes column. The person the article was written with ran their customer relationships that way, and ran them well. What the row cannot hold is what happened: the emails, word for word, the call last Tuesday, what was promised. "The difference is not the tool. It is what counts as the record." In a spreadsheet the record is a summary you typed. In a folder the record is everything that happened, kept as it happened, and the summary is derived from it. That reversal gives an agent something to work with.

## The folder, and the policy

Make a folder called Contacts. Inside it, one folder per person. Inside each, five documents, with these names so that you and the agent mean the same thing:

- **Record**: role, company, how you met, stage, the next step and its date, what they care about, every fact with where it came from in brackets. The row, promoted.
- **Ledger**: one line per event: the date, in or out, the channel, one sentence. Only ever added to. A correction is a new line.
- **Messages**: every email and note exchanged, pasted word for word, newest at the bottom.
- **Notes**: calls and meetings, dated, including what you said into your phone afterwards.
- **Summary**: written by the agent from the four above, rewritten when you ask, never edited by hand. If it is wrong, fix the Record or the Ledger and regenerate.

In the Claude app, connect Drive and Gmail, make one Project called Contacts, and put the behaviour policy in its instructions. Six lines, from the article, which I will not shorten:

1. You work for me. Every email you write is a draft that I read and send. You never send.
2. You read the Contacts folder in my Drive and my Gmail. You write only into a person's folder in Contacts, and only into their Ledger, Messages, Notes and Summary. You never change the Record without showing me the change first.
3. You add to the Ledger and the Messages. You never rewrite or delete a line. A correction is a new line.
4. Every fact you put in a Record or a Summary names where it came from.
5. If a person has no folder, you ask before making one. If a request would reach outside the folder, you ask.
6. At the end of every task you say, in one line, what you read and what you wrote.

Draft and never send; append and never rewrite; stay in the folder. The first three are the ones the newsroom learned the hard way. Most of this is told, not enforced; the rest is a rule the agent keeps, which is why line 6 exists. The one-line report is how you check.

What you have built is, in the terms of *Lenses, roles and loops*, an agent: a role on a loop with a goal, and the Project's instructions are its role description. *How I work with Claude* says it more plainly: a session with a focus and a `role.md`. Keep one session per topic, and name it.

## The afternoon, and the first week

The migration is four steps. Export the sheet as CSV, drop it in the folder, and ask the agent to say, for each row, the folder it would make and the Record it would write, without making anything yet. Make the folders from a template; twenty people is twenty minutes by hand. Per person, ask it to read a year of your mail with that person and write the Record and the first Ledger lines, each fact with its source; read the Record and correct it once. Then ask for the Summaries, read three, and where one is wrong fix the source document, not the summary. From then on nothing is retyped.

Then five exercises, one a day for the first week, each a single message:

1. **Ask.** Who have I not spoken to in more than a month, grouped by stage, with the last Ledger line for each?
2. **Prepare.** I am meeting someone on Thursday: brief me from the folder, what we last agreed, the last three emails, what we promised.
3. **Draft.** Draft my follow-up, in my voice, from Notes. Do not send. Add a Ledger line that says a draft exists. You change two words, send it, and tell the agent "sent".
4. **Debrief.** Speak for two minutes into your phone after the meeting; the agent puts the notes in Notes, updates the next step, adds the Ledger line and regenerates the Summary. This is the one that changes the habit.
5. **Campaign.** Find everyone whose Record says they care about X, show the list with the reason for each, then draft one note to each, and send none.

It will get two things wrong, predictably: a fact in the Record without a source, or a stage inferred from tone, fixed by a stricter line 4; and a Summary rewritten so that it drops something you cared about, fixed by putting the thing in the Record and regenerating. Every mistake adds a line to the policy. That is how the newsroom's grew, and it is what *Follow the rabbit holes* means by a system that once cost "hundreds of thousands or millions of pounds" being now "a brief and a feedback loop".

> **For Dinis:** the walkthrough is written for someone with customers, and asks for three real contacts and the topic the person sells to be substituted. For a reader looking for a first job, should the exercises be rewritten around their own contacts?

The folders move into a vault when one of three signals appears: a second agent needs to read them, the files should not be readable by whoever runs the drive, or the record has to carry between tools. Until then the folders are enough, and when the day comes the move is a copy; the policy does not change.
