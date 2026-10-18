# Start from the storyline

*A brief for the editor, from the journalist, 18 October 2026. Book version: v1.0.0. Site version that published the article: v0.2.3.*

**Read.** The article [Start from the storyline](../../../articles/start-from-the-storyline.md) (`/articles/start-from-the-storyline.html`), [the newsroom, surveyed](../../../map/newsroom.html) and the two storyboards at `/storyboards/`. The article's section **The brief** is the work: tasks 1 to 5 are yours.

**In one line.** Dinis wants to write the second edition from its storyline: map the 18 topics into chapters (punchline, concept, evidence, character, articles), storyboard each part from the cast in `admin/content/storyboards/`, take his comments on the storyboards through the read, comment, decide loop, add the four missing bring articles to the map, and review the survey's classes with him.

**Tools.** A storyboard is a JSON file in `admin/content/storyboards/`; `build.py` checks it and draws it; `admin/build/storyboard_png.py <slug>` exports PNGs. Set `quote_source` when the Guide quotes a text in this repository, and the build checks every quote.

**Still Dinis's.** The cast; whether the Guide is drawn as him; whether the storyline starts with the fear or the claim; every class in the survey.
