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

- Run the `/codebase-design` skill for the architecture vocabulary (**module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**) and its principles (the deletion test, "the interface is the test surface", "one adapter = hypothetical seam, two = real"). Use these terms exactly in every suggestion — don't drift into "component," "service," "API," or "boundary."
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

Publish the review as a **Claude Artifact** so the user gets a clickable, shareable URL and nothing lands in the repo. Load the `artifact-design` skill first — the Artifact contract requires it, and it owns how the page looks. Everything below is about what the report *says*. Write the report to the session scratchpad as `refactor-interfaces-audit.html`, then call `Artifact` with that path, a `title`, a one-sentence `description`, and a `favicon`. Give the user the returned URL, not a filesystem path. Re-reviewing the same repo republishes from the same filename, which redeploys to the same URL.

The report is a header, one card per candidate, and a closing **Top recommendation** — which candidate you'd tackle first, one sentence on why, linked to its card. The header is repo name, date, and a compact legend (solid box = module, dashed line = seam, red arrow = leakage, thick inverted box = deep module). No introduction paragraph — straight into the candidates.

Each candidate card carries:

- **Title** — short, names the deepening (e.g. "Collapse the Order intake pipeline")
- **Recommendation strength** — `Strong`, `Worth exploring`, or `Speculative`, as a badge, plus a tag for the dependency category (`in-process`, `local-substitutable`, `ports & adapters`, `mock`)
- **Files** — monospaced list of the files/modules involved
- **Before / After diagram** — the centrepiece, side by side, illustrating the shallowness and the deepening
- **Problem** — one sentence. What hurts.
- **Solution** — one sentence. What changes.
- **Wins** — bullets, ≤6 words, named in glossary terms: "locality: bugs concentrate in one module", "leverage: one interface, N call sites", "delete 4 shallow wrappers". Never "easier to maintain" or "cleaner code".

The diagrams carry the weight; prose stays sparse. If a diagram needs a paragraph to be understood, redraw the diagram. Be visual, and vary the pattern — don't let every candidate look the same:

- **Mermaid flowchart or sequence** — the workhorse for "X calls Y calls Z, and look at the mess" and "before: 6 round-trips; after: 1". Artifacts render `<pre class="mermaid">` natively, so there's no library to load — but Mermaid's palette comes from its own theme rather than the page's, so pin `theme: neutral` in the diagram's config frontmatter and colour leakage explicitly with `classDef`.
- **Hand-built boxes and arrows** — bordered divs, arrows as inline SVG. Reach for this when the "after" should feel like one thick-bordered deep module with greyed-out internals, and whenever the visual has to read exactly right in both light and dark.
- **Cross-section** — stacked horizontal bands for the layers a call passes through. Before: 6 thin layers each doing nothing. After: 1 thick band.
- **Mass diagram** — interface rectangle against implementation rectangle. Shallow: near-equal. Deep: short interface, tall implementation.
- **Call-graph collapse** — a tree of nested call boxes, collapsed in the "after" into one box with the now-internal calls faded inside.

**Use the codebase's own vocabulary for the domain, and the `/codebase-design` vocabulary for the architecture.** If the domain calls it "Order," talk about "the Order intake module" — not "the FooBarHandler," and not "the Order service." No hedging, no throat-clearing: if a sentence could be a bullet, make it a bullet.

Do NOT propose interfaces yet. After the report is published, ask the user: "Which of these would you like to explore?"

### 3. Work through the chosen candidate

Once the user picks a candidate, walk the design tree with them — constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. Choose whatever approach fits the candidate and the conversation: a one-question-at-a-time interview, a written design sketch, or a direct proposal you refine together.

**Want to explore alternative interfaces for the deepened module?** Run the `/codebase-design` skill and use its design-it-twice parallel sub-agent pattern.
