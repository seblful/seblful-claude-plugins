---
description: Extract project-relevant knowledge from unprocessed weekly reports and merge it into the right project notes — no back-links, no archiving, just clean knowledge transfer.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Write, Glob, Grep
---

You are running **Knowledge Harvest**. Today's date: use the system date.

## Your job

Read weekly reports that have not yet been harvested, identify project-relevant knowledge inside them, write that knowledge into the appropriate project notes, then mark each weekly report as processed. Do not add wikilinks back to the source weekly reports. Do not archive or move anything.

## Steps

### 1. Find unprocessed weekly reports

Look in `Weekly/` (all year subfolders) for weekly report notes — files named `W{n}.md`. A report is **unprocessed** if its frontmatter does NOT contain `harvested: true`. Read all unprocessed reports before writing anything.

### 2. Map the vault's project structure

Scan the vault to find where project notes live. Build a list of known projects and their note paths so you know where to write.

### 3. For each weekly report, identify extractable knowledge

Extract only items with lasting value — skip routine entries. Look for:

| Category | Where it goes |
|---|---|
| Decisions about how to build or implement something | Relevant project note — Decisions or Architecture section |
| Technical findings (API quirks, tool behavior, config tricks) | Relevant project note — Notes / Technical Details section |
| Lessons learned, patterns worth remembering | Relevant project note — Lessons Learned section |
| Scope changes, requirement clarifications | Relevant project note — Requirements or Scope section |
| Open questions or risks that need tracking | Relevant project note — Risks / Open Questions section |
| Tasks discovered mid-work | Relevant project note — Backlog or Next Steps section |

### 4. Write to project notes

For each piece of extracted knowledge:

1. Find the right project note. If no project note exists for a referenced project, create a minimal one.
2. Place the content in the appropriate section of that note. If the section does not exist, add it.
3. Write the content as a standalone fact — no reference to "this week", "W42", or the source weekly report. It should read as if it was always part of the project note.
4. Use `[[wikilinks]]` when referencing other vault notes inline — tools, concepts, related projects. Resolve exact filenames before linking; do not guess.
5. Do not duplicate: if the same information is already in the project note, skip it or merge rather than repeat.
6. Do not add wikilinks back to the weekly report.

### 5. Mark each weekly report as processed

After successfully harvesting a weekly report, add `harvested: true` to its frontmatter. This prevents it from being processed again in future runs.

### 6. Report

List every piece of knowledge extracted, the source weekly report it came from (for your own audit trail in the chat), and the destination project note it was written to.

## Judgment

- Minor entries (routine tasks, quick check-ins) do not need extraction
- If the same finding appears across multiple weekly reports, write one consolidated entry
- Prefer adding to an existing section over creating a new one — only add a section if none fits
- If content could belong to multiple projects, write it to the primary one and mention the overlap inline
