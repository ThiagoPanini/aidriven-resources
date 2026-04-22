.PHONY: help validate sync sync-check release-check lint-md lint-yaml lint new-skill

PYTHON ?= python3

help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z0-9_-]+:.*##/ {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

validate: ## Run the repository validator (structure + frontmatter + manifest sync)
	@$(PYTHON) scripts/validate_repo.py

sync: ## Regenerate manifest.json from SKILL.md frontmatter
	@$(PYTHON) scripts/sync_manifest.py

sync-check: ## Fail if manifest.json is out of sync (non-destructive)
	@$(PYTHON) scripts/sync_manifest.py --check

release-check: validate sync-check ## Full preflight — same gates CI runs before a release
	@echo "release-check: OK — safe to tag."

lint-md: ## Lint all markdown with markdownlint-cli (requires npm install -g markdownlint-cli)
	@markdownlint --config .markdownlint.yml "**/*.md" --ignore node_modules

lint-yaml: ## Lint YAML files in .github and config roots
	@yamllint -c .yamllint.yml .github/ .markdownlint.yml .yamllint.yml

lint: lint-md lint-yaml ## Run all linters

new-skill: ## Scaffold a new skill directory: make new-skill name=my-skill
	@test -n "$(name)" || { echo "usage: make new-skill name=<kebab-case-name>"; exit 1; }
	@$(PYTHON) scripts/new_skill.py "$(name)"
