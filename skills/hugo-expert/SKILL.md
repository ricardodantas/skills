---
name: hugo-expert
description: Expert guidance for building and maintaining Hugo (gohugo.io) static sites — templating and layouts, theme creation and customization, content modeling, configuration and Hugo Modules, performance and the asset pipeline, deployment and CI, multilingual/i18n, SEO and feeds, and version upgrades. Fetches version-appropriate Hugo docs via Context7. Use inside or when starting a Hugo repo — building or customizing a theme, fixing or writing Go templates and partials, configuring hugo.toml or modules, optimizing builds, deploying, adding i18n or SEO, upgrading Hugo, or any "Hugo best practices" question. For writing blog posts in the author's voice, use hugo-write-post.
---

# Hugo Expert

Deep help with Hugo static sites. This skill carries durable Hugo best-practices and pins live
documentation lookups to the repo's actual Hugo version — Hugo ships frequently and APIs change, so
verify current syntax against the docs rather than from memory.

## Preflight — live docs via find-docs

Current Hugo syntax, template functions, and config keys are fetched with the `find-docs` skill
(Context7). Confirm it's available (it appears in your available skills); if it's missing, tell the
user and offer to install it — `npx skills find find-docs`. Without it, say so and proceed from
general knowledge, flagging that version-specific details may be stale.

## 1. Detect the target version

Run the detector at the repo root to pin doc lookups to the right version:

```bash
"<skill-dir>/scripts/detect_hugo.py" .
```

It reports the config file/format, the pinned Hugo version, Hugo Modules usage, an
extended-vs-standard hint, and configured themes. For a **brand-new repo** (`is_new_repo`), use the
**latest** Hugo release — look it up (`hugo version`, the GitHub releases page, or Context7); never
assume a hardcoded version.

## 2. Fetch current docs when it matters

Before asserting exact template-function signatures, config keys, or version-specific behavior, use
the `find-docs` skill to pull the current Hugo docs (library `Hugo` → `/gohugoio/hugo`). Query one
specific topic at a time, and pin the repo's version when it declares one. Rely on the references
below for durable practice; reach for live docs when the detail is version-sensitive.

## 3. Route to the reference for the task

Read only the file(s) the task needs:

| Task | Reference |
|------|-----------|
| Go templates, partials, blocks, render hooks, lookup order | [references/templating.md](references/templating.md) |
| Creating/customizing a theme, overriding, publishing | [references/themes.md](references/themes.md) |
| Sections, page/leaf bundles, taxonomies, front matter, archetypes | [references/content-modeling.md](references/content-modeling.md) |
| `hugo.toml`/environments, Hugo Modules, mounts | [references/config-modules.md](references/config-modules.md) |
| Hugo Pipes, image processing, minify/fingerprint, caching | [references/performance.md](references/performance.md) |
| Netlify/Vercel/Pages, CI, `HUGO_VERSION`, `baseURL` | [references/deployment.md](references/deployment.md) |
| Version bumps, deprecations, extended vs standard | [references/upgrade-migration.md](references/upgrade-migration.md) |
| Multilingual sites, translations | [references/i18n.md](references/i18n.md) |
| Sitemap, RSS/output formats, meta/OpenGraph, structured data | [references/seo-feeds.md](references/seo-feeds.md) |

## 4. Best-practice bar (holds across versions)

- Prefer configuration over hardcoding; keep environment-specific values in `config/<env>/`.
- Build themes as **Hugo Modules** over copying files; override by shadowing layouts in the project.
- Compose layouts from **partials** and **render hooks**; don't duplicate markup across templates.
- Route CSS/JS/images through the **asset pipeline** (Hugo Pipes) — fingerprint and minify for production.
- **Pin `HUGO_VERSION`** in CI/deploy so local and production builds match.
- Verify with `hugo server` during work and a clean `hugo --minify` before shipping; treat build
  **warnings and deprecations** as work to resolve.

## 5. Writing blog posts → delegate

To write a blog post in the author's established voice, use the `hugo-write-post` skill rather than
drafting prose here.

## 6. Validate the work

Confirm the site still builds: `hugo` completes without errors, `hugo server` renders the change,
and no new deprecation warnings were introduced. Report the outcome and any warnings.
