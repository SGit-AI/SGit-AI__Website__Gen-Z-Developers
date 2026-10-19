# A release candidate is read on the site from a frozen snapshot, marked, and is not a version

**Decided.** 2026-10-19

**By.** Dinis Cruz.

**Said.** "Let's do a release of it and see what it looks like. [...] Our first release candidate for the book, which should be an end-to-end book, fully built, with introduction. [...] Let's basically put that there, and then see where we are, and then I can read it, and then I'll print it out, and then I'll start providing feedback on those materials."

**Means.** Decision 008 says release candidates are working versions and live in the vault; this one says how Dinis reads one. The working copy of a candidate is in the vault (`book/rc1/`, one markdown file per chapter, its ideas, sources and 2018 files in the front matter). To be read, printed and marked up it has to be built, so the repository carries a **frozen snapshot** of each candidate under `v2/content/`, rendered by `admin/build/book_v2.py` at `/v2/book/` (one page per chapter with its provenance, the contents, the whole book on one page, a PDF, the reader at `/read/v2.html`). The snapshot is frozen once (its assembled text written to `v2/versions/<candidate>.md`, its hash recorded under `candidates` in `admin/content/book/versions.json`), so what Dinis read cannot change behind him; the build refuses a changed candidate and asks for the next one. The snapshot is not a working copy (edits happen in the vault, and reach the repository as the next candidate) and not a version (it is not in `versions`, every page says what it is, the versions page lists it apart, and nothing is published from it outside this site). The publisher's rule stands: only a signed-off version in this repository is official, and only an official version is published. The build refuses a chapter that cites an idea, source, part or 2018 file that does not exist, so the candidate's provenance is checked the way the register's is.

**Supersedes.** Nothing; it applies decision 008 to the website, and fills the gap left open in `CLAUDE.md` ("the layout for `v2/` is to be decided when the first one arrives").

**Recorded in.** [The release candidate, written from the register](/agent-articles/the-release-candidate-written-from-the-register.md).
