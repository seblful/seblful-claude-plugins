---
description: Scan a codebase for deepening opportunities — shallow modules, wrong seams, leaking interfaces — present them as a visual Artifact report, then work through whichever one you pick.
allowed-tools: Read, Glob, Grep, Agent, Write, Skill, Artifact
---

# Refactor Interfaces

Surface architectural friction and propose **deepening opportunities** — refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

## Scope: interfaces and seams, not implementations

This command changes **interfaces** and where they live. Its sibling `/code-sweep` changes implementations and leaves every interface intact. One rule decides:

> **Would the fix change what a caller must know?**
> **Yes** → it belongs here. **No** → hand it to `/code-sweep`.

So splitting a god object, deleting a wrapper callers go through, moving a seam, and reshaping a signature are all in scope. Fixing a swallowed exception, flattening nesting, deleting dead code, and renaming a local are not — a caller's view is unchanged, so they belong to `/code-sweep` and its `code-smells` catalog. When the scan turns those up, close with one line pointing at `/code-sweep`; don't fix them here, and don't give them cards.

The two outputs are deliberately different in shape, so they never read as the same document: `/code-sweep` just lists its findings — a numbered defect list, tiered by severity and evidenced by before/after **code** — and ends by applying fixes in batches. This one is a **diagram-led Artifact**, and ends in a design conversation.

This command is built on a shared design vocabulary:

- Load the `codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion — don't drift into "component," "service," "API," or "boundary."
- Use the codebase's own domain terms for the modules — not generic names like "FooBarHandler" or "the Order service."

## Process

### 1. Explore

Use the Agent tool with `subagent_type=Explore` to walk the codebase. Don't follow rigid heuristics — explore organically and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow** — interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow: would deleting it concentrate complexity, or just move it? A "yes, concentrates" is the signal you want.

### 2. Present candidates as an Artifact report

Publish the review as a **Claude Artifact** so the user gets a clickable, shareable URL and nothing lands in the repo.

**The page design is already decided.** The report is `$CLAUDE_PLUGIN_ROOT/skills/codebase-design/REPORT-TEMPLATE.html` — a complete, publishable page with one worked candidate in it (if `$CLAUDE_PLUGIN_ROOT` is unset, use this plugin folder's real path). Copy it to the session scratchpad as `refactor-interfaces-audit.html` and fill the slots. Three rules make every run of this command produce the same document:

> **Fill slots, never restyle.** Don't touch the `<style>` block, don't add a class the template doesn't define, don't introduce a font, a colour, or a section. A candidate is added by duplicating the `<article class="candidate">` block whole and rewriting its contents.
> **One diagram form.** Every diagram is a mermaid `flowchart LR`, in a before/after pair, carrying the template's `classDef` block unchanged — that block is what makes the legend true.
> **Fixed identity.** Title `Interface Audit — <repo>` (already in the template), `favicon` 🧱, `icon` `report`, filename `refactor-interfaces-audit.html`. Same repo, same filename, same URL on a re-review.

Load the `artifact-design` skill before publishing — the Artifact contract requires it — but read it for the publishing mechanics only. **The template owns the look**; a design idea it doesn't already contain is out of scope for this command.

Then call `Artifact` with the scratchpad path, that `favicon` and `icon`, and a one-sentence `description` naming this repo and the count. Give the user the returned URL, not a filesystem path.

#### What fills the slots

Header: repo name, date, candidate count. **Rank the cards `Strong`, then `Worth exploring`, then `Speculative`**, and number them in that order — the rank is the reading order, not the order you found them. **Six candidates maximum**; a seventh means the cut isn't sharp enough.

Each candidate card carries:

- **Title** — short, names the deepening (e.g. "Collapse the Order intake pipeline")
- **Recommendation strength** — `Strong`, `Worth exploring`, or `Speculative`, as a badge, plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`)
- **Files** — monospaced list of the files/modules involved
- **Before / After diagram** — the centrepiece, side by side, illustrating the shallowness and the deepening
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes.
- **Wins** — bullets, ≤6 words, named in glossary terms: "locality: bugs concentrate in one module", "leverage: one interface, N call sites", "delete 4 shallow wrappers". Never "easier to maintain" or "cleaner code".

The diagrams carry the weight; prose stays sparse. If a diagram needs a paragraph to be understood, redraw the diagram. What varies between candidates is the **shape of the graph, never the styling** — the template's four node classes are the whole vocabulary:

| Class | Means | Use it for |
| --- | --- | --- |
| `:::module` | an ordinary module | anything with an interface and an implementation |
| `:::deep` | a deep module, thick border | the one module the "after" collapses into |
| `:::faded` | now internal | calls that stopped being a caller's problem, inside the "after" subgraph |
| `:::leak` | leaking across a seam | a module callers reach past its seam to touch |

A dashed link (`-.->`) is a seam; leakage is a red link, coloured with an explicit `linkStyle`. Artifacts render `<pre class="mermaid">` natively, so there is no library to load — and the `theme: neutral` frontmatter already in the template's diagrams stays, because Mermaid takes its palette from its own theme rather than the page's.

**Not diagrams you draw here:** sequence diagrams, hand-built SVG boxes, stacked layer cross-sections, interface-vs-implementation mass rectangles, anything with a measured axis. Each is a fine picture in isolation; each also turns the report into a different document than the last one.

**Use the codebase's own vocabulary for the domain, and the `codebase-design` vocabulary for the architecture.** If the domain calls it "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service." No hedging, no throat-clearing: if a sentence could be a bullet, make it a bullet.

Do NOT propose interfaces yet. After the report is published, ask the user: "Which of these would you like to explore?"

### 3. Work through the chosen candidate

Once the user picks a candidate, walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. Choose whatever approach fits the candidate and the conversation: a one-question-at-a-time interview, a written design sketch, or a direct proposal you refine together.

**Want to explore alternative interfaces for the deepened module?** Load the `codebase-design` skill and use its design-it-twice parallel sub-agent pattern.
