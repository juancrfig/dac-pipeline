# DAC — Docs-as-Code Pipeline

> AI-native documentation that stays true to your codebase.

## Origin Story

This project started with a real problem: we were trying to contribute to [Hermes Agent](https://github.com/NousResearch/hermes-agent), an AI-powered coding assistant framework. The project has a massive developer guide (`AGENTS.md`, ~35k characters) that AI assistants use to understand the codebase. We discovered it was drifting — file references pointed to renamed files, function signatures were stale, and new patterns were undocumented. AI assistants were burning context tokens on wrong assumptions.

We ran experiments on the Hermes codebase to measure the drift. The results were stark: **41% of file references were stale**. We built a prototype drift checker, validated it worked, and realized this problem isn't unique to Hermes — every project using AI assistants faces it.

So we extracted the solution into a standalone tool: **DAC** (Docs-as-Code). A CI pipeline that treats your AI-facing documentation as code — automatically scanned, validated, and kept in sync with your actual codebase.

## The Problem

AI coding assistants (Cursor, Copilot, Claude Code, Hermes) rely on project docs to understand your codebase. But docs drift:

- Files get renamed, docs still reference old paths
- Functions change signatures, examples go stale
- Architecture evolves, diagrams become lies
- After 100 PRs, your AGENTS.md is a minefield of hallucinations

Result: AI agents waste tokens, make wrong assumptions, break your code.

## The Solution

DAC is a CI pipeline that treats docs as code — automatically scanned, validated, and kept in sync with your actual codebase.

### Core Features

| Feature | What it does |
|---------|--------------|
| **Drift Detection** | Scans docs for file/function references, verifies they exist |
| **Signature Sync** | Extracts actual function signatures from AST, compares to docs |
| **Invariant Enforcement** | Maintains a minimal "critical rules" file that never contradicts full docs |
| **Token Budget** | Warns when docs grow too large for AI context windows |
| **PR Gate** | Blocks merges when docs are stale |
| **Auto-Fix (LLM)** | Optional: LLM suggests doc updates based on code diff |

### How It Works

```
Your Repo
├── src/                    # Your code
├── docs/                   # Your documentation
│   └── AGENTS.md          # AI assistant guide
├── .github/
│   └── workflows/
│       └── dac.yml        # DAC CI pipeline
└── dac.config.yaml        # Project-specific rules

On every PR:
  1. Extract all code references from docs
  2. Verify against actual codebase (AST + filesystem)
  3. Check invariant file is subset of full docs
  4. Measure token count
  5. (Optional) LLM analyzes diff, suggests doc updates
  6. Pass/fail with detailed report
```

## Quick Start

### GitHub Action

```yaml
# .github/workflows/dac.yml
name: Docs-as-Code
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: nousresearch/dac@v1
        with:
          docs: "AGENTS.md,README.md,docs/"
          strict: true
          llm-provider: "anthropic"  # optional
```

### CLI

```bash
pip install dac-pipeline

# Check docs for drift
dac check AGENTS.md

# Check with strict mode (fail on warnings)
dac check --strict

# Auto-fix where possible
dac fix AGENTS.md

# Initialize config for your project
dac init
```

## Background & Research

- [Experiments](docs/EXPERIMENTS.md) — Full methodology and raw results from the Hermes audit
- [Architecture](docs/ARCHITECTURE.md) — System design, language support, extension points
- [Configuration](docs/CONFIGURATION.md) — `dac.config.yaml` reference
- [Hackathon Submission](docs/HACKATHON.md) — Why this fits the Hermes Creative Hackathon

## Development

```bash
git clone https://github.com/juancrfig/dac-pipeline
cd dac-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE).

---

Built for the Hermes Agent Creative Hackathon 2026.
