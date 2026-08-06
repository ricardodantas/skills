# AI agent skills

[![skills.sh](https://skills.sh/b/ricardodantas/skills)](https://skills.sh/ricardodantas/skills)

Agent skills for real engineering work — starting with understanding unfamiliar codebases, plus small utilities for terminal media and headless web scraping.

The headline skill, `learn-codebase`, first discovers which agent skills you already have installed, then reaches for the ones relevant to *this* repo's stack to do the analysis — so the more skills you have, the smarter it gets. Alongside it are focused tools: `terminal-screenshots` (VHS-based terminal GIFs/screenshots) and `podman-browser` (Podman + Playwright page scraping).

## Installation (30-second setup)

Two ways in, two philosophies. **The [Claude Code plugin](https://code.claude.com/docs/en/plugins)** installs the set as a managed bundle that updates when this repo ships — you subscribe rather than fork. **[skills.sh](https://skills.sh/ricardodantas/skills)** copies editable skill files into your project, so you can hack on them and make them your own. Pick one — installing both leaves you with every skill twice.

### 1. Get the skills

<details>
<summary><strong>Claude Code</strong></summary>

Add this repo as a plugin marketplace, then install the plugin:

```bash
/plugin marketplace add ricardodantas/skills
/plugin install learn-about-repo-skills@learn-about-repo-skills
```

Updates arrive when you run `/plugin update`.

</details>

<details>
<summary><strong>Codex, and other agents</strong></summary>

```bash
npx skills@latest add ricardodantas/skills
```

Pick the skills you want and which coding agents to install them on. Requires Node.js.

</details>

<details>
<summary><strong>For tinkerers</strong></summary>

Use the same installer, on any agent — including Claude Code:

```bash
npx skills@latest add ricardodantas/skills
```

It writes the skills into your repo as ordinary files you own and can edit. Nothing updates behind your back; pull the latest changes when you want them with `npx skills update`.

Handy flags: `-l` lists the skills without installing, `--skill learn-codebase -g` installs just that one globally, `-a <agent>` targets a single agent, `-y` skips prompts. Use once without installing via `npx skills use ricardodantas/skills@learn-codebase`, and remove with `npx skills remove learn-codebase`.

</details>

### 2. Run it

In your agent, just mention the skill:

> "Use the learn-codebase skill to give me an overview of this repository."

It produces an in-conversation briefing and writes a `CODEBASE_OVERVIEW.md` to the repo.

## Why This Skill Exists

**The problem.** Landing in an unfamiliar codebase is slow. Agents guess from file names, miss the real architecture, and skip the one command that actually runs the tests. And most "explain this repo" prompts throw away the specialized skills you already have installed.

**The fix.** `learn-codebase` treats your installed skills as a toolbox. It reads the live list of available skills, detects the repo's stack from its manifests and config, selects the skills that fit (design, review, debugging, language/framework guidance), and applies them to trace the code end to end — then leaves behind a `CODEBASE_OVERVIEW.md` you can keep.

## Reference

Skills split on one axis — who can invoke them. **User-invoked** skills run only when you type them; their job is to orchestrate. **Model-invoked** skills can be invoked by you _or_ reached for automatically by the agent when the task fits.

### Engineering

**Model-invoked**

- **[learn-codebase](./skills/learn-codebase/SKILL.md)** — Discovers the installed agent skills, applies the ones relevant to a repo's stack, and maps its architecture, modules, data flow, conventions, and build/run/test — producing an in-conversation briefing plus a saved `CODEBASE_OVERVIEW.md`.

### Tooling

**Model-invoked**

- **[terminal-screenshots](./skills/terminal-screenshots/SKILL.md)** — Generate reproducible terminal screenshots and animated GIF/MP4/WebM recordings from VHS (Charmbracelet) `.tape` scripts, for docs, READMEs, and CLI demos.
- **[podman-browser](./skills/podman-browser/SKILL.md)** — Headless browser automation via Podman + Playwright (Chromium) to fetch and scrape JavaScript-rendered pages as text or HTML.

## Repository layout

```
.
├── .claude-plugin/marketplace.json   # plugin/marketplace manifest
├── skills/                           # one directory per skill
│   ├── learn-codebase/
│   ├── terminal-screenshots/
│   └── podman-browser/
├── template/SKILL.md                 # blank starting point for a new skill
└── README.md
```

### Adding a skill

1. Copy the template into a new folder under `skills/`: `cp -r template skills/my-skill`.
2. Set `name: my-skill` in `skills/my-skill/SKILL.md` (must match the folder), write a trigger-rich `description` and the instructions. Add optional `scripts/`, `references/`, `assets/` as needed.
3. Register it in [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) under `plugins[].skills` as `"./skills/my-skill"`.
4. Add it to the Reference section above.
