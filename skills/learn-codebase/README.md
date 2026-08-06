# Learn Codebase

> An agent skill for understanding an unfamiliar codebase — fast.

Point an agent at a repo and get a real briefing: architecture, key modules, data flow, how to build/run/test, and where the rough edges are. Instead of guessing from file names, this skill first discovers which agent skills you already have installed, then reaches for the ones relevant to *this* repo's stack to do the analysis.

## What it does

1. **Discovers** the available agent skills (from the injected list, or by scanning skill dirs with `scripts/list_skills.py`).
2. **Detects** the repo's stack from manifests and config.
3. **Selects** the skills that fit (design, review, debugging, language/framework guidance).
4. **Analyzes** the code end to end — architecture, modules, data/control flow, entry points, build/run/test, conventions, risks.
5. **Outputs** an in-conversation briefing **and** writes `docs/CODEBASE_OVERVIEW.md` into the repo.

## Usage

In your agent, just mention it:

> "Use the learn-codebase skill to give me an overview of this repository."

## Install

This skill lives in [`ricardodantas/skills`](https://github.com/ricardodantas/skills). Install it with the [skills.sh](https://skills.sh) CLI:

```bash
npx skills add ricardodantas/skills --skill learn-codebase
```

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill instructions and metadata |
| `scripts/list_skills.py` | Scans skill directories for full `name: description` pairs |
| `references/report-template.md` | Structure for the generated `docs/CODEBASE_OVERVIEW.md` |

See [SKILL.md](SKILL.md) for the full workflow.
