# Deployment & CI

Fetch host-specific and current flag details via `find-docs`
(`docs /gohugoio/hugo "hosting and deployment"`).

## Version pinning (most common breakage)

- **Pin `HUGO_VERSION`** in the deploy/CI config so production matches local. Netlify:
  `[build.environment] HUGO_VERSION = "x.y.z"`. Vercel/other CI: an env var or the install step.
- Match **Hugo Extended** vs standard to what the site needs (Sass ⇒ Extended). A standard binary
  building a Sass site fails only in CI — pin the edition too.

## Build command

- Production build: `hugo --minify` (optionally `--gc`). Hugo defaults to the `production`
  environment, enabling minification/analytics from `config/production/`.
- Set the correct `baseURL` per environment; hosts often inject it (Netlify `$DEPLOY_PRIME_URL`
  for previews) — pass `--baseURL` in preview builds so links resolve.

## Hosts

- **Netlify/Vercel/Cloudflare Pages**: set build command (`hugo --minify`), publish dir (`public`),
  and `HUGO_VERSION`. Commit `netlify.toml`/host config so it's reproducible.
- **GitHub Pages**: a workflow that installs a pinned Hugo, runs `hugo --minify`, and uploads
  `public/` via the Pages action.

## Guidance

- Treat the deploy config as source-controlled truth; never rely on the host's default Hugo version.
- Fail CI on Hugo build errors and (ideally) on new deprecation warnings.
