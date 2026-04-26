# Repo: anomalyco/opencode

## Standard Check
- File exist: yes (root AGENTS.md found)
- Markdown standard: yes (standard Markdown, no proprietary syntax)
- Imperative language: yes (action-oriented bullets and instructions)
- Sections found: Style Guide (General Principles, Destructuring, Variables, Control Flow, Schema Definitions), Testing, Type Checking
- Issues:
  - No explicit "Setup" section
  - No explicit "Testing" section beyond a short bullet list (only 3 bullets)
  - No "Architecture" or "Dependencies" sections
  - Contains repo-specific shorthand (e.g. "guard: `do-not-run-tests-from-root`") without explanation
  - Top bullets are plain sentences, not all imperative (e.g. "The default branch in this repo is `dev`.")

## Accuracy Check

### Claim 1: "To regenerate the JavaScript SDK, run `./packages/sdk/js/script/build.ts`."
- Status: true
- Evidence: `packages/sdk/js/script/build.ts` exists and is executable Bun script
- Detail: File present at exact path. Starts with `#!/usr/bin/env bun` and changes into its own package dir. Command is copy-pasteable from repo root.

### Claim 2: "Tests cannot run from repo root (guard: `do-not-run-tests-from-root`); run from package dirs like `packages/opencode`."
- Status: true
- Evidence: `bunfig.toml` line 5: `root = "./do-not-run-tests-from-root"`
- Detail: The guard file mechanism is real. Bun test root is pointed to a non-existent directory to prevent accidental root-level test runs. Confirmed by `bunfig.toml`.

### Claim 3: "Always run `bun typecheck` from package directories (e.g., `packages/opencode`), never `tsc` directly."
- Status: stale / partially false
- Evidence: `packages/opencode/package.json` line 10: `"typecheck": "tsgo --noEmit"`
- Detail: The command `bun typecheck` in `packages/opencode` does NOT run `tsc`; it runs `tsgo --noEmit`. The AGENTS.md warns against `tsc` but the actual tool in use is `tsgo` (TypeScript Go native preview), not `tsc`. The instruction is misleading about what command executes under the hood.

### Claim 4: "In `src/config`, follow the existing self-export pattern at the top of the file (for example `export * as ConfigAgent from "./agent"`) when adding a new config module."
- Status: true
- Evidence: `packages/opencode/src/config/agent.ts` line 1: `export * as ConfigAgent from "./agent"`
- Detail: Pattern is consistently applied across all config modules (agent, command, config, error, formatter, keybinds, layout, lsp, managed, markdown, mcp, model-id, parse, paths, permission, plugin, provider, server, skills, variable). Each file has `export * as ConfigX from "./x"` at the top.

### Claim 5: "The default branch in this repo is `dev`."
- Status: true
- Evidence: `git log` shows `HEAD -> dev` and `origin/HEAD -> origin/dev`
- Detail: Local checkout is on `dev`, and remote HEAD points to `dev`. No local `main` branch exists. Claim is accurate.
