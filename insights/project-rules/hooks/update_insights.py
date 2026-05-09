#!/usr/bin/env python3
"""
Stop-hook: detects user corrections in Claude Code transcripts and outputs
an instruction for Claude to update .claude/PROJECT_RULES.md.

No API key required — Claude Code handles rule extraction.
Copy to .claude/update_insights.py and register as a Stop hook.
"""
import json
import os
import re
import sys
from pathlib import Path

BASE_DIR   = Path(__file__).parent
STATE_FILE = BASE_DIR / ".insights_state.json"

SECTION_ANCHORS = {
    "product":      "## Product Rules",
    "dev_practice": "## Development Practices",
    "anti_pattern": "## Anti-patterns",
}

CORRECTION_SIGNALS = [
    # Russian
    r"\bне\s+делай\b", r"\bне\s+надо\b", r"\bнет[,!\.]\s",
    r"\bнеправильно\b", r"\bне\s+пиши\b", r"\bне\s+добавляй\b",
    r"\bне\s+используй\b", r"\bне\s+нужно\b", r"\bне\s+так\b",
    r"\bне\s+то\b", r"\bвместо\s+этого\b", r"\bнаоборот\b",
    r"\bзачем\s+ты\b", r"\bты\s+неправильно\b", r"\bлучше\s+бы\b",
    r"\bубери\b", r"\bотмени\b", r"\bверни\b",
    # English
    r"\bno[,!]\s", r"\bdon'?t\b", r"\bstop\b", r"\bwrong\b",
    r"\bincorrect\b", r"\binstead\b", r"\bnever\b", r"\bavoid\b",
    r"\bremove that\b", r"\bundo\b", r"\brevert\b",
    r"\bthat'?s not\b", r"\byou shouldn'?t\b", r"\bplease don'?t\b",
]


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"sessions": {}}


def save_state(state: dict):
    try:
        STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except Exception:
        pass


def parse_transcript(path: str) -> list:
    messages = []
    try:
        with open(path, encoding="utf-8") as f:
            for idx, raw_line in enumerate(f):
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    msg   = entry.get("message", entry)
                    role  = msg.get("role") or entry.get("type", "")
                    if role not in ("user", "assistant"):
                        continue
                    content = msg.get("content", "")
                    if isinstance(content, list):
                        text = " ".join(
                            b.get("text", "")
                            for b in content
                            if isinstance(b, dict) and b.get("type") == "text"
                        )
                    else:
                        text = str(content)
                    text = text.strip()
                    if text:
                        messages.append({"idx": idx, "role": role, "content": text})
                except (json.JSONDecodeError, AttributeError):
                    pass
    except Exception:
        pass
    return messages


def has_correction_signal(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in CORRECTION_SIGNALS)


def format_window(window: list) -> str:
    return "\n\n".join(
        f"[{m['role'].upper()}]: {m['content'][:700]}" for m in window
    )


def main():
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return

        hook_input      = json.loads(raw)
        session_id      = hook_input.get("session_id", "")
        transcript_path = hook_input.get("transcript_path", "")

        if not transcript_path or not os.path.exists(transcript_path):
            return

        messages = parse_transcript(transcript_path)
        if len(messages) < 2:
            return

        state        = load_state()
        sessions     = state.setdefault("sessions", {})
        last_idx     = sessions.get(session_id, -1)
        new_last_idx = last_idx
        found        = []

        for i, msg in enumerate(messages):
            new_last_idx = max(new_last_idx, msg["idx"])
            if msg["idx"] <= last_idx:
                continue
            if msg["role"] != "user":
                continue
            if not has_correction_signal(msg["content"]):
                continue

            window = []
            if i > 0:
                window.append(messages[i - 1])
            window.append(msg)
            if i + 1 < len(messages):
                window.append(messages[i + 1])

            found.append(window)

        sessions[session_id] = new_last_idx
        if len(sessions) > 100:
            for old_key in sorted(sessions.keys())[:-100]:
                del sessions[old_key]
        save_state(state)

        for window in found:
            print(
                f"[insights] Correction detected — update .claude/PROJECT_RULES.md:\n\n"
                f"{format_window(window)}\n\n"
                f"Append one imperative rule to the correct section "
                f"({' / '.join(SECTION_ANCHORS.values())}) with today's date."
            )

    except Exception:
        pass


if __name__ == "__main__":
    main()
