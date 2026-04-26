#!/usr/bin/env python3
"""
update-standard-reference.py

Checks if the upstream AAIF standard (agentsmd/agents.md) has changed.
If so, uses an LLM to regenerate docs/AAIF-STANDARD-REFERENCE.md
in caveman style.

Usage:
  python scripts/update-standard-reference.py \\
      --reference docs/AAIF-STANDARD-REFERENCE.md \\
      --template AGENTS-TEMPLATE.md
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

UPSTREAM_OWNER = "agentsmd"
UPSTREAM_REPO = "agents.md"
UPSTREAM_BRANCH = "main"
URL_README = f"https://raw.githubusercontent.com/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/{UPSTREAM_BRANCH}/README.md"
URL_AGENTS = f"https://raw.githubusercontent.com/{UPSTREAM_OWNER}/{UPSTREAM_REPO}/{UPSTREAM_BRANCH}/AGENTS.md"

DEFAULT_MODEL = os.environ.get("VALIDATOR_MODEL", "openai/gpt-5-nano")
STATE_FILE = ".agents-standard-state.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fetch(url: str) -> str | None:
    try:
        req = Request(url, headers={"User-Agent": "dac-pipeline/1.0"})
        with urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"[WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        return None


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _call_llm(prompt: str, model: str) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a technical writer. Write in caveman style: "
                    "short sentences, imperative, no filler words, no passive voice, "
                    "bullets only, max 15 words per sentence."
                ),
            },
            {"role": "user", "content": prompt},
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
            "X-Title": "AAIF Standard Reference Updater",
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
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, help="Path to AAIF-STANDARD-REFERENCE.md")
    parser.add_argument("--template", required=True, help="Path to AGENTS-TEMPLATE.md")
    args = parser.parse_args()

    reference_path = Path(args.reference)
    template_path = Path(args.template)

    # Fetch upstream
    print("[INFO] Fetching upstream AAIF standard ...")
    readme = _fetch(URL_README) or ""
    agents_md = _fetch(URL_AGENTS) or ""

    if not readme and not agents_md:
        print("[WARN] Could not fetch upstream. Skipping update.")
        return 0

    upstream_combined = f"{readme}\n\n{agents_md}"
    upstream_hash = _content_hash(upstream_combined)

    # Check if we have state
    state_path = Path(STATE_FILE)
    if state_path.exists():
        state = json.loads(state_path.read_text())
        last_hash = state.get("reference_hash", "")
        if last_hash == upstream_hash:
            print("[INFO] Upstream unchanged. No update needed.")
            return 0

    print(f"[INFO] Upstream changed (hash: {upstream_hash}). Regenerating reference ...")

    # Build prompt for LLM
    prompt = f"""Update the AAIF standard reference document based on the latest upstream content.

Current reference doc:
{reference_path.read_text() if reference_path.exists() else "(does not exist yet)"}

Current template:
{template_path.read_text() if template_path.exists() else "(does not exist yet)"}

Latest upstream README.md:
{readme[:8000]}

Latest upstream AGENTS.md:
{agents_md[:8000]}

Write a complete, updated AAIF-STANDARD-REFERENCE.md file. Rules:
- Follow caveman style strictly
- Include all required sections from the standard
- Add validation checklist
- Keep it under 150 lines
- Include links to AAIF project
- Use `uv` for all Python tooling examples. Never use `pip`.
  Use `uv sync`, `uv run pytest`, `uv run python`, etc.
- Remove any lines that contain the word " pip "

Return ONLY the raw markdown content. No code blocks, no explanations."""

    model = os.environ.get("VALIDATOR_MODEL", DEFAULT_MODEL)
    new_reference = _call_llm(prompt, model)

    # Clean up any markdown fences the LLM might have added
    new_reference = re.sub(r"^```markdown\n", "", new_reference)
    new_reference = re.sub(r"\n```$", "", new_reference)
    new_reference = new_reference.strip() + "\n"

    # Post-process: remove any lines containing " pip "
    lines = new_reference.splitlines()
    filtered = [line for line in lines if " pip " not in line]
    new_reference = "\n".join(filtered) + "\n"

    reference_path.write_text(new_reference)
    print(f"[INFO] Wrote updated reference to {reference_path}")

    # Update state
    now = __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc
    ).isoformat()
    state = {"reference_hash": upstream_hash, "last_update": now}
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"[INFO] Updated state file {state_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
