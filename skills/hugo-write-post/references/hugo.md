# Hugo reference

What `hugo-write-post` needs to place a post correctly. See the official docs at
https://gohugo.io/documentation/ for anything not covered here.

## Content organization

- Posts live under `content/`, usually in a section dir — commonly `content/posts/` or
  `content/blog/` (check the site; whatever the existing posts use is the convention).
- A **section** is a top-level dir under `content/`. `_index.md` is its list page; regular files
  are single pages.
- **Page bundles**: a leaf bundle is a directory with an `index.md` plus co-located resources
  (images, etc.); a plain single page is just `<slug>.md`. Match whichever the author already uses.
- Filename becomes the URL slug unless a `slug`/`url` front-matter field overrides it. Mirror the
  author's filename pattern (e.g. `my-post-title.md`, or dated `2026-08-07-title.md`).

## Front matter

Every content file starts with front matter in one of three formats — use the one the author uses:

- **TOML**, fenced by `+++`:
  ```toml
  +++
  title = "Post title"
  date = 2026-08-07T10:00:00+02:00
  draft = false
  tags = ["hugo", "writing"]
  categories = ["blog"]
  description = "One-line summary."
  +++
  ```
- **YAML**, fenced by `---`:
  ```yaml
  ---
  title: "Post title"
  date: 2026-08-07T10:00:00+02:00
  draft: false
  tags: ["hugo", "writing"]
  categories: ["blog"]
  description: "One-line summary."
  ---
  ```
- **JSON**, fenced by `{ … }`.

Common fields: `title`, `date`, `lastmod`, `draft`, `tags`, `categories`, `description`,
`summary`, `slug`, `aliases`, `weight`, `keywords`, `author`. Only use the fields the author's own
posts use — don't add fields they never set.

## Creating content

Prefer Hugo's generator so the site's archetype and default front matter are applied:

```bash
hugo new content posts/my-post.md
```

- **Archetypes** (`archetypes/`) are templates for new content. `archetypes/default.md` (or a
  section-specific `archetypes/posts.md`) defines the front matter `hugo new` scaffolds. Read it to
  see the exact fields/format the site expects.
- If the Hugo CLI isn't installed, create the file by hand and copy the front-matter shape from the
  newest existing post in the same section.

## Taxonomies

Hugo's default taxonomies are `tags` and `categories`. Sites can define others in config
(`[taxonomies]`). Draw tag/category values from the author's existing vocabulary rather than
inventing new ones.

## Build and preview

```bash
hugo server -D        # local live-reload preview, includes drafts (-D / --buildDrafts)
hugo                  # production build into public/
hugo --buildDrafts    # include drafts in a build
```

## Detecting the author's conventions

To match the author, inspect (the analyzer script automates most of this):

1. **Config** (`hugo.toml`/`hugo.yaml`/`config/`) — base URL, taxonomies, content settings.
2. **`archetypes/`** — the intended front-matter shape for new posts.
3. **The most recent posts** under the section — the living example of format, fields, filename
   pattern, length, tone, and structure. Trust these over the archetype if they differ.
