---
description: Extract knowledge from this week's daily reports into permanent notes in Work/twelvedevs/ — decisions, tool evaluations, patterns, and future tasks. Runs every Friday. Tags processed reports with #extracted.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **Knowledge Extraction from Daily Reports**. Scope: `Work/twelvedevs/` only — all reads and writes stay within this folder. Today's date: use the system date.

## Your job

Move knowledge trapped in this week's daily reports into permanent notes where it can be found and built upon later. The daily report becomes a pointer; the permanent note holds the knowledge.

## Steps

1. **Identify this week's reports** — scan `Work/twelvedevs/Reports/Daily Reports/` for reports dated Monday through today. Skip any already tagged `#extracted`.

2. **Read each report** and identify extractable knowledge:
   - A decision about how to build or structure something → destination: the relevant project note in `Work/twelvedevs/Projects/`, under a dated section
   - A tool, library, or service evaluated → destination: the relevant research note in `Work/twelvedevs/Research/`; if none exists, create one
   - A pattern, standard, or lesson that applies beyond one project → destination: `Work/twelvedevs/Standards.md`
   - Something to revisit or try later → destination: `Work/twelvedevs/Задачи на будущее.md`

3. **Write to destination notes**:
   - If the destination note exists, extend it — don't create a parallel note
   - If the same finding appears in multiple reports this week, consolidate into one entry
   - Add a wikilink back to the source report so the chain of reasoning is traceable
   - Skip findings that are too minor or obvious to be useful in six months

4. **Mark processed reports** — add tag `#extracted` to frontmatter of each processed report.

## What does NOT belong here

General technical knowledge (ML concepts, Python patterns, algorithms) with no specific connection to the work context. That belongs in `Data Science/` or `Programming/`, handled separately.

## Judgment

- If a finding is truly minor (routine bug fix, brief meeting), skip it
- When in doubt about destination, prefer the project note over Standards.md
- Consolidation beats duplication — one good entry beats three near-identical ones
