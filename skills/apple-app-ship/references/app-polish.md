# App Polish & Ship-Readiness

## Debug Data Seeder

Ship a `#if DEBUG` seeder that populates screenshot-ready sample data (and a matching
delete-all), wired into `SettingsView` behind `#if DEBUG`. It's what makes App Store
screenshots look real. For the SwiftUI/SwiftData code itself, use `swiftui-expert-skill`.

### Data Seeder Tips

- Span 30-60 days for realistic charts/heatmaps
- Vary data density (some busy days, some quiet)
- Include edge cases (streaks, milestones, empty days)
- Use realistic names/titles (not "Test 1, Test 2")
- For multi-target apps (TV), copy seeder to each target's Services/ folder

## iPad/macOS Layout Polish

Adaptive layout (`horizontalSizeClass`, grids, split views) → `swiftui-ui-patterns`. For the
iOS 26+ visual design language (Liquid Glass materials, effects) → `swiftui-liquid-glass`.
Ship-specific reminders:

- macOS: `.frame(maxWidth: 520)` for wizard-style centered layouts; `.labelsHidden()` on Pickers that read redundant on Mac; 2-column grid (maxWidth ~960) for list views
- tvOS: buttons instead of sliders (Siri Remote compatibility)

## Pre-Ship Checklist

Before submitting, run `app-store-review` to evaluate the code against Apple's App Store Review
Guidelines and catch likely rejections. For macOS builds distributed **outside** the App Store,
use `asc-notarization` (Developer ID signing + Apple notarization).

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

Use `swift-testing-pro` for the test code itself. Ship coverage bar:

- [ ] Unit tests for business logic (Services, Calculators)
- [ ] UI tests for critical flows
- [ ] Test on real devices (especially watch, TV)
- [ ] Test CloudKit sync between devices
- [ ] Test fresh install (no data) vs populated states
