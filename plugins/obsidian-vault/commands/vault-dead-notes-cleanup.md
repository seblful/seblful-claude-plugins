---
description: Clean up dead weight across the vault — complete or delete stubs, resolve TODO-tagged notes, connect or remove orphans, merge duplicates, and populate or delete empty glossaries. Runs monthly.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__delete_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **Dead Notes Cleanup**. Scope: whole vault. Today's date: use the system date.

## Your job

Every note in the vault should either contain knowledge worth having, or be a useful navigation point. Anything that does neither is noise. This routine removes it or brings it to completion.

## Categories to evaluate

### Stubs
Find notes tagged `#stub` or notes that are nearly empty (a title, maybe one sentence).

For each: decide one of three outcomes — complete it now, leave it with a scheduled plan in the note, or delete it. "I'll add to it later" without a plan is how stubs survive for years.

### TODO-tagged notes
Find notes with `#TODO` in their tags. Same decision: complete, schedule, or remove the tag if it no longer applies.

### Orphan notes
Find notes with no incoming links and no outgoing links (completely isolated).

For each: either connect it to the graph (add it to a MOC, link to it from a related note), or delete it if it has no place.

### Duplicate content
Find notes in different folders covering the same topic. Most likely pairs:
- `Work/twelvedevs/Research/<topic>.md` and `Data Science/<topic>.md`

For each duplicate pair: decide the canonical home, then either merge, cross-link with a clear primary, or redirect. Don't let two diverging versions of the same knowledge coexist.

### Empty glossaries
Check `Data Science/Sources/Glossary.md` and `English/Sources/Glossary.md`. For each empty one: either populate it with at least 20 meaningful terms, or delete it and remove any wikilinks pointing to it.

## Report

Output a summary: stubs resolved/deleted, TODOs resolved, orphans connected/deleted, duplicates merged/redirected, glossaries populated/deleted.

## Judgment

- A note with three lines of real, accurate content is not a candidate for deletion — short is fine, empty is not
- When merging duplicates, keep the version that is more accurate, more complete, or better formatted — not necessarily the older one
- Orphans in `Work/` may be fine as standalones (task lists, plan notes); orphan concept notes in `Data Science/` are a problem
