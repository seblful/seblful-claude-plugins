---
name: writing-docs
description: Principles and a smell catalog for a project's documentation — how to write a doc worth reading, what is wrong with one that already exists, and the false positives to suppress. Use when writing or editing any README, guide, or other markdown doc in a codebase, when /docs-sweep runs, or when the user asks whether a doc is any good. Covers markdown a human reads — docstrings and in-code comments belong to code-smells and the language skills, CLAUDE.md and AGENTS.md to claude-md-improver.
---

# Writing Docs

Documentation is the only part of a codebase that can be **wrong without failing**. Nothing compiles it, nothing tests it, and the reader who trusts it pays the cost hours later, alone. Everything here follows from that.

**Scope: markdown a human reads.** Whatever docs the project actually has — an entry point, guides, design notes, contributing or history files. No document is mandatory and none has a required shape; a project's docs are whatever its readers need. Out of scope: docstrings and in-code comments (`code-smells`, `python-patterns`), and agent-facing instructions like `CLAUDE.md` (`claude-md-improver`).

## Four laws

**1. Name the reader before the first sentence.** Who arrives here, and what do they already know? A doc written for everyone is read by no one, and you cannot decide what to cut until you know who you are cutting for.

**2. Answer one question.** Say which question in the opening. Two questions means either two docs, or one doc a reader has to search — and a reader who has to search does not trust the answer they find.

**3. Never restate what the code says.** Prose mirroring a signature, a config default, a file tree, or a flag list is stale the day it is written, and now there are two sources of truth with no way to tell which one lost. Document what the code cannot say: why it is this way, when to reach for it, what happens if you don't, what to do instead.

**4. Every instruction must be runnable.** A command the reader copies has to work as written, from the state the doc has put them in. Check the flag, the path, the version, the prerequisite. **An instruction you did not verify is a guess, and it reads exactly like a fact.**

## Concision

**Every sentence must change what the reader does.** Cut the ones that do not. A doc nobody finishes is a doc nobody read.

**Delete before you sync; link before you duplicate.** When a doc and the code disagree, deleting the section is often the better fix — a paragraph that must be maintained to stay true eventually will not be. The cheapest correct doc is the one that does not exist.

**Length is a signal, never a finding.** A doc past ~200 lines, or a section running past one screen without a heading, is worth reading closely. It is not a defect on its own — reference docs are long because they are references.

## Consistency: the project wins on form, this skill wins on truth

| The project wins | This skill wins |
| --- | --- |
| Heading style and depth, voice, tense, person | Stale claims, unrunnable instructions |
| List vs table, fence style, link style | Duplication that will drift into a lie |
| Terminology — use the codebase's **own** domain vocabulary | Dead links, wrong paths, wrong versions |
| Where docs live and what they are called | Filler that costs the reader time and buys nothing |

Read the neighbouring docs before writing a line. Matching a convention you would not have chosen is correct; imposing your own is churn that hides the real fix inside the diff.

## Writing a new doc

Five steps, each with one output. Do not skip to drafting — steps 1 and 2 are what make step 5 possible.

1. **Name the reader and what they already know.** → One line, written down, even if it never ships.
2. **State the one question.** → The doc's opening sentence. If you cannot write it in one sentence, the scope is wrong, not the sentence.
3. **Write the shortest answer that works.** → A draft. Structure follows the reader's order: what they do first comes first, not what is architecturally primary.
4. **Verify every claim and command against the repo.** → Each command traced to a manifest or script, each path to a file, each version to a lockfile. Anything you could not check is marked, not smoothed over.
5. **Cut.** → Apply the cut test to every sentence, then re-read as the reader from step 1. Most first drafts lose a third.

---

# The catalog

Three lenses, descending by severity. Each lists **signals** (what to look for, and the fix) and **not a finding** (what to suppress). The suppression lists matter as much as the signals: a sweep that reports fifty nitpicks gets ignored wholesale, and the false-positive rate decides whether the next one is trusted.

## 1. Truth

The doc says something the repo does not. **Highest severity** — a reader who follows it fails, and blames themselves first.

> **The code is truth — unless the doc states intent.**
> Default: the code is what ships, so the doc gets corrected. The exception: when the doc reads as a *promise* rather than a description — a documented contract, a stated invariant, an advertised flag, a guaranteed error — the code may be the bug. Then **stop, say which one you think is wrong and why, and hand it to `/code-sweep`.** Never quietly rewrite a doc to match a regression: that launders the bug and destroys the evidence it was ever a bug.

### Signals

- **Stale command** — an install, build, test, or run command that no longer exists in the manifest, or whose flags changed. → Correct it against `package.json` scripts / `pyproject.toml` / `Makefile` / the CI workflow, and say where you checked.
- **Wrong path, flag, or name** — a file, directory, module, env var, or option named in the doc that is not in the repo. → Fix or delete. A path that moved usually means the paragraph around it moved too.
- **Version drift** — a pinned version, minimum runtime, or dependency named in prose that disagrees with the lockfile or manifest. → Take the manifest's number, or stop naming it in prose at all.
- **Contradicts the code** — a documented default, limit, return, or error the code does not produce. → Decide which is the bug by the rule above.
- **Documents removed behaviour** — a flag, endpoint, or workflow that was deleted. → Delete the section. Do not leave "(deprecated)" on something that is already gone.
- **Dead link** — a relative link to a moved or deleted file, an anchor that no longer exists, an external URL that 404s. → Repoint or remove. Every in-repo link is checkable, so check it.
- **Unstated condition** — instructions true only on one OS, one runtime version, or one environment, written as universal. → Name the condition at the step, not in a footnote.

### Not a finding

- A section explicitly marked planned, roadmap, or not yet implemented. The label makes it a promise, not a false claim. *(An unlabelled feature described in the present tense that does not exist **is** a finding.)*
- A simplification that is true at the level it is written — "run `make test`" need not enumerate what the Makefile does.
- An external link that is merely old but still resolves and still says the right thing.
- A doc deliberately describing another version or system: a migration guide, a comparison, an upgrade note.
- A claim you could not check because it needs credentials, hardware, or a live service. **Report it as unverified; an unchecked claim is not evidence of a defect.**

## 2. Orientation

Everything in the doc is true and the reader still cannot get what they came for.

### Signals

- **No entry point** — the project has no README, or one that never says what this is and how to run it. **The only absence worth reporting.**
- **Answer below the fold** — install, run, or the one command everyone needs, sitting under badges, history, background, or a table of contents for a two-screen doc.
- **Wrong reader assumed** — a getting-started that assumes the architecture, or an internals doc re-explaining the basics. → Split, or re-aim at one reader.
- **Unstated prerequisite** — a step that silently needs a tool, credential, service, env var, or an earlier step. → State it immediately before the step that needs it.
- **Steps out of order** — an instruction depending on a later one; a "first" that is actually third.
- **Unexplained jargon** — a domain term used before it is defined, or two names for one concept across docs. → One name, the project's own, used consistently.
- **Untitled destination** — bare URLs, "click here", "see this". The reader cannot tell where it goes or whether it is worth the trip.
- **No exit** — in a set of docs with an obvious next step, a doc that answers its question and strands the reader.

### Not a finding

- **A missing doc nobody asked for. Unwritten docs are not debt** — only the entry point counts as absence. Do not propose a guides folder, a contributing file, or an architecture page to fill out a checklist.
- Marketing tone on the entry point's first screen. That screen sells the project to a stranger deciding whether to try it, which is its job. *(The same tone deeper in, or in an internal doc, is Weight.)*
- Deliberate redundancy at an entry point — repeating a command the reader would otherwise have to go and find. *(Repeating an **explanation** that must then be maintained in two places is duplication, and **is** a finding: drift makes one of them wrong.)*
- An order that looks odd to you but matches the tool's actual flow.
- Depth a reference doc genuinely needs.

## 3. Weight

Prose that should not exist, or that costs more to read than it returns. Lowest severity, **highest volume — so suppression discipline matters most here.**

### Signals

- **Said twice** — the same explanation maintained in two docs. One gets updated and the other does not, and then one of them is a lie. → One home, a link from the other.
- **Restates the code** — a parameter table mirroring a signature, a file tree mirroring `ls`, an options list mirroring the schema. → Delete, or replace with the one thing the code cannot say.
- **Filler** — "This document describes…", "It is important to note", "As you can see", "simply", "just", "easy". → Cut the sentence. If the paragraph is all filler, cut the paragraph.
- **Dead section** — a heading over a stub, a "coming soon" from two years ago, a TODO nobody will do. → Delete it. Git has it.
- **Ceremony** — a table of contents for a short doc, badges nobody reads, a preamble explaining that the document is a document.
- **Explaining the obvious** — three paragraphs on what a virtualenv is, in a project README.
- **Over-hedging** — "may", "might", "could possibly" where the doc knows the answer. A hedged fact makes the reader go and verify it, which is the work the doc existed to do.

### Not a finding

- **Long because it is a reference.** A doc that is skimmed rather than read is long by nature; the length signal must not fire on it.
- Verbosity that is **explicitness** — spelling out a dangerous step, quoting an exact error message, writing the full command instead of an abbreviation.
- Examples that look alike but cover genuinely different cases.
- A changelog or history file that is repetitive by format.
- Tone you merely dislike. **Misleading is a finding; not-your-taste is not.**

## Never a finding, in any lens

- **Generated docs** — autodoc output, rendered API pages, anything with a "do not edit" banner or a generator in CI. Fix the generator or its source; an edit to the output is thrown away on the next build.
- **Vendored or upstream files** — a template's own docs, licences, code of conduct, `.github` boilerplate, third-party copies pinned on purpose.
- **Agent-facing instructions** — `CLAUDE.md`, `AGENTS.md`, and friends. Different reader, different rules, different owner.
- **A convention of this project you would have written differently.** Check the neighbouring docs first — consistency beats preference.
- Anything owned by tooling that already runs: a link checker in CI, a markdown linter, a changelog generator. No point reporting what CI reports.
