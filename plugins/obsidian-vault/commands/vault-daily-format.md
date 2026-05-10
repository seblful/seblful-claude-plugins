---
description: Format and normalize today's daily report — fix frontmatter, make tasks atomic, make completed items self-explanatory, and convert bare URLs to titled links. Never changes substance or language.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Daily Report Format**. Today's date: use the system date.

## Your job

Find today's daily report and clean it up so it reads well as a future reference — without changing what was actually written.

## Steps

1. **Locate today's report.** Look for a daily note or journal entry dated today. If none exists, tell the user and stop.

2. **Fix frontmatter.**
   - Any reference fields (project, area, etc.) must be `[[wikilinks]]`, not plain text
   - `tags` must reflect the note's actual content
   - Date fields must match the file's real creation/modification dates

3. **Make planned tasks atomic.** Each item in the "planned" or "todo" section must describe exactly one concrete action. Split compound or vague items. Keep the user's original ordering.

4. **Make completed items self-explanatory.** Each item in the "done" or "completed" section must be understandable on its own six months from now — no assumed context, no pronouns with unclear referents.

5. **Make status unambiguous.** It must be clear which planned items were done, which were skipped, and which new items came up during the day. Use consistent markers throughout.

6. **Fix links.** Convert bare URLs to titled links (`[Title](url)`). Convert vault note references to `[[wikilinks]]`.

7. **Fix formatting.** Consistent heading levels, spacing, and indentation throughout.

## Hard constraints

- Do not change the meaning of anything written
- Do not change the language — preserve whatever language the note is written in
- Do not reorder items — the user's ordering is intentional
- Do not add content that wasn't in the original
