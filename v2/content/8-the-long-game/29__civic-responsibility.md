---
title: Civic responsibility
slug: civic-responsibility
part: the-long-game
number: 29
ideas: [hack-your-country, the-plumbing-is-the-states-road, what-the-state-pays-for-belongs-to-the-commons, smaller-models-more-of-them]
answers_2018: [4.life-patterns/civic-responsibility.md]
sources: [book:4.life-patterns/civic-responsibility.md, news:portugal-2010-a-challenge, news:portugal-2016-hacking-portugal, news:judo-for-small-countries, news:sovereignty-is-the-ability-to-move, news:move-the-cloud-not-the-code, art:gen-zx-developers]
character: guide
gravity: all
status: draft
---

The 2018 book had an outline called *Civic Responsibility* that I never wrote up. Its notes were six lines. As a developer you have a major civic responsibility. Code is law. You are one of the most important pieces of the puzzle. You can choose where you work and whether your code has a positive or negative impact in the world, and if you cannot choose that at the moment, make sure you are actively looking to change your job. Give the risks you create to the business owners, and make them accountable for the decisions they are making.

I am writing that chapter now, with my own country, because that is where I have made this argument for sixteen years, and the record of what came true and what did not is a better teacher than a list of principles. And I am writing it for a founder, because in 2026 the person who chooses where the code goes is, more and more, the person who started the company.

## Lisbon, 2010 and 2016

On 17 December 2010 I gave the keynote at OWASP's IBWAS conference in Lisbon: 168 slides, five proposed focuses and twelve proposed actions for government and industry, from allowing ethical hacking to liability for software and "'Proper' SSL support for 50% of websites". It ended by arguing that Portugal, which had "nothing to lose", could become the Switzerland of hacking. What I asked for "doesn't cost any money"; "It only takes courage, focus and commitment".

Sixteen years later, more of it came true than I expected, though mostly from Brussels rather than Lisbon: from 9 December 2026 the EU's Product Liability Directive brings software under strict, no-fault liability, and since 11 September 2026 the Cyber Resilience Act requires manufacturers to report actively exploited vulnerabilities within 24 hours. What I got wrong was the mechanism. I thought fear of a disaster would move governments quickly. What moved them was a decade of slow, unglamorous regulation.

On 11 November 2016 I gave the keynote at BSidesLisbon, *Hacking Portugal*, 103 slides, and three weeks later published it as a book on Leanpub, 75 pages. Its first lines are the premise of this chapter: "If the word 'hack' means to solve problems, then 'Hacking Portugal' means to find innovative ways to solve existing problems." The ideas were blunt. Make the Portuguese network hostile to insecure code. Replace the old compulsory military service with a Portuguese Hacking Service for 15 to 21 year olds. A hackathon league as famous as football. *OpenSource.pt*: all code paid for by government released under an open-source licence. A Ministry of Code.

Ten years on, the Hacking Service, the league and the Ministry of Code have not happened, as far as I know. The best news is in the spirit of OpenSource.pt: on 1 July 2026 Portugal released Amália, a national language model for European Portuguese, built by a consortium of universities with 5.5 million euros of EU recovery money and published with its dataset and code under an open licence.

And the biggest change is one I did not see in 2016. Then, learning to hack meant learning to code first. Now a sixteen-year-old can explore a system by talking to it, which *Explorer coding, not vibe coding, and the handover* called explorer coding. The talk's central claim, that a small country can choose to lead in code, is more possible than it was, because everyone who can brief an agent can now build.

## The plumbing is the state's road

The conversation about a national AI strategy keeps circling the biggest model, the most GPUs, the largest data centre. On a Wardley map those sit at the far right, in commodity, with a lead held by companies that have invested amounts a small country's whole technology budget would not match. A small country should not enter that race.

Put a person at the top of it: a developer in Cluj, a designer in Porto, a pharmacist in Braga with twenty-five years inside a problem, selling a service to a buyer abroad. What stops them is not talent, energy or price. It is forming a company, hiring across a border, being paid across Europe, working in a language the buyer reads, a contract, an invoice, a tax form valid on both sides. None of that is the service. All of it is plumbing, and in most of Europe each piece is custom built by the person who needs it, which means built badly, late, and at a cost that falls on the wrong side. In the last Eurostat figures with a breakdown, for 2021, 18.5 percent of EU enterprises sold online to customers in their own country, 8.1 percent to other EU countries and 4.6 percent to the rest of the world. Commerce does not happen, most of the time, because of attrition.

If you have read *The company itself: the UK, Portugal, Lithuania, the European Union* and done *Form your company*, you have met every one of those pieces, and you built them alone. We understand that a government builds roads, because they enable everybody. The shop that opens on the new road did not pay for the road; it paid taxes. Yet we ask every person who wants to sell a service out of a small country to build their own road first. That plumbing is infrastructure in the road sense, and a state that builds it enables all of its people at once.

Estonia did it. A person anywhere can become an e-resident and form an Estonian company online; the programme's dashboard lists more than 142,000 e-residents and more than 43,000 companies, and in 2026 alone e-residents had founded more than 4,200 companies by mid-September. Underneath sits X-Road, which connects around a thousand organisations and is open source under the MIT licence, so another country can take the road rather than draw it again. Estonia is a case study, not a template; the claim is that the pattern transfers.

I have paid for the absence of this plumbing myself. As a CISO and a CTO I spent millions on Upwork building distributed teams, and it worked only because we built the infrastructure around it first; the infrastructure is the whole difference between a talent market that works and a race to the bottom. Those numbers are mine, and this chapter cannot prove them.

## What the state pays for belongs to the commons

The plumbing has to be open source and run on open schemas, because that is what turns infrastructure into sovereignty. A road with a toll gate owned by one company is lock-in with tarmac. You cannot have sovereignty without open source and open schemas, because sovereignty means you can leave. Independence is the ability to run a parallel service, move the data and keep going.

It follows that what the state pays for should belong to the commons. Not so everyone changes the production system, but so everyone can see it, run it and leave with their data. That is how the local industry around it comes into being: an ecosystem of smaller firms, yours among them, can only grow around infrastructure it is allowed to see.

And a market for the alternative does not appear on the day the single point of failure fails. So create the demand before the day you need it. Run parallel services. Buy the local or open alternative for part of the estate now, and accept that it has fewer features, because the point is that when the day comes there is somewhere to go. Procurement is the lever a state already holds; it needs no new law to prefer open schemas and data mobility. It is a resilience case, not an ideological one.

The hyperscalers know this argument. AWS's European Sovereign Cloud went live on 15 January 2026, operated by EU residents. It is a real step, and it makes the point: your code still talks to one vendor's API under one vendor's terms, and sovereignty that depends on one company's API is sovereignty by permission. What stops workloads moving is code, not policy, so the answer I am building towards is a twin: an open source service the application cannot tell from the real one, so the destination becomes a setting and not a rewrite. For an operator in Romania, Portugal or the UK it is a business, and a judo move: the customer's existing code, the hyperscaler's own API and open source, used as the weight rather than fought.

The playbook, in five moves: map the attrition, every place commerce stops between a talented person and a buyer abroad; commoditise the plumbing, built once, open to all; create the demand, before the day you need it; put the money where the market is still genesis, small models, data that stays with its owner, agents with the least agency, not GPUs; regulate what settled, after the market and not before it. This is not a national strategy. It is a map and a set of moves from one person's experience.

## Smaller models, more of them

Most work does not need a frontier model and should not use one. Frontier models are for finding the art of the possible. For things that have to work, every day, at a price, a frontier model is too expensive, too much power for the task, and dangerous in proportion. Give an agent the least agency that does the job, because that is what you can trust. The right end state is the one *Serverless, for real* described for your own product: the model is used once to build the tool, and production is plain files and plain code, with no prompt in the path.

That means small models, and many of them. There is a market, still at genesis, for Portuguese, and not one Portuguese: the Portuguese of Portugal and of Brazil, of Angola, of Cape Verde, of Mozambique, each with its culture in the training data and not just its spelling. Amália is the right shape: a public model is a public road. For a founder, that end of the map is where a small company can still lead.

Treat constraints as the input, not the excuse. DeepSeek's own report says its V3 model was trained in 2.788 million GPU hours on export-restricted H800 chips whose interconnect was deliberately throttled. The dollar figure is disputed and I do not rely on it. The lab that could not buy the chips did the interesting work, and yours will too.

## Sovereignty is the ability to move

In padel, which I am learning, the striking thing about a good player is how much time they have. They read the ball and they are already where it will be. The ball today is the frontier model and the data centre; where the ball is going is the ability to move: workloads, data and the actions agents take, from one provider to another, when you decide and not on the day a supplier decides for you. Technology sovereignty is the ability to move, almost liquidity.

The test is a Wardley map with one question. Put the customer at the top, the service, the application, the data, and under them the products and commodities you buy. For each dot you do not control: take it away, what happens? If the service stops, you have found the problem, and it belongs on the risk register with a name next to it. That is what the 2018 outline meant by giving the risks you create to the business owners. In your own company, that name is yours.

Nobody gets from zero to a hundred. The bar is not an alternative as good as today; it is one that works for the minimum viable company, the priority customers and the services that must never stop. Run it in QA, all the time, on twins of the dependencies you do not control, so that every small problem is found on a Tuesday rather than during an outage. And it has to be open source, because even a European supplier is one acquisition away from not being one. Control that survives a change of owner is the only control that counts.

If you founded the company, you already chose where your code goes. If you are in a small country, you are not behind. You are at the end of the map where the market still exists.

> **For Dinis:** the register notes that a Portuguese edition, or both languages, is your open question, and this chapter is the one it bears on most. Which is it, and does the Hacking Portugal material stay here or move to the new edition of that book?

In 2010 I said what I asked for would cost no money, only courage, focus and commitment. In 2016 I said to hack means to solve problems. Both still hold. What has changed is who can do the hacking: in 2016 the people who had learned to code, now anyone who can brief an agent, which makes the civic responsibility wider, not narrower. You are one of the most important pieces of the puzzle. Act like it.
