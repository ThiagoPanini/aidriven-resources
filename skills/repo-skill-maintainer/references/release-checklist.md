# Release checklist

Publishing a new version of `aidriven-resources` is a branch-PR-tag dance.
Most of it is automated; the manual parts exist on purpose.

## 1. Decide the version

Look at the branch prefixes of every PR merged since the previous tag:

| Prefixes merged | Required bump |
|---|---|
| only `docs/*` | none — don't release |
| `fix/*`, `chore/*` (no `feat/*`) | patch (`0.1.0` → `0.1.1`) |
| at least one `feat/*` | minor (`0.1.0` → `0.2.0`) |
| removed/renamed a skill, schema change, or any breaking change | major (`0.1.0` → `1.0.0`) |

## 2. Cut the release branch

```bash
git checkout main && git pull --ff-only
git checkout -b release/vX.Y.Z

$EDITOR manifest.json                # bump "version"
make sync                            # refresh updated_at + derived fields
make release-check                   # local preflight

git commit -am "release: vX.Y.Z"
git push -u origin release/vX.Y.Z
```

The `PR Hygiene` workflow accepts `release/v<semver>` branches specifically.
Open a PR titled `release: vX.Y.Z`, get a review, and merge.

## 3. Tag and push

After the release PR is merged to `main`:

```bash
git checkout main && git pull --ff-only
git tag vX.Y.Z
git push origin vX.Y.Z
```

The `Release` workflow runs its own preflight and will **refuse** to publish
if any of these fail:

- validator reports any error
- manifest is out of sync with `skills/`
- tag version doesn't equal `manifest.json`'s `version`
- tagged commit didn't come from a `release/vX.Y.Z` PR merge (or a direct
  `release: vX.Y.Z` commit on `main`)

## 4. After the release ships

- Verify the GitHub release page populated with auto-generated notes.
- If a skill was added or renamed, update the **Skill catalog** table in
  [`README.md`](../../../README.md). The README blurbs are the only catalog
  text that is *not* auto-synced.
- If this is the first release after changing repo layout or workflows,
  mention it in the release notes by hand so consumers notice.
