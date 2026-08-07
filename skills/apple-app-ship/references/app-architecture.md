# App Architecture & Code

## Tooling

- **Always use the latest Swift and Xcode versions** (currently Swift 6, Xcode 26)
- Target the latest OS versions (iOS 26+, macOS Tahoe 26+, watchOS 26+, tvOS 26+)
- Use XcodeGen (`project.yml`) for project generation when creating new apps

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

## SwiftData Models

```swift
import SwiftData

@Model
final class Item {
    // All properties optional for CloudKit sync
    var title: String?
    var createdAt: Date?
    var category: String?  // Use String for enums (CloudKit compatibility)

    init(title: String, createdAt: Date = .now, category: String = "default") {
        self.title = title
        self.createdAt = createdAt
        self.category = category
    }
}
```

Key rules:
- All properties optional (CloudKit requirement)
- Use `String` for enum-like fields (CloudKit can't sync Swift enums)
- Add `init()` with sensible defaults
- Bundle ID: `com.yourcompany.<appname>`
- CloudKit container: `iCloud.com.yourcompany.<appname>`

## Service Layer Pattern

```swift
import SwiftUI
import SwiftData

@Observable
final class AppService {
    private let modelContext: ModelContext

    init(modelContext: ModelContext) {
        self.modelContext = modelContext
    }

    func createItem(title: String) {
        let item = Item(title: title)
        modelContext.insert(item)
        try? modelContext.save()
    }
}
```

Inject via environment: `.environment(AppService(modelContext: context))`. Read it back in views with `@Environment(AppService.self) private var service`. Create the service once (not inline in a re-evaluated `body`) so its `@Observable` state survives view updates.

## App Entry Point

```swift
@main
struct AppNameApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Item.self])
    }
}
```

For CloudKit sync add: `.modelContainer(for: [Item.self], cloudKitDatabase: .automatic)`

## Platform-Specific Code

```swift
#if os(iOS)
    // iPhone/iPad specific
#elseif os(macOS)
    // Mac specific (NOT matched by "Designed for iPad" apps)
#elseif os(watchOS)
    // Watch specific
#elseif os(tvOS)
    // TV specific — use buttons not sliders (Siri Remote)
#endif
```

Use `@Environment(\.horizontalSizeClass)` for iPad vs iPhone layout switching:
- `.compact` = iPhone portrait
- `.regular` = iPad, Mac, iPhone landscape

## Logging

```swift
import OSLog
private let logger = Logger(subsystem: "com.yourcompany.appname", category: "ServiceName")
logger.info("Something happened")
logger.error("Something failed: \(error.localizedDescription)")
```

## AppIntents & Siri Shortcuts

```swift
struct DoSomethingIntent: AppIntent {
    static let title: LocalizedStringResource = "Do Something"
    static let description = IntentDescription("Does something useful")

    @Parameter(title: "Input") var input: String

    func perform() async throws -> some IntentResult {
        // action
        return .result()
    }
}

struct AppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(intent: DoSomethingIntent(),
                    phrases: ["Do something in \(.applicationName)"],
                    shortTitle: "Do Something",
                    systemImageName: "star")
    }
}
```

**Critical**: `isDiscoverable = false` does NOT work on intents in `AppShortcutsProvider` — build error. To avoid duplicate Shortcuts entries, rename the intent's `title` to differ from `AppShortcut.shortTitle`.

## Audio (AVFoundation)

- File playback: use `AVAudioPlayer` (simple, reliable for one-shot sounds)
- Real-time mixing/synthesis: use `AVAudioEngine` with `AVAudioPlayerNode`
- **Lesson**: `AVAudioPlayer` >> `AVAudioEngine` for one-shot file playback (engine approach causes choppy audio)
- watchOS: haptics only (no audio playback on most watch apps)

## Testing

Use Swift Testing framework:

```swift
import Testing
@testable import AppName

@Test func calculatesCorrectly() {
    let result = calculate(5, 10)
    #expect(result == 15)
}
```
