# obsidian-vault

Maintenance and authoring routines for [Obsidian](https://obsidian.md) vaults — formatting, knowledge harvesting into projects, weekly reports by project, structural scanning, accuracy review, wikilink connectivity, inbox ingestion, and authoring or rewriting source-of-truth reference notes.

Every routine defers to [`CONVENTIONS.md`](CONVENTIONS.md) for the shared schema, link rules, heading rules, MOC detection, and the folder/archive model. The two authoring routines additionally share [`AUTHORING.md`](AUTHORING.md) for voice, technical standards, diagrams, document shape, and the plan-then-write workflow. The routines validate and edit notes *against* those conventions — and discover the vault's own conventions first when they differ from the defaults.

## Prerequisites

These routines run inside a **live Obsidian vault**, not a code repo, and reach it through the **`obsidian` CLI** — not an MCP server. Before using this plugin:

1. **Obsidian must be open** on the target vault while a routine runs (the CLI talks to the running app so the live index, daily-note config, and wikilink resolution stay correct).
2. **The `obsidian` CLI must be installed.** It ships as the `obsidian-cli` skill from [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills). Run `obsidian help` to confirm it's available and to see the authoritative command list.

Structural moves the CLI doesn't cover (archiving notes, relocating attachments, deleting consumed captures) operate on the vault folder directly with the filesystem tools.

## Routines

Lighter, everyday operations are **skills** (auto-trigger on natural language); periodic whole-vault audits are **commands** (invoke deliberately).

### Skills

- **vault-daily-format** — Normalize today's daily report: frontmatter, atomic tasks, self-explanatory completed items, titled links. Never changes substance or language.
- **vault-inbox-ingest** — Empty the Inbox: merge each raw capture into the right note (or create one), relocate its images, wire into a MOC, delete the consumed capture.
- **vault-weekly-harvest** — Extract project-relevant knowledge from unprocessed weekly reports into project notes, marking each report harvested.
- **vault-weekly-report** — Synthesize this week's daily reports grouped by project, store in `Weekly/`, and archive the dailies.
- **vault-note-create** — Author a new source-of-truth reference note on a subject: plan scope and table of contents first, then on approval write a deep, modern engineering-handbook note.
- **vault-note-rewrite** — Refactor and expand informal or fragmented notes into a source-of-truth reference note: audit and plan first, then on approval rewrite.

### Commands

- **/vault-accuracy-review** — Verify every claim in every note (excluding Logs and the archive) and stamp each with a `reviewed` date.
- **/vault-structural-scan** — Fix broken wikilinks, misplaced files, frontmatter errors, stale MOCs, plus dead weight (stubs, orphans, duplicates, empty notes).
- **/vault-wikilink-sprint** — Add inline prose wikilinks between conceptually related notes, starting at the most-referenced hub notes.

## Conventions

See [`CONVENTIONS.md`](CONVENTIONS.md) for the full specification. In brief: per-type YAML frontmatter with ISO dates, `[[wikilinks]]` for internal references, no body H1, one concept per file, a daily/weekly/archive folder model with a self-healing year sweep, and a hard rule never to change a note's language or meaning.
