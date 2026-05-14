---
description: Add inline wikilinks between conceptually related notes across the vault, starting with the most-referenced hub notes — prose links only, no "See Also" dumps, no MOC curation.
allowed-tools: mcp__plugin_obsidian_obsidian__read_vault_file, mcp__plugin_obsidian_obsidian__update_vault_file, mcp__plugin_obsidian_obsidian__list_vault_directory, mcp__plugin_obsidian_obsidian__search_vault, Read, Edit, Glob, Grep
---

You are running **Wikilink Connectivity Sprint**. Scope: whole vault. Today's date: use the system date.

## Your job

Systematically build **inline prose wikilinks** between notes that are conceptually related but currently isolated. Success is measured by whether navigating from a concept to its prerequisites, applications, and related ideas becomes natural — not by the raw count of links added.

Out of scope: curating MOCs, index notes, or "See Also" sections. MOC freshness (broken entries, missing notes) is handled by `vault-structural-scan`. This command only touches links that sit inside a note's prose.

## How to prioritize

Before linking, scan the vault to identify hub notes — notes that many other notes reference or depend on conceptually, but that currently have few outgoing or incoming links. These unlock the most graph connectivity per edit.

Good candidates for hub notes:
- Core concept notes in a domain (foundational ideas that other notes build on)
- Notes about tools or frameworks that multiple other notes reference
- Notes that are frequently mentioned by name in prose but not yet linked

Start with the most isolated hubs and work outward. Note: MOCs themselves are not hub notes for this purpose — they're indexes, and their entries are listings rather than prose mentions.

## Principles for good linking

- Links appear **inline in prose** where the concept is naturally mentioned — not collected into a "See Also" section
- Only link when the connection is genuinely useful for navigation or understanding
- **Bidirectionality matters**: if note A links to note B, check whether note B should link back
- Prefer specific notes (`[[Gradient Descent]]`) over broad folder-level notes when the specific concept is what's being referenced

## Steps

1. **Identify hub notes** by scanning the vault for conceptually central but under-linked notes
2. **Read the hub note** and identify every concept mentioned that has its own note in the vault
3. **Resolve exact filenames** before linking — do not guess
4. **Add links inline** where concepts are naturally mentioned in the prose
5. **Check bidirectionality** — if the linked note doesn't reference this one, add a natural link there too
6. **Move to the next hub note**

## Hard constraints

- Do not link to notes that don't exist — that creates broken links
- Always resolve the correct filename before linking — don't approximate
- Do not add links that aren't naturally motivated by the prose
