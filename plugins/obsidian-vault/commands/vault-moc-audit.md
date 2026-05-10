---
description: Audit and update MOCs (Maps of Content) and tags across the whole vault — create missing MOCs, link new notes into existing ones, consolidate near-duplicate tags. Runs on the 1st of every month.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **MOC & Tag Audit**. Scope: whole vault. Today's date: use the system date.

## Your job

Keep MOCs and tags working as the vault's navigation system. A healthy MOC is a true entry point — someone landing on it for the first time can reach any note in that domain within two clicks. A healthy tag system is minimal and consistent.

## MOC health check

| MOC | Action |
|-----|--------|
| `Data Science/MOC.md` | Exists — verify notes added this month are listed |
| `Work/MOC.md` | Exists — verify new projects and research notes are listed |
| `English/MOC.md` | Create if missing |
| `Programming/MOC.md` | Create if missing |
| `Books/MOC.md` | Create if missing |

**For missing MOCs**, create a simple navigable structure:
- One paragraph domain overview
- Grouped list of wikilinks to all major notes in that folder
- Don't over-engineer — a MOC that's easy to maintain is better than a perfect one that gets abandoned

**For existing MOCs**, find notes added this month that aren't listed yet and add them under the appropriate section.

## Tag audit

1. **Find near-duplicates** (e.g., `deep-learning` and `deeplearning`) — consolidate to the more readable, hyphenated-lowercase canonical form; update all affected notes
2. **Find missing required tags**:
   - Notes in `Work/` missing `work` and `twelvedevs` tags — add them
   - Notes in `Data Science/` missing `data-science` — add them
3. **Remove noise tags** — tags that appear on only one or two notes and don't add navigational value
4. **Evaluate new tags** — if a new project or research theme emerged this month, decide whether it deserves a canonical tag or should use an existing one

## Report

Output: MOCs created/updated, tags consolidated, tags added, tags removed.

## Judgment

- When two tags are near-duplicates, pick the more readable consistent form — prefer hyphenated lowercase
- Don't add tags mechanically — accurate specific tags beat generic ones
- A MOC doesn't need to list every file — list every important entry point
