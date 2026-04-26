# AAIF Standard — Agent Quick Reference

## What This Is

This doc tells agents how to write AGENTS.md files. It follows the Agentic AI Foundation (AAIF) standard. Source: https://github.com/agentsmd/agents.md

## Required Sections

An AGENTS.md file MUST have these sections. Order is flexible.

1. **Setup commands** — How to install deps and start the project.
2. **Testing instructions** — How to run tests. Single tests too.
3. **Code style** — Linter, formatter, naming rules.
4. **PR instructions** — Title format, pre-commit checks.

Optional but recommended:

5. **Architecture overview** — Key dirs, entry points, data flow.
6. **Common tasks** — Steps for frequent operations.
7. **Debugging tips** — How to trace errors, find logs.
8. **Security notes** — Secrets handling, auth rules.

## Format Rules

- Use Markdown. No proprietary syntax.
- File lives at repo root. Name is `AGENTS.md`.
- Keep it under 200 lines.
- Update every 90 days max.

## Writing Rules (Caveman Style)

- Short sentences. Max 15 words.
- One idea per sentence.
- No filler words: "basically", "essentially", "in order to".
- No passive voice. Say WHO does WHAT.
- Command form: "Run tests." Not "You should run tests."
- Use bullets. No prose paragraphs.
- Quantify: "Max 500 lines." Not "Keep files small."
- No hedging: "Always X." Not "Prefer X when possible."
- No markdown tables.
- No emojis.
- No "please", "kindly", "thank you".
- Max 10 bullets per section.
- Start with the instruction. No preamble.

## Example (Good)

```markdown
# AGENTS.md

## Setup commands
- Install deps: `pip install -r requirements.txt`
- Start server: `python manage.py runserver`

## Testing instructions
- Run all tests: `pytest`
- Run single test: `pytest tests/test_example.py::TestClass::test_method`
- All commits must pass CI before merge.

## Code style
- Use project's configured linter and formatter.
- Follow existing naming conventions.

## PR instructions
- Title format: `[<scope>] <description>`
- Run lint and tests before commit.
```

## Example (Bad)

```markdown
# AGENTS.md

## Introduction and Overview

This document serves as the comprehensive guide for all AI agents interacting with this codebase. It is extremely important that all agents read this document carefully before attempting any modifications...
```

## Validation Checklist

- [ ] File exists at repo root.
- [ ] Uses standard Markdown.
- [ ] Has at least 4 required sections.
- [ ] Instructions are imperative.
- [ ] Commands are exact and copy-pasteable.
- [ ] No placeholder text left unmodified.
- [ ] Updated within last 90 days.
- [ ] Follows caveman style rules above.

## Links

- AAIF Project: https://github.com/agentsmd/agents.md
- AAIF Website: https://aaif.io/
- This Pipeline: https://github.com/juancrfig/dac-pipeline
