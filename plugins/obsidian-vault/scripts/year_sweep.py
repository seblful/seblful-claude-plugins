"""Plan (or apply) the self-healing year sweep on the Weekly/ folder.

Any weekly report whose `year` is earlier than the current year is moved to
`Archive/Weekly/{year}/`, mirroring the live path. Reports a plan by default;
pass --apply to perform the moves. Archived content is frozen — this only moves
files, it never edits their contents.

Usage:
    python year_sweep.py --vault PATH [--folder Weekly] [--apply]

Output (JSON to stdout): list of {from, to, year} moves planned or applied.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import date
from pathlib import Path

from _vault import load_note


def plan_sweep(vault: Path, folder: str, current_year: int) -> list[dict[str, object]]:
    weekly_dir = vault / folder
    if not weekly_dir.is_dir():
        return []
    moves: list[dict[str, object]] = []
    for md in sorted(weekly_dir.glob("*.md")):
        note = load_note(md)
        raw_year = note.frontmatter.get("year")
        try:
            year = int(str(raw_year))
        except (TypeError, ValueError):
            continue
        if year < current_year:
            dest = vault / "Archive" / folder / str(year) / md.name
            moves.append({"from": str(md), "to": str(dest), "year": year})
    return moves


def apply_moves(moves: list[dict[str, object]]) -> None:
    for move in moves:
        dest = Path(str(move["to"]))
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(move["from"], dest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root (default: cwd)")
    parser.add_argument("--folder", default="Weekly", help="Weekly folder name")
    parser.add_argument("--apply", action="store_true", help="Perform the moves")
    args = parser.parse_args()

    moves = plan_sweep(Path(args.vault), args.folder, date.today().year)
    if args.apply:
        apply_moves(moves)
    print(json.dumps({"applied": args.apply, "moves": moves}, indent=2))


if __name__ == "__main__":
    main()
