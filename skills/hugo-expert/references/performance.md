# Performance & asset pipeline

Fetch current Hugo Pipes / image-processing function signatures via `find-docs`
(`docs /gohugoio/hugo "hugo pipes asset processing"` and `"image processing methods"`).

## Asset pipeline (Hugo Pipes)

- Put CSS/JS/images that need processing in `assets/` (not `static/`, which is copied verbatim).
- Pipeline pattern: get the resource → transform → `fingerprint` → use `.RelPermalink`. Fingerprint
  in production for cache-busting; add `integrity` for SRI.
- CSS: `css.Sass`/`css.TailwindCSS` (needs **Hugo Extended** for Sass), then `minify` +
  `fingerprint`. JS: `js.Build` (esbuild) for bundling/tree-shaking.
- Guard prod-only steps with `hugo.IsProduction` so `hugo server` stays fast.

## Images

- Process page-resource images with `.Resize`/`.Fit`/`.Fill`/`.Process`; serve modern formats
  (WebP/AVIF) and `srcset` for responsive images. Processed images are cached in `resources/`.
- Commit or cache `resources/_gen/` in CI to avoid reprocessing every build.

## Build speed

- `partialCached` for invariant partials; avoid O(n²) `range … where` over all pages inside page
  loops — build lookups once.
- Enable Hugo's caches (`[caches]`) and keep the `resources/` cache warm in CI.
- Measure with `hugo --templateMetrics` / `--templateMetricsHints` to find slow templates.

## Guidance

- `static/` = passthrough; `assets/` = processed. Don't fingerprint from `static/`.
- Ship minified, fingerprinted assets in production; readable ones in development.
