---
description: Audit and update MOCs (Maps of Content) and tags across the whole vault — create missing MOCs, link new notes into existing ones, consolidate near-duplicate tags.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **MOC & Tag Audit**. Scope: whole vault. Today's date: use the system date.

## Your job

Keep MOCs and tags working as the vault's navigation system. A healthy MOC is a true entry point — someone landing on it for the first time can reach any note in that domain within two clicks. A healthy tag system is minimal and consistent.

## MOC health check

1. **Discover existing MOCs** — search for files named `MOC.md`, `Index.md`, or similar index files across the vault.

2. **For each existing MOC** — find notes added recently that aren't listed yet and add them under the appropriate section.

3. **Find folders without a MOC** — any top-level or major folder that lacks an index note is a candidate. For each missing MOC, create a simple navigable structure:
   - One paragraph domain overview
   - Grouped list of wikilinks to all major notes in that folder
   - Don't over-engineer — a MOC that's easy to maintain beats a perfect one that gets abandoned

## Tag audit

1. **Find near-duplicates** (e.g., `deep-learning` and `deeplearning`) — consolidate to the more readable, hyphenated-lowercase canonical form and update all affected notes
2. **Find notes missing expected folder-level tags** — if the vault uses folder-based tags (e.g., notes in a folder consistently share a tag), find notes in that folder missing the tag and add it
3. **Remove noise tags** — tags that appear on only one or two notes and don't add navigational value
4. **Evaluate new tags** — if a new topic or theme has emerged recently, decide whether it deserves a canonical tag or should use an existing one

## Report

One line: `MOCs created: N | updated: N | Tags consolidated: N | added: N | removed: N`. Nothing else.

## Judgment

- When two tags are near-duplicates, pick the more readable, consistent form — prefer hyphenated lowercase
- Don't add tags mechanically — accurate specific tags beat generic ones
- A MOC doesn't need to list every file — list every important entry point
