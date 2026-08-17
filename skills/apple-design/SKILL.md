---
name: apple-design
description: >
  Comprehensive Apple Human Interface Guidelines (HIG) and design system reference.
  Covers Liquid Glass (iOS 26+), SF Symbols, Icon Composer, typography, color, layout,
  accessibility, navigation patterns, UI components, and platform-specific guidance for
  iOS, macOS, watchOS, tvOS, and visionOS. Enables building properly designed Apple apps
  that feel native and follow current Apple design standards.
---

# Apple Design Skill

## Apple Design Philosophy

Apple design centers on three pillars:
1. **Clarity** — Text is legible, icons precise, adornments subtle. Functionality motivates design.
2. **Deference** — UI helps people understand and interact with content, never competes with it.
3. **Depth** — Visual layers and realistic motion convey hierarchy and facilitate understanding.

Starting with iOS 26 / macOS Tahoe (2025), **Liquid Glass** is the unified design language across all Apple platforms — a translucent, dynamic material that refracts/reflects content behind it.

## When to Reference Which File

| Need | File |
|------|------|
| Color, typography, layout, icons, accessibility | `references/hig-foundations.md` |
| Navigation, modality, search, settings, onboarding | `references/hig-patterns.md` |
| Buttons, lists, forms, sheets, alerts, pickers | `references/hig-components.md` |
| Liquid Glass material, `.glassEffect()`, migration | `references/liquid-glass.md` |
| SF Symbols usage, rendering modes, animations | `references/sf-symbols.md` |
| App icon design, Icon Composer, multi-layer icons | `references/icon-design.md` |
| iOS vs macOS vs watchOS vs visionOS vs tvOS | `references/platform-specific.md` |

## Core Principles Checklist

- [ ] Use system fonts (SF Pro) with Dynamic Type text styles
- [ ] Minimum touch target: 44×44 pt
- [ ] Minimum text size: 11 pt
- [ ] Support Dark Mode with semantic/system colors
- [ ] Provide @2x and @3x image assets
- [ ] Support Dynamic Type (all accessibility sizes)
- [ ] Use SF Symbols instead of custom icons where possible
- [ ] Adopt Liquid Glass for navigation/control layers (iOS 26+)
- [ ] Keep content as the hero — controls defer to content
- [ ] Use standard navigation patterns (NavigationStack, TabView)
- [ ] Test with accessibility settings (VoiceOver, Reduce Motion, Increase Contrast, Reduce Transparency)
- [ ] Multi-layer app icons via Icon Composer
- [ ] Respect safe areas and layout margins

## Common Mistakes to Avoid

1. **Applying Liquid Glass to content** — Glass is ONLY for the navigation/control layer, never for content (lists, tables, media)
2. **Custom backgrounds on sheets** — iOS 26 sheets auto-apply glass; remove `.presentationBackground()` overrides
3. **Multiple glass elements without `GlassEffectContainer`** — Causes inefficient rendering and inconsistent sampling
4. **Flat app icons** — iOS 26 requires multi-layer icons; flat icons look outdated
5. **Ignoring Dynamic Type** — Hard-coding font sizes breaks accessibility
6. **Using non-system colors without dark mode variants** — Always define both light and dark appearances
7. **Tap targets below 44pt** — Causes frustration and accessibility failures
8. **Overusing color/tint** — Use tint sparingly for semantic meaning, not decoration
9. **Custom navigation patterns** — Use system NavigationStack/TabView; users expect standard gestures
10. **Not testing Reduce Transparency** — Liquid Glass must remain legible with reduced transparency enabled
11. **Ignoring platform differences** — macOS needs menu bar support, keyboard shortcuts; watchOS needs glanceable UI
12. **Using raster images where SF Symbols exist** — Symbols scale, adapt to weight/size, and support accessibility automatically
