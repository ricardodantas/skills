# HIG Foundations

## Typography

### System Fonts
- **SF Pro** — Primary system font for iOS, iPadOS, macOS, tvOS
- **SF Compact** — watchOS and small UI elements
- **SF Mono** — Code, monospaced content (Xcode)
- **New York** — Serif, traditional reading face (small sizes) / graphic display (large sizes)
- **SF Arabic, SF Armenian, SF Georgian, SF Hebrew** — Multilingual support

### Dynamic Type Text Styles (Default Sizes at "Large" setting)

| Style | Weight | Size | Leading | Use |
|-------|--------|------|---------|-----|
| Large Title | Regular | 34pt | 41pt | Screen titles, top-level headings |
| Title 1 | Regular | 28pt | 34pt | Section headers |
| Title 2 | Regular | 22pt | 28pt | Sub-section headers |
| Title 3 | Regular | 20pt | 25pt | Tertiary headers |
| Headline | Semi-Bold | 17pt | 22pt | Key labels, emphasized body |
| Body | Regular | 17pt | 22pt | Primary content text |
| Callout | Regular | 16pt | 21pt | Secondary content |
| Subheadline | Regular | 15pt | 20pt | Below headlines |
| Footnote | Regular | 13pt | 18pt | Supplementary info |
| Caption 1 | Regular | 12pt | 16pt | Labels, annotations |
| Caption 2 | Regular | 11pt | 13pt | Smallest readable text (minimum) |

### Typography Best Practices
- Always use Dynamic Type (`UIFont.TextStyle` / SwiftUI `.font(.body)` etc.)
- Minimum readable text: **11pt** (Caption 2 built-in minimum)
- Use `adjustsFontForContentSizeCategory = true` in UIKit
- In SwiftUI, system text styles auto-scale
- Custom fonts: wrap with `UIFontMetrics(forTextStyle:).scaledFont(for:)`
- Test at all Dynamic Type sizes including accessibility sizes (up to ~53pt for Body)
- Prefer **bold weight for emphasis** over color alone
- Line spacing: use system defaults; don't compress leading

## Color

### System Colors
Apple provides semantic colors that adapt to light/dark mode:

| Color | Light | Dark | Use |
|-------|-------|------|-----|
| `.label` | Black | White | Primary text |
| `.secondaryLabel` | 60% gray | 60% gray | Secondary text |
| `.tertiaryLabel` | 30% gray | 30% gray | Disabled/placeholder |
| `.systemBackground` | White | Black | Primary background |
| `.secondarySystemBackground` | F2F2F7 | 1C1C1E | Grouped content bg |
| `.tertiarySystemBackground` | White | 2C2C2E | Elevated content bg |
| `.separator` | C6C6C8 | 38383A | Thin lines |
| `.systemGroupedBackground` | F2F2F7 | Black | Grouped table bg |

### Tint/Accent Colors
- iOS system tint colors: `.systemBlue`, `.systemGreen`, `.systemRed`, `.systemOrange`, `.systemYellow`, `.systemPink`, `.systemPurple`, `.systemTeal`, `.systemIndigo`, `.systemMint`, `.systemCyan`, `.systemBrown`
- Use **one primary tint color** consistently for interactive elements
- Use `.tint()` modifier in SwiftUI or `UIView.tintColor` in UIKit

### Color Best Practices
- Use semantic/system colors — they auto-adapt to dark mode, high contrast, and accessibility
- Minimum contrast ratio: **4.5:1** for body text, **3:1** for large text (WCAG AA)
- Don't rely on color alone to convey meaning — combine with icons, text, or shapes
- Test with color blindness simulators
- Provide both light and dark variants for any custom colors via Asset Catalog
- Use P3 wide color gamut for richer colors on supported displays

## Layout

### Key Measurements
- **Safe area insets**: Always respect. Content must not extend under notch, home indicator, or status bar
- **Standard margins**: 16pt (compact width), 20pt (regular width on iPad)
- **Standard spacing**: 8pt base unit; use multiples (8, 16, 24, 32, 40)
- **Navigation bar height**: 44pt (standard), 96pt (with large title)
- **Tab bar height**: ~49pt (standard), ~83pt (with safe area on notched devices)
- **Status bar height**: ~54pt (notched/Dynamic Island), ~20pt (legacy)

### Layout System
- Use Auto Layout (UIKit) or SwiftUI layout system
- `LazyVStack` / `LazyHStack` for long scrollable lists
- `GeometryReader` sparingly — prefer built-in layout
- Use `.padding()` with system defaults for consistent spacing

### Adaptive Layout
- **Size classes**: Compact Width (iPhone portrait) vs Regular Width (iPad, iPhone landscape)
- Use `@Environment(\.horizontalSizeClass)` to adapt
- **iPhone**: Single column, tab bar navigation
- **iPad**: Split view, sidebar navigation, multi-column
- Grid layouts: `LazyVGrid` / `LazyHGrid` with adaptive columns

### Safe Area
```swift
// Respect safe area (default behavior)
Text("Content")

// Extend behind safe area (backgrounds only)
Color.blue.ignoresSafeArea()
```

## Icons

### App Icons
- See `icon-design.md` for full details
- iOS 26+: Multi-layer Liquid Glass icons via Icon Composer
- Single 1024×1024 design; system generates all sizes
- Support Default, Dark, and Mono (tinted) modes
- No transparency in final icon (system applies shape mask)

### SF Symbols
- See `sf-symbols.md` for full details
- 6,900+ symbols, 9 weights, 3 scales
- Use `Image(systemName:)` in SwiftUI
- Preferred over custom icons for system concepts

## Accessibility

### Required Support
1. **VoiceOver** — All interactive elements must have accessibility labels
2. **Dynamic Type** — All text must scale with user's preferred size
3. **Reduce Motion** — Provide alternatives to animations
4. **Reduce Transparency** — Liquid Glass auto-adapts; verify legibility
5. **Increase Contrast** — Test with high contrast mode
6. **Switch Control** — All actions reachable via sequential navigation
7. **Bold Text** — System handles; verify layout doesn't break

### Implementation Checklist
- Set `.accessibilityLabel()` on all images and icons
- Set `.accessibilityHint()` for non-obvious actions
- Use `.accessibilityElement(children:)` to group related elements
- Mark decorative images with `.accessibilityHidden(true)`
- Support `.accessibilityAction()` for custom gestures
- Test with VoiceOver ON (swipe through every screen)
- Ensure focus order is logical (top-to-bottom, left-to-right)
- Announce dynamic content changes with `UIAccessibility.post(notification:)`
- Minimum touch target: **44×44 pt**
- Never disable user interaction for accessibility-critical controls
- Support Smart Invert (avoid bitmap-inverted images with `.accessibilityIgnoresInvertColors`)

### Color Accessibility
- Don't use color as the sole indicator (add icons/text)
- Contrast ratio ≥ 4.5:1 for normal text, ≥ 3:1 for large text
- Test with Accessibility Inspector and color blindness filters
