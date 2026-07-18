---
name: issue
description: Capture a bug, feature, enhancement, task, or idea as a GitHub issue in the backlog repo set by the CLAUDE_ISSUES_REPO env var (no default — stops if it is unset). Use when the user says /issue or asks to "file/open/log an issue", "track this", "add a bug/feature", "capture this idea" — and proactively when one of the user's plugins or systems misbehaves and the failure would otherwise be lost. Drafts and confirms before filing; never files silently.
---

# File Issue

Capture a **bug, feature request, enhancement, task, or idea** as a GitHub issue in a **backlog repo you configure**, so it is remembered instead of lost when the session ends. Nothing here is tied to a specific project — point it at any repo and reuse it for any current or future system or skill.

**Core rule — draft, then confirm.** Filing or commenting is outward-facing. Always show the full draft and get an explicit "yes" before running `gh issue create`, including when you offer proactively. Never file silently.

## Prerequisites

`gh` must be installed and authenticated — verify with `gh auth status`. If not, tell the user and stop. Do not attempt to file through the web UI or any other channel.

## Where issues go — the backlog repo

The destination is the `CLAUDE_ISSUES_REPO` environment variable (set under `env` in `~/.claude/settings.json`, or a project's `.claude/settings.json`). **There is no default** — if it is unset or empty, stop and ask the user to set `CLAUDE_ISSUES_REPO` to an `owner/name`. Never fall back to any repo.

Resolve it **once** at the start and reuse that literal `owner/name` in every `gh` command (each Bash call is a fresh shell, so do not rely on a variable persisting):

```
gh repo view "$CLAUDE_ISSUES_REPO" --json nameWithOwner -q .nameWithOwner
```

If `$CLAUDE_ISSUES_REPO` is empty this errors — treat that as "not configured" and stop. Otherwise pass `--repo <that value>` to **every** `gh` command below, so the working directory never decides where the issue lands. If the repo is inaccessible, say so and stop.

## When to use

- **On request** — the user types `/issue` or asks to "file/open/log an issue", "track this", "add a bug", "file a feature request", "capture this idea". Capture whatever they point at.
- **Proactively** — when one of the user's plugins or systems misbehaves during a session (a skill, command, agent, or hook triggering when it should not, doing the wrong thing, or failing), even while working in an unrelated project. Offer it, e.g. *"Want me to file that as an issue?"*, then draft on agreement. Do not let a real failure evaporate just because the user did not think to ask.

## Steps

### 1. Resolve the backlog repo
Get `owner/name` from `CLAUDE_ISSUES_REPO` with the command above. If it is unset or empty, stop and ask the user to set it — there is no default. Otherwise confirm access.

### 2. Classify the item
Decide the type from context, asking only if genuinely unclear: **bug**, **feature**, **enhancement**, **task**, or **idea**. The type shapes the body template (step 6) and the label (step 5).

### 3. Gather the substance
Build it from what you actually observed or what the user described:
- **bug / failure** — what was attempted, the exact error, the command or `path:line`, expected vs. actual behavior.
- **feature / enhancement / idea** — the motivation (the problem it solves), the proposed behavior, and any alternatives considered.
- **task** — the concrete outcome wanted and any acceptance criteria.

**Do not invent** repro steps, stack traces, versions, or requirements you did not see. If something is unknown, omit it or mark it "unknown". A thin accurate issue beats a padded speculative one.

### 4. Check for duplicates
`gh issue list --repo <owner/name> --search "<key terms>" --state all --limit 10`. If a clear match exists, offer to comment on it (`gh issue comment <n> --repo <owner/name> --body-file <file>`) instead of opening a duplicate.

### 5. Pick labels (existing ones only)
`gh label list --repo <owner/name>`. Choose 0–2 that fit the type (e.g. `bug`, `enhancement`). **Never pass a label that is not in the list** — `gh issue create --label` errors on unknown labels. If none fit, use no label. If a new label is clearly warranted, ask before `gh label create`.

### 6. Draft
Title: one concise line naming the problem or change — not "error occurred". Include only sections you can actually fill.

**Bug / failure**
```
## Summary
<one or two sentences>

## Steps to reproduce
1. …

## Expected
…

## Actual
…

## Environment
<OS, tool / versions — only if known>

## Where it happened
<repo or directory the session was in, e.g. `owner/name` or the path — include when the backlog collects from multiple projects>

## References
- `path:line`
- <commands, links>
```

**Feature / enhancement / idea / task**
```
## Summary
<one or two sentences>

## Motivation
<the problem this solves>

## Proposed behavior
<what it should do>

## Alternatives considered
<optional>

## References
- <links, `path:line`>
```

End every body with:
```

---
Filed from a Claude Code session.
```

### 7. Confirm
Show the user the target repo, item type, title, labels, and full body. Wait for an explicit yes. Revise and re-show if they want changes.

### 8. Create
Write the body to a temp file first (avoids shell-quoting problems, especially in PowerShell), then:

```
gh issue create --repo <owner/name> --title "<title>" --label <label> --body-file <tmpfile>
```

Print the returned issue URL. If the user chose to comment on an existing issue instead, use `gh issue comment <n> --repo <owner/name> --body-file <tmpfile>`.
