---
description: Create a weekly report note by synthesizing this week's daily reports — what was done, decisions made, problems encountered, and what carries over to next week.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__create_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Write, Glob, Grep
---

You are running **Weekly Report Creation**. Today's date: use the system date.

## Your job

Read this week's daily reports and produce a single weekly report note that summarizes the week clearly and concisely. The weekly report should stand on its own — someone reading it without the daily reports should get the full picture.

## Steps

1. **Find this week's daily reports.** Locate daily notes dated Monday through today. If fewer than two exist, tell the user and ask whether to proceed.

2. **Read all of them** before writing anything. Build a complete picture of the week first.

3. **Create the weekly report note.** Place it near the daily reports (e.g. in a `Weekly/` sibling folder or the same folder with a `W` prefix). Name it clearly with the week's date range (e.g. `2024-W42` or `2024-10-14 – 2024-10-18`).

4. **Write the report with these sections:**

   ### What was accomplished
   A concise list of meaningful work completed this week. Group related items. Skip trivial or routine tasks — only include things worth remembering.

   ### Decisions made
   Any significant decisions taken this week — what was decided and why. Each entry should be understandable without reading the daily reports.

   ### Problems and blockers
   Issues encountered, their status (resolved / ongoing / escalated), and how they were handled.

   ### Carry-over
   Tasks that were planned this week but not completed, and are being moved to next week.

   ### Notes and observations
   Anything worth remembering that doesn't fit the above — patterns noticed, things to try, ideas worth revisiting.

5. **Add wikilinks** from the weekly report to each daily report it was built from.

## Judgment

- Consolidate when the same topic appears across multiple days — one entry beats five near-identical ones
- Skip items that are too minor to be worth remembering in a month
- Keep the report skimmable — prefer bullet points over prose paragraphs
- Do not invent or infer content beyond what is written in the daily reports
