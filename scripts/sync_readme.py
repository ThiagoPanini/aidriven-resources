#!/usr/bin/env python3
"""Regenerate derived sections of ``README.md`` from ``SKILL.md`` frontmatter.

The README currently derives two blocks from the catalog:

* the **Skill catalog** table (skill name + short description)
* the ``skills/`` subtree inside the **Repository layout** code block

Both blocks are delimited by HTML-comment markers so the surrounding prose
stays human-owned. ``--check`` mirrors ``sync_manifest.py --check`` — fails
with exit 1 when the README is out of date, without writing.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_manifest import load_skill_entries  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parent.parent
README_PATH = ROOT / "README.md"

CATALOG_START = "<!-- skills:catalog:start -->"
CATALOG_END = "<!-- skills:catalog:end -->"
TREE_START = "<!-- skills:tree:start -->"
TREE_END = "<!-- skills:tree:end -->"


def render_catalog_table(entries: list[dict]) -> str:
    header = ["| Skill | Use it for |", "|---|---|"]
    rows = [
        f"| [`{e['name']}`]({e['path_in_repo']}/) | {e['description']} |"
        for e in entries
    ]
    return "\n".join(header + rows)


def render_tree_block(entries: list[dict]) -> str:
    names = [e["name"] for e in entries]
    lines = []
    for i, name in enumerate(names):
        connector = "└──" if i == len(names) - 1 else "├──"
        lines.append(f"│   {connector} {name}/")
    return "\n".join(lines)


def replace_block(text: str, start: str, end: str, body: str) -> str:
    pattern = re.compile(
        rf"({re.escape(start)})(.*?)({re.escape(end)})",
        re.DOTALL,
    )
    if not pattern.search(text):
        raise SystemExit(
            f"error: markers '{start}' / '{end}' not found in README.md"
        )
    return pattern.sub(f"\\1\n{body}\n\\3", text)


def build_readme(current: str) -> str:
    entries = load_skill_entries()
    new = replace_block(current, CATALOG_START, CATALOG_END, render_catalog_table(entries))
    new = replace_block(new, TREE_START, TREE_END, render_tree_block(entries))
    return new


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync README.md derived sections.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail (exit 1) if the README is out of date instead of rewriting it",
    )
    args = parser.parse_args(argv)

    current = README_PATH.read_text(encoding="utf-8")
    new = build_readme(current)

    if current == new:
        print("README.md derived sections already in sync.")
        return 0

    if args.check:
        print("::error::README.md derived sections are out of sync. Run `make sync`.")
        return 1

    README_PATH.write_text(new, encoding="utf-8")
    print("README.md derived sections rewritten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
