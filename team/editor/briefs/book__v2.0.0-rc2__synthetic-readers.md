# Synthetic readers of release candidate 2: will they buy it?

*A brief for the editor, written by the site's agent from Dinis's request of 19 October 2026. Book version: v2.0.0-rc2 (a candidate, not a version). Site version that published the brief: v0.2.27.*

**Read.** [How to run synthetic users on your own site](https://newsroom.sgit.ai/articles/how-to-run-synthetic-users.html) (the method), [Short, punchy, and co-written with Claude](../../../briefs/index.html) (synthetic readers, and the right to say no), [Gen ZX Developers](../../../articles/index.html) (the frame) and your own `role.md`, primary responsibility 4.

**In one line.** Five invented readers read rc2, from the first page, the way each would; we record where each would put it down and whether they would buy it there, then ask them to finish it as beta readers, interview them, and order what they found by what it costs. One of the five is a publisher deciding whether to commission it.

## What Dinis asked

In his words, condensed: read the book's structure and objectives; create the pages and run five synthetic users who read the book and give feedback on its pacing, its content and its structure, what is strong, what makes sense and what does not; and at the end ask the question, will they buy it, will they see the value, and how would they make it better. Two from Generation Z, two from Generation X, and one publisher, who ultimately decides whether to commission the book, to publish it under their brand. The pages go on this site, not in a vault, because we are going to keep track of them.

## The study

| | |
|---|---|
| **The readers** | `admin/content/readers/01-rc2/personas.json`: Aisha (Gen Z, codes with agents, on a phone), Ellie (Gen Z, never coded, has an idea), Nadia (Gen X, the expert founder), Martin (Gen X, the sceptic who will probably never buy), Catherine (publisher at an invented independent house) |
| **What we expect** | `journeys.json`, written and released before any run |
| **How they read** | `admin/content/readers/protocol.json`: the newsroom's loop with the text in place of the screenshot, two phases (natural, then asked), the same twelve questions for everyone and five more for the publisher |
| **What is evidence** | The candidate's text. Every quote is checked by the build against the unit it cites, and the study is pinned to rc2's sha256 |
| **The runs** | `runs/<reader>.json`, one Sonnet agent per reader, in parallel |
| **After the runs** | `checks.json` (every surprising finding checked against the text, kept and labelled if it does not hold) and `synthesis.json` (will they buy, and the recommendations, ordered by cost) |
| **The pages** | [/readers/](../../../readers/index.html) |

## The work

1. **Run the five.** Done when each run is on the site and the build has checked its quotes.
2. **Check before you believe.** Every finding that would change the book is checked against the candidate: a claimed repetition is two passages, a claimed gap is a search. Done when `checks.json` says which held.
3. **Answer every finding.** Fix, rc3, article first, later, or not doing it; declined with a reason is an answer, and deleting a finding is not. Done when no finding on [the findings page](../../../readers/01-rc2/findings.html) is unanswered. The ones that change the book go to the board as proposals for the rc2 to rc3 change set.
4. **Run the same five on rc3.** A finding that disappears is a fix that worked; a new one is something the fix broke.

## What this does not claim

- **Synthetic readers are a tool, not readers.** Real readers come after; nothing here is market research.
- **The price is the study's assumption** (an ebook at £9.99, a paperback at £19.99), so that the buy question has something to answer. Nothing has been decided.
- **The publisher is invented**, and so is Fernhill Press. Her verdict is a way of reading the manuscript as a commissioning publisher would, not an offer.
