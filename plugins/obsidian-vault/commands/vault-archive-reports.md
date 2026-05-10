---
description: Archive daily reports older than 90 days — extract remaining knowledge into permanent notes, tag with #archived, and move to Work/twelvedevs/Reports/Archive/YYYY/. Runs on the 1st of every month.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, mcp__plugin_obsidian_obsidian__move_vault_file, Read, Edit, Write, Glob, Grep
---

You are running **Archive & Distill Old Daily Reports**. Scope: `Work/` folder only. Today's date: use the system date.

## Your job

Process daily reports older than 90 days: extract any remaining knowledge into permanent notes, then move each report to archive.

## Steps

1. **Calculate the cutoff** — subtract 90 days from today's date. Do not use hardcoded dates.

2. **Find reports to process** — scan `Work/twelvedevs/Reports/Daily Reports/` for all reports whose filename date falls before the cutoff.

3. **For each report**:

   a. **Extract knowledge** (abbreviated if already tagged `#extracted` — just check for anything missed):
      - Decisions about building/structuring → relevant project note in `Work/twelvedevs/Projects/`
      - Tools/libraries evaluated → relevant research note in `Work/twelvedevs/Research/`; create if missing
      - Patterns/lessons → `Work/twelvedevs/Standards.md`
      - Future tasks → `Work/twelvedevs/Задачи на будущее.md`
      - Add wikilink back to source report in the destination note

   b. **Tag the report** — add `#archived` to frontmatter

   c. **Move the file** — to `Work/twelvedevs/Reports/Archive/YYYY/` where YYYY is the year of the report. Create the folder if it doesn't exist.

4. **Report** — list all processed reports and where findings were written.

## Judgment

- If multiple old reports cover the same topic, consolidate findings into one entry rather than creating redundant dated sections
- If a "Материалы" link is dead, note it in the destination research note — don't silently drop it
- Minor tasks (small bug fixes, routine meetings) do not need to be extracted — only decisions, findings, and reusable knowledge
- A report already tagged `#extracted` can be archived quickly — just scan for anything the weekly extraction may have missed
