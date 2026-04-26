# AGENTS-TEMPLATE.md

> **Auto-generated from the AAIF AGENTS.md standard.**
> Source: `agentsmd/agents.md` @ `251d980b`
> Do not edit manually. Run `python scripts/sync-agents-standard.py` to update.

---

## About This Template

This file is the **canonical reference** that the dac-pipeline uses to validate
and lint `AGENTS.md` files in target repositories. It encodes the current best
practices as defined by the Agentic AI Foundation (AAIF).

When the pipeline detects a target repo's `AGENTS.md` deviates from this template,
it flags the deviation as documentation drift.

---

## Recommended Sections

An effective `AGENTS.md` should include the following sections (order is flexible):

- **Dev environment tips**
- **Testing instructions**
- **PR instructions**

---

## Guidance Rules

The following rules are derived from the official standard and real-world examples:

- Title format: [<project_name>] <Title>
- Prefer TypeScript (`.tsx`/`.ts`) for new components and utilities.

---

## Minimal Example

```markdown
# AGENTS.md

## Setup commands
- Install dependencies: `<your-install-command>`
- Start dev server: `<your-start-command>`

## Testing instructions
- Run the full test suite: `<your-test-command>`
- Run a single test: `<your-test-command> path/to/test.py::TestClass::test_method`
- All commits must pass CI before merging.

## Code style
- Use the project's configured linter and formatter.
- Follow existing naming conventions in the codebase.

## PR instructions
- Title format: `[<scope>] <description>`
- Run lint and tests before committing.
```

---

## Validation Checklist

When the dac-pipeline lints a repo's `AGENTS.md`, it checks:

- [ ] File exists at repo root (or nearest to edited file in monorepos)
- [ ] Uses standard Markdown (no proprietary syntax)
- [ ] Contains at least 2 recommended sections from the list above
- [ ] Instructions are action-oriented (imperative, not descriptive)
- [ ] Commands are exact and copy-pasteable where possible
- [ ] No placeholder text left unmodified (e.g., `<your command>`)
- [ ] Updated within the last 90 days (living document principle)

---

## Changelog

- `251d980b` — Auto-synced from upstream `agentsmd/agents.md`

