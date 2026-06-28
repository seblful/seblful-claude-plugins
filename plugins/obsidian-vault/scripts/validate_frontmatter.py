"""Validate note frontmatter against the conventions in CONVENTIONS.md.

Deterministic backing for vault-structural-scan and vault-daily-format. Reports
schema violations per note; it flags, it does not fix — the calling routine
applies fixes against the vault so the live index stays correct. Archive/ is
skipped (archived frontmatter is frozen).

Checks: required fields present per note type; dates ISO `YYYY-MM-DD[THH:MM:SS]`;
`tags` a lowercase kebab-case list; link-valued fields (`project`, `area`,
`related`) carry `[[wikilinks]]`.

Usage:
    python validate_frontmatter.py --vault PATH

Output (JSON to stdout): {"issues": [{"file", "type", "problem"}]}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _vault import ISO_DATE_RE, KEBAB_RE, iter_notes
from _vault import Note

REQUIRED: dict[str, set[str]] = {
    "general": {"tags", "created", "modified"},
    "daily": {"tags", "created", "modified"},
    "weekly": {"year", "week", "tags", "harvested"},
}
DATE_FIELDS = {"created", "modified", "reviewed"}
LINK_FIELDS = {"project", "area", "related"}


def check_note(note: Note) -> list[str]:
    nt = note.note_type
    if nt == "archived":
        return []
    fm = note.frontmatter
    problems: list[str] = []

    for required in REQUIRED.get(nt, REQUIRED["general"]):
        value = fm.get(required)
        if value is None or value == "" or value == []:
            problems.append(f"missing required field `{required}`")

    for field_name in DATE_FIELDS:
        value = fm.get(field_name)
        if isinstance(value, str) and not ISO_DATE_RE.match(value):
            problems.append(f"`{field_name}` is not ISO date: {value!r}")

    tags = fm.get("tags")
    if isinstance(tags, list):
        bad = [t for t in tags if isinstance(t, str) and not KEBAB_RE.match(t)]
        if bad:
            problems.append(f"tags not lowercase-kebab: {bad}")
    elif isinstance(tags, str) and tags:
        problems.append("`tags` should be a YAML list")

    for field_name in LINK_FIELDS:
        value = fm.get(field_name)
        values = value if isinstance(value, list) else [value] if value else []
        for v in values:
            if isinstance(v, str) and "[[" not in v:
                problems.append(f"`{field_name}` value not a wikilink: {v!r}")

    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root (default: cwd)")
    args = parser.parse_args()

    issues: list[dict[str, str]] = []
    for note in iter_notes(Path(args.vault), include_archive=False):
        for problem in check_note(note):
            issues.append(
                {"file": str(note.path), "type": note.note_type, "problem": problem}
            )
    print(json.dumps({"issues": issues}, indent=2))


if __name__ == "__main__":
    main()
