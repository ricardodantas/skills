# Typefully CLI Command Reference

## typefully auth

Verify API key and display account info.

```bash
typefully auth
typefully auth --json
```

## typefully config init

Interactive setup for API key and default social set.

```bash
typefully config init
```

## typefully sets

List all social sets with connected platforms.

```bash
typefully sets
typefully sets --json
```

## typefully draft create

Create a new draft.

| Flag | Description | Default |
|------|-------------|---------|
| `--set <id>` | Social set ID | Config default |
| `--content <text>` | Content (reads stdin if omitted) | - |
| `--platform <p>` | Target platforms (comma-separated) | `x` |
| `--publish-at <when>` | `now`, `next-free-slot`, or ISO-8601 | Draft (no publish) |
| `--tag <name>` | Tags (repeatable) | - |
| `--media <id>` | Media IDs (repeatable) | - |

Thread support: content containing `---` on its own line is split into multiple posts.

## typefully draft list

List drafts with filtering and pagination.

| Flag | Description | Default |
|------|-------------|---------|
| `--set <id>` | Social set ID | Config default |
| `--status <s>` | `draft`, `scheduled`, or `published` | All |
| `--tag <name>` | Filter by tag | - |
| `--sort <field>` | `created_at`, `updated_at`, `scheduled_date`, `published_at` | `created_at` |
| `--limit <n>` | Max results | `20` |
| `--offset <n>` | Pagination offset | `0` |

## typefully draft get \<draft_id\>

Get a single draft by ID.

```bash
typefully draft get abc123
typefully draft get abc123 --json
```

## typefully draft edit \<draft_id\>

Edit an existing draft.

| Flag | Description |
|------|-------------|
| `--set <id>` | Social set ID |
| `--content <text>` | New content |
| `--publish-at <when>` | Reschedule |
| `--tag <name>` | Replace tags (repeatable) |
| `--share <bool>` | Toggle sharing |

## typefully draft delete \<draft_id\>

Delete a draft. Requires `--force` or interactive confirmation.

```bash
typefully draft delete abc123
typefully draft delete abc123 --force
```

## typefully draft publish \<draft_id\>

Publish a draft immediately (shortcut for edit with `publish_at: now`).

```bash
typefully draft publish abc123
```

## typefully draft schedule \<draft_id\> \<time\>

Schedule a draft. Accepts `next-free-slot` or ISO-8601 datetime.

```bash
typefully draft schedule abc123 next-free-slot
typefully draft schedule abc123 "2025-06-20T14:00:00Z"
```

## typefully media upload \<file\>

Upload media (image, video, GIF, PDF). Returns `media_id` for use with `draft create --media`.

Supported formats: PNG, JPEG, GIF, WebP, MP4.

```bash
typefully media upload photo.jpg
typefully media upload banner.png --json
```

The CLI handles the 3-step upload process automatically:
1. Request presigned URL from Typefully
2. Upload file to S3
3. Poll until processing completes

## typefully tags list

List all tags for a social set.

```bash
typefully tags list
typefully tags list --json
```

## typefully tags create \<name\>

Create a new tag.

```bash
typefully tags create "product-launch"
typefully tags create "weekly-update" --set set_abc123
```

## typefully update

Self-update to the latest version. Detects Homebrew or cargo and updates accordingly.

```bash
typefully update
```
