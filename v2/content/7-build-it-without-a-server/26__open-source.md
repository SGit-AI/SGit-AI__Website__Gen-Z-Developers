---
title: Open source
slug: open-source
part: build-it-without-a-server
number: 26
ideas: [the-fork-next-door, first-pr, open-source-community-as-the-way-in, open-source-removes-the-moat-excuse, open-source-all-of-it-or-it-is-an-evaluation-version, sell-the-build-not-the-code, open-source-is-not-free]
answers_2018: [2.mvp-for-gen-z-dev/content/open-source.md, 2.mvp-for-gen-z-dev/content/creative-commons.md, 2.mvp-for-gen-z-dev/draft/github-flow.md]
sources: [art:gen-zx-developers, news:the-fork-next-door, news:what-open-source-is-and-is-not, news:the-eyeballs-get-cheap, news:sell-dont-issue, news:who-will-fix-your-mess, news:open-source-is-not-free, news:the-value-of-constraints, news:riskmandate-ten-questions, news:our-first-pr-in-ruflo, news:act-as-the-job-you-want, news:no-server-by-design, news:the-question-is-whether-they-miss-it, art:where-the-thinking-came-from, book:2.mvp-for-gen-z-dev/content/open-source.md, book:2.mvp-for-gen-z-dev/content/owasp.md, book:2.mvp-for-gen-z-dev/content/creative-commons.md, book:2.mvp-for-gen-z-dev/draft/github-flow.md]
character: tomas
gravity: all
status: draft
---

In 2018 I asked a question I already knew the answer to: "Why don't you open source your code?" The answers, I wrote, would be some mix of "I don't think my code is good enough", "I'm embarrassed about my code" and "Nobody will want to use my code". My advice was blunt: "The key is to just do it!" Create a repository, add a licence file, and that is it. Then I told the truth about what happens next: "Nothing!" Most open source is maintained by a very small number of people.

Eight years on, everything in that chapter still holds, and the reason to do it has become clearer to me, and sharper now that the reader may be starting a company rather than joining one. It was never about contributions. It is that nobody can lock you in, and that includes you.

## What open source is, and what it is not

Open source is a copyright licence: the holder using the right to control copying to grant the opposite, you may copy, use, change and share, on these terms. The GNU General Public License, in 1989, made sharing a condition; the term "open source" came in 1998 as a pragmatic reframing of the same freedoms for businesses. The repositories behind the newsroom are Apache 2.0 for code and Creative Commons for writing, and this book is CC BY 4.0, as the first edition was.

One thing I believed for a while, and was wrong about: that the most open thing was not to licence at all. With no licence, all rights are reserved; if you want people to use your work, a licence is how you say so.

At an event in October 2026 I heard misconceptions that are now common among developers who use open source every day without having grown up in its culture, and *What open source is, and what it is not* corrects six: that nobody controls it (a few maintainers do, visibly); that anybody contributes (almost every project is a handful of people); that it is more, or less, secure than proprietary software (the metric is whether somebody was paid to review it); that it costs nothing; that open weights are open source (weights are a compiled binary); and the one I just confessed to. Through all of it, one sentence from 2018 is the one I would keep. When I see an application given away for free, as in zero cost rather than as in freedom, "I always think 'What is their agenda?'"

## The fork next door

Here is why that matters to a company. In a healthy startup everything is open source, so the technology is not the moat; customers stay for the service, the quality and the trust. Now ask what happens when one corner goes wrong. In an open source company every corner has an exit, and the exit takes the technology with it. If the founders stop executing, investors can fund a team to run the same code next door. If a new owner changes direction or the licence, the founders can leave with the code. If anyone lets the customers down, the customers can move, as long as their data moves with them. *The fork next door* lays the triangle out.

Forks are rare and serious: in a study of 220 significant forks, only 7 merged back. So the real defence is execution, and in the agent era, speed. The moat is a rate, not a wall: "A competitor who forks our code today gets our position as of today. They do not get our velocity."

This is also the answer to the investor who asks what happens if the founder goes rogue, which *Fund it, or do not* comes back to. In a conventional round, control is the insurance: the right to replace the founder. Here the fork is the insurance: the right to replace the company. The fork disciplines the founder because it is possible and protects the founder because it is slow. Two conditions make it real: a genuinely open licence, not open core, and a copyright structure not gathered into one corporate holder. The same protection works for your customer: with the code open and the record kept, "who will fix it?" has many answers, your team, the partner, another partner, or the agents, under a mandate, reading the record.

The security argument has moved too. Eric Raymond's line was "Given enough eyeballs, all bugs are shallow", and the honest answer was always that the eyeballs were not there. Models can now run deep security reviews, over and over, at a cost that used to buy one consultant for a day; *The eyeballs get cheap* tells curl's year, ending with a frontier scan that found one vulnerability, "yes, as in singular one". The thing open source lacked was paid attention, and that is what just became abundant. It is why I think open source is about to become the most secure software we have.

## Open source is not free

Somebody is paying for open source, even if only with their time. I gave my agents an old iMac as a desktop of their own, clean-installed with the newest system it would take, and the package manager would not install, the container tool would not install. Every project that dropped that machine did it for the same reason: supporting it costs money, in CI hardware and maintainer time, and the people who still need the support are not the ones paying.

The long tail is measurable and not small. In Homebrew's install analytics, 6.99% of macOS install events in the last 30 days, and 16.66% over a year, came from versions older than the newest three; on PyPI, 18.55% of pip downloads run on end-of-life Python. Money flows to old versions when a vendor owns them and not when a community does: Oracle earned $19.8 billion from support last year; Red Hat's subscriptions ran at about 93% gross margin; open source as a whole receives about 0.09% of its estimated value in investment, and in one survey 60% of maintainers describe themselves as unpaid hobbyists. The xz maintainer wrote "this is an unpaid hobby project" two years before the backdoor. The question was never whether somebody pays. It is whether the people who get the value have an easy way to pay for it.

## All of it, or it is an evaluation version

For a founder, open source is a constraint, and its value is in what it takes away. There is no private code. That makes the code easy to deploy, run and change, including by the customer, which solves a lot of sovereignty problems on its own. And it removes two temptations. The first is to lock the customer in; without lock-in, the only reason anyone uses the product is that they want to, and the best product is not the one you use because you have to but the one that hurts when you stop. The second is what I think is the curse of most startups: they win customers, and the customers get them to build every feature and integration only they need, until the roadmap belongs to everyone but the startup. With open source the answer is: here is the code; integrate it yourself, or pay us to do that specific thing.

That is why you cannot open source half of it. A community edition that turns proprietary as soon as you use it for real is an evaluation version with a better name. Elastic, HashiCorp and Redis each moved to a licence that is not open source, each produced a well-funded fork backed by the cloud providers it targeted, OpenSearch, OpenTofu and Valkey, and two of the three have since added an open licence back. The Open Source Initiative's verdict on one of those licences was that it was not an open source licence at all.

## Sell the build, not the code

So what do you sell? The two constraints, open code and a server that holds nothing, remove a lot of bad business decisions and leave the good one: you cannot sell access to the code or rent the data back, so you sell customisation, and keeping it working. Everything RiskMandate and sgit build is open source: policies, code, vaults, backend. What the customer buys is a customised, maintained build for them, sometimes with fewer features and so less attack surface, tested on their target, kept working as models, connectors and threats change, with someone accountable for it, and cheaper through us than doing it themselves. The moat is delivery, maintenance and trust, not lock-in.

I tested whether that pays in a model of one project at Homebrew's scale with one long-tail target to keep alive. Donations covered the cost in 24% of draws. Supported builds sold to individuals at about £1.80 a machine a year covered it in half the draws with typical conversion, and no price reached nine in ten. Customised builds for companies, priced below what it costs them to keep the tool working themselves, covered it in 94%. It is a model, not a forecast. But the shape is the one I would build a company on. Not a donation, and not a licence that gives you a reason to make the free version worse. "The value is the support, not the code, so the code can stay open."

## Why it is easy to throw your own technology away

There is a quieter benefit, and it is the one I feel most in my own work. When everything I build is open source, I do not have a moat I have to keep using. There is no part of the stack I need to protect from being replaced, and I am usually the first to try to replace it when something better appears. The habit is to ask of every component whether it is still earning its place, and open source removes the one bad reason to say yes: that I built it. *Serverless, for real* leans on that habit throughout, and *The question is whether they miss it* adds the founder's version: build in the open and the work is still yours when you move on. You leave with your tools.

## Your first pull request

Now the part for the reader going into a job rather than making one. In 2018 I wrote that a great way to get a job in a company is to contribute to an open source project hosted by that company, and the OWASP chapter put it more plainly: most projects are maintained by a couple of people, and all of them need help. *Act as the job you want* adds the 2026 version: if you are looking for a job, you have time, so do the work in public, where it can be linked.

Here is what a good first contribution looks like now. On 16 October 2026, late in the evening, Mondweep Chakravorty opened a pull request against an agent framework with 9,625 commits on its main branch. It added one page, 83 lines of documentation, describing his adapter: a behaviour policy compiled into the framework's own rules, gating memory checkpoints into an encrypted vault. The maintainer merged it the next afternoon; what got it in was the page being specific about what it claims. It pinned the exact commits it depends on. It listed its evidence and its gaps in the same breath: "Semantic quality is NOT validated." A page that does not oversell can be merged in under a day.

That is the bar, and it has risen since 2018: curl's contribution rules now say that if you asked an AI tool to find problems, you must reveal that, so a first pull request today carries its provenance, what you did, what you checked, what you did not. The 2018 outline *GitHub Flow* was five bullets I never wrote up, "Learn how to do Forks, Commits and Pull Requests" among them; the mechanics take an afternoon with an agent beside you.

I should say where this came from, because ideas have a lineage. My own shift into an open source mindset happened, as the 2018 chapter records, "20 years ago after I read" *The Cathedral and the Bazaar*: "Release early. Release often. And listen to your customers." Linus Torvalds built two of the things all of this stands on, Linux and Git. OWASP is where I learnt that knowledge compounds fastest in the open, and some of my best friends in the industry came from it. The 2018 chapter on Creative Commons quoted Tim O'Reilly: "For a typical author, obscurity is a far greater threat than piracy".

> **For Dinis:** your own first pull request to someone else's project, and what it led to; the 2018 chapter says the usual outcome is nothing, and a reader will want the counter-example from your life.

The excuse I hear from careful graduates is the one I heard in 2018: the code is not good enough yet. Put the licence on it, send the small, honest pull request, and let the people who want to help you find something they can link.
