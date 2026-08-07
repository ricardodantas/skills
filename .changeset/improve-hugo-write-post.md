---
"skills": patch
---

Improve `hugo-write-post`: invoke `analyze_style.py` by its skill-directory path (the working directory at runtime is the Hugo repo, not the skill folder), handle the cold-start case of a blog with too few posts to learn from, and add a content-integrity guardrail (no fabricated facts, quotes, or stats — leave marked `TODO:` placeholders instead).
