# Architecture

## System Overview

DAC is a multi-layer pipeline:

```
┌─────────────────────────────────────────┐
│  Input: Markdown docs (AGENTS.md, etc.) │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Extractors                             │
│  - File references (regex + AST)        │
│  - Function signatures (tree-sitter)    │
│  - Import graphs (static analysis)      │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Validators                             │
│  - Filesystem existence                 │
│  - AST signature matching               │
│  - Invariant subset check               │
│  - Token count                          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Reporters                              │
│  - Markdown (human-readable)            │
│  - JSON (machine-readable)              │
│  - GitHub PR comment                    │
│  - CLI (rich terminal output)           │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Optional: LLM Bridge                   │
│  - Diff analysis                          │
│  - Doc update suggestions                 │
│  - Auto-PR generation                     │
└─────────────────────────────────────────┘
```

## Language Support

| Language | File refs | Function sigs | Imports | Parser |
|----------|-----------|---------------|---------|--------|
| Python | ✅ | ✅ | ✅ | Built-in `ast` |
| TypeScript | ✅ | ✅ | ✅ | Tree-sitter |
| JavaScript | ✅ | ✅ | ✅ | Tree-sitter |
| Go | ✅ | ✅ | ✅ | Tree-sitter |
| Rust | ✅ | 🚧 | 🚧 | Tree-sitter |
| Ruby | ✅ | 🚧 | 🚧 | Tree-sitter |

## Extension Points

### Custom Extractors

```python
from dac.core.extractors import BaseExtractor

class MyExtractor(BaseExtractor):
    def extract(self, doc_path: Path) -> list[Reference]:
        # Your logic here
        return references
```

### Custom Validators

```python
from dac.core.validators import BaseValidator

class MyValidator(BaseValidator):
    def validate(self, refs: list[Reference]) -> list[Issue]:
        # Your logic here
        return issues
```

### LLM Providers

```python
from dac.llm_bridge import BaseProvider

class MyProvider(BaseProvider):
    def analyze(self, diff: str, docs: str) -> Suggestion:
        # Your logic here
        return suggestion
```

## Data Flow

1. **Discovery**: Find all doc files matching `dac.config.yaml` patterns
2. **Extraction**: Parse each doc for code references
3. **Resolution**: Map references to actual source files
4. **Validation**: Check existence, signatures, invariants
5. **Reporting**: Generate human + machine readable output
6. **Action**: Pass/fail CI, suggest fixes, or auto-fix

## Performance Targets

- Small repo (< 100 files): < 2 seconds
- Medium repo (1k files): < 10 seconds
- Large repo (10k files): < 60 seconds
- LLM analysis: < 30 seconds (async, non-blocking)
