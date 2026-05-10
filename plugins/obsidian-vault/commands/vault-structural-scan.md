---
description: Scan the whole vault for structural problems — broken wikilinks, misplaced files, frontmatter errors, and stub notes — and fix them in-place.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Structural Scan**. Scope: whole vault. Today's date: use the system date.

## Your job

Catch structural problems that accumulated since the last scan and fix them while they are still recent. Every note should be self-consistent, locatable, and connected.

## What to check

### Frontmatter problems
- Missing or empty `tags`, `created`, or `modified` fields — fill them in
- Link fields (e.g. `project:`, `area:`) written as plain text instead of `[[wikilinks]]` — convert them
- Date fields that don't match when the file was actually created or last changed — correct them

### Broken links
- `[[wikilinks]]` that resolve to nothing because a note was renamed or moved — if the target is obvious from context, fix it; if ambiguous, flag it for review
- Image or file embeds pointing to deleted or moved attachments — flag for review

### Misplaced files
- First, understand the vault's folder structure and what each folder is meant to contain
- Identify any notes that clearly don't match their folder's purpose
- Flag misplaced files for the user rather than moving them unilaterally

### Stub notes
- Files that are essentially empty: just a title, or a title with placeholder headings and no real content
- Tag these with `#stub` so they can be scheduled for completion

## Report

After scanning, output a summary:
- Files fixed (with what was changed)
- Files flagged for human review (with reason)
- Stub notes tagged
- Broken links resolved vs. flagged

## Judgment

- A note with a few lines of real content is not a stub; a note with only headings and one sentence is
- If a broken link's target is obvious from context, fix it; if ambiguous, flag rather than guess
- Don't restructure notes that are merely different in style — only fix things that are genuinely wrong
