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

This skill owns the *ship workflow*, not general SwiftUI/testing/design craft — those are
delegated to dedicated skills that stay current:

| When you're… | Use skill |
|--------------|-----------|
| Building SwiftUI views/components — layout, navigation, TabView, composition | `swiftui-ui-patterns` |
| SwiftUI engineering — state/`@Observable` data flow, performance/invalidation, Instruments traces, latest/deprecated APIs | `swiftui-expert-skill` |
| Writing or reviewing tests | `swift-testing-pro` |
| Implementing or reviewing the visual design (iOS 26+ Liquid Glass) | `swiftui-liquid-glass` |

Before that work, confirm the skill is available (it appears in your available skills). If one
is missing, tell the user and offer to install it — `npx skills find <skill-name>` — rather than
falling back to inline guidance here.

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

### Key Conventions (All Phases)

- **Always use the latest versions of Swift and Xcode** (currently Swift 6, Xcode 26+)
- **Bundle identifier pattern**: `com.yourcompany.<appname>` (e.g. `com.yourcompany.nutricounter`) — use your own reverse-DNS domain
- **CloudKit container pattern**: `iCloud.com.yourcompany.<appname>`
- Zero third-party dependencies (100% Apple frameworks)
- All SwiftData model properties optional (CloudKit requirement)
- `#if DEBUG` for any debug-only code (stripped from Release builds)
- Platform conditionals: `#if os(iOS)`, `#if os(macOS)`, `#if os(watchOS)`, `#if os(tvOS)`
- macOS "Designed for iPad" apps: `#if os(macOS)` does NOT match — use `#if os(iOS)`
- watchOS/tvOS targets get their own copies of models (not shared framework)
- Package manager: **pnpm** (not npm) for web projects

For SwiftUI UI patterns (views, layout, navigation, TabView, composition) defer to
`swiftui-ui-patterns`; for SwiftUI engineering (state, `@Observable`, performance, latest APIs)
defer to `swiftui-expert-skill`; for tests defer to `swift-testing-pro`; for Liquid Glass design
defer to `swiftui-liquid-glass`.

### Reusable Assets

- `scripts/generate-appstore-images.js` — Parameterized Node + sharp script for generating App Store marketing images (iPhone, iPad, Mac) with device frames, Dynamic Island, headlines, and shadows. See references/app-store-images.md for configuration.
