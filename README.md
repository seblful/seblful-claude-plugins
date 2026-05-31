# Seblful Claude Plugins Marketplace

A curated marketplace of Claude Code plugins for Python development, design review, architectural refactoring, and Obsidian vault maintenance.

> **⚠️ Important:** Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's source for more information.

## Structure

- **`/plugins/python-plugin`** — Python coding and testing practices (PEP 8, type hints, pytest, uv/ruff/ty stack)
- **`/plugins/code-review`** — Senior code reviewer agent for diff and design review
- **`/plugins/refactoring`** — Architectural deepening: surface friction and reduce shallow modules
- **`/plugins/lenses`** — Perspective and communication lenses (zoom-out map, caveman terse mode)
- **`/plugins/planning`** — Stress-test plans and designs through relentless interview-style grilling
- **`/plugins/obsidian-vault`** — Scheduled maintenance routines for Obsidian vaults (formatting, weekly reports, structural scans, accuracy review)

## Installation

Add this marketplace to Claude Code:

```
/plugin marketplace add seblful/seblful-claude-plugins
```

Then install plugins individually:

```
/plugin install python-plugin@seblful-claude-plugins
/plugin install code-review@seblful-claude-plugins
/plugin install refactoring@seblful-claude-plugins
/plugin install planning@seblful-claude-plugins
/plugin install lenses@seblful-claude-plugins
/plugin install obsidian-vault@seblful-claude-plugins
```

Or browse them in `/plugin > Discover`.

## Plugins

### python-plugin

- **python-patterns** — Modern Python idioms, PEP 8, type hints, project tooling.
- **python-testing** — Pytest, fixtures, parametrization, mocking, async, coverage.

### code-review

- **code-reviewer** (agent) — Senior code reviewer that evaluates diffs across correctness, readability, architecture, security, and performance, with severity-labeled line-level suggestions.

### refactoring

- **improve-codebase-architecture** — Surface deepening opportunities and reduce shallow modules.

### planning

- **grill-me** — Stress-test a plan through relentless one-question-at-a-time interview.

### lenses

- **zoom-out** — Map the surrounding modules and callers when unfamiliar with an area.
- **caveman** — Ultra-compressed terse communication mode (~75% token reduction).

### obsidian-vault

- **vault-accuracy-review** — Verify every claim in every non-Work note and stamp reviewed dates.
- **vault-daily-format** — Normalize today's daily report (frontmatter, atomic tasks, titled links).
- **vault-inbox-ingest** — Empty the Inbox: merge each raw capture into the right note (or create one), relocate its images, wire into a MOC, delete the consumed capture.
- **vault-structural-scan** — Fix broken wikilinks, misplaced files, frontmatter errors, stale MOCs, plus dead weight (stubs, orphans, duplicates, empty notes).
- **vault-weekly-harvest** — Extract project-relevant knowledge from weekly reports into project notes, marking each report harvested.
- **vault-weekly-report** — Synthesize this week's daily reports grouped by project and archive the dailies.
- **vault-wikilink-sprint** — Add inline wikilinks between conceptually related notes, starting at hub notes.

## Plugin Structure

Each plugin follows the standard Claude Code plugin layout:

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json      # Plugin metadata (required)
    ├── skills/              # Skill definitions (optional)
    │   └── <skill-name>/
    │       └── SKILL.md
    ├── commands/            # Slash commands (optional)
    │   └── <command>.md
    ├── agents/              # Subagents (optional)
    │   └── <agent>.md
    └── hooks/               # Lifecycle hooks (optional)
```

## Contributing

Open an issue or PR if you'd like to suggest a skill, fix a bug, or improve a description.

## License

MIT — see [LICENSE](LICENSE).

## Documentation

For more information on developing Claude Code plugins, see the [official documentation](https://code.claude.com/docs/en/plugins).
