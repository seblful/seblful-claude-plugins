---
name: project-rules
description: >
  Update .claude/PROJECT_RULES.md when the user corrects a mistake Claude just made.
  Trigger when you receive the instruction to update project rules from the hook,
  or when the user explicitly asks to save a rule or lesson learned.
allowed-tools: Read, Glob, Edit, Write
---

When instructed to update project rules, do the following silently before responding:

## 1. Find or create the rules file

Use Glob to locate `.claude/PROJECT_RULES.md`. If it does not exist, create it
with the template below using Write.

## 2. Distil one rule from the correction

Look at your previous response and the user's correction. Extract ONE imperative
rule that prevents this mistake from recurring:

- Imperative: "Never use X", "Always Y", "Do not add Z unless…"
- Specific to the actual mistake
- One sentence

Classify as one of:
- **Product Rule** — UX, features, data behaviour
- **Development Practice** — code patterns, tooling, architecture
- **Anti-pattern** — things to never do

Write one sentence explaining why the rule exists.

## 3. Check for duplicates

Read the current file. If an equivalent rule already exists, skip writing.

## 4. Append the rule

Insert after the matching section header (before the next `---`):

```
- **[YYYY-MM-DD]** <rule>
  > <reason>
```

Update the `*Last updated:` line.

## 5. Continue normally

Do not mention that you updated the file unless the user asks.

---

## PROJECT_RULES.md template

```markdown
# Project Rules & Lessons Learned

Auto-updated from corrections. Loaded into every session via CLAUDE.md.

## Project Context

**App:** <!-- brief description -->
**Stack:** <!-- e.g. Python, FastAPI, PostgreSQL -->
**Architecture:** <!-- e.g. layered, event-driven -->

---

## Product Rules

---

## Development Practices

---

## Anti-patterns

---

*Last updated: YYYY-MM-DD*
```

## Setup note

For rules to load in future sessions, add this line to the project's `CLAUDE.md`:

```
@.claude/PROJECT_RULES.md
```

Add `.claude/.insights_state.json` to `.gitignore` — the hook writes session state there.
