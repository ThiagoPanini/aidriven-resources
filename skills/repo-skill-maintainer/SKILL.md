---
name: repo-skill-maintainer
description: >
  Maintain the aidriven-resources skills catalog itself — add a new skill, edit an existing one,
  fix a failing validator run, regenerate the manifest, or prepare a release of this repository.
  Trigger this skill whenever the user says things like "add a new skill to this repo", "update
  the SKILL.md for X", "the CI validator is failing", "manifest is out of sync", "regenerate the
  manifest", "run release preflight", "bump the catalog version", "prep a release", "my skill
  folder is wrong", or "help me add a skill called Y". Only use inside the aidriven-resources
  repository — it encodes repo-specific conventions (Makefile targets, validator rules, manifest
  sync flow) and is not a general-purpose skill-authoring assistant. For creating brand-new
  skills from scratch in an unrelated project, prefer the general skill-creator flow instead.
---

# Repo Skill Maintainer

This skill keeps the `aidriven-resources` catalog healthy. It is the repo's internal accelerator
for the four operations maintainers actually do: **add**, **edit**, **validate**, **release**.
It does not replace the CI gates — those are the source of authority — but it makes sure you
arrive at the gates with a green tree.

## Golden rules

1. **`SKILL.md` frontmatter is the source of truth.** `manifest.json` is derived; do not edit it
   by hand — regenerate it with `make sync`.
2. **Skill directory name must equal `name:` in frontmatter.** Both must be kebab-case.
3. **Every change ends with `make validate`.** If it reports an error, fix it before committing;
   CI runs the exact same script and will block the PR otherwise.
4. **Releases are driven by `manifest.json` version + a matching `v*` git tag.** Never tag
   without running `make release-check` first.

## Branch taxonomy (enforced by CI)

Every agent-driven change must use the right branch prefix. The `PR Hygiene`
workflow rejects anything else.

| Prefix | Use for | Release bump |
|---|---|---|
| `feat/<slug>` | New skill or new capability | minor |
| `fix/<slug>` | Correction to existing skill | patch |
| `chore/<slug>` | Repo governance, CI, internal skills | patch |
| `docs/<slug>` | Docs not touching SKILL.md frontmatter | none |
| `release/vX.Y.Z` | Release PRs only | — |

`feat/` and `fix/` branches are **scope-locked** by CI: the diff must touch
only `skills/<slug>/` plus optionally `manifest.json`, `README.md`,
`CONTRIBUTING.md`, or `RELEASING.md`. Cross-skill edits belong under
`chore/`.

## The four operations

### 1. Add a new skill

```bash
git checkout -b feat/<kebab-case-name>
make new-skill name=<kebab-case-name>
# edit skills/<name>/SKILL.md — replace the placeholder description with a real, trigger-rich one
make sync         # add the new skill to manifest.json
make validate     # confirm everything is green
git commit -am "feat: add <kebab-case-name>"
```

Good descriptions are the #1 quality signal. See [references/description-rules.md](references/description-rules.md)
before finalizing.

### 2. Edit an existing skill

```bash
git checkout -b fix/<existing-skill-name>
```

* Change `SKILL.md` or its references/assets/scripts freely.
* If you touched the frontmatter `description`, run `make sync` so the manifest's short
  description (first sentence) stays aligned.
* Run `make validate` before committing.
* Don't rename the directory without also updating the `name:` frontmatter field — the validator
  will fail the mismatch.
* Commit title: `fix(<skill>): <summary>`. PR title prefix must match the branch prefix or the
  `PR Hygiene` workflow fails.

### 3. Fix a failing validator

The validator is a single Python script: [`scripts/validate_repo.py`](../../scripts/validate_repo.py).
The most common failures and their fixes:

| Error substring | Root cause | Fix |
|---|---|---|
| `missing SKILL.md entry point` | Directory under `skills/` has no entry file | Either add `SKILL.md` or delete the stray directory |
| `SKILL.md has no YAML frontmatter` | File doesn't start with `---` | Add a proper frontmatter block |
| `does not match directory` | `name:` frontmatter ≠ folder name | Align them (usually rename one to the other) |
| `is not kebab-case` | Folder has underscores, caps, or spaces | Rename to `kebab-case` |
| `broken relative link` | `SKILL.md` references a missing file | Create the file or remove the link |
| `manifest.json lists '<x>' but no such directory` | Stale manifest entry | Run `make sync` |
| `exists under skills/ but is not listed in manifest.json` | Missing manifest entry | Run `make sync` |
| `duplicate skill name` | Two skills share `name:` | Pick one — names must be globally unique |

For the full rule list, see [references/validator-rules.md](references/validator-rules.md).

### 4. Prepare a release

Releases **must** come from a `release/vX.Y.Z` branch PR — the Release
workflow's provenance check enforces this.

```bash
git checkout -b release/vX.Y.Z
$EDITOR manifest.json                # bump "version"
make sync                            # refresh derived fields
make release-check                   # local preflight
git commit -am "release: vX.Y.Z"
git push -u origin release/vX.Y.Z    # open and merge the PR

# After merge:
git checkout main && git pull --ff-only
git tag vX.Y.Z && git push origin vX.Y.Z
```

See [`RELEASING.md`](../../RELEASING.md) for the full checklist.

## What this skill will NOT do

* Edit `manifest.json` by hand — always sync instead.
* Skip `make validate` before declaring work done.
* Invent skill names not confirmed by the user.
* Add skills whose descriptions are vague or placeholder-only — a weak description is worse than
  no skill at all because it pollutes trigger matching across the catalog.

## Reference index

| Topic | File |
|---|---|
| What makes a strong `description:` | [references/description-rules.md](references/description-rules.md) |
| Exact validator rules & exit conditions | [references/validator-rules.md](references/validator-rules.md) |
| Release-day checklist (beyond `make release-check`) | [references/release-checklist.md](references/release-checklist.md) |
