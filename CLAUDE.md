# CLAUDE.md

A Claude Code plugin marketplace. Plugins live in `plugins/<name>/`, each with its own `.claude-plugin/plugin.json`; the marketplace manifest is `.claude-plugin/marketplace.json`.

## What to write: skill, command, or agent

| Kind | When | Lives in |
| --- | --- | --- |
| **command** | the user invokes it — a workflow with phases and a deliverable | `commands/<slash-name>.md` |
| **skill** | the model invokes it — reference knowledge a command or a session pulls in | `skills/<name>/SKILL.md` |
| **agent** | fan-out work run in a subagent with its own tool set | `agents/<name>.md` |

**A workflow the user asks for is a command, not a skill** — that is what `849d44c` settled by moving `issue` from one to the other. When in doubt, ask which way it should go.

Process and reference are paired, not merged: `/code-sweep` ↔ `code-smells`, `/refactor-interfaces` ↔ `codebase-design`. A new command either joins that pattern or deliberately stays out of it — say which.

## Layout and frontmatter

- kebab-case directories; `SKILL.md` uppercase; a command's filename **is** its slash name.
- **Command** — `description`, `allowed-tools`, plus `argument-hint` when it takes `$ARGUMENTS`.
- **Skill** — `name`, `description`. **Agent** — `name`, `description`, optional `tools`.
- The `description` is what makes a skill trigger. Write it as *when to use this*, name the triggers, and name what it is **not** for.
- `plugins/obsidian-vault/` has its own `AUTHORING.md` and `CONVENTIONS.md` — read them before touching anything in that plugin.

## Voice

Match the files already here.

- **Imperative and dense.** No preamble, no "this document will". Cut every sentence that does not change what the reader does.
- **Phases, not narrative.** Numbered phases with a stated output each.
- **Tables and bold rules over paragraphs.** One memorable rule per section, bolded.
- **Say what goes wrong, not "cleaner".** Name the consequence.
- **Suppress false positives explicitly.** Any skill that finds problems must also say what is *not* a finding.
- **Audit before touching anything**, and **do not commit unless asked** — the house default for every command that changes files.

## Ground the shell commands you write

These files are full of literal shell invocations that have to work. Verify flags and behavior against the real docs (context7, the tool's `--help`, the actual repo) before writing them in — never from memory. Same for a template's or tool's own config: read it, don't assume it.

## Versioning

**Every change bumps two versions**, in the same commit: the touched plugin's `version` in `plugins/<name>/.claude-plugin/plugin.json`, and the marketplace `version` in `.claude-plugin/marketplace.json`. Never one without the other.

**Patch-bump both by default** — `0.5.1 → 0.5.2`, `0.13.0 → 0.13.1`. That includes adding a new skill, command, or agent.

Larger bumps happen **only when the user asks**: minor for a new skill, command, or plugin, or a change in what an existing one does; major for a breaking rename or removal. The trigger is the request, not the size of the diff.

## Keeping descriptions in sync

Each plugin's description is written twice — `plugins/<name>/.claude-plugin/plugin.json` and that plugin's entry in `.claude-plugin/marketplace.json`. Change one, change the other. Adding or removing a skill, command, or agent also means updating its bullet in `README.md`.
