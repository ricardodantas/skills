---
name: apple-app-ship
description: >
  End-to-end workflow for building, polishing, and shipping native Apple platform apps
  (iOS, iPadOS, macOS, watchOS, tvOS) with SwiftUI — from architecture to App Store submission.
  Includes marketing website generation (Astro + Tailwind), App Store screenshot/image generation
  (Node + sharp), debug data seeders, and App Store Connect metadata.
  Use when: (1) creating a new Apple app from scratch, (2) polishing an existing app for release,
  (3) building a marketing website for an Apple app, (4) generating App Store marketing screenshots,
  (5) preparing App Store Connect submission (metadata, privacy labels, review notes),
  (6) adding debug data seeders for screenshot-ready previews, (7) any "ship this app" workflow
  covering multiple phases from code to published listing.
---

# Apple App Ship

End-to-end skill for building and shipping Apple platform apps. Covers five phases:

1. **App Architecture & Code** → references/app-architecture.md
2. **App Polish & Ship-Readiness** → references/app-polish.md
3. **Marketing Website** → references/marketing-website.md
4. **App Store Images** → references/app-store-images.md
5. **App Store Connect Submission** → references/app-store-connect.md

## Companion skills

This skill owns the *ship workflow*; the craft in each phase is delegated to dedicated skills
that stay current. The table below is the **registry** — **up front, before starting**, check
that the companions for the phases you'll run are available (they appear in your available
skills). For any that are missing, tell the user and offer to install it —
`npx skills find <skill-name>` — then proceed. Don't fall back to inline guidance for delegated work.

| Phase / area | Companion skills |
|--------------|------------------|
| Plan & build (1) — UI/HIG, SwiftUI, build, signing | `apple-design`, `swiftui-ui-patterns`, `swiftui-expert-skill`, `swiftui-liquid-glass`, `xcode-mcp`, `asc-signing-setup`, `asc-xcode-build` |
| Polish & readiness (2) — tests, guidelines, notarization | `swift-testing-pro`, `app-store-review`, `asc-notarization` |
| Marketing website (3) | `frontend-design` |
| App Store images (4) | `asc-shots-pipeline`, `asc-screenshot-resize` |
| App Store Connect submission (5) — record, metadata, ASO, release | `asc-app-create-ui`, `asc-metadata-sync`, `asc-whats-new-writer`, `asc-localize-metadata`, `asc-aso-audit`, `asc-release-flow`, `asc-submission-health`, `asc-build-lifecycle`, `asc-id-resolver`, `asc-workflow`, `asc-cli-usage` |
| TestFlight & beta | `asc-testflight-orchestration`, `asc-crash-triage` |
| Monetization | `asc-ppp-pricing`, `asc-subscription-localization`, `asc-revenuecat-catalog-sync`, `asc-apple-ads` |
| Final review | `apple-appstore-reviewer` |

All `asc-*` skills drive the `asc` CLI — `asc-cli-usage` covers its basics.

## Workflow

Determine which phase the user needs, then read only that reference file. Most projects flow sequentially but users may jump to any phase.

### Phase Selection

| User says | Phase |
|-----------|-------|
| "Build me an app" / "Create a new app" | 1 → app-architecture.md |
| "Polish for release" / "Add data seeder" / "Fix shortcuts" | 2 → app-polish.md |
| "Build the website" / "Marketing site" | 3 → marketing-website.md |
| "Generate App Store screenshots" / "Marketing images" | 4 → app-store-images.md |
| "Submit to App Store" / "App Store metadata" | 5 → app-store-connect.md |
| "Ship this app" (end-to-end) | Read phases sequentially as needed |

### Final review

When the work is finished — before submitting to App Store Connect — run a review of the
codebase with `apple-appstore-reviewer` to catch App Store optimizations and likely rejection
reasons. Confirm it's available; if missing, tell the user and offer to install it —
`npx skills find apple-appstore-reviewer`. For an end-to-end "ship this app" run, always finish
with this review.

### Key Conventions (All Phases)

- **Always use the latest versions of Swift and Xcode** (currently Swift 6, Xcode 26+)
- **Bundle identifier pattern**: `com.yourcompany.<appname>` (e.g. `com.yourcompany.myapp`) — use your own reverse-DNS domain
- **CloudKit container pattern**: `iCloud.com.yourcompany.<appname>`
- Zero third-party dependencies (100% Apple frameworks)
- All SwiftData model properties optional (CloudKit requirement)
- `#if DEBUG` for any debug-only code (stripped from Release builds)
- Platform conditionals: `#if os(iOS)`, `#if os(macOS)`, `#if os(watchOS)`, `#if os(tvOS)`
- macOS "Designed for iPad" apps: `#if os(macOS)` does NOT match — use `#if os(iOS)`
- watchOS/tvOS targets get their own copies of models (not shared framework)
- Package manager: **pnpm** (not npm) for web projects

When planning the app's UI (HIG, navigation, SF Symbols, typography, color, layout) defer to
`apple-design`; for SwiftUI UI patterns (views, layout, TabView, composition) defer to
`swiftui-ui-patterns`; for SwiftUI engineering (state, `@Observable`, performance, latest APIs)
defer to `swiftui-expert-skill`; for tests defer to `swift-testing-pro`; for Liquid Glass design
defer to `swiftui-liquid-glass`.

### Reusable Assets

- **App Store screenshots**: prefer the `asc-shots-pipeline` skill (capture → frame → upload). The Node + sharp script below is the fallback for bespoke branded marketing frames.
- `scripts/generate-appstore-images.js` — Parameterized Node + sharp script for generating App Store marketing images (iPhone, iPad, Mac) with device frames, Dynamic Island, headlines, and shadows. See references/app-store-images.md for configuration.
