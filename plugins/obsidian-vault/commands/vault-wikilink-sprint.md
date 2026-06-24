---
description: Add inline wikilinks between conceptually related notes across the vault, starting with the most-referenced hub notes — prose links only, no "See Also" dumps, no MOC curation.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Wikilink Connectivity Sprint

Systematically build **inline prose wikilinks** between notes that are conceptually related but currently isolated. Success is whether navigating from a concept to its prerequisites, applications, and related ideas becomes natural — not the raw count of links added. Scope: whole vault. Link mechanics live in [CONVENTIONS.md](../CONVENTIONS.md).

**Out of scope:** curating MOCs, index notes, or "See Also" sections. MOC freshness (broken entries, missing notes) belongs to `vault-structural-scan`. This command only touches links inside a note's prose.

## How to prioritize

Scan the vault for **hub notes** — conceptually central notes that many others depend on, but that currently have few incoming or outgoing links. These unlock the most connectivity per edit. Good candidates: core concept notes a domain builds on; tool/framework notes many others reference; notes frequently named in prose but not yet linked. Start with the most isolated hubs and work outward. MOCs are not hubs for this purpose — they're indexes, and their entries are listings, not prose mentions.

## Principles for good linking

- Links appear **inline in prose** where the concept is naturally mentioned.
- Only link when the connection is genuinely useful for navigation or understanding — never add links the prose doesn't motivate.
- **Bidirectionality matters:** if A links to B, check whether B should link back.
- Prefer the specific note (`[[Gradient Descent]]`) over a broad folder-level note when the specific concept is what's meant.

## Steps

1. Identify hub notes by scanning for conceptually central but under-linked notes.
2. Read the hub note; identify every mentioned concept that has its own note in the vault.
3. Resolve exact filenames before linking (see CONVENTIONS.md — never guess, never link a note that doesn't exist).
4. Add links inline where concepts are naturally mentioned.
5. Check bidirectionality — add a natural link back where it's missing.
6. Move to the next hub note.
