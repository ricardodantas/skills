# learn-about-repo skills

A collection of [agent skills](https://code.claude.com/docs/en/skills) for understanding
and working within codebases. Structured like
[anthropics/skills](https://github.com/anthropics/skills) so new skills can be added easily.

## Layout

```
.
├── .claude-plugin/
│   └── marketplace.json   # plugin/marketplace manifest listing the skills
├── skills/                # one directory per skill
│   └── learn-codebase/
├── template/
│   └── SKILL.md           # blank starting point for a new skill
└── README.md
```

## Skills

| Skill | Description |
| --- | --- |
| [`learn-codebase`](skills/learn-codebase) | Discovers the installed agent skills, applies the ones relevant to the repo's stack, and produces a codebase briefing plus a saved `CODEBASE_OVERVIEW.md`. |

## Adding a skill

1. Scaffold a new folder under `skills/`:

   ```bash
   cp -r template skills/my-skill        # or use skill-creator's init_skill.py
   ```

   Set `name: my-skill` in `skills/my-skill/SKILL.md` (must match the folder name) and write a
   trigger-rich `description`.

2. Add optional `scripts/`, `references/`, and `assets/` subfolders as needed.

3. Register it in `.claude-plugin/marketplace.json` under `plugins[].skills`:

   ```json
   "./skills/my-skill"
   ```

4. Add a row to the Skills table above.

## Packaging a skill

Use skill-creator's packager to produce a distributable `.skill` archive (git-ignored):

```bash
package_skill.py skills/my-skill .
```
