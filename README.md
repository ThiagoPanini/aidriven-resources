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

**Contents:** [Skill catalog](#skill-catalog) · [Quick start](#quick-start) · [Skill anatomy](#skill-anatomy) · [Repository layout](#repository-layout) · [Operating model](#operating-model) · [Maintainer workflow](#maintainer-workflow)

## Skill catalog

| Skill | Use it for | Includes |
|---|---|---|
| [`ai-dev-setup`](skills/ai-dev-setup/) | Auditing, bootstrapping, and optimizing repositories for AI-assisted development. | Detection, backup, validation scripts; templates for agent files; references for MCP, SDD, token optimization, and agent IDE setup. |
| [`github-actions-workflow-setup`](skills/github-actions-workflow-setup/) | Creating, updating, or modernizing GitHub Actions workflows. | Action catalog, workflow patterns, and stack-specific CI/CD recipes for Python, Node.js, Go, Rust, Docker, and publishing flows. |
| [`python-unit-tests`](skills/python-unit-tests/) | Generating pytest unit tests with clear Given/When/Then structure. | Test planning guidance, fixture and mocking rules, parameterization patterns, and edge-case coverage strategy. |
| [`repo-skill-maintainer`](skills/repo-skill-maintainer/) | *Internal.* Maintaining this catalog itself — adding skills, fixing validator failures, preparing releases. | Validator rules, description guidelines, release checklist. |

> [!NOTE]
> [`manifest.json`](manifest.json) is **derived** from each skill's `SKILL.md` frontmatter. Do not edit it by hand — run `make sync` instead.

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
│   ├── ai-dev-setup/
│   ├── github-actions-workflow-setup/
│   ├── python-unit-tests/
│   └── repo-skill-maintainer/       # Internal maintenance skill
├── scripts/                # Repo automation (validator, manifest sync, scaffolder)
│   ├── validate_repo.py
│   ├── sync_manifest.py
│   └── new_skill.py
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
- The [`repo-skill-maintainer`](skills/repo-skill-maintainer/) skill is an **accelerator**, not a
  gate — it helps agents do the right thing by default.

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
