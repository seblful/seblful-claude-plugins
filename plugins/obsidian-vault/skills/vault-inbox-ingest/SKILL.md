---
name: vault-inbox-ingest
description: Empty the Inbox — merge each raw capture into the right destination note (or create one), relocate its images into the destination's attachments, wire the result into the relevant MOC, then delete the consumed capture.
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# Inbox Ingest

The inbox holds raw captures dropped in without a home. File each into the place it belongs and leave the inbox empty: read it, decide where its knowledge goes, merge it there, relocate its images, wire the result into a MOC, then delete the consumed capture. Today's date: use the system date. Frontmatter, link, MOC-detection, and note-creation rules live in [CONVENTIONS.md](../../CONVENTIONS.md).

**Process only the inbox.** Don't touch folders holding work the user is actively authoring (drafts, texts) — those are owned documents, not material to dissolve. If unsure whether a folder is an inbox or a drafts area, ask.

## Steps

1. **Locate the inbox** (`Inbox/`, or this vault's clear equivalent) and list it. If empty, say so and stop.

2. **Read every capture first** — content, frontmatter, embedded images — so you can spot duplicates and group related ones.

3. **Decide each destination.** Map the vault's folders and search the topic before assuming no home exists.
   - A note already covers it → **enrich that note in place**.
   - Genuinely new concept with lasting value → **create a standalone note** in the right folder (per CONVENTIONS.md → Creating notes).
   - Duplicate → merge into the single destination; don't create twice.
   - No lasting value → discard, and report what and why.

4. **Merge cleanly.** Write the knowledge as a standalone fact — strip capture-context ("note to self", timestamps) so it reads as if it always belonged, in the capture's language. Don't duplicate what's already there. Use `[[wikilinks]]` for inline references (resolve exact filenames per CONVENTIONS.md).

5. **Relocate referenced images** into the destination's attachments folder (mirror the vault's convention). **Rename on collision** rather than overwrite; update the embed to the new path; move the binary on disk with Bash and leave nothing in the inbox.

6. **Wire into a MOC.** New notes go under the right section of the relevant MOC (detected by role — see CONVENTIONS.md → MOCs); if none fits, add at least one incoming `[[wikilink]]` so the note isn't orphaned. Enriched notes need this only if they were missing from their MOC.

7. **Delete the consumed capture** — only after its content is merged, images relocated, and it's wired in. If any destination is uncertain, leave the capture and flag it. Never delete an unplaced capture.

## Report

Per capture: destination (enriched vs. new note) and path; images relocated with any renames; MOC entries added; anything discarded or left for review (with reason); final inbox state.

## Judgment

- Enrich an existing note over creating a near-duplicate — proliferation is the failure mode to avoid.
- A capture worth keeping but too thin to stand alone belongs *inside* a broader note, not as its own stub.
- When a capture could fit several notes, place it in the primary one and cross-link the rest inline.
- Can't confidently place it? Leave it in the inbox and ask. An unfiled capture is recoverable; a wrongly-merged-then-deleted one is not.
