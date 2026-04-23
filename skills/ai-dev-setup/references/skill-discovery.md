# Skill discovery

When the in-scope work includes installing reusable skills, do active, **repo-aware** discovery before shortlisting. Do not recommend skills from memory — they may have been renamed, removed, or may never have existed. Do not anchor on any single well-known skill; let the detection profile drive the search.

## Prerequisite: `find-skills`

`find-skills` (Vercel's discovery helper that wraps `npx skills` and the `skills.sh` index) is the **required** entry point for this phase. Phase 1 detection already reports whether it's available (`ai_artifacts.find_skills` / `ai_artifacts.skills_cli`).

| Detection state | Action |
|---|---|
| `find_skills: true` **or** `skills_cli: true` | Proceed to the discovery workflow below. |
| Both `false` | **Stop and propose installing `find-skills` first** (or at minimum ensuring `npx skills --help` works). Treat this as a dedicated decision block — do not silently fall back to web browsing unless the user explicitly declines. |

Install proposal skeleton:

```
Decision: Install `find-skills` as the discovery prerequisite?
Why: No repeatable skill-search tool is available in this environment. Installing it now unblocks this phase and every future discovery pass.

  Option A — Recommended: install find-skills (project-scoped)
    Source: https://skills.sh/  (vercel-labs/skills)
    Best fit because: <tie to detection — e.g. "you already have .claude/skills/, so this lives alongside it">

  Option B: skip this phase entirely
    Best fit if: you don't want to add skills right now.

  Option C: one-shot web search of skills.sh
    Best fit if: you want a single recommendation and no persistent tooling.
```

## Deriving search terms from the repo (not from examples)

Do **not** start from a fixed list of "skills to always consider". Derive search terms from the detection profile so the discovery is biased toward what this specific repo needs:

| Detection signal | Derived search terms |
|---|---|
| `project.langs` | each language name, plus common frameworks detected in manifests (`django`, `fastapi`, `next`, `express`, `actix`, ...) |
| `project.pkg_mgr` | package-manager-specific skills (`uv`, `pnpm`, `poetry`, ...) |
| Test/build tools (pytest, jest, Makefile, justfile, tox) | testing skills for that runner |
| IaC / infra files (`*.tf`, `cdk.json`, `docker-compose.yml`, `k8s/`) | infra / cloud skills |
| `mcp.servers` already configured | complementary skills (e.g. a GitHub MCP suggests PR-review or release-prep skills) |
| `sdd.specify: true` | spec-driven skills (`speckit-*`) |
| `ai_artifacts.copilot` / `cursor` / `codex` | agent-specific skills for those tools |
| Gaps flagged in Phase 1 (no README, no tests, no CI) | skills that close those gaps (`create-readme`, test scaffolders, CI setup) |
| User's stated intent in the scope decision | their exact words as a search query |

Run a query per term, not one catch-all query. A broad "AI dev" query returns noise; targeted queries return signal.

Never include a skill in the shortlist merely because it appears in this repo's examples, registry, or past runs. Every candidate must trace back to a detection signal or an explicit user ask.

## Discovery workflow

### Step 1 — Verify the prerequisite

See the table above. Either `find-skills` is installed, `npx skills` works, or the user has explicitly approved a fallback.

### Step 2 — Build the query set

From the detection profile and user scope, enumerate 5–15 targeted search terms. Keep them narrow (e.g. `pytest fixtures`, not `python`). Deduplicate.

### Step 3 — Query and collect

For each term:

- If `find-skills` is installed, invoke it and read its recommendations.
- Otherwise run `npx skills find <term>` (or WebFetch against `skills.sh` if the user approved that fallback).

Collect raw results per term. Do not filter yet.

### Step 4 — Filter against the repo

Drop candidates that:

- are already present in `ai_artifacts.skills_dirs`;
- overlap in capability with an installed skill or MCP server (see [compatibility.md](compatibility.md));
- target a stack that doesn't exist here (e.g. a Terraform skill in a repo with no `.tf`);
- have no identifiable source repo or unclear maintenance status.

### Step 5 — Shortlist

Per approved category, keep **at most 3** candidates. Each entry must include:

- name
- source (repo / URL verified to exist)
- one-line description
- which detection signal(s) it maps to (explicit, not hand-wave)
- conflicts or overlap with already-installed skills/servers
- install path (managed registry? direct copy?)

If a category yields zero candidates after filtering, say so plainly instead of padding the list.

### Step 6 — Present using the decision block

Follow [interaction.md](interaction.md). One decision block per skill. The "Best fit because" line must cite a concrete signal from the detection profile (e.g. "you have `pytest.ini` and a tests/ dir, no existing testing skill"). Never "because it's popular".

### Step 7 — Install via the correct path

- **If a skill registry is detected** (`skills-lock.json` etc.): use the registry's own CLI. Do not write into the managed skills dir directly — the lock hash will break.
- **If no registry**: copy the skill folder into the appropriate skills directory (project-scoped by default — `.claude/skills/<name>/` or `.agents/skills/<name>/` depending on the existing convention).
- **Always validate**: after install, confirm the skill appears in the available-skills list (it will show up in the next session's `<system-reminder>` listing).

### Step 8 — Record

Add a line to `.ai-dev-setup/changelog.md`:

```
2026-04-22  install skill <name> from <source> via find-skills (mapped to signal: <signal>)
```

If a registry tool owns this file, let the registry record it and just note the registry invocation in the changelog instead.

## Common mistakes to avoid

- Starting the shortlist with a skill that was *mentioned in documentation* instead of one that maps to a detected signal.
- Recommending a skill that's already in `ai_artifacts.skills_dirs`.
- Recommending a skill whose source repo can't be located — silent invention.
- Skipping user approval because the skill "is obviously useful."
- Installing into the managed skills dir when a lockfile is in use.
- Overloading the shortlist with many skills. Three per category is the ceiling.
- Falling back to web browsing without proposing `find-skills` first.
