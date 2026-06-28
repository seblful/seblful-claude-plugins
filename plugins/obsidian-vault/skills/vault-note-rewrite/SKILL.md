---
name: vault-note-rewrite
description: Refactor and expand informal or fragmented notes into a durable source-of-truth reference note — audit and plan the changes first, then on approval rewrite into a deep, modern, well-structured note. Use when the user asks to rewrite, refactor, clean up, restructure, or expand an existing note or pasted notes.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Rewrite Into Reference Note

Refactor, correct, and expand fragmented engineering notes into the vault's authoritative reference on the subject: audit and plan before touching anything, get approval, then rewrite. The authoring standard — voice, technical standards, diagrams, document shape, and the two-step workflow — lives in [AUTHORING.md](../../AUTHORING.md); vault mechanics live in [CONVENTIONS.md](../../CONVENTIONS.md). Read both before planning.

## Input

The note(s) to rewrite — a vault note name/path, or pasted text. Read the source in full (and any notes it links) before planning. Never change the source's language (CONVENTIONS → Language and substance).

## Step 1 — Refactoring plan

Audit the source and produce the plan:

- **Proposed changes** — the key structural and thematic restructuring, each with its rationale.
- **Corrections** — inaccuracies, deprecated logic, and errors found in the source, each with its fix.
- **Exclusions** — content to cut (irrelevant tangents, duplication), each with justification.
- **Technology updates** — specific legacy libraries or methods to replace with modern standards (AUTHORING → Technical standards).
- **Table of contents** — the full `##`/`###`/`####` outline of the rewritten note, following AUTHORING → Document shape.

Output only the plan, then ask: *"Do you approve this plan? Type 'Yes' to proceed with the rewrite."* Stop and wait.

## Step 2 — Rewrite (after approval)

Apply the approved plan and the AUTHORING standard. If the source is an existing vault note, rewrite it in place and bump `modified` per CONVENTIONS; if it's pasted text, create the note per CONVENTIONS → Creating notes. Preserve what already works — keep the source's language, and retain its images, embeds, and citations in their logical positions, re-formatted per CONVENTIONS → Links and Body formatting. Wire the result into a MOC if it isn't already.

## Report

The note rewritten (path), the structural changes and corrections applied, content cut, and technology updated.
