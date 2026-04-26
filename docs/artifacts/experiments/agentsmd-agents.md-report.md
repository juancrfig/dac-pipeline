# Repo: agentsmd/agents.md

## Standard Check
- File exist: yes
- Markdown standard: yes
- Imperative language: yes
- Sections: found 4 sections
  1. Use the Development Server, not npm run build
  2. Keep Dependencies in Sync
  3. Coding Conventions
  4. Useful Commands Recap
- Issues:
  - Missing recommended sections: Setup, Testing, Style (no explicit style guide section, only brief conventions mention)
  - No mention of package manager (pnpm is pinned in package.json but AGENTS.md mentions npm/pnpm/yarn generically)
  - Commands table lists `npm run test` but no test script exists in package.json
  - No mention of Turbopack (dev command in package.json uses `--turbopack`)
  - No mention of Tailwind CSS v4 (used in project)

## Accuracy Check

### Claim 1: "This repository contains a Next.js application located in the root of this repository."
- Status: true
- Evidence: package.json shows `next` dependency, next.config.ts exists at root
- Detail: package.json has `"next": "16.1.0"`, pages/ and components/ dirs present. Confirmed Next.js app at root.

### Claim 2: "Always use `npm run dev` (or `pnpm dev`, `yarn dev`, etc.)"
- Status: stale / partially inaccurate
- Evidence: package.json line 6: `"dev": "next dev --turbopack"`
- Detail: The AGENTS.md says to use `npm run dev` but does not mention that the actual dev command runs with `--turbopack`. This is a meaningful omission since Turbopack behavior differs from standard Webpack dev. Also, package.json specifies `"packageManager": "pnpm@9.15.1"`, so `pnpm dev` is the canonical command, not `npm run dev`.

### Claim 3: "Update the appropriate lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`)"
- Status: partially stale
- Evidence: package.json line 26: `"packageManager": "pnpm@9.15.1+sha256..."`; pnpm-lock.yaml exists at root; no package-lock.json or yarn.lock found
- Detail: Only `pnpm-lock.yaml` exists. The repo is pnpm-only (enforced by packageManager field). Mentioning npm/yarn lockfiles is misleading since pnpm is the only supported package manager here.

### Claim 4: "`npm run test` — Execute the test suite (if present)."
- Status: false
- Evidence: package.json scripts block lines 5-10: `"dev"`, `"build"`, `"start"`, `"lint"` only. No `test` script.
- Detail: There is no test script in package.json. The command `npm run test` would fail with `Missing script: "test"`. The "(if present)" qualifier is weak cover — the command is listed in the "Useful Commands Recap" table as if it works.

### Claim 5: "Prefer TypeScript (`.tsx`/`.ts`) for new components and utilities."
- Status: true
- Evidence: components/ dir has 16 `.tsx` files; pages/ dir has 3 `.tsx` files; zero `.js` or `.jsx` files in repo
- Detail: Entire codebase is TypeScript. tsconfig.json exists and is properly configured. This claim matches reality.

### Claim 6: "Co-locate component-specific styles in the same folder as the component when practical."
- Status: unverified / likely false
- Evidence: components/ dir contains only `.tsx` files, no `.css` or `.module.css` files alongside them. Global styles live in `styles/globals.css`.
- Detail: No component-specific styles are co-located. All styling appears to be done via Tailwind CSS (global config) or inline. The repo does not practice co-located styles.
