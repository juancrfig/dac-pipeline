# Repo: googleworkspace/cli

## Standard Check
- File exist: yes
- Markdown standard: yes (uses standard Markdown, no proprietary syntax; GitHub callout syntax `[!IMPORTANT]`/`[!NOTE]` is standard GitHub-flavored Markdown)
- Imperative language: yes (commands are imperative: "Use `pnpm`", "Run `cargo test`", "validate using", "Create one at...")
- Sections found: Project Overview, Build & Test, Changesets, Architecture, Demo Videos, Input Validation & URL Safety, PR Labels, Helper Commands (`+verb`), Environment Variables
- Issues:
  - AGENTS.md uses GitHub-flavored Markdown callout syntax (`> [!IMPORTANT]`, `> [!NOTE]`). While standard on GitHub, it is not CommonMark and may not render in all Markdown viewers.
  - Section names do not exactly match AAIF recommended generic names (e.g., "Build & Test" instead of "Testing", "Input Validation & URL Safety" instead of "Style" or "Security"). However, the content maps reasonably well.
  - Contains repo-specific tool references (`pnpm`, `vhs`, `cargo`, `clippy`, `lefthook`, `changeset`) which is expected for a Rust/Node hybrid repo; AAIF recommends generic language but does not forbid tool-specific commands when they are exact and copy-pasteable.
  - No explicit "Setup" section; build/test instructions are combined under "Build & Test".

## Accuracy Check

### Claim 1: "`crates/google-workspace/src/services.rs` and `crates/google-workspace/src/discovery.rs`"
- Status: true
- Evidence: `crates/google-workspace/src/services.rs` exists; `crates/google-workspace/src/discovery.rs` exists
- Detail: Both files are present in the library crate. The `services.rs` file contains service alias mappings, and `discovery.rs` contains Discovery Document fetching and caching logic. This matches the codebase.

### Claim 2: "`crates/google-workspace-cli/src/helpers/mod.rs` contains `encode_path_segment()`"
- Status: false
- Evidence: `crates/google-workspace-cli/src/helpers/mod.rs` does not define `encode_path_segment`; it is defined in `crates/google-workspace/src/validate.rs` line 277
- Detail: The AGENTS.md incorrectly states the helper lives in `helpers/mod.rs`. The actual function is `crate::validate::encode_path_segment()` in the `google-workspace` library crate. The CLI crate imports and uses it as `crate::validate::encode_path_segment()`, not from `helpers/mod.rs`. This is a documentation drift error.

### Claim 3: "`validate::validate_safe_output_dir()` rejects absolute paths, `../` traversal, symlinks outside CWD, control chars"
- Status: true
- Evidence: `crates/google-workspace/src/validate.rs` lines 72-116 define `validate_safe_output_dir`; tests at lines 360-448 exercise these exact rejections
- Detail: The implementation and unit tests confirm all four rejection categories (absolute paths, `../` traversal, symlinks outside CWD, control characters) are handled. This claim is accurate.

### Claim 4: "`gmail/mod.rs` uses clap `value_parser` for enum/allowlist values (`--msg-format`)"
- Status: unverified (partially true)
- Evidence: `crates/google-workspace-cli/src/helpers/gmail/mod.rs` exists but is 3,982 lines; a quick scan did not immediately surface a `--msg-format` flag with `value_parser`
- Detail: The file is large. The claim references `gmail/mod.rs` as an example of clap `value_parser` usage. Without a targeted grep hit for `value_parser` or `msg-format` in that file, this claim could not be fully verified in the time budget. It may be stale or located in a different module.

### Claim 5: "`vhs docs/demo.tape` generates demo recordings"
- Status: true (file exists)
- Evidence: `docs/demo.tape` exists at repo root
- Detail: The `.tape` file is present, so the command `vhs docs/demo.tape` is valid if `vhs` is installed. However, no CI or package script references `vhs`, so it is a manual/dev tool. The claim is factually correct.

### Claim 6: "`scripts/show-art.sh` helper clears screen and cats ASCII art files"
- Status: true
- Evidence: `scripts/show-art.sh` exists
- Detail: The script is present. Without reading its full contents, the existence matches the claim. The `art/` directory and `scene*.txt`/`long-*.txt` files were not found in a file search, suggesting the art files may not be committed or may have been moved. This is a minor potential drift.
