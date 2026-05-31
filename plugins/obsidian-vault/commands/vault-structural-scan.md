---
description: Scan the whole vault for structural problems and dead weight — broken wikilinks, misplaced files, frontmatter errors, stale MOCs, plus stubs, orphans, duplicates, and empty notes — and fix them in-place.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Structural Scan**. Scope: whole vault. Today's date: use the system date.

## Your job

Catch structural problems and dead weight that accumulated since the last scan and fix them while they are still recent. Every note should be self-consistent, locatable, connected, and worth keeping — either it contains knowledge worth having or it's a useful navigation point. Fix what you safely can in-place (frontmatter, headings, links, connecting orphans); **never delete a note** — flag deletion candidates for the user to decide.

## What to check

### Frontmatter problems

Validate against the **vault note schema**:

| Note type | Required properties | Notes |
|---|---|---|
| Daily (`YYYY-MM-DD.md`) | `tags`, `created`, `modified`, optionally `project`, `area` | `project`/`area` must be list-of-links |
| Weekly (`Weekly/W{n}.md`) | `year`, `week`, `tags`, `harvested` | `harvested` is boolean; `Weekly/` sits next to `Daily/` |
| Project notes | `tags`, `created`, `modified`, optionally `aliases` | |
| Reviewed notes (outside `Work/`) | adds `reviewed` (date `YYYY-MM-DD`) | |
| Archived (`Archive/Daily/YYYY/...`, `Archive/Weekly/YYYY/...`) | unchanged from original — do not rewrite | `Archive/` sits next to `Daily/` and `Weekly/` |

General rules:
- Missing or empty required fields — fill them in
- All date fields in `YYYY-MM-DD` (or `YYYY-MM-DDTHH:mm:ss` for datetime properties)
- Link fields (e.g. `project:`, `area:`, `related:`) must be wikilinks, not plain text. Use single-string form for one value (`related: "[[Note]]"`) and YAML list form for multiple values
- `tags:` must be a YAML list; tag names lowercase, kebab-case
- Obsidian reserved keys (`aliases`, `cssclasses`, `tags`) — preserve if present; `aliases` and `cssclasses` are YAML lists
- Date fields that don't match the file's real ctime/mtime — correct them

### Heading structure

- Notes must not contain any level-1 heading (`# ...`) in the body — the filename plays that role, and Obsidian renders it as the page title. A body-level H1 duplicates that.
- Top-level sections start at `##`. Demote any `#` heading to `##`, or delete it if it merely repeats the filename.
- Heading levels must not skip (e.g. `##` followed by `####`) — fix by promoting the deeper heading.

### Broken links
- `[[wikilinks]]` that resolve to nothing because a note was renamed or moved — if the target is obvious from context, fix it; if ambiguous, flag it for review
- Heading links `[[Note#Heading]]` whose target heading no longer exists — flag for review
- Image or file embeds pointing to deleted or moved attachments — flag for review

### Misplaced files
- First, understand the vault's folder structure and what each folder is meant to contain
- Identify any notes that clearly don't match their folder's purpose
- Flag misplaced files for the user rather than moving them unilaterally

### Dead weight

Find notes that are neither knowledge worth having nor useful navigation points. Resolve what you can in-place; flag the rest — **never delete anything**.

- **Stubs** (`#stub` or near-empty) — complete now, or leave a concrete plan and tag `#stub`; flag if pointless.
- **Orphans** (no incoming or outgoing links) — connect via a `[[wikilink]]` from a related note or MOC; flag if it has no place.
- **Duplicates** (same topic, different notes) — consolidate into the canonical note, cross-link with one marked primary, flag the redundant copy.
- **Empty notes** (title only) — populate or flag.

### Stale MOCs
Treat MOCs (files named `MOC.md`, `Index.md`, or notes that function as folder/domain indexes) as structural assertions about the vault — and check them the same way you check links.

- Entries in a MOC that point to renamed, moved, or deleted notes — fix if the new target is obvious, flag if ambiguous
- Notes that clearly belong to a MOC's domain (same folder, same tag cluster, same topic) but are missing from it — add them under the appropriate section
- Empty MOC sections or duplicate entries — clean up

Out of scope here: deciding what a MOC *should* cover, restructuring its sections, or creating new MOCs from scratch — that's editorial work, not structural validation.

## Report

After scanning, output a summary:
- Files fixed (with what was changed)
- Files flagged for human review (with reason)
- Broken links resolved vs. flagged
- Dead weight: stubs completed/planned, orphans connected, duplicates consolidated/cross-linked, empty notes populated — and everything flagged as a deletion candidate (with reason)

## Judgment

- A note with a few lines of real, accurate content is not a stub or a deletion candidate — short is fine, empty is not
- If a broken link's target is obvious from context, fix it; if ambiguous, flag rather than guess
- Don't restructure or delete notes that are merely different in style — only fix things that are genuinely wrong
- When merging duplicates, keep the version that is more accurate, complete, or better formatted — not necessarily the older one
- Standalone task lists, plan notes, and log notes are fine as orphans; isolated concept or reference notes are a problem
- For MOCs: only do mechanical upkeep (broken entries, obviously-missing notes). If a MOC's structure or scope seems wrong, flag it — don't redesign it
