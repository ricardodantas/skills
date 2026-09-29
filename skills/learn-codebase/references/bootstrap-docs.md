# Bootstrapping missing docs

Create these only when the repo has **none** of the matching files (see the detection lists in
SKILL.md). Never overwrite or restructure an existing README or agent file. Fill every section
from the verified analysis. Write "Unknown" or leave a section out rather than guess. Commands
must come from manifests, scripts, or CI. Delete sections that don't apply.

## README.md

Human-facing. Put it at the repo root.

```markdown
# <Project name>

<One or two sentences: what it does and who it's for.>

## Features
- …

## Requirements
- <runtime + version, from manifests/tool-versions/CI>

## Getting started

    # install
    …
    # run (dev)
    …

## Usage
<The main CLI invocation, API call, or UI entry point, with a short example.>

## Development

    # test
    …
    # lint / build
    …

## Project structure
| Path | Purpose |
| --- | --- |
| `src/…` | … |

See [docs/CODEBASE_OVERVIEW.md](docs/CODEBASE_OVERVIEW.md) for the architecture.

## License
<From LICENSE / manifest `license` field. Leave this section out if neither exists.>
```

## AGENTS.md

Agent-facing. Write it for an AI agent that is about to edit the code. Keep it short and
imperative, and include only what an agent can't easily work out from the code. Put it at the
repo root.

```markdown
# AGENTS.md

Guidance for AI agents working in this repository.

## Overview
<One paragraph: what the project is, and the stack.>

## Commands
    # install
    …
    # test (all / single file)
    …
    # lint / format / typecheck
    …
    # build
    …

## Layout
<Top-level dirs and what lives in each, plus where the entry points are.>

## Conventions
- <Patterns to imitate: naming, error handling, state, test style, import rules.>
- <Generated or vendored paths that must not be edited by hand.>

## Workflow
- <Branching, commit-message, changelog/changeset rules, or PR checks that CI enforces.>

See [docs/CODEBASE_OVERVIEW.md](docs/CODEBASE_OVERVIEW.md) for the full architecture.
```

## CLAUDE.md

Create it next to a new `AGENTS.md` so Claude Code picks up the same guidance without a second
copy to maintain:

```markdown
# CLAUDE.md

This repository's agent guidance lives in [AGENTS.md](./AGENTS.md).

@AGENTS.md
```
