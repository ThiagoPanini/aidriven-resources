#!/usr/bin/env python3
"""Regenerate ``manifest.json`` from ``skills/*/SKILL.md`` frontmatter.

``manifest.json`` is a *derived* catalog in this repository. Skills declare
their identity in their own ``SKILL.md`` frontmatter — the manifest exists to
give release automation and catalog consumers a single machine-readable index.

Running this script refreshes every skill entry from disk while preserving
two fields that only a human should own:

* the top-level ``version`` (release cadence decision)
* each entry's ``added_in`` (history of when a skill first shipped)

New skills that have never appeared in the manifest inherit ``added_in`` from
the current top-level ``version`` so the field is always populated.

Exit codes:
    0 — manifest is already in sync (no write needed)
    1 — manifest was out of sync and has been rewritten
    2 — invalid input (e.g. missing SKILL.md frontmatter)

Use ``--check`` to fail (exit 1) without writing — useful in CI to detect
manifest drift without auto-fixing it.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_repo import (  # type: ignore[import-not-found]  # local sibling module
    MANIFEST_PATH,
    ROOT,
    iter_skill_dirs,
    parse_frontmatter,
)


def _first_sentence(text: str) -> str:
    """Return the first sentence of a description, trimmed for the catalog."""
    text = " ".join(text.split()).strip()
    for terminator in (". ", "? ", "! "):
        idx = text.find(terminator)
        if idx != -1:
            return text[: idx + 1].strip()
    return text


def load_skill_entries() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for skill_dir in iter_skill_dirs():
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        parsed = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if parsed is None:
            raise SystemExit(
                f"error: {skill_md.relative_to(ROOT)} has no YAML frontmatter"
            )
        frontmatter, _ = parsed
        name = frontmatter.get("name", "").strip()
        description = frontmatter.get("description", "").strip()
        if not name or not description:
            raise SystemExit(
                f"error: {skill_md.relative_to(ROOT)} frontmatter missing name/description"
            )
        entries.append(
            {
                "name": name,
                "description": _first_sentence(description),
                "path_in_repo": str(skill_dir.relative_to(ROOT)).replace("\\", "/"),
                "entry": "SKILL.md",
            }
        )
    entries.sort(key=lambda e: e["name"])
    return entries


def build_manifest() -> dict:
    existing: dict = {}
    if MANIFEST_PATH.is_file():
        existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    version = existing.get("version", "0.1.0")
    existing_added_in = {
        e.get("name"): e.get("added_in")
        for e in existing.get("skills", [])
        if isinstance(e, dict)
    }

    skills = load_skill_entries()
    for entry in skills:
        entry["added_in"] = existing_added_in.get(entry["name"]) or version

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "name": existing.get("name", "aidriven-resources"),
        "description": existing.get(
            "description",
            "Reusable skills, templates, and references for AI-assisted development workflows.",
        ),
        "version": version,
        "schema_version": existing.get("schema_version", 1),
        "updated_at": _dt.date.today().isoformat(),
        "skills": skills,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync manifest.json from SKILL.md frontmatter.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail (exit 1) if the manifest is out of date instead of rewriting it",
    )
    args = parser.parse_args(argv)

    rebuilt = build_manifest()
    new_text = json.dumps(rebuilt, indent=2, ensure_ascii=False) + "\n"

    current_text = MANIFEST_PATH.read_text(encoding="utf-8") if MANIFEST_PATH.is_file() else ""

    current_compare = current_text
    new_compare = new_text
    if current_text:
        try:
            current_data = json.loads(current_text)
            new_data = json.loads(new_text)
            current_data.pop("updated_at", None)
            new_data.pop("updated_at", None)
            current_compare = json.dumps(current_data, sort_keys=True)
            new_compare = json.dumps(new_data, sort_keys=True)
        except json.JSONDecodeError:
            pass

    if current_compare == new_compare:
        print("manifest.json is already in sync.")
        return 0

    if args.check:
        print("::error::manifest.json is out of sync. Run `make sync`.")
        return 1

    MANIFEST_PATH.write_text(new_text, encoding="utf-8")
    print(f"manifest.json rewritten ({len(rebuilt['skills'])} skill(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
