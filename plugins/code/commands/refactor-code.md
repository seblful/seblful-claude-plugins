---
description: Sweep a codebase for bad practices, latent bugs, and bad implementations, publish a ranked audit as a visual Artifact report, then apply only the fixes you approve.
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Agent, Skill, Artifact
---

# Refactor Code

Find what is wrong with code that already works, then fix it — **audit first, apply only on approval**.

Sweep the whole codebase. `$ARGUMENTS`, if given, narrows it to that subtree; it does not change the process.

## Scope: implementations, not interfaces

This command changes **implementations** and leaves every **interface** where it is. Its sibling `/refactor-modules` changes interfaces and seams. One rule decides:

> **Would the fix change what a caller must know?**
> **No** → it belongs here. **Yes** → hand it to `/refactor-modules`.

So renaming a local, collapsing nesting, fixing a swallowed exception, and deleting dead code are all in scope — a caller's view is unchanged. Splitting a god object, removing a wrapper callers go through, and reshaping a signature are not: those move a seam.

Two further handoffs. When the sweep turns one up, **list it in the report's handoff section and do not fix it here**:

| Finding | Belongs to |
| --- | --- |
| Security hazard — injection, unsafe deserialization, hardcoded secret, missing input validation | `/security-review` |
| Performance problem — N+1 query, hot-path O(n²), unbounded growth | `/diagnosing-bugs` (measure first) |
| Shallow module, wrong seam, interface redesign | `/refactor-modules` |

## Phase 0 — Bound the sweep and take a baseline

**Bound it.** Enumerate what is in scope before reading anything closely: the source directories, and the exclusions — vendored code, generated files, migrations, lockfiles, fixtures, `node_modules`, build output. Read `CONTEXT.md` and `CLAUDE.md` if present, and check ADRs: **a convention you mistake for a smell is the most expensive kind of false positive.**

**Take a baseline.** Find the verification signal and run it *before touching anything*:

- Test command (`pytest`, `npm test`, `cargo test`, …)
- Type-check (`ty`, `mypy`, `tsc --noEmit`)
- Lint (`ruff check`, `eslint`)

Record, for each: does it exist, and is it green **right now**. A red baseline is fine and important — you must know which failures you inherited. Write down the exact commands; every batch in Phase 4 re-runs them.

Verification is **best-effort**. Where a signal is missing or a file is untested, that is not a blocker — it is **recorded risk**, carried onto the finding cards as low confidence and reported at the end. Do not stall the sweep to write tests.

## Phase 1 — Sweep with three lenses

Load the `code-smells` skill first — it defines the signals for each lens **and the false positives to suppress**. Then run three `Explore` agents **in parallel**, one per lens:

1. **Correctness & robustness** — defects that already misbehave or will under plausible input.
2. **Bad practices & idiom** — constructs that work but mislead, or that fight the language and stack.
3. **Duplication, dead weight & complexity** — code that should not exist, or that costs too much to read.

Brief each agent to return, per finding: `file:line`, the **quoted code**, which catalog signal it matches, the **concrete consequence**, and every call site it affects. Tell each agent explicitly: **no style preferences, no "consider maybe", no findings it did not read the code for.**

Use the codebase's own domain vocabulary throughout — "the Order intake loop", not "the handler in file 3".

## Phase 2 — Verify every finding, then classify it

Agents over-report. This phase is where a sweep becomes trustworthy, so **do it yourself, not in a subagent**.

Open the actual code for every candidate and keep it only if all four hold:

- [ ] **Real** — you read the code and the smell is there as described.
- [ ] **Consequential** — you can name what goes wrong: a specific input that misbehaves, a change that will break, a reader who will be misled. "Not idiomatic" with no consequence is **not a finding**.
- [ ] **Not already handled** — check the callers. A missing `None` check is not a finding when every call site guarantees non-`None`.
- [ ] **Not a lateral move** — the fix must be clearly better, not differently-shaped. If you would accept a reviewer reverting it, drop it.
- [ ] **In scope** — the fix leaves every interface intact. Otherwise it goes to the handoff section.

Then classify each survivor by **kind** — this distinction drives everything downstream:

- **Refactor** — behaviour-preserving. Same outputs, same side effects, same errors, for every input.
- **Behaviour change** — a bug fix. Semantics change. Every one must state **old behaviour → new behaviour** explicitly, on the card and in the final report. Never let one hide inside a refactor.

And by **severity**: `High` (wrong results, data loss, silent failure), `Medium` (will bite on the next change, or actively misleads), `Low` (dead weight, noise).

## Phase 3 — Publish the audit, then stop

Load the `artifact-design` skill first — the Artifact contract requires it and it owns how the page looks. Everything here is about what the report *says*.

Write to the session scratchpad as `refactor-code-audit.html`, then call `Artifact` with that path, a title, a one-sentence description, and a favicon. Give the user the URL, never a filesystem path. Re-running on the same repo republishes the same filename, which redeploys to the same URL.

**The report is a defect list, not a design document** — that is what keeps it visually distinct from `/refactor-modules`, whose report is diagram-led. Here the *code* is the evidence: every card shows real before/after, and there are no diagrams.

- **Header** — repo, date, scope (dirs swept, dirs excluded), and a **baseline strip**: each verification command with its status, plus untested-area count. No introduction paragraph.
- **Finding cards**, `High` → `Low`, each numbered so the user can answer "do 3, 7, 12":
  - **Title** — names the fix, imperative: "Stop swallowing the parse error in `load_config`"
  - **Badges** — severity, and kind (`Refactor` / `Behaviour change`)
  - **Files** — monospaced `path:line` list
  - **Before / After** — real code, side by side, minimal but syntactically complete. The centrepiece.
  - **Smell** — one sentence. What is wrong.
  - **Consequence** — one sentence. What it costs. For a behaviour change, the explicit old → new semantics.
  - **Blast radius** — call sites touched, and whether the verification signal covers them
- **Recommended batch** — which findings to take first and why, in one sentence. Bias toward high severity with tight blast radius.
- **Handed off** — the table above, with what was found and where it goes. Listed, not fixed.

Prose stays sparse; the before/after carries the weight. Never write "cleaner code" or "easier to maintain" — say what changes.

**Then stop and ask which findings to apply.** Do not edit anything before an answer.

## Phase 4 — Apply in batches

Work in **small coherent batches**, lowest risk first. After each batch, re-run the Phase 0 commands.

Rules, in order of importance:

1. **Never mix a refactor and a behaviour change in one batch.** When verification goes red, you must be able to attribute it.
2. **Red after a batch → revert that batch and diagnose.** Do not pile the next batch on a broken signal. If it was already red at baseline, confirm you did not make it *worse* rather than trying to make it green.
3. **Update every call site.** No compatibility shim unless the user asks — a shim is a new shallow module.
4. **One finding, one fix.** Do not opportunistically improve code the approved finding did not name. Anything new you spot goes in the final report as a follow-up.
5. **Language specifics.** For Python, load `python-patterns`; if the batch touches tests, also `python-testing`.

Where a batch has no verification coverage, say so as you apply it, and lean harder on reading the callers.

## Phase 5 — Report

Terminal summary, no Artifact needed:

- [ ] Batches applied, with the verification result after each
- [ ] **Behaviour changes**, listed separately, each as old → new semantics
- [ ] Findings approved but **not** applied, and why
- [ ] Files changed without verification coverage — the standing risk
- [ ] Follow-ups spotted mid-flight, and anything handed to `/refactor-modules`, `/security-review`, or `/diagnosing-bugs`

Do not commit unless asked.
