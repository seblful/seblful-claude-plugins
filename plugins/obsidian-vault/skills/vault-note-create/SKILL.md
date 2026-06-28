---
name: vault-note-create
description: Author a new durable source-of-truth reference note on a subject — plan the scope and table of contents first, then on approval write a deep, modern engineering-handbook note into the vault. Use when the user asks to create or write a reference, concept, or knowledge note on a topic.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Create Reference Note

Turn a subject into the vault's authoritative reference note on it: plan before writing, get approval, then author a deep note a machine-learning engineer can rely on. The authoring standard — voice, technical standards, diagrams, document shape, and the two-step workflow — lives in [AUTHORING.md](../../AUTHORING.md); vault mechanics live in [CONVENTIONS.md](../../CONVENTIONS.md). Read both before planning.

## Input

The subject to document, plus any context the user gives (desired depth, angle, constraints). If no subject is given, or it's too broad to scope into one note, ask before planning.

## Step 1 — Creation plan

First check whether the vault already covers the subject (search per CONVENTIONS → Accessing the vault). If a note already exists, the user likely wants `vault-note-rewrite` instead — say so and stop. Otherwise produce the plan:

- **Scope** — the boundaries of the note: which aspects of the subject it covers.
- **Key concepts** — the core theoretical and practical ideas it must explain.
- **Exclusions** — adjacent topics deliberately left out to keep the note focused, and where each belongs instead.
- **Technology stack** — the specific modern libraries and frameworks the examples will assume (AUTHORING → Technical standards).
- **Table of contents** — the full `##`/`###`/`####` outline, following AUTHORING → Document shape (Concept → Architecture → Implementation → Operational Considerations).

Output only the plan, then ask: *"Do you approve this plan? Type 'Yes' to proceed with the note creation."* Stop and wait.

## Step 2 — Write the note (after approval)

Write the note into the right folder and wire it in per CONVENTIONS → Creating notes (frontmatter, footnote citations, and a MOC entry or at least one incoming `[[wikilink]]`). Follow the approved table of contents and the AUTHORING standard throughout — depth over breadth, modern and timeless, diagrams where they clarify structure.

## Report

The note created (path), the sections written, and how it was wired into the vault (MOC or linking note).
