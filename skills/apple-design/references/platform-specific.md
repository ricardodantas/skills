# Platform-Specific Design

## iOS (iPhone)

### Key Characteristics
- **Single-column layout** in portrait (compact width)
- **Tab bar** navigation at bottom (max 5 visible tabs)
- **Edge-to-edge** content with safe area insets
- **Touch-first** — 44pt minimum tap targets
- **Gestures**: Swipe back, pull-to-refresh, swipe actions on rows

### iOS 26 Specifics
- Liquid Glass tab bars, toolbars, navigation bars
- Tab bar minimizes on scroll (`.tabBarMinimizeBehavior(.onScrollDown)`)
- Floating search button with `Tab(..., role: .search)`
- Dynamic wallpapers influence Liquid Glass appearance
- Layered app icons with motion parallax
- Edge-to-edge Safari

### Screen Sizes (points)
| Device | Width | Height |
|--------|-------|--------|
| iPhone SE (3rd) | 375 | 667 |
| iPhone 14/15 | 390 | 844 |
| iPhone 14/15 Pro Max | 430 | 932 |
| iPhone 16 Pro Max | 440 | 956 |

## iPadOS

### Key Characteristics
- **Multi-column** layouts (NavigationSplitView)
- **Sidebar** navigation (primary pattern)
- **Multitasking** — Split View, Slide Over, Stage Manager
- **Pointer/keyboard** support essential
- **Regular width** size class in most orientations

### iPad-Specific Patterns
- Popovers instead of action sheets
- Drag and drop between apps
- Keyboard shortcuts (`.keyboardShortcut()`)
- Pencil support where relevant
- `.navigationSplitViewColumnWidth()` for sidebar sizing

## macOS

### Key Characteristics
- **Menu bar** with full menu hierarchy — required for Mac apps
- **Window management** — Resize, minimize, full screen, multiple windows
- **Keyboard-first** with comprehensive shortcuts
- **Right-click** context menus everywhere
- **Smaller hit targets** — Pointer precision allows smaller controls
- **Toolbar** at window top (not bottom)

### macOS Tahoe (26) Specifics
- Transparent menu bar with Liquid Glass
- Contextual sidebars reflecting workspace context
- Spatial desktop widgets
- Floating Liquid Glass sidebar in NavigationSplitView

### Mac Catalyst / Designed for iPad
- Enable keyboard shortcuts
- Support resize and multiple windows
- Add menu bar items via `UIMenuBuilder`
- Adapt touch targets for pointer use
- Consider Mac-native frameworks (AppKit/SwiftUI) over Catalyst

### Key Differences from iOS
- Toolbar at top (not bottom tab bar)
- Settings via `Settings` scene (not in-app settings screen)
- `@Environment(\.openWindow)` for multi-window
- Hover effects (`.onHover()`)
- `.focusable()` for keyboard navigation

## watchOS

### Key Characteristics
- **Glanceable** — Information in 2-3 seconds
- **Brief interactions** — Most sessions < 10 seconds
- **Single-column** vertical scroll
- **Digital Crown** for scrolling and input
- **Complications** for at-a-glance data on watch face
- **Small screen**: 40mm (162×197), 41mm (176×215), 45mm (198×242), 49mm Ultra

### watchOS 26 Specifics
- Location-aware widgets in Smart Stack
- Fluid Control Center navigation
- Liquid Glass UI kit

### Design Principles
- Minimal text, large fonts
- Dark backgrounds (OLED power saving)
- System navigation (page-based or hierarchical)
- Use `.navigationBarTitleDisplayMode(.large)` for readability
- Haptic feedback for interactions
- 2-3 actions per screen maximum

### Complications / Widgets
- Provide WidgetKit timeline entries
- Support multiple widget families: `.accessoryCircular`, `.accessoryRectangular`, `.accessoryInline`, `.accessoryCorner`

## tvOS

### Key Characteristics
- **10-foot UI** — Large text, high contrast, designed for viewing distance
- **Focus-based** navigation (no touch, no pointer)
- **Siri Remote** — Swipe, click, Menu button
- **Parallax** effects on focused elements
- **Top shelf** — Showcase content on home screen

### Design Principles
- Content-forward: Full-bleed images, minimal chrome
- Large minimum text: 29pt body
- Focus states: Clear visual indicator of focused element
- Layered images for parallax effect
- Avoid dense text or complex forms

### tvOS 26
- Liquid Glass design language
- Parallax with Liquid Glass materials

## visionOS (Apple Vision Pro)

### Key Characteristics
- **Spatial computing** — Windows float in 3D space
- **Eye tracking + hand gestures** — Look and tap to interact
- **Windows, Volumes, Immersive Spaces** — Three content types
- **Glass material** background (original inspiration for Liquid Glass)
- **No fixed screen** — Adaptive layout

### Design Principles
- Windows: Standard 2D content in floating panels
- Volumes: 3D objects viewable from all angles
- Immersive Spaces: Full environment replacement
- **Minimum tap target: 60pt** (indirect eye-hand input is less precise)
- Use system glass material for window backgrounds
- Respect user's physical space
- Avoid overwhelming with too many floating windows

### visionOS 26
- Persistent spatial widgets
- Immersive photo experiences
- Liquid Glass refinements

### Ergonomics
- Place primary content at eye level
- Windows at comfortable distance (~1.5-2m)
- Avoid content that requires looking up/down for extended periods
- Use subtle depth cues, not extreme parallax

## Cross-Platform Strategy

### SwiftUI Shared Code
```swift
#if os(iOS)
    // iPhone/iPad specific
#elseif os(macOS)
    // Mac specific
#elseif os(watchOS)
    // Watch specific
#elseif os(tvOS)
    // TV specific
#elseif os(visionOS)
    // Vision Pro specific
#endif

// Or use environment
@Environment(\.horizontalSizeClass) var sizeClass
```

### Universal Design (iOS 26+)
- Liquid Glass provides visual consistency across all platforms
- Each platform maintains its own interaction paradigms
- Single SwiftUI codebase can adapt via size classes and platform checks
- App icons: One design in Icon Composer, auto-adapts per platform
- SF Symbols work identically across all platforms
