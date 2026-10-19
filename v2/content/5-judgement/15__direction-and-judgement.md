---
title: Direction is the scarce skill
slug: direction-and-judgement
part: judgement
number: 15
ideas: [direction-is-the-scarce-skill, knowing-when-to-stop, one-way-two-way-doors, agents-decide-people-answer, a-budget-per-step-is-the-objective-good-enough]
answers_2018: [5.concepts/deadlines.md, 4.life-patterns/start-with-why.md, 3.technologies/content/brain.md, 4.life-patterns/one-way-two-way-doors.md, 5.concepts/chaos-engineering.md, 4.life-patterns/civic-responsibility.md]
sources: [news:places-of-highest-leverage, news:not-a-straight-line, news:i-miss-it, art:connect-the-dots-backwards, news:knowing-when-to-stop, news:how-cheap-is-it-to-undo, news:the-human-in-the-loop, news:footprint-and-blast-radius, news:agency-is-not-a-yes, news:who-will-fix-your-mess, news:who-owns-the-words, news:the-policy-draws-the-liability-line, news:riskmandate-ten-questions, news:if-somebody-built-a-company-on-code-review, art:gen-zx-developers, book:3.technologies/content/brain.md, book:5.concepts/deadlines.md, book:4.life-patterns/start-with-why.md, book:4.life-patterns/one-way-two-way-doors.md, book:5.concepts/chaos-engineering.md, book:4.life-patterns/civic-responsibility.md]
character: sam
gravity: town-planner
status: draft
---

One morning in October 2026 I asked the agent that runs my newsroom to read the day's articles and tell me what it could build next. It came back with a long list, all of it possible: an inbox mode, reading modes, automating the wire's daily run, more beats, scheduling, analytics. When the agents can go in every direction, where do you focus?

Direction is the scarce thing. Agents can build in any direction; what they cannot generate is the sense of what to build next, for whom, and when to stop. Providing that is the job, and the thing to hire for. Building stopped being the bottleneck the day anyone could brief an agent. Choosing is what is left. For a founder it is what the company lives or dies by, because nobody else is going to choose.

## Places of highest leverage

My rule has a name I gave it years ago, when I was a CISO: places of highest leverage. At any moment there are many things that could be done. Most are blocked on something. Some are not blocked but would not change much. A few are not blocked and would change a lot. Work on those, and only those, until they stop being that.

It is a rule about where, not what. You start somewhere, and the somewhere can be slightly wrong, because the first step's job is not to be right; it is to produce the second step's information, and by the time I get to the hard part I have better tooling, a better understanding and a better view.

The rule explains why the newsroom solved a problem my company could not. Where to keep a user's master vault key had resisted six months of attempts, each of which failed my simplicity test, because complicated is how security designs fail. The newsroom solved it in two days, because it needed it badly enough: readers on every device I own, and a workflow failing me in a way I could feel. The rule under that is one every founder should write on the wall: always follow the users, even when the user is you, and follow the feedback loops. A problem solved before anybody needs it is solved in the abstract, and abstract solutions are where the complexity creeps in. When I miss a feature in something I built, that is the product telling me where it wants to go. "Focus on one thing only" assumes progress runs in a straight line; it rarely does. Focus is undivided attention on the place of highest leverage, not work on only one product, and the measure is one question: am I getting better?

The 2018 book had drafts on deadlines and on starting with why; the second matters more now, because the better I explain the why in a brief, the better the result.

## Knowing when to stop

The hardest call in most work is not what to do next but when to stop, and this is the part agents lack most. Their range is the feature. But an entity that can go anywhere has no natural reason to stop anywhere. It sees twenty things wrong and has a go at all of them, without the perspective to know that nineteen do not matter, or matter later, or are someone else's.

People have the same problem, with less range. The best security teams I worked with ran out of real work, and then some kept going. I was once called into a meeting where security champions and developers were debating whether GUIDs were random enough: a movie plot, in Bruce Schneier's phrase for the dramatic threats we imagine instead of the ordinary ones that happen. What I did in those rooms was give people perspective: yes, that is technically possible, and it does not matter here, because of who our attackers are, what else is in place and what we are protecting.

That perspective is much of what seniority is: knowing who the attackers are, which phase the business is in, where the bottleneck is, and what good enough looks like. The 2018 chapter on the brain asked "Who is actually making the decisions in your head?" Seniority is an answer to that question: a fast kind of thinking, backed by a bigger picture. An agent has the speed and not the picture, so the picture has to be designed in: a brief that explains the thinking and not only the task; a mandate that only reaches what the job needs; memory that holds the strategy and the threats; a stop named before the work begins; and shipping often enough that users tell you whether it mattered. None of these is a rule that says do less. Each puts the bigger picture where the decision is made.

The junior version is this. Name the stop before you start: a time, a budget, or a result that counts as good enough. And give yourself explicit permission to leave things undone, and write down what you left and why.

## A budget per step

The junior version has a mechanism, and it is the one piece of seniority that can be written down in advance. Agents keep going; that is what they do, and one agent handing work to another looks efficient while it spends. The way to stay on the right side of diminishing returns is a budget per step, decided before anything runs: a ceiling per altitude and per change, so that a workflow's maximum cost is knowable before it runs rather than discovered afterwards. Work handed from agent to agent carries its budget with it and never widens it. And every agent doing the work runs under a behaviour policy written before its first run.

Being able to say to a team that the budget for this is spent was one of the most useful controls I ever had, because teams are very good at keeping going. Much of what gets called over-engineering is work that had no objective way to know it had reached diminishing returns. A budget per step is an objective way to say good enough, and for a founder paying for every token, a bill you planned rather than one you discover.

Then the budget moves, and what moves it is the five whys. Every finding at one layer is a question about the layer below: why did the story stop holding, why did the command change, why did no check catch it? The fix goes below the bug, as a rule or a query, and the next change like it is caught for the price of a query rather than a review. The same discipline says how to start on anything large: at one point, never by analysing everything; the first slice is dear and every later one cheaper.

## Where a person belongs

The 2018 book had an outline on one-way and two-way doors, with a story I attributed to someone at Google: "My metric for approve or not a project is based on how easy it is to roll back the changes (and its impact of real customers)". Jeff Bezos wrote the idea down in his 2015 letter to shareholders: a few decisions are "consequential and irreversible or nearly irreversible"; most are "changeable, reversible", and the mistake is to use the heavy process for both.

> **For Dinis:** the Google executive's test appears in the 2018 outline and again in *How cheap is it to undo*, both times from memory; if the source can be found the book should name it, and if not, say so once.

Now apply the test to every output an agent produces. Not "do I trust the agent", which has no answer, but: if this is wrong, how cheap is it to undo, and what does it break before I do? On 13 October 2026 my newsroom shipped fourteen releases, every commit made by an agent and none approved by a person first. The same day the twelve agents that run my correspondence drafted every email and sent none. An article is a two-way door: a correction is a new version, and the next reader gets the fixed page. An email in my name is a one-way door.

The same test settles a founder's oldest argument, build or buy. The question is how much it costs to reverse a mistake and how mature the controls are. A narrow internal tool that a few people use and that can be switched off is a two-way door: build it, explore, learn. A tool that touches regulated data every day is a one-way door until the controls are mature, and that is where the villagers have to be in place first, yours or a partner's.

A person checking every output is a bottleneck, because it does not scale, and a weak safety net, because people approve almost everything they are shown: Anthropic measured that its coding agent's users approve 93% of permission prompts. Put the person where an output cannot be undone and the blast radius is large: sending in my name, typing a secret, spending money, deleting what has no backup. Everywhere else, use controls that do not get tired: a validator, a policy row enforced outside the model, a record read afterwards.

Blast radius means what it would cost the business if a row of the agent's reach were used in full, today. It is defined over the reach, not the mandate, because whoever takes an agent over inherits its reach and ignores its mandate. And it changes while the action does not. Picture an agent whose cleanup step drops a staging table: nearly empty the first time, six weeks of real records the third. Someone reading the footprint, what the agent actually did, could say: this is not the first time. The 2018 draft on chaos engineering said the first step was to understand and visualise what is going on. It still is.

When the person does review, the review should be worth more than a yes. I once received a permission prompt asking me to add label 756-459-3214. A decider with no options, no context, no time and no authority is not exercising agency; they are holding liability for a decision the system made, and the accountability belongs to whoever designed the decision point. And the record moves the line: when the record of drafts I did not have to change is long enough for one kind of message, that kind can leave my hands, by a decision written into the policy.

## Agents decide, people answer

An early user of my email agents asked the right question. If the agents only gather and draft, and I review and send, does presenting them as a team imply an agency they do not have?

Two things are true at once. These are not sentient beings; they are mirrors that can simulate any emotion, which is why we anthropomorphise them, as people did with Joseph Weizenbaum's ELIZA in 1966. And since models started running in loops and calling tools, they make real decisions: every tool call is a choice. What does not travel with the decision is responsibility. It stays with whoever granted the reach and set the mandate. The moment of authorisation is the moment you granted the reach, not the moment you wrote the mandate; the exposure exists the instant the grant exists.

An Agent Behaviour Policy is a job description for an agent, some agency inside a role, published, and the rows that matter most are the prohibitions: do not send an email directly; do not edit files another agent owns; do not attack other websites, even though you can; speak on your own behalf, never on mine. Most of those are still hope. But a prohibition that is written down and then broken is a different thing in a dispute from no prohibition at all. My hypothesis is that towards the world the deployer still answers, and between deployer and vendor the written policy is what turns "you allowed it" into "your product ignored what it was told".

If your company sells agents, or the policies that run them, decide early where you stand. Mine carries none of its customers' risk, by design, through three firebreaks: we are not in the request path; the customer's agent executes; and every prompt or policy we hand over is reviewed and put into production by someone on the customer's side. Accountability sits with whoever runs the system. Which side you are on is a one-way door.

The 2018 book had a draft on civic responsibility that said "code is law", and that developers should give the risks they create to business owners and make them accountable for the decisions they are making. The behaviour policy is that sentence, written down for an agent. What remains valuable, as fluent writing becomes a commodity, is judgement, and someone who owns it: who decided this is true, who decided to send it, who will answer for it. That is the person who gets paid, the person I would hire, and the person a customer is buying when they buy from a founder.
