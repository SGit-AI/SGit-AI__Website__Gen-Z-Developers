# Record Dinis's first review of the plan

**What.** Dinis reviews the plan at `infographics/plan.html` and exports the review (markdown or JSON). Each verdict becomes the proposal's state in `admin/content/infographics/plan.json`: accept to `accepted`, change to `changes` with the note, decline to `declined` with the reason, later to `deferred`; `decided_by` names Dinis and the review file. Then: draw the accepted ones not yet drawn, redraw the changed ones, and brief the editor on where each accepted one goes in the next candidate.

**Done when.** The plan's states match the review, every accepted proposal is drawn, and the editor has a brief listing them.

**From.** The infographics agent article, site v0.2.32.
