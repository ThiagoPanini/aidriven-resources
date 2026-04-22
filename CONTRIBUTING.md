# Contributing to aidriven-resources

Thanks for helping improve the catalog. This repository is a collection of
**agent skills** — self-contained instruction packs that tell an AI coding
assistant *when* and *how* to perform a specific task.

## TL;DR

```bash
git checkout -b feat/my-new-skill
make new-skill name=my-new-skill           # scaffolds skills/my-new-skill/
$EDITOR skills/my-new-skill/SKILL.md        # replace the placeholder description
make sync                                   # regenerates manifest.json
make validate                               # same gate CI runs
git commit -am "feat: add my-new-skill"
git push -u origin feat/my-new-skill
```

A draft PR is opened automatically on first push.

## The operating model

- **Source of truth**: each skill's `SKILL.md` frontmatter.
- **Derived catalog**: `manifest.json`. Never edit it by hand — run `make sync`.
- **Quality gate**: [`scripts/validate_repo.py`](scripts/validate_repo.py),
  run locally (`make validate`) and by CI on every push and PR.
- **Hygiene gate**: branch names, PR titles, and PR scope are enforced by CI.
- **Internal accelerator**: the [`repo-skill-maintainer`](skills/repo-skill-maintainer/)
  skill encodes all of this for agents working inside the repo.

## Branch taxonomy (enforced by CI)

Every branch targeting `main` must follow this convention. The `CI` workflow
rejects anything else (except `dependabot/**` and `revert-**`).

| Prefix | Use for | Semver bump at release | PR title prefix | Auto-label |
|---|---|---|---|---|
| `feat/<slug>` | New skill, or new capability in an existing skill | **minor** | `feat:` | `new-skill` |
| `fix/<slug>` | Correcting instructions, links, or scripts in an existing skill | **patch** | `fix:` | `skill-update` |
| `chore/<slug>` | CI, Makefile, lint, governance, internal skills | **patch** | `chore:` | `governance` |
| `docs/<slug>` | README/CONTRIBUTING/RELEASING edits that do not touch skill frontmatter | none | `docs:` | `docs` |
| `release/vX.Y.Z` | Release PRs (version bump + tag) | — | `release:` | `release` |

Rules:

- `<slug>` is **kebab-case**. For `feat/` and `fix/`, it should match the
  skill directory name being added or changed.
- A PR under `feat/` or `fix/` must touch **only** `skills/<slug>/` plus
  optionally `manifest.json`, `README.md`, `CONTRIBUTING.md`, or `RELEASING.md`.
  Cross-skill edits must use `chore/` (or be split into separate PRs).
- PR titles follow [conventional-commits-lite](https://www.conventionalcommits.org/)
  shape: `type(optional-scope): summary` — e.g. `feat(python-unit-tests): add parametrize guidance`.
- Dependabot branches (`dependabot/**`) are exempt from the branch-name and
  PR-title checks — they are produced by automation.

## Adding a new skill

1. `git checkout -b feat/<kebab-case-name>`
2. `make new-skill name=<kebab-case-name>`
3. Replace the placeholder `description` in `SKILL.md` with a specific,
   trigger-rich one. See
   [skills/repo-skill-maintainer/references/description-rules.md](skills/repo-skill-maintainer/references/description-rules.md).
4. Write the body: **When to use / When NOT to use / Workflow / References**.
5. Put long-form background in `references/`, reusable files in `assets/`,
   and deterministic helpers in `scripts/`.
6. `make sync && make validate`
7. `git commit -am "feat: add <name>"` and push — CI opens a draft PR.

## Editing an existing skill

1. `git checkout -b fix/<existing-skill-name>`
2. Edit `SKILL.md` (or any of its `references/`, `assets/`, `scripts/` files).
3. If you changed the frontmatter `description`, run `make sync` so the
   manifest's short description (the first sentence) stays aligned.
4. `make validate` must pass before pushing.
5. `git commit -am "fix(<skill>): <summary>"` and push.

## What CI enforces

One CI workflow runs on every push and PR:

**[CI](.github/workflows/ci.yml)** — quality and convention gates:

- `SKILL.md` exists in every skill directory and has valid YAML frontmatter.
- `name:` frontmatter matches the directory name (both kebab-case).
- No duplicate skill names.
- All relative markdown links resolve.
- `manifest.json` is in sync with `skills/` (same names, real paths).
- Markdown and YAML pass lint.
- Branch name matches the taxonomy above.
- PR title matches the branch prefix.
- For `feat/` and `fix/` branches, the diff is scoped to a single skill.
- Draft PR is opened automatically from non-`main` pushes (except dependabot).

Any of these failing will block the PR. Run `make validate && make lint`
locally to catch the quality side before pushing; branch/title issues are
caught by CI on the first push.

## Releasing

Releases are a maintainer responsibility. See [`RELEASING.md`](RELEASING.md)
for the flow — it is built around a `release/vX.Y.Z` branch PR.
