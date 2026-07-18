---
name: file-issue
description: Capture a bug in one of the plugins in seblful/seblful-claude-plugins (a skill, command, agent, or hook) as a GitHub issue in that repo's backlog. Use when the user says /issue or asks to "file/open/log an issue", "track this", "add a bug", and proactively when one of those plugins triggers wrongly, does the wrong thing, or fails — even while working in an unrelated project. Drafts and confirms before filing; never files silently.
---

# File Issue

Capture a failure, bug, or follow-up as a GitHub issue in the **`seblful/seblful-claude-plugins`** repository — the backlog for problems with the plugins in that repo — no matter which directory the session is running in, so a plugin bug is remembered instead of lost when the session ends.

**Core rule — draft, then confirm.** Filing an issue is outward-facing. Always show the full draft and get an explicit "yes" before running `gh issue create`, including when you are offering proactively after a failure. Never file silently.

## When to use

This backlog tracks problems with **the plugins in `seblful/seblful-claude-plugins`** — a skill, command, agent, or hook that triggers when it should not, does the wrong thing, produces a bad result, or fails outright. That is the scope of the proactive offer.

- **Proactively**, when one of those plugins misbehaves during a session — even while you are working in a completely unrelated project: offer it, e.g. *"That looks like a bug in your `<plugin>` plugin — want me to file it?"*, then draft on agreement. Do not let a real plugin failure evaporate just because the user did not think to ask.
- **On request**, when the user types `/issue` or asks to "file/open/log an issue", "track this", "add a bug" — here capture whatever they point at, still into this backlog.

## Prerequisites

`gh` must be installed and authenticated — verify with `gh auth status`. If it is not, tell the user and stop. Do not attempt to file through the web UI or any other channel.

## Steps

### 1. Target repo — always the same
The issue always goes to **`seblful/seblful-claude-plugins`**, regardless of the current directory. Pass `--repo seblful/seblful-claude-plugins` to **every** `gh` command below (`issue list`, `label list`, `issue create`, `issue comment`) so the working directory never changes where it lands. Sanity-check access once with `gh repo view seblful/seblful-claude-plugins`.

### 2. Gather the substance
Build the issue from what you actually observed:
- If `$ARGUMENTS` or the user's request names the subject, start from that.
- Otherwise reconstruct from the recent conversation: what was attempted, the exact error, the command or `path:line` involved, and expected vs. actual behavior.
- **Do not invent** repro steps, stack traces, or version numbers you did not see. If something is unknown, omit it or mark it "unknown". A thin accurate issue beats a padded speculative one.

### 3. Check for duplicates
Before drafting a new issue, search existing ones: `gh issue list --repo seblful/seblful-claude-plugins --search "<key terms>" --state all --limit 10`. If a clear match already exists, offer to add a comment to it (`gh issue comment <n> --repo seblful/seblful-claude-plugins --body-file <file>`) instead of opening a duplicate.

### 4. Pick labels (existing ones only)
List them with `gh label list --repo seblful/seblful-claude-plugins`. Choose 0–2 that genuinely fit (e.g. `bug`, `enhancement`). **Never pass a label that is not in the list** — `gh issue create --label` errors on unknown labels. If none fit, use no label.

### 5. Draft
Title: one concise line naming what is wrong — not "error occurred".
Body (Markdown), including only the sections you can actually fill:

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
<the repo or directory the session was working in when the failure occurred, e.g. `owner/name` or the path — since this backlog collects issues from every project>

## References
- `path:line`
- <commands, links>

---
Filed from a Claude Code session.
```

### 6. Confirm
Show the user the target repo, title, labels, and full body. Wait for an explicit yes. If they want changes, revise and re-show.

### 7. Create
Write the body to a temp file first (avoids shell-quoting problems, especially in PowerShell), then:

```
gh issue create --repo seblful/seblful-claude-plugins --title "<title>" --label <label> --body-file <tmpfile>
```

Print the returned issue URL. If the user chose to comment on an existing issue instead, use `gh issue comment <n> --repo seblful/seblful-claude-plugins --body-file <tmpfile>`.
