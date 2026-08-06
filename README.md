[![skills.sh](https://skills.sh/b/ricardodantas/skills)](https://skills.sh/ricardodantas/skills)

# Skills

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Skills teach Claude how to complete specific tasks in a repeatable way.

For more information, check out:
- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)

# About This Repository

This repository contains agent skills for understanding and working within codebases. It is structured like [anthropics/skills](https://github.com/anthropics/skills) so new skills can be added easily.

Each skill is self-contained in its own folder under [`skills/`](./skills) with a `SKILL.md` file containing the instructions and metadata that Claude uses.

Current skills:
- [`skills/learn-codebase`](./skills/learn-codebase) — Discovers the installed agent skills, applies the ones relevant to a repo's stack, and produces a codebase briefing plus a saved `CODEBASE_OVERVIEW.md`.

# Skill Sets
- [./skills](./skills): The skills in this repository, one folder each
- [./template](./template): Skill template

# Try in Claude Code

You can register this repository as a Claude Code Plugin marketplace by running the following command in Claude Code:
```
/plugin marketplace add ricardodantas/skills
```

Then, to install the skills:
1. Select `Browse and install plugins`
2. Select `learn-about-repo-skills`
3. Select `Install now`

Alternatively, install the plugin directly via:
```
/plugin install learn-about-repo-skills@learn-about-repo-skills
```

After installing, use a skill by just mentioning it. For instance: "Use the learn-codebase skill to give me an overview of this repository."

## Install with the skills CLI (skills.sh)

This repo is also installable via the [skills.sh](https://skills.sh) CLI. Requires Node.js.

Install everything in the repo (interactive picker):
```
npx skills add ricardodantas/skills
```

Install just the `learn-codebase` skill, globally (available to all your agents):
```
npx skills add ricardodantas/skills --skill learn-codebase -g
```

Useful flags:
- `-l` — list the skills in the repo without installing
- `-a <agent>` — install to a single agent (e.g. `-a claude`) instead of all
- `-y` — skip confirmation prompts

Use a skill once without installing (generates a prompt):
```
npx skills use ricardodantas/skills@learn-codebase
```

Remove an installed skill:
```
npx skills remove learn-codebase
```

Installs are counted anonymously by the CLI and feed the skills.sh leaderboard.

# Creating a Basic Skill

Skills are simple to create — just a folder with a `SKILL.md` file containing YAML frontmatter and instructions. You can use the **template-skill** in [`./template`](./template) as a starting point:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter requires only two fields:
- `name` - A unique identifier for your skill (lowercase, hyphens for spaces; must match the folder name)
- `description` - A complete description of what the skill does and when to use it

## Adding a skill to this repository

1. Copy the template into a new folder under `skills/`:
   ```bash
   cp -r template skills/my-skill
   ```
2. Set `name: my-skill` in `skills/my-skill/SKILL.md`, add a trigger-rich `description`, and write the instructions. Add optional `scripts/`, `references/`, and `assets/` subfolders as needed.
3. Register it in [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) under `plugins[].skills`:
   ```json
   "./skills/my-skill"
   ```
4. Add it to the skills list above.
