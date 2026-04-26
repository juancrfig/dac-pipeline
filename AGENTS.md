# [dac-pipeline] AGENTS.md

## Dev environment tips
- Run tests.
- Install dependencies: `uv pip install -e ".[dev]"`.
- Install with LLM support: `uv pip install -e ".[dev,llm]"`.
- Use Python 3.10 or newer.
- Build backend: hatchling.

## Testing instructions
- Run tests: `pytest`.
- Run with coverage: `pytest --cov=dac`.
- Run a single test: `pytest tests/test_file.py::TestClass::test_method -xvs`.
- CI runs tests before merge.

## Code style
- Format code: `black dac/ scripts/ tests/`.
- Lint code: `ruff check dac/ scripts/ tests/`.
- Type check: `mypy dac/`.
- Max line length: 100 characters.
- Target Python version: 3.10.

## PR instructions
- Title format: `[<scope>] <description>`.
- Run lint and tests before commit.
- Update AGENTS.md when build or test steps change.
- Add `#agents-md-override` in PR description to skip validation.

## Architecture overview
- `dac/` is the main package.
- It contains core modules.
- It contains cli module.
- It contains llm_bridge module.
- `scripts/` is a directory of standalone scripts.
- It includes `sync-agents-standard.py`.
- It includes `validate-agents-md.py`.
- `tests/` is the test suite.
- `docs/` contains ADRs, architecture docs, experiments.
- `docs/ADRs/` contains Decision records: 000, 002, 003.
- CLI entry point is `dac`.
- It maps to `dac.cli:main`.
- It uses tree-sitter for AST parsing across Python, JS, TS, Go.

## Common tasks
- Sync standard from upstream: `python scripts/sync-agents-standard.py`.
- Sync with LLM extraction: `python scripts/sync-agents-standard.py --llm`.
- Validate AGENTS.md: `python scripts/validate-agents-md.py --agents-md AGENTS.md`.
- Run CI workflows locally with `act`.
- Push to a test branch for CI validation.
- Update AAIF reference: `python scripts/update-standard-reference.py`.

## Changelog
- `20260426` — Caveman rewrite to AAIF standard.
- `251d980b` — Auto-synced from upstream `agentsmd/agents.md`
