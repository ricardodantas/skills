# Configuration & Hugo Modules

Fetch current config keys and module commands via `find-docs`
(`docs /gohugoio/hugo "configuration directory and hugo modules"`).

## Configuration

- Single file (`hugo.toml`/`.yaml`/`.json`) is fine for small sites. For anything with
  environment differences, use the **config directory**: `config/_default/`, `config/production/`,
  `config/development/` — Hugo merges `_default` with the active environment.
- `hugo` builds in `production` by default; `hugo server` in `development`. Put analytics, minify,
  and real `baseURL` in `production`; keep drafts/fast settings in `development`.
- Keep tunables in `[params]` (theme/site options) rather than scattering literals in templates.

## Hugo Modules

- Modules are Go modules: `hugo mod init <path>` creates `go.mod`. Import themes/components with
  `[[module.imports]]`; update with `hugo mod get -u ./...` and tidy with `hugo mod tidy`.
- **Mounts** (`[[module.mounts]]`) map source dirs into Hugo's virtual filesystem — use them to
  place assets/content from modules or non-standard folders without moving files.
- Commit `go.mod` and `go.sum` for reproducible builds; vendor with `hugo mod vendor` when the CI
  can't reach module sources.

## Guidance

- Prefer config + modules over copy-paste: a value that differs by environment belongs in
  `config/<env>/`, not a template `if`.
- Declare `[module.hugoVersion]` `min` so contributors on older Hugo get a clear error.
