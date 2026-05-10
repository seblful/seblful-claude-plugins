---
description: Review all notes outside Work/ for factual accuracy — verify every claim in every note, correct errors in-place, and tag each reviewed note with the current month.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Factual Accuracy Review**. Scope: all notes in the vault except the `Work/` folder. Today's date: use the system date.

## Your job

Read every note in scope and verify that its content is factually correct. Fix errors in-place. Tag each note after review so it is not re-reviewed unnecessarily next session.

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
- Add or update a `#reviewed-YYYY-MM` tag in frontmatter (use today's year and month)
- If a note is fully correct, still update the reviewed tag — the verification itself has value
- If a claim cannot be verified confidently, add `#needs-verification` to the note rather than leaving it silently uncertain

## Prioritization

If the vault is large and a full pass is not possible in one session, prioritize notes that lack a `#reviewed-YYYY-MM` tag entirely, then notes whose tag is oldest.

## Report

One line: `Reviewed: N | Corrected: N | Needs verification: N`. Name only the corrected and flagged notes. Nothing else.
