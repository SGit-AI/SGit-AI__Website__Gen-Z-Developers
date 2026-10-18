# A website to finish the book: a build brief for gen-z-developers.sgit.ai

*Source: [newsroom.sgit.ai/admin/notes/2026-10-18__a-website-to-finish-the-book.md](https://newsroom.sgit.ai/admin/notes/2026-10-18__a-website-to-finish-the-book.md), a build brief written by newsroom.writer on 2026-10-18. Captured verbatim on 2026-10-18 for this repository.*

*18 October 2026, written by newsroom.writer for the agent that builds the book's website. Status: a brief; nothing in it is built. The articles are [a website to finish the book](https://newsroom.sgit.ai/articles/a-website-to-finish-the-book.html) and [a book for one reader](https://newsroom.sgit.ai/articles/a-book-for-one-reader.html); the book's plan is [Generation Z Developers, again](https://newsroom.sgit.ai/articles/generation-z-developers-again.html) and its note [Generation Z Developers, second edition](https://newsroom.sgit.ai/admin/notes/2026-10-18__generation-z-developers-second-edition.md).*

## The ask

The most productive environment Dinis can have to review and finish the second edition of *Generation Z Developers*, consolidating the best of what the project's repositories have built. Address: gen-z-developers.sgit.ai (to confirm), matching the printed cover's *Gen Z Developers*. Repository: `SGit-AI/SGit-AI__Website__Gen-Z-Developers`, following the pattern of `SGit-AI__Website__PKI`, `SGit-AI__Website__Graphs` and `SGit-AI__Website__Newsroom__API` (recommended to Dinis on 18 October; he creates it).

## The rule

**The repository holds the official versions; the vault holds the working versions.**

- v1 is the book as released (September 2018, Leanpub 60%, source in `DinisCruz/Book_Generation_Z_Developer`). It goes into the new repository as it is, dated, and the site's first version shows exactly that book.
- All work after v1 happens in a public vault (its read key published, so anyone can read along): drafts, comments, graphs, reviews, the board.
- A version moves from the vault to the repository when it is signed off, on top of the one before. Each move publishes a delta against the previous version, block by block and word by word, reusing `admin/build/page_versions.py` from the newsroom (v0.12.113) rather than writing a new differ.

## Keys

- **The OpenRouter key never goes in the public vault.** Anything in a vault whose read key is published is readable by everyone. Put it in a separate private vault opened only by Dinis's passkey (the newsroom's reader-vault pattern), and set a credit limit on the key at OpenRouter.
- The public vault's write key is never published; only the read key is.

## What to reuse first

Read graphs.sgit.ai before building anything: its shelf with versions, the seven roles with a folder each (librarian, researcher, writer, editor, developer, QA, publisher), the book as a graph down to the word, and the altitude ladder (the same book at five altitudes). Many of this site's concepts first appeared there. From the newsroom: the passkey vault, the reading meter, section summaries, reviews on the record, the briefs map, figures and graphs per article.

## The site, in order

1. **v1 in the repository and on the site**, as released.
2. **The vault**, public read, with the working copy of v1.
3. **The graph**: ontology and taxonomy for the book's concepts; chapters, sections and paragraphs as nodes; links to the newsroom articles that answer each outline.
4. **Altitudes**: the book at every level, from one page to the full text, with an infographic at each: the whole book, per part, per chapter, per area of the graph. A narrative path through it.
5. **Review tools**: voice comments while reading, attached to a section; comments; a board; issues.
6. **Roles**: editor, copywriter, publisher at least; each reads, gives feedback, challenges, and writes interview scripts for Dinis; sign-off per part.
7. **Research tasks**: market research, validation, evidence and maps per section, later per paragraph.
8. **Personal editions and the meter** (from *a book for one reader*): an agent assembles an edition for one reader from the graph and a private brief; delivered as a PDF or in the browser, not published; metered from five pounds of credit, more read, more paid; kept locally, with the reader's vault as an option.
9. **Quality**: every paragraph, group of paragraphs and chapter carries its evidence, facts, hypotheses and purpose in the graph; a repetition check across the graph; synthetic readers of several types; every finding answered, with declined as a valid answer; a measured ratio of memo and review words to book words (see *short, punchy, and co-written with Claude*).
10. **The last part of the book**: how all of this was built.

## Privacy, for personal editions

The brief for a personal edition may come from the private CRM of the correspondence agents. That data is read, never copied into the edition or any public place. The edition carries choices (chapters, altitude, examples), not notes about the person. Send it only to that person; encrypt it to their key once the people directory on pki.sgit.ai exists.

## Questions for Dinis

- The address: gen-z-developers.sgit.ai?
- The first reader for a personal edition, and in which language?
- The price shape: five pounds of credit, then what per chapter?
