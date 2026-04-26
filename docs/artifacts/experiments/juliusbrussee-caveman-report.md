# Repo: JuliusBrussee/caveman

## Standard Check
- File exist: yes
- Markdown standard: NO — use `@./path` include syntax. Not human readable. Not standard markdown.
- Imperative language: yes (in referenced SKILL.md files)
- Sections: NONE in AGENTS.md. Sub-files have Rules, Examples, Boundaries, Intensity, Auto-Clarity. No Setup, no Testing, no Style, no Build.
- Issues:
  - AGENTS.md is manifest file, not doc. Four `@./` pointers only.
  - No standard AAIF sections anywhere.
  - Content split across 4 files. Agent must chase pointers.
  - No copy-pasteable setup commands in AGENTS.md itself.

## Accuracy Check

### Claim 1: "The compression scripts live in `caveman-compress/scripts/`... search for `caveman-compress/scripts/__main__.py`"
- Status: true
- Evidence: caveman-compress/scripts/__main__.py exist. Also cli.py, compress.py, detect.py, validate.py, benchmark.py.
- Detail: Directory structure match claim exactly.

### Claim 2: "Run: `cd caveman-compress && python3 -m scripts <absolute_filepath>`"
- Status: true
- Evidence: __main__.py present in caveman-compress/scripts/. Package structure valid.
- Detail: Command syntax correct for module execution.

### Claim 3: (from README/CLAUDE context) "To reproduce: `uv run python benchmarks/run.py` (needs `ANTHROPIC_API_KEY` in `.env.local`)"
- Status: true
- Evidence: benchmarks/run.py lines 16-23 load `.env.local` and use `anthropic.Anthropic()`.
- Detail: Script exists, expects exact env var, uses exact tool. Claim accurate.

### Claim 4: "CI will automatically sync these changes to `skills/compress/` and `plugins/caveman/skills/compress/`"
- Status: true
- Evidence: Identical SKILL.md and scripts found in all three locations: `skills/compress/`, `plugins/caveman/skills/compress/`, `caveman-compress/`. CONTRIBUTING.md confirms CI sync.
- Detail: Content duplicated across 3 paths. CI sync claim match actual repo structure.

### Claim 5: (from caveman-compress/SKILL.md) Compression preserves code blocks, inline code, URLs, file paths, commands exactly.
- Status: unverified
- Evidence: Validation logic exists in caveman-compress/scripts/validate.py. No live run performed.
- Detail: Code structure support claim but runtime accuracy not confirmed.
