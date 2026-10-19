---
title: Ship it, and see if they miss it
slug: ship-it-and-see-if-they-miss-it
part: start-the-company
number: 18
ideas: [do-they-miss-it, the-roadmap-deciders-must-use-it, the-loop-is-the-moat, sg-send-live-in-five-days, silence-is-a-signal]
answers_2018: [4.life-patterns/content/be-a-founder.md]
sources: [news:the-question-is-whether-they-miss-it, news:i-miss-it, news:price-it-then-give-it-away, news:from-send-to-sgit, book:4.life-patterns/content/be-a-founder.md, art:gen-zx-developers]
character: marta
gravity: explorer
status: draft
---

Most advice about starting a company is about raising money. This chapter is not that. It is the operating model I actually use, in three pillars, in an order that matters: be profitable; the investors should be talking to you, not the other way round; open source everything. Each one buys you the position you need for the next. The second pillar is *Fund it, or do not*, and the third is *Open source*. This chapter is the first, and the first begins with one word.

Strip away the mythology and a startup is simple. You make a thing somebody wants to buy, at a price that is profitable to you. Which means the single most important skill is the ability to ship. "Not to plan, not to pitch, not to architect. Ship." And ship every day, because shipping is how you find out what is true.

If you have spent twenty-five years describing the tool you need to people who never built it, this is the hardest and the best news in the book. The description was never the problem. The build was, and the build is now yours to do.

Be careful with the word, because it has been worn smooth. Shipping does not mean a proof of concept. It does not mean a demo, or a video of a demo, or a prototype you walk somebody through on a call. It means a thing somebody else can go and use, on their own, and get value from. It can be held together with tape. Nobody using it cares how it was built, and neither should you, yet.

I need to be honest about a tension here, because two things I have written pull against each other. The newsroom article behind this chapter says the shipped thing "can be vibe coded". The frame of this book, in *Explorer coding, not vibe coding, and the handover*, is that the explorer builds to find out, and that what the exploration produces is the brief for the version other people will rely on. Both are true, and the gap between them is the point of this chapter. The first thing you put in a stranger's hands can be explorer code. What cannot be explorer code is the thing people come to depend on. The test below is how you find out which of the two you are holding, and it is cheaper than guessing.

To ship that often you need the running cost to be near nothing, so build accordingly: serverless, as few databases and as little live state as you can stand. *Serverless, for real* is the long version. And do not underestimate the plumbing. Getting a working thing into a stranger's hands is still, in 2026, genuinely hard. "Solving that is not overhead, it is the first real product you build." Everything after it gets cheaper.

## Give it away, then take it away

Now hand it to people for free. Not forever: a short window, whatever unit makes sense. You want the feedback loop tight, and you want the cost of generosity inside what you can absorb.

Just doing this solves dozens of problems you did not know you had. How people get access. What breaks when somebody unfamiliar touches it. What they try first. What they never find. "The feedback starts the moment somebody who is not you has the thing."

Then comes the part almost nobody does deliberately. Take it away. The trial expired. It is not available right now. Nothing else about the product changes, and no apology is needed. And ask the only question that matters.

Do they miss it?

If they shrug and go back to their day, you do not have a product yet. You have something people will accept when it is free, which is a much weaker signal than it feels like from the inside. No sense of loss means no why now, and without a why now there is nothing to sell. If they come back and ask for it, you have something. That is the moment the whole model turns on, and it is worth engineering your trial so that this moment arrives early and unambiguously.

Then two questions, and people answer only the first. Is the price one they are happy to pay? And is that price profitable for you? If you cannot get revenue at all, that is the problem to solve, and it is not a marketing problem. And one trap: do not reach for a subscription by default. Charging rent for something people are not using is a worse business than being paid when you deliver. *Price it, then give it away* takes the next step, which is defining the thing, pricing it, and offering it free to the people who already know you.

## Five days, ten customers, twenty-two minutes

Here is what the loop looks like with dates, from my own repositories. In October 2026 I asked this site's agent to check my memory of SG/Send against its briefs and commits, because I knew the order I remembered would be wrong in places, and it was.

SG/Send started because sending a file securely to someone was harder than it should be, and because I wanted a service where the server holds nothing: the best way to protect an asset is not to have it. The first commit was on 8 February 2026, with a specification that set the rule everything since has followed: "files are encrypted on the client before upload, and the decryption key is never sent to the server." On 13 February, send.sgraph.ai was live. Five days.

Then I took it to market, end to end, which is where I learnt Stripe, pricing and everything else a real product needs; by the time I built the newsroom I already knew how, which is how exploring something early pays off later, in a way nobody plans. The Stripe checkout went live on 1 March. On 2 March there were ten paying customers, recruited with a simple offer: buy £5 of credits and I would send a £5 Amazon voucher. "Several declined the Amazon voucher." A number I used to say, thirty paying customers, appears only in an investor one-pager and could not be verified; ten is the recorded number, and ten is what the book says.

The first feature request came the same day. A user wanted to send a folder, not a file. At 20:26 the proposal for folder upload as a client-side zip was committed; at 20:48 the implementation; at 22:15 a viewer for the zip on the download page. The debrief the next morning: "First feature request (folder upload) shipped in 90 minutes." That is what a tight loop feels like from the inside.

The pace behind it: 4,476 commits on the SG/Send app on 246 of its first 249 days, 739 release tags from v0.1.0 to v0.34.0, and the command line's unit tests grew from 237 on 5 March to 4,232 on 14 October.

## What the market said

The technology worked. The use case did not land, and the briefs said so three days after the first customers. On 5 March: "We have paying customers but not enough usage. Users buy credits, test once, and don't come back. Credits sit unused."

Read that against the test above. People took it when it was free, and some paid when asked by someone they knew. Then nobody ran out of credits and came back for more, and nobody came back asking for the next feature. That silence was the signal. It was the miss-it test, failed, and I had the numbers to see it. I should say that the usage is described, not counted: the briefs say the credits sat unused, and no usage figures were found.

It was a platform without a workflow that needed it. The difference now is that I have the workflows: the newsroom, RiskMandate and the vaults themselves need exactly the features SG/Send built, which is why the same features are used every day. Explorers find things early; the use case decides when they matter. If you build something that works and nobody uses yet, that is not a verdict on the thing. It is a verdict on the why now, and a why now can arrive later, from a direction you did not plan.

## The test applies to you

A strong connection with users is critical, and everybody says so. What is said less often is who the most important users are: the people building the product, and above all the people who control its roadmap. If the developers, the product owner and the founder use it every day on real work, the loop between using it and changing it is as short as it can be. They feel the friction first. They find the uses nobody planned. They know, without a survey, which of the hundred possible next features is the one that hurts. I think this is one of the reasons Apple is so good at what it does, as far as I can see from the outside: the people there use what they make.

This is brutal to say about my own work, and it is true. My last startups were good ideas. The Cyber Boardroom, MyFeeds, and early on even sgit as a startup. I still think they are good ideas. But I was not using them, and that was the signal I should have listened to. If I have access, I can change it, I can do a lot with it, and I still do not use it, then something is missing, and it is not the code. Why those companies did not take off has more than one reason; not using them is the one I can see most clearly and the one I can act on.

The vaults are the opposite story. I create them for almost everything, my agents create them, we share them, and 54 are published on sgit.ai with their read keys. They are getting really good, and it is not because of a roadmap. It is because every day I hit something, and the next release fixes it. One user is not a market. But I have seen the other pattern in startups many times: a product whose own team uses something else, or uses it only for the demo. Nothing in the code says so. The behaviour of the team does, and it usually means the product is not as good as it looks, or not as simple to deploy, or valuable only in a narrow case.

So before you ask whether a stranger misses it, ask whether you would. If you have spent twenty-five years in your field and you would not pick up your own tool on Monday morning, you have your answer early and cheaply.

## The loop is the moat

I said in *Be a founder* that the technology is not the moat. What is defensible is the data, the relationships, the distribution, or the speed at which you ship. Using your own product makes the last one concrete.

With agents, we can develop just about anything, in any direction. What we cannot generate is the sense of what to build next, for whom, and when to stop. Context and focus come from somewhere, and the most reliable place they come from is using the thing. When I say I miss a feature, that is not a complaint. It is the product telling me where it wants to go, through the only user whose day it fully controls. *Direction is the scarce skill* makes the general case; this is the founder's case.

A workflow I now have most days: somebody makes a comment, I write an article, a feature ships, and I use it. I put myself as a user in the middle of the loop, deliberately. In October 2026 a reading list made for one person went from brief to live in 81 minutes, and a link to a persona from brief to live in 17 hours; the times are from the git logs. Fast prototyping to production, and fast release, is what is hard to copy, much harder than any single feature. A competitor can take your code. They cannot take the loop.

> **For Dinis:** the five-day, ten-customer, 90-minute story is told here with the dates the research agents confirmed, and the thirty-customer figure is named as unverified. Do you want the SG/Send story in this chapter at this length, or kept short here and told in full in *Your first price and your first ten customers*?

In 2018 I asked what was stopping you, and said it was just you. The version for 2026 is shorter. Ship it. Give it away. Take it away. Ask. Then do whatever the answer tells you, including the thing you did not want to hear.
