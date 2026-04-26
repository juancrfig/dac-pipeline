# ADR 002: Caveman Style for Agent-Facing Documentation

**Status:** Proposed  
**Date:** 2026-04-26  
**Author:** dac-pipeline maintainers  
**Stakeholders:** AI coding agents, human contributors, doc-tool pipeline  

---

## Context

We have decided to adopt the AGENTS.md standard (ADR-000) as the canonical format for providing AI coding agents with project context. The standard intentionally uses plain Markdown with no rigid schema, which means the *quality* of the content depends heavily on how it is written.

Recent research and community experiments have demonstrated that **ultra-compressed, imperative communication** — colloquially called "caveman style" — significantly improves agent comprehension, instruction-following accuracy, and token efficiency.

## Decision

All **agent-facing documentation** in this project — specifically `AGENTS.md`, `AGENTS-TEMPLATE.md`, and any future files consumed by AI coding agents — will be written in **caveman style**.

Human-facing documents (ADRs, README.md, architecture docs) remain in standard prose. This ADR applies only to files whose primary audience is AI agents.

---

## What is Caveman Style?

Caveman style is a writing discipline that maximizes information density while preserving technical precision. It is not broken English — it is *intentionally compressed* English.

### Rules

| Drop | Keep |
|------|------|
| Articles (`a`, `an`, `the`) | Technical terms (exact) |
| Filler (`just`, `really`, `basically`, `actually`, `simply`) | Imperative verbs |
| Pleasantries (`sure`, `certainly`, `of course`, `happy to`) | Code blocks (unchanged) |
| Hedging (`might`, `should`, `consider`, `perhaps`) | Error quotes (exact) |
| Long conjunctions | Short synonyms (`fix` not `implement a solution for`) |

### Pattern

```
[thing] [action] [reason]. [next step].
```

### Examples

**Normal prose:**
> "You should always run the full test suite before committing any changes to the repository. This ensures that no regressions are introduced."

**Caveman style:**
> "Run full tests before commit. No regressions."

**Normal prose:**
> "If Docker networking fails, you should run `docker network prune` first and then retry the command."

**Caveman style:**
> "Docker net fail -> `docker network prune`. Retry."

**Normal prose:**
> "The agent will attempt to execute relevant programmatic checks and fix any failures before finishing the task."

**Caveman style:**
> "Agent runs checks. Fixes failures. Then done."

---

## Evidence

### 1. Caveman Prompting Repository

The **Caveman Prompting** project by Julius Brussee provides a systematic exploration of compressed prompting:

- **Repository:** [https://github.com/JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman)
- **Core claim:** Dropping filler, articles, and hedging while keeping technical terms exact improves agent task completion rates.
- **Mechanism:** Reduced token count leaves more context window for code. Imperative structure aligns with how agents parse instructions.

### 2. Academic Paper (arXiv)

- **Paper:** [https://arxiv.org/html/2604.00025v1](https://arxiv.org/html/2604.00025v1)
- **Finding:** Quantitative evidence that compressed prompts reduce hallucination and improve instruction-following accuracy in large language models.
- **Key insight:** Agents parse atomic, imperative statements more reliably than descriptive prose. Every token saved in the prompt = more room for code context in the agent's working memory.

### 3. Hermes Agent Skill

The caveman style is formally recognized as a skill in the Hermes Agent ecosystem:

- **Skill:** `caveman` — "Ultra-compressed communication mode. Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accuracy."
- **Trigger:** Activated when user says "caveman mode", "talk like caveman", "use caveman", "less tokens", "be brief", or invokes `/caveman`.
- **Persistence:** Once triggered, stays active across all subsequent responses until explicitly disabled.

---

## Why This Matters for AGENTS.md

1. **Token efficiency** — Agents have finite context windows. A 500-line AGENTS.md in caveman style may use ~40% fewer tokens than the same content in standard prose. Those tokens are available for code context instead.

2. **Reduced ambiguity** — "Should run tests" leaves room for interpretation. "Run tests" is a command. Agents follow commands more reliably than suggestions.

3. **Faster parsing** — Imperative, atomic statements are easier for agents to segment and act upon. Descriptive prose requires an extra inference step: "What does the human want me to *do*?"

4. **Consistency with the standard** — The AAIF AGENTS.md standard already recommends action-oriented language. Caveman style is the logical extreme of that recommendation.

---

## Scope

### In Scope (Caveman Style Required)

| File | Audience |
|------|----------|
| `AGENTS.md` (root and nested) | AI coding agents |
| `AGENTS-TEMPLATE.md` | AI coding agents + pipeline validator |
| LLM validation prompts | The validation LLM itself |
| Any future `.agent-*` files | AI coding agents |

### Out of Scope (Standard Prose)

| File | Audience |
|------|----------|
| `docs/ADRs/*.md` | Human architects |
| `README.md` | Human contributors |
| `docs/ARCHITECTURE.md` | Human contributors |
| `docs/CONFIGURATION.md` | Human operators |

---

## Consequences

### Positive
- Improved agent comprehension and task completion rates
- Reduced token usage in agent context windows
- Faster agent response times (less text to process)
- Alignment with emerging best practices in prompt engineering

### Negative
- Steep learning curve for human contributors writing agent-facing docs
- Risk of over-compression leading to ambiguity
- Code review friction: humans may instinctively "correct" caveman style
- Requires discipline to keep technical terms exact while compressing everything else

### Mitigations
- Provide the examples in this ADR as a style guide
- Add a CI check that flags non-caveman patterns in AGENTS.md files
- Train reviewers: caveman is intentional, not a mistake
- Use the LLM validation prompt (ADR-003) to enforce caveman style automatically

---

## Validation

We will know this decision is correct if:
- Agent-generated PRs from repos with caveman-style AGENTS.md have fewer iterations
- Agent task completion rates improve (measured via success/failure logs)
- Token usage in agent sessions decreases (measured via API billing)

---

## References

- [Caveman Prompting Repository](https://github.com/JuliusBrussee/caveman) — Julius Brussee
- [arXiv Paper 2604.00025v1](https://arxiv.org/html/2604.00025v1) — Academic evidence for compressed prompting
- [Hermes Agent Caveman Skill](caveman/SKILL.md) — Formal skill definition
- [ADR-000: AGENTS.md Standard Adoption](000-AGENTS-FILE-STANDARD.md) — Parent decision

---

## Decision Record

| Date | Event |
|------|-------|
| 2026-04-26 | ADR drafted, proposed for discussion |
