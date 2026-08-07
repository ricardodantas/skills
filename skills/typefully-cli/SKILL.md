---
name: typefully-cli
description: "Manage social media content via the Typefully CLI. Create, schedule, publish, and manage drafts across X, LinkedIn, Threads, Bluesky, and Mastodon from the terminal. Use when: (1) creating or publishing social media posts/threads, (2) scheduling content for specific times or next free slot, (3) listing or managing existing drafts, (4) uploading media for posts, (5) managing tags, (6) any Typefully API interaction from the command line. NOT for: direct web browser interactions with typefully.com."
---

# Typefully CLI

CLI client for the Typefully API v2. Binary: `typefully`.

## Installation

```bash
# Homebrew
brew install ricardodantas/tap/typefully

# From crates.io
cargo install typefully

# From source
git clone https://github.com/ricardodantas/typefully-cli.git
cd typefully-cli
cargo install --path .
```

## Setup

Config at `~/.config/typefully/config.toml`:

```toml
api_key = "your-key"
default_social_set_id = "your-set-id"
```

Run `typefully config init` for interactive setup.

API key precedence: `--api-key` flag > `TYPEFULLY_API_KEY` env > config file.

## Commands

See [references/commands.md](references/commands.md) for full command reference with all flags and options.

### Quick Reference

```bash
# Auth
typefully auth

# List connected accounts
typefully sets

# Create draft
typefully draft create --content "Hello world!"

# Create thread (split on ---)
typefully draft create --content "First post
---
Second post
---
Third post"

# Pipe from stdin
echo "Posted from CLI" | typefully draft create

# Publish immediately
typefully draft create --content "Live now!" --publish-at now

# Schedule next free slot
typefully draft create --content "Queued" --publish-at next-free-slot

# Schedule specific time (ISO-8601)
typefully draft create --content "Timed" --publish-at "2025-06-15T10:00:00Z"

# Multi-platform
typefully draft create --content "Everywhere" --platform x,linkedin,threads

# With tags
typefully draft create --content "Update" --tag launch --tag product

# List drafts
typefully draft list
typefully draft list --status scheduled --tag marketing --limit 10

# Get/edit/delete
typefully draft get <id>
typefully draft edit <id> --content "Updated"
typefully draft delete <id> --force

# Publish/schedule existing draft
typefully draft publish <id>
typefully draft schedule <id> next-free-slot

# Media upload (returns media_id)
typefully media upload photo.jpg
typefully draft create --content "With image" --media <media_id>

# Tags
typefully tags list
typefully tags create "new-tag"

# Self-update
typefully update
```

## Global Flags

All commands accept: `--json`, `--no-color`, `-q`/`--quiet`, `-v`/`--verbose`, `--api-key <key>`.

Use `--json` for machine-readable output (pipe to `jq`).

## Scripting Patterns

```bash
# List scheduled draft IDs
typefully draft list --status scheduled --json | jq -r '.[].id'

# Publish all drafts tagged "ready"
for id in $(typefully draft list --tag ready --json | jq -r '.[].id'); do
  typefully draft publish "$id"
done

# Upload media and create draft in one go
MEDIA_ID=$(typefully media upload photo.jpg --json | jq -r '.media_id')
typefully draft create --content "New photo!" --media "$MEDIA_ID"
```

## Platforms

Supported: `x`, `linkedin`, `threads`, `bluesky`, `mastodon`.
Default: `x`. Use `--platform` flag (comma-separated or repeated) to target others.

## Exit Codes

- `0`: Success
- `1`: API/runtime error
- `2`: Invalid usage
