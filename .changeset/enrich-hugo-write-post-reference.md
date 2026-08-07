---
"skills": patch
---

Enrich `hugo-write-post`'s Hugo reference (verified against the official gohugoio/hugo docs): document the `hugo new content --kind` archetype flag, note that archetypes are Go templates with variables like `{{ .Date }}`/`{{ .Name }}` that Hugo fills in (don't copy literally), and add `hugo convert toTOML/toYAML/toJSON` as a front-matter format-normalization failsafe.
