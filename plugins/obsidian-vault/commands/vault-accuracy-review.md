---
description: Review all notes outside Work/ for factual accuracy — verify every claim in every note, correct errors in-place, and stamp each reviewed note with a reviewed date property.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Factual Accuracy Review**. Scope: all notes in the vault except the `Work/` folder. Today's date: use the system date.

## Your job

Read every note in scope and verify that its content is factually correct. Fix errors in-place. Stamp each note after review so it is not re-reviewed unnecessarily next session.

## What to verify

Check every factual claim in each note — not just a subset. This includes:

- Definitions and explanations — are they accurate?
- Descriptions of how something works — still correct?
- Version numbers, API signatures, configuration options — still valid?
- Code snippets — do they work with current versions?
- Comparisons and rankings — still accurate?
- Named examples, references, or citations — do they point to real, correct things?
- Any other concrete assertion the note makes

## After verifying each note

- Correct any errors or outdated information in-place
- When correcting references to other vault notes, use `[[wikilinks]]` instead of plain text — resolve the exact filename before linking. Use heading links (`[[Note#Section]]`) when pointing at a specific section.
- For link properties in frontmatter, use single-string form (`related: "[[Note]]"`) for one value and YAML list form for multiple values
- Add or update a `reviewed` frontmatter property set to today's date in `YYYY-MM-DD` format — same style as `created` and `modified` properties
- If a note is fully correct, still update `reviewed` — the verification itself has value
- Preserve Obsidian reserved frontmatter keys (`aliases`, `cssclasses`, `tags`) if present; do not strip them
## Prioritization

If the vault is large and a full pass is not possible in one session, prioritize notes that lack a `reviewed` property entirely, then notes whose `reviewed` date is oldest.

## Report

After the session: total notes reviewed, notes corrected.
