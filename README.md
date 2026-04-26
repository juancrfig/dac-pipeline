# DAC — Docs-as-Code Pipeline

> AI-native documentation that stays true to your codebase.

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

## Configuration

```yaml
# dac.config.yaml
docs:
  main: AGENTS.md
  invariants: HERMES_INVARIANTS.md
  paths:
    - "docs/**/*.md"
    - "README.md"

checks:
  file_refs: true
  function_signatures: true
  imports: true
  token_count:
    warn: 8000
    fail: 15000

llm:
  enabled: true
  provider: anthropic
  model: claude-sonnet-4
  on_drift: suggest_fixes  # or "auto_pr"

ignore:
  - "*.template.md"
  - "docs/examples/"
```

## Language Support

| Language | File refs | Function sigs | Imports | AST parser |
|----------|-----------|---------------|---------|------------|
| Python | ✅ | ✅ | ✅ | Built-in |
| TypeScript | ✅ | ✅ | ✅ | Tree-sitter |
| JavaScript | ✅ | ✅ | ✅ | Tree-sitter |
| Go | ✅ | ✅ | ✅ | Tree-sitter |
| Rust | ✅ | 🚧 | 🚧 | Tree-sitter |
| Ruby | ✅ | 🚧 | 🚧 | Tree-sitter |

## The Creative Angle (Hackathon)

DAC enables creative coding with AI by removing the friction:

- **Game dev**: AI agents understand your engine architecture without reading 10k lines
- **Generative art**: Docs stay synced with your p5.js/Three.js pipeline
- **Audio tools**: Function references in docs always match your DSP code
- **Interactive media**: Architecture diagrams auto-update when you refactor

Less time fixing AI mistakes → more time creating.

## Architecture

```
dac-pipeline/
├── cli/                    # `dac check`, `dac fix`, `dac init`
├── core/
│   ├── extractors/        # Parse docs for code references
│   ├── validators/        # Verify against codebase
│   ├── reporters/         # Markdown, JSON, GitHub comments
│   └── ast_parsers/       # Language-specific parsers
├── llm_bridge/            # Optional LLM integration
│   ├── prompts/           # Drift analysis prompts
│   └── providers/         # OpenAI, Anthropic, local
├── github-action/         # action.yml + Dockerfile
└── presets/               # Templates for different project types
    ├── python-lib.md.hbs
    ├── react-app.md.hbs
    ├── rust-cli.md.hbs
    └── hermes-agent.md.hbs
```

## Development

```bash
git clone https://github.com/nousresearch/dac-pipeline
cd dac-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT — use it, fork it, build on it.

---

Built for the Hermes Agent Creative Hackathon 2026.
