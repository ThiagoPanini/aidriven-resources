# aidriven-resources

Curated collection of AI skills for Claude Code, GitHub Copilot, and other AI-assisted development tools. Each skill is a self-contained set of instructions and resources that teaches an AI assistant how to perform a specific task well.

## Skills

| Skill | Description |
|---|---|
| [github-actions-workflow-setup](skills/github-actions-workflow-setup/) | Create, update, or modernize GitHub Actions workflows for any repository |
| [python-project-setup](skills/python-project-setup/) | Configure modern Python development tooling (pyproject.toml, ruff, mypy, pre-commit) |
| [python-unit-tests](skills/python-unit-tests/) | Generate high-quality pytest tests using the Given/When/Then pattern |
| [skill-creator](skills/skill-creator/) | Create new skills, run evals, benchmark performance, and optimize triggering |

The full list with metadata is available in [`skills.json`](skills.json).

## Skill structure

Every skill follows the same layout:

```
skill-name/
├── SKILL.md              # Entry point (required) — YAML frontmatter + instructions
├── references/           # Documentation loaded into context as needed
├── assets/               # Templates, config files, static resources
└── scripts/              # Helper scripts for deterministic tasks
```

`SKILL.md` must start with YAML frontmatter containing at least `name` and `description`. The description controls when the AI assistant activates the skill. Only `SKILL.md` is required — the subdirectories are optional.

## Using a skill

### Claude Code

Copy the skill directory into your project's `.claude/skills/`:

```bash
cp -r skills/python-project-setup .claude/skills/
```

Or reference it directly when installing from this repository.

### GitHub Copilot

Copy the skill directory into your project's `.copilot/skills/`:

```bash
cp -r skills/python-project-setup .copilot/skills/
```

### Pinning a version

Each [release](https://github.com/ThiagoPanini/aidriven-resources/releases) is tagged with a semantic version (e.g., `v0.1.0`). To use a stable snapshot instead of tracking `main`:

```bash
git clone --branch v0.1.0 --depth 1 https://github.com/ThiagoPanini/aidriven-resources.git
```

The `version` field in [`skills.json`](skills.json) always matches the latest release tag.

## Repository layout

```
aidriven-resources/
├── skills/                  # Canonical source of all published skills
│   ├── github-actions-workflow-setup/
│   ├── python-project-setup/
│   ├── python-unit-tests/
│   └── skill-creator/
├── skills.json              # Manifest — lists all skills with metadata
├── .claude/skills/          # Internal skills used to maintain this repo (Claude Code)
├── .copilot/skills/         # Internal skills used to maintain this repo (Copilot)
├── .github/
│   ├── workflows/           # CI, validation, release, auto-PR workflows
│   ├── ISSUE_TEMPLATE/      # Bug report and feature request templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
├── .editorconfig
├── .markdownlint.yml
├── .yamllint.yml
└── .gitignore
```

`skills/` is the distributable content. `.claude/` and `.copilot/` are internal tooling consumed by this project itself and are not intended for external use.

## Contributing

All changes go through pull requests. Direct push to `main` is blocked.

### Adding a new skill

1. Create a branch: `feat/skill-name`
2. Add `skills/skill-name/SKILL.md` with YAML frontmatter (`name`, `description`)
3. Add supporting files under `references/`, `assets/`, or `scripts/` as needed
4. Add an entry to `skills.json`
5. Push — a draft PR is created automatically and CI runs on the branch

### Updating an existing skill

1. Create a branch: `fix/skill-name-short-description`
2. Edit the skill files
3. Update `skills.json` if the description changed
4. Push — draft PR is created, CI validates everything

### Branch naming

| Prefix | Purpose | Auto-label |
|---|---|---|
| `feat/**` | New skill or feature | `new-skill` |
| `fix/**` | Fix or update to existing skill | `skill-update` |
| `chore/**` | CI, config, governance changes | `governance` |

### What CI checks

Every PR must pass these checks before merge:

| Check | What it validates |
|---|---|
| **Markdown Lint** | Markdown formatting in `skills/` and `README.md` |
| **Link Check** | No broken links in markdown files |
| **YAML Lint** | Valid YAML in `.github/` workflow files |
| **Validate Skill Structure** | Every skill has `SKILL.md` with frontmatter, kebab-case naming, `skills.json` is in sync |

### Merge strategy

All PRs are **squash merged** — each PR becomes a single clean commit on `main`. Branches are deleted automatically after merge.

## Versioning

This repository uses **repository-wide semantic versioning** tracked in `skills.json`:

- The `version` field reflects the current release version
- Each GitHub Release tag (e.g., `v0.1.0`) must match the manifest version
- Individual skills track which version they were added in via the `added_in` field

### Creating a release

1. Bump `version` in `skills.json` and merge via PR
2. Tag and push: `git tag v0.2.0 && git push origin v0.2.0`
3. The release workflow validates the tag against the manifest and creates a GitHub Release with auto-generated notes

## License

[MIT](LICENSE)
