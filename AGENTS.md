# AGENTS.md

Guidance for AI agents working in this repository.

## What this repo is

A monorepo of **agent skills** — reusable capabilities an AI agent loads to do specialized
tasks. It follows the [`anthropics/skills`](https://github.com/anthropics/skills) layout so new
skills can be added and published (via [skills.sh](https://skills.sh) and the Claude Code plugin
marketplace) with minimal ceremony. See [README.md](./README.md) for user-facing install docs.

## Layout

```
.
├── .claude-plugin/marketplace.json   # plugin manifest; every published skill is listed here
├── skills/                           # one directory per skill
│   └── learn-codebase/
│       ├── SKILL.md                  # instructions + YAML frontmatter (required)
│       ├── scripts/                  # executable helpers (optional)
│       └── references/               # docs loaded on demand (optional)
├── template/SKILL.md                 # blank starting point for a new skill
├── AGENTS.md                         # this file
├── CLAUDE.md                         # imports this file
└── README.md
```

## SKILL.md rules (enforced by validation)

- Frontmatter has exactly two fields: `name` and `description`. No others.
- `name`: hyphen-case (`[a-z0-9-]`), no leading/trailing/double hyphens, **must match the folder name**.
- `description`: what the skill does **and** when to use it (triggers/keywords). No angle brackets (`<`/`>`). Max 1024 chars.
- Keep the body lean; move long reference material into `references/` and point to it from SKILL.md.
- Do **not** add README/CHANGELOG/INSTALL files inside a skill folder — only what the skill needs.

## Adding a skill

1. `cp -r template skills/my-skill` (or use skill-creator's `init_skill.py`).
2. Write `skills/my-skill/SKILL.md` (set `name: my-skill`, a trigger-rich `description`, the instructions).
3. Register it in `.claude-plugin/marketplace.json` under `plugins[].skills` as `"./skills/my-skill"`.
4. Add it to the **Reference** section of `README.md`.

A skill is not "done" until it is listed in `marketplace.json` — otherwise it won't publish.

## Validate & package

Use the **skill-creator** skill's scripts (they live in that skill, not this repo):

```bash
quick_validate.py skills/my-skill          # checks frontmatter/naming/structure
package_skill.py  skills/my-skill .        # builds my-skill.skill (git-ignored)
```

If a skill ships a script with non-trivial logic, keep its runnable self-check
(e.g. `scripts/list_skills.py --self-check`) working.

## Conventions

- `*.skill` archives are build artifacts — git-ignored, never committed.
- The `learn-codebase` skill writes its generated repo overview to `docs/CODEBASE_OVERVIEW.md`.
- Commits include the trailer: `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
- Prefer the smallest change that fully solves the task; don't add speculative abstractions.
