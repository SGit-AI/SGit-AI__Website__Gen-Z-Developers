---
title: Your own newsroom and inbox
slug: your-own-publishing
part: hands-on-2026
number: 29
ideas: []
answers_2018: []
sources: [news:your-own-newsroom, news:replicating-the-agentic-inbox, news:how-the-voice-works, news:no-server-by-design]
character: priya
gravity: villager
status: draft
---

By the end of this chapter you will have two things the newsroom has written up as recipes: a site of your own, written from voice memos by an agent that checks every claim and publishes it; and an inbox worked by an agent that drafts and never sends. Neither needs you to write code. Both are the newsroom's own setups, from *Your own newsroom* and *Replicating the agentic inbox*, and both are honest about what is not finished.

## Voice memo in, a checked site out

The recipe, in eight steps, from *Your own newsroom*:

1. Create a public GitHub repository and turn on Pages, with GitHub Actions as the source. On a free plan the repository must be public, so nothing confidential goes in it.
2. Add a workflow that validates before it publishes. The rule that matters is that a failed check stops the release.
3. Write the house rules: one file at the root that the agent reads at the start of every session. Your voice, what to check, what never to publish, the release steps. It grows by one line every time you correct the agent.
4. Connect a cloud session to the repository, from a browser or from your phone.
5. Give it the first brief. The article gives the brief to paste: set up the folders, the article template, a small build script, a validator, and publish a first page about you. The agent writes the code. You do not.
6. Record, paste, review. Record a memo, paste the transcript, read what comes back on your phone, and correct it by voice.
7. Add the reader meter when there is something worth paying for. It never blocks a page, and while the payment link is empty no money moves.
8. Keep the record. Every article ends with what it does not claim and where it comes from; a correction is a new version with its diff, never a silent change.

The house rules are the product. The next step is to write them as a behaviour policy: what the agent is granted (push to this one repository and nothing else), what it is for, and the rules, each marked by what keeps it. A rule in a prompt is a hope. Only a rule that a hook or the build keeps is enforced, and the article's example marks which is which: at most one article a day, kept by a hook; every fact has a source, kept by the agent. You can also split the work as the newsroom does: a writer, an editor who can send a draft back, and a publisher that alone may push.

People ask how the agent sounds so human. *How the voice works* answers in two voices, mine and the model's, and the answer is not a prompt that says "write like me". It is four inputs: a corpus, which on the newsroom is the articles already written, each citing the ones before it; the memos, spoken not typed, which carry how I think and the order I reached things in; a short list of wording rules, seven on the newsroom, each a correction made once and written into the policy so it never comes back; and me, reading everything before and after it goes live. Take any one away and it stops working. "The method transfers. The voice does not." Your first memo, your first draft read on your phone, and your first rule are where yours starts.

## The email workflow, in phases

The inbox is the other half, and the article says the setup is copyable in an afternoon for the simple version and in a week for the full one. It is accounts, a policy, drafts and files, and you can stop at any phase.

**Phase 0, the accounts.** A mailbox of its own for the agent, on a domain you own. Never connect your own inbox: yours has years of secrets in it, the agent's is empty on day one, and that isolation is what lets you give it more as you learn to trust it. A Claude seat of its own, so the grants to mail, calendar and drive live only there; afterwards, confirm that your own account holds no connection to the agent's mailbox.

**Phase 1, one session.** The inbox agent reads, labels, moves and summarises, and writes replies as drafts. You send. Write its behaviour policy before the first run: the reach, the mandate, the gap between them, and for each row of the gap what actually stops the rest. On a Team plan most of those entries are "the policy, and nothing technical", and writing that down is the setup being honest about where trust is doing the work. Run it for a week, reading every draft.

**Phase 2, roles talking in files.** When one session is doing more than one kind of work, split it: inbox, drafts, CRM, briefs, dev, each a session with its own policy, talking through files in a vault rather than through the mailbox. Only one role reads the mailbox; only one writes to Drafts.

**Phase 3, the interfaces and the record.** Because every message is a file and every draft is in the mailbox, the whole workflow leaves a footprint you can read afterwards. You do not have to believe what the agent says it did. You can read what it did.

The rule that never changes: the agent drafts, and a person sends. The one exception, a security finding, has a row in the policy and a mechanism behind it, and the article's last piece of advice is to write the exception down before you need it.

## What you are learning underneath

The site you just built has no server of yours. Static files on a free host, code that runs in the reader's browser, the reader's balance in the reader's own browser. *No server, by design* calls this the second step after retiring the database: retire the back end. Not "no servers": no servers of yours with logic in them. It ships fast, because a release is a set of files and a rollback is a commit, and it leaves gaps, written down and accepted, because a reader who edits a balance that unlocks nothing has cheated nobody but themselves. *Your own newsroom* says building one is the most native way to learn what publishing a pure client-side site means, and you will have learned it by briefing, not by coding.
