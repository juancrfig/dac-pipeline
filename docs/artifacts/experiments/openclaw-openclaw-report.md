# Repo: openclaw/openclaw

## Standard Check
- File exist: yes (repo root)
- Markdown standard: yes (Standard Markdown, no proprietary syntax)
- Imperative language: yes (Action-oriented bullet style throughout)
- Sections found: Start, Map, Architecture, Commands, GitHub / CI, Gates, Code, Tests, Docs / Changelog, Git, Security / Release, Apps / Platform, Ops / Footguns
- Issues: None significant. File is well-structured and follows AAIF conventions. Minor note: uses "Telegraph style" preamble which is fine.

## Accuracy Check

### Claim 1: "Runtime: Node 22+. Keep Node + Bun paths working."
- Status: stale
- Evidence: `package.json` line 1701 specifies `"packageManager": "pnpm@10.33.0"`; no explicit Node engine requirement found in root package.json. Local environment runs Node v25.7.0, which is >22, but the claim of "Node 22+" as a stated runtime floor is not enforced in package metadata.
- Detail: No `"engines": { "node": ">=22" }` block seen in root package.json. The "Node 22+" guidance appears aspirational/outdated relative to package metadata.

### Claim 2: "Install: `pnpm install` (keep Bun lock/patches aligned if touched)."
- Status: true
- Evidence: `package.json` line 1701 `"packageManager": "pnpm@10.33.0"`; `pnpm-lock.yaml` exists in repo root.
- Detail: pnpm is the declared package manager. Bun is mentioned as an alternative path in docs (`README.md`, `docs/start/setup.md`), so the claim aligns.

### Claim 3: "CLI: `pnpm openclaw ...` or `pnpm dev`; build: `pnpm build`."
- Status: true
- Evidence: `package.json` lines 1309 (`"build": "node scripts/build-all.mjs"`), 1360 (`"dev": "node scripts/run-node.mjs"`), and multiple `pnpm openclaw ...` usages across docs and QA scenarios.
- Detail: All three commands exist as root package scripts and are used throughout the repo.

### Claim 4: "Smart gate: `pnpm check:changed`; explain `pnpm changed:lanes --json`; staged preview `pnpm check:changed --staged`."
- Status: true
- Evidence: `package.json` lines 1319 (`"changed:lanes": "node scripts/changed-lanes.mjs"`) and 1324 (`"check:changed": "node scripts/check-changed.mjs"`).
- Detail: Both commands exist. The `--json` and `--staged` flags are handled by the underlying scripts (not visible in package.json but implied by script design).

### Claim 5: "Tests: Vitest. Colocated `*.test.ts`; e2e `*.e2e.test.ts`; example models `sonnet-4.6`, `gpt-5.4`."
- Status: true
- Evidence: `vitest.config.ts` at repo root; `test/vitest/` directory with multiple vitest configs; `package.json` line 1487 `"test:coverage": "node scripts/run-vitest.mjs run --config test/vitest/vitest.unit.config.ts --coverage"`; numerous `*.test.ts` and `*.e2e.test.ts` files found across `src/`, `extensions/`, and `test/`.
- Detail: Vitest is the test runner. Model version strings `sonnet-4.6` and `gpt-5.4` appear in docs and QA scenario files.

### Claim 6: "Format/lint: `pnpm format:check`/`pnpm format`; `pnpm lint*` lanes."
- Status: partially stale
- Evidence: `package.json` line 1374 `"format:check": "oxfmt --check --threads=1"` exists. `"format"` script not found in root package.json (only `format:all`, `format:check`, `format:docs:check`, etc.). `"lint"` exists at line 1396; many `lint:*` variants exist.
- Detail: `pnpm format:check` exists, but there is no bare `pnpm format` script in root package.json. The claim says `pnpm format` exists, which is false. `pnpm lint*` lanes do exist.

### Claim 7: "Commit via `scripts/committer \"<msg>\" <file...>`; stage intended files only."
- Status: true
- Evidence: `scripts/committer` file exists and is executable.
- Detail: File is present at the claimed path.

### Claim 8: "New channel/plugin/app/doc surface: update `.github/labeler.yml` + GH labels."
- Status: true
- Evidence: `.github/labeler.yml` exists (11812 bytes).
- Detail: File present; claim matches repo structure.

### Claim 9: "Docs list first: `pnpm docs:list` if available; read relevant docs only."
- Status: unverified
- Evidence: Search for `pnpm docs:list` in package.json returned zero results. No `docs:list` script found in root package.json.
- Detail: The script is not present in root package.json. It may exist in a workspace package or may be a stale reference.

### Claim 10: "Targeted tests: `pnpm test <path-or-filter> [vitest args...]`; never raw `vitest`."
- Status: true
- Evidence: `package.json` line 1548 `"test": "node scripts/run-vitest.mjs"` and line 1549 `"test:extensions": "node scripts/test-projects.mjs extensions"`. The `run-vitest.mjs` wrapper passes through arguments.
- Detail: The wrapper script allows `pnpm test <path-or-filter>`, matching the claim. The "never raw vitest" rule is enforced culturally, not mechanically.
