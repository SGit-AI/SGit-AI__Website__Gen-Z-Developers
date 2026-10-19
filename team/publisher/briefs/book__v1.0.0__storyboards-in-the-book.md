# Storyboards in the book: panels in print, PDF and e-books

*A brief for the publisher, from the storyboards agent, 19 October 2026. Book version: v1.0.0. Site version that published the agent article: v0.2.30.*

**Read.** The agent article [Storyboards on the shelf, and into the book](../../../agent-articles/storyboards-on-the-shelf-and-into-the-book.html), the plan and its "How".

**In one line.** If Dinis puts panels in the book, they reach print, the PDF and the e-books as files the build draws once, in black and white, frozen with the candidate; checking them in each format is yours.

**What it would mean for you.**
- **Formats.** Decision 003 holds: the panels come from the same build as the text, as SVG for the PDF and PNG for EPUB and Kindle; no store converter draws them.
- **Black and white.** The renderer gains a print mode without colour; judge it printed, not on a screen.
- **Size.** A panel's bubbles and captions should not print smaller than the body text; `print-book.css` would gain a rule for a panel on the page.
- **Frozen.** A candidate's panels are hashed with its text; a panel that changes is a new candidate.

**Not asked yet.** Nothing until Dinis decides where panels go and in which candidate.
