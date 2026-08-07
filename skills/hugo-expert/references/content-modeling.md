# Content modeling

Fetch current front-matter fields and bundle rules via `find-docs`
(`docs /gohugoio/hugo "page bundles and front matter"`).

## Sections & bundles

- A **section** is a top-level directory under `content/`; `_index.md` is its list (branch) page.
- **Leaf bundle**: a directory with `index.md` + co-located resources (images, data) — a single
  page that owns its assets. **Branch bundle**: a directory with `_index.md` — a list page with
  descendants. Choose leaf bundles for posts that carry their own images.
- Access co-located files as **page resources** (`.Resources.GetMatch`) — the clean way to handle
  per-post images, including through image processing.

## Front matter & archetypes

- Pick one front-matter format for the site (TOML `+++`, YAML `---`, or JSON) and keep it
  consistent; only use fields the site actually consumes.
- **Archetypes** (`archetypes/`) template new content; `hugo new content <section>/<slug>.md`
  applies the matching archetype (`archetypes/<section>.md`, else `default.md`). Keep archetypes in
  sync with what layouts expect.

## Taxonomies

- Default taxonomies are `tags` and `categories`; define others under `[taxonomies]` in config.
- Keep taxonomy terms controlled — reuse existing terms rather than proliferating near-duplicates.

## Guidance

- Model content around how it's queried in templates (`where .Site.RegularPages "Section" "posts"`),
  not around folder aesthetics.
- Use **data files** (`data/`) for structured non-page data (authors, nav) instead of hardcoding in
  templates.
