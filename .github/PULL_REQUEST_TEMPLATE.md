<!--
  PR title must match the branch prefix:
    feat/*    → feat: ...
    fix/*     → fix: ...
    chore/*   → chore: ...
    docs/*    → docs: ...
    release/* → release: vX.Y.Z
  The PR Hygiene workflow will reject mismatches.
-->

## Summary

<!-- Describe the changes in this PR. What does it do? Why? -->

## Type of change

- [ ] `feat` — new skill or new capability in an existing skill
- [ ] `fix`  — correction to an existing skill
- [ ] `chore` — repo governance, CI, internal skill
- [ ] `docs` — README / CONTRIBUTING / RELEASING edit
- [ ] `release` — version bump PR

## Scope

<!-- Which skill(s) does this PR affect? For feat/* and fix/* PRs, CI requires exactly one. -->

## Related issues

<!-- Link any related issues: Closes #123, Fixes #456 -->

## Checklist

- [ ] `make validate` passes locally
- [ ] `make sync` was run if frontmatter changed
- [ ] PR title matches the branch prefix (enforced by CI)
- [ ] Self-reviewed the diff
