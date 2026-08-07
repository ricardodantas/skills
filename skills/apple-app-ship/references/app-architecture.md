# App Architecture & Code

## Tooling

- **Always use the latest Swift and Xcode versions** (currently Swift 6, Xcode 26)
- Target the latest OS versions (iOS 26+, macOS Tahoe 26+, watchOS 26+, tvOS 26+)
- Use XcodeGen (`project.yml`) for project generation when creating new apps
- Build/run via `xcode-mcp`; signing and archive/upload via `asc-signing-setup` / `asc-xcode-build`

## Bundle Identifier

Always use this pattern:
- **Bundle ID**: `com.yourcompany.<appname>` (e.g. `com.yourcompany.nutricounter`) — replace `com.yourcompany` with your own reverse-DNS domain
- **CloudKit container**: `iCloud.com.yourcompany.<appname>`

## Project Structure

Standard SwiftUI multi-platform app structure:

```
AppName/
├── AppNameApp.swift          # @main entry, WindowGroup, modelContainer
├── Models/                   # SwiftData models
├── Services/                 # Business logic (@Observable services)
├── Views/
│   ├── Components/           # Reusable UI components
│   ├── Screens/              # Full-screen views
│   └── Settings/             # SettingsView
├── Intents/                  # AppIntents + AppShortcutsProvider
├── Theme/                    # Colors, typography, spacing constants
└── Extensions/               # Swift extensions
```

For multi-target (watchOS/tvOS): duplicate Models/ and Services/ into each target folder rather than sharing via framework.

> Planning the app's UI (HIG, navigation, SF Symbols, typography, color, layout) →
> `apple-design`; SwiftUI UI (views, layout, TabView, composition) → `swiftui-ui-patterns`;
> SwiftUI engineering (state, `@Observable`, `@Environment`, performance, latest APIs) →
> `swiftui-expert-skill`; tests → `swift-testing-pro`; Liquid Glass design →
> `swiftui-liquid-glass`; build/run → `xcode-mcp`; signing (bundle IDs, certs, profiles) →
> `asc-signing-setup`; archive/export/upload → `asc-xcode-build`. The rules below are the
> ship-specific constraints those skills don't cover.

## SwiftData Models

- All `@Model` properties **optional** — CloudKit sync requirement
- Use `String` for enum-like fields (CloudKit can't sync Swift enums)
- Give `init()` sensible defaults
- Attach the store at the app entry: `.modelContainer(for: [Item.self])`; for CloudKit sync add `cloudKitDatabase: .automatic`

## Services & SwiftUI wiring

Business logic goes in `@Observable` services injected with `.environment(...)`; create each
service once so its state survives view updates. Ship-specific platform notes:

- `#if os(macOS)` does **not** match "Designed for iPad" apps — use `#if os(iOS)`
- tvOS uses buttons, not sliders (Siri Remote)

## Logging

`import OSLog`; `Logger(subsystem: "com.yourcompany.appname", category: "...")` — subsystem = your bundle ID.

## AppIntents & Siri Shortcuts

Standard `AppIntent` + `AppShortcutsProvider`, with these ship gotchas:

- `isDiscoverable = false` does **not** work on intents in `AppShortcutsProvider` — build error.
- To avoid duplicate Shortcuts entries, make the intent's `title` differ from `AppShortcut.shortTitle`.
- Use `static let` (not `static var`) for `title`/`description` under Swift 6 strict concurrency.

## Audio (AVFoundation)

- File playback: `AVAudioPlayer` (simple, reliable for one-shot sounds)
- Real-time mixing/synthesis: `AVAudioEngine` + `AVAudioPlayerNode`
- **Lesson**: `AVAudioPlayer` >> `AVAudioEngine` for one-shot file playback (engine approach causes choppy audio)
- watchOS: haptics only (no audio playback on most watch apps)
