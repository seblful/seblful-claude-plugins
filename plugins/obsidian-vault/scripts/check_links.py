"""Find broken wikilinks/embeds and (optionally) orphan notes across a vault.

Deterministic backing for vault-structural-scan and the authoring verify step.
A link is broken when its target note name doesn't match any note's filename.
An orphan has neither incoming nor outgoing wikilinks. Archive/ is excluded from
editing scope but still counts as a valid link target.

Usage:
    python check_links.py --vault PATH [--orphans]

Output (JSON to stdout):
    {"broken": [{"file", "link", "target", "embed"}], "orphans": ["file", ...]}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from _vault import EMBED_RE, WIKILINK_RE, iter_notes, link_target, note_index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root (default: cwd)")
    parser.add_argument("--orphans", action="store_true", help="Also report orphans")
    args = parser.parse_args()

    vault = Path(args.vault)
    index = note_index(vault, include_archive=True)
    notes = iter_notes(vault, include_archive=False)

    broken: list[dict[str, object]] = []
    linked_from: set[str] = set()  # notes that are link targets (have incoming)
    has_outgoing: set[str] = set()

    for note in notes:
        embeds = {m for m in EMBED_RE.findall(note.text)}
        for raw in WIKILINK_RE.findall(note.text):
            target = link_target(raw)
            if not target:
                continue
            is_embed = raw in embeds
            if not is_embed:
                has_outgoing.add(note.stem.lower())
            if target.lower() in index:
                linked_from.add(target.lower())
            elif not is_embed:
                # Embeds may point at images/attachments, not notes — skip those.
                broken.append(
                    {
                        "file": str(note.path),
                        "link": raw,
                        "target": target,
                        "embed": is_embed,
                    }
                )

    result: dict[str, object] = {"broken": broken}
    if args.orphans:
        orphans = [
            str(n.path)
            for n in notes
            if n.stem.lower() not in linked_from
            and n.stem.lower() not in has_outgoing
        ]
        result["orphans"] = orphans
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
