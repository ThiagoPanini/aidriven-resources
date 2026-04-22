# Releasing aidriven-resources

Releases are cut by merging a **`release/vX.Y.Z`** branch into `main` and
pushing a matching `vX.Y.Z` tag. Both sides are enforced by CI — the Release
workflow refuses to publish if the tag didn't come from a release PR.

## Before you tag

From a clean checkout of `main`:

```bash
git pull --ff-only
make release-check
```

`make release-check` runs the full validator **and** the `--check` mode of
the manifest sync script. It is the exact same gate the release workflow
runs, so a green result here means the tag will be accepted.

## Versioning

Semantic versioning, applied to the *catalog* as a whole. The branch prefix
of each merged PR tells you which bump it requires:

| Merged PR branches since last release | Required bump |
|---|---|
| Only `docs/*` | none — skip the release |
| Any `fix/*`, `chore/*`, or a mix without `feat/*` | **patch** (`0.1.0` → `0.1.1`) |
| At least one `feat/*` (new skill or new capability) | **minor** (`0.1.0` → `0.2.0`) |
| Removed/renamed a skill, changed the manifest schema, or any breaking change | **major** (`0.1.0` → `1.0.0`) |

## Cut the release

Use the release helper from a clean checkout:

```bash
make prepare-release version=X.Y.Z
```

It performs the guarded flow end to end:

- checks that the working tree is clean
- checks out and fast-forwards `main`
- creates `release/vX.Y.Z`
- bumps `manifest.json` `version`
- runs `make sync` and `make release-check`
- commits `release: vX.Y.Z`
- pushes the branch to `origin`

Manual equivalent:

```bash
git checkout -b release/vX.Y.Z
$EDITOR manifest.json                 # bump "version" to X.Y.Z
make sync                             # refresh updated_at + derived fields
make release-check                    # local preflight
git commit -am "release: vX.Y.Z"
git push -u origin release/vX.Y.Z
```

The `PR Hygiene` workflow will accept this branch because it matches
`release/v<semver>`. Open a PR titled `release: vX.Y.Z`, get it reviewed,
then merge into `main`.

## Tag and publish

After the `release/vX.Y.Z` PR is merged:

```bash
make publish-release version=X.Y.Z
```

Manual equivalent:

```bash
git checkout main
git pull --ff-only
git tag vX.Y.Z
git push origin vX.Y.Z
```

The `Release` workflow then runs its own preflight:

1. `validate_repo.py` — every skill is valid
2. `sync_manifest.py --check` — no manifest drift
3. Tag version equals `manifest.json` `version`
4. **Provenance** — the tagged commit came from a `release/vX.Y.Z` PR merge
   (or is a direct `release: vX.Y.Z` commit on `main`)

If any of the four fails, publishing is aborted before the release is
created. That's why the `release/v*` branch is non-optional — it is the
paper trail the provenance check looks for.

Once preflight passes, GitHub release notes are auto-generated from the PRs
merged since the previous tag, grouped by their branch-prefix labels.

## After the release ships

- Update the **Skill catalog** table in [`README.md`](README.md) if skills
  were added, renamed, or retired. README blurbs are the only catalog text
  not auto-generated.
- Announce the release in whatever downstream channel your consumers watch.

## What *not* to do

- Do **not** tag directly from a `feat/`, `fix/`, `chore/`, or `docs/`
  branch. The Release workflow's provenance check will reject it.
- Do **not** move a tag. If a release is broken, publish a new patch.
- Do **not** edit `manifest.json` by hand except for the `version` field.
  Everything else is derived from `SKILL.md` frontmatter via `make sync`.
