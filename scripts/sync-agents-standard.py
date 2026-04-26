#!/usr/bin/env python3
"""
sync-agents-standard.py

Fetches the latest canonical AGENTS.md guidance from the upstream
agentsmd/agents.md repository and updates our local AGENTS-TEMPLATE.md.

Two extraction modes:
  --regex (default) : Fast heuristic extraction. Fragile to upstream changes.
  --llm             : Robust LLM-based extraction. Parses semantic intent.
                      Recommended for CI cron jobs.

Run:
  python scripts/sync-agents-standard.py           # regex mode
  python scripts/sync-agents-standard.py --llm     # LLM mode
  python scripts/sync-agents-standard.py --dry-run # preview, no write
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

UPSTREAM_OWNER = "agentsmd"
UPSTREAM_REPO = "agents.md"
UPSTREAM_BRANCH = "main"

URL_README = f"https://raw.githubusercontent.com/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/{UPSTREAM_BRANCH}/README.md"
URL_AGENTS = f"https://raw.githubusercontent.com/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/{UPSTREAM_BRANCH}/AGENTS.md"
API_CONTENTS = f"https://api.github.com/repos/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/contents/"

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "AGENTS-TEMPLATE.md"
STATE_PATH = REPO_ROOT / ".agents-standard-state.json"

HEADERS = {}
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


# ---------------------------------------------------------------------------
# Fetch helpers
# ---------------------------------------------------------------------------

def fetch_text(url: str, timeout: int = 30) -> str | None:
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except HTTPError as e:
        print(f"[WARN] HTTP {e.code} fetching {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[WARN] Error fetching {url}: {e}", file=sys.stderr)
        return None


def fetch_json(url: str, timeout: int = 30) -> list | dict | None:
    try:
        api_headers = {**HEADERS, "Accept": "application/vnd.github.v3+json"}
        req = Request(url, headers=api_headers)
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[WARN] Error fetching JSON {url}: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# LLM extraction (robust, future-proof)
# ---------------------------------------------------------------------------

def extract_with_llm(readme: str, agents_md: str, extra_files: dict[str, str]) -> dict:
    """Use an LLM to semantically extract the standard's current structure."""
    try:
        import openai
    except ImportError:
        print("[ERROR] openai package not installed. Install: pip install openai", file=sys.stderr)
        sys.exit(1)

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Build context
    context_parts = ["=== README.md ===", readme, "=== AGENTS.md ===", agents_md]
    for name, content in extra_files.items():
        context_parts.extend([f"=== {name} ===", content])
    context = "\n".join(context_parts)

    # Truncate if massive
    max_chars = 150_000
    if len(context) > max_chars:
        context = context[:max_chars] + "\n...[truncated]"

    prompt = (
        "You are a specification parser. Extract the current AGENTS.md "
        "standard from the upstream content below.\n\n"
        "Return ONLY a JSON object with this exact schema:\n"
        "{{\n"
        '  "recommended_sections": ["list of section names the standard recommends"],\n'
        '  "guidance_rules": ["action-oriented rules / do\'s and don\'ts"],\n'
        '  "minimal_example": "a generic, tool-agnostic markdown example of a good AGENTS.md",\n'
        '  "validation_criteria": ["criteria for checking if an AGENTS.md follows the standard"],\n'
        '  "notes": "any other important patterns or conventions from the standard"\n'
        "}}\n\n"
        "Rules:\n"
        "- Sections should be generic (not tool-specific: no pnpm, turbo, vite, npm, next.js)\n"
        "- Rules must be imperative and action-oriented\n"
        "- Example must use placeholder commands like `<your-install-command>`\n"
        "- Do NOT include any text outside the JSON\n\n"
        f"Upstream content:\n{context}\n"
    )

    print("[INFO] Calling LLM for semantic extraction ...")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    raw = resp.choices[0].message.content
    parsed = json.loads(raw)

    # Normalize
    return {
        "sections": parsed.get("recommended_sections", []),
        "rules": parsed.get("guidance_rules", []),
        "example": parsed.get("minimal_example", ""),
        "validation": parsed.get("validation_criteria", []),
        "notes": parsed.get("notes", ""),
    }


# ---------------------------------------------------------------------------
# Regex extraction (fast, fragile)
# ---------------------------------------------------------------------------

def extract_recommended_sections(readme: str, agents_md: str) -> list[str]:
    sections = []

    list_pattern = re.compile(
        r"(?:Popular choices|Common sections|Recommended sections|Cover what matters).*?\n"
        r"(?:\s*[-*]\s+(.+?)\n)+",
        re.IGNORECASE | re.DOTALL,
    )
    for match in list_pattern.finditer(readme):
        for line in match.group(0).splitlines():
            if line.strip().startswith(("- ", "* ")):
                section = line.strip()[2:].strip()
                section = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", section)
                sections.append(section)

    faq_patterns = [
        r"##?\s+(.+?)\n+.*?Add sections",
        r"##?\s+(.+?)\n+.*?Popular choices",
    ]
    for pat in faq_patterns:
        for match in re.finditer(pat, readme, re.IGNORECASE | re.DOTALL):
            sections.append(match.group(1).strip())

    heading_pattern = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    for text in (readme, agents_md):
        for match in heading_pattern.finditer(text):
            h = match.group(1).strip()
            noise_keywords = (
                "command", "example", "template", "recap", "website", "development server",
                "dependencies", "coding conventions", "useful commands", "about this",
                "changelog", "running", "app locally", "install dependencies",
            )
            if any(k in h.lower() for k in noise_keywords):
                continue
            if re.match(
                r"^\d+\s*\.\s*(Use|Keep|Do|Don't|Always|Never|Prefer|Run|Install)",
                h,
                re.I,
            ):
                continue
            if h not in sections:
                sections.append(h)

    seen = set()
    deduped = []
    for s in sections:
        key = s.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(s)

    return deduped


def extract_guidance_rules(readme: str, agents_md: str) -> list[str]:
    rules = []
    combined = f"{readme}\n\n{agents_md}"

    imperative_pattern = re.compile(
        r"^\s*[-*]\s+(?:\*\*)?(Do|Don't|Never|Always|Prefer|Avoid|Use|Run|Install|Place|Commit|Title|Format)\b.*?$",
        re.MULTILINE | re.IGNORECASE,
    )
    for match in imperative_pattern.finditer(combined):
        rule = match.group(0).strip()
        if any(
            tool in rule.lower()
            for tool in ("pnpm", "npm run", "turbo", "vite", "eslint", "next.js", "hmr")
        ):
            continue
        if rule not in rules:
            rules.append(rule)

    return rules[:30]


def extract_examples(readme: str) -> list[str]:
    examples = []
    code_block_pattern = re.compile(r"```markdown\n(.*?)\n```", re.DOTALL)
    for match in code_block_pattern.finditer(readme):
        block = match.group(1).strip()
        if block and block not in examples:
            examples.append(block)

    generic_examples = []
    for ex in examples:
        if not any(tool in ex.lower() for tool in ("pnpm", "turbo", "vite", "npm", "next.js")):
            generic_examples.append(ex)

    return generic_examples if generic_examples else examples


# ---------------------------------------------------------------------------
# Template generation
# ---------------------------------------------------------------------------

def generate_template(
    sections: list[str],
    rules: list[str],
    examples: list[str],
    upstream_sha: str,
    validation: list[str] | None = None,
    notes: str = "",
) -> str:

    lines = [
        "# AGENTS-TEMPLATE.md",
        "",
        "> **Auto-generated from the AAIF AGENTS.md standard.**",
        f"> Source: `agentsmd/agents.md` @ `{upstream_sha[:8]}`",
        "> Do not edit manually. Run `python scripts/sync-agents-standard.py` to update.",
        "",
        "---",
        "",
        "## About This Template",
        "",
        "This file is the **canonical reference** that the dac-pipeline uses to validate",
        "and lint `AGENTS.md` files in target repositories. It encodes the current best",
        "practices as defined by the Agentic AI Foundation (AAIF).",
        "",
        "When the pipeline detects a target repo's `AGENTS.md` deviates from this template,",
        "it flags the deviation as documentation drift.",
        "",
        "---",
        "",
        "## Recommended Sections",
        "",
        "An effective `AGENTS.md` should include the following sections (order is flexible):",
        "",
    ]

    for section in sections:
        lines.append(f"- **{section}**")
    if not sections:
        lines.append(
            "- *(No sections could be inferred from upstream — "
            "standard may still be evolving)*"
        )

    lines.extend([
        "",
        "---",
        "",
        "## Guidance Rules",
        "",
        "The following rules are derived from the official standard and real-world examples:",
        "",
    ])

    for rule in rules:
        clean_rule = re.sub(r"^\s*[-*]\s*", "", rule).strip()
        lines.append(f"- {clean_rule}")
    if not rules:
        lines.append("- *(No rules could be inferred — check upstream manually)*")

    lines.extend([
        "",
        "---",
        "",
        "## Minimal Example",
        "",
        "```markdown",
    ])

    if examples:
        first_ex = examples[0]
        if any(
            tool in first_ex.lower()
            for tool in ("pnpm", "turbo", "vite", "npm run", "next.js", "hmr")
        ):
            lines.extend(_generic_example_lines())
        else:
            lines.extend(first_ex.splitlines())
    else:
        lines.extend(_generic_example_lines())

    lines.extend([
        "```",
        "",
        "---",
        "",
        "## Validation Checklist",
        "",
        "When the dac-pipeline lints a repo's `AGENTS.md`, it checks:",
        "",
    ])

    if validation:
        for criterion in validation:
            lines.append(f"- [ ] {criterion}")
    else:
        lines.extend([
            "- [ ] File exists at repo root (or nearest to edited file in monorepos)",
            "- [ ] Uses standard Markdown (no proprietary syntax)",
            "- [ ] Contains at least 2 recommended sections from the list above",
            "- [ ] Instructions are action-oriented (imperative, not descriptive)",
            "- [ ] Commands are exact and copy-pasteable where possible",
            "- [ ] No placeholder text left unmodified (e.g., `<your command>`)",
            "- [ ] Updated within the last 90 days (living document principle)",
        ])

    lines.extend([
        "",
        "---",
        "",
        "## Changelog",
        "",
        f"- `{upstream_sha[:8]}` — Auto-synced from upstream `agentsmd/agents.md`",
        "",
    ])

    if notes:
        lines.extend([
            "## Notes",
            "",
            notes,
            "",
        ])

    return "\n".join(lines) + "\n"


def _generic_example_lines() -> list[str]:
    return [
        "# AGENTS.md",
        "",
        "## Setup commands",
        "- Install dependencies: `<your-install-command>`",
        "- Start dev server: `<your-start-command>`",
        "",
        "## Testing instructions",
        "- Run the full test suite: `<your-test-command>`",
        "- Run a single test: `<your-test-command> path/to/test.py::TestClass::test_method`",
        "- All commits must pass CI before merging.",
        "",
        "## Code style",
        "- Use the project's configured linter and formatter.",
        "- Follow existing naming conventions in the codebase.",
        "",
        "## PR instructions",
        "- Title format: `[<scope>] <description>`",
        "- Run lint and tests before committing.",
    ]


# ---------------------------------------------------------------------------
# State / checksum tracking
# ---------------------------------------------------------------------------

def compute_checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Sync AGENTS.md standard from upstream")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print what would change without writing"
    )
    parser.add_argument(
        "--force", action="store_true", help="Regenerate even if upstream unchanged"
    )
    parser.add_argument(
        "--llm", action="store_true", help="Use LLM for semantic extraction (robust)"
    )
    parser.add_argument("--regex", action="store_true", help="Use regex heuristics (fast, fragile)")
    args = parser.parse_args()

    print(f"[INFO] Fetching upstream from {UPSTREAM_OWNER}/{UPSTREAM_REPO} ...")

    readme = fetch_text(URL_README) or ""
    agents_md = fetch_text(URL_AGENTS) or ""

    if not readme and not agents_md:
        print("[ERROR] Could not fetch any upstream content. Aborting.", file=sys.stderr)
        return 1

    # Discover extra files
    extra_files = {}
    contents = fetch_json(API_CONTENTS)
    if contents and isinstance(contents, list):
        for item in contents:
            name = item.get("name", "").lower()
            if name in ("spec", "guidelines", "specs", "standards") and item.get("type") == "dir":
                sub_url = item.get("url", "")
                if sub_url:
                    sub_items = fetch_json(sub_url)
                    if sub_items and isinstance(sub_items, list):
                        for sub in sub_items:
                            if sub.get("type") == "file":
                                raw_url = sub.get("download_url", "")
                                if raw_url:
                                    content = fetch_text(raw_url)
                                    if content:
                                        extra_files[sub.get("name", "")] = content

    combined_upstream = f"{readme}\n{agents_md}\n"
    for name, content in extra_files.items():
        combined_upstream += f"\n--- {name} ---\n{content}\n"

    upstream_sha = compute_checksum(combined_upstream)
    state = load_state()

    if not args.force and state.get("last_sha") == upstream_sha:
        print("[INFO] Upstream unchanged. No update needed.")
        return 0

    # Extract patterns
    if args.llm:
        llm_result = extract_with_llm(readme, agents_md, extra_files)
        sections = llm_result["sections"]
        rules = llm_result["rules"]
        examples = [llm_result["example"]] if llm_result["example"] else []
        validation = llm_result["validation"]
        notes = llm_result["notes"]
    else:
        print("[INFO] Extracting patterns via regex heuristics ...")
        sections = extract_recommended_sections(readme, agents_md)
        rules = extract_guidance_rules(readme, agents_md)
        examples = extract_examples(readme)
        validation = None
        notes = ""

    print(f"[INFO] Found {len(sections)} sections, {len(rules)} rules, {len(examples)} examples")

    template = generate_template(sections, rules, examples, upstream_sha, validation, notes)

    if args.dry_run:
        print("\n--- GENERATED TEMPLATE (dry run) ---\n")
        print(template)
        print("\n--- END TEMPLATE ---")
        return 0

    TEMPLATE_PATH.write_text(template)
    print(f"[INFO] Wrote {TEMPLATE_PATH}")

    state["last_sha"] = upstream_sha
    state["last_sync"] = __import__("datetime").datetime.utcnow().isoformat() + "Z"
    state["upstream_repo"] = f"{UPSTREAM_OWNER}/{UPSTREAM_REPO}"
    state["sections_found"] = sections
    state["rules_found"] = len(rules)
    state["extra_files"] = list(extra_files.keys())
    state["extraction_mode"] = "llm" if args.llm else "regex"
    save_state(state)
    print(f"[INFO] Wrote state to {STATE_PATH}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
