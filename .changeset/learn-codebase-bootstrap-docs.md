---
"skills": minor
---

learn-codebase: a new step 6 creates `README.md` and `AGENTS.md` + `CLAUDE.md` (which imports `AGENTS.md`) when the analyzed repo has none. It checks for any README variant and for the common agent-guidance files (AGENTS.md, CLAUDE.md, GEMINI.md, Copilot, Cursor, Windsurf, Cline) first, never overwrites existing files, and fills the new ones from the verified analysis using the templates in `references/bootstrap-docs.md`.
