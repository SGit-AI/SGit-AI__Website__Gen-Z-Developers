---
title: Serverless, for real
slug: building-blocks
part: build-it-without-a-server
number: 23
ideas: [lego-blocks, the-file-system-is-the-database, no-server-by-design, ship-now-ship-serverless, what-serverless-costs-when-idle, the-glue-behind-the-commodity, the-code-must-not-know-it-moved]
answers_2018: [2.mvp-for-gen-z-dev/draft/aws.md, 5.concepts/serverless.md, 5.concepts/micro-services.md, 7.your-cv/git.md, 2.mvp-for-gen-z-dev/content/docker.md]
sources: [art:gen-zx-developers, news:ephemeral-town-planner-services, news:the-question-is-whether-they-miss-it, news:cloudflare-as-lego-blocks, news:free-models-your-own-key, news:sgit-is-a-standard, news:the-tokens-hook, news:no-server-by-design, news:the-key-is-the-billing-system, news:the-value-of-constraints, news:chat-on-a-static-site, news:move-the-cloud-not-the-code, book:2.mvp-for-gen-z-dev/draft/aws.md, book:5.concepts/serverless.md, book:5.concepts/micro-services.md, book:7.your-cv/git.md, book:2.mvp-for-gen-z-dev/content/docker.md]
character: marta
gravity: villager
status: draft
---

The first edition had a draft on the cloud that warned it "is as complex as an OS". True, and the wrong thing to tell you. You do not need to learn the cloud. You need to know what the blocks are, which are free, and how to have an agent click them together once. I am technical, and I could learn any of these platforms. I do not want to. And a founder is also the person who gets woken up when it breaks. So this chapter has a rule before it has a map. Ship your company serverless. A founder with no servers has nothing to run at three in the morning and nothing to pay for when nobody is using it.

## The by-the-hour test

The 2018 outline on serverless said the word does not mean no servers, and that it was important to understand the limitations. To me it always meant four things: it scales to zero, it costs little or nothing when it is not there, it starts fast, and it turns a capability into a commodity. The CNCF's whitepaper says "there is no charge when code is not running", and the Berkeley paper warned in 2019 that few so-called elastic services could scale to zero.

The word has been stretched since. In October 2026 I read the pricing pages of the products sold under the name and asked each one question: what does it cost when nobody is using it? Excluding storage, on 18 October 2026:

| Product | Idle | How it bills |
|---|---|---|
| Lambda event functions | Zero | Per request and per millisecond |
| Cloud Run | Zero | Per 100 ms; idle instances not charged |
| Cosmos DB serverless | Zero | Per request unit, no minimum |
| Neon | Zero | Compute suspends when idle |
| Redshift Serverless | Zero | Per second while running |
| Aurora Serverless v2 | Zero since November 2024 | Pauses after a set idle time |
| OpenSearch, next generation | Zero since May 2026 | Scales to zero after 10 idle minutes |
| OpenSearch, classic | About $350 a month | A floor of 2 capacity units |
| MSK Serverless | About $550 a month | $0.75 per cluster-hour |
| Neptune Serverless | About $80 a month | A floor of 1 capacity unit |
| ElastiCache Serverless | From $6 a month | A minimum of storage, metered hourly |

The monthly figures are my arithmetic at 730 hours and US East rates. The line between the two halves is the test: **if it bills you by the hour when nobody is using it, it is not serverless**, and whoever runs it has something running on their side. The table is dated because floors fall, and *Ship a serverless product in a weekend* renews it each year. The test does not date, and a founder needs it because of the line in *The question is whether they miss it*: "Not to plan, not to pitch, not to architect. Ship." To ship that often the running cost has to be near nothing.

## The glue behind the commodity

I would rather replace the word than keep defending it. Three words each carry a part: ephemeral, because it comes and goes with use and costs nothing when gone; town planner, Simon Wardley's word for something mature and industrialised, a commodity; and services, because it is exposed for others to use. Ephemeral town planner services. Lambda is one, sitting on town planner services like S3, which are always there. The name is a proposal, not a prediction.

Naming things this way makes you ask whether something is really a commodity or only looks like one. Plenty of things are treated as commodities while, behind the scenes, they are a large amount of custom technology glued together, which is what a Wardley map shows. Lambda is the documented case. In its builders' own words, "we chose to use Linux containers to isolate functions" and "We were unsatisfied with this approach"; from 2018 they moved customers to Firecracker. For four years, the definition of serverless was containers inside rented machines, glued together, while it matured with its customers. That is how services become commodities, and your first version will be the same, a villager's work dressed as a town planner's. But a per-hour bill for a "serverless" product usually means the provider cannot yet spin the thing up and down fast and safely enough to bill by use: an engineering gap on their side, passed to you as a cost. Build the villager's version. Just do not bill by the hour and call it serverless.

## Cloud as Lego

In October 2026 I mapped the developer platform of the company I keep my domains with, Cloudflare, as the smallest blocks a non-specialist could put together: static files served free, small pieces of code at the edge, object storage that can be pinned to the EU, hosted models with a promise not to train on what you send, inbound email, a sign-in gate. *Cloudflare as Lego blocks* has the limits as the pages gave them on 18 October 2026, and they change. The blocks are more useful as packages, each the smallest set for one job: a site on your domain; your vault, hosted; an assistant over your documents; an inbox that does things; a form or a small API.

A read-only vault needs no code at all: a published folder of encrypted files that any static host can serve. A read-write vault needs one function of 83 lines, one storage bucket and one tiny coordinator per vault, run against the real client with no plaintext anywhere on the server. I should be straight about those 83 lines, because the rule of this chapter is no servers of mine with logic in them, and 83 lines of mine, running on someone else's platform, is logic. They store encrypted objects, check a hash of the write key, keep two pushes from overwriting each other, and cannot read a byte. That is the honest version of the rule: not that there is no code on the server side, but that whatever is there holds nothing, knows nothing, and can be replaced by any other store that does the same job.

The catch is setup, and it is in your favour. The platform's API cannot be called from a web page, so the one-time setup is a deploy button or an agent with a terminal that signs in, runs the commands and hands back the URL. It happens once; *Your first workspace* is where you learn to ask for it. The 2018 chapter on Docker had the same instinct: stop clicking buttons and write the environment down as code.

Three smaller blocks. The one you will use most is a model, and the question is who pays; on 18 October 2026 four free offers let anyone start without a card and let a web page call them directly, so the key goes from your browser to the provider and nowhere else (*Free models, your own key*). Free means they may learn from it: fine for what is already public, never for your customers' data. Git: the 2018 outline said "use Git everyday", and what I would add is why Git won. Not because of GitHub, but because it is a standard that any tool, any host and any person can read; sgit, in the next chapter, is the same kind of thing with the trust in a different place. If what a tool stores is not a format other tools can read, you are renting your own history. And the bill: models are paid for by the token, and the person who sees least is the user. A hook of 132 lines shows under each answer what a session read, how much came from the cache and what it cost; the session that wrote *The tokens hook* had read 99% from the cache, the difference at list prices between about $170 and about $1,950. You need the box under the answer, and the habit of looking at it.

> **For Dinis:** what a founder on their first product should expect to pay in a month, for one site, one vault and a model on a free tier with their own key; the register says costs for a newcomer is still a gap, and only you have the receipts.

## The file system is the database

Here is a rule I have held for years: you do not need a database. The file system is the database. A database server is a large, stateful, always-on thing you have to provision, secure, back up and pay for whether or not anyone is using it; it fails the by-the-hour test before you have a customer. Load the state, work on it in memory, save it back. I call the pattern LETS, Load, Extract, Transform, Save: a cache, a database and an audit trail in one, with Git as its history.

If you run a business on a shared spreadsheet you already know this; what you lacked was a way to query the file, and now the newsroom runs two real database engines inside the browser, over the JSON files its pages are built from. The database is the files; the engines are just readers. The 2018 outline on micro-services worried about a constellation of services nobody understands. Files have the opposite property: every piece of state is a thing you can open.

## No server, by design

The second step crept up on me over months, and the newsroom made it explicit: retire the back end too. The newsroom keeps personas, charges by the share of a page read, takes money and runs SQL over its own data, and none of that logic runs on a server. What is left is commodity: static hosting, a vault server that stores only ciphertext, a payment provider's hosted page, DNS and a build pipeline. I am not saying there are no servers. It is no servers of mine with logic in them.

I did not choose this architecture and then add encryption. Encryption came first, and the client-side design followed, because the vault server cannot read a byte, so anything that reads the user's data has to run where the key is: in the browser. A server that cannot read has nothing to compute, so there is no server code to deploy or patch.

Here is what no server buys a company, from a product we built in August 2026 that turns a voice note into a transcript and a debrief, in the browser, on the user's own key, with nothing stored. We never see the audio. That one fact removes, at a stroke: data custody and its governance; a place where a breach can happen; a billing system; a database of users; a thing that has to scale; a thing that has to be up at three in the morning, and a person to wake. Add a server and every item comes back. "That is not one feature; it is a different company, with a different cost base and a different risk register." No server is the product, not a preference. Its first three weeks, 239 commits and 27 releases, are what moving fast looks like, because the complexity of the moving parts is what decides how fast you can move.

There is one honest limit, and a founder meets it first. Anything the user must not hold cannot live in the user's browser. A static site has no place to keep a secret, so a chat box on one cannot hold an API key; the honest answers are the reader's own key, or a bridge through a vault. The voice product met the same wall as a billing question: a capped key per paying user, metered by the provider, was the plan, and the provider's terms, not the architecture, stopped it. The route left, a metering proxy, is the smallest possible backend and still a backend: the audio passes through it, and custody, scaling and on-call all return. Servers are not bad; a bank's ledger needs shared, live state. The pattern is for products where each user's state is theirs, which is most first products, and the next chapter is about the key that makes it work.

## The code must not know it moved

One more thing a founder in Europe will be asked, usually by the first serious customer: where is the data, and could you move it? At a digital sovereignty event in October 2026, one conversation kept returning to the same point. What stops workloads moving is not policy or price. It is code. Every call to S3, EC2 and IAM is written into applications that work today and that nobody wants to touch. A hyperscaler's European cloud does not answer it: your code still talks to one vendor's API under one vendor's terms. Sovereignty that depends on one company's API is sovereignty by permission.

So the requirement is that the application must not know it has moved. Not one line changes. The same calls land on a twin: an open source interface to a real system, valued for one thing, that the client cannot tell the difference. The twin decides where the bytes go: real S3, an sgit vault, a European operator's data centre, a laptop. Switching a mock costs a code path; switching a twin costs an endpoint, and if it costs an endpoint, migration is a configuration decision rather than a project, and projects get cancelled. The S3 twin exists, as open source; EC2 and IAM do not yet. And none of it works if the twin layer is closed: swap one vendor's API for another vendor's wrapper and the lock-in has moved, not gone.

For a company with no servers of its own this is cheap to honour from day one: your product's state is files in a vault whose key the user holds, so make where the files live a setting, and the customer's question has a one-word answer. *Shipped means the user has it* takes the same twin into testing, where it may matter even more.
