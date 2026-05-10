---
description: Archive daily reports older than 90 days — extract remaining knowledge into permanent notes, tag with #archived, and move to an archive folder.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, mcp__plugin_obsidian_obsidian__move_vault_file, Read, Edit, Write, Glob, Grep
---

You are running **Archive & Distill Old Daily Reports**. Today's date: use the system date.

## Your job

Process daily reports older than 90 days: extract any remaining knowledge into permanent notes, then move each report to an archive folder.

## Steps

1. **Calculate the cutoff** — subtract 90 days from today's date. Do not use hardcoded dates.

2. **Locate daily reports** — find the folder(s) where daily reports or journal notes live. Identify all reports whose date falls before the cutoff.

3. **Understand the vault's permanent note structure** — before writing anything, scan the vault to find where project notes, research notes, standards, and backlog notes live.

4. **For each report**:

   a. **Extract knowledge** (abbreviated if already tagged `#extracted` — just check for anything missed):
      - Decisions about building or structuring something → the relevant project note
      - Tools or services evaluated → the relevant research or reference note; create if missing
      - Patterns or lessons that apply broadly → a standards or principles note
      - Things to revisit later → a backlog or future-tasks note
      - Add a wikilink back to the source report in each destination note

   b. **Tag the report** — add `#archived` to frontmatter

   c. **Move the file** — to an `Archive/YYYY/` folder near the original reports folder, where YYYY is the year of the report. Create the folder if it doesn't exist.

5. **Report** — list all processed reports and where findings were written.

## Judgment

- If multiple old reports cover the same topic, consolidate findings into one entry
- If a link in the report is dead, note it in the destination note — don't silently drop it
- Minor tasks (routine fixes, brief meetings) don't need extraction — only decisions, findings, and reusable knowledge
- A report already tagged `#extracted` can be archived quickly — just scan for anything the weekly extraction may have missed
