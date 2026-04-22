# What makes a strong `description:`

The `description` field in a skill's frontmatter is the single most important
string in the whole skill. It is what the assistant reads to decide whether
*this* skill matches *this* user request. A vague description means the skill
never triggers when it should — or worse, triggers on unrelated requests and
pollutes the catalog.

## Targets

- **Length**: between ~100 and ~1500 characters. The validator warns below 40
  and errors above 4096, but those are hard bounds — aim for the middle.
- **Shape**: one tight opening sentence that names the capability, followed
  by concrete trigger phrases and an optional "don't use when" clause.
- **Voice**: describe what the skill *does* for the user, not what the author
  built. "Generate pytest unit tests…" not "A skill for tests."

## Must include

1. **A concrete capability verb** — "generate", "bootstrap", "modernize",
   "audit", "create", "review". Never "helps with" or "related to".
2. **The noun the skill acts on** — "GitHub Actions workflows", "pytest unit
   tests", "AI-assisted development setup", etc.
3. **Real user phrasings** — quote the kinds of requests this should match.
   "Invoke when the user says 'add CI', 'fix my workflow', 'set up tests for
   this module'." The model pattern-matches these heavily.
4. **Scope boundary** — one line on what this skill is *not* for. This is
   what stops collisions with neighbouring skills in the catalog.

## Avoid

- Abstract marketing language ("powerful", "seamless", "comprehensive").
- Listing implementation details ("uses Python 3.12 and yaml parsing").
- Repeating the skill name instead of describing it.
- Trigger phrases copied verbatim from another skill in the catalog —
  collisions degrade routing accuracy.

## Good example (ai-dev-setup, abbreviated)

> Bootstrap and optimize a repository for AI-assisted development. Analyzes
> the repo, detects existing AI tooling, curates candidate artifacts
> (skills, prompts, agent instructions, SDD scaffolding, MCP servers, token
> optimizers, IDE integrations), asks for approval on each meaningful
> decision, then installs and validates. Trigger on phrasings like
> "configure this project for AI", "install an MCP server here", "add Spec
> Kit", "review our agentic setup"…

Note: verb-first opener, concrete nouns, explicit user phrasings, implicit
boundary ("repository-scoped, not a codegen tool").

## Bad example

> A useful skill for developers who want to work with AI tools in their
> projects and get better results from their setup.

No verb that tells the model *when* to fire, no trigger phrases, no scope.
This description will either never match or match everything — both fail modes
erode catalog quality.
