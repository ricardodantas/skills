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
/plugin install ricardodantas-skills@ricardodantas-skills
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

In your agent, just mention a skill by name — for example:

> "Use the learn-codebase skill to give me an overview of this repository."

Model-invoked skills are also reached for automatically when a task fits.

## Why These Skills Exist

Small, composable skills — not a framework. Each solves one real problem an agent hits:

- **learn-codebase** — Landing in an unfamiliar repo is slow; agents guess from file names and miss the real architecture. This skill treats your installed skills as a toolbox: it detects the stack, picks the skills that fit, traces the code end to end, and leaves a `docs/CODEBASE_OVERVIEW.md` behind.
- **apple-app-ship** — Shipping an Apple app spans architecture, polish, a marketing site, App Store screenshots, and submission — each a specialty. This skill orchestrates the workflow, checking for and delegating to the right companion skill at each phase instead of re-teaching everything.
- **terminal-screenshots** — Hand-recorded terminal GIFs drift and look inconsistent. VHS `.tape` scripts make them reproducible and re-runnable in CI.
- **podman-browser** — A plain HTTP fetch returns empty markup on JavaScript-rendered pages. This renders the page headlessly in a Podman + Playwright container and returns the real text or HTML.
- **hugo-write-post** — Blog posts written by an agent read generic. This skill learns your voice from your existing Hugo posts and drafts a new one on a given topic that matches it, placed with the right front matter — delegating the writing to `social-content`.
- **hugo-expert** — Hugo ships often and its APIs move, so cached knowledge goes stale. This skill pairs durable Hugo best-practices (themes, templating, config, performance, deploy, i18n, SEO) with live, version-pinned docs fetched via Context7 — expert help that stays current with the repo's Hugo version.

## Reference

Skills split on one axis — who can invoke them. **User-invoked** skills run only when you type them; their job is to orchestrate. **Model-invoked** skills can be invoked by you _or_ reached for automatically by the agent when the task fits.

### Engineering

**Model-invoked**

- **[learn-codebase](./skills/learn-codebase/SKILL.md)** — Discovers the installed agent skills, applies the ones relevant to a repo's stack, and maps its architecture, modules, data flow, conventions, and build/run/test — producing an in-conversation briefing plus a saved `docs/CODEBASE_OVERVIEW.md`.
- **[apple-app-ship](./skills/apple-app-ship/SKILL.md)** — End-to-end workflow for building, polishing, and shipping native Apple platform apps (SwiftUI) — architecture, marketing website, App Store screenshots, and App Store Connect submission. Orchestrates specialized companion skills at each phase (checking they're installed first) rather than re-teaching the craft.
- **[docs-update-expert](./skills/docs-update-expert/SKILL.md)** — Reconciles a repo's docs (README, `docs/`, CHANGELOG, agent docs, API refs, inline comments) with its current state. Orchestrates `learn-codebase` to model the repo, `writing-for-agents` for agent-facing docs, and `find-docs` for version-specific details.

### Tooling

**Model-invoked**

- **[terminal-screenshots](./skills/terminal-screenshots/SKILL.md)** — Generate reproducible terminal screenshots and animated GIF/MP4/WebM recordings from VHS (Charmbracelet) `.tape` scripts, for docs, READMEs, and CLI demos.
- **[podman-browser](./skills/podman-browser/SKILL.md)** — Headless browser automation via Podman + Playwright (Chromium) to fetch and scrape JavaScript-rendered pages as text or HTML.

### Content

**Model-invoked**

- **[hugo-write-post](./skills/hugo-write-post/SKILL.md)** — In a Hugo (gohugo.io) repo, learns the author's writing style from existing posts and writes a new post on a given topic that matches that voice, placed with correct Hugo front matter. Delegates the prose to `social-content`.
- **[hugo-expert](./skills/hugo-expert/SKILL.md)** — Expert Hugo (gohugo.io) guidance across themes, templating, content modeling, config/modules, performance, deployment, i18n, SEO, and upgrades — fetching version-appropriate docs via Context7 (`find-docs`) for the repo's Hugo version. Delegates blog-post writing to `hugo-write-post`.

## Repository layout

```
.
├── .claude-plugin/marketplace.json   # plugin/marketplace manifest
├── skills/                           # one directory per skill
│   ├── learn-codebase/
│   ├── terminal-screenshots/
│   ├── podman-browser/
│   ├── apple-app-ship/
│   ├── hugo-write-post/
│   └── hugo-expert/
├── template/SKILL.md                 # blank starting point for a new skill
└── README.md
```

### Adding a skill

1. Copy the template into a new folder under `skills/`: `cp -r template skills/my-skill`.
2. Set `name: my-skill` in `skills/my-skill/SKILL.md` (must match the folder), write a trigger-rich `description` and the instructions. Add optional `scripts/`, `references/`, `assets/` as needed.
3. Register it in [`.claude-plugin/marketplace.json`](./.claude-plugin/marketplace.json) under `plugins[].skills` as `"./skills/my-skill"`.
4. Add it to the Reference section above.
5. Record a changeset so the release versions it: `pnpm changeset` (see [AGENTS.md](./AGENTS.md#conventions)).
