#!/usr/bin/env python3
"""
validate-agents-md.py

Validates an AGENTS.md file against:
1. The AAIF standard (via AGENTS-TEMPLATE.md)
2. Caveman style rules (ADR-002)

Uses an LLM (default: gpt-4o-mini via OpenRouter) to score and suggest fixes.
Outputs a markdown report and posts it as a PR comment.

Environment:
  OPENROUTER_API_KEY  - API key for OpenRouter
  VALIDATOR_MODEL     - Model to use (default: openai/gpt-4o-mini-2024-07-18)
  GITHUB_TOKEN        - For posting PR comments
  GITHUB_REPOSITORY   - owner/repo
  PR_NUMBER           - Pull request number

Usage:
  python scripts/validate-agents-md.py --agents-md AGENTS.md --template AGENTS-TEMPLATE.md --pr-number 42
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from urllib.request import urlopen, Request

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "openai/gpt-5-nano"
CACHE_DIR = Path(__file__).resolve().parent.parent / ".agents-validation-cache"

# Caveman rules from ADR-002
CAVEMAN_RULES = [
    "Use short sentences. Max 15 words per sentence.",
    "One idea per sentence.",
    "No filler words: 'basically', 'essentially', 'in order to', 'it is important to note'.",
    "No passive voice. Agent must know WHO does WHAT.",
    "No nested clauses. One verb per sentence preferred.",
    "Use bullet points for lists. No prose paragraphs.",
    "Command form: 'Run tests.' Not 'You should run the tests.'",
    "Quantify when possible. 'Max 500 lines.' Not 'Keep files small.'",
    "No hedging. 'Always X.' Not 'Prefer to X when possible.'",
    "No markdown tables. Use bullets or numbered lists.",
    "No emojis or decorative ASCII.",
    "No 'please', 'kindly', 'thank you'.",
    "No section longer than 10 bullets.",
    "No preamble. Start with the instruction.",
]

# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def _cache_path(key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{key}.json"

def _cache_get(key: str) -> dict | None:
    path = _cache_path(key)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return None
    return None

def _cache_set(key: str, value: dict) -> None:
    _cache_path(key).write_text(json.dumps(value, indent=2) + "\n")

# ---------------------------------------------------------------------------
# LLM call via OpenRouter
# ---------------------------------------------------------------------------

def _call_llm(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    chosen_model = model or os.environ.get("VALIDATOR_MODEL") or DEFAULT_MODEL

    payload = {
        "model": chosen_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
    }

    req = Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/dac-pipeline",
            "X-Title": "AGENTS.md Validator",
        },
    )

    try:
        with urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}", file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------------------------
# Validation stages
# ---------------------------------------------------------------------------

def validate_standard_compliance(agents_md: str, template: str, model: str | None) -> dict:
    """Check if AGENTS.md follows the AAIF standard."""
    cache_key = f"std-{_content_hash(agents_md + template)}"
    cached = _cache_get(cache_key)
    if cached:
        print("[INFO] Using cached standard validation result")
        return cached

    system = """You are an AGENTS.md validator. Check if the provided AGENTS.md follows the AAIF standard.

Return ONLY a JSON object with this exact schema:
{
  "score": 0-100,
  "passed": true|false,
  "issues": [
    {
      "severity": "error|warning|info",
      "category": "missing_section|wrong_format|stale_info|other",
      "message": "human-readable description",
      "suggestion": "how to fix it"
    }
  ],
  "summary": "one-line summary"
}

Rules:
- Score < 70 = fail
- Issues must reference exact text from AGENTS.md when possible
- Suggestions must be specific and actionable
- Do NOT include any text outside the JSON"""

    user = f"=== AGENTS-TEMPLATE.md (standard) ===\n{template}\n\n=== AGENTS.md (to validate) ===\n{agents_md}"

    raw = _call_llm(system, user, model)
    # Extract JSON if wrapped in markdown
    json_match = re.search(r"```json\n(.*?)\n```", raw, re.DOTALL)
    if json_match:
        raw = json_match.group(1)

    result = json.loads(raw)
    _cache_set(cache_key, result)
    return result


def validate_caveman_style(agents_md: str, model: str | None) -> dict:
    """Check caveman style compliance."""
    cache_key = f"cave-{_content_hash(agents_md)}"
    cached = _cache_get(cache_key)
    if cached:
        print("[INFO] Using cached caveman validation result")
        return cached

    system = f"""You are a caveman style validator. Check if the AGENTS.md follows these rules:

{chr(10).join(f"- {r}" for r in CAVEMAN_RULES)}

Return ONLY a JSON object:
{{
  "score": 0-100,
  "passed": true|false,
  "violations": [
    {{
      "rule": "which rule was broken",
      "location": "exact text from AGENTS.md",
      "fix": "rewritten in caveman style"
    }}
  ],
  "summary": "one-line summary"
}}

Scoring guidelines:
- 90-100: Excellent caveman style. Minor issues only.
- 70-89: Good caveman style. A few fixable issues.
- 50-69: Needs work. Several violations.
- 0-49: Poor. Many violations.

Score < 70 = fail. Be FAIR, not pedantic. Small imperfections are OK if the overall style is clear and concise. Do NOT nitpick single words or split obvious pairs. Do NOT include text outside JSON."""

    user = f"=== AGENTS.md ===\n{agents_md}"

    raw = _call_llm(system, user, model)
    json_match = re.search(r"```json\n(.*?)\n```", raw, re.DOTALL)
    if json_match:
        raw = json_match.group(1)

    result = json.loads(raw)
    _cache_set(cache_key, result)
    return result


def generate_rewrite(agents_md: str, template: str, std_issues: list, cave_violations: list, model: str | None) -> str:
    """Generate a rewritten AGENTS.md that fixes all issues."""
    cache_key = f"rewrite-{_content_hash(agents_md + template + json.dumps(std_issues) + json.dumps(cave_violations))}"
    cached = _cache_get(cache_key)
    if cached:
        return cached.get("rewrite", "")

    system = """You are an AGENTS.md rewriter. Rewrite the provided AGENTS.md to:
1. Follow the AAIF standard exactly
2. Use caveman style (short sentences, imperative, no fluff)
3. Fix all reported issues

Return ONLY the rewritten AGENTS.md content as raw markdown. No explanations, no JSON, no preamble."""

    user = f"=== Standard Template ===\n{template}\n\n=== Issues to Fix ===\nStandard issues: {json.dumps(std_issues, indent=2)}\n\nCaveman violations: {json.dumps(cave_violations, indent=2)}\n\n=== Current AGENTS.md ===\n{agents_md}"

    rewrite = _call_llm(system, user, model)
    _cache_set(cache_key, {"rewrite": rewrite})
    return rewrite

# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    agents_md_path: Path,
    std_result: dict,
    cave_result: dict,
    rewrite: str,
) -> str:
    lines = [
        "# AGENTS.md Validation Report",
        "",
        f"**File:** `{agents_md_path}`",
        f"**Date:** {__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()}",
        "",
        "---",
        "",
        "## Standard Compliance",
        "",
        f"**Score:** {std_result.get('score', 0)}/100",
        f"**Status:** {'PASS' if std_result.get('passed') else 'FAIL'}",
        "",
    ]

    issues = std_result.get("issues", [])
    if issues:
        lines.append("### Issues")
        for issue in issues:
            emoji = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(issue.get("severity"), "•")
            lines.append(f"{emoji} **{issue.get('category', 'issue')}** — {issue.get('message', '')}")
            if issue.get("suggestion"):
                lines.append(f"   → *Fix:* {issue['suggestion']}")
            lines.append("")
    else:
        lines.append("✅ No standard compliance issues found.")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Caveman Style",
        "",
        f"**Score:** {cave_result.get('score', 0)}/100",
        f"**Status:** {'PASS' if cave_result.get('passed') else 'FAIL'}",
        "",
    ])

    violations = cave_result.get("violations", [])
    if violations:
        lines.append("### Violations")
        for v in violations:
            lines.append(f"❌ **{v.get('rule', 'Rule broken')}**")
            lines.append(f"   → *Found:* `{v.get('location', 'N/A')}`")
            lines.append(f"   → *Fix:* {v.get('fix', 'N/A')}")
            lines.append("")
    else:
        lines.append("✅ No caveman style violations found.")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Suggested Rewrite",
        "",
        "The following rewrite addresses all issues above:",
        "",
        "```markdown",
        rewrite,
        "```",
        "",
        "---",
        "",
        "## Action Items",
        "",
    ])

    if not std_result.get("passed") or not cave_result.get("passed"):
        lines.append("- [ ] Review the suggested rewrite above")
        lines.append("- [ ] Apply fixes manually or merge the suggested rewrite")
        lines.append("- [ ] Re-run validation after changes")
    else:
        lines.append("- [x] All checks passed — no action needed")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by dac-pipeline AGENTS.md validator*")

    return "\n".join(lines) + "\n"

# ---------------------------------------------------------------------------
# GitHub PR comment
# ---------------------------------------------------------------------------

def post_pr_comment(report: str, pr_number: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repo or not pr_number:
        print("[WARN] Missing GITHUB_TOKEN, GITHUB_REPOSITORY, or PR_NUMBER — skipping PR comment")
        return

    # Truncate if too long (GitHub limit ~65536 chars)
    body = report
    if len(body) > 60000:
        body = body[:60000] + "\n\n... (truncated)"

    payload = json.dumps({"body": body}).encode("utf-8")
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    req = Request(url, data=payload, headers={
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json",
    })

    try:
        with urlopen(req, timeout=30) as resp:
            print(f"[INFO] Posted comment to PR #{pr_number}")
    except Exception as e:
        print(f"[WARN] Failed to post PR comment: {e}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AGENTS.md against AAIF standard")
    parser.add_argument("--agents-md", required=True, help="Path to AGENTS.md file")
    parser.add_argument("--template", required=True, help="Path to AGENTS-TEMPLATE.md")
    parser.add_argument("--pr-number", default="", help="PR number for posting comment")
    parser.add_argument("--model", default=None, help="Override LLM model")
    parser.add_argument("--no-rewrite", action="store_true", help="Skip rewrite generation")
    args = parser.parse_args()

    agents_path = Path(args.agents_md)
    template_path = Path(args.template)

    if not agents_path.exists():
        print(f"[ERROR] AGENTS.md not found: {agents_path}", file=sys.stderr)
        return 1
    if not template_path.exists():
        print(f"[ERROR] Template not found: {template_path}", file=sys.stderr)
        return 1

    agents_md = agents_path.read_text()
    template = template_path.read_text()

    print("[INFO] Validating standard compliance ...")
    std_result = validate_standard_compliance(agents_md, template, args.model)
    print(f"[INFO] Standard score: {std_result.get('score', 0)}/100")

    print("[INFO] Validating caveman style ...")
    cave_result = validate_caveman_style(agents_md, args.model)
    print(f"[INFO] Caveman score: {cave_result.get('score', 0)}/100")

    rewrite = ""
    if not args.no_rewrite and (not std_result.get("passed") or not cave_result.get("passed")):
        print("[INFO] Generating rewrite ...")
        rewrite = generate_rewrite(
            agents_md, template,
            std_result.get("issues", []),
            cave_result.get("violations", []),
            args.model,
        )
    else:
        rewrite = agents_md  # already good

    report = generate_report(agents_path, std_result, cave_result, rewrite)

    report_path = Path("agents-md-validation-report.md")
    report_path.write_text(report)
    print(f"[INFO] Wrote report to {report_path}")

    if args.pr_number:
        post_pr_comment(report, args.pr_number)

    # Exit code: 0 if both pass, 1 if either fails
    if std_result.get("passed") and cave_result.get("passed"):
        print("[INFO] All checks passed.")
        return 0
    else:
        print("[WARN] Validation failed — see report for details", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
