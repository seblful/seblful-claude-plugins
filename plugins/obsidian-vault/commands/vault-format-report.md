---
description: Format and normalize today's daily report — clean frontmatter, atomic tasks, readable summaries, and proper links. Substance and language are never changed.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Daily Report Formatting**. Today's date: use the system date.

## Your job

Find today's daily report and make it clean, consistent, and useful as a future reference — without changing what was actually written.

## Steps

1. **Locate** today's report. Look for a daily report or journal note dated today — check folders commonly used for daily notes, journals, or logs. If no report exists, tell the user and stop.

2. **Check frontmatter** — ensure all declared fields are present and accurate:
   - Any link fields (e.g. `project:`, `area:`) must be `[[wikilinks]]` to real notes, not plain text
   - `tags:` must reflect the note's content; add any obviously missing tags
   - Date fields must match the file's actual dates

3. **Normalize planned tasks** — each item must be atomic and actionable (one concrete thing per line). Split vague or compound items. Preserve the user's ordering.

4. **Normalize completed work** — each item must be readable as a standalone summary. Anyone reading it months later should understand what happened without follow-up questions.

5. **Mark task status clearly** — it must be obvious which planned tasks were completed, which were skipped, and which new things came up unexpectedly. Use consistent markers throughout.

6. **Fix links in materials or references sections** — convert bare URLs to titled links (`[Page Title](url)`). Convert vault note references to `[[wikilinks]]`.

7. **Fix formatting** — consistent spacing, indentation, and heading levels throughout.

## Hard constraints

- Do not change the substance or meaning of anything written
- Do not change the language — if the note is in another language, keep it
- Do not reorder tasks — that ordering reflects the user's priorities
- Do not add information that wasn't in the original draft
