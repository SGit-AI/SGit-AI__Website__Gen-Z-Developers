# The plan: how an article becomes a chapter, and how we know where everything is

*By the librarian, 18 October 2026, from Dinis's message asking for the graph, the mappings and the tracking; revised the same day for the three articles released since. Book version: v1.0.0. This is the operating plan for the second edition's material; the articles it operates on are [the briefs](../briefs/index.html), [this site's articles](../articles/index.html) and [the newsroom, surveyed](../map/newsroom.html). Nothing in it decides what goes in the book: that is Dinis's, through the loop.*

## In short

- **Everything is a node with a state.** A source, an idea, a chapter, a task, a decision. The state answers "what has been done with this" without a spreadsheet.
- **Provenance is an edge.** An idea names the article and the section it came from, the 2018 chapter it answers, and the chapter it goes to. The build refuses a dangling edge.
- **Articles are processed into ideas, not into chapters.** A chapter is made of ideas; an idea can move between chapters, or out of the book, without losing where it came from.
- **Dinis decides at the idea.** Keep, rewrite, merge, cut, article first, later, not doing it: the verbs of [read, comment, decide](../articles/read-comment-decide.html), applied to ideas as well as to 2018 chapters.
- **The librarian keeps the graph.** A role: it reads every new article, extracts its ideas, places them, and reports what is still to process. It never decides.
- **Four pages answer the four questions.** [Which sources have we processed](sources.html); [which ideas exist and what state they are in](ideas/index.html); [where each goes](chapters.html); [what the articles asked for and what is done](tasks.html).

## The pipeline

| Stage | Node | Who | States |
|---|---|---|---|
| 1. A source arrives | an article (newsroom or here), a decision, a memo, a 2018 file | the journalist writes; the librarian captures | to process, processed; to mine, mined; background, skipped; a 2018 file: answered, unanswered |
| 2. Ideas are extracted | one idea per core claim, frame, advice, method, story or piece of evidence, with provenance | the librarian | candidate, accepted, drafting, signed off, declined, deferred |
| 3. Ideas are placed | a chapter in the chapter map, or next version, another book, the process | the librarian proposes; the editor maps; Dinis decides | this edition, next version, another book, the process, undecided |
| 4. Chapters are written | the working copy in the vault, from the ideas, the interviews and the 2018 text | the editor, with Dinis; the reviewer records | proposed, mapped, storyboarded, drafting, reviewed, signed off, published |
| 5. A version is released | the signed-off text comes into the repository; every format from one source | the publisher | v1.0.1 and on; v2.0.0 when Dinis says so |

Each stage reads the one before it and writes a file the build can check. Nothing is tracked by hand.

## What an idea is

An idea is the smallest thing Dinis can decide on. Not a chapter (too big to say yes to in one go) and not a sentence (too small to place). The test: can it be stated in one sentence that the book would stand behind, and does it have at least one source? Kinds: a *frame* (a way of seeing the whole book uses), a *claim* (something the book asserts and must back), *advice* (what the reader should do), a *method* (a way of working the reader can copy), a *story* (a lived example, dated), *evidence* (a number or a source), and *process* (how the book itself is made, which goes in the last part, or is not the book at all).

Every idea carries: its statement; its sources, each with the section; the 2018 files it answers; the topic from the survey; the proposed chapter; a centre of gravity (explorer, villager, town planner or all); its state and destination; and who decided, if anyone.

## How a newsroom article is processed

1. The survey says what it is: bring, content, context or skip. Bring and content are the work; context is for the agents; skip is skipped.
2. The librarian reads it in full (the newsroom's markdown twin), and writes one idea per thing the book would say, or attaches its number, story or quote to an idea that exists. The article's state moves by itself: an idea that cites it makes it processed (bring) or mined (content).
3. If the article answers a 2018 outline, the idea names the file, and the map's row and the idea agree.
4. If the article says something the book should say and no chapter fits, the chapter map gains a proposed chapter, marked so.
5. The librarian never writes an idea in the book's voice. The statement is a summary; the chapter is written from the article, by the editor, with Dinis.

The four bring articles still to process, and the content articles still to mine, are counted on [the sources page](sources.html) and in [the graph's hub](index.html).

## How Dinis decides

The loop is [read, comment, decide](../articles/read-comment-decide.html), and an idea is an item in it: Dinis reads the idea page (the statement, the provenance, where it is proposed to go), comments in his own words, and picks a verb. The editor records the decision in the vault (`board/decisions/`) and changes the idea's state and destination in `ideas.json` in the same change, naming the decision. So "accepted" on the register always points at a file in the vault, and "declined" always has a reason.

Until the loop runs, an idea is "accepted" only when Dinis said it as his own position in a co-written article (the opening with wonder, maps before names, the centre of gravity, read it on paper, and the rest marked so); the editor still records those in the vault, which is task 1 of three briefs already.

## The rules

- **A source is processed when an idea cites it, not when someone says so.** The override file can only say that a source was read and has nothing to give, or that Dinis has placed everything from it.
- **No idea without a source. No chapter without an idea.** The build stops on a dangling reference.
- **An idea does not move to the book by being written here.** It moves by a decision in the vault and then by a signed-off version. The repository holds the official versions; the vault holds the working versions.
- **Declined is a state, with a reason.** It stays in the register, so the next person who proposes the same idea finds the answer.
- **The graph is public.** Like everything on this site except the keys. A reader can see why a chapter says what it says.

## The order of work from here

1. **Dinis reads the register** (81 ideas, in the order of the chapter map) and decides the candidates, or tells the editor to run the first batch of the loop on them with the four Introduction chapters.
2. **The editor records the accepted ideas** in the vault as decisions on the text (three briefs already ask for it), and takes the proposed chapter map as the start of its own, with Dinis's changes.
3. **The librarian processes the four bring articles left**, mines the content articles as each chapter is drafted (the chapter page lists what to mine), and makes a pass over the 2018 files that have neither an article nor an idea: each becomes an idea marked "article first", or a proposal to cut.
4. **The journalist writes the gap articles**, the fear and the job hunt in 2026 first, and each becomes ideas within a release.
5. **The publisher releases v1.0.0 end to end**, so the pipeline's last stage exists before the first signed-off change (v1.0.1) needs it.
6. **The chapter pages get the ideas.** When the editor's map exists, each proposed chapter's page shows its ideas in order, the 2018 text it replaces, and the articles to mine: the brief for writing it.

## What this is for, beyond this book

The process is the product as much as the book: a repository for the official versions, a public vault for the working ones, articles as briefs, roles with folders, decisions as files, and a graph that says where every idea came from and where it went. A second book starts by copying the folders. The last part of this book describes it; this page is its working state.

## What this does not claim

- **The ideas are a reading.** The librarian's, of the articles as published on 18 October 2026. Dinis has decided none of them through the loop yet.
- **The chapter map is a proposal.** The editor owns the chapter map; this one exists so the ideas have somewhere to point.
- **"Shares terms" in the reader's graph is a heuristic; this graph is not.** Every edge here is a named reference in a file.
- **Counts move on every build.** The numbers on these pages are computed, not typed.
