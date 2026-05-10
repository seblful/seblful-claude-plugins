---
description: Create a weekly report note by synthesizing this week's daily reports — grouped by project, stored in Weekly/YYYY/W{n}, then archive the daily notes.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, mcp__plugin_obsidian_obsidian__move_vault_file, Read, Write, Glob, Grep
---

You are running **Weekly Report Creation**. Today's date: use the system date.

## Your job

Read this week's daily reports, produce a weekly report note grouped by project, store it under `Weekly/YYYY/`, then archive the daily notes.

## Steps

### 1. Locate this week's daily reports

Find daily notes dated Monday through today. If fewer than two exist, tell the user and ask whether to proceed.

### 2. Read everything first

Read all daily reports before writing anything. Build a full picture — note which projects appear and what was done per project.

### 3. Create the weekly report note

**Path:** `Weekly/{YYYY}/W{week_number}.md` — e.g. `Weekly/2024/W42.md`  
Use ISO week number (Monday-anchored). Create the year folder if it does not exist.

**Structure:**

```markdown
---
week: {YYYY-Wnn}
date_range: {YYYY-MM-DD} – {YYYY-MM-DD}
tags: [weekly-report]
---

# W{n} — {YYYY}

## {Project Name} [[Project Name]]

### Accomplished

- …

### Decisions

- …

### Problems

- …

### Carry-over

- …

---

## {Another Project} [[Another Project]]

…

---

## Cross-project / General

### Notes and observations

- …
```

**Grouping rules:**

- One `##` section per project that appeared in the daily reports. Use the exact vault name of the project note as the heading and add a `[[wikilink]]` to it inline.
- If an entry does not belong to any specific project, place it under `## Cross-project / General`.
- Within each project section use four sub-sections: Accomplished, Decisions, Problems, Carry-over. Omit a sub-section if it has no entries.
- Consolidate: if the same work appears across multiple days, write one entry, not five.
- Skip trivial or purely routine items.
- Accomplished — one bullet per outcome, not per task. Group anything that served the same goal. Daily granularity belongs in notes, not here.

**Add wikilinks** from the weekly report to each daily note it was built from (list them at the bottom under `## Sources`).

### 4. Archive the daily notes and their attachments

After the report is created and saved, for each daily note included in the report:

1. **Find attachments.** Scan the daily note for embedded files — images, PDFs, audio, and other non-markdown files referenced via `![[filename]]` or `![](path)` syntax. Also check for any attachment folder that mirrors the note name (e.g. `2024-10-14/` or `attachments/2024-10-14/`).

2. **Move the note** to `Archive/{YYYY}/` (where YYYY is the year of that note). Create the folder if it does not exist.

3. **Move the attachments.** Move each attachment file to `Archive/{YYYY}/attachments/`. Create the folder if it does not exist. After moving, do not update the links inside the archived note — they are archived and no longer need to resolve.

Report which notes and attachments were moved and where.

## Judgment

- Prefer bullet points over prose
- Do not invent or infer content beyond what is written in the daily reports
- If a project note does not exist in the vault, still create the section — use the name from the daily note
