# Configuration Reference

## `dac.config.yaml`

```yaml
# Required: which docs to check
docs:
  main: AGENTS.md           # Primary AI assistant guide
  invariants: INVARIANTS.md  # Minimal critical rules
  paths:
    - "docs/**/*.md"
    - "README.md"
    - "CONTRIBUTING.md"

# Optional: which checks to run
checks:
  file_refs: true           # Verify file references exist
  function_signatures: true # Verify function signatures match
  imports: true             # Verify import paths are valid
  token_count:
    warn: 8000              # Warn when docs exceed this
    fail: 15000             # Fail when docs exceed this

# Optional: LLM integration
llm:
  enabled: true
  provider: anthropic       # or "openai", "local"
  model: claude-sonnet-4
  on_drift: suggest_fixes   # "suggest_fixes" | "auto_pr" | "comment_only"
  api_key: ${ANTHROPIC_API_KEY}  # Env var reference

# Optional: ignore patterns
ignore:
  - "*.template.md"
  - "docs/examples/"
  - "**/*.draft.md"

# Optional: custom rules
rules:
  - name: "no_hardcoded_paths"
    pattern: "~/.hermes"
    severity: error
    message: "Use get_hermes_home() instead of hardcoded paths"

  - name: "env_var_secrets_only"
    pattern: "OPTIONAL_ENV_VARS.*description"
    severity: warning
    message: "Non-secret settings belong in config.yaml, not .env"
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | If LLM enabled | For Claude integration |
| `OPENAI_API_KEY` | If LLM enabled | For GPT integration |
| `DAC_STRICT` | No | Set to "1" for strict mode |

## CLI Flags

```bash
dac check [files...]        # Check specific files
dac check --strict          # Fail on warnings
dac check --fix             # Auto-fix where possible
dac check --json            # Machine-readable output
dac init                    # Create dac.config.yaml
dac init --template python  # Use language-specific template
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All clean |
| 1 | Drift detected |
| 2 | Configuration error |
| 3 | Internal error |
