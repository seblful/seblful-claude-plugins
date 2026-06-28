# Authoring Reference Notes

Shared spec for the routines that author durable **source-of-truth** reference notes — `vault-note-create` and `vault-note-rewrite`. Each skill states its own job and its own plan; the standards both obey live here once, so they can't drift apart.

Vault mechanics are **not** repeated here. Frontmatter schema, `[[wikilinks]]`, footnote citations, heading rules, math and variable-key formatting, image alt text, MOC wiring, note creation, and CLI access all live in [CONVENTIONS.md](CONVENTIONS.md) — follow it. This file adds only what's specific to writing deep reference documents.

## What a reference note is

A reference note is the vault's single source of truth on its subject: a durable engineering-handbook entry, not a quick capture or a log. It favors theoretical depth, system-design rationale, and long-term maintainability over breadth or novelty. One subject per note (CONVENTIONS → Creating notes); when a subject is too large, narrow the scope rather than write shallow.

## Audience and voice

- Written for a mid-level machine-learning engineer who must understand and apply the subject, not merely recognize it.
- **Authoritative** — precise and definitive. State how something works and why it's built that way; don't hedge or editorialize.
- **Timeless** — no relative time references ("recently", "current state of the art", "new"). Write a standard that stays true. Name specific versions instead of "latest".

## Technical standards

- **Modern by default** — examples and logic assume current industry standards (e.g. PyTorch 2.x, the Transformers ecosystem, contemporary MLOps). Treat legacy approaches as legacy: cover one only when the note is explicitly about a legacy system; otherwise upgrade it silently.
- **Engineering bias** — prioritize scalability, robustness, and efficiency in every recommendation, and explain the design rationale behind a choice, not just the mechanism.
- **Code sparingly** — include a snippet only when it's essential for architectural clarity. Prefer high-level logic descriptions and diagrams. Any code that stays follows CONVENTIONS → Body formatting.

## Diagrams

- Use **Mermaid** fenced blocks (` ```mermaid `) for architectures, pipelines, and flowcharts — they render in Obsidian.
- Keep each diagram valid and Obsidian-compatible: simple node text, and avoid syntax Obsidian's renderer rejects (e.g. unquoted parentheses or brackets in node labels — wrap such labels in quotes). One diagram per distinct structure; don't add decorative ones.

## Document shape

The body progresses **Concept → Architecture → Implementation → Operational Considerations**: what it is and why it exists, how it's structured, how it's built, then how it's run, scaled, and maintained. Headings are descriptive and unnumbered, starting at `##` (CONVENTIONS → Headings).

## Interactive two-step workflow

These skills **never** emit the final note in one shot. They gate on the user:

1. **Plan first.** Produce the plan your skill defines — its scope/audit fields, exclusions, tech choices, and a full hierarchical `##`/`###`/`####` Table of Contents following the document shape above. Output only the plan.
2. **Stop and ask.** End the planning turn with the skill's approval question and generate nothing further until the user answers.
3. **Execute on approval.** Once approved, write the note into the vault per CONVENTIONS (frontmatter, links, footnote citations, MOC wiring), following the approved Table of Contents.
