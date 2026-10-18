# Working in this repository

This is the contributor contract for agent sessions. `README.md` describes the layout; this file
describes the behaviour expected of you. Read both before touching anything.

## The one-paragraph orientation

This repository is the website `gen-z-developers.sgit.ai` and the official versions of the book
*Generation Z Developers*. **The repository holds the official versions; the vault holds the working
versions.** `v1/` is the 2018 first edition, frozen. Every push to `dev` is a narrated, tagged,
deployed release. The roles that finish the book (reviewer, editor, publisher) live in `team/`, with the journalist
who briefs them in articles (`admin/content/articles/`, rendered at `/articles/`), and
their working copies in the public vault.

## What you must not do

- **Do not edit anything under `v1/content/` or `v1/images/`.** It is the 2018 book as released. A
  spelling fix goes in the working copy in the vault, and reaches this repository only as part of
  the next signed-off version, with a new entry in `admin/content/book/versions.json`. The build and
  the gate both refuse a silent change.
- **Do not hand-edit a generated page.** Every `.html` is written by `admin/build/build.py`; the
  manifests record the hashes and the gate refuses a page edited behind its source. Change the
  source (markdown, the JSON under `admin/content/`, or `build.py`) and rebuild.
- **Do not put a private key anywhere in the tree.** Not in a file, a comment, a commit message or
  a test fixture. The gate refuses any string with sgit's private-key prefix. The public read key is
  the only key that belongs here.
- **Do not write into another role's `issues/` folder.** You may read it. Work for a role arrives as
  a brief in its `briefs/`. (`team/ISSUES.md`.)
- **Do not publish a version from the vault.** Only a version in this repository is official, and
  only an official version is published (the publisher's rule).

## The release ritual, every push to `dev`

1. `git fetch origin dev --tags` first. Never choose a version number without fetching.
2. `printf 'vX.Y.Z' > admin/build/version.txt`: always the next minor, the last number. The middle number moves
   only when Dinis says a change is major; an agent never chooses it (decision 006, `/decisions/`). The same
   rule holds for the book's versions.
3. Add a row to `admin/content/versions.json` saying what changed and why, for a reader who will
   not open the diff.
4. `python3 admin/build/build.py` (and `gen_map.py` first if the authored reading changed).
5. `node admin/build/validate.js`, green.
6. Commit as `site vX.Y.Z: what changed`, the colon straight after the version; CI parses it.
7. Push your branch, then `dev`. On a version collision: fetch, renumber, rebuild, retry; never force.

## Articles, agent articles and decisions

- **Articles** (`admin/content/articles/`, `/articles/`) are co-written with Dinis, in Dinis's voice, by the journalist;
  they brief the roles. A role pointed at one reads it, opens its own issues from its brief, and does the work.
- **Agent articles** (`admin/content/agent-articles/`, `/agent-articles/`): when you finish a significant body of
  work, write one, in your own voice as the agent: what you did, the flows, the changes, what you leave for the
  other roles. Not one per release; one per body of work. When you refer to a human decision, name who made it.
- **Decisions** on how the book is made, versioned and published are records in `admin/content/decisions/`
  (`/decisions/`), one per decision, never deleted. Decisions on the book's **text**, and the text issues
  themselves, live in the vault (`board/`), not here (decision 005).

## Storyboards

A storyboard is data (`admin/content/storyboards/NN__<slug>.json`, with the cast in `cast.json`), drawn in the browser
by `assets/storyboard.js` with Rough.js; there is no image file to edit. The build refuses a character not in the cast,
an unknown pose, mood or kind, and, when a storyboard names a `quote_source`, any Guide line or quote card that is not
in it word for word (a panel that is not meant as a quote says so with `not_a_quote` and a note).

## Published and drafts

What the 2018 build published is a rule, not a judgement: a file with `status: content` in its front matter
(28 of them) went into the Leanpub book and the print PDF; everything else stayed in the repository as a
draft (6 with text) or an outline (89). `v1.0.0` is the published book. The drafts are shown apart and
marked, never mixed into the published sequence, and never counted as part of a version. Keep that line.

## The reader (read/)

`assets/reader.js` keeps everything in the browser (`genz.reader.v1`): the meter's balance and charges, the
state of each chapter, the comments, the folds. It sends nothing. The export is how a review reaches the
vault's `reviews/` folder. Do not add a server, an analytics call or a network write to it; the newsroom's
rules for the meter (charge by share read, never less than a tenth once opened, below zero allowed,
nothing blocked) are the rules here.

## The graph (graph/)

`admin/content/graph/` is the librarian's folder: the ideas register, the proposed chapter map, the source and
task states, the plan. An idea names its sources and sections; the build refuses an idea that cites a source that
does not exist, a chapter nothing names, a source marked processed that nothing cites, or a task state for a task
no article has. A source's processing state is derived from the edges, never ticked by hand. When Dinis decides an
idea through the loop, the editor records the decision in the vault and the idea's state moves in the same release,
naming the decision. Process every new co-written article, decision and bring article into ideas within a release.

## Two version streams

The **site's** version (`admin/build/version.txt`) moves on every push. The **book's** version
(`admin/content/book/versions.json`) moves only when a signed-off version of the book comes in from
the vault, and `v1.0.0` is the 2018 edition. A file name carrying a version says which stream:
`book__v1.0.0__<slug>.md` for work on the book at that version, `v0.1.0__<slug>.md` for work on the
site.

## When a new version of the book comes in

1. The editor has signed off the version in the vault, and the publisher has agreed it is official.
2. Copy the signed-off text into the repository as the next version (the layout for `v2/` is to be
   decided when the first one arrives; keep `v1/` untouched).
3. Add the entry to `admin/content/book/versions.json` with its `text_sha256` (the build prints the
   hash it expects when the text changes).
4. Rebuild: `page_versions.freeze` writes `v<N>/versions/<version>.md` once, and the versions page
   computes the delta from the frozen files. Do not write a second differ.

## Working as a role

Read `team/<role>/role.md` first. Every role names what it refuses; hold to it. Stamp your debriefs
with the version you reviewed. Record every finding's answer next to it; "declined" with a reason is
a valid answer, and deleting a finding is not.

## The vault

`sgit clone <read key>` from `admin/content/vault.json` gives a read-only working copy of the vault.
Writing into it needs the write key, which Dinis holds. If you were given it, use it with
`sgit --token <token> push` and never paste it into this repository, a chat log that becomes a file,
or a commit.
