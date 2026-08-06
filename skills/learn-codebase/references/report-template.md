# CODEBASE_OVERVIEW.md template

Write this file into the analyzed repo. Keep it factual and verified against the code — every
claim should be traceable to a file. Fill sections that apply; delete those that don't. Prefer
concrete file paths and commands over prose.

```markdown
# Codebase Overview

## Summary
One paragraph: what this project is, who uses it, and the primary problem it solves.

## Tech stack
- **Languages:** …
- **Frameworks / runtime:** …
- **Build / package manager:** …
- **Datastores / external services:** …
- **Skills applied:** which installed skills informed this overview.

## Architecture
Major components and their responsibilities, and how they relate. A small text diagram helps:

    [client] -> [api/server] -> [service layer] -> [db]

For each component: what it owns, its boundary, and the key directory/file.

## Key modules
| Path | Responsibility |
| --- | --- |
| `src/…` | … |

## Data & control flow
Trace one or two representative paths end to end (e.g. an HTTP request, a CLI command, a job).
Note where state/config lives and how components communicate.

## Entry points
Where execution starts — `main`, server bootstrap, CLI, route registration — with file paths.

## Build, run, and test
Exact commands, sourced from manifests/CI (not guessed):

    # install
    …
    # run (dev)
    …
    # test
    …
    # build / lint
    …

## Conventions
Patterns the repo follows: structure, naming, error handling, state management, testing style.
Note anything a new contributor must imitate.

## Risks & rough edges
TODOs, fragile areas, missing tests, dead code, known tech debt — with file references.

## Glossary / where to look next
Domain terms and the best files to start reading for each major area.
```
