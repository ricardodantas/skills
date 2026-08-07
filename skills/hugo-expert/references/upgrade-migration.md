# Upgrades & migration

Always fetch the target version's changes via `find-docs` before upgrading
(`docs /gohugoio/hugo/<version> "deprecations and breaking changes"`).

## Before upgrading

- Detect the current pinned version (`scripts/detect_hugo.py`) and note the target (usually latest).
- Read the release notes between current and target — Hugo announces deprecations before removing
  them. Fetch them; don't assume.

## Doing the upgrade

- Bump `HUGO_VERSION` in every place it's pinned (config `[module.hugoVersion]`, `netlify.toml`, CI
  workflows) — keep them consistent.
- For module-based sites, update modules too: `hugo mod get -u ./...` then `hugo mod tidy`.
- Rebuild with `hugo` and resolve **every** warning/deprecation it prints — that output is the
  migration checklist.

## Extended vs standard

- **Extended** adds Sass/SCSS transpilation and WebP encoding. If the build errors on `css.Sass`
  or image encoding, the environment is running the standard binary — switch to Extended.

## Guidance

- Upgrade in a branch, diff the built `public/` (or eyeball key pages) before merging.
- Prefer small, frequent bumps over one large jump — fewer deprecations to untangle at once.
