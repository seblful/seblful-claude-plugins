---
description: Create a weekly report note by synthesizing this week's daily reports — grouped by project, stored in a Weekly/ folder next to the daily reports, then archive the daily notes.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, mcp__plugin_obsidian_obsidian__move_vault_file, Read, Write, Glob, Grep
---

You are running **Weekly Report Creation**. Today's date: use the system date.

## Your job

Read this week's daily reports, produce a weekly report note grouped by project, store it in a `Weekly/` folder next to where the daily reports live, then archive the daily notes.

## Steps

### 1. Locate this week's daily reports

Find daily notes dated Monday through today. If fewer than two exist, tell the user and ask whether to proceed.

### 2. Read everything first

Read all daily reports before writing anything. Build a full picture — note which projects appear and what was done per project.

### 3. Keep `Weekly/` scoped to the current year

`Weekly/` is a flat folder of `W{nn}.md` files, so it can only hold one year's reports at a time without filename collisions. Whenever this routine touches `Weekly/`, sweep out anything that belongs to a previous year: read the `year:` property of each report and, for any whose `year` is earlier than the current year, archive it using the mirror principle from step 5 — a report in `Weekly/` moves to `Archive/Weekly/{that_year}/`.

This makes the rule self-healing: if a year boundary is crossed without the sweep running, the next invocation cleans up.

### 4. Create the weekly report note

**Path:** the weekly folder is a sibling of the daily-reports folder, wherever the user keeps dailies. Place the report in a `Weekly/` folder at that same level, creating it if needed. Filename: `W{nn}.md` — e.g. `W42.md`. Use ISO 8601 week number (Monday-anchored), equivalent to moment.js `gggg-[W]ww`.

**Structure:**

```markdown
---
year: {YYYY}
week: {nn}
tags:
  - weekly-report
harvested: false
---

# W{nn}

## [[Project Name]]

> [!success] Accomplished
> - …

> [!note] Decisions
> - …

> [!warning] Problems
> - …

> [!todo] Carry-over
> - …

---

## [[Another Project]]

…

---

## Cross-project / General

### Notes and observations

- …

## Sources

- [[YYYY-MM-DD]]
- [[YYYY-MM-DD]]
```

**Grouping rules:**

- One `##` section per project that appeared in the daily reports. The heading itself is the `[[wikilink]]` to the project note — no separate inline link needed.
- If an entry does not belong to any specific project, place it under `## Cross-project / General`.
- Within each project section use four callouts: `> [!success] Accomplished`, `> [!note] Decisions`, `> [!warning] Problems`, `> [!todo] Carry-over`. Omit a callout if it has no entries.
- Consolidate: if the same work appears across multiple days, write one entry, not five.
- Skip trivial or purely routine items.
- Accomplished — one bullet per outcome, not per task. Group anything that served the same goal. Daily granularity belongs in notes, not here.
- `harvested: false` marks the report as eligible for knowledge harvesting; the harvest routine flips it to `true` once processed.

**Add wikilinks** from the weekly report to each daily note it was built from under `## Sources`. Use the daily note filename (`[[YYYY-MM-DD]]`).

### 5. Archive the daily notes and their attachments

**Archive principle:** archive paths mirror live paths under a top-level `Archive/` folder that sits next to `Daily/` and `Weekly/`. A note that lives at `Daily/...` is archived to `Archive/Daily/...`; a note at `Weekly/...` is archived to `Archive/Weekly/...`. The mirror always partitions by year (`Archive/Daily/{YYYY}/`, `Archive/Weekly/{YYYY}/`), using the year the note belongs to.

After the report is created and saved, for each daily note included in the report:

1. **Find attachments.** An attachment is any non-markdown file the note depends on. That covers anything embedded via `![[filename]]` or `![](path)` syntax (images, PDFs, audio, canvases, etc.) and any sibling folder named after the note (e.g. `2024-10-14/` or `attachments/2024-10-14/`).

2. **Move the note** into the mirrored archive path (`Archive/Daily/{YYYY}/`), creating folders as needed.

3. **Move the attachments** into an `attachments/` subfolder of that same archive path (`Archive/Daily/{YYYY}/attachments/`). Do not rewrite links inside the archived note — archived content is frozen and does not need to resolve.

Report which notes and attachments were moved and where.

## Judgment

- Prefer bullet points over prose
- Do not invent or infer content beyond what is written in the daily reports
- If a project note does not exist in the vault, still create the section — use the name from the daily note
