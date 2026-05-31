---
description: Scan the whole vault for structural problems and dead weight — broken wikilinks, misplaced files, frontmatter errors, stale MOCs, plus stubs, orphans, duplicates, and empty notes — and fix them in-place.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

# Structural Scan

Catch structural problems and dead weight that accumulated since the last scan and fix them while they're still recent. Every note should be self-consistent, locatable, connected, and worth keeping — either it holds knowledge worth having or it's a useful navigation point. Fix what you safely can in-place; **never delete a note** — flag deletion candidates for the user. Scope: whole vault. The canonical schema, link rules, heading rules, MOC detection, and folder/archive model live in [CONVENTIONS.md](CONVENTIONS.md); this command validates notes *against* them.

## What to check

### Frontmatter

Validate against the note schema in CONVENTIONS.md → Frontmatter (general/reviewed/daily/weekly/project/archived). Then:

- Fill missing or empty required fields.
- Ensure dates are `YYYY-MM-DD` and match the file's real ctime/mtime; correct mismatches.
- Ensure link-valued fields are wikilinks (single-string for one value, YAML list for many), `tags` is a lowercase kebab-case list, and reserved keys (`aliases`, `cssclasses`, `tags`) are preserved.
- Never rewrite frontmatter inside archived notes — they're frozen.

### Heading structure

Enforce CONVENTIONS.md → Headings: no body H1 (demote stray `#` to `##` or drop it if it just repeats the filename), top-level sections start at `##`, no skipped levels.

### Broken links

- `[[wikilinks]]` resolving to nothing (note renamed/moved) — fix if the target is obvious from context; flag if ambiguous.
- Heading links `[[Note#Heading]]` whose target heading is gone — flag for review.
- Image/file embeds pointing to deleted or moved attachments — flag for review.

### Misplaced files

- Understand the vault's folder structure and what each folder is meant to hold.
- Identify notes that clearly don't match their folder's purpose.
- Flag misplaced files for the user rather than moving them unilaterally.

### Dead weight

Find notes that are neither knowledge worth having nor useful navigation points. Resolve what you can in-place; flag the rest — **never delete anything**.

- **Stubs** (`#stub` or near-empty) — complete now, or leave a concrete plan and tag `#stub`; flag if pointless.
- **Orphans** (no incoming or outgoing links) — connect via a `[[wikilink]]` from a related note or MOC; flag if it has no place.
- **Duplicates** (same topic, different notes) — consolidate into the canonical note, cross-link with one marked primary, flag the redundant copy.
- **Empty notes** (title only) — populate or flag.

### Stale MOCs

Treat MOCs (detected by role — see CONVENTIONS.md → MOCs) as structural assertions about the vault, and check them like links:

- Entries pointing to renamed/moved/deleted notes — fix if the new target is obvious, flag if ambiguous.
- Notes that clearly belong to a MOC's domain (same folder, tag cluster, topic) but are missing from it — add them under the appropriate section.
- Empty MOC sections or duplicate entries — clean up.

Out of scope here: deciding what a MOC *should* cover, restructuring its sections, or creating new MOCs — that's editorial work, not structural validation.

## Report

- Files fixed (with what changed).
- Files flagged for human review (with reason).
- Broken links resolved vs. flagged.
- Dead weight: stubs completed/planned, orphans connected, duplicates consolidated/cross-linked, empty notes populated — and everything flagged as a deletion candidate (with reason).

## Judgment

- A note with a few lines of real, accurate content is not a stub or a deletion candidate — short is fine, empty is not.
- If a broken link's target is obvious from context, fix it; if ambiguous, flag rather than guess.
- Don't restructure or delete notes that are merely different in style — only fix what's genuinely wrong.
- When merging duplicates, keep the version that's more accurate, complete, or better formatted — not necessarily the older one.
- Standalone task lists, plan notes, and log notes are fine as orphans; isolated concept or reference notes are a problem.
- For MOCs: only mechanical upkeep (broken entries, obviously-missing notes). If a MOC's structure or scope seems wrong, flag it — don't redesign it.
