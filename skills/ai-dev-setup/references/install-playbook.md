# Install / configure / validate / rollback playbook

The concrete rules for writing to the repo. Apply these to every install, regardless of category.

## Preconditions

Before any write:

1. Detection profile exists at `.ai-dev-setup/last-detection.json` (or in memory from Phase 1).
2. User has approved each decision, or approved the scope.
3. Git state known. If dirty, warn and offer to stash or create a branch — **git is the rollback mechanism**, so the working tree must be in a state where diffs are meaningful.
4. Working directory ensured: `mkdir -p .ai-dev-setup` as needed.
5. `.ai-dev-setup/` is git-ignored (add an entry to `.gitignore` on first use if missing).

## Reversibility via git

This skill does **not** maintain its own backup tarballs. Rollback relies on git:

- Make sure the tree is clean (or intentionally dirty with known changes) before each install step.
- Prefer one logical change per commit so a targeted `git revert` works cleanly.
- If the user wants to land everything in one commit, still stage each change separately so `git diff --staged` is reviewable.

If the repo is not a git repository, warn the user up front and either (a) initialize one with their approval or (b) proceed only with fully additive, easy-to-delete changes.

## Write rules

1. **Additive merge when possible.** For JSON/TOML/YAML configs, read → modify the relevant key → write. Don't clobber the whole file.
2. **Diff-preview before non-additive writes.** If you must replace, show the user the diff (even a compact one) and ask before writing.
3. **Idempotent.** Writing the skill's result twice should produce the same file. Check for presence of your target block before adding.
4. **No implicit creation.** If a parent directory doesn't exist and creating it has implications (e.g. `.cursor/` in a non-Cursor repo), confirm first.
5. **File permissions**: keep file modes as they were. Never make executable things non-executable or vice versa by accident.
6. **Line endings and final newline**: match existing convention; default to `\n` and a trailing newline.

## Secrets handling

- Never write a secret into a committed file.
- Reference secrets via env vars: `${GITHUB_PAT_TOKEN}`, `${OPENAI_API_KEY}`, etc.
- Ensure `.env` is in `.gitignore` before adding any file that could end up loading one.

## Changelog

Every run that writes anything appends to `.ai-dev-setup/changelog.md`:

```
## 2026-04-22T14:02:11Z  (run-id: <uuid>)
Mode: bootstrap
Decisions approved: 4

Changes:
- Created AGENTS.md (was missing)
- Merged "serena" into .mcp.json (previous: [mintlify])
- Added hook entry to .claude/settings.json (SessionStart -> serena-hooks activate)

Commit(s): <sha> (or "uncommitted — see git diff")
```

This is the single source of truth for what this skill has done over time.

## Validation

After writes, run category-specific validators or the general `scripts/validate.sh [category]`:

| Category | Validator checks |
|----------|------------------|
| ai-artifacts | File exists, under ~150 lines if always-loaded, no duplicate rules |
| mcp | `jq . <config>` passes; for stdio servers, binary on PATH |
| token-opt | `rtk gain` works (or Serena hook fires on next session start) |
| sdd | `.specify/` or chosen scaffolding exists with expected files |
| skills | Skill appears in the next session's skill listing |

Validation **must run**. A setup that "installed without errors" but doesn't actually work is worse than no setup.

## Rollback

All rollback goes through git. Tailor the command to how much the user wants to undo.

### Full rollback of an uncommitted run
```bash
# Discard everything this skill just wrote (working tree + staged)
git restore --staged --worktree .
# If new untracked files were created, drop them too:
git clean -fd
```

### Rollback of a committed run
```bash
git revert <sha>        # creates an inverse commit — preferred on shared branches
# or, if the branch is local-only and you're sure:
git reset --hard <sha-before-run>
```

### Partial rollback
The changelog lists per-file actions. Use `git restore` / `git checkout` for just those files:

```bash
git restore --source=<sha-before-run> -- .mcp.json
```

### When rollback isn't possible
Certain operations have side effects beyond files (running a CLI that mutates global config, installing a binary, writing to `~/`). List these in the changelog explicitly as "non-reversible via git" so the user knows.

## Summary contract

Every completed run produces, in order:

1. Changelog entry referencing the commit(s) or uncommitted diff.
2. Validation report (pass/fail per category).
3. User-facing report (see [interaction.md](interaction.md)).
4. Explicit rollback instructions (git commands) in the report.

If any of these is missing, the run is not complete.
