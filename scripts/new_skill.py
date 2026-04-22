#!/usr/bin/env python3
"""Scaffold a new skill directory under ``skills/``.

Usage:
    python3 scripts/new_skill.py <kebab-case-name>

Creates ``skills/<name>/SKILL.md`` with a minimal, validator-passing template
plus empty ``references/``, ``assets/``, and ``scripts/`` subdirectories. The
skill still needs a real description before release — the scaffold only
guarantees ``make validate`` passes with a placeholder warning.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from validate_repo import KEBAB_RE, ROOT  # type: ignore[import-not-found]

SKILL_TEMPLATE = """\
---
name: {name}
description: >
  TODO: Replace this placeholder with a specific, trigger-rich description for
  the {name} skill. Describe *when* an assistant should invoke it, name the
  realistic user phrasings that should activate it, and call out tasks that
  are out of scope. The description is the primary signal the model uses to
  decide whether this skill fits the current request.
---

# {title}

One-paragraph overview of what this skill does and why it exists.

## When to use

- Trigger condition 1
- Trigger condition 2

## When NOT to use

- Out-of-scope case 1

## Workflow

1. Step one
2. Step two
3. Step three

## References

<!-- Link any files under references/ that an agent should consult -->
"""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: new_skill.py <kebab-case-name>", file=sys.stderr)
        return 2
    name = argv[1].strip()
    if not KEBAB_RE.match(name):
        print(f"error: '{name}' is not kebab-case", file=sys.stderr)
        return 2

    target = ROOT / "skills" / name
    if target.exists():
        print(f"error: {target} already exists", file=sys.stderr)
        return 1

    (target / "references").mkdir(parents=True)
    (target / "assets").mkdir()
    (target / "scripts").mkdir()

    title = re.sub(r"-+", " ", name).title()
    (target / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(name=name, title=title),
        encoding="utf-8",
    )

    print(f"scaffolded {target.relative_to(ROOT)}")
    print("next steps:")
    print(f"  1. edit {target.relative_to(ROOT)}/SKILL.md (replace the placeholder description)")
    print("  2. run `make sync && make validate`")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
