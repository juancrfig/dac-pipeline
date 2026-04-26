# ADR 000: Adoption of AGENTS.md as Project Context Standard

**Status:** Proposed  
**Date:** 2026-04-26  
**Author:** dac-pipeline maintainers  
**Stakeholders:** AI coding agents, human contributors, CI/CD pipeline  

---

## Context

The **Agentic AI Foundation (AAIF)** — a Linux Foundation project — is stewarding an emerging open standard called **AGENTS.md**. It is already used by **60,000+ open-source projects** and supported by a growing ecosystem of AI coding agents (OpenAI Codex, Google Jules, Goose, Aider, Zed, Warp, Cursor, Factory, opencode, etc.).

Our project (`dac-pipeline`) is a Docs-as-Code CI pipeline. We intend to leverage AI coding agents extensively for documentation drift detection, automated fixes, and PR generation. To do this effectively, agents need structured, predictable context about our codebase.

## Decision

We will adopt **AGENTS.md** as the canonical file for providing AI coding agents with project-specific context, instructions, and conventions. This ADR defines how we will structure, maintain, and evolve this file.

Additionally, we will implement an **automated standard-sync mechanism**: a script that fetches canonical patterns, guidance, and examples from the upstream `agentsmd/agents.md` repository and updates our local `AGENTS-TEMPLATE.md` and validation rules. This ensures our pipeline's enforcement of the standard is always aligned with the latest AAIF guidance.

---

## What AGENTS.md Is (Per the Standard)

> *"A simple, open format for guiding coding agents. Think of AGENTS.md as a README for agents: a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project."* — [agents.md](https://agents.md)

### Core Principles of the Standard

| Principle | Description |
|-----------|-------------|
| **Predictable location** | `AGENTS.md` at repo root (or nested in subdirectories for monorepos) |
| **Standard Markdown** | No required fields, no rigid schema — just Markdown the agent parses |
| **Agent-focused** | Contains what agents need: build steps, test commands, conventions, gotchas |
| **Living document** | Updated continuously as the project evolves |
| **Proximity wins** | In monorepos, the nearest `AGENTS.md` to the edited file takes precedence |
| **User prompt overrides** | Explicit user chat instructions always beat `AGENTS.md` |

### Why Separate from README.md?

- **README.md** = for humans (quick start, project description, contribution guidelines)
- **AGENTS.md** = for agents (detailed build/test steps, code style, tool-specific gotchas)
- Keeps READMEs concise while giving agents the verbose context they need

---

## Effective Format & Structure

Based on analysis of real-world examples (OpenAI Codex, Apache Airflow, Temporal SDK) and the official guidance, an effective `AGENTS.md` should be:

### 1. **Traceable to Real Failures**

> *"Every line in a good AGENTS.md should be traceable back to a specific thing that went wrong."* — Addy Osmani

Each instruction should solve a real problem the agent has encountered (or will likely encounter).

### 2. **Action-Oriented**

Use imperative language. Agents execute instructions; they don't interpret intent.

**Good:**
```markdown
## Testing
- Run `pytest tests/ -xvs` before committing.
- If Docker networking fails, run `docker network prune` first.
```

**Bad:**
```markdown
## Testing
We use pytest for testing. Make sure everything passes.
```

### 3. **Section-Based Organization**

Common sections across 60k+ projects:

| Section | Purpose |
|---------|---------|
| `## Setup commands` | How to install deps, start dev environment |
| `## Build commands` | Compilation, bundling, generation steps |
| `## Testing instructions` | Exact test commands, CI expectations |
| `## Code style` | Linting rules, formatting, naming conventions |
| `## Architecture boundaries` | What not to touch, module boundaries |
| `## Security considerations` | Secrets handling, sandbox rules |
| `## PR / commit conventions` | Title formats, required checks |
| `## Common gotchas` | Known pitfalls, environment quirks |

### 4. **Tool-Specific Precision**

Agents need exact commands, not approximations:

```markdown
## Commands
- Run a single test: `uv run --project <PROJECT> pytest path/to/test.py -xvs`
- Type-check: `prek run mypy-airflow-core --all-files`
- Lint changed files only: `prek run ruff --from-ref <target_branch>`
```

### 5. **Monorepo Support (Nested AGENTS.md)**

For large repos, place `AGENTS.md` in subdirectories. Agents read the nearest one. Example: OpenAI's main repo has **88 nested AGENTS.md files**.

---

## Role AGENTS.md Plays in the Ecosystem

The standard is trying to establish AGENTS.md as:

1. **A universal contract** between human maintainers and AI agents — any agent (Codex, Jules, Goose, etc.) can read the same file and understand how to work on the project.

2. **A neutral, open format** — stewarded by AAIF under the Linux Foundation, not controlled by any single vendor. This prevents fragmentation into proprietary formats (`.cursorrules`, `.aider.conf.yml`, etc.).

3. **A living, versioned instruction set** — unlike one-shot prompts, AGENTS.md persists in the repo, evolves with the code, and is always contextually relevant.

4. **The agent's "first read"** — agents automatically discover and load AGENTS.md before working on a project, making it zero-friction for developers.

### Supported Agents (as of 2026-04)

| Agent | Integration |
|-------|-------------|
| OpenAI Codex | Native |
| Google Jules | Native |
| Factory | Native |
| Aider | Configurable via `.aider.conf.yml` |
| Goose | Native |
| opencode | Native |
| Zed | Native |
| Warp | Native |
| Gemini CLI | Configurable via `.gemini/settings.json` |
| Cursor | Native |

---

## How We Will Use It in dac-pipeline

Our `AGENTS.md` will focus on:

1. **Pipeline orchestration rules** — how the doc-tool stages interact
2. **AST parsing conventions** — which parsers to use for which languages
3. **Drift detection heuristics** — what constitutes "drift" vs. intentional change
4. **CI/CD integration** — how agents should generate PRs that pass our checks
5. **Security boundaries** — no secrets in generated docs, no arbitrary code execution

### Standard-Sync Mechanism

Because the AAIF standard is evolving, we will not hard-code our understanding of "good AGENTS.md" structure. Instead:

1. **`scripts/sync-agents-standard.py`** — A script that fetches the latest canonical guidance from the upstream `agentsmd/agents.md` repo (README.md, their own AGENTS.md, and any new files in a `spec/` or `guidelines/` directory if introduced).
2. **`AGENTS-TEMPLATE.md`** — A derived template file that captures the current recommended sections, formatting patterns, and examples from the standard. This is what our pipeline uses as the "reference" for linting/validating AGENTS.md files in target repos.
3. **CI cron job** — Runs the sync script weekly. If the upstream changed, it opens a PR updating `AGENTS-TEMPLATE.md` and our validation rules.
4. **Pipeline integration** — When the doc-tool pipeline processes a repo, it compares the repo's `AGENTS.md` against our `AGENTS-TEMPLATE.md` and flags deviations (missing recommended sections, non-action-oriented language, etc.) as documentation drift.

This makes the DaC pipeline self-updating with respect to the AGENTS.md standard — we don't just follow it, we actively propagate it.

---

## Consequences

### Positive
- Agents will have structured, predictable context about our project
- Reduced onboarding friction for new AI-assisted contributors
- Alignment with an emerging industry standard (60k+ projects, Linux Foundation-backed)
- Future-proof as more agents adopt the format

### Negative
- Requires ongoing maintenance — stale AGENTS.md is worse than none
- No formal schema means consistency depends on human discipline
- Risk of over-instruction (too much context = token bloat, agent confusion)

### Mitigations
- Review AGENTS.md in every PR that changes build/test/architecture
- Keep it concise: aim for <500 lines at root level
- Use nested AGENTS.md for sub-packages if the project grows

---

## References

- [https://agents.md](https://agents.md) — Official project site
- [https://aaif.io/projects/agents-md/](https://aaif.io/projects/agents-md/) — AAIF project page
- [https://github.com/agentsmd/agents.md](https://github.com/agentsmd/agents.md) — GitHub repo
- [OpenAI Codex AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md) — Real-world example
- [Apache Airflow AGENTS.md](https://github.com/apache/airflow/blob/main/AGENTS.md) — Real-world example
- [Addy Osmani on Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/) — Philosophy

---

## Decision Record

| Date | Event |
|------|-------|
| 2026-04-26 | ADR drafted, proposed for discussion |
| 2026-04-26 | Added Standard-Sync Mechanism: `scripts/sync-agents-standard.py` + `AGENTS-TEMPLATE.md` |

---

## Appendix: Files Introduced by This ADR

| File | Purpose |
|------|---------|
| `docs/ADRs/000-AGENTS-FILE-STANDARD.md` | This decision record |
| `scripts/sync-agents-standard.py` | Fetches upstream AAIF guidance and regenerates `AGENTS-TEMPLATE.md` |
| `AGENTS-TEMPLATE.md` | Canonical reference for pipeline validation of `AGENTS.md` files |
| `.agents-standard-state.json` | Tracks last-sync SHA to avoid redundant updates |
