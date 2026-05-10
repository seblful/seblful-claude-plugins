---
description: Scan the whole vault for structural problems — broken wikilinks, misplaced files, frontmatter errors, and stub notes — and fix them in-place. Runs every Sunday.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Structural Scan**. Scope: whole vault, read-only scan with fixes applied in-place. Today's date: use the system date.

## Your job

Catch small structural problems that accumulated over the week while they are still recent and easy to fix. Every note should be self-consistent, locatable, and connected.

## What to check

### Frontmatter problems
- Missing or empty `tags`, `created`, or `modified` fields — fill them in
- `project:` written as plain text instead of `[[wikilink]]` — convert to wikilink
- Dates that don't match when the file was actually created or last changed — correct them

### Broken links
- `[[wikilinks]]` that resolve to nothing because a note was renamed or moved — if the target is obvious from context, fix it; if ambiguous, add a comment flagging it for review
- Image embeds pointing to deleted or moved attachments — flag for review

### Misplaced files
- `.md` files sitting directly in the vault root
- Programming notes inside `Data Science/`
- Work-context research inside `Texts/` instead of `Work/twelvedevs/Research/`
- Any file that clearly doesn't match its folder's purpose

### Stub notes
- Files that are essentially empty: just a title, or a title with placeholder headings and no real content
- Tag these with `#stub` so they appear in Checklist queries and can be scheduled for completion

## Report

After scanning, output a summary:
- Files fixed (list with what was changed)
- Files flagged for human review (list with reason)
- Stub notes tagged (list)
- Count of broken links resolved vs. flagged

## Judgment

- A note with five lines of real content is not a stub; a note with five lines of headings and one sentence is
- If a broken link's target is obvious from context (e.g., a renamed file), fix it; if ambiguous, flag rather than guess
- Don't restructure notes that are merely different in style — only fix things that are genuinely wrong
