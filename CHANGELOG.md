# skills

## 1.5.0

### Minor Changes

- 28155cb: Add the `app-idea-research` skill — researches and validates an app or software product idea end-to-end and returns a brutally honest go/no-go verdict. It is an orchestrator: it preflights the installed research skills (`apple-app-research`, `android-app-research`, `ios-app-research`, `research`, `competitor-alternatives`, `pricing-strategy`, `marketing-ideas`, `launch-strategy`, `find-docs`, `find-skills`) and fans out parallel subagents across community pain points (Reddit/forums), competitors, market size and trends, target demographics, monetization, and the latest Apple and Android frameworks — then synthesizes a single report with 1–10 scores per dimension, a platform recommendation (iOS/Mac-only, Android-only, or multiplatform), a detailed concept description, concrete examples, evidence with citations, risks, and MVP scope. Delivers both an in-conversation briefing and a saved `app-idea-research-<slug>.md`. Ships two references: `research-playbook.md` (parallel subagent briefs, per-platform source lists, framework-check guidance) and `verdict-report.md` (the report template).
- 2b68960: Add the `apple-design` skill — a comprehensive Apple Human Interface Guidelines (HIG) and design system reference covering Liquid Glass (iOS 26+), SF Symbols, Icon Composer, typography, color, layout, accessibility, navigation patterns, UI components, and platform-specific guidance for iOS, macOS, watchOS, tvOS, and visionOS. Ships seven references (`hig-foundations.md`, `hig-patterns.md`, `hig-components.md`, `liquid-glass.md`, `sf-symbols.md`, `icon-design.md`, `platform-specific.md`) plus a design-philosophy summary and a core-principles checklist in `SKILL.md`. `apple-app-ship` already treats `apple-design` as a companion dependency for its plan-and-build phase; it now ships in this repo instead of relying on it being installed separately.
- 2b68960: add apple-design skill

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
