#!/usr/bin/env python3
"""The chapter-to-article map: one row per file of the 2018 book, the newsroom articles that answer it, and the gap.

Writes admin/content/map.json from v1/content/ and the AUTHORED reading below. The reading is the first one, taken
from the articles Generation Z Developers, again and the build brief of 18 October 2026, and extended file by file by
the agent that built this repository on the same day. It is a reading, not a verdict: the reviewer's records and the
editor's interviews (team/) decide what each chapter becomes. A row for every file is what the brief asked for; the
build refuses to run if a file has no row.

Run: python3 admin/build/gen_map.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "v1" / "content"
OUT = ROOT / "admin" / "content" / "map.json"

NEWSROOM = "https://newsroom.sgit.ai/articles/"

# slug -> title, for the articles this map cites. Titles as the newsroom index gives them, shortened.
ARTICLES = {
    "hired-for-the-workflow": "Hired for the workflow",
    "act-as-the-job-you-want": "Act as the job you want",
    "generation-z-developers-again": "Generation Z Developers, again",
    "a-book-for-one-reader": "A book for one reader",
    "a-website-to-finish-the-book": "A website to finish the book",
    "short-punchy-and-co-written": "Short, punchy, and co-written with Claude",
    "bringing-my-past-work-back": "Bringing my past work back",
    "your-own-newsroom": "Your own newsroom",
    "the-graphs-books": "The graphs books",
    "search-as-navigation": "Search as navigation",
    "introducing-fractal-semantic-graphs": "Fractal Semantic Graphs",
    "software-vendors-as-villagers": "Software vendors should become villagers and town planners",
    "explorer-coding": "Explorer coding",
    "the-fork-next-door": "The fork next door",
    "what-open-source-is-and-is-not": "What open source is, and what it is not",
    "open-source-is-not-free": "Open source is not free",
    "the-eyeballs-get-cheap": "The eyeballs get cheap",
    "the-man-behind-the-curtain": "The man behind the curtain",
    "how-much-of-this-did-i-write": "How much of this did I write?",
    "how-the-voice-works": "How the voice works",
    "books-from-articles": "Books from articles",
    "the-citizen-developer": "The citizen developer is good news",
    "why-i-love-wardley-maps": "Why I love Wardley maps",
    "ephemeral-town-planner-services": "Ephemeral town planner services",
    "explorer-to-villager-newsroom": "Go slow to go fast: from an explorer project to a villager one",
    "the-controllable-founder": "The controllable founder",
    "the-expert-founders": "The expert founders",
    "sell-dont-issue": "Sell, don't issue",
    "not-a-straight-line": "Not a straight line",
    "places-of-highest-leverage": "Places of highest leverage",
    "knowing-when-to-stop": "Knowing when to stop",
    "how-cheap-is-it-to-undo": "The human in the loop is a spectrum: how cheap it is to undo",
    "every-mistake-added-a-rule": "Every mistake added a rule",
    "how-i-work-with-claude": "How I work with Claude",
    "replicating-the-agentic-inbox": "Replicating the agentic inbox",
    "the-agent-team-as-it-runs": "The agent team as it runs",
    "the-mandate-stack": "The Mandate Stack",
    "omnichannel-programming": "Omnichannel programming",
    "my-memory-checked": "My memory, checked",
    "reviews-on-the-record": "Reviews on the record",
    "riskmandate-ten-questions": "Ten hard questions for RiskMandate",
    "how-to-run-synthetic-users": "How to run synthetic users on your own site",
    "who-is-speaking": "Who is speaking",
    "who-owns-the-words": "Who owns the words",
    "the-code-you-do-not-ship": "The code you do not ship",
    "code-review-as-a-fractal-semantic-graph": "Code review as a fractal semantic graph",
    "if-somebody-built-a-company-on-code-review": "If somebody built a company on code review",
    "every-risk-is-already-accepted": "Every risk is already accepted",
    "who-are-you-protecting-against": "Who are you protecting against?",
    "footprint-and-blast-radius": "Footprint and blast radius",
    "attacks-rewritten-as-mandates": "Attacks rewritten as mandates: 28 supply-chain incidents",
    "the-minimum-code-below": "The minimum code below: container security from the top down",
    "ai-baseline-control-framework": "An open AI governance framework",
    "green-does-not-mean-live": "Green does not mean live",
    "sgit-in-a-ci-pipeline": "sgit in a CI pipeline",
    "sgit-actions-side-by-side": "sgit in GitHub Actions, side by side",
    "no-server-by-design": "No server, by design",
    "move-the-cloud-not-the-code": "Move the cloud, not the code",
    "cloudflare-as-lego-blocks": "Cloudflare as Lego blocks",
    "what-sgit-is": "Git for things you cannot put on GitHub",
    "sgit-is-a-standard": "sgit is a standard, not a server",
    "encrypted-memory-for-isolated-agents": "Encrypted memory for agents that run somewhere else",
    "the-homepage-is-a-vault": "The homepage is a vault",
    "the-vault-is-live": "The vault is live",
    "nineteen-sites": "Twenty sites in fifteen days",
    "three-linkedin-pages": "Three companies, three LinkedIn pages",
    "a-reading-list-in-a-link": "From me to you, in a link",
    "the-scripted-talk": "The scripted talk",
    "the-deck-i-could-not-download": "The deck I could not download",
    "judo-for-small-countries": "Judo for small countries",
    "portugal-2016-hacking-portugal": "Hacking Portugal, 2016",
    "portugal-2010-a-challenge": "A web application security challenge to Portugal, 2010",
    "portugal-and-europe-2025": "Portugal and Europe, 2025",
    "the-infographic-bake-off": "The infographic bake-off",
    "fix-the-page-yourself": "Fix the page yourself: the bookmarklet trick",
    "a-minimal-viable-browser": "A minimal viable browser",
    "the-value-of-constraints": "The value of constraints",
    "i-miss-it": "I miss it, so it is working",
    "the-question-is-whether-they-miss-it": "The most important question is whether they miss it",
    "price-it-then-give-it-away": "Price it, then give it away",
    "paying-after-the-value": "Paying after the value",
    "pay-after-you-read": "Pay after you read",
    "the-agents-write-too": "The agents write too",
    "the-wall-under-the-reply": "The wall under the reply",
    "handing-secrets-to-agents": "Handing secrets to agents and browsers",
    "where-the-vault-keys-live": "Where the vault keys live",
    "secrets-on-public-keys": "secrets.sgit.ai on public keys",
    "a-directory-of-people-and-keys": "A directory of people and their keys",
    "memory-is-not-a-spectator-sport": "Memory is not a spectator sport",
    "knowledge-that-maintains-itself": "Knowledge that maintains itself",
    "the-librarians-daily-brief": "The Librarian's daily brief",
    "from-a-spreadsheet-to-a-folder-per-person": "From a spreadsheet to a folder per person",
    "agentic-cost-is-an-engineering-problem": "Agentic cost is an engineering problem",
    "the-key-is-the-billing-system": "The key is the billing system",
    "authority-outside-the-model": "Authority outside the model",
    "a-policy-beside-the-prompt": "A policy beside the prompt",
    "are-hooks-the-sweet-spot": "Are hooks the sweet spot?",
    "the-human-in-the-loop": "The human in the loop, safety net or bottleneck",
    "one-article-five-readers": "One article, five readers",
    "firing-journalists": "Firing journalists is the worst thing a publication can do",
    "stop-the-bleeding-then-ask-for-it-back": "Stop the bleeding, then ask for it back",
    "connector-twin-before-you-deploy-an-agent": "Before you give an agent a connector, give the connector a twin",
}

# path -> (articles, gap). "then-now" marks a written chapter whose 2018 claims need a then-and-now box.
# A gap of "" means the articles answer it; "none" means no article yet; anything else says what is missing.
READING = {
    # introduction
    "1.introduction/_index.md": ([], "Keep. Rewrite the frame: everyone who can brief an agent is a developer now; the seven lines on the cover stay (Generation Z Developers, again)."),
    "1.introduction/generation-z.md": (["generation-z-developers-again", "hired-for-the-workflow"], "then-now: the oldest are 30 now, not 22; the worry about curiosity becomes the worry about fear of AI among young Europeans."),
    "1.introduction/how-this -book-was-created.md": (["short-punchy-and-co-written", "a-website-to-finish-the-book", "books-from-articles", "how-much-of-this-did-i-write"], "Rewrite as the last part of the book: how the second edition was made, co-written with Claude, with the memo-to-word ratio."),
    "1.introduction/how-to-get-a-job.md": (["act-as-the-job-you-want", "hired-for-the-workflow"], "then-now: the list of competitive advantages (Jira, WallabyJs, AWS) dates; the one advantage now is running agentic workflows."),
    "1.introduction/stem-tech-stack.md": (["the-citizen-developer", "explorer-coding"], "The three PlantUML figures it references were never generated; redraw as infographics. Add the agent layer to the stack."),
    # MVP for Gen Z dev
    "2.mvp-for-gen-z-dev/_index.md": (["hired-for-the-workflow", "your-own-newsroom"], "Rewrite the MVP around the agentic workflow: a GitHub account, an agent, a site, a vault; keep the TASK device."),
    "2.mvp-for-gen-z-dev/content/creative-commons.md": ([], "Keep, corrected. then-now: the repository licence (Apache) and the book's licence (CC BY) disagree; settle it."),
    "2.mvp-for-gen-z-dev/content/docker.md": (["the-minimum-code-below", "move-the-cloud-not-the-code"], "then-now: containers are where agents run now; the chapter's install walk-through dates."),
    "2.mvp-for-gen-z-dev/content/dot-language.md": (["introducing-fractal-semantic-graphs", "the-graphs-books"], "Keep the hands-on part; connect to graphs as the way of thinking, not only a drawing tool."),
    "2.mvp-for-gen-z-dev/content/google-search-gdd-sre.md": (["search-as-navigation"], "then-now: search as a navigation of a graph you own, and agents as the searcher."),
    "2.mvp-for-gen-z-dev/content/hugo.md": (["your-own-newsroom", "nineteen-sites", "no-server-by-design"], "then-now: static sites built by an agent from a voice memo; Hugo itself is one option among several."),
    "2.mvp-for-gen-z-dev/content/jira.md": (["the-agent-team-as-it-runs"], "then-now: issues as files in folders, the board the agents run; Jira as the thing it replaced."),
    "2.mvp-for-gen-z-dev/content/open-source.md": (["the-fork-next-door", "what-open-source-is-and-is-not", "open-source-is-not-free", "the-eyeballs-get-cheap"], "Keep; add the fork as protection and who pays for the long tail."),
    "2.mvp-for-gen-z-dev/content/owasp.md": (["hired-for-the-workflow", "portugal-2010-a-challenge"], "Keep; the OWASP work is the worked example of act as the job you want."),
    "2.mvp-for-gen-z-dev/content/python.md": (["explorer-coding"], "then-now: Python is still the language of the agent era; the reader may write less of it by hand."),
    "2.mvp-for-gen-z-dev/content/slack-and-chatops.md": (["replicating-the-agentic-inbox", "omnichannel-programming"], "then-now: from ChatOps to agents in the inbox, briefs by voice, previews on the phone."),
    "2.mvp-for-gen-z-dev/content/xcode-and-swift.md": (["a-minimal-viable-browser"], "then-now: an app built by an agent for one person (a browser for one); Xcode still the door to iOS."),
    "2.mvp-for-gen-z-dev/draft/aws.md": (["cloudflare-as-lego-blocks", "move-the-cloud-not-the-code", "ephemeral-town-planner-services"], ""),
    "2.mvp-for-gen-z-dev/draft/continuous-integration.md": (["green-does-not-mean-live", "sgit-in-a-ci-pipeline", "sgit-actions-side-by-side"], ""),
    "2.mvp-for-gen-z-dev/draft/electron.md": ([], "none"),
    "2.mvp-for-gen-z-dev/draft/github-flow.md": (["act-as-the-job-you-want"], "GitHub flow as the way an agent and a person share a repository; no article on the flow itself."),
    "2.mvp-for-gen-z-dev/draft/iot.md": ([], "none"),
    "2.mvp-for-gen-z-dev/draft/linux.md": (["the-minimum-code-below"], "The container chapter touches it; no article on Linux as a thing to learn."),
    "2.mvp-for-gen-z-dev/draft/minecraft.md": ([], "none; consider cutting or merging into Learning."),
    "2.mvp-for-gen-z-dev/draft/raspberry-pi.md": ([], "none"),
    "2.mvp-for-gen-z-dev/draft/stack-overflow.md": (["search-as-navigation"], "Where answers come from now: the agent, with the source behind it; no article on Stack Overflow itself."),
    "2.mvp-for-gen-z-dev/draft/tdd.md": (["code-review-as-a-fractal-semantic-graph", "the-code-you-do-not-ship"], "Tests as the thing that lets an agent change code safely; no article on TDD as such."),
    "2.mvp-for-gen-z-dev/draft/wallaby-and-ncrunch.md": ([], "Written in 2018 (it is the longest chapter) but filed under draft. then-now: live test runners dated; the idea, instant feedback, is what agents give now."),
    "2.mvp-for-gen-z-dev/draft/wikipedia.md": ([], "none"),
    # technologies
    "3.technologies/_index.md": ([], "Reframe: the technologies a Gen Z developer needs to understand (not operate) in 2026."),
    "3.technologies/content/AST.md": (["code-review-as-a-fractal-semantic-graph"], "Keep; code is already a graph, which is where the AST chapter was heading."),
    "3.technologies/content/assembly-and-bytecode.md": ([], "Keep as history; no article."),
    "3.technologies/content/books.md": ([], "Keep; refresh the list. Add the graphs books and this one."),
    "3.technologies/content/brain.md": (["knowing-when-to-stop", "how-cheap-is-it-to-undo"], "Keep; connect to what experience gives people and what has to be designed into agents."),
    "3.technologies/content/ide.md": (["explorer-coding", "how-i-work-with-claude"], "then-now: the IDE is now a conversation with an agent and a terminal; keep the history."),
    "3.technologies/content/ml-ai.md": (["hired-for-the-workflow", "authority-outside-the-model"], "then-now: the 2018 chapter pointed at cloud ML services to program; the shift was learning to use it and direct agents. The chapter that changed most."),
    "3.technologies/content/pen-and-paper.md": (["why-i-love-wardley-maps"], "Keep; add the handwritten notes from the printed copy as figures."),
    "3.technologies/draft/blockchain.md": ([], "none; the editor decides whether it stays."),
    "3.technologies/draft/browser-automation.md": (["a-minimal-viable-browser", "how-to-run-synthetic-users"], ""),
    "3.technologies/draft/dopamine.md": ([], "none"),
    "3.technologies/draft/dsl.md": (["introducing-fractal-semantic-graphs"], "Graphs as the DSL; no article on DSLs as such."),
    "3.technologies/draft/ngrok.md": ([], "none; likely cut."),
    "3.technologies/draft/node-js.md": ([], "none"),
    "3.technologies/draft/r-language.md": ([], "none; likely cut."),
    "3.technologies/draft/scratch.md": (["the-citizen-developer"], "Scratch as the first door; the citizen developer is the grown-up version."),
    "3.technologies/draft/streams.md": ([], "none"),
    "3.technologies/draft/web-proxies.md": (["a-minimal-viable-browser"], "The browser chapter touches it; no article on proxies as such."),
    # life patterns
    "4.life-patterns/_index.md": ([], "Keep the part; it is where most outlines were."),
    "4.life-patterns/BBS-and-modems.md": ([], "none; keep as history (Dinis's own story), short."),
    "4.life-patterns/automate-your-workflows.md": (["your-own-newsroom", "replicating-the-agentic-inbox", "omnichannel-programming"], ""),
    "4.life-patterns/civic-responsibility.md": (["judo-for-small-countries", "portugal-and-europe-2025"], "The Portugal articles carry it; no article on civic responsibility as such."),
    "4.life-patterns/content/backup-your-life.md": (["what-sgit-is", "encrypted-memory-for-isolated-agents", "the-vault-is-live"], "then-now: back up into a vault you hold the key to."),
    "4.life-patterns/content/be-a-founder.md": (["the-controllable-founder", "the-expert-founders", "sell-dont-issue", "not-a-straight-line"], "Keep; add what investors pick, and the expert founder."),
    "4.life-patterns/content/being-criticized-is-a-privilege.md": (["reviews-on-the-record", "riskmandate-ten-questions"], "Keep; the book itself is now reviewed on the record, finding by finding, declined allowed."),
    "4.life-patterns/content/future-needs-you.md": (["hired-for-the-workflow", "the-code-you-do-not-ship"], "Keep; then-now on what the future turned out to need."),
    "4.life-patterns/content/learning.md": (["hired-for-the-workflow"], "Keep: learn how to learn is on the cover. Add: you have to do it to see it."),
    "4.life-patterns/content/talking-to-yourself.md": (["my-memory-checked", "the-librarians-daily-brief"], "then-now: talking to yourself by voice memo, and an agent that checks what you said."),
    "4.life-patterns/curse-of-knowledge.md": (["how-the-voice-works", "one-article-five-readers"], "Readers at several altitudes; no article on the curse of knowledge as such."),
    "4.life-patterns/ideas.md": (["bringing-my-past-work-back", "the-briefs-so-far" if False else "books-from-articles"], "Ideas as briefs, kept and acted on later."),
    "4.life-patterns/impostor-syndrome.md": (["hired-for-the-workflow"], "You are more technical than you think; no article on impostor syndrome as such."),
    "4.life-patterns/king-is-naked.md": (["firing-journalists", "stop-the-bleeding-then-ask-for-it-back"], "Saying the thing nobody says; no article on the fable itself."),
    "4.life-patterns/learn-to-hack.md": (["who-are-you-protecting-against", "fix-the-page-yourself"], ""),
    "4.life-patterns/love-maths.md": ([], "none"),
    "4.life-patterns/mentors.md": (["act-as-the-job-you-want"], "Let the people who want to help you, help you; no article on mentors as such."),
    "4.life-patterns/nudge.md": ([], "none; the file has no title."),
    "4.life-patterns/one-way-two-way-doors.md": (["how-cheap-is-it-to-undo", "the-human-in-the-loop"], ""),
    "4.life-patterns/pionners-settlers-town-planners.md": (["software-vendors-as-villagers", "explorer-coding", "why-i-love-wardley-maps", "explorer-to-villager-newsroom"], "Becomes the frame of the whole edition: explorers, villagers and town planners, and Wardley maps explained."),
    "4.life-patterns/power-of-habits.md": ([], "none"),
    "4.life-patterns/publish-publish-publish.md": (["your-own-newsroom", "act-as-the-job-you-want", "nineteen-sites"], ""),
    "4.life-patterns/refactoring.md": (["the-code-you-do-not-ship", "short-punchy-and-co-written"], "Refactoring code, and refactoring a book that is a graph."),
    "4.life-patterns/start-with-why.md": ([], "none"),
    "4.life-patterns/the-zone.md": ([], "none; the Introduction already describes it."),
    "4.life-patterns/thinking-as-programmer.md": (["the-citizen-developer", "explorer-coding"], ""),
    "4.life-patterns/why-diversity-matters.md": (["one-article-five-readers"], "Several readers, several altitudes; no article on diversity as such."),
    "4.life-patterns/workflows.md": (["your-own-newsroom", "how-i-work-with-claude", "the-mandate-stack"], ""),
    # concepts
    "5.concepts/_index.md": ([], "Keep the part; 26 of its 27 files are outlines."),
    "5.concepts/CI-Testing.md": (["green-does-not-mean-live", "sgit-in-a-ci-pipeline"], ""),
    "5.concepts/agile-and-kanban.md": (["the-agent-team-as-it-runs"], "The board as folders; no article on agile as such."),
    "5.concepts/amazon-press-releases.md": (["three-linkedin-pages"], "Writing the announcement first; no article on the press-release method."),
    "5.concepts/change-engineering.md": ([], "none"),
    "5.concepts/changes.md": (["every-mistake-added-a-rule", "how-cheap-is-it-to-undo"], ""),
    "5.concepts/chaos-engineering.md": (["connector-twin-before-you-deploy-an-agent", "footprint-and-blast-radius"], ""),
    "5.concepts/deadlines.md": (["i-miss-it", "the-question-is-whether-they-miss-it"], ""),
    "5.concepts/design.md": (["the-infographic-bake-off"], "Infographics for every chapter; no article on design as a concept."),
    "5.concepts/devops.md": (["green-does-not-mean-live", "no-server-by-design"], ""),
    "5.concepts/draft/spotify-model.md": ([], "none; likely cut."),
    "5.concepts/facts.md": (["my-memory-checked", "reviews-on-the-record"], "Make fact based decisions is on the cover; the newsroom's method of checking is the answer."),
    "5.concepts/feedback-loops.md": (["reviews-on-the-record", "how-to-run-synthetic-users"], ""),
    "5.concepts/funtional-programming.md": ([], "none"),
    "5.concepts/gamification.md": ([], "none"),
    "5.concepts/gdpr.md": (["ai-baseline-control-framework"], "The governance articles touch it; no article on GDPR for developers."),
    "5.concepts/graphs.md": (["the-graphs-books", "search-as-navigation", "introducing-fractal-semantic-graphs", "memory-is-not-a-spectator-sport"], ""),
    "5.concepts/inventing-on-principle.md": (["explorer-coding"], "Instant feedback while making; no article on Bret Victor's talk."),
    "5.concepts/karma-points.md": ([], "none"),
    "5.concepts/legacy-applications.md": (["the-code-you-do-not-ship"], ""),
    "5.concepts/micro-services.md": (["ephemeral-town-planner-services", "no-server-by-design"], ""),
    "5.concepts/netflix-culture.md": ([], "none"),
    "5.concepts/pair-programming.md": (["how-i-work-with-claude", "explorer-coding"], "Pairing with an agent."),
    "5.concepts/recursive-functions.md": (["introducing-fractal-semantic-graphs"], "Fractal graphs are the recursive idea; no article on recursion as such."),
    "5.concepts/repl.md": (["explorer-coding"], ""),
    "5.concepts/serverless.md": (["ephemeral-town-planner-services", "no-server-by-design", "cloudflare-as-lego-blocks"], ""),
    "5.concepts/sre.md": (["green-does-not-mean-live"], "Thin; no article on SRE as such."),
    "5.concepts/strong-vs-weak-types.md": ([], "none; the file has no title."),
    # security
    "6.security/_index.md": ([], "All eight files are outlines; the newsroom has the material for most."),
    "6.security/3rd-party-modules.md": (["attacks-rewritten-as-mandates", "the-eyeballs-get-cheap", "open-source-is-not-free"], ""),
    "6.security/bug-bounties.md": (["act-as-the-job-you-want"], "Find vulnerabilities in open-source projects and report them properly; no article on bounties as such."),
    "6.security/defcon.md": ([], "none"),
    "6.security/dont-touch-production.md": (["footprint-and-blast-radius", "connector-twin-before-you-deploy-an-agent"], ""),
    "6.security/pointers.md": ([], "none"),
    "6.security/security-better-developers.md": (["who-are-you-protecting-against", "if-somebody-built-a-company-on-code-review"], ""),
    "6.security/strings-should-be-banned.md": ([], "none"),
    "6.security/threat-modeling.md": (["every-risk-is-already-accepted", "who-are-you-protecting-against", "footprint-and-blast-radius"], ""),
    # your CV
    "7.your-cv/_index.md": (["act-as-the-job-you-want"], "Keep the part; your CV should be online, with links to the work."),
    "7.your-cv/blogs.md": (["your-own-newsroom", "act-as-the-job-you-want"], ""),
    "7.your-cv/future-self.md": (["bringing-my-past-work-back", "memory-is-not-a-spectator-sport"], ""),
    "7.your-cv/git.md": (["what-sgit-is", "sgit-is-a-standard"], "Git, and git for things you cannot put on GitHub."),
    "7.your-cv/github.md": (["act-as-the-job-you-want", "the-fork-next-door"], ""),
    "7.your-cv/leanpub.md": (["books-from-articles", "generation-z-developers-again"], ""),
    "7.your-cv/linkedin.md": (["three-linkedin-pages", "act-as-the-job-you-want"], ""),
    "7.your-cv/personal-brand.md": (["who-is-speaking", "how-the-voice-works", "the-man-behind-the-curtain"], "The file has no title; the voice articles answer it."),
    "7.your-cv/twitter.md": ([], "none; then-now: the platform changed, the practice (your public notebook) moved to your own site."),
    "7.your-cv/upwork.md": ([], "none"),
    # misc
    "10.misc/_index.md": ([], "A holding part; its files move into chapters or are cut."),
    "10.misc/books-to-read.md": ([], "Merge into Books."),
    "10.misc/diagrams-to-add.md": (["the-infographic-bake-off"], "Becomes the figures list for the edition."),
    "10.misc/gen-z-digital-env.md": ([], "none; merge into Generation Z."),
    "10.misc/gen-z-research.md": (["generation-z-developers-again"], "A research task for the researcher role: who the reader is in 2026."),
    "10.misc/o2-platform.md": (["bringing-my-past-work-back"], "Dinis's own history; the back-catalogue worker covers it."),
    "10.misc/stories-to-tell.md": (["portugal-2016-hacking-portugal", "portugal-2010-a-challenge"], "Some stories are now articles."),
    "10.misc/technium.md": ([], "none"),
    "10.misc/wait-but-why.md": ([], "none; likely cut."),
    # apparatus
    "_index.md": ([], "Site home of the Hugo build; not a chapter."),
    "_footer.md": ([], "The licence line (CC BY-SA 4.0 here; CC BY on the cover): settle which."),
    "_template.md": ([], "The outline template; not a chapter."),
    "for-print.md": ([], "Hugo print layout; not a chapter."),
    "_manuscript/book.md": ([], "Hugo Leanpub layout; not a chapter."),
    "_manuscript/change-log.md": ([], "Keep as the record of v0.30 to v0.60 and the contributors to credit."),
    "_manuscript/github-issues.md": (["reviews-on-the-record"], "Feedback by GitHub issues then; reviews and a board in the vault now."),
}

PARTS = {
    "1.introduction": "Introduction", "2.mvp-for-gen-z-dev": "MVP for Gen Z Dev", "3.technologies": "Technologies",
    "4.life-patterns": "Life Patterns", "5.concepts": "Concepts", "6.security": "Security", "7.your-cv": "Your CV",
    "10.misc": "Misc", "_manuscript": "Manuscript apparatus", "": "Apparatus",
}


def frontmatter(text):
    m = re.match(r"---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def main():
    rows, missing = [], []
    files = sorted(p for p in CONTENT.rglob("*.md"))
    for p in files:
        rel = p.relative_to(CONTENT).as_posix()
        fm, body = frontmatter(p.read_text(encoding="utf-8"))
        t = re.search(r"^title\s*:\s*(.*)$", fm, re.M)
        title = t.group(1).strip().strip('"') if t else ""
        st = re.search(r"^status\s*:\s*(\w+)", fm, re.M)
        status = st.group(1) if st else ""
        outline = "Topics to cover" in body
        words = len(re.findall(r"\w+", body))
        part = rel.split("/")[0] if "/" in rel else ""
        apparatus = rel.startswith("_") or rel.endswith("/_index.md") or rel == "for-print.md"
        kind = "apparatus" if apparatus else ("outline" if outline else "written")
        if rel in READING:
            arts, gap = READING[rel]
        else:
            missing.append(rel); arts, gap = [], "none"
        bad = [a for a in arts if a not in ARTICLES]
        if bad:
            sys.exit(f"gen_map: unknown article slug(s) {bad} on {rel}")
        rows.append({
            "file": rel, "part": PARTS.get(part, part), "title": title or rel.rsplit("/", 1)[-1].removesuffix(".md"),
            "status_2018": status or "unset", "kind": kind, "words": words,
            "articles": [{"slug": a, "title": ARTICLES[a], "url": NEWSROOM + a + ".html"} for a in arts],
            "gap": gap,
        })
    if missing:
        sys.exit("gen_map: no reading for: " + ", ".join(missing))
    counts = {k: sum(1 for r in rows if r["kind"] == k) for k in ("written", "outline", "apparatus")}
    answered = sum(1 for r in rows if r["articles"])
    doc = {
        "what": "One row per markdown file of the 2018 book (v1/content/), the newsroom articles that answer it, and the gap. "
                "A first reading, from the article Generation Z Developers, again and the build brief of 18 October 2026, "
                "extended file by file; the reviewer's records and the editor's interviews decide. "
                "kind: written (a chapter with text), outline (a chapter that is a title and 'Topics to cover and ideas'), apparatus (the part indexes and the Hugo files, not chapters; the outline template is one of them). "
                "gap: '' means the articles answer it; 'none' means no article yet; otherwise what is missing or what to do.",
        "source": "https://github.com/DinisCruz/Book_Generation_Z_Developer at 61886444fe5ab118ab18726147826ab05f794edc (2024-03-01), content/",
        "newsroom": NEWSROOM.rstrip("/"),
        "counts": {"files": len(rows), **counts, "answered_by_articles": answered,
                   "articles_cited": len({a["slug"] for r in rows for a in r["articles"]})},
        "rows": rows,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"gen_map: {len(rows)} rows, {counts}, {answered} answered, {doc['counts']['articles_cited']} articles cited -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
