---
"skills": minor
---

Add the `docs-update-expert` skill — reconciles a repository's documentation with its current state across every category: human docs (README, `docs/`, guides), CHANGELOG/release notes (git changes since the last tag), agent docs (AGENTS.md, CLAUDE.md, `.claude/`, skill files), API/reference docs, and inline comments. It orchestrates `learn-codebase` to build a ground-truth model of the repo, `writing-for-agents` to edit agent-facing docs, and `find-docs` (Context7) for version-specific library/framework/CLI details, rather than re-implementing any of them. Ships a `scan_docs.py` helper that enumerates and classifies doc files and builds a drift map from a chosen baseline — the last release tag by default, or a `--since <ref>` merge-base for a PR/feature branch — including uncommitted work, so docs can be synced in the same batch before committing.
