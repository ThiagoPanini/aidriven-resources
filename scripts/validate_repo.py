#!/usr/bin/env python3
"""Repository-wide validator for aidriven-resources.

Single source of truth: each ``skills/<name>/SKILL.md`` frontmatter.
``manifest.json`` is a *derived* catalog. This validator enforces:

* every skill directory has a ``SKILL.md`` entry point
* every ``SKILL.md`` starts with YAML frontmatter and declares required fields
* the ``name`` field matches the containing directory
* skill directory names are kebab-case
* descriptions are substantive (length guard against placeholder text)
* no duplicate skill names
* ``manifest.json`` parses, has a valid version, and is in sync with ``skills/``
* relative links in ``SKILL.md`` resolve to files that actually exist
* shell scripts have the executable bit set

Emits GitHub Actions ``::error::`` annotations when run in CI so failures
surface on the PR diff, and a human-readable report otherwise.

Exit code is non-zero when any check fails. Safe to run locally:

    python3 scripts/validate_repo.py
    python3 scripts/validate_repo.py --format=github   # force CI style
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MANIFEST_PATH = ROOT / "manifest.json"

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MIN_DESCRIPTION_LEN = 40
MAX_DESCRIPTION_LEN = 4096
REQUIRED_FRONTMATTER_FIELDS = ("name", "description")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, msg: str, file: str | None = None) -> None:
        self.errors.append(_format(msg, file))

    def warn(self, msg: str, file: str | None = None) -> None:
        self.warnings.append(_format(msg, file))

    @property
    def ok(self) -> bool:
        return not self.errors


def _format(msg: str, file: str | None) -> str:
    return f"{file}: {msg}" if file else msg


def parse_frontmatter(text: str) -> tuple[dict[str, str], int] | None:
    """Parse a minimal YAML frontmatter block.

    Supports simple ``key: value`` pairs and the ``key: >`` folded block scalar
    (enough for the ``description`` field as used in this repo). Returns the
    parsed mapping and the line index where the body begins, or ``None`` if
    the document has no frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: dict[str, str] = {}
    i = 1
    current_key: str | None = None
    folded_buf: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            if current_key is not None:
                data[current_key] = " ".join(folded_buf).strip()
            return data, i + 1
        if current_key is not None:
            if line.startswith((" ", "\t")):
                folded_buf.append(line.strip())
                i += 1
                continue
            data[current_key] = " ".join(folded_buf).strip()
            current_key = None
            folded_buf = []
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value in (">", "|"):
                current_key = key
                folded_buf = []
            else:
                if value.startswith('"') and value.endswith('"') and len(value) >= 2:
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'") and len(value) >= 2:
                    value = value[1:-1]
                data[key] = value
        i += 1
    return None  # never found closing ---


def iter_skill_dirs() -> Iterable[Path]:
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())


def validate_skill(skill_dir: Path, report: Report, seen_names: dict[str, Path]) -> dict[str, str] | None:
    name_from_dir = skill_dir.name
    rel = skill_dir.relative_to(ROOT)

    if not KEBAB_RE.match(name_from_dir):
        report.error(
            f"skill directory '{name_from_dir}' is not kebab-case",
            file=str(rel),
        )

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        report.error("missing SKILL.md entry point", file=str(rel))
        return None

    text = skill_md.read_text(encoding="utf-8")
    parsed = parse_frontmatter(text)
    if parsed is None:
        report.error(
            "SKILL.md has no YAML frontmatter (must start with '---' and close with '---')",
            file=str(skill_md.relative_to(ROOT)),
        )
        return None
    frontmatter, _ = parsed

    for field_name in REQUIRED_FRONTMATTER_FIELDS:
        if field_name not in frontmatter or not frontmatter[field_name].strip():
            report.error(
                f"SKILL.md frontmatter is missing required field '{field_name}'",
                file=str(skill_md.relative_to(ROOT)),
            )

    name = frontmatter.get("name", "").strip()
    if name and name != name_from_dir:
        report.error(
            f"SKILL.md 'name: {name}' does not match directory '{name_from_dir}'",
            file=str(skill_md.relative_to(ROOT)),
        )

    if name:
        previous = seen_names.get(name)
        if previous is not None:
            report.error(
                f"duplicate skill name '{name}' (also declared by {previous.relative_to(ROOT)})",
                file=str(skill_md.relative_to(ROOT)),
            )
        else:
            seen_names[name] = skill_md

    description = frontmatter.get("description", "").strip()
    if description:
        if len(description) < MIN_DESCRIPTION_LEN:
            report.warn(
                f"description is very short ({len(description)} chars) — weak trigger signal",
                file=str(skill_md.relative_to(ROOT)),
            )
        if len(description) > MAX_DESCRIPTION_LEN:
            report.error(
                f"description is too long ({len(description)} chars > {MAX_DESCRIPTION_LEN})",
                file=str(skill_md.relative_to(ROOT)),
            )

    _check_relative_links(skill_md, text, report)
    _check_script_executable(skill_dir, report)

    return frontmatter


def _check_relative_links(skill_md: Path, text: str, report: Report) -> None:
    for match in LINK_RE.finditer(text):
        target = match.group(2).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        resolved = (skill_md.parent / target_path).resolve()
        if not resolved.exists():
            report.error(
                f"broken relative link -> '{target_path}'",
                file=str(skill_md.relative_to(ROOT)),
            )


def _check_script_executable(skill_dir: Path, report: Report) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    for script in scripts_dir.iterdir():
        if script.suffix != ".sh":
            continue
        if not os.access(script, os.X_OK):
            report.warn(
                f"shell script is not executable (chmod +x recommended)",
                file=str(script.relative_to(ROOT)),
            )


def validate_manifest(skill_frontmatter: dict[str, dict[str, str]], report: Report) -> None:
    if not MANIFEST_PATH.is_file():
        report.error("manifest.json is missing", file="manifest.json")
        return
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(f"manifest.json is not valid JSON: {exc}", file="manifest.json")
        return

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_RE.match(version):
        report.error(
            f"manifest.json 'version' must be semver (got {version!r})",
            file="manifest.json",
        )

    manifest_skills = manifest.get("skills")
    if not isinstance(manifest_skills, list):
        report.error("manifest.json 'skills' must be a list", file="manifest.json")
        return

    manifest_by_name: dict[str, dict] = {}
    for entry in manifest_skills:
        if not isinstance(entry, dict):
            report.error("manifest.json skill entries must be objects", file="manifest.json")
            continue
        name = entry.get("name")
        if not isinstance(name, str):
            report.error("manifest.json skill entry missing 'name'", file="manifest.json")
            continue
        if name in manifest_by_name:
            report.error(f"duplicate manifest entry for '{name}'", file="manifest.json")
            continue
        manifest_by_name[name] = entry

        path_in_repo = entry.get("path_in_repo", "")
        entry_file = entry.get("entry", "")
        if not path_in_repo or not (ROOT / path_in_repo).is_dir():
            report.error(
                f"manifest entry '{name}' references missing directory '{path_in_repo}'",
                file="manifest.json",
            )
        elif entry_file and not (ROOT / path_in_repo / entry_file).is_file():
            report.error(
                f"manifest entry '{name}' references missing entry file '{entry_file}'",
                file="manifest.json",
            )

    disk_names = set(skill_frontmatter)
    manifest_names = set(manifest_by_name)

    for missing in sorted(disk_names - manifest_names):
        report.error(
            f"skill '{missing}' exists under skills/ but is not listed in manifest.json "
            f"(run `make sync` to regenerate)",
            file="manifest.json",
        )
    for orphan in sorted(manifest_names - disk_names):
        report.error(
            f"manifest.json lists '{orphan}' but no such directory exists under skills/ "
            f"(run `make sync` to regenerate)",
            file="manifest.json",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the aidriven-resources repository.")
    parser.add_argument(
        "--format",
        choices=("auto", "github", "plain"),
        default="auto",
        help="output format; 'auto' detects GitHub Actions via GITHUB_ACTIONS env",
    )
    args = parser.parse_args(argv)

    if args.format == "auto":
        use_gha = os.environ.get("GITHUB_ACTIONS") == "true"
    else:
        use_gha = args.format == "github"

    report = Report()
    seen_names: dict[str, Path] = {}
    skill_frontmatter: dict[str, dict[str, str]] = {}

    skill_dirs = list(iter_skill_dirs())
    if not skill_dirs:
        report.error("no skills found under skills/", file="skills/")

    for skill_dir in skill_dirs:
        fm = validate_skill(skill_dir, report, seen_names)
        if fm is not None and "name" in fm:
            skill_frontmatter[fm["name"]] = fm

    validate_manifest(skill_frontmatter, report)

    _emit(report, use_gha=use_gha, skill_count=len(skill_frontmatter))
    return 0 if report.ok else 1


def _emit(report: Report, *, use_gha: bool, skill_count: int) -> None:
    for warning in report.warnings:
        if use_gha:
            print(f"::warning::{warning}")
        else:
            print(f"[warn] {warning}")
    for err in report.errors:
        if use_gha:
            print(f"::error::{err}")
        else:
            print(f"[error] {err}")
    if report.ok:
        prefix = "::notice::" if use_gha else ""
        print(f"{prefix}validated {skill_count} skill(s); manifest in sync; no errors.")


if __name__ == "__main__":
    sys.exit(main())
