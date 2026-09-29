---
name: learn-codebase
description: Learn and explain an unfamiliar codebase by first discovering which agent skills are installed, then applying the ones relevant to this repo's stack to map its architecture, modules, data flow, conventions, and how to build/run/test it. Produces an in-conversation briefing and a saved docs/CODEBASE_OVERVIEW.md, and creates a README.md and AGENTS.md/CLAUDE.md when the repo has none. Use when the user asks to "understand/learn/explain this repo", "onboard me to this codebase", "give me an overview of the project", "how does this codebase work", "this repo has no README/AGENTS.md", or when starting work in a repo you have not seen before.
---

# Learn Codebase

## Overview

Orchestrate the *other* installed skills to understand a codebase. First find out what
skills exist, pick the ones that fit this repo, then use them to produce a briefing plus a
saved `docs/CODEBASE_OVERVIEW.md`. If the repo has no README or no agent guidance file, create
them from the same analysis.

## Workflow

1. **Discover skills** — see [what's available](#1-discover-available-skills).
2. **Detect the stack** — cheap signals reveal languages/frameworks/tooling.
3. **Select relevant skills** — match stack + task to skills.
4. **Analyze** — apply the selected skills to learn the repo.
5. **Output** — deliver a briefing and write `docs/CODEBASE_OVERVIEW.md`.
6. **Bootstrap missing docs** — create `README.md` and `AGENTS.md` + `CLAUDE.md` if absent.

## 1. Discover available skills

The agent's injected `<available_skills>` list is the primary source — read it first.
It is frequently **truncated** ("Additional skills available…"), so when full descriptions
are needed for selection, run the bundled scanner to recover complete `name: description`
pairs:

```bash
scripts/list_skills.py            # scans ~/.agents/skills, ~/.claude/skills, ./.claude/skills, ./skills
scripts/list_skills.py /path/to/skills   # add a non-standard location
```

Invoke it by its full path in *this skill's* directory — your cwd is usually the target repo,
not the skill folder.

Do not hardcode a skill catalog — always read the live list, since installed skills change.

## 2. Detect the stack

Read only what's cheap and decisive before committing to skills:

- **Docs first**: `README`, `AGENTS.md` / `CLAUDE.md`, `CONTRIBUTING`, `docs/` — the
  highest-signal source for purpose, conventions, and the *real* build/run/test commands.
  Note which of these are missing. Step 6 needs that list.
- **Manifests / lockfiles**: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`,
  `*.csproj`, `Gemfile`, `pom.xml`, `Package.swift`, `*.xcodeproj`.
- **Config**: framework configs (next.config, vite, tailwind, astro), `Dockerfile`,
  compose files, CI under `.github/`, `Makefile`.
- **Monorepo?**: check for workspaces (pnpm/yarn/npm `workspaces`, `packages/*`, `apps/*`,
  Cargo/Go workspaces) and analyze each package, not just the root.
- **Shape**: top-level dirs, file-extension histogram, entry points, test dirs.

Skip vendored/generated dirs (`node_modules`, `.git`, `dist`, `build`, `target`, `vendor`,
`.venv`) — they skew signals and waste effort.

## 3. Select relevant skills

Match stack signals and the user's goal to skills from step 1. Selection is
**category-based** — map signals to the *kind* of skill, then pick whatever concrete skills
in the live list fit. Only pick skills that clearly apply; ignore the rest.

| Signal / goal | Skill category to look for | Examples often present |
| --- | --- | --- |
| Any codebase | Structure & design comprehension | `codebase-design`, `code-review` |
| Understanding tests / adding them | Testing practice | `tdd`, `swift-testing-pro` |
| Bug or unclear failure | Debugging | `diagnosing-bugs` |
| TypeScript / JS | Language deep-dives | `typescript-advanced-types` |
| React / Next / Vercel | Framework guidance | `vercel-react-best-practices` |
| Swift / Apple platforms | Framework guidance | `swiftui-pro`, `swiftui-expert-skill`, `apple-design` |
| Frontend / UI | Design & UX | `frontend-design` |
| Docs to read/produce | Summarization & writing | `summarize`, `writing-for-agents` |
| "Find a skill for X" gap | Skill discovery | `find-skills` |

When a skill fits, **read its SKILL.md** and apply its guidance during analysis. Prefer one or
two high-leverage skills over loading many.

## 4. Analyze

Apply the selected skills to trace the repo end to end and capture:

- **Purpose** — what the project does and who uses it.
- **Architecture** — major components/modules and their responsibilities and boundaries.
- **Data & control flow** — request/render/job lifecycles; where state lives.
- **Entry points** — how execution starts (main, server, CLI, routes).
- **Build / run / test** — the exact commands, from manifests and CI.
- **Conventions** — patterns, naming, error handling, folder structure the repo follows.
- **Risks / rough edges** — TODOs, dead code, fragile spots, missing tests.

For large repos, dispatch parallel `explore` sub-agents on independent areas (e.g. backend,
frontend, infra) and merge findings. Verify claims against the code — don't infer from names.

## 5. Output

Deliver **both**:

1. A concise briefing in the conversation (lead with purpose + architecture).
2. A written report at `docs/CODEBASE_OVERVIEW.md` in the analyzed repo, following
   [references/report-template.md](references/report-template.md). Create the `docs/` folder if it
   doesn't exist. Anchor the report with the current date and commit SHA. If the file already
   exists, reconcile/update it rather than blindly overwriting.

## 6. Bootstrap missing docs

Check the repo root (and, in a monorepo, only the root unless the user asks for per-package docs).
Use the templates in [references/bootstrap-docs.md](references/bootstrap-docs.md).

- **README**: if no `README*` file exists (any case or extension, e.g. `readme.md`,
  `README.rst`, `README.txt`), create `README.md`.
- **Agent guidance**: if none of these exist, create `AGENTS.md` plus a `CLAUDE.md` that imports it:
  `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
  `.github/instructions/`, `.cursorrules`, `.cursor/rules/`, `.windsurfrules`, `.clinerules`.
  If only some exist, leave them alone. Don't add a second, parallel set.

Rules:

- Only create files that are missing. Never overwrite, rename, or restructure an existing file.
  If an existing one looks stale or thin, say so in the briefing and don't edit it.
- Build the content from the step 4 analysis, not from assumptions. Take commands from manifests
  and CI. Leave out any section you couldn't verify.
- Link both new files to `docs/CODEBASE_OVERVIEW.md` instead of copying the architecture into them.
- In the briefing, list which files were created and which already existed.

Write the report and any bootstrapped files but do **not** commit them automatically — leave that
to the user.
