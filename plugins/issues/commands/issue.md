---
description: Capture what just went wrong (or a follow-up you name) as a GitHub issue in the seblful/seblful-claude-plugins backlog — drafted from the conversation, dedup-checked, and shown to you before anything is filed. Optional subject as $ARGUMENTS.
allowed-tools: Bash, Read, Grep, Glob
---

Invoke the `file-issue` skill to draft and — only after I approve — file a GitHub issue in the `seblful/seblful-claude-plugins` repository (my central backlog), no matter which directory this session is running in.

If `$ARGUMENTS` is non-empty, use it as the seed for what the issue is about. Otherwise work out the subject from what just happened in this conversation: the task that failed, the error, or the blocker. Note in the issue which repo or directory the failure came from.

Never create the issue without first showing me the full draft (repo, title, labels, body) and getting my explicit yes.
