# SEO, feeds & output formats

Fetch current output-format and templating details via `find-docs`
(`docs /gohugoio/hugo "custom output formats and rss"`).

## Feeds & output formats

- Hugo generates RSS and a sitemap for list pages by default. Customize RSS by overriding the RSS
  output template rather than disabling it.
- Add machine-readable outputs (JSON search index, Atom) via `[outputs]` + a matching template —
  don't hand-write files into `static/`.

## Metadata

- Centralize `<head>` in a partial: title, `<meta name="description">` from `.Description`/summary,
  canonical URL from `.Permalink`, and Open Graph / Twitter cards from front matter with sensible
  fallbacks. Hugo ships internal templates for OpenGraph/Twitter cards — use them via
  `{{ template "_internal/opengraph.html" . }}`.
- Emit **structured data** (JSON-LD `Article`/`BreadcrumbList`) from a partial driven by page front
  matter — real values only, no fabricated fields.

## Guidance

- Set an absolute, correct `baseURL` per environment so canonical URLs, sitemaps, and feeds resolve.
- Generate a sitemap and reference it from `robots.txt`; keep both in the output pipeline, not
  hand-maintained.
- Don't duplicate meta logic across templates — one `head` partial is the single source of truth.
