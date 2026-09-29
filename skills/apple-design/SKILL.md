---
name: apple-design
description: >
  Comprehensive Apple Human Interface Guidelines (HIG) and design system reference, current
  through the 27 releases (iOS 27, iPadOS 27, macOS 27, watchOS 27, tvOS 27, visionOS 27).
  Covers Liquid Glass (introduced in iOS 26, refined in 27), SF Symbols 8, Icon Composer 2,
  typography, color, layout, accessibility, navigation patterns, UI components, toolbars,
  Siri snippets, iPhone Duo, widgets, Live Activities, inputs (gestures, keyboards, Pencil,
  Digital Crown, game controls), Apple technologies (Sign in with Apple, Apple Pay, In-App
  Purchase, CarPlay, SharePlay), and platform-specific guidance for iOS, iPadOS, macOS,
  watchOS, tvOS, and visionOS. Sections cite their live HIG pages. Use when designing or reviewing Apple app UI, adopting Liquid Glass,
  migrating to the 27 SDK, or building apps that feel native and follow current Apple design
  standards.
---

# Apple Design Skill

## Apple Design Philosophy

Apple design centers on three pillars:
1. **Clarity** — Text is legible, icons precise, adornments subtle. Functionality motivates design.
2. **Deference** — UI helps people understand and interact with content, never competes with it.
3. **Depth** — Visual layers and realistic motion convey hierarchy and facilitate understanding.

Starting with iOS 26 / macOS Tahoe (2025), **Liquid Glass** is the unified design language across all Apple platforms — a translucent, dynamic material that refracts/reflects content behind it. The 27 releases (2026) refine it — more uniform refraction, better contrast, and a user slider from clear to tinted — and make it mandatory: apps built with the 27 SDK can no longer opt out.

## When to Reference Which File

| Need | File |
|------|------|
| Design principles, color, dark mode, typography, layout, icons, accessibility, motion, writing, right-to-left, inclusion, privacy | [references/hig-foundations.md](references/hig-foundations.md) |
| Navigation, modality, search, settings, onboarding, Siri snippets, feedback, data entry, drag and drop, undo, notifications, haptics, charting | [references/hig-patterns.md](references/hig-patterns.md) |
| Buttons, lists, forms, sheets, alerts, pickers, segmented controls, menus, toolbars | [references/hig-components.md](references/hig-components.md) |
| Popovers, windows, split/scroll views, page & disclosure controls, text/web views, charts, gauges | [references/hig-components-extended.md](references/hig-components-extended.md) |
| Widgets, Live Activities, Controls, notifications, App Shortcuts, complications, watch faces, Top Shelf | [references/hig-system-experiences.md](references/hig-system-experiences.md) |
| Gestures, keyboards, pointer, Apple Pencil, Digital Crown, Action button, Camera Control, eyes, focus, game controls, remotes | [references/hig-inputs.md](references/hig-inputs.md) |
| Sign in with Apple, Apple Pay, In-App Purchase, Wallet, CarPlay, Siri, SharePlay, Generative AI, HealthKit, Maps, and other Apple technologies | [references/hig-technologies.md](references/hig-technologies.md) |
| Liquid Glass material, `.glassEffect()`, what changed in 27, migration | [references/liquid-glass.md](references/liquid-glass.md) |
| SF Symbols usage, rendering modes, animations | [references/sf-symbols.md](references/sf-symbols.md) |
| App icon design, Icon Composer, multi-layer icons | [references/icon-design.md](references/icon-design.md) |
| iOS vs iPadOS vs macOS vs watchOS vs visionOS vs tvOS, iPhone Duo | [references/platform-specific.md](references/platform-specific.md) |

## Core Principles Checklist

- [ ] Use system fonts (SF Pro) with Dynamic Type text styles
- [ ] Touch targets: 44×44 pt default on iOS/iPadOS (28×28 pt absolute minimum)
- [ ] Minimum text size: 11 pt
- [ ] Support Dark Mode with semantic/system colors
- [ ] Provide @2x and @3x image assets
- [ ] Support Dynamic Type (all accessibility sizes)
- [ ] Use SF Symbols instead of custom icons where possible
- [ ] Adopt Liquid Glass for navigation/control layers (iOS 26+; mandatory with the 27 SDK)
- [ ] Keep content as the hero — controls defer to content
- [ ] Use standard navigation patterns (NavigationStack, TabView)
- [ ] Test with accessibility settings (VoiceOver, Reduce Motion, Increase Contrast, Reduce Transparency) and across the 27 Liquid Glass slider (clear → tinted)
- [ ] Multi-layer app icons via Icon Composer
- [ ] Respect safe areas and layout margins

## Common Mistakes to Avoid

1. **Applying Liquid Glass to content** — Glass is ONLY for the navigation/control layer, never for content (lists, tables, media)
2. **Custom backgrounds on sheets** — sheets auto-apply glass (iOS 26+); remove `.presentationBackground()` overrides
3. **Multiple glass elements without `GlassEffectContainer`** — Causes inefficient rendering and inconsistent sampling
4. **Flat app icons** — layered Liquid Glass icons are the norm since iOS 26 (Icon Composer 2 adds the sharper 27 rendering); flat icons look outdated
5. **Ignoring Dynamic Type** — Hard-coding font sizes breaks accessibility
6. **Using non-system colors without dark mode variants** — Always define both light and dark appearances
7. **Tap targets below the 44×44 pt default** — Causes frustration and accessibility failures
8. **Overusing color/tint** — Use tint sparingly for semantic meaning, not decoration
9. **Custom navigation patterns** — Use system NavigationStack/TabView; users expect standard gestures
10. **Not testing Reduce Transparency** — Liquid Glass must remain legible with reduced transparency enabled
11. **Ignoring platform differences** — macOS needs menu bar support, keyboard shortcuts; watchOS needs glanceable UI
12. **Using raster images where SF Symbols exist** — Symbols scale, adapt to weight/size, and support accessibility automatically
13. **Relying on `UIDesignRequiresCompatibility` to skip Liquid Glass** — the system ignores it when you build with the 27 SDK; design for glass instead of opting out
14. **Hard-coding a glass look** — people choose anywhere from ultra-clear to fully tinted in the 27 slider; check legibility at both ends rather than tuning for one
