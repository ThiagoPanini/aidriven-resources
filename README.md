# aidriven-resources

*Reusable skills, templates, and references for AI-assisted development workflows.*

[![CI](https://img.shields.io/github/actions/workflow/status/ThiagoPanini/aidriven-resources/ci.yml?branch=main&style=flat-square&label=ci)](https://github.com/ThiagoPanini/aidriven-resources/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/ThiagoPanini/aidriven-resources?style=flat-square)](https://github.com/ThiagoPanini/aidriven-resources/releases)
[![Catalog](https://img.shields.io/badge/skills-catalog-3c873a?style=flat-square)](skills/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

This repository is a curated catalog of **agent skills**: self-contained instruction packs that help
AI coding assistants perform specific tasks with more consistency, context, and care. Each skill
combines a `SKILL.md` entry point with optional references, reusable assets, and deterministic
scripts.

Use it as a source of ready-made skills, or as a reference for building your own skill catalog.

**Contents:** [Skill catalog](#skill-catalog) · [Quick start](#quick-start) · [AI Setup](#ai-setup) · [Skill anatomy](#skill-anatomy) · [Repository layout](#repository-layout) · [Operating model](#operating-model) · [Maintainer workflow](#maintainer-workflow)

## Skill catalog

<!-- skills:catalog:start -->
| Skill | Use it for |
|---|---|
| [`ai-dev-setup`](skills/ai-dev-setup/) | Bootstrap and optimize a repository for AI-assisted development. |
| [`github-actions-workflow-setup`](skills/github-actions-workflow-setup/) | Create, update, or modernize GitHub Actions workflows for any repository. |
| [`python-unit-tests`](skills/python-unit-tests/) | Generate high-quality Python unit tests using pytest, organized with the Given/When/Then (GWT) pattern. |
<!-- skills:catalog:end -->

> [!NOTE]
> The table above and the `skills/` subtree in [Repository layout](#repository-layout) are **derived** from each `SKILL.md` frontmatter. Do not edit them by hand — run `make sync` instead. The same applies to [`manifest.json`](manifest.json).

## Quick start

Clone the catalog:

```bash
git clone https://github.com/ThiagoPanini/aidriven-resources.git
cd aidriven-resources
```

Install a skill into a project-local skills directory:

```bash
mkdir -p /path/to/your-project/.agents/skills
cp -R skills/python-unit-tests /path/to/your-project/.agents/skills/
```

For Claude Code-style project skills, use `.claude/skills/` instead:

```bash
mkdir -p /path/to/your-project/.claude/skills
cp -R skills/github-actions-workflow-setup /path/to/your-project/.claude/skills/
```

Then invoke the skill by name in your assistant prompt, for example:

```text
Use the python-unit-tests skill to add pytest coverage for src/orders.py.
```

> [!TIP]
> The `description` field in each `SKILL.md` is what helps an assistant decide when to activate a skill automatically. Keep it specific, action-oriented, and full of realistic trigger phrases.

## AI Setup

The repository is configured for AI-assisted maintenance so skills can be authored, validated, and released with minimal friction. Each component is scoped to the workflow it serves:

- [`AGENTS.md`](AGENTS.md) — single source of truth for agent-agnostic rules (Claude Code, Codex, Cursor, Copilot). Keeps catalog conventions in one place instead of duplicating them per tool.
- [`CLAUDE.md`](CLAUDE.md) — thin Claude Code entry point that imports `AGENTS.md`, so rule updates propagate without drift.
- [`.agents/skills/`](.agents/skills/) — canonical install location for maintainer-facing skills used *by* this repo (`ai-dev-setup`, `find-skills`, `skill-creator`, `create-readme`).
- [`.claude/skills/`](.claude/skills/) — symlinks into `.agents/skills/` so Claude Code discovers the same skills without duplication.
- [`find-skills`](https://skills.sh/) (prerequisite) — discovery helper for `skills.sh`. The `ai-dev-setup` skill requires it before recommending new skills; install it first if it's missing.
- [`scripts/`](scripts/) + [`Makefile`](Makefile) — deterministic validators, manifest sync, and scaffolder. Agents can run `make validate` / `make sync` to verify their work instead of guessing.
- [`manifest.json`](manifest.json) — derived catalog index regenerated from each `SKILL.md` frontmatter, keeping agents and humans reading from the same source of truth.

Together these components keep agent context small, rules consistent across tools, and catalog changes reviewable.

## Skill anatomy

Every skill follows the same basic shape:

```text
skill-name/
├── SKILL.md       # Required entry point: YAML frontmatter + instructions
├── references/    # Optional deeper guidance loaded only when needed
├── assets/        # Optional templates, snippets, configs, and static files
└── scripts/       # Optional executable helpers for repeatable work
```

`SKILL.md` starts with YAML frontmatter:

```yaml
---
name: python-unit-tests
description: Generate high-quality Python unit tests using pytest with the Given/When/Then pattern.
---
```

Good skills are small enough to load quickly, but complete enough to guide an agent through the
task without guesswork. Prefer focused references and scripts over one giant instruction file.

## Repository layout

```text
aidriven-resources/
├── skills/                 # Published skill source (the catalog)
<!-- skills:tree:start -->
│   ├── ai-dev-setup/
│   ├── github-actions-workflow-setup/
│   └── python-unit-tests/
<!-- skills:tree:end -->
├── scripts/                # Repo automation (validator, sync, scaffolder, release helper)
│   ├── validate_repo.py
│   ├── sync_manifest.py
│   ├── sync_readme.py
│   ├── new_skill.py
│   └── release.py
├── manifest.json           # Derived catalog (generated from SKILL.md frontmatter)
├── Makefile                # Maintainer entry points
├── CONTRIBUTING.md
├── RELEASING.md
├── .github/
│   ├── workflows/          # CI and release automation
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
├── .markdownlint.yml
├── .yamllint.yml
└── .gitignore
```

Ignored directories such as `.agents/` and `.claude/` may exist locally for maintaining this
repository, but distributable skills live under [`skills/`](skills/).

## Operating model

One idea drives the whole repo:

> **`SKILL.md` frontmatter is the single source of truth. Everything else is derived.**

- `manifest.json` is regenerated from each `SKILL.md`'s frontmatter by
  [`scripts/sync_manifest.py`](scripts/sync_manifest.py). Only `version` and `added_in` are
  human-owned; the rest is mechanical.
- [`scripts/validate_repo.py`](scripts/validate_repo.py) is the **authoritative quality gate** —
  CI runs the exact same script, so "green locally" means "green in CI".
- GitHub Actions enforce mandatory CI gates: validator + manifest sync on every push/PR; release
  preflight on every `v*` tag.

## Maintainer workflow

Everything you need is behind four Make targets:

```bash
make validate        # Run the repository validator (structure + frontmatter + manifest sync)
make sync            # Regenerate manifest.json from SKILL.md frontmatter
make sync-check      # Fail if manifest.json is out of sync (non-destructive)
make release-check   # Full preflight — same gates CI runs before a release
```

Plus two helpers:

```bash
make new-skill name=<kebab-case-name>   # Scaffold skills/<name>/
make lint                                # Markdown + YAML lint
```

For the full flow, see [`CONTRIBUTING.md`](CONTRIBUTING.md). For releases, see
[`RELEASING.md`](RELEASING.md).

### Branch taxonomy (enforced by CI)

| Prefix | Use for | Release bump |
|---|---|---|
| `feat/<slug>` | New skill or new capability | minor |
| `fix/<slug>` | Correction to existing skill | patch |
| `chore/<slug>` | CI, Makefile, governance, internal skills | patch |
| `docs/<slug>` | README/CONTRIBUTING/RELEASING edits | none |
| `release/vX.Y.Z` | Release PRs | — |

`feat/` and `fix/` branches are scope-locked by CI to `skills/<slug>/` plus a
short allow-list of root files. Dependabot branches bypass the convention.
Full details in [CONTRIBUTING.md](CONTRIBUTING.md).

### What CI enforces

| Workflow | Triggered on | What it prevents |
|---|---|---|
| [`CI`](.github/workflows/ci.yml) — `validate` | every push, every PR | missing `SKILL.md`, broken frontmatter, kebab-case violations, name/dir mismatch, duplicate skills, broken relative links, manifest drift |
| [`CI`](.github/workflows/ci.yml) — `lint` | every push, every PR | markdown and YAML formatting regressions |
| [`CI`](.github/workflows/ci.yml) — `branch-name` | every push, every PR | off-convention branch names |
| [`CI`](.github/workflows/ci.yml) — `pr-title` | every PR | PR titles that don't match the branch prefix |
| [`CI`](.github/workflows/ci.yml) — `skill-scope` | every `feat/*` / `fix/*` PR | PRs that accidentally touch multiple skills |
| [`Release`](.github/workflows/release.yml) — `preflight` | `v*` tags | drifted manifest, tag/version mismatch, or a tag that didn't come from a `release/v*` PR |
