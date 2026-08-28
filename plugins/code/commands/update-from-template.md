---
description: Pull the latest Copier template changes into this project — run copier update, then resolve the conflicts by intent instead of leaving markers and .rej files behind, and prove the result with the project's own gates.
argument-hint: [template ref to move to — e.g. v0.7.7 or HEAD; omit for the latest tag]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Update From Template

Bring a project back in line with the [Copier](https://copier.readthedocs.io/) template it was generated from. `copier update` does the mechanical three-way merge and stops at the first thing it cannot decide; **this command owns everything after that** — the conflict markers, the `.rej` hunks, and the gates that prove the result still works.

`$ARGUMENTS`, if given, is the template ref to move to (`v0.7.7`, `HEAD`). Omit it for the latest tag, which is what Copier picks by default.

Nothing here is tied to one template. The template URL comes from the project's own answers file, so this works on any Copier subproject; the worked examples use `gh:seblful/template-project`, which is also the default when a project has no answers file yet (Phase 5).

## Prerequisites

- **`uv`** — Copier runs through `uvx --with jinja2-time copier`, so nothing needs installing globally. The `jinja2-time` extension is not optional: templates that stamp the current year into a LICENSE fail to render without it.
- **A git repo with a clean working tree.** Copier refuses to update a dirty destination, and without a clean state there is no abort point.
- Run everything from the project root.

## Phase 0 — Find the link, then take a baseline

**The link.** Look for the answers file at the project root: `.copier-answers.yml`, or `.copier-answers.*.yml` when the project tracks more than one template. Two keys matter:

| Key | What it is |
| --- | --- |
| `_src_path` | the template — e.g. `gh:seblful/template-project` |
| `_commit` | the template version the project last synced to |

No answers file → **the project predates the template.** Go to Phase 5. Do not hand-write an answers file to force `copier update` — Copier's own docs say never to edit that file by hand, and the merge it produces is against a rendering the project never matched.

**The target.** Resolve where you are going — `gh api repos/<owner>/<name>/tags --jq '.[].name'` for a `gh:` path, `git ls-remote --tags <url>` otherwise. Default is the newest tag; `$ARGUMENTS` overrides. If `_commit` already equals the target, say so and stop.

**The preview.** Show what the template changed *before* touching anything:

```
gh api repos/<owner>/<name>/compare/<_commit>...<target> --jq '.files[] | "\(.status) \(.filename)"'
```

Group it by what it touches — dependencies, tooling config, package source, tests, assistant instructions — and list the commit subjects. This is the user's chance to say "not now".

**The baseline.** Run the project's gates *now*, before the update, and record each as green or red. Read the project's `pyproject.toml` and `CLAUDE.md`/`AGENTS.md` for the real commands; for a project on this template stack they are:

```
uv sync
uv run ruff check .
uv run ty check src/ tests/
uv run pytest -v
uv run pre-commit run --all-files
```

**A red baseline is not a blocker — it is the control.** Without it you will blame the template for a failure the project already had.

## Phase 1 — Branch, then update

```
git switch -c chore/template-update-<target>
git rev-parse HEAD          # record it — this is your abort point
```

Then:

```
uvx --with jinja2-time copier update --trust --defaults --conflict inline
```

| Flag | Why |
| --- | --- |
| `--trust` | the template runs Jinja extensions and `_tasks`; Copier refuses without it |
| `--defaults` | reuse every stored answer and take the template's default for questions added since — the non-interactive form |
| `--conflict inline` | git-style markers in place, both sides visible where the code is. `--conflict rej` instead collects rejected hunks in `.rej` files and leaves each file syntactically valid — switch to it if the markers are too tangled to work in |
| `--vcs-ref=<ref>` | only when `$ARGUMENTS` names one; otherwise Copier takes the newest tag, not `HEAD` |
| `--data key=value` | change a stored answer in the same run — a new `python_version`, a different `license`. No interactive session needed |

**Expect the template's own tasks to fail, and do not re-run.** A template whose `_tasks` format or lint the project — `ruff format .`, `ruff check --fix .`, `mdformat .` — runs them *after* the merge, and none of those can parse a file with conflict markers in it. Copier reports the task failure; the merged files are already on disk. Carry on to Phase 2. Re-running from a now-dirty tree only fails differently.

**Abort** at any point: `git reset --hard <recorded sha>` then `git clean -fd`.

## Phase 2 — Resolve what Copier could not

Find every one:

```
grep -rln "^<<<<<<<" . --exclude-dir=.git
find . -name "*.rej" -not -path "./.git/*"
```

**The rule: the project wins on content, the template wins on shape.** The template owns how the project is built — rule sets, tool tables, module skeletons, hook versions. The project owns what it actually is — its dependencies, its prose, its settings fields, its commands, its tests. A hunk that mixes both gets merged, never resolved by picking a side wholesale.

Two corollaries:

- **Lists union, they do not choose.** Dependencies, ruff `select`, pre-commit repos, gitignore lines, env keys — take both sides.
- **Deliberate divergence is the trap.** A pinned older dependency, a disabled lint rule, a rewritten `settings.py`: where the template now changes exactly the thing the project changed on purpose, do not silently adopt the template. Check `git log -- <file>` for why, and ask if the answer is not there.

| File | How it resolves |
| --- | --- |
| `pyproject.toml` | Union. Keep every real dependency the project added and its own `name`, `description`, `version`, scripts; take the template's tool tables (`[tool.ruff]`, `[tool.pytest]`, `[tool.coverage]`) whole. |
| `.pre-commit-config.yaml` | Union of hooks; take the template's `rev` bumps. |
| `CLAUDE.md` / `AGENTS.md` | Template sections describe the stack — take them. Project sections describe *this* project — keep them intact. Never let a template default overwrite a real instruction. |
| `src/<pkg>/settings.py`, `logging.py`, `cli.py` | Take the template's new shape, then re-apply the project's own settings fields, log processors and CLI commands on top. These grow project-specific code fastest. |
| `tests/conftest.py`, `tests/**` | Take the template's fixtures; keep every project test. |
| `.gitignore`, `.env*`, `.python-version` | Union. Never drop a project-specific ignore or env key, and never let a template placeholder overwrite a real local value. |
| `README.md` | The project's, always. Take only genuinely new template sections — a new command, a new gate. |
| `.copier-answers.yml` | Copier's, untouched. It records the new `_commit`; that file *is* the update. |

Anything genuinely ambiguous goes to the user with **both candidate resolutions named** — not a guess, and not a silent choice.

When you are done, delete every `.rej` file you applied and re-run both searches until they come back empty. **A left-behind marker is a broken project**, not a stray comment.

## Phase 3 — Verify

Run the formatters the template's tasks could not (`uv run ruff format .`, `uv run mdformat .`), then re-run the Phase 0 gates in order.

- **Red where the baseline was green → the update caused it.** Fix it.
- **Red where the baseline was red → inherited.** Confirm you did not make it worse, and do not fold an unrelated pre-existing fix into this change.
- **A new lint or type error from a rule the template just added is a real finding.** Fix the code. Do not disable the rule to reach green unless the user says so.

Iterate until the gates match or beat the baseline.

## Phase 4 — Report

- **Version** — `_commit` → target, with the template's commit subjects.
- **What the template changed**, grouped: dependencies, tooling config, package source, tests, assistant instructions.
- **Conflicts resolved** — one line each: file, what the template wanted, what the project wanted, what you did.
- **Surfaced, not resolved** — every ambiguity left to the user, with both candidates.
- **Answers newly defaulted** — any question the template added that `--defaults` answered on the user's behalf, so they can override it with `--data`.
- **Gates** — baseline vs. now.

Do not commit unless asked. The branch and the abort SHA stay as they are.

## Phase 5 — Adoption: a project with no answers file

A project that predates the template has no common ancestor, so **`copier update` has nothing to merge against.** Build the ancestor instead of faking it:

**1. Infer the answers** from what the project already is:

| Answer | Read it from |
| --- | --- |
| `project_slug` | `[project] name` in `pyproject.toml`, kebab-cased |
| `package_name` | the directory under `src/` |
| `project_description` | `[project] description` |
| `author_name` / `author_email` | `[project] authors` |
| `license` | the `LICENSE` file, or `None` |
| `python_version` | `.python-version`, else `requires-python` |
| `code_assistant` | `CLAUDE.md` → `claude`, `AGENTS.md` → `opencode`, `.cursorignore` → `cursor` |
| `environments` | which `.env.<env>` files exist |

Read the template's `copier.yml` for the questions it actually asks — the list above is this template's, and another template's will differ. Show the table and **confirm before generating**: a wrong `package_name` renders the whole template into the wrong path.

**2. Render a baseline into a scratch directory**, never over the project:

```
uvx --with jinja2-time copier copy --trust --defaults --data-file <scratch>/answers.yml gh:seblful/template-project <scratch>/baseline
```

The template's `_tasks` will `git init`, `uv sync` and format in there — harmless, but it takes a minute.

**3. Merge the baseline into the project** file by file, under the Phase 2 rule. Files the project lacks get added; files it has get merged; nothing is overwritten wholesale.

**4. Take `.copier-answers.yml` from `<scratch>/baseline`** — it already records the correct `_src_path` and `_commit`. From here the project is an ordinary Copier subproject and Phases 0–4 work on it.

**5. Verify and report** as in Phases 3–4, and say plainly which template files were adopted and which were skipped as inapplicable.
