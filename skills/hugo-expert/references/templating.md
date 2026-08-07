# Templating & layouts

Durable practice for Hugo's Go-template layer. Fetch current function signatures and the exact
lookup order via `find-docs` (`docs /gohugoio/hugo "template lookup order"` etc.) — they shift
between releases.

## Structure

- **Base templates + blocks**: define `layouts/_default/baseof.html` with `{{ block "main" . }}`
  placeholders; each template fills the blocks. One skeleton, no per-page `<html>` duplication.
- **Partials**: extract repeated markup (`header`, `footer`, cards) into `layouts/partials/` and
  include with `{{ partial "name.html" . }}`. Use `partialCached` for partials that don't vary per
  page (menus, head) to cut build time.
- **Lookup order**: Hugo picks a template by kind/section/type/layout. When a template isn't
  applying, verify the lookup order (fetch it — it's version-specific) rather than guessing.

## Content in templates

- **Render hooks** (`layouts/_default/_markup/render-{link,image,heading,codeblock}.html`) customize
  how Markdown becomes HTML — the right place for external-link handling, image processing, heading
  anchors, and syntax highlighting. Prefer these over post-processing HTML.
- **Shortcodes** (`layouts/shortcodes/`) give authors safe, reusable components inside Markdown.
- Scope data with context: `.` is the current context; capture the page with `$` or `$page` before
  entering `range`/`with` blocks so inner scopes can still reach it.

## Guidance

- Keep logic in templates thin; compute once (assign to variables) and reuse.
- Prefer built-in functions (`where`, `first`, `sort`, `partial`) over ad-hoc loops.
- When output looks wrong, check whether the value is a `template.HTML` (safe) vs a string that got
  escaped — use `safeHTML`/`htmlUnescape` deliberately, never blanket-applied.
