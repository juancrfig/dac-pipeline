# Repo: NVIDIA/NemoClaw

## Standard Check
- File exist: yes
- Markdown standard: yes
- Imperative language: yes
- Sections: Project Overview, Agent Skills, Architecture, Quick Reference, Key Architecture Decisions, Code Style and Conventions, Git Hooks (prek), Working with This Repo, Documentation, PR Requirements
- Issues:
  - Section names not exactly "Setup", "Testing", "Style" — but content equivalent present (Quick Reference, Testing Strategy, Code Style and Conventions). This is minor deviation, not critical.
  - One command uses `npm link` in install chain which can fail silently on some systems — still copy-pasteable.
  - No "Environment Variables" or "Dependencies" standalone sections — info scattered.

## Accuracy Check

### Claim 1: "`e2e-brev` — `test/e2e/brev-e2e.test.js` — cloud E2E (requires `BREV_API_TOKEN`)"
- Status: false
- Evidence: vitest.config.ts line 45, test/e2e/ directory listing
- Detail: File is `test/e2e/brev-e2e.test.ts` (TypeScript), not `.js`. AGENTS.md says `.js`. Small but real inaccuracy.

### Claim 2: "Coverage thresholds are ratcheted in `ci/coverage-threshold-*.json`"
- Status: true
- Evidence: `ls ci/` shows `coverage-threshold-cli.json`, `coverage-threshold-plugin.json`
- Detail: Files exist exactly as described. Pattern match confirmed.

### Claim 3: "The `.claude/skills` symlink points to `.agents/skills` — both paths resolve to the same content"
- Status: true
- Evidence: `ls -la .claude/` shows `skills -> ../.agents/skills`
- Detail: Symlink exists and resolves correctly. Claim accurate.

### Claim 4: "Follow existing preset structure (see `slack.yaml`, `discord.yaml`)"
- Status: true
- Evidence: `ls nemoclaw-blueprint/policies/presets/` shows `slack.yaml`, `discord.yaml` plus 11 others
- Detail: Both files exist in presets directory. Claim accurate.

### Claim 5: "All hooks managed by prek (installed via `npm install`)"
- Status: true
- Evidence: package.json line 25 shows `prepare` script runs `prek install`; package-lock.json shows `@j178/prek` dependency
- Detail: prek is a devDependency and `npm install` triggers hook setup via `prepare`. Claim accurate.

### Claim 6: "Follow PR template (`.github/PULL_REQUEST_TEMPLATE.md`)"
- Status: true
- Evidence: `.github/PULL_REQUEST_TEMPLATE.md` exists
- Detail: File present at exact path. Claim accurate.

### Claim 7: "`npm run typecheck:cli`" exists as command
- Status: true
- Evidence: package.json line 17 defines `"typecheck:cli": "tsc -p tsconfig.cli.json"`; tsconfig.cli.json exists
- Detail: Command works, config file present. Claim accurate.

### Claim 8: "ESLint config in `eslint.config.mjs`"
- Status: true
- Evidence: `eslint.config.mjs` exists at root and `nemoclaw/eslint.config.mjs` exists
- Detail: Both root and plugin ESLint configs present. Claim accurate.

### Claim 9: "ShellCheck enforced (`.shellcheckrc` at root)"
- Status: true
- Evidence: `.shellcheckrc` exists at root
- Detail: File present. Claim accurate.
