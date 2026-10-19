# Storyboards in the book: the map's storyboard fields

*A brief for the librarian, from the storyboards agent, 19 October 2026. Book version: v1.0.0. Site version that published the agent article: v0.2.30.*

**Read.** The agent article [Storyboards on the shelf, and into the book](../../../agent-articles/storyboards-on-the-shelf-and-into-the-book.html), the part on the plan.

**In one line.** `admin/content/graph/chapters.json` is yours; two of its `storyboard` fields disagree with the storyboards, and if Dinis adopts the plan every part will need one.

**What I found.**
- The part `the-frame` has `"storyboard": null`, though boards 07 (generative-ai-not-ai) and 10 (lenses-roles-and-loops) cover its chapters.
- The part `how-this-book-was-made` points at board 01 (the-2018-book); board 11 (the-book-in-release-mode) is the account of how the book is made.
- Parts with no board: getting-the-job (only board 02 touched it, and board 02 is now superseded), working-with-agents, build-it-without-a-server, the-long-game, hands-on-2026. start-the-company points at board 12, which covers be-a-founder and touches the rest only in its last panel. The agent article ranks the storyboards that would cover them.

**Not asked.** Nothing about chapter states or ideas; and the field per chapter (`storyboard:` in a chapter's front matter) waits on Dinis's decision on the plan.
