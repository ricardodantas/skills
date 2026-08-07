# Doc types — reconciliation checklist

One section per category. For each doc, read it, compare against the ground-truth model from
`learn-codebase`, and fix only what drifted. Edit discipline (bottom) applies to every category.

## Human docs — README, `docs/`, guides, wikis

Reconcile against what the repo actually does now:

- **Install / setup** — commands, prerequisites, supported versions match manifests/lockfiles.
- **Usage & examples** — sample commands, flags, and code compile/run against current APIs.
- **Feature list** — add shipped features, drop removed ones; no vaporware.
- **Architecture / layout** — directory trees and module descriptions match the tree on disk.
- **Links** — internal paths resolve; external links still point somewhere real.
- **Badges / versions** — version numbers, min-runtime, and status badges are current.

When a claim depends on a specific library/framework/CLI version, pull current docs with
`find-docs` before rewriting it — don't trust memory for version-specific syntax or config.

## Changelog / release notes

- Derive entries from the drift map (`scan_docs.py` reports the baseline and changed files; use
  `git log <baseline>..HEAD` for the messages).
- Group by kind (Added / Changed / Fixed / Removed / Deprecated / Security); user-facing voice,
  not raw commit subjects.
- Respect the repo's release tooling: if it uses **Changesets** (`.changeset/`),
  **release-please**, **semantic-release**, or a `[Unreleased]` "Keep a Changelog" section, add to
  that mechanism instead of hand-editing generated history. Never rewrite already-released entries.

## Agent docs — AGENTS.md, CLAUDE.md, `.claude/`, `.cursor/`, skill files

Consumed by an agent, so **edit them through the `writing-for-agents` skill** — it is the source of
truth for the writing levers (pointers, single-source-of-truth, no-ops, progressive disclosure).
Apply them there rather than restating them here.

Reconcile the parts that track the repo's *current state*:

- **Commands & paths** — build/test/lint commands, file paths, and directory layout match the
  current environment.
- **Stack facts** — languages, versions, tools, and conventions match what `learn-codebase` found.
- **Skill files** — for each `SKILL.md`, frontmatter `name` still matches its folder and the
  described workflow reflects the current scripts/references.

## API / code reference docs

- Sync documented signatures, parameters, return types, and config keys with the code.
- Regenerate generated docs (e.g. `typedoc`, `sphinx`, `godoc`, `swagger`) via the repo's own
  command rather than hand-editing generated output.
- Update endpoint/CLI references (routes, flags, env vars) to match the code that serves them.

## Inline code comments / headers

- Fix only comments on code that actually changed — a comment that now contradicts its code.
- Update file headers, module docstrings, and `TODO/FIXME` that reference moved/renamed/removed
  things. Delete comments describing deleted code.
- Don't add narration to code that doesn't need it (respect the repo's existing comment density).

---

## Edit discipline (all categories)

- **Surgical** — change only what drifted; leave correct, unrelated docs untouched.
- **No fabrication** — never invent facts, stats, dates, or links to fill a gap. Where a real value
  is needed but unknown, leave a marked `TODO:` for the maintainer.
- **Preserve voice & format** — match each doc's existing tone, heading style, and front matter.
- **Single source of truth** — don't duplicate a fact across docs; point to the canonical one.
- **Verify before claiming done** — resolve links, run sample commands/snippets, and run the repo's
  docs build if one exists.
