---
title: Building blocks
slug: building-blocks
part: building-safely
number: 18
ideas: [lego-blocks, the-file-system-is-the-database, no-server-by-design]
answers_2018: [2.mvp-for-gen-z-dev/draft/aws.md, 5.concepts/serverless.md, 5.concepts/micro-services.md, 7.your-cv/git.md, 2.mvp-for-gen-z-dev/content/docker.md]
sources: [news:cloudflare-as-lego-blocks, news:free-models-your-own-key, news:ephemeral-town-planner-services, news:sgit-is-a-standard, news:the-tokens-hook, news:no-server-by-design, book:2.mvp-for-gen-z-dev/draft/aws.md, book:5.concepts/serverless.md, book:5.concepts/micro-services.md, book:7.your-cv/git.md, book:2.mvp-for-gen-z-dev/content/docker.md]
character: priya
gravity: villager
status: draft
---

The first edition had a draft on the cloud that never got past its notes. One asked what you were waiting for, if you did not yet have a cloud account. The draft warned that the cloud "is as complex as an OS". True, and the wrong thing to tell you. You do not need to learn the cloud. You need to know what the blocks are, which are free, and how to have an agent click them together once, so the result is something you own and do not think about again. I am technical, and I could learn any of these platforms. I do not want to. If that is your position too, this chapter is the map.

## Cloud as Lego

In October 2026 I mapped the developer platform of the company I keep my domains with, Cloudflare, as the smallest blocks a non-specialist could put together. *Cloudflare as Lego blocks* has the list, with the limits as the pages gave them on 18 October 2026, and they change. To put something on the web: static files, served free with no request limit; small pieces of code at the edge, 100,000 requests a day free. To keep data: object storage, 10 GB free with no charge for reading it out; a small SQL database; a key-value store. To think: hosted models with a free daily allowance, running on the platform's own machines, with a privacy page that says it does not train on what you send. To talk and guard: inbound email to your domain, free; a sign-in gate in front of anything, free for up to 50 users.

The blocks are more useful as packages, each the smallest set for one job: a site on your domain; your vault, hosted; an assistant over your documents; an inbox that does things; a form or a small API. We tested the hardest. A read-only vault needs no code at all: a published folder of encrypted files that any static host can serve. A read-write vault needs one function of 83 lines, one storage bucket and one tiny coordinator per vault, and we ran it in the platform's own runtime against the real client: create, push, clone, and no plaintext anywhere on the server.

The catch is setup, and it is a catch in your favour. The platform's API cannot be called from a web page, so the one-time setup is a deploy button, a temporary account, or an agent with a terminal that signs in, runs the commands and hands back the URL. That is fine, because it happens once. *Your first workspace* is where you learn to ask for it.

The 2018 chapter on Docker is the one piece of that part I would keep as it stands. A container is "a process that exposes a multi-layered file system as a fully isolated OS", and the point of learning it was to move from building environments by clicking buttons to writing them down as code. That instinct is still right.

## Free models, with your own key

The block you will use most is a model, and the question is who pays. We checked every free offer we could find, as of 18 October 2026, against two tests: can anyone start free without a card, and can a web page call it directly, so the key goes from your browser to the provider and nowhere else. Four passed both: Groq, Google's Gemini through AI Studio, Mistral's free mode, and OpenRouter's free models. *Free models, your own key* has the table, and two warnings.

Free moves: in 2026 four offers we would have recommended at the start of the year disappeared or gained a card, GitHub Models among them, retired on 30 July. And free means they may learn from it. On the free tiers, assume your words may be kept, learned from and, on one of them, read by people. That is fine for material that is already public. Never for anything private, and your team's spreadsheet is private.

One more thing I would not let an agent do: create the account for you. What an agent does well is guide: open the right page, explain each setting, point at the privacy switch, check the key works, and store it where you choose.

## Git is a standard, and what tokens cost

The 2018 outline on Git was a page of bullets I never wrote up, and it had the right ones: use Git as your backup, version all your documents, "use Git everyday". The line I would add now is why Git won. Not because of GitHub. Because it is a standard: a way of laying out objects that any tool, any host and any person can read. Your history is not in anyone's product. sgit, which the newsroom runs on, is the same kind of thing with one change, where the trust sits: everything is encrypted before it leaves your machine, and any storage that answers a plain read can serve it. *sgit is a standard, not a server* makes the case; there is a server, "and it is the least interesting part". When you choose a tool to keep your work in, ask whether what it stores is a format other tools can read. If not, you are renting your own history.

Then the bill. Models are paid for by the token, and the person who sees least is the user. I asked for a hook that shows, under each answer, what the session has read, how much came from the cache, what it wrote and roughly what it cost; the newsroom's agent built it in 132 lines. A prompt cannot do this job: asked to report its own usage, the model said, correctly, that it could not see the numbers. The hook could. The session that wrote *The tokens hook* had read 99% of its input from the cache, which at list prices is the difference between about $170 and about $1,950. You do not need to understand caching. You need the box under the answer, and the habit of looking at it.

> **For Dinis:** what a newcomer like Priya should expect to pay in a month, for one site, one vault and a model on a free tier with their own key; the register says costs for a newcomer is still a gap, and only you have the receipts.

## The file system is the database

Here is a rule I have held for years: you do not need a database. The file system is the database. A database server is a large, stateful, always-on thing that you have to provision, secure, back up, migrate and pay for, whether or not anyone is using it, and most of the time what it holds would be quite happy as files. Load the state, work on it in memory, save it back. I call the pattern LETS, Load, Extract, Transform, Save, and *No server, by design* traces it through the projects it runs. It is a cache, a database and an audit trail in one, and Git gives it history for free.

If you have run a team on a shared spreadsheet, you already know this. The spreadsheet is a file. What you did not have was a way to query it like a database without buying one. You do now: the newsroom runs two real database engines, compiled to run inside the browser, over the JSON files its pages are built from. The database is the files; the engines are just readers. The 2018 outline on micro-services worried about moving from one blob of code into a constellation of services nobody fully understands. Files have the opposite property: every piece of state is a thing you can open.

## No server, by design

The second step crept up on me over months, and the newsroom made it explicit: retire the back end too. The newsroom today lands a reader as a persona, charges by the share of a page they read, takes money and runs SQL over its own data. None of that logic runs on a server. What is left on the server side is commodity: static hosting, a vault server that stores only ciphertext, a payment provider's hosted page, DNS and a build pipeline. I am not saying there are no servers. What there is not is a server of mine with application logic in it. Each of those is a product, used as it comes, replaceable by another that does the same job.

I did not choose this architecture and then add encryption. Encryption came first, and the client-side design followed, because the vault server cannot read a byte, so anything that needs to read the reader's data has to happen where the key is: in the browser. And once the logic is in the browser, the question changes from "where on the server should this go?" to "why would this need a server at all?" That is a question you can ask of any tool your team is sold, and you do not need to write code to ask it.

The results are the ones you would want. It scales without its complexity scaling: a hundred thousand readers mean a hundred thousand browsers each doing their own work, against a server side that serves cached files; the server's work grows with bandwidth, and its complexity does not grow at all. It ships fast: 114 releases between 1 and 11 October 2026, and the reading meter went from an experiment to a working pay-on-demand design in seven releases in an afternoon. And it lines up with the things I care about: sovereignty, because the reader holds the data and the keys; privacy as a property, because the server cannot read what it does not have; explainability, because the whole application is files anyone can read; determinism, because the same files give the same result.

The 2018 outline on serverless said the word does not mean no servers, and that it was important to understand the limitations. The word has been stretched since: it now sits on products that bill you every hour whether anyone uses them or not, one of them at $0.75 a cluster-hour. So here is my test: if it bills you by the hour when nobody is using it, it is not serverless, and whoever runs it has something running on their side. I would rather replace the word with three that each carry part of it: ephemeral, because it comes and goes with use and costs nothing when gone; town planner, Simon Wardley's word for something industrialised and mature; and services, because it is exposed for others to use. Ephemeral town planner services.

There is one honest limit. Anything the reader must not hold cannot live in the reader's browser: a shared key, a price that unlocks something. And this is not a claim that servers are bad. A trading system, a multiplayer game and a bank's ledger need shared, live, authoritative state. This pattern is for applications where each user's state is theirs. First the database went, and the work got simpler. Now the back end is going, and the work is getting faster. I do not know yet where the pattern stops, which is why it is worth pushing.
