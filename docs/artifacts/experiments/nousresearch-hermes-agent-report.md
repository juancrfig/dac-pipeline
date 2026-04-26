# Repo: NousResearch/hermes-agent

## Standard Check
- File exist: yes
- Markdown standard: yes
- Imperative language: yes
- Sections: Development Environment, Project Structure, File Dependency Chain, AIAgent Class, CLI Architecture, TUI Architecture, Adding New Tools, Adding Configuration, Skin/Theme System, Plugins, Skills, Important Policies, Profiles: Multi-Instance Support, Known Pitfalls, Testing
- Issues:
  - No explicit "Setup" section ("Development Environment" covers it)
  - No explicit "Style" section (covered under "Known Pitfalls" and inline rules)
  - Contains future-dated claim: "Rule (Teknium, May 2026)" — document dated Apr 2026 references May 2026
  - Very long file (~35K chars) — some sections are dense; could benefit from a table of contents
  - Commands are exact and copy-pasteable

## Accuracy Check

### Claim 1: "`scripts/run_tests.sh` probes `.venv` first, then `venv`, then `$HOME/.hermes/hermes-agent/venv`"
- Status: true
- Evidence: `scripts/run_tests.sh` exists and `grep -n "venv\|\.venv" scripts/run_tests.sh` shows probing logic
- Detail: Script exists at repo root and implements the described venv probing.

### Claim 2: "`run_agent.py` # AIAgent class — core conversation loop (~12k LOC)"
- Status: true
- Evidence: `wc -l run_agent.py` → 12838 lines
- Detail: File is 12,838 lines, matching the ~12k LOC claim.

### Claim 3: "`cli.py` # HermesCLI class — interactive CLI orchestrator (~11k LOC)"
- Status: true
- Evidence: `wc -l cli.py` → 11060 lines
- Detail: File is 11,060 lines, matching the ~11k LOC claim.

### Claim 4: "Tests: Pytest suite (~15k tests across ~700 files as of Apr 2026)"
- Status: true
- Evidence: `find tests -type f | wc -l` → 779 files; `grep -r "def test_" tests/ | wc -l` → 15,609 test definitions
- Detail: 779 total files under `tests/`, ~754 test files, and ~15,609 `def test_*` definitions. The ~15k tests / ~700 files claim is accurate.

### Claim 5: "`model_tools.py` # Tool orchestration, `discover_builtin_tools()`, `handle_function_call()`"
- Status: true
- Evidence: `grep -n "def handle_function_call" model_tools.py` → line 494; `grep -n "discover_builtin_tools" model_tools.py` → imported from `tools/registry.py` and called at line 139
- Detail: Both functions exist. `handle_function_call` is defined in `model_tools.py`. `discover_builtin_tools` is defined in `tools/registry.py` and imported/called from `model_tools.py`.

### Claim 6: "`ui-tui/` # Ink (React) terminal UI — `hermes --tui`" and "`tui_gateway/` # Python JSON-RPC backend for the TUI"
- Status: true
- Evidence: `ls -la | grep ui-tui` and `ls -la | grep tui_gateway` both return directories; `grep -r "hermes --tui" .` returns 38 matches across code and docs
- Detail: Both directories exist. The `hermes --tui` command is referenced throughout the codebase, release notes, and web server code.

### Claim 7: "The dashboard embeds the real `hermes --tui` — not a rewrite. See `hermes_cli/pty_bridge.py` + the `@app.websocket(\"/api/pty\")` endpoint in `hermes_cli/web_server.py`."
- Status: true
- Evidence: `hermes_cli/pty_bridge.py` exists; `grep -n '@app.websocket("/api/pty")' hermes_cli/web_server.py` → line 2379
- Detail: Both files exist and the WebSocket endpoint is present exactly as described.

### Claim 8: "`hermes_cli/curses_ui.py` — see `hermes_cli/tools_config.py` for the canonical pattern."
- Status: true
- Evidence: `hermes_cli/curses_ui.py` exists; `hermes_cli/tools_config.py` exists and imports/uses curses UI
- Detail: Both files exist. The curses UI module is real and used as the preferred alternative to `simple_term_menu`.

### Claim 9: "`_apply_profile_override()` in `hermes_cli/main.py` sets `HERMES_HOME` before any module imports."
- Status: true
- Evidence: `grep -n "def _apply_profile_override" hermes_cli/main.py` → line 99
- Detail: Function exists in `hermes_cli/main.py`.

### Claim 10: "`_get_profiles_root()` returns `Path.home() / \".hermes\" / \"profiles\"`, NOT `get_hermes_home() / \"profiles\"`."
- Status: true
- Evidence: `grep -n "def _get_profiles_root" hermes_cli/profiles.py` → line 120
- Detail: Function exists in `hermes_cli/profiles.py` (not `main.py` as the AGENTS.md text might loosely imply), and its implementation returns `Path.home() / ".hermes" / "profiles"`.

### Claim 11: "Agent loop: `response = client.chat.completions.create(model=model, messages=messages, tools=tool_schemas)`"
- Status: false
- Evidence: `grep -n "client.chat.completions.create" run_agent.py` returns no direct match in the main loop; actual API calls use `self._ensure_primary_openai_client(...).chat.completions.create(...)` or `active_client.responses.create(...)` or `_anthropic_messages_create(...)`
- Detail: The AGENTS.md presents a highly simplified pseudocode loop. The real loop (starting ~line 9563) does not contain the exact `client.chat.completions.create(model=model, messages=messages, tools=tool_schemas)` line. It uses internal client wrappers, budget consumption, checkpointing, and multiple provider paths. The pseudocode is architecturally representative but not literally copy-pasteable as real code.

### Claim 12: "`AIAgent.__init__` takes ~60 parameters"
- Status: true
- Evidence: `grep -n "def __init__" run_agent.py` → line 833; counting parameters from `base_url` through `pass_session_id` yields ~62 named parameters
- Detail: The real `__init__` signature has approximately 62 parameters, matching the "~60" claim.

### Claim 13: "`tests/conftest.py` also enforces points 1-4 as an autouse fixture so ANY pytest invocation gets hermetic behavior"
- Status: true
- Evidence: `tests/conftest.py` exists; `grep -n "_isolate_hermes_home" tests/conftest.py` → line 281 defines the fixture
- Detail: The autouse fixture exists and redirects `HERMES_HOME` to a temp dir.

### Claim 14: "`hermes_cli/commands.py` — central `COMMAND_REGISTRY` list of `CommandDef` objects"
- Status: true
- Evidence: `grep -n "COMMAND_REGISTRY" hermes_cli/commands.py` → multiple matches; `grep -n "CommandDef" hermes_cli/commands.py` → multiple matches
- Detail: File exists and contains `COMMAND_REGISTRY` and `CommandDef` exactly as described.

### Claim 15: "`hermes_cli/skin_engine.py` — data-driven CLI theming"
- Status: true
- Evidence: `hermes_cli/skin_engine.py` exists; `grep -n "SkinConfig" hermes_cli/skin_engine.py` → matches
- Detail: File exists and implements the skin engine with `SkinConfig` dataclass and built-in skins (`default`, `ares`, `mono`, `slate`).

## Summary
- 15 claims checked
- 14 true, 1 false (the simplified agent-loop pseudocode is not literal code)
- No stale file paths or missing commands found
- The AGENTS.md is remarkably accurate and well-maintained for a repo of this size
- Minor issue: the pseudocode loop in Claim 11 is architecturally correct but not literal; it should perhaps be labeled as pseudocode
