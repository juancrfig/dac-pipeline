# [dac-pipeline] AGENTS.md

## Dev environment tips
- Run tests.
- Install deps: `pip install -e '.[dev]'`.
- Install with LLM support: `pip install -e '.[dev,llm]'`.
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
- Update AGENTS.md if build or test steps change.
- Add `#agents-md-override` in PR description to skip validation.

## Architecture overview
- `dac/` is main package.
- Contains core module.
- Contains cli module.
- Contains llm_bridge module.
- `scripts/` has standalone scripts.
- Includes `sync-agents-standard.py`.
- Includes `validate-agents-md.py`.
- `tests/` is test suite.
- `docs/` has ADRs, architecture docs, experiments.
- `docs/ADRs/` has decision records: 000, 002, 003.

## Architecture overview (continued)
- CLI entry point is `dac`.
- Maps to `dac.cli:main`.
- Uses tree-sitter for AST parsing across Python, JS, TS, Go.

## Changelog

- `251d980b` — Auto-synced from upstream `agentsmd/agents.md`
- Fix install commands; replace `uv` with `pip` in AGENTS.md.
