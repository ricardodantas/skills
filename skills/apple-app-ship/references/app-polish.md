# App Polish & Ship-Readiness

## Debug Data Seeder

Create screenshot-ready sample data behind `#if DEBUG`:

```swift
#if DEBUG
import SwiftData

struct DebugDataSeeder {
    static func populate(context: ModelContext) {
        // Clear existing
        try? context.delete(model: Item.self)

        let calendar = Calendar.current
        let today = Date()

        // Create realistic data spanning 30-60 days
        for dayOffset in 0..<45 {
            guard let date = calendar.date(byAdding: .day, value: -dayOffset, to: today) else { continue }
            let item = Item(title: "Sample \(dayOffset)", createdAt: date)
            context.insert(item)
        }
        try? context.save()
    }

    static func deleteAll(context: ModelContext) {
        try? context.delete(model: Item.self)
        try? context.save()
    }
}
#endif
```

Add to Settings behind `#if DEBUG`:

```swift
#if DEBUG
Section("Debug") {
    Button("Populate Sample Data") {
        DebugDataSeeder.populate(context: modelContext)
    }
    Button("Delete All Data", role: .destructive) {
        DebugDataSeeder.deleteAll(context: modelContext)
    }
}
#endif
```

### Data Seeder Tips

- Span 30-60 days for realistic charts/heatmaps
- Vary data density (some busy days, some quiet)
- Include edge cases (streaks, milestones, empty days)
- Use realistic names/titles (not "Test 1, Test 2")
- For multi-target apps (TV), copy seeder to each target's Services/ folder

## iPad/macOS Layout Polish

Use `horizontalSizeClass` for adaptive layouts:

```swift
@Environment(\.horizontalSizeClass) private var horizontalSizeClass

var body: some View {
    if horizontalSizeClass == .regular {
        // Wide: 2-column grid, side-by-side cards
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())]) { ... }
    } else {
        // Compact: single column stack
        VStack { ... }
    }
}
```

macOS-specific patterns:
- Use `.frame(maxWidth: 520)` for wizard-style centered layouts
- `.labelsHidden()` to suppress Picker labels that look redundant on Mac
- 2-column `LazyVGrid` for completed/list views (maxWidth ~960)
- tvOS: buttons instead of sliders (Siri Remote compatibility)

## Pre-Ship Checklist

### Required
- [ ] App icon (all sizes) via Icon Composer or asset catalog
- [ ] Privacy manifest (`PrivacyInfo.xcprivacy`)
- [ ] App Store privacy label (Data Not Collected / appropriate category)
- [ ] Debug code behind `#if DEBUG`
- [ ] Error handling (no force unwraps in production paths)
- [ ] Accessibility labels on custom controls
- [ ] Dark mode support (or dark-only with explicit choice)

### Recommended
- [ ] Localization (at minimum, English strings file)
- [ ] Onboarding / TipKit hints
- [ ] Widgets (Lock Screen, StandBy, Home Screen)
- [ ] Control Center widget (iOS 18+)
- [ ] CoreSpotlight indexing
- [ ] StoreKit review prompts
- [ ] Live Activities (if timer/progress based)
- [ ] Siri Shortcuts (3-7 intents)

### Testing
- [ ] Unit tests for business logic (Services, Calculators)
- [ ] UI tests for critical flows
- [ ] Test on real devices (especially watch, TV)
- [ ] Test CloudKit sync between devices
- [ ] Test fresh install (no data) vs populated states
