# Contributing to aidriven-resources

Thanks for helping improve the catalog. This repository is a collection of
**agent skills** — self-contained instruction packs that tell an AI coding
assistant *when* and *how* to perform a specific task.

## TL;DR

```bash
make install-hooks                          # one-time: wires .githooks/ into this clone
git checkout -b feat/my-new-skill
make new-skill name=my-new-skill           # scaffolds skills/my-new-skill/
$EDITOR skills/my-new-skill/SKILL.md        # replace the placeholder description
make validate                               # same gate CI runs
git commit -am "feat: add my-new-skill"    # pre-commit hook runs make sync for you
git push -u origin feat/my-new-skill
```

A draft PR is opened automatically on first push. After it's merged into
`main`, the release is cut and tagged automatically — you don't need to
bump versions or run any release commands.

> [!TIP]
> `make install-hooks` points `core.hooksPath` at [`.githooks/`](.githooks/).
> The `pre-commit` hook then auto-runs `make sync` whenever a `SKILL.md` is
> in the staged change, re-staging the regenerated `manifest.json` and
> README sections so the commit is self-consistent. Running it per clone is
> a one-liner; skipping it just means you'll have to run `make sync` by
> hand before pushing (CI will tell you if you forgot).

## The operating model

- **Source of truth**: each skill's `SKILL.md` frontmatter.
- **Derived catalog**: `manifest.json`. Never edit it by hand — run `make sync`.
- **Quality gate**: [`scripts/validate_repo.py`](scripts/validate_repo.py),
  run locally (`make validate`) and by CI on every push and PR.
- **Hygiene gate**: branch names, PR titles, and PR scope are enforced by CI.

## Branch taxonomy (enforced by CI)

Every branch targeting `main` must follow this convention. The `CI` workflow
rejects anything else (except `dependabot/**` and `revert-**`). The prefix
you pick also tells the [Auto release](.github/workflows/auto-release.yml)
workflow which semver bump to apply once your PR is merged.

| Prefix | Use for | Semver bump at release | PR title prefix | Auto-label |
|---|---|---|---|---|
| `feat/<slug>` | New skill, or new capability in an existing skill | **minor** | `feat:` | `new-skill` |
| `fix/<slug>` | Correcting instructions, links, or scripts in an existing skill | **patch** | `fix:` | `skill-update` |
| `chore/<slug>` | CI, Makefile, lint, governance, internal skills | **patch** | `chore:` | `governance` |
| `docs/<slug>` | README/CONTRIBUTING/RELEASING edits that do not touch skill frontmatter | none (no release cut) | `docs:` | `docs` |
| `release/vX.Y.Z` | Release PRs (opened by Auto release; you normally don't create these by hand) | — | `release:` | `release` |

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
   trigger-rich one — it should name concrete phrases the user would say
   when they want this skill, not a generic summary.
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

As a contributor, you don't need to do anything special — the
[Auto release](.github/workflows/auto-release.yml) workflow opens the
`release: vX.Y.Z` PR and pushes the tag after a maintainer approves it.
Branch prefix drives the bump (see the taxonomy above).

If you're a maintainer and need to cut a release by hand (major bump,
off-schedule patch, recovering from a broken automation run), see
[`RELEASING.md`](RELEASING.md) for the manual flow.
