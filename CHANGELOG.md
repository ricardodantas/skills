# skills

## 1.4.0

### Minor Changes

- c164e7b: Add the `docs-update-expert` skill — reconciles a repository's documentation with its current state across every category: human docs (README, `docs/`, guides), CHANGELOG/release notes (git changes since the last tag), agent docs (AGENTS.md, CLAUDE.md, `.claude/`, skill files), API/reference docs, and inline comments. It orchestrates `learn-codebase` to build a ground-truth model of the repo, `writing-for-agents` to edit agent-facing docs, and `find-docs` (Context7) for version-specific library/framework/CLI details, rather than re-implementing any of them. Ships a `scan_docs.py` helper that enumerates and classifies doc files and builds a drift map from a chosen baseline — the last release tag by default, or a `--since <ref>` merge-base for a PR/feature branch — including uncommitted work, so docs can be synced in the same batch before committing.

## 1.3.0

### Minor Changes

- e036a4e: Add the `hugo-expert` skill — expert guidance for Hugo (gohugo.io) sites across templating, theme creation, content modeling, configuration and Hugo Modules, performance, deployment, i18n, SEO, and upgrades. It detects the repo's Hugo version and fetches version-appropriate documentation via Context7 (`find-docs`), keeping durable best-practices in references while sourcing current syntax live. Delegates blog-post writing to `hugo-write-post`.

## 1.2.2

### Patch Changes

- 6626dbb: Enrich `hugo-write-post`'s Hugo reference (verified against the official gohugoio/hugo docs): document the `hugo new content --kind` archetype flag, note that archetypes are Go templates with variables like `{{ .Date }}`/`{{ .Name }}` that Hugo fills in (don't copy literally), and add `hugo convert toTOML/toYAML/toJSON` as a front-matter format-normalization failsafe.

## 1.2.1

### Patch Changes

- 6ba0611: Docs: refresh `README.md` and `docs/CODEBASE_OVERVIEW.md` to reflect the current repo state — five skills, `apple-app-ship` recast as a companion-skill orchestrator, the new `hugo-write-post` skill, and the proven Changesets release flow.
- 1ffa936: Improve `hugo-write-post`: invoke `analyze_style.py` by its skill-directory path (the working directory at runtime is the Hugo repo, not the skill folder), handle the cold-start case of a blog with too few posts to learn from, and add a content-integrity guardrail (no fabricated facts, quotes, or stats — leave marked `TODO:` placeholders instead).

## 1.2.0

### Minor Changes

- 671be60: Add the `hugo-write-post` skill — in a Hugo repo, it learns the author's writing style from their existing posts and writes a new post on a given topic that matches that voice, placing it with correct Hugo front matter. Delegates the prose to the `social-content` skill.

## 1.1.0

### Minor Changes

- bca328b: Add the `apple-app-ship` skill — an end-to-end workflow for building, polishing, and shipping native Apple platform apps.
- fcc1304: Added new skill apple-app-ship

### Patch Changes

- f095324: optimize skill and make it more concise

## 1.0.0

### Major Changes

- 44734cc: first version

### Patch Changes

- 249b1b1: fix CI
