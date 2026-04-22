# Validator rules

The validator is [`scripts/validate_repo.py`](../../../scripts/validate_repo.py).
It is the authoritative gate — CI runs the exact same script, so "green
locally" means "green in CI".

## Structural rules

| Rule | Level |
|---|---|
| every directory under `skills/` contains a `SKILL.md` | error |
| `SKILL.md` starts with `---` and has a closing `---` frontmatter delimiter | error |
| frontmatter contains `name` and `description` fields | error |
| skill directory name is kebab-case (`^[a-z0-9]+(-[a-z0-9]+)*$`) | error |
| frontmatter `name` matches the directory name | error |
| no two skills share the same `name` | error |
| description length is between 40 and 4096 chars | warn/error |

## Link and script rules

| Rule | Level |
|---|---|
| every relative markdown link in `SKILL.md` resolves to an existing file | error |
| `http(s)://`, `mailto:`, and `#anchor` links are skipped (not checked) | — |
| `.sh` scripts under a skill's `scripts/` directory have the executable bit set | warn |

## Manifest rules

| Rule | Level |
|---|---|
| `manifest.json` exists and parses as JSON | error |
| `version` is a valid semver string | error |
| `skills` is an array of objects, each with a unique `name` | error |
| every manifest entry's `path_in_repo` exists | error |
| every manifest entry's `entry` file exists | error |
| every skill on disk is listed in the manifest | error |
| every manifest entry has a matching skill directory (no orphans) | error |

## Running the validator

```bash
python3 scripts/validate_repo.py              # human-readable (local)
python3 scripts/validate_repo.py --format=github   # CI annotations
make validate                                 # preferred entry point
```

Exit code: `0` on success, non-zero on any error. Warnings do not fail.

## Relationship to `make sync`

`make sync` rewrites `manifest.json` from `SKILL.md` frontmatter. If the
validator complains the manifest is out of sync, `make sync` is always the
correct fix — hand-editing the manifest is never the right move.
