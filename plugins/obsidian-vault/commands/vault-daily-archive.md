---
description: Archive daily reports older than 90 days — move them to an Archive/YYYY/ folder and tag them #archived. Extracts any knowledge not yet captured into permanent notes.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, mcp__plugin_obsidian_obsidian__move_vault_file, Read, Edit, Write, Glob, Grep
---

You are running **Daily Report Archive**. Today's date: use the system date.

## Your job

Move old daily reports out of the active view and into an archive, after making sure any valuable knowledge inside them has been captured elsewhere.

## Steps

1. **Calculate the cutoff.** Subtract 90 days from today. Do not use hardcoded dates.

2. **Find daily reports to archive.** Locate the folder(s) where daily reports live. Identify all reports whose date falls before the cutoff.

3. **Scan the vault's permanent note structure.** Before writing anything, find where long-lived knowledge is stored — project notes, reference notes, standards or principles notes, and backlog notes.

4. **For each report:**

   a. **Check for unextracted knowledge.** Skip this step if the report is already tagged `#extracted` — just do a quick scan for anything missed. Otherwise, extract:
      - Decisions about how to build or do something → the relevant project or reference note
      - Tools or services evaluated → the relevant reference note; create one if it doesn't exist
      - Lessons or patterns worth keeping → a standards or principles note
      - Tasks to revisit → a backlog note
      - Add a `[[wikilink]]` back to the source report in each destination note

   b. **Tag the report.** Add `#archived` to its frontmatter.

   c. **Move the report** to `Archive/YYYY/` next to the reports folder, where YYYY is the year of the report. Create the folder if it doesn't exist.

5. **Report.** List every archived report and where any extracted findings were written.

## Judgment

- Minor entries (routine tasks, brief check-ins) do not need extraction — only decisions, findings, and reusable knowledge
- If the same finding appears across multiple reports, write one consolidated entry rather than duplicates
- If a link inside the report is dead, note it in the destination note rather than silently dropping it
