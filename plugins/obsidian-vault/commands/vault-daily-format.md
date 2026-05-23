---
description: Format and normalize today's daily report — fix frontmatter, make tasks atomic, make completed items self-explanatory, and convert bare URLs to titled links. Never changes substance or language.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Daily Report Format**. Today's date: use the system date.

## Your job

Find today's daily report and clean it up so it reads well as a future reference — without changing what was actually written.

## Steps

1. **Locate today's report.** Look for a file named `YYYY-MM-DD.md` (Obsidian Daily Notes default) matching today's date. Check the vault root and any folder configured for daily notes. If none exists, tell the user and stop.

2. **Fix frontmatter.**
   - Reference fields (`project`, `area`, etc.) must be wikilinks, not plain text. Use single-string form for one value, YAML list form for multiple:
     ```yaml
     project: "[[Project A]]"
     area:
       - "[[Area X]]"
       - "[[Area Y]]"
     ```
     This matches Obsidian's Links property type (single) and list-of-links type (multi).
   - `tags` must be a YAML list and reflect the note's actual content. Use lowercase, kebab-case tag names (`#deep-work`, not `#DeepWork` or `#TODO`).
   - Date fields must match the file's real creation/modification dates in `YYYY-MM-DD` format.
   - Preserve Obsidian's reserved keys (`aliases`, `cssclasses`, `tags`) if present.

3. **Make planned tasks atomic.** Each item in the "planned" or "todo" section must describe exactly one concrete action and use Obsidian task syntax (`- [ ]` open, `- [x]` done). Split compound or vague items. Keep the user's original ordering.

4. **Make completed items self-explanatory.** Each item in the "done" or "completed" section must be understandable on its own six months from now — no assumed context, no pronouns with unclear referents.

5. **Make status unambiguous.** It must be clear which planned items were done and which new items came up during the day. Use the task markers above consistently.

6. **Fix links.** Convert bare URLs to titled links (`[Title](url)`). Convert vault note references to `[[wikilinks]]`. Use heading links (`[[Note#Section]]`) when referring to a specific section of another note.

7. **Fix formatting.** Consistent heading levels, spacing, and indentation throughout. No level-1 heading (`# ...`) in the body — the filename is the title. Top-level sections start at `##`; demote any stray `#` heading.

## Hard constraints

- Do not change the meaning of anything written
- Do not change the language — preserve whatever language the note is written in
- Do not reorder items — the user's ordering is intentional
- Do not add content that wasn't in the original
