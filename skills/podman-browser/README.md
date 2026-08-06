# podman-browser

Headless browser automation using Podman + Playwright for scraping JavaScript-rendered pages.

## What it does

This skill runs a headless Chromium browser inside a Podman container using Microsoft's official Playwright image. It's useful for:

- Scraping pages that require JavaScript to render content
- Fetching dynamically loaded data (SPAs, React apps, etc.)
- Automated browser tasks without installing browser dependencies locally

## Prerequisites

- **Podman 5.x+** installed and running
- **Node.js 18+** (for running the CLI)
- Internet connection (first run pulls ~1.5GB container image)

## Installation

This skill lives in [`ricardodantas/skills`](https://github.com/ricardodantas/skills). Install it with the [skills.sh](https://skills.sh) CLI:

```bash
npx skills add ricardodantas/skills --skill podman-browser
```

To call `browse.js` directly from your shell, symlink it onto your PATH (adjust the path to wherever the skill was installed):

```bash
chmod +x browse.js
ln -sf "$(pwd)/browse.js" ~/.local/bin/podman-browse
```

## Usage

### Basic usage

```bash
# Get rendered text content from a page
podman-browse "https://example.com"

# Or run directly
./browse.js "https://example.com"
```

### Options

| Option | Description |
|--------|-------------|
| `--html` | Return raw HTML instead of text |
| `--wait <ms>` | Wait time after load (default: 2000ms) |
| `--selector <css>` | Wait for specific CSS selector before capturing |
| `-h, --help` | Show help |

### Examples

```bash
# Get rendered text content from Hacker News
podman-browse "https://news.ycombinator.com"

# Get raw HTML
podman-browse --html "https://news.ycombinator.com"

# Wait for specific element
podman-browse --selector ".itemlist" "https://news.ycombinator.com"

# Extra wait time for slow pages
podman-browse --wait 5000 "https://news.ycombinator.com/newest"
```

## How it works

1. Launches Microsoft's official Playwright container via Podman
2. Uses Chromium in headless mode with a realistic user agent
3. Navigates to the URL and waits for network idle
4. Optionally waits for a specific CSS selector
5. Applies additional wait time for JavaScript to settle
6. Returns text content (or HTML with `--html` flag)

## Files

| File | Description |
|------|-------------|
| `browse.js` | Self-contained Node.js CLI (handles args + spawns podman) |
| `SKILL.md` | Skill instructions and metadata |

## Container Image

Uses `mcr.microsoft.com/playwright:v1.61.0-noble` with `playwright@1.61.0` npm package.

**Note**: The Playwright npm package version must match the container image version.

## Performance Notes

- First run pulls the container image (~1.5GB)
- Each run starts a fresh container (clean but takes ~10-15s)
- Uses `--ipc=host` for Chromium stability
- Uses `--init` to handle zombie processes

## License

GPL-3.0 License - see [LICENSE](LICENSE) file.

## Contributing

Contributions welcome! Please open an issue or PR.

## Author

Ricardo Dantas ([@ricardodantas](https://github.com/ricardodantas))
