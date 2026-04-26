# ADR 003: LLM-Based AGENTS.md Validation Pipeline

**Status:** Proposed  
**Date:** 2026-04-26  
**Author:** dac-pipeline maintainers  
**Stakeholders:** AI coding agents, human contributors, CI/CD pipeline, PR reviewers  

---

## Context

We have adopted the AGENTS.md standard (ADR-000) and caveman style (ADR-002) for all agent-facing documentation. Now we need a mechanism to *enforce* these standards automatically. Manual review of AGENTS.md files is not scalable, and simple regex checks cannot catch semantic drift (e.g., "You should run tests" vs. "Run tests").

The solution is an **LLM-based validation pipeline** that reads a repo's AGENTS.md, compares it against our AGENTS-TEMPLATE.md (from ADR-000), and produces:
1. A **pass/fail verdict**
2. A **rewritten AGENTS.md** that fixes all detected issues
3. A **diff report** showing what changed and why

---

## Decision

We will implement a validation pipeline stage (`scripts/validate-agents-md.py`) that uses an LLM to analyze AGENTS.md files. The pipeline will:

1. **Fail the CI check** if the AGENTS.md does not meet standards
2. **Output a rewritten AGENTS.md** as an artifact
3. **Attach the rewritten file + diff to the PR** as a suggestion (if running in PR context)
4. **Assign a "cavemanness" score** (0-100) to prevent endless LLM rewrites

---

## Pipeline Behavior

### Input
- `AGENTS.md` from the target repo
- `AGENTS-TEMPLATE.md` (our canonical reference)
- `002-CAVEMAN-STYLE.md` (caveman rules)

### Output
- `agents-md-validation-report.json` — structured findings
- `AGENTS.md.rewritten` — the corrected version (if changes needed)
- `AGENTS.md.diff` — human-readable diff
- Exit code: `0` (pass) or `1` (fail)

### CI Integration

```yaml
# .github/workflows/agents-md-validate.yml
- name: Validate AGENTS.md
  run: |
    python scripts/validate-agents-md.py \
      --agents-md AGENTS.md \
      --template AGENTS-TEMPLATE.md \
      --output-dir ./validation-output
    
    if [ $? -ne 0 ]; then
      echo "::error::AGENTS.md validation failed"
      # Attach rewritten file as PR suggestion
      gh pr comment ${{ github.event.pull_request.number }} \
        --body-file ./validation-output/AGENTS.md.diff
      exit 1
    fi
```

---

## The Validation Prompt

The LLM receives this structured prompt:

```
You are an AGENTS.md validator. Your job is to check if the provided AGENTS.md
follows the AAIF standard and caveman style rules.

## Standard Checks (from AGENTS-TEMPLATE.md)
1. File exists at repo root (or nearest in monorepo)
2. Standard Markdown, no proprietary syntax (no @./ includes)
3. Action-oriented (imperative) language
4. Contains recommended sections: Setup, Build, Test, Style, Architecture, Security, PR/Commit, Gotchas
5. Commands are exact and copy-pasteable
6. No descriptive prose where imperative suffices

## Caveman Style Checks (from ADR-002)
1. No articles: a, an, the
2. No filler: just, really, basically, actually, simply
3. No pleasantries: sure, certainly, of course, happy to
4. No hedging: might, should, consider, perhaps
5. Pattern: [thing] [action] [reason]. [next step].
6. Technical terms remain exact and unchanged

## Output Format
Return a JSON object:

{
  "pass": false,
  "score_standard": 72,
  "score_caveman": 45,
  "findings": [
    {
      "category": "standard|caveman",
      "severity": "error|warning|info",
      "line": 42,
      "original": "You should always run the full test suite before committing any changes.",
      "issue": "Contains hedging ('should') and filler ('always', 'any'). Not imperative.",
      "fix": "Run full tests before commit. No regressions."
    }
  ],
  "rewritten_agents_md": "<full rewritten content>",
  "summary": "3 errors, 2 warnings. Main issues: non-imperative tone, missing Test section."
}
```

---

## The "Cavemanness" Score

### Problem
If we ask the LLM to "make this caveman style" on every pipeline run, it will keep finding edge-case words to change. A file that scored 85 last run might score 82 next run because the LLM decided "use" should be "utilize" or vice versa. This creates **endless churn**.

### Solution: Threshold-Based Gate

Instead of requiring perfect caveman style, we assign a **cavemanness score (0-100)** and only fail if it drops below a threshold.

| Score | Interpretation | Pipeline Action |
|-------|---------------|-----------------|
| 90-100 | Excellent caveman | Pass, no rewrite |
| 75-89 | Good, minor issues | Pass with warnings, suggest rewrite |
| 50-74 | Needs work | Fail, output rewritten AGENTS.md |
| 0-49 | Not caveman | Fail, output rewritten AGENTS.md |

### How the Score is Calculated

The LLM evaluates the entire file against these weighted criteria:

```
CAVEMANNESS_SCORE = 
  30% * imperative_ratio      (% of sentences that are commands, not descriptions)
+ 25% * article_drop_ratio    (% of sentences with no a/an/the)
+ 20% * filler_drop_ratio     (% of sentences with no filler words)
+ 15% * hedge_drop_ratio      (% of sentences with no might/should/consider)
+ 10% * pattern_match         (% of sentences following [thing] [action] [reason] pattern)
```

**Important:** The score is **deterministic** — same input produces same score (temperature=0). The LLM is instructed to be conservative: a sentence that is *arguably* fine should not be penalized.

### Preventing Endless Rewrites

1. **Idempotent prompt:** The rewrite prompt includes the instruction: "Only change sentences that clearly violate caveman rules. If a sentence is already acceptable, leave it exactly as-is."

2. **Diff gate:** The pipeline only outputs a rewritten file if `score_caveman < 75` OR `score_standard < 70`. If scores are above threshold, the pipeline passes even if the LLM *could* find minor improvements.

3. **Human override:** A PR comment containing `#agents-md-override` skips validation for that PR.

---

## PR Integration: Attaching the Rewritten File

When validation fails, the pipeline should make it **easy for the human to apply the fixes**.

### Option A: PR Suggestion Comments (Preferred)

Use GitHub's multi-line suggestion feature:

```python
# In the CI workflow
for finding in report["findings"]:
    if finding["severity"] == "error":
        gh api repos/{owner}/{repo}/pulls/{pr}/comments \
          -f body=f"```suggestion\n{finding['fix']}\n```\n\n{finding['issue']}" \
          -f path="AGENTS.md" \
          -f line=finding["line"]
```

### Option B: Commit the Rewritten File

If the PR author adds the label `agents-md-auto-fix`, the pipeline commits `AGENTS.md.rewritten` as `AGENTS.md` directly to the PR branch.

### Option C: Artifact Download

Always upload `AGENTS.md.rewritten` as a workflow artifact. Human can download and apply manually.

---

## Consequences

### Positive
- Automated enforcement of AGENTS.md standard and caveman style
- Reduced human review burden for documentation formatting
- Consistent agent-facing documentation across all repos using the pipeline
- Self-documenting: the validation report teaches contributors what "good" looks like

### Negative
- LLM calls cost money and add latency to CI (~2-5s per validation)
- False positives: the LLM might flag acceptable phrasing as non-caveman
- Dependency on external LLM API (rate limits, downtime)
- Contributors may find automated rewrites intrusive

### Mitigations
- **Smart cache with content-hash fingerprinting** — see Cache Strategy section below
- Use a cheap, fast model for validation (e.g., Claude Haiku, GPT-4o-mini)
- Allow `#agents-md-override` in PR description to skip validation
- Human reviewers can always reject auto-generated rewrites

---

## Cache Strategy: Content-Hash Fingerprinting

To avoid redundant LLM calls when AGENTS.md has not changed, the pipeline implements a **deterministic cache** based on content hashing.

### How It Works

1. **Compute fingerprint** of the AGENTS.md file at validation time:
   ```python
   import hashlib
   fingerprint = hashlib.sha256(open("AGENTS.md", "rb").read()).hexdigest()[:16]
   ```

2. **Cache key** combines the file fingerprint + template version + rules version:
   ```python
   cache_key = hashlib.sha256(
       f"{agents_md_hash}:{template_hash}:{rules_hash}".encode()
   ).hexdigest()[:16]
   ```

3. **Lookup cache** in `.agents-validation-cache.json` (committed to repo or stored as CI artifact):
   ```json
   {
     "abc123def4567890": {
       "timestamp": "2026-04-26T12:00:00Z",
       "pass": true,
       "score_standard": 85,
       "score_caveman": 78,
       "findings_count": 0
     }
   }
   ```

4. **Cache hit** → skip LLM call, return cached result instantly.
5. **Cache miss** → run LLM validation, store result in cache.

### Cache Invalidation Rules

| Scenario | Action |
|----------|--------|
| AGENTS.md content changes | Re-validate (new fingerprint) |
| AGENTS-TEMPLATE.md changes | Invalidate all cache entries (new template hash) |
| ADR-002 (caveman rules) changes | Invalidate all cache entries (new rules hash) |
| Pipeline version changes | Invalidate all cache entries (bump version in config) |
| `#agents-md-override` in PR | Skip cache, skip validation |

### Cache Storage Options

| Option | Pros | Cons |
|--------|------|------|
| Commit `.agents-validation-cache.json` to repo | Survives CI runner rotation, shared across branches | Repo bloat, merge conflicts |
| CI artifact (`actions/cache`) | No repo bloat, automatic eviction | Branch-specific, expires after retention period |
| External cache (Redis, S3) | Fast, shared across all pipelines | Infrastructure cost, complexity |

**Recommended:** CI artifact cache for simplicity. Commit cache only if repo has <100 contributors and AGENTS.md changes infrequently.

### Cache Hit Rate Target

> 80% of pipeline runs should hit cache. If hit rate drops below this, investigate: frequent template changes, overly broad invalidation rules, or contributors editing AGENTS.md too often.

---

## Validation

We will know this decision is correct if:
- AGENTS.md files in repos using our pipeline show consistent structure and style
- Agent task completion rates improve when consuming pipeline-validated AGENTS.md
- Contributor complaints about "robot rewriting my docs" are minimal (<5% of PRs)

---

## References

- [ADR-000: AGENTS.md Standard Adoption](000-AGENTS-FILE-STANDARD.md)
- [ADR-002: Caveman Style](002-CAVEMAN-STYLE.md)
- [AAIF AGENTS.md Standard](https://agents.md)
- [Caveman Prompting Repository](https://github.com/JuliusBrussee/caveman)

---

## Decision Record

| Date | Event |
|------|-------|
| 2026-04-26 | ADR drafted, proposed for discussion |
| 2026-04-26 | Added cavemanness score threshold mechanism to prevent endless rewrites |

---

## Appendix: Example Validation Report

```json
{
  "pass": false,
  "score_standard": 68,
  "score_caveman": 52,
  "findings": [
    {
      "category": "standard",
      "severity": "error",
      "line": 15,
      "original": "## Getting Started",
      "issue": "Section should be '## Setup commands' per AGENTS-TEMPLATE.md",
      "fix": "## Setup commands"
    },
    {
      "category": "caveman",
      "severity": "warning",
      "line": 23,
      "original": "You should always run the full test suite before committing any changes to the repository.",
      "issue": "Contains hedging ('should'), filler ('always'), articles ('the', 'any'). Not imperative.",
      "fix": "Run full tests before commit. No regressions."
    },
    {
      "category": "caveman",
      "severity": "error",
      "line": 45,
      "original": "If Docker networking fails, you might want to consider running docker network prune first.",
      "issue": "Hedging ('might', 'consider'), filler ('want to'). Weak imperative.",
      "fix": "Docker net fail -> docker network prune. Retry."
    }
  ],
  "rewritten_agents_md": "## Setup commands\n...",
  "summary": "1 standard error, 1 caveman error, 1 caveman warning. Scores: standard=68, caveman=52. Rewrite required."
}
```
