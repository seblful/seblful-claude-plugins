---
description: Add wikilinks to disconnected notes across the vault, starting with hub notes in Data Science/ then English/ — inline links only, no "See Also" dumps. Runs monthly.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Wikilink Connectivity Sprint**. Scope: whole vault; Today's date: use the system date.

## Your job

Systematically build wikilink connections between notes that are conceptually related but currently isolated. Success is measured by whether navigating from a concept to its prerequisites, applications, and related ideas becomes natural — not by the raw count of links added.

## Priority order

1. **Hub notes in `Data Science/Deep Learning/` and `Data Science/Traditional Machine Learning/`** — most referenced concepts, currently most isolated. Do these first.
2. **Math foundation notes** (`Linear Algebra`, `Probability`, `Statistics`) — link to the ML/DL notes that depend on them
3. **Framework notes** (`PyTorch`, `TensorFlow`, `YOLO`) — link to the concepts they implement
4. **`English/Grammar/` notes** — link to IELTS notes where those grammar rules are applied

## Principles for good linking

- Links appear **inline in prose** where the concept is naturally mentioned — not collected into a "See Also" section
- Only link when the connection is genuinely useful for navigation or understanding — not every mention of "neural network" needs a wikilink
- **Bidirectionality matters**: if `[[CNN]]` mentions `[[Neural Networks]]`, the Neural Networks note should have a path back
- Prefer specific sub-notes (`[[Gradient Descent]]`) over general folder notes (`[[Deep Learning]]`) when that's what's being referenced

## Steps

1. **Pick a hub note** from the priority list
2. **Read it** and identify every concept mentioned that has its own note in the vault
3. **Resolve exact filenames** before linking — do not guess
4. **Add links inline** where concepts are naturally mentioned
5. **Check bidirectionality** — if the linked note doesn't mention this one, add a natural reference there too
6. **Move to the next hub note**

## Hard constraints

- Do not add wikilinks to concepts that don't yet have a note — that creates broken links R03 will flag
- Always resolve the correct filename before linking — don't guess or approximate
- Do not add links that aren't naturally motivated by the prose
