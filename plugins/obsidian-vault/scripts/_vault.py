"""Shared vault-scanning helpers for the obsidian-vault deterministic scripts.

Standard library only — these run against a user's live vault folder on any
machine with Python 3.9+, with no third-party dependencies to install.

The frontmatter parser here is intentionally tolerant: it recognizes the simple
`key: value` and YAML-list shapes these vaults use, and is meant to *flag* issues
for a human or the calling routine to resolve, not to be a full YAML engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
EMBED_RE = re.compile(r"!\[\[([^\]]+)\]\]")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2})?$")
DAILY_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WEEKLY_NAME_RE = re.compile(r"^W\d{1,2}$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.MULTILINE)
FOOTNOTE_REF_RE = re.compile(r"(?<!^)\[\^([^\]]+)\]")


@dataclass
class Note:
    """A markdown note: its path, raw text, parsed frontmatter, and body."""

    path: Path
    text: str
    frontmatter: dict[str, object] = field(default_factory=dict)
    body: str = ""

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def note_type(self) -> str:
        """Classify by path and filename: archived | daily | weekly | general."""
        parts = {p.lower() for p in self.path.parts}
        if "archive" in parts:
            return "archived"
        if DAILY_NAME_RE.match(self.stem):
            return "daily"
        if "weekly" in parts and WEEKLY_NAME_RE.match(self.stem):
            return "weekly"
        return "general"


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Split a `---`-fenced YAML frontmatter block from the body.

    Returns (frontmatter_dict, body). Values are str, list[str], or bool.
    Tolerant by design — unknown shapes are kept as raw strings.
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, text

    fm: dict[str, object] = {}
    current_key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        list_item = re.match(r"^\s*-\s+(.*)$", raw)
        if list_item and current_key is not None:
            fm.setdefault(current_key, [])
            if isinstance(fm[current_key], list):
                fm[current_key].append(list_item.group(1).strip())  # type: ignore[union-attr]
            continue
        kv = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            current_key = key
            if value == "":
                fm[key] = []  # likely a YAML list that follows on later lines
            elif value.lower() in ("true", "false"):
                fm[key] = value.lower() == "true"
            else:
                fm[key] = value.strip("\"'")
    body = "\n".join(lines[end + 1 :])
    return fm, body


def load_note(path: Path) -> Note:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm, body = parse_frontmatter(text)
    return Note(path=path, text=text, frontmatter=fm, body=body)


def iter_notes(vault: Path, *, include_archive: bool = False) -> list[Note]:
    """Load every markdown note under the vault, skipping Archive by default."""
    notes: list[Note] = []
    for md in sorted(vault.rglob("*.md")):
        parts = {p.lower() for p in md.relative_to(vault).parts}
        if not include_archive and "archive" in parts:
            continue
        notes.append(load_note(md))
    return notes


def note_index(vault: Path, *, include_archive: bool = True) -> set[str]:
    """Set of resolvable wikilink targets: note stems (case-insensitive)."""
    index: set[str] = set()
    for md in vault.rglob("*.md"):
        parts = {p.lower() for p in md.relative_to(vault).parts}
        if not include_archive and "archive" in parts:
            continue
        index.add(md.stem.lower())
    return index


def link_target(raw: str) -> str:
    """Normalize a wikilink payload to its target note name.

    `Note#Section|Display` -> `Note`; strips alias and heading anchors.
    """
    return raw.split("|", 1)[0].split("#", 1)[0].strip()
