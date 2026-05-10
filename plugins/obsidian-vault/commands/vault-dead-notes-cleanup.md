---
description: Clean up dead weight across the vault — complete or delete stubs, resolve TODO-tagged notes, connect or remove orphans, and merge duplicate notes.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__delete_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **Dead Notes Cleanup**. Scope: whole vault. Today's date: use the system date.

## Your job

Every note in the vault should either contain knowledge worth having or be a useful navigation point. Anything that does neither is noise. This routine removes it or brings it to completion.

## Categories to evaluate

### Stubs
Find notes tagged `#stub` or notes that are nearly empty (a title, maybe one sentence).

For each: decide one of three outcomes — complete it now, leave it with a concrete plan written into the note, or delete it. "I'll add to it later" without a plan is how stubs survive for years.

### TODO-tagged notes
Find notes with `#TODO` in their tags. Same decision: complete, schedule with a concrete plan, or remove the tag if it no longer applies.

### Orphan notes
Find notes with no incoming links and no outgoing links (completely isolated).

For each: either connect it to the graph (add it to a MOC, link to it from a related note) or delete it if it has no place.

### Duplicate content
Find notes in different folders covering the same topic. Look for notes with very similar titles or overlapping content.

For each duplicate pair: decide the canonical home, then either merge, cross-link with a clear primary, or redirect. Don't let two diverging versions of the same knowledge coexist.

### Empty notes
Find notes that are completely empty or contain only a title. Decide: populate or delete.

## Report

One line: `Stubs: N resolved, N deleted | TODOs: N resolved | Orphans: N connected, N deleted | Duplicates: N merged | Empty: N populated, N deleted`. Nothing else.

## Judgment

- A note with a few lines of real, accurate content is not a candidate for deletion — short is fine, empty is not
- When merging duplicates, keep the version that is more accurate, more complete, or better formatted — not necessarily the older one
- Standalone task lists, plan notes, and log notes are fine as orphans; isolated concept or reference notes are a problem
