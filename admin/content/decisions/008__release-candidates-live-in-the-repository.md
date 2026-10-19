# Release candidates live in the repository, marked, and are not versions

**Decided.** 2026-10-19

**By.** Dinis Cruz.

**Said.** "I think we're in a place where we can write a first version of the next book, and let's do a release of it and see what it looks like. [...] Our first release candidate for the book, which should be an end-to-end book, fully built, with introduction. [...] Then I can read it, and then I'll print it out, and then I'll start providing feedback on those materials."

**Means.** A release candidate of the book is written in the repository under `v2/content/`, one markdown file per chapter, each naming in its front matter the ideas in the register it was written from, the sources it drew on and the 2018 files it answers; `admin/build/book_v2.py` renders it at `/v2/book/` and refuses a chapter that cites an idea, source, part or file that does not exist. A candidate is frozen like a version (its text written once to `v2/versions/<candidate>.md`, its hash recorded once under `candidates` in `admin/content/book/versions.json`), so that what Dinis read and marked up cannot change behind him; the next round of feedback produces the next candidate, never an edit of this one. A candidate is **not** an official version: it is not in the `versions` list, the versions page shows it apart, every page of it says what it is, and nothing is published from it outside this site. The publisher's rule stands: only a signed-off version in this repository is official, and only an official version is published. The working copy of the candidate is also in the public vault (`book/v2/`), where the text issues live (decision 005).

**Supersedes.** Nothing; it fills the gap left open in `CLAUDE.md` ("the layout for `v2/` is to be decided when the first one arrives").

**Recorded in.** [The release candidate, written from the register](/agent-articles/the-release-candidate-written-from-the-register.md).
