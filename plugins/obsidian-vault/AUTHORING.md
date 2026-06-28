# Authoring Reference Notes

Shared spec for the routines that author durable **source-of-truth** reference notes — `vault-note-create` and `vault-note-rewrite`. Each skill states its own job and its own plan; the standards both obey live here once, so they can't drift apart.

Vault mechanics are **not** repeated here. Frontmatter schema, `[[wikilinks]]`, footnote citations, heading rules, math and variable-key formatting, image alt text, MOC wiring, note creation, and CLI access all live in [CONVENTIONS.md](CONVENTIONS.md) — follow it. This file adds only what's specific to writing deep reference documents.

## What a reference note is

A reference note is the vault's single source of truth on its subject: a durable engineering-handbook entry, not a quick capture or a log. It favors theoretical depth, system-design rationale, and long-term maintainability over breadth or novelty. One subject per note (CONVENTIONS → Creating notes); when a subject is too large, narrow the scope rather than write shallow.

## Scoping: one note or a cluster

A reference note holds one subject, but a subject can be larger than one note. Decide the shape before outlining:

- **One note** — a single coherent concept whose depth fits one readable note.
- **A cluster** — a domain ("Transformers", "Distributed training") whose sub-topics are each note-worthy. Plan a short hub/MOC note plus a small set of linked sub-notes, one concept each, rather than one sprawling note. The hub follows CONVENTIONS → MOCs.

Bias toward depth over size: if a section of the outline is itself note-worthy, split it into its own note and link it rather than bury it. Never pad to feel comprehensive.

## Audience and voice

- Written for a mid-level machine-learning engineer who must understand and apply the subject, not merely recognize it.
- **Authoritative** — precise and definitive. State how something works and why it's built that way; don't hedge or editorialize.
- **Timeless** — no relative time references ("recently", "current state of the art", "new"). Write a standard that stays true. Name specific versions instead of "latest".

## Technical standards

- **Modern by default** — examples and logic assume current industry standards. Treat legacy approaches as legacy: cover one only when the note is explicitly about a legacy system; otherwise upgrade it silently.
- **Engineering bias** — prioritize scalability, robustness, and efficiency in every recommendation, and explain the design rationale behind a choice, not just the mechanism.
- **Code sparingly** — include a snippet only when it's essential for architectural clarity. Prefer high-level logic descriptions and diagrams. Any code that stays follows CONVENTIONS → Body formatting.

## Research and grounding

A source-of-truth note must be verifiable, not recalled from memory — a note full of plausible-but-wrong API signatures or version numbers is the exact failure `vault-accuracy-review` exists to catch. Before and while writing:

- **Verify every concrete claim against a real source** — version numbers, API signatures, configuration options, benchmark figures, named references. Prefer authoritative primary documentation; use a documentation MCP such as context7 when the session has one, otherwise web search and fetch.
- **Cite what you consulted.** Every external claim or definition gets a footnote pointing at the source actually used (CONVENTIONS → Links). Never cite a source you didn't read.
- **Don't invent citations or numbers.** If a fact can't be verified, state it as a general principle without a fabricated reference, or leave it out.

The bar: a note this skill produces should pass `vault-accuracy-review` unchanged.

## Diagrams

- Use **Mermaid** fenced blocks (` ```mermaid `) for architectures, pipelines, and flowcharts — they render in Obsidian.
- Keep each diagram valid and Obsidian-compatible: simple node text, and avoid syntax Obsidian's renderer rejects (e.g. unquoted parentheses or brackets in node labels — wrap such labels in quotes). One diagram per distinct structure; don't add decorative ones.

## Document shape

The body progresses **Concept → Architecture → Implementation → Operational Considerations**: what it is and why it exists, how it's structured, how it's built, then how it's run, scaled, and maintained. Headings are descriptive and unnumbered, starting at `##` (CONVENTIONS → Headings).

## Connecting the note

The note joins the vault's graph, not just a folder. Go beyond the CONVENTIONS minimum (one incoming link or a MOC entry):

- **Survey related notes first.** Before writing, find the existing notes for the subject's prerequisites, applications, and sibling concepts.
- **Link out** from the prose to those notes where each concept is naturally mentioned (CONVENTIONS → Links).
- **Link in.** Add a natural inline link from the most relevant existing notes back to this one, so it's reachable from where readers already are.

Bidirectionality is the goal (the `vault-wikilink-sprint` principle), done at authoring time instead of as later cleanup.

## Interactive workflow

These skills **never** emit the final note in one shot. They gate on the user:

1. **Research and plan.** Ground the subject (Research and grounding) and survey the graph (Connecting the note), then produce the plan your skill defines — its scope/audit fields, the one-note-or-cluster decision (Scoping), exclusions, tech choices, planned connections, and a full hierarchical `##`/`###`/`####` Table of Contents following the document shape above. Output only the plan.
2. **Stop and ask.** End the planning turn with the skill's approval question and generate nothing further until the user answers.
3. **Execute on approval.** Write the note(s) into the vault per CONVENTIONS (frontmatter, links, footnote citations, connections), following the approved Table of Contents.
4. **Verify before reporting** (Verify before done).

## Verify before done

Before reporting the note complete, check and fix:

- Every footnote reference `[^n]` has a matching definition and vice versa (CONVENTIONS → Links).
- Every `[[wikilink]]` resolves to a real note — no accidental broken links (CONVENTIONS → Links).
- Each Mermaid block is valid and renders in Obsidian (Diagrams).
- Every concrete claim that needs a source has one (Research and grounding).
- Frontmatter, headings, and math match CONVENTIONS.
