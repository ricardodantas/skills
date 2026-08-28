---
name: docs-update-expert
description: Reconcile a repository's documentation with its current state — README, docs/, guides, CHANGELOG/release notes, agent docs (AGENTS.md, CLAUDE.md, .claude/, skill files), API/reference docs, and inline comments — and wire them together, fixing broken links and orphaned pages so every doc is reachable. Orchestrates learn-codebase to model the repo, writing-for-agents to edit agent-facing docs, and find-docs (Context7) for version-specific library/framework/CLI details. Use when the user asks to "update the docs", "sync docs with the code", "docs are out of date", "refresh the README/AGENTS.md", "document recent changes", "link the docs together", "fix broken doc links", "nothing links to this doc", or after features land before a PR or release.
---

# Docs Update Expert

Bring every doc in a repo back in line with what the code actually does — and with each other,
so the set reads as one connected whole rather than a pile of files. This skill is an
**orchestrator** — it composes three companion skills rather than re-deriving their work:

- **`learn-codebase`** — builds the ground-truth model of the repo and surfaces other installed
  skills that fit its stack.
- **`writing-for-agents`** — the writing discipline for agent-facing docs.
- **`find-docs`** (Context7) — current docs for a library/framework/CLI when a claim is
  version-sensitive.

Per-category reconciliation rules and edit discipline live in
[references/doc-types.md](references/doc-types.md) — read it before editing.

## 0. Preflight — companion skills

Confirm `learn-codebase`, `writing-for-agents`, and `find-docs` are available (they appear in your
available skills). If any is missing, tell the user and offer to install it — `npx skills find
<name>` — and don't start until the ones you need are present. `writing-for-agents` is required only
when agent docs are in scope; `find-docs` only when a doc makes version-specific claims.

## 1. Ground truth — model the repo

Delegate to `learn-codebase` to map the stack, architecture, commands, and conventions, and to
surface repo-relevant skills. Reuse an existing `docs/CODEBASE_OVERVIEW.md` only if the commit SHA
it records still matches `git rev-parse HEAD`; otherwise — or if it's absent — re-run learn-codebase
to rebuild the model. This model — not memory — is what every doc is measured against. Apply any
repo-relevant skills it surfaces (e.g. a framework or testing skill) when they sharpen a specific
doc.

## 2. Discover the docs

Run the scanner from this skill's directory (your cwd is the target repo):

```bash
"<skill-dir>/scripts/scan_docs.py" .                                          # baseline: last release tag
"<skill-dir>/scripts/scan_docs.py" . --since "$(git merge-base origin/HEAD HEAD)"  # a PR / feature branch
```

It classifies every doc file (`human`, `agent`, `changelog`) and reports two things: the **drift
map** — files changed since a baseline, plus any uncommitted work — and the **link graph**
(`links`), covering how the docs reference each other (used in step 4). Choose the baseline for
the situation:

- **Release** — omit `--since`; it defaults to the last release tag.
- **PR / feature branch** — pass `--since <merge-base with the base branch>` so the map is the
  branch's own changes, not everything since the last tag.
- **No tag / no baseline** — the scanner reports `has_baseline: false` and only uncommitted changes.
  There's no diff baseline, so reconcile the whole doc set against the model from step 1.

**Docs describing changed code are the ones most likely stale — prioritize them.** Uncommitted
changes are included so you can sync docs in the same batch before committing.

## 3. Reconcile each doc against the model

For every doc that drifted, route to its category in
[references/doc-types.md](references/doc-types.md) and apply that checklist:

| Category | Handling |
|----------|----------|
| Human docs (README, `docs/`, guides) | Match current features, commands, layout, links. |
| Changelog / release notes | Entries from `git log <last-tag>..HEAD`; respect the repo's release tooling. |
| Agent docs (AGENTS.md, CLAUDE.md, `.claude/`, skills) | Edit through **`writing-for-agents`** levers. |
| API / reference docs | Sync signatures/config; regenerate generated docs via the repo's command. |
| Inline comments / headers | Fix only comments on code that changed. |

When a doc asserts version-specific syntax, config keys, or CLI flags, pull the current docs with
`find-docs` before rewriting — don't trust memory for details that shift between versions.

## 4. Connect the docs

A correct doc nobody can reach is still broken. The scanner's `links` block reports the graph:
`graph` (each doc's `in`/`out` edges), `broken_links` (targets that don't resolve on disk), and
`orphans` (docs with no inbound link).

- **Broken links** — fix every one: repoint moved files, drop links to deleted docs.
- **Orphans** — give each an inbound link from the doc that owns its topic (README → guide, guide →
  deep-dive, `SKILL.md` → its `references/`). If nothing *should* link to it, it's dead weight —
  propose deleting it rather than leaving it stranded. Judge before acting: a path mentioned only in
  backticks reads as an orphan to the scanner even when that was deliberate.
- **New docs** — a doc you add in this pass isn't done until something links to it.
- **Related docs** — cross-link docs covering adjacent ground so a reader lands on the current one
  instead of a stale near-duplicate.
- **Hubs** — a README or `docs/` index should reach everything under it in one or two hops; wire new
  sections into it.

Conventions (link style, hub layout, dedupe-by-pointer):
[references/doc-types.md](references/doc-types.md#cross-linking--navigation).

## 5. Apply edits directly

Make surgical edits in place. Never fabricate facts, stats, or links to fill a gap — leave a marked
`TODO:` where a real value is needed but unknown. Full edit discipline:
[references/doc-types.md](references/doc-types.md).

## 6. Verify

- Internal links/paths resolve; sample commands and code snippets run against the current code.
- If the repo has a docs build (`mkdocs`, `docusaurus`, `hugo`, `sphinx`, `typedoc`, …), run it and
  fix warnings you introduced.
- Re-run `scan_docs.py`: `broken_links` is empty, and every remaining orphan is one you kept on
  purpose.

## 7. Summarize

Report the changes per file (what drifted, what you changed), the links you added or fixed, any
orphan you left in place and why, and any `TODO:` placeholders left for the maintainer. Leave
committing and pushing to the user.
