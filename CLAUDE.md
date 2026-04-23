# Agent guide — aidriven-resources

This repository is a **catalog of agent skills**, not an application. If you are an AI assistant landing here (Claude Code, Codex, Copilot, Cursor, or any other), read this file before making changes.

## What lives here

- [skills/](skills/) — published skills, one folder per skill, each with `SKILL.md` as the entry point plus optional `references/`, `assets/`, `scripts/`.
- [manifest.json](manifest.json) — **derived** catalog index. Built from each skill's `SKILL.md` frontmatter.
- [.agents/skills/](.agents/skills/) — canonical install location for skills used *by* this repo's maintainers.
- [.claude/skills/](.claude/skills/) — symlinks pointing into `.agents/skills/` so Claude Code discovers them without duplication.
- [scripts/](scripts/) — Python helpers: `validate_repo.py`, `sync_manifest.py`, `new_skill.py`, `release.py`.

## Golden rules

1. **Never hand-edit `manifest.json`.** It is generated. Edit `SKILL.md` frontmatter and run `make sync`.
2. **Never hand-edit `skills-lock.json`.** It is managed by a skill-registry tool; the `computedHash` will be wrong if you touch it by hand.
3. **Scaffold new skills with `make new-skill name=<kebab-case>`**, not by hand-copying folders.
4. **Run the preflight before claiming done**: `make validate` (structure, frontmatter, manifest sync). For release prep, `make release-check`.
5. **Markdown and YAML must lint clean**: `make lint` (requires `markdownlint-cli` and `yamllint`).

## Common workflows

| Task | Command |
|------|---------|
| Validate the catalog | `make validate` |
| Regenerate manifest after editing a `SKILL.md` | `make sync` |
| Check manifest is in sync (read-only) | `make sync-check` |
| Add a new skill | `make new-skill name=<kebab-case>` |
| Lint markdown + yaml | `make lint` |
| Full release preflight | `make release-check` |
| Prepare a release branch | `make prepare-release version=<semver>` |
| Publish a tagged release | `make publish-release version=<semver>` |

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor etiquette and [RELEASING.md](RELEASING.md) for the full release playbook.

## Agent context files

- [AGENTS.md](AGENTS.md) — this file; canonical guidance, read by Codex, Cursor, and most agent tools.
- [CLAUDE.md](CLAUDE.md) — Claude Code entry point; imports this file via `@AGENTS.md`.

When updating guidance, edit **this file** and let `CLAUDE.md` pick it up via the import.

## Recommended companion skills

External skills that fit the maintainer workflow (install via your skill-registry tool, e.g. `find-skills`):

- **`find-skills`** (vercel-labs/skills) — search [skills.sh](https://skills.sh/) locally when deciding what to pull into the catalog.
- **`skill-creator`** (anthropics/skills) — already tracked in `skills-lock.json`; use for authoring new skills from scratch.
- **`create-readme`** (github/awesome-copilot) — already tracked; use for generating/refreshing READMEs.

## What this repo is *not*

- Not a place for application code, tests beyond skill-level fixtures, or product features.
- Not a dumping ground — every skill earns its place via the validator rules in [`scripts/validate_repo.py`](scripts/validate_repo.py).
