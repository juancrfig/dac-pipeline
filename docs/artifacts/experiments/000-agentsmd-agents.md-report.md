# AGENTS.md Contradiction & Standard Compliance Report
## Repo: https://github.com/agentsmd/agents.md

---

## 1. AGENTS.md EXISTS
Yes. File at `/home/juanes/agents.md/AGENTS.md`.

---

## 2. AAIF STANDARD FORMAT CHECK

Standard expect sections like: Setup, Testing, Code Style, PR instructions.

AGENTS.md sections found:
- 1. Use the Development Server, **not** `npm run build`
- 2. Keep Dependencies in Sync
- 3. Coding Conventions
- 4. Useful Commands Recap

**Missing standard sections:**
- No "Setup" or "Install" section
- No "Testing" section (only a one-line command mention)
- No "Code Style" section (only "Coding Conventions" with 2 bullets)
- No "PR instructions" section

**Verdict:** AGENTS.md does **NOT** follow AAIF standard format. It is a short Next.js dev-hints doc, not a full agent instruction spec.

---

## 3. CONTRADICTIONS (AGENTS says -> Actually happening -> Location)

### A. Dev server command
**AGENTS says:** Use `npm run dev` (or `pnpm dev`, `yarn dev`, etc.)  
**Actually happening:** `package.json` script is `"dev": "next dev --turbopack"`. README says use `pnpm run dev`. Lockfile is `pnpm-lock.yaml`. Package manager is `pnpm@9.15.1`.  
**Location:** `package.json` line 6, `README.md` line 43-47, `pnpm-lock.yaml` exists, no `package-lock.json` or `yarn.lock`.

### B. Test command
**AGENTS says:** `npm run test` — Execute the test suite (if present).  
**Actually happening:** No `test` script in `package.json`. No test files, no test config (no jest, vitest, playwright).  
**Location:** `package.json` lines 5-10. Search for `*.test.*`, `*.spec.*`, `__tests__` returned zero results.

### C. Lint command
**AGENTS says:** `npm run lint` — Run ESLint checks.  
**Actually happening:** `package.json` has `"lint": "next lint"`. But no ESLint config file exists (no `.eslintrc*`, no `eslint.config.*`).  
**Location:** `package.json` line 9. No eslint config in repo root.

### D. Lockfile sync
**AGENTS says:** Update lockfile (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`).  
**Actually happening:** Only `pnpm-lock.yaml` exists. No `package-lock.json`, no `yarn.lock`. AGENTS.md implies all three are possible, but repo is pnpm-only.  
**Location:** repo root listing.

### E. TypeScript preference
**AGENTS says:** Prefer TypeScript (`.tsx`/`.ts`) for new components and utilities.  
**Actually happening:** All source files are `.tsx` or `.ts`. No `.js` components found. This one **matches**.  
**Location:** `components/`, `pages/`, `next.config.ts`.

### F. Co-locate styles
**AGENTS says:** Co-locate component-specific styles in same folder as component when practical.  
**Actually happening:** All styles live in single `styles/globals.css`. No component-level CSS/modules found.  
**Location:** `styles/globals.css` exists. No `*.module.css` or component CSS files in `components/`.

### G. Next.js app location
**AGENTS says:** "This repository contains a Next.js application located in the root of this repository."  
**Actually happening:** True. App is root-level, uses `pages/` router (not `app/` router).  
**Location:** repo root. No `app/` directory.

---

## 4. SUMMARY

- AGENTS.md exists but is **not AAIF-compliant** (missing Setup, Testing, Code Style, PR sections).
- **4 contradictions** found: test command missing, lint config missing, style co-location not practiced, lockfile advice is overly broad.
- **1 match**: TypeScript preference is followed.
- Repo is a simple Next.js website (pages router, pnpm, Tailwind v4, no tests, no eslint config).
