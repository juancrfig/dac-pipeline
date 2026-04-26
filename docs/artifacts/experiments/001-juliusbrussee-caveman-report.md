# JuliusBrussee/caveman AGENTS.md Contradiction Report

## Caveman say: Me scan repo for AGENTS.md claims vs real code. Find many things.

---

## 1. AGENTS.md File

**AGENTS says this:**
- AGENTS.md exist at root. Point to four skill files:
  - `@./skills/caveman/SKILL.md`
  - `@./skills/caveman-commit/SKILL.md`
  - `@./skills/caveman-review/SKILL.md`
  - `@./caveman-compress/SKILL.md`

**This is what is actually happening:**
- AGENTS.md exist. But it only contain relative `@./` references — no actual instructions for agents. It a pointer file, not real AGENTS.md with dev env tips, testing instructions, code style, PR instructions, architecture overview. Caveman repo AGENTS.md = 4 lines, all `@./` includes.

**Exact location:**
- `AGENTS.md` line 1-4

---

## 2. AAIF Standard Compliance

**AGENTS says this:**
- AGENTS.md should follow AAIF (Agent-Interface Format) standard with sections: Dev environment tips, Testing instructions, Code style, PR instructions, Architecture overview, Changelog.

**This is what is actually happening:**
- No AAIF compliance. No dev env tips, no testing instructions, no code style, no PR instructions, no architecture overview in AGENTS.md. Only `@./` includes. Caveman repo use `CLAUDE.md` and `CLAUDE.original.md` as main agent instruction files — not AGENTS.md.

**Exact location:**
- `AGENTS.md` — entire file (4 lines)
- `CLAUDE.md` line 1-215 — this is where actual agent instructions live

---

## 3. Package.json / pyproject.toml / Makefile

**AGENTS says this:**
- Most repos have package.json, pyproject.toml, or Makefile for build/test.

**This is what is actually happening:**
- No package.json at root. No pyproject.toml at root. No Makefile at root. Repo is markdown + JS + Python scripts. No centralized build manifest. `caveman-compress/scripts/` have Python code but no pyproject.toml or setup.py. `hooks/` have JS but no package.json at root (only a `hooks/package.json` with `{"type":"commonjs"}` marker).

**Exact location:**
- Root directory — missing package.json, pyproject.toml, Makefile
- `hooks/package.json` line 1 — only `{"type": "commonjs"}` marker, not real package manifest

---

## 4. SKILL.md Claims vs Code

### 4a. caveman-compress Process Claims

**AGENTS says this (via `caveman-compress/SKILL.md`):**
- "The CLI will: detect file type (no tokens), call Claude to compress, validate output (no tokens), if errors: cherry-pick fix with Claude (targeted fixes only, no recompression), retry up to 2 times, if still failing after 2 retries: report error to user, leave original file untouched"

**This is what is actually happening:**
- `caveman-compress/scripts/compress.py` does call Claude (via `call_claude()`), validate (via `validate.validate()`), retry up to 2 times, and restore original on failure. BUT: `call_claude()` uses `ANTHROPIC_API_KEY` env var + `claude-sonnet-4-5` model by default. It DOES consume tokens for compression and fix. SKILL.md claim "no tokens" for detect and validate is misleading — detect/validate are local code, but compression itself uses API tokens.

**Exact location:**
- `caveman-compress/SKILL.md` line 29-35
- `caveman-compress/scripts/compress.py` line 75-101 (`call_claude()`), line 155-227 (`compress_file()`)

### 4b. caveman-commit Conventional Commits Types

**AGENTS says this (via `skills/caveman-commit/SKILL.md`):**
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`

**This is what is actually happening:**
- Types list match Conventional Commits spec. No contradiction.

**Exact location:**
- `skills/caveman-commit/SKILL.md` line 16

### 4c. caveman-review Severity Prefixes

**AGENTS says this (via `skills/caveman-review/SKILL.md`):**
- `🔴 bug:`, `🟡 risk:`, `🔵 nit:`, `❓ q:`

**This is what is actually happening:**
- `commands/caveman-review.toml` prompt say: "Severity: bug, risk, nit, q. Skip praise. Skip obvious. If code look good, say 'LGTM' and stop." — matches SKILL.md. No contradiction.

**Exact location:**
- `skills/caveman-review/SKILL.md` line 16-20
- `commands/caveman-review.toml` line 2

---

## 5. README Claims vs Code

### 5a. Install Command for Claude Code

**AGENTS says this (via README.md):**
- "Claude Code | `claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman`"

**This is what is actually happening:**
- Command look plausible but `claude plugin install caveman@caveman` syntax is unusual (plugin@namespace?). No way to verify without running. README claim it work — cannot confirm from code alone.

**Exact location:**
- `README.md` line 136

### 5b. Benchmark Numbers

**AGENTS says this (via README.md):**
- "Average 1214 normal tokens → 294 caveman tokens = 65% savings"
- "caveman-compress saves 46% input tokens on average"

**This is what is actually happening:**
- `benchmarks/` and `evals/` directories exist with scripts (`run.py`, `llm_run.py`, `measure.py`). README say numbers from real runs. Cannot verify without running benchmarks, but code structure supports claim. No obvious contradiction.

**Exact location:**
- `README.md` line 371-388 (benchmarks table)
- `README.md` line 358-365 (compress table)

### 5c. Codex Auto-Activation

**AGENTS says this (via README.md):**
- "Codex uses `$caveman` syntax, not `/caveman`. This repo ships `.codex/hooks.json`, so caveman auto-starts when you run Codex inside this repo."

**This is what is actually happening:**
- `.codex/hooks.json` exists and has SessionStart hook with caveman activation command. `.codex/config.toml` has `codex_hooks = true`. But the hook command is just an `echo` of caveman rules — it does not load SKILL.md. It a basic echo, not full skill integration.

**Exact location:**
- `.codex/hooks.json` line 1-17
- `.codex/config.toml` line 1-2

---

## 6. Hook System Claims vs Code

### 6a. SessionStart Hook Behavior

**AGENTS says this (via `CLAUDE.md`):**
- "`hooks/caveman-activate.js` — SessionStart hook: Writes the active mode to `$CLAUDE_CONFIG_DIR/.caveman-active` via `safeWriteFlag` (creates if missing). Emits caveman ruleset as hidden stdout. Checks `settings.json` for statusline config; if missing, appends nudge."

**This is what is actually happening:**
- `caveman-activate.js` does all three things. It uses `safeWriteFlag()` from `caveman-config.js`. It reads `skills/caveman/SKILL.md` at runtime and filters to active level. It checks for statusline and nudges if missing. Matches claim.

**Exact location:**
- `hooks/caveman-activate.js` line 1-143

### 6b. safeWriteFlag Security Claims

**AGENTS says this (via `CLAUDE.md`):**
- "`safeWriteFlag()` — symlink-safe flag write. Refuses if flag target or its immediate parent is a symlink. Opens with `O_NOFOLLOW` where supported. Atomic temp + rename. Creates with `0600`."

**This is what is actually happening:**
- `caveman-config.js` `safeWriteFlag()` does refuse symlink at target and immediate parent. Uses `O_NOFOLLOW`. Atomic temp+rename. `0o600` permissions. Matches claim.

**Exact location:**
- `hooks/caveman-config.js` line 73-107

### 6c. Mode Tracker Natural Language Activation

**AGENTS says this (via `CLAUDE.md`):**
- "`hooks/caveman-mode-tracker.js` — UserPromptSubmit hook: Matches phrases like 'activate caveman', 'turn on caveman mode', 'talk like caveman' and writes the configured default mode. Matches 'stop caveman', 'disable caveman', 'normal mode', 'deactivate caveman' etc. and deletes the flag file."

**This is what is actually happening:**
- `caveman-mode-tracker.js` has regex for natural language activation and deactivation. It writes default mode on activation phrases. It deletes flag on deactivation phrases. Matches claim.

**Exact location:**
- `hooks/caveman-mode-tracker.js` line 23-31, 64-68

---

## 7. caveman-compress Code Issues

### 7a. Syntax Error in compress.py

**AGENTS says this:**
- `caveman-compress/scripts/compress.py` should be valid Python.

**This is what is actually happening:**
- Line 40 has syntax error: `SENSITIVE_NAME_TOKENS=***` — this is NOT valid Python. Should be `SENSITIVE_NAME_TOKENS = frozenset({...})` or similar. The `***` is invalid syntax. This file would fail to import.

**Exact location:**
- `caveman-compress/scripts/compress.py` line 40

### 7b. Missing Requirements / Dependencies

**AGENTS says this:**
- `caveman-compress` requires Python 3.10+.

**This is what is actually happening:**
- No `requirements.txt`, `pyproject.toml`, or `setup.py` in `caveman-compress/`. The script imports `anthropic` optionally (falls back to CLI). No dependency manifest. User must manually install `anthropic` if they want API mode.

**Exact location:**
- `caveman-compress/` directory — no requirements.txt or pyproject.toml
- `caveman-compress/scripts/compress.py` line 79 (`import anthropic` inside try/except)

---

## 8. CI Sync Workflow Claims vs Code

### 8a. Sync Triggers

**AGENTS says this (via `CLAUDE.md`):**
- "`.github/workflows/sync-skill.yml` triggers on main push when `skills/caveman/SKILL.md` or `rules/caveman-activate.md` changes."

**This is what is actually happening:**
- `sync-skill.yml` triggers on `skills/caveman/SKILL.md`, `rules/caveman-activate.md`, `caveman-compress/SKILL.md`, AND `caveman-compress/scripts/**`. CLAUDE.md omits compress triggers.

**Exact location:**
- `.github/workflows/sync-skill.yml` line 7-10
- `CLAUDE.md` line 58

### 8b. Sync Outputs

**AGENTS says this (via `CLAUDE.md`):**
- "Copies `skills/caveman/SKILL.md` to all agent-specific SKILL.md locations. Rebuilds `caveman.skill` as ZIP. Rebuilds all agent rule files. Commits with `[skip ci]`."

**This is what is actually happening:**
- Workflow also syncs `caveman-compress/SKILL.md` to `skills/compress/SKILL.md` and `plugins/caveman/skills/compress/SKILL.md`, patches names and paths with `sed`, copies scripts. CLAUDE.md does not mention compress sync.

**Exact location:**
- `.github/workflows/sync-skill.yml` line 40-61
- `CLAUDE.md` line 59-65

---

## 9. Test Coverage

**AGENTS says this:**
- `tests/` directory has tests.

**This is what is actually happening:**
- `tests/test_hooks.py` has unit tests for hook install/upgrade/uninstall. `tests/verify_repo.py` has integration checks. But `tests/caveman-compress/` only has fixture files (original + compressed markdown pairs), no actual Python unit tests for compress/validate/detect logic. The `verify_repo.py` does test compress CLI skip/error paths and fixture validation, but no dedicated test file for compress modules.

**Exact location:**
- `tests/test_hooks.py` line 1-161
- `tests/verify_repo.py` line 1-342
- `tests/caveman-compress/` — only `.md` and `.original.md` fixtures, no `.py` tests

---

## 10. Missing Files Referenced in Code

**AGENTS says this:**
- Code references files that should exist.

**This is what is actually happening:**
- `caveman-activate.js` references `skills/caveman/SKILL.md` at `path.join(__dirname, '..', 'skills', 'caveman', 'SKILL.md')`. For standalone installs (hooks copied to `~/.claude/hooks/`), this path resolves to `~/.claude/skills/caveman/SKILL.md` which does NOT exist. The code has a try/catch fallback to hardcoded rules, but the comment says "Reads SKILL.md at runtime so edits to the source of truth propagate automatically — no hardcoded duplication to go stale." — yet standalone installs will always use stale hardcoded fallback.

**Exact location:**
- `hooks/caveman-activate.js` line 54-58, 92-110

---

## Summary

| # | Issue | Severity |
|---|-------|----------|
| 1 | AGENTS.md is pointer file, not real AAIF-compliant AGENTS.md | Medium |
| 2 | No AAIF standard compliance (no dev env, testing, style, PR, architecture sections) | Medium |
| 3 | No package.json/pyproject.toml/Makefile at root | Low |
| 4 | caveman-compress SKILL.md says "no tokens" for detect/validate — technically true but misleading since compression uses tokens | Low |
| 5 | `compress.py` line 40 has `***` syntax error — invalid Python | **High** |
| 6 | No dependency manifest for caveman-compress | Low |
| 7 | CI sync workflow triggers include compress paths not documented in CLAUDE.md | Low |
| 8 | Standalone hook installs cannot find SKILL.md, always use stale fallback | Medium |
| 9 | No dedicated Python unit tests for compress/validate/detect modules | Low |

**Caveman brain still big. But code have rock in shoe.**
