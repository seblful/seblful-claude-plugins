---
description: Sweep a project's documentation for stale claims, disorientation, and dead weight, list the findings ranked by severity, then apply only the fixes you approve.
argument-hint: [doc or subtree to narrow the sweep to — omit to sweep every doc in the project]
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Agent, Skill
---

# Docs Sweep

Find what is wrong with documentation that already exists, then fix it — **audit first, apply only on approval**.

Sweep every markdown doc a human reads. `$ARGUMENTS`, if given, narrows it to that file or subtree; it does not change the process.

## Scope: prose, not code

This command changes **markdown**. It never edits code, and never a docstring or an in-code comment — those belong to `/code-sweep`. One rule decides:

> **Is the fix a change to prose a human reads, outside the code?**
> **Yes** → it belongs here. **No** → hand it to `/code-sweep`.

Handoffs. When the sweep turns one up, **list it in the report's handoff section and do not fix it here**:

| Finding | Belongs to |
| --- | --- |
| The doc states intent and the **code** is the bug | `/code-sweep` — never document a regression as intended behaviour |
| Stale docstring or in-code comment | `/code-sweep` (the `code-smells` catalog owns those) |
| `CLAUDE.md`, `AGENTS.md`, agent-facing instructions | the `claude-md-improver` skill |
| Generated page that is wrong | its generator or source, never the output |

## Phase 0 — Bound the sweep and build the fact base

**Bound it.** Enumerate what is in scope before reading any prose closely. Exclude: generated output, vendored and upstream-template files, `node_modules`, built sites, agent-facing files, and anything a tool owns end to end. Note which docs are the project's **entry point** — they carry the most readers and the most cost.

**Build the fact base.** The sweep checks claims against the repo, so gather what it checks *against* first:

- Manifests and scripts — `package.json`, `pyproject.toml`, `Makefile`, CI workflows: the commands that actually exist, with their real flags.
- Entry points, top-level directories, and the names the code uses for its own concepts.
- Versions, from lockfiles and manifests rather than from other prose.
- Whether a link checker or markdown linter already runs in CI. If one does, what it covers is **its** job, not a finding here.

**Triage with git, never judge with it.** Compare each doc's last commit against the churn in what it describes (`git log -1 --format=%ad -- <doc>`, then the same for its subject). A doc untouched while its subject moved heavily gets read first. **Churn is triage — a stable doc describing stable code is correct, not stale.**

**Do not run a doc's commands.** Static cross-check is the default: a README's instructions can install, delete, or deploy. Execute one only when the user asks, for one named doc, and say what you are about to run before you run it.

## Phase 1 — Read with three lenses

Load the `writing-docs` skill first — it defines the signals for each lens **and the false positives to suppress**. Then read the docs **yourself**: a docs corpus is small, and every truth check needs the code context you already have in hand. A subagent returns a summary you would have to re-verify anyway.

Only when the corpus is genuinely large — past ~15 docs or ~3k lines — fan out to `Explore` agents, **one per group of docs, never one per lens**. A single doc has to be judged for truth, orientation, and weight at once, and cross-document problems (the same thing explained twice, contradictory instructions, a broken cross-link) are invisible to an agent that sees one file. Brief each to return, per candidate: `file:line`, the **quoted line**, which catalog signal it matches, and the **concrete consequence**.

Three lenses, in this order:

1. **Truth** — the doc says something the repo does not.
2. **Orientation** — all true, and the reader still cannot get what they came for.
3. **Weight** — prose that should not exist, or costs more than it returns.

Use the project's own domain vocabulary throughout — "the ingest guide", not "the third file in docs".

## Phase 2 — Verify every finding, then classify it

Open the doc **and** the repo fact it contradicts, for every candidate. **Do this yourself, not in a subagent.** Keep it only if all four hold:

- [ ] **Real** — you read the line, and you read the manifest, file, or code that contradicts it.
- [ ] **Consequential** — you can name the reader who is misled and what it costs them. "Could be clearer" is **not a finding**.
- [ ] **Not already handled** — a linter, link checker, or generator does not already own it.
- [ ] **In scope** — markdown a human reads. Anything else goes to the handoff table.

Then classify each survivor by **kind**:

- **Correction** — changes what the doc asserts. Every one states **old claim → true claim**, on the card and in the final report.
- **Edit** — same assertions, better form: order, structure, cuts.

**Never let a correction hide inside an edit.** A restructure that silently changes a claim is how a wrong fact survives review.

And by **severity**: `High` (a reader who follows it fails, or is actively misled), `Medium` (true but incomplete, unfindable, or out of order), `Low` (dead weight and noise).

## Phase 3 — List the findings, then stop

**Just list them — no Artifact, no report file.** Here the *doc and the repo fact beside it* are the evidence, and the output is a scannable defect list.

Open with a two-line preamble, no introduction paragraph: scope (docs swept / excluded) and the **fact base** — what was checkable, and what could not be verified. Then the counts per tier. Number findings in one continuous sequence so the user can answer "do 3, 7, 12".

**Tier 1 — `High`.** Full treatment, one block each:

- **Title** — names the fix, imperative: "Correct the install command in `README.md`"
- **Kind** — `Correction` or `Edit`, on the title line
- **Where** — `path:line`
- **Says / Is** — two short quoted blocks: the doc's claim, then the repo fact beside it. The centrepiece. Keep each to the lines that matter.
- **Consequence** — one sentence. Which reader hits it, and what happens to them.
- **Reach** — other docs repeating the same claim, which must move with it.

**Tier 2 — `Medium`.** One tight entry each, no blocks: numbered title, kind, `path:line`, then a single line of smell → consequence.

**Tier 3 — `Low`.** A table, one row per finding: number, `path:line`, and the fix in a few words. No prose.

Close with:

- **Recommended batch** — which document to fix first and why, in one sentence. Bias toward the entry point and toward `High` corrections.
- **Handed off** — the table above, with what was found and where it goes. Listed, not fixed.
- **Unverified** — claims you could not check, and why. This is standing risk, not a finding.

Never write "improves readability" or "makes it clearer" — say what the reader gets wrong today. If the sweep produced more than ~10 `Low` findings, keep the table and say the count rather than padding it out.

**Then stop and ask which findings to apply.** Do not edit anything before an answer.

## Phase 4 — Apply, one document at a time

Batch by **file**, not by finding: every approved finding in one doc lands as a single coherent edit, so the diff reads as a revision rather than six unrelated patches. Take the lowest-risk doc first.

Rules, in order of importance:

1. **Corrections before edits, within a doc.** Fix what is false, then reshape. A restructure done first makes the correction unreviewable.
2. **One finding, one fix.** Do not improve what the approved finding did not name. Anything new you spot goes into the final report as a follow-up.
3. **Match the project on form.** Heading style, voice, tense, list style, and the project's own vocabulary come from the neighbouring docs — never from your preference. Style-only churn hides the real fix.
4. **Never fix code from here.** A doc that is right against code that is wrong is a handoff, not an edit.
5. **Re-check what you touched** — every command, path, version, and link you wrote or moved, against the Phase 0 fact base.

Where a claim had to be left unverified, say so as you apply the edit around it.

## Phase 5 — Report

Close with a short summary:

- [ ] Documents changed, one line each on what the revision did
- [ ] **Corrections**, listed separately, each as old claim → true claim
- [ ] Findings approved but **not** applied, and why
- [ ] Claims still unverified — the standing risk
- [ ] Follow-ups spotted mid-flight, and anything handed to `/code-sweep` or `claude-md-improver`

Do not commit unless asked.
