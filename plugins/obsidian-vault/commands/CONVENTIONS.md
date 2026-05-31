# Vault Conventions

Shared reference for every `obsidian-vault` maintenance routine. Each command states its own job; the rules that *all* of them must obey live here, once, so they cannot drift apart.

## Discovering a vault's conventions

These routines run inside a live Obsidian vault, not a code repo. Before applying any default below, learn what the vault actually does:

1. If the vault documents its own conventions (a `CLAUDE.md`, a `README`, a `System/`-style meta folder), that documentation wins over anything here.
2. Otherwise, infer conventions from existing notes — open a few representative notes and mirror their frontmatter shape, link style, and folder layout.
3. The structures described below are the **defaults** to fall back on, and the shape these routines assume when they create or reorganize content.

When a vault's real convention and a default here disagree, follow the vault and do not "correct" it toward the default.

## Frontmatter

Every note carries YAML frontmatter. Schema by note type:

| Note type | Required | Notes |
|---|---|---|
| General / concept | `tags`, `created`, `modified` | |
| Reviewed (verified for accuracy) | adds `reviewed` | date `YYYY-MM-DD` |
| Daily (`YYYY-MM-DD.md`) | `tags`, `created`, `modified` | optional `project`, `area` as list-of-links |
| Weekly (`Weekly/W{nn}.md`) | `year`, `week`, `tags`, `harvested` | `harvested` boolean; `Weekly/` sits beside the daily folder |
| Project | `tags`, `created`, `modified` | optional `aliases` |
| Archived (`Archive/.../YYYY/...`) | unchanged — frozen | never rewrite archived frontmatter |

Rules:

- Dates are ISO `YYYY-MM-DD` (or `YYYY-MM-DDTHH:mm:ss` for datetime properties). Never relative dates inside frontmatter.
- `created` is set once and never changed. `modified` bumps whenever content changes. `reviewed` bumps only when a human or an accuracy routine has verified the note's claims.
- Date fields must match the file's real ctime/mtime; correct them when they don't.
- `tags` is a YAML list; tag names lowercase and kebab-case (`deep-work`, not `DeepWork`).
- Link-valued properties (`project`, `area`, `related`, …) are wikilinks, not plain text — single-string form for one value (`related: "[[Note]]"`), YAML list form for multiple.
- Preserve Obsidian's reserved keys (`aliases`, `cssclasses`, `tags`) if present; `aliases` and `cssclasses` are YAML lists. Never strip them.

## Links

- Internal references are `[[wikilinks]]`, never `[markdown](links)`. Use `[[Note|display text]]` for custom text and `[[Note#Section]]` to point at a heading.
- **Resolve the exact filename before linking — never guess or approximate.** A wikilink to a note that doesn't exist yet is fine *only* when deliberately marking a planned note; an accidental misspelling is a broken link.
- Bare external URLs become titled markdown links: `[Title](https://…)`.
- Link inline, in prose, where a concept is naturally mentioned — not in a "See Also" dump. A short `See also:` footer is acceptable only on index/leaf notes.

## Headings

- No level-1 heading (`#`) in a note body — the filename is the title and Obsidian renders it as the page heading. Top-level sections start at `##`.
- Demote any stray `#` to `##`, or drop it if it merely repeats the filename.
- Don't skip levels (`##` → `####`); promote the deeper heading.

## MOCs and index notes

A MOC (Map of Content) is any note that functions as a domain or folder index. Detect one by **role**, not just filename: a note is a MOC if it lists/links the notes of a domain. Common naming patterns — a name ending in ` MOC` (`Programming MOC.md`), or named `MOC.md` / `Index.md`, or carrying a `moc` tag — but treat the role as decisive.

Mechanical upkeep of MOCs (fixing broken entries, adding obviously-missing notes) belongs to `vault-structural-scan`. Deciding what a MOC *should* cover or redesigning its sections is editorial work — flag it, don't do it unprompted.

## Folder roles and the archive model

- The **daily folder** holds `YYYY-MM-DD.md` notes (Obsidian Daily Notes default). It may be the vault root or a configured folder.
- **`Weekly/`** is a flat folder of `W{nn}.md` reports, a sibling of the daily folder. Being flat, it holds one year at a time without filename collisions.
- **`Archive/`** is a sibling of the daily and weekly folders. Archive paths **mirror** live paths and partition by year: a daily note archives to `Archive/Daily/{YYYY}/`, a weekly note to `Archive/Weekly/{YYYY}/`, using the year the note belongs to.
- **Year sweep (self-healing).** Whenever a routine touches `Weekly/`, archive any report whose `year` is earlier than the current year. Because the sweep runs on every touch, a missed year boundary is cleaned up on the next invocation.
- Archived content is **frozen**: move it as-is, don't rewrite links or frontmatter inside it.
- An attachment is any non-markdown file a note depends on — embedded via `![[file]]` / `![](path)`, or living in a sibling folder named after the note. When archiving, move attachments into an `attachments/` subfolder of the same mirrored archive path.

## Language and substance

- **Never change the language of a note.** If content is written in another language (e.g. Russian work logs), keep it that language — never translate or rewrite it in English. When synthesizing one note from others, write the synthesis in the source notes' language.
- **Preserve meaning.** Format, clarify, link, and tidy — never silently change what the user wrote. This is load-bearing in work logs and daily reports.
- Don't reorder items the user wrote; their ordering is intentional.

## Creating notes

When a routine creates a note:

- Follow the schema above, and any matching template the vault keeps (e.g. a `System/Templates/` folder) for that note type.
- Connect it: place it under the right section of the relevant MOC, or add at least one incoming `[[wikilink]]` from a related note so it isn't orphaned.
- No decorative dividers, auto-generated TOCs, "Last updated by …" footers, or emojis (unless the user already uses them).
- One concept per file. Don't create a near-duplicate of an existing note — enrich the existing one instead.
