---
title: Controlling your agent, and security for the agent era
slug: controlling-your-agent
part: building-safely
number: 16
ideas: [mandate-reach-gap, code-is-a-liability, learn-to-hack, secrets-never-in-the-chat, security-as-a-business-tool]
answers_2018: [6.security/threat-modeling.md, 6.security/3rd-party-modules.md, 6.security/security-better-developers.md, 4.life-patterns/learn-to-hack.md, 6.security/pointers.md, 6.security/strings-should-be-banned.md, 4.life-patterns/content/future-needs-you.md]
sources: [news:what-can-your-agent-reach, news:are-hooks-the-sweet-spot, news:attacks-rewritten-as-mandates, news:three-policies-for-an-agent, news:the-code-you-do-not-ship, news:the-minimum-code-below, news:who-are-you-protecting-against, news:fix-the-page-yourself, news:portugal-2016-hacking-portugal, news:handing-secrets-to-agents, news:seven-vaults-one-method, news:skill-behaviour-policy, news:no-server-by-design, book:6.security/threat-modeling.md, book:6.security/3rd-party-modules.md, book:6.security/security-better-developers.md, book:4.life-patterns/learn-to-hack.md, book:6.security/strings-should-be-banned.md, book:4.life-patterns/content/future-needs-you.md]
character: sam
gravity: town-planner
status: draft
---

The first edition had a whole part on security, and most of it is bullets I never wrote up. *Learn to Hack* was four lines, the last of them the one that mattered: "in order to write secure code you need to understand how to exploit it". *Threat Modeling* said the technique "helps with the two curses of developers": changes to the brief, and the lack of accountability for those changes. Then the thing that takes the brief became an agent. This is the chapter for the person who will be asked, after something goes wrong, what the agent was allowed to do.

## Mandate, reach and the gap

When you connect an agent to something, it gets a credential, and that credential lets it do far more than the job you had in mind. So before you give an agent access, write down four things. Its **reach**: what the credential actually lets it touch. Its **mandate**: what you authorised it to do. The **gap** between them, which *What can your agent reach?* calls "authority nobody ever accepted". And for every capability in the gap, the **barrier**: what actually stands in the way.

There are four kinds of barrier, and only one bounds anything: nothing; a rule written in the prompt; a setting the agent's own account can change; and a boundary enforced above the agent, out of its reach. The test is one sentence: "A control bounds a grant only if it is enforced by something the grant does not include." Most of what gets called an agent control is a line in a prompt. I call that hope-based security: the rule holds because the model keeps it. The agent that writes the newsroom works under a policy of eleven rules, and when I measured it, ten were kept by the agent's good behaviour. Rules in a prompt are hope. Rules in a hook, a gateway or the platform are enforcement. *Are hooks the sweet spot?* records my attempt to move those eleven rules into hooks: four moved fully, two mostly, three partly and two not at all.

A behaviour policy answers "may it?". It does not answer "is it right?". An agent allowed to refund up to $200 refunds $150 to a customer owed $120, and every control passes. So there are three policies, not one. Behaviour says what the agent may do. Decision says, at a branch point, who chooses, on what evidence, within what limits, and who is called when the case is out of bounds. Workflow says which steps run, in what order.

One company that rebuilds open source from source keeps a public ledger of supply-chain attacks: 28 incidents from May 2024 to October 2026, 23 of them from 2026. Every row is reach beyond mandate. By my reading, a control on the consumer's side would likely have held in 26 of the 28; a written answer to what a credential was for, on the publisher's side, in 16. The first is a product you can buy. The second is a document almost nobody has written. My 2018 outline on third-party modules had seen half of it: the reason more libraries had not been compromised was not that they were built securely, it was that attackers had no business model. They have one now, and the next maintainer holding a publish token is an agent.

## Code is a liability

Every line of code that ships is a capability. In my career the vulnerability was rarely in the thing the application was for. It was in something the application could also do, that nobody had asked it to. A library that parses a hundred formats, in an application that reads one, has a reach of a hundred and a mandate of one.

Log4Shell is the clean example. In 2013 someone asked for a convenience, a lookup inside log messages, and anyone who could get a string into a log could make the server fetch and run code. The fix was not a patch; version 2.16.0 said "Completely remove support for Message Lookups". My 2018 outline *Strings should be banned* was the same instinct: "You never want a string, you want a specific type". A string is a grant of anything.

I have argued for removing code for years, and it never scaled. Removing code safely needs a map of what each piece is for and tests good enough to prove nothing broke, and vendors were paid for new features, not for less. Both are weaker now, because the most useful thing models have done for my engineering is not writing the feature but everything around it: the harness, the fixtures, the check that proves a change broke nothing that matters. We measured it on our own tool: of 1,500 files in sgit and its dependencies, 428 ran for one real use case, and a tree holding only those passed it. Commands outside the use case failed, because their code was not there. The capability is gone, not just unused. *The minimum code below* records the limits too.

So the direction of travel is the minimal viable code path: the smallest code that does exactly the job. The best code to protect is the code that is not there. If you want one line on a CV that a security person will stop at, it is a pull request that removed something, with the proof that nothing broke.

## Learn to hack, and name the attacker

The 2018 line still holds: to write secure code you need to understand how to exploit it. *Security creates better developers* said why: security "requires to go deep", and it promotes a problem-solving, pragmatic approach that is useful everywhere else. In my 2016 keynote in Lisbon I put it as a definition: if the word hack means to solve problems, then hacking a country means finding new ways to solve its problems. In 2016 learning to hack meant learning to code first. Now a sixteen-year-old can explore a system by talking to it, with a mandate that says what they may and may not touch.

My own habit, when most of my work was finding vulnerabilities, was the bookmarklet: a bookmark whose address is a line of JavaScript, so an attack is something you click rather than describe. On one assessment I wrapped a flaw that let one user see data they should never have seen in a bookmarklet with a quick interface, and handed it to the business owner. She was far more excited about the interface than about the vulnerability. *Fix the page yourself* tells the story. Learning to break things teaches you how they work, and sometimes how they should have worked.

Then draw the line where the attacker is, not above it. Three questions come before any control: who is the threat agent, what is the attack vector, and how sophisticated are they. *Who are you protecting against?* turns that into a ladder of six tiers, from your own mistakes to states. The encouraging truth is at the bottom, in the NCSC's words: "Organisations that defend effectively against commodity threats present a very hard target for all attackers." Draw the line too high and you protect against an attacker who is not there: sell something better than what the customer has, not something beyond what they need.

> **For Dinis:** the 2018 outline on third-party modules asked for the story behind the developers who thought of mining coins from users with the sleep function, and a simulated npm hack story. Only you know whether either belongs here.

## Secrets never in the chat

A rule from running agents every day. The more a prompt insists that a value is a secret, the more likely the model is to refuse to use it at all. And an agent told something cannot untell it: the session transcript holds everything the model was told. So the secret goes from the drop into the tool, never into the chat. The instructions say what to run; the secret travels through a pipe into the command and never enters the prompt, the transcript or the model's context. *Handing secrets to agents* ran that end to end.

The rule before that one is to classify the credential before it touches anything. When we published seven encrypted vaults in a fortnight, three arrived as a vault key, which is write access, described as a read key. They were caught by shape, and a catch that depends on somebody looking is not a control, so it became a script, then a tripwire in the build, which has caught its own author three times. As *Seven vaults, one method* puts it, "a rule that only catches other people is not a rule." The 2018 chapter *The future needs you* set a project for exactly this: a tool to search git history, because secrets "deleted" with a commit are still there.

The shape to fear has a name, the lethal trifecta: private data, untrusted content and a way out, in one place. I ran a static reader over 899 public agent skills: 812 could reach something beyond their own scripts, and 39 had a feature their description never mentioned. The clearest case was an honest one, a skill that reads your chat history, searches a public forum and posts a report to a chat channel. It says so, and it still needs a control.

## Security as a business tool

I have spent my career in security, and that experience is exactly what lets me say: yes, let's deploy a system with a list of security gaps, because the gaps do not match our readers. The newsroom's reading meter runs entirely in the browser, and *No server, by design* writes the gaps down. A reader can edit their balance in the developer tools, open a private window and start again at £5, open the topped-up page with an invented payment id and credit themselves. Every one of those changes a number only the cheater sees. Closing them would need accounts, a database, a server, a webhook and a sign-up wall between the reader and the page. The model also says what would change the call: if the balance ever unlocked something, the gaps would stop being acceptable, and that feature would get a signed receipt or a server, and not before.

Ask who you are protecting against. Accept, in writing, what does not match the threat. Name the condition that would make the gaps unacceptable. Then publish the threat model on one page and ask people who have seen the attack whether your line is too low or too high. The five synthetic readers we ran through the site found no security problem; what they found was that "credit can go below zero" reads as a debt to someone worried about money. The gaps' cost landed in the words on the page, and that is where we fixed it.

The 2018 threat-modelling outline ended with the right sentence: a threat model "leads to the creation of risks which are then given to the business owners". Every risk is already accepted; the only question is by whom. The person worth hiring is the one who can list the gaps, match them to the people who will actually use the thing, and say what would change the call.
