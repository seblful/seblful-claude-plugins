---
description: Extract knowledge from this week's daily reports into permanent notes — decisions, tool evaluations, patterns, and future tasks. Tags processed reports with #extracted.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **Knowledge Extraction from Daily Reports**. Today's date: use the system date.

## Your job

Move knowledge trapped in this week's daily reports into permanent notes where it can be found and built upon later. The daily report becomes a pointer; the permanent note holds the knowledge.

## Steps

1. **Locate this week's reports** — find daily reports or journal notes dated Monday through today. Skip any already tagged `#extracted`.

2. **Identify the vault's permanent note structure** — before writing anything, scan the vault to understand where permanent knowledge lives: look for project notes, research notes, reference notes, standards or principles notes, and backlog or future-tasks notes.

3. **Read each report** and identify extractable knowledge. Route each finding to the most appropriate permanent note based on what you found in step 2:
   - Decisions about how to build or structure something → the relevant project note, under a dated section
   - A tool, library, or service evaluated → the relevant reference or research note; create one if it doesn't exist
   - A pattern, standard, or lesson that applies broadly → a standards or principles note
   - Something to revisit or try later → a backlog or future-tasks note

4. **Write to destination notes**:
   - If the destination note exists, extend it — don't create a parallel note
   - If the same finding appears in multiple reports this week, consolidate into one entry
   - Add a wikilink back to the source report so the chain of reasoning is traceable
   - Skip findings that are too minor or obvious to be useful in six months

5. **Mark processed reports** — add tag `#extracted` to frontmatter of each processed report.

## Judgment

- If a finding is truly minor (routine task, brief meeting), skip it
- Consolidation beats duplication — one good entry beats three near-identical ones
- When the right destination is unclear, prefer a more specific note over a general one
