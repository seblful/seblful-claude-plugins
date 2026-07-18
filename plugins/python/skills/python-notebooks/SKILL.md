---
name: python-notebooks
description: Apply when creating, editing, running, reviewing, or cleaning up Jupyter notebooks — any .ipynb work, including exploratory data analysis, ML experiments, data-driven reports, and teaching material. Enforces the reproducibility contract (Restart & Run All passes top-to-bottom), hidden-state discipline, uv-managed kernels (never !pip install in cells), promotion of stable code into src/ modules, and jupytext pairing for version control. Trigger whenever a notebook is created or modified, when a notebook fails on rerun or on someone else's machine, on notebook kernel or environment issues, and when converting between notebooks and scripts. Skip only for explicitly throwaway scratch.
---

# Jupyter Notebooks

A notebook interleaves code, results, and prose — its value is the narrative, its danger is hidden state. One contract governs everything below:

**Restart kernel → Run All must succeed top-to-bottom and reproduce the results the prose claims.**

A notebook that only works when cells run in a secret order is a broken build that renders green. Verify the contract headless before calling any notebook work done:

```bash
uv run jupyter execute notebook.ipynb                                        # run, discard outputs
uv run jupyter nbconvert --to notebook --execute --inplace notebook.ipynb    # run, keep outputs
```

## Notebook vs module

Notebooks are for exploration, analysis, experiments, reports, teaching — anywhere the narrative is the product. Logic that stabilizes or gets reused belongs in a module.

**The promotion loop:** explore in the notebook → a function stabilizes → move it to `src/` with types and tests ([[python-patterns]], [[python-testing]]) → import it back. The notebook keeps the story; the package keeps the logic. A helper copy-pasted into a second notebook is already overdue for promotion.

When importing local code, put this in the setup cell so module edits apply without kernel restarts:

```python
%load_ext autoreload
%autoreload 2
```

A notebook executed on a schedule is a script in costume — promote it. If the rendered document itself is the deliverable, parameterize it and run with `papermill`.

## Structure

1. **Markdown title cell** — the question this notebook answers, its inputs, what it produces.
2. **One setup cell** — every import, constant, seed, and path. A missing dependency then fails in seconds instead of at cell 40, and the notebook's requirements are visible at a glance.
3. **Markdown headings** section the analysis — a short lead-in per section, not an essay. The code and its output carry the story; prose only frames it.
4. **One logical step per cell** — cheap to re-run, meaningful on its own. Name intermediate results; don't chain everything into one uninspectable expression.
5. **Findings stated in a line or two** next to the evidence. Skip meta-commentary — "now we will plot the trend" narrates what the next cell already shows.

Between setup and findings, follow the data's logical order — load → inspect → clean → transform → analyze — each step building on the one before, nothing used before it's introduced. The same order holds inside each step: within a section, derive before you display. A reader scrolling top to bottom follows the reasoning without jumping around.

Keep notebooks self-descriptive and low-text. One notebook answers one clear question; when a second moves in, split.

## Hidden-state discipline

The kernel remembers everything ever executed; the file shows only what's currently there. Keep the two in sync:

- **Cells are idempotent** — running a cell twice yields the same state. Self-referential filters (`df = df[df.score > 0]`) silently shrink data on every re-run; derive a new name instead (`active = df[...]`).
- **No in-place mutation across cells** — `inplace=True` makes a cell's outcome depend on execution history. Pure transformations into new names.
- **Cell order is execution order.** If it only works run out of order, reorder until top-to-bottom is the truth.
- **One name, one meaning.** Reusing `df` for four different tables makes every cell's behavior depend on scroll position.
- Deleted cells leave their variables alive. Restart & Run All is the only proof the file matches the state.

## Environment

| Concern | Do | Never |
|:--------|:---|:------|
| Dependencies | `uv add <pkg>` — recorded in `pyproject.toml` | `!pip install` in a cell |
| Kernel | project-env kernel: `uv run python -m ipykernel install --user --name <project>` | system Python kernel |
| Launch | `uv run jupyter lab` | — |
| Lint / format | `uv run ruff check --fix` / `uv run ruff format` — native `.ipynb` support | — |

`!pip install` mutates the environment invisibly and records nothing — the notebook works today and fails for the next person (often you, after a restart). Declared in `pyproject.toml`, the same environment is reproducible anywhere.

## Determinism and data

- **Seed all randomness in the setup cell** — `rng = np.random.default_rng(SEED)`, `random.seed(SEED)`, framework seeds when used. Conclusions drawn from unseeded runs can't be reproduced or reviewed.
- **Paths from the project root via `pathlib`** — never absolute user paths, never cwd assumptions. The notebook must run from a fresh clone.
- **Cache expensive fetches** — a fetch cell writes parquet, analysis cells read it. Re-running the analysis costs seconds, so rerun-everything stays viable.
- **Secrets via env vars, never literals** — and outputs capture whatever a cell prints: a token echoed once gets committed with the file.

## Version control

Committed outputs mean megabytes of base64 images, unreviewable diffs, and whatever data got printed. Pair every notebook with a `py:percent` script via `jupytext`:

```bash
uv run jupytext --set-formats ipynb,py:percent notebook.ipynb   # pair once
uv run jupytext --sync notebook.ipynb                           # after edits
```

The paired `.py` is the reviewable, diffable source of truth in git; the `.ipynb` with its outputs stays local — gitignore it.

## Testing notebooks

Notebooks that must stay green get a CI smoke run: `uv run pytest --nbmake notebooks/`. Logic is never tested inside a notebook — that's what promotion to `src/` is for; the smoke run only proves the narrative still executes.

## Anti-patterns — fix silently

- `!pip install` in a cell → `uv add`, project kernel.
- Self-referential or in-place mutation → assign to a new name.
- Works only out of order → reorder cells.
- Helper copy-pasted across notebooks → promote to `src/`.
- Imports scattered mid-notebook → consolidate into the setup cell.
- Absolute or cwd-dependent paths → `pathlib` from project root.
- Unseeded randomness under stated conclusions → seed in setup.
- Giant do-everything notebook → split by question.
- `.ipynb` with outputs committed → pair with `jupytext`, gitignore the `.ipynb`.
- `.ipynb` edited as raw JSON → notebook-aware tooling (in Claude Code: `NotebookEdit`); the format corrupts easily.

**Before calling it done: restart, run all, top to bottom, clean.**
