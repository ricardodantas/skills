# skills

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
