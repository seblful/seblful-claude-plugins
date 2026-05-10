---
description: Format and normalize today's daily work report in the Work/ folder — clean frontmatter, atomic tasks, readable summaries, and titled wikilinks. Scope is Work/ only; substance and language are never changed.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Daily Report Formatting**. Scope: `Work/` folder only. Today's date: use the system date.

## Your job

Find today's daily report in `Work/twelvedevs/Reports/Daily Reports/` and make it clean, consistent, and useful as a future reference — without changing what was actually written.

## Steps

1. **Locate** today's report. If it doesn't exist, tell the user and stop.
2. **Check frontmatter** — ensure these fields are present and accurate:
   - `project:` — must be a `[[wikilink]]` to a real note, not plain text
   - `tags:` — must reflect the work domain; add missing domain tags
   - `created:` and `modified:` — verify they match the file's actual dates
3. **Normalize "Что Буду Делать"** — each item must be atomic and actionable (one concrete thing per line). Split vague or compound items. Preserve the user's ordering.
4. **Normalize "Что Сделал"** — each item must be readable as a standalone summary. Anyone reading it six months later should understand what happened without follow-up questions. Clarify ambiguous references if the meaning is clear from context.
5. **Mark task status clearly** — it must be obvious which planned tasks were completed, which were skipped, and which new things came up unexpectedly. Use consistent markers.
6. **Fix "Материалы"** — convert bare URLs to titled links (`[Page Title](url)`). Convert vault note references to `[[wikilinks]]`.
7. **Fix formatting** — consistent spacing, indentation, and heading levels throughout.

## Hard constraints

- Do not change the substance or meaning of anything written
- Do not change the language — Russian stays Russian
- Do not reorder tasks — that ordering reflects the user's priorities
- Do not add information that wasn't in the original draft
