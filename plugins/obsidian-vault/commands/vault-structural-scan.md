---
description: Scan the whole vault for structural problems — broken wikilinks, misplaced files, frontmatter errors, and stub notes — and fix them in-place.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Structural Scan**. Scope: whole vault. Today's date: use the system date.

## Your job

Catch structural problems that accumulated since the last scan and fix them while they are still recent. Every note should be self-consistent, locatable, and connected.

## What to check

### Frontmatter problems

Validate against the **vault note schema**:

| Note type | Required properties | Notes |
|---|---|---|
| Daily (`YYYY-MM-DD.md`) | `tags`, `created`, `modified`, optionally `project`, `area` | `project`/`area` must be list-of-links |
| Weekly (`Weekly/YYYY/W{n}.md`) | `week`, `date_range`, `tags`, `harvested` | `harvested` is boolean |
| Project notes | `tags`, `created`, `modified`, optionally `aliases` | |
| Reviewed notes (outside `Work/`) | adds `reviewed` (date `YYYY-MM-DD`) | |
| Archived (`Archive/YYYY/...`) | unchanged from original — do not rewrite | |

General rules:
- Missing or empty required fields — fill them in
- All date fields in `YYYY-MM-DD` (or `YYYY-MM-DDTHH:mm:ss` for datetime properties)
- Link fields (e.g. `project:`, `area:`, `related:`) must be wikilinks, not plain text. Use single-string form for one value (`related: "[[Note]]"`) and YAML list form for multiple values
- `tags:` must be a YAML list; tag names lowercase, kebab-case
- Obsidian reserved keys (`aliases`, `cssclasses`, `tags`) — preserve if present; `aliases` and `cssclasses` are YAML lists
- Date fields that don't match the file's real ctime/mtime — correct them

### Broken links
- `[[wikilinks]]` that resolve to nothing because a note was renamed or moved — if the target is obvious from context, fix it; if ambiguous, flag it for review
- Heading links `[[Note#Heading]]` whose target heading no longer exists — flag for review
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
