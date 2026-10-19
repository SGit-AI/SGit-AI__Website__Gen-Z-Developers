---
title: Explorer coding, not vibe coding, and the handover
slug: explorer-coding-and-the-handover
part: the-frame
number: 9
ideas: [explorer-coding, the-handover, the-villagers-craft, explorer-coding-not-vibe-coding, no-new-features-during-the-move, the-agents-leave-a-record, the-bonus-test-is-accountability, not-ready-to-be-in-line, an-explorer-version-of-every-product]
answers_2018: [5.concepts/repl.md, 5.concepts/legacy-applications.md, 4.life-patterns/refactoring.md]
sources: [art:gen-zx-developers, news:explorer-coding, news:saas-apocalypse-decided-by-inertia-not-by-ai, news:a-browser-for-one, news:who-will-fix-your-mess, news:the-citizen-developer, news:explorer-to-villager-newsroom, news:move-the-cloud-not-the-code, art:where-the-thinking-came-from, book:5.concepts/repl.md, book:5.concepts/legacy-applications.md, book:4.life-patterns/refactoring.md]
character: marta
gravity: explorer
status: draft
---

If you have spent twenty years inside a problem, you have described the software you needed more than once: to a vendor, who sold you the product that did most of it; to a spreadsheet, when nobody else would listen. You were always the person who knew what the tool should do. What you never had was a way to build it yourself. Now you describe it to an agent, and it appears.

People call that vibe coding. This chapter says why I do not, and what comes after it. The entrepreneurs this book is for are developers: they are coding, with agents, and the way they do it has two halves, the exploring and the handover. A founder needs both.

## From vibe coding to explorer coding

The phrase is Andrej Karpathy's, from a post in February 2025: "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists."

I think the word is doing harm. It sounds as if people are just typing, going with a feeling. It hides what is happening. Andrew Ng said in May 2025 that coding with AI is "a deeply intellectual exercise".

What the word actually describes is people writing very good briefs. Everybody was already vibe coding, just very slowly: the loop from *I want this* to *here it is* was weeks or months. The brief was fine. The execution was the bottleneck. Now the loop is minutes, and a thing that was always true becomes visible: very few products let you strip out the 90% you do not want and keep the 10% you do. That 10% is exactly what you can now build.

So I would like to propose a better name: explorer coding. The word is already in Wardley maps, which *Where do you land?* introduced. Explorers, in Simon Wardley's words, "explore never-before-discovered concepts, the uncharted land"; "They show you wonder but they fail a lot." What people call vibe coding is exploration, and the word should say so.

## The founder's way of building

The first edition had an outline called *REPL*, Read Execute Print Loop, the oldest fast feedback loop in programming: type a line, see the result, type the next. One bullet said the idea was "still not very well understood and used". I thought it was for programmers; it explains what everyone is doing now.

People have always built software with whatever they controlled, and for most of them it was a spreadsheet. Spreadsheets won because of the feedback loop: change a cell and see the result, a read-evaluate-print loop for people who would never call it that. Now the loop is fast for anything. It is the best thing to happen to software since the spreadsheet.

My own example is small. The browsers on my phone had frustrated me for years. Then, after weeks of building with agents, writing my own browser for one site stopped sounding unreasonable, and I wrote the brief. What changed was not the browsers. It was me. Frustration plus the power to build is where explorer coding starts; for a founder the frustration is older and the stakes higher.

Explorer coding is not a way to ship. It is a way to find out. What explorers produce is the best brief there is: a working app says what its user wants better than any document, because it runs. That is the first half. The second half begins when somebody else wants it.

## Not ready to be in line

An explorer-coded app may look like an application and feel like an application, but it is a brief. Nobody has read the code. Nobody has validated the architecture. It is not ready to be *in line*: in the path of work that other people depend on.

The trap is that dependence comes quickly. Once something gets used, it is mission critical, even for one person, if it replaced how they work. For a founder, that person is your first customer. The first edition's outline *Legacy Applications* had the bullet "The code you are writing today will be legacy tomorrow." Explorer code becomes legacy the moment someone relies on it.

The direction is set by where the code sits on the map. The further towards commodity, the fewer agents in line, and the more deterministic the code. I have argued it in the newsroom for code review: "A model has no place in line on a mission-critical path." The thing that runs your customer's work should not have a model in line.

## The gap is a handover

In October 2026 Harvard Business Review published an article on turning vibe-coded prototypes into tools a company can use. Its argument: the prototype is the easy part, and turning it into a tool people rely on every day is the hard part, the deployment gap. One author's post opened: "'Build or buy in the age of AI?' Wrong question. The real one is: 'Who will fix your mess?'" I have read the summary and the post, not the paywalled article.

I agree with almost all of it, and would change two things. First, I would not start from the mess. The prototype is not a mess. It is the most precise requirement the company has ever had: a brief that runs. The mistake is to confuse the brief with a product. People never bought software as a service for the features; they bought it because the thing is maintained. Every non-functional requirement the vendor paid for now lands on an application a non-engineer built in an afternoon, and that person does not want to maintain it. They want to build it and hand it over.

Second, the gap is not a place to stop. It is a handover between people with different skills. Explorers find what is needed. Villagers make it reliable: tests, data handling, releases that do not break it, and now behaviour policies for the agents that work on it. Town planners run it at scale and own it in production. The article's warning story, a European bank that piloted a Swiss startup's tool, built its own prototype instead, and went back to the startup a year later, is not a story of a weak team. An explorer team was asked to be villagers and town planners as well, on a regulated, daily-use tool the startup had already hardened for many clients.

For a founder this is good news. The future it points at is village and town-planner companies, which take the finished brief and run it, paid by consumption and by the fact that it keeps working, not by the seat. With agents, the handover itself becomes a file move plus a version bump, logged and reviewable. Some of the companies I hope this book starts will be those.

## Make the agents leave a record

The line I most want to answer: "the AI designs the architecture, not your team. So nobody in-house knows how the tool is built." That is true of most agent-built software today. It does not have to be.

If the agents work under a written mandate, keep their memory in a versioned store the company owns, and describe what they built as a graph, the architecture is a record the next team can read, not a mystery. Someone built one on my tools: Mondweep Chakravorty's run of SGit with Ruflo was built with agents, but with its versions pinned, sixteen tests, a folder of evidence, a written behaviour policy, and a README that says plainly what it does not do yet. The record is a proposal, not a standard: my sites run it, and few organisations do yet. I have a stake: my companies sell this kind of record. For your company, it is the difference between a product you own and one only an agent session understood.

## The bonus test is accountability

The post also offered a test for a chief executive: would your team accept a bonus tied to how this tool performs in production? It has a name in the Wardley frame. It is the moment the town planners take the code and answer for it. If nobody will put their name, or their bonus, on a tool in production, it is not ready to be in line, whoever wrote it.

More of the industry says so. The Linux kernel's rules for AI coding assistants say "AI agents MUST NOT add Signed-off-by tags" and "Only humans can legally certify the Developer Certificate of Origin". Fedora's proposed policy says "The contributor is always the author and is fully accountable for their contributions." We cannot make an explorer accountable for code they never read. We can make the team the work is handed to accountable, and the town planners above all. In a company of one, that team is you.

## No new features while you move

The newsroom went through a handover. Its first version had a crazy amount of features, including a meter that charges by how far you read, and it was live and taking money. Measured on 11 October 2026, the live reader code was about 2,700 lines and the tests 433, which the one workflow never ran. That is explorer code, and a mistake in the meter was now a mistake with someone's money. So the brief was to go slow to go fast, in six phases, with no behaviour change until the fifth: map everything; move the code to its own repository as a pure refactoring, "the same behaviour and the same bugs", proved by hashing every file the live site serves before and after; write tests, with every known bug recorded as a test that passes; review; refactor; and only then, the explorer returns.

The rule underneath it holds for any handover, and I repeated it at a digital sovereignty event about moving between clouds. A migration is a pure villager move: take something that works and make it boring, reliable and cheap, without changing what it does. You cannot add new features. It is tempting, and it is the moment everything derails, because now the migration is also a product change, and nobody can tell which of the two broke what. The argument that the move is what will allow the features is right; it is also exactly why the two must not be mixed. Move first, with the code unmodified. Then add the features.

## An explorer version of every product

The name also suggests a commercial model, and if you are about to build a product, I would build it in. Products need an explorer version: users talk to the product with a model, reshape it, move things around and keep their own version; the product is treated as primitives. When a user has something they want to keep, they submit it, and that submission is the brief. They pay to convert it into a villager product, maintained across releases, and, if it matters enough, into a town planner product, built properly or kept as a maintained fork. Each step is a revenue stream, and each submission tells you exactly what your users want. This is a proposal: I know of no vendor selling it yet.

## The villager's craft

The handover is where the people who make things last take over, and their craft has a canon. Design, in the sense that design is how it works and not decoration, became a mandatory step in how my agents build interfaces: every change has to be simpler, and reverting it should feel worse. The wider design canon says every element must earn its place. Christopher Alexander's *A Pattern Language*, from 1977, is where software design patterns came from; its lesson for the town planner is that code is a space people inhabit.

The first edition had a third outline here, *Refactoring*: what it is, and how to apply it to your life. Refactoring is the villager's verb: changing the structure of a thing without changing what it does, with a test to prove it. Applied to a company: build fast to find out what your customers want, then, before they depend on it, slow down and make it something they can rely on.

Even power users want that handover. When my browser for one works, I will not want to maintain it: not because I cannot, because it is not my focus. I would rather pay someone a couple of pounds a month to keep it working. The explorer builds the brief. The villager keeps it alive. A founder is the first, has to arrange for the second, and knowing which one you are on which day is most of the skill.

> **For Dinis:** in a company of one, is the villager someone you hire, a village company you pay by consumption, or you on alternate days? Your answer belongs at the end of this chapter.

> **For Dinis:** the chapter says you read HBR's public summary and Olivier Laplace's post, not the full article. If that has changed since 17 October, the sentence should change with it.
