# Seblful Claude Plugins Marketplace

A curated marketplace of Claude Code plugins for Python development, design review, and architectural refactoring.

> **⚠️ Important:** Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's source for more information.

## Structure

- **`/plugins/python-plugin`** — Python coding and testing practices (PEP 8, type hints, pytest, uv/ruff/ty stack)
- **`/plugins/code-review`** — Interview-style plan grilling and senior code reviewer agent
- **`/plugins/refactoring`** — Architectural deepening and Python SOLID/clean-code refactoring
- **`/plugins/lenses`** — Perspective and communication lenses (zoom-out map, caveman terse mode)
- **`/plugins/planning`** — Stress-test plans and designs against the codebase and domain model

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
```

Or browse them in `/plugin > Discover`.

## Plugins

### python-plugin

- **python-patterns** — Modern Python idioms, PEP 8, type hints, project tooling.
- **python-testing** — Pytest, fixtures, parametrization, mocking, async, coverage.

### code-review

- **grill-me** — Stress-test a plan through relentless one-question-at-a-time interview.
- **grill-with-docs** — Grilling that updates `CONTEXT.md` and ADRs inline as decisions land.

### refactoring

- **improve-codebase-architecture** — Surface deepening opportunities and reduce shallow modules.
- **solid-refactor** — Refactor Python code to follow SOLID principles and clean-code practices.

### lenses

- **zoom-out** — Map the surrounding modules and callers when unfamiliar with an area.
- **caveman** — Ultra-compressed terse communication mode (~75% token reduction).

## Plugin Structure

Each plugin follows the standard Claude Code plugin layout:

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json      # Plugin metadata (required)
    └── skills/              # Skill definitions
        └── <skill-name>/
            └── SKILL.md
```

## Contributing

Open an issue or PR if you'd like to suggest a skill, fix a bug, or improve a description.

## License

MIT — see [LICENSE](LICENSE).

## Documentation

For more information on developing Claude Code plugins, see the [official documentation](https://code.claude.com/docs/en/plugins).
