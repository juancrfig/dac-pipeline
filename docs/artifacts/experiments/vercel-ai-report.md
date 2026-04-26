# Repo: vercel/ai

## Standard Check
- File exist: yes
- Markdown standard: yes
- Imperative language: partially (descriptive prose in Overview, Structure, Architecture sections dilutes imperative tone)
- Sections: Project Overview, Repository Structure, Development Setup, Development Commands, Core APIs, Import Patterns, Coding Standards, Error Pattern, Architecture Decision Records, Project Philosophies, Architecture, Contributing Guides, Changesets, Task Completion Guidelines, Do Not
- Issues:
  - Tone not consistently action-oriented; many sections describe rather than instruct
  - Some "Package-Level Commands" listed as universal are absent in several packages (e.g., `pnpm test:watch`, `pnpm build:watch`)
  - Pre-commit hook claim does not match visible `package.json` / `lint-staged` config

## Accuracy Check

### Claim 1: "The SDK supports both Zod 3 and Zod 4. Use correct imports: `import * as z3 from 'zod/v3';` ... `import * as z4 from 'zod/v4';` ... Use `z4.core.$ZodType` for type references"
- Status: true
- Evidence: packages/provider-utils/src/schema.ts, packages/rsc/src/stream-ui/stream-ui.tsx, packages/xai/src/xai-image-options.ts
- Detail: `zod/v3` imports found in provider-utils compatibility code. `zod/v4` imports found in xai, fal, klingai, cohere, etc. `z4.core.$ZodType` used in provider-utils schema.ts and rsc stream-ui.tsx.

### Claim 2: "`- **Pre-commit hook**: Runs `pnpm install` if `package.json` changes are staged`"
- Status: false
- Evidence: package.json lint-staged config
- Detail: Root package.json shows `"lint-staged": { "*.{js,jsx,ts,tsx,mjs,cjs}": ["ultracite fix"] }` and `"prepare": "husky"`. No `pnpm install` step visible in configured hooks. CONTRIBUTING.md mentions this behavior but it is not reflected in committed config.

### Claim 3: "`- **Fixtures**: Store in `__fixtures__` subfolders`" and "`- **Snapshots**: Store in `__snapshots__` subfolders`"
- Status: false
- Evidence: Search results
- Detail: Search for `__fixtures__` returned 0 files in repo. Search for `__snapshots__` returned 0 files. These conventions are claimed but not practiced in current codebase.

### Claim 4: "Provider type interfaces (`LanguageModelV4`)" (from Import Patterns table)
- Status: unverified / possibly stale
- Evidence: content/docs/07-reference/01-ai-sdk-core/65-language-model-v2-middleware.mdx
- Detail: `LanguageModelV4` string appears in many provider files and docs, but a docs file named `language-model-v2-middleware.mdx` exists, suggesting newer model spec versions may be in use. Without reading the provider package source directly, cannot confirm V4 is still the canonical interface name.

### Claim 5: "Run these from within a package directory (e.g., `packages/ai`): `pnpm test:watch`"
- Status: stale
- Evidence: packages/ai/package.json vs packages/xai/package.json
- Detail: `test:watch` exists in `packages/ai/package.json` (`"test:watch": "vitest --config vitest.node.config.js"`), but absent in many other packages (e.g., xai, workflow, voyage, vercel, etc. only have `test:node`, `test:edge`, `test:update`). Not a universal package-level command as implied.
