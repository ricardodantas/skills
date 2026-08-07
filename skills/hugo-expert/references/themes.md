# Theme creation & customization

Fetch current theme-config keys and module syntax via `find-docs`
(`docs /gohugoio/hugo "hugo modules theme configuration"`).

## Prefer Hugo Modules over classic themes

- A **module** theme is pulled via `hugo.toml` `[module] [[module.imports]]` and versioned with
  `go.mod` — reproducible and updatable (`hugo mod get -u`). Prefer this to a `themes/<name>/` git
  submodule for new work.
- Initialize a themed project as a module: `hugo mod init <module-path>`, then import the theme.

## Customizing without forking

- **Shadowing**: to change a theme file, place a file at the same path in the **project root**
  (`layouts/…`, `assets/…`, `i18n/…`, `static/…`). Hugo's union filesystem lets the project win —
  never edit files inside `themes/`.
- Expose knobs through `[params]` in `hugo.toml` so behavior is configurable, not hardcoded.
- Override only what you need; keep the rest inheriting so theme updates still land.

## Building a distributable theme

- Standard dirs: `layouts/`, `assets/`, `static/`, `i18n/`, `archetypes/`, plus `theme.toml`
  (name, license, min Hugo version, author) and an `exampleSite/` demonstrating usage.
- Declare a minimum Hugo version in `theme.toml` / `[module.hugoVersion]` so users on older Hugo get
  a clear message.
- Ship sensible `[params]` defaults and document them in the exampleSite config.
