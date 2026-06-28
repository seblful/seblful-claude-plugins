# Seblful Claude Plugins Marketplace

A curated marketplace of Claude Code plugins, grouped by **what they act on**: your Python code, any codebase, your Obsidian notes, and the conversation itself.

> **⚠️ Important:** Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's source for more information.

## Structure

Four plugins, grouped by their target:

- **`/plugins/python`** — acts on Python code: coding and testing practices (type hints, pytest, the uv/ruff/ty stack)
- **`/plugins/code`** — acts on any codebase: review, bug diagnosis, and architectural deepening
- **`/plugins/obsidian-vault`** — acts on your notes: maintenance routines for Obsidian vaults
- **`/plugins/lenses`** — acts on you and the conversation: code maps, terse mode, plan grilling, and a teaching workspace

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add seblful/seblful-claude-plugins
```

Then install plugins individually:

```
/plugin install python@seblful-claude-plugins
/plugin install code@seblful-claude-plugins
/plugin install obsidian-vault@seblful-claude-plugins
/plugin install lenses@seblful-claude-plugins
```

Or browse them in `/plugin > Discover`.

## Plugins

### python

- **python-patterns** (skill) — Robust Python idioms: intent-obvious code, illegal states unrepresentable, a type-driven safety net, on top of the uv/ruff/ty stack.
- **python-testing** (skill) — Pytest, fixtures, parametrization, mocking, async, coverage.

### code

- **code-reviewer** (agent) — Senior code reviewer that evaluates diffs across correctness, readability, architecture, security, and performance, with severity-labeled line-level suggestions.
- **diagnosing-bugs** (skill) — A feedback-loop-first discipline for hard bugs and performance regressions: build a tight red-capable repro, minimise it, generate falsifiable hypotheses, instrument, fix with a regression test, then clean up.
- **codebase-design** (skill) — Shared vocabulary for designing deep modules: module, interface, depth, seam, adapter, leverage, locality, plus the deepening and design-it-twice patterns.
- **improve-codebase-architecture** (command) — Surface deepening opportunities and reduce shallow modules, presented as a visual HTML report.

### obsidian-vault

> Requires a **running Obsidian** instance, the **`obsidian` CLI** ([`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills)), and **Python 3.9+** for the deterministic scripts (stdlib only). See the [plugin README](plugins/obsidian-vault/README.md).

- **vault-daily-format** (skill) — Normalize today's daily report (frontmatter, atomic tasks, titled links).
- **vault-inbox-ingest** (skill) — Empty the Inbox: merge each raw capture into the right note (or create one), relocate its images, wire into a MOC, delete the consumed capture.
- **vault-weekly-harvest** (skill) — Extract project-relevant knowledge from weekly reports into project notes, marking each report harvested.
- **vault-weekly-report** (skill) — Synthesize this week's daily reports grouped by project and archive the dailies.
- **vault-note-create** (skill) — Author a new source-of-truth reference note from a subject: plan scope and table of contents, then write a deep, modern note on approval.
- **vault-note-rewrite** (skill) — Refactor and expand fragmented notes into a source-of-truth reference note: audit and plan, then rewrite on approval.
- **vault-moc-create** (skill) — Build or restructure a Map of Content (MOC) for a domain; the canonical hub-building routine the other skills defer to.
- **vault-accuracy-review** (command) — Verify every claim in every note (excluding Logs and the archive) and stamp reviewed dates.
- **vault-structural-scan** (command) — Fix broken wikilinks, misplaced files, frontmatter errors, stale MOCs, plus dead weight (stubs, orphans, duplicates, empty notes).
- **vault-wikilink-sprint** (command) — Add inline wikilinks between conceptually related notes, starting at hub notes.

### lenses

- **zoom-out** (command) — Map the surrounding modules and callers when unfamiliar with an area.
- **caveman** (command) — Ultra-compressed terse communication mode (~75% token reduction).
- **grill-me** (command) — Stress-test a plan through relentless one-question-at-a-time interview.
- **teach** (skill) — Stateful, multi-session teaching workspace: grounds every lesson in a mission, gathers high-trust resources, and builds storage strength through beautiful interactive HTML lessons, glossaries, and learning records.

## Plugin Structure

Each plugin follows the standard Claude Code plugin layout:

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json      # Plugin metadata (required)
    ├── skills/              # Model-invoked skills (optional)
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── commands/            # User-invoked slash commands (optional)
    │   └── <command>.md
    ├── agents/              # Subagents (optional)
    │   └── <agent>.md
    ├── scripts/             # Deterministic helpers shared by routines (optional)
    └── hooks/               # Lifecycle hooks (optional)
```

## Contributing

Open an issue or PR if you'd like to suggest a skill, fix a bug, or improve a description.

## License

MIT — see [LICENSE](LICENSE).

## Documentation

For more information on developing Claude Code plugins, see the [official documentation](https://code.claude.com/docs/en/plugins).
