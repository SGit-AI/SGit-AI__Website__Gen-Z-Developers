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

By the end of this chapter you will have a folder for every person you deal with, an agent that reads those folders and drafts for you, and six lines of rules that make it safe. It takes one afternoon, and it needs no developer, no vault and no new tool: a Google Workspace account and a Claude seat are enough. The steps are the newsroom's, from *From a spreadsheet to a folder per person*, and I am keeping them in the order the article gives them.

This part of the book is dated 2026. The tools in it move; the article itself says the Claude app's connectors are described as of October 2026 and vary by plan and settings. The shape of the workflow is what to learn: the folder, the policy, the exercises. The rest you will renew.

## What a spreadsheet cannot hold

Start with what you already have. If you are in touch with people, companies you have applied to, people who said "send me something", you probably have a spreadsheet: one row per person, a stage, a date, a next step, and a notes column that holds whatever fits. The person I sat with, the day the article was written, ran their customer relationships that way, and ran them well.

What the row cannot hold is what happened: the emails, word for word, the call last Tuesday, what was promised. That lives in your mail, in a notebook and in your head, and only you can read it in context. "The difference is not the tool. It is what counts as the record." In a spreadsheet the record is a summary you typed. In a folder the record is everything that happened, kept as it happened, and the summary is derived from it. That reversal is what gives an agent something to work with.

## The folder, and the policy

Make a folder called Contacts. Inside it, one folder per person. Inside each, five documents, with these names so that you and the agent mean the same thing:

- **Record**: role, company, how you met, stage, the next step and its date, what they care about. Every fact says where it came from, in brackets. This is the row, promoted.
- **Ledger**: one line per event: the date, in or out, the channel, one sentence. Only ever added to. A correction is a new line.
- **Messages**: every email and note exchanged, pasted word for word, newest at the bottom.
- **Notes**: calls and meetings, dated, including what you said into your phone afterwards.
- **Summary**: written by the agent from the four above, rewritten when you ask, never edited by hand. If it is wrong, fix the Record or the Ledger and regenerate.

Then the agent. In the Claude app, connect Drive and Gmail, make one Project called Contacts, and put the behaviour policy in its instructions. The article gives six lines, and I will not shorten them, because the first three are the ones the newsroom learned the hard way:

1. You work for me. Every email you write is a draft that I read and send. You never send.
2. You read the Contacts folder in my Drive and my Gmail. You write only into a person's folder in Contacts, and only into their Ledger, Messages, Notes and Summary. You never change the Record without showing me the change first.
3. You add to the Ledger and the Messages. You never rewrite or delete a line. A correction is a new line.
4. Every fact you put in a Record or a Summary names where it came from.
5. If a person has no folder, you ask before making one. If a request would reach outside the folder, you ask.
6. At the end of every task you say, in one line, what you read and what you wrote.

Draft and never send; append and never rewrite; stay in the folder. Most of this is told, not enforced: in the app, "draft, never send" holds as far as Gmail drafting goes, and the rest is a rule the agent keeps. That is why line 6 exists. The one-line report is how you check.

If you have read *Lenses, roles and loops*, you will recognise what you have just built. A role is a model with a description and a question; an agent is that role on a loop with a goal. The Project's instructions are the role description. *How I work with Claude* says the same thing more plainly: an agent is a session with a focus and a `role.md`. Name the session for what it does, and keep one session per topic, so the frame of reference stays small and right.

## The afternoon, and the first week

The migration is four steps. Export the sheet as CSV and drop it in the folder, then ask the agent to tell you, for each row, the folder it would make and the Record it would write, without making anything yet. Make the folders, from a template you made once; the article reckons twenty people is twenty minutes if you copy them by hand. Per person, ask it to read everything in your mail with that person from the last year and write the Record and the first Ledger lines, each fact with its source. Read the Record and correct it once. Then ask for the Summaries, read three, and where one is wrong fix the source document, not the summary. From then on, nothing is retyped. The article says one afternoon is for twenty to fifty contacts.

Then five exercises, one a day for the first week, each one message to the agent:

1. **Ask.** Who have I not spoken to in more than a month, grouped by stage, with the last Ledger line for each?
2. **Prepare.** I am meeting someone on Thursday: brief me from the folder, what we last agreed, the last three emails, what we promised and have not done.
3. **Draft.** Draft my follow-up, in my voice, from Notes. Do not send. Add a Ledger line that says a draft exists. You open it, change two words, send it, and tell the agent "sent".
4. **Debrief.** Speak for two minutes into your phone after the meeting; have the agent put the notes in Notes, update the next step, add the Ledger line and regenerate the Summary. This is the one that changes the habit, because the record is kept at the moment the thing happens.
5. **Campaign.** Find everyone whose Record says they care about X, show the list with the reason for each, then draft one note to each, and send none.

It will get two things wrong, predictably. It will put a fact in the Record without a source, or infer a stage from tone; the fix is a stricter line 4. And it will rewrite the Summary in a way that drops something you cared about; the fix is not to edit the Summary but to put the thing in the Record, where it is a fact with a source. Every mistake adds a line to the policy. That is how the newsroom's policies grew, and it is what *Follow the rabbit holes* means when it says that what once cost "hundreds of thousands or millions of pounds" to build is now "a brief and a feedback loop".

> **For Dinis:** the walkthrough is written for someone with customers, and asks the agent that sends it to substitute three real contacts and the topic the person sells. For a reader looking for a first job, should the exercises be rewritten around their own contacts, or kept as the newsroom has them?

When should the folders move into a vault? Three signals: a second agent needs to read them; the files should not be readable by whoever runs the drive; or the record has to carry between tools. Until one appears, the folders are enough. The shape is the same, so when the day comes the move is a copy, and the policy does not change at all.
