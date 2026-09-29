# Liquid Glass Design Language

## Overview

Liquid Glass is Apple's unified design language introduced at WWDC 2025 (June 9, 2025). It's a translucent, dynamic material that reflects and refracts surrounding content. Shipped in iOS 26, iPadOS 26, macOS Tahoe, tvOS 26, visionOS 26, and watchOS 26.

**Refined in 27** (WWDC26, June 8, 2026; shipped September 14, 2026): more uniform refraction and improved contrast, plus a user-facing Liquid Glass slider. The SwiftUI `Glass` API (`.regular`, `.clear`, `.identity`, `.tint()`, `.interactive()`) is unchanged — no new variants. See [What Changed in 27](#what-changed-in-27).

**Key principle**: Liquid Glass is ONLY for the navigation/control layer that floats above content. Never apply to content itself.

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Core Characteristics

- **Lensing** — Bends and concentrates light in real-time (not just blur)
- **Materialization** — Elements appear by gradually modulating light bending
- **Fluidity** — Gel-like flexibility with instant touch responsiveness
- **Morphing** — Dynamic transformation between control states
- **Adaptivity** — Multi-layer composition adjusting to content, color scheme, and size
- **Device motion response** — Reacts to iPhone/iPad gyroscope for parallax effect

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Material Variants

| Variant | Use Case | Transparency |
|---------|----------|-------------|
| `.regular` | Default — toolbars, nav bars, tab bars, buttons | Medium, fully adaptive |
| `.clear` | Small floating controls over media-rich backgrounds | High, requires bold foreground |
| `.identity` | Conditional disable (no effect) | N/A |

- `.regular` blurs the backdrop and adjusts its luminosity so foreground text stays legible; most system components use it. Choose it when the backdrop could hurt legibility or the component is text-heavy (alerts, sidebars, popovers)
- `.clear` is highly translucent and keeps rich backdrops prominent — reserve it for components floating over photos and video
- Both variants change with the user's preferred Liquid Glass look and with Reduce Transparency / Increase Contrast

### When to Use `.clear` (ALL must be true):
- Element sits over media-rich content
- Content won't be negatively affected by dimming layer
- Content above glass is bold and bright

### Dimming Layer for `.clear`
- Bright content underneath → consider a dark dimming layer at **35% opacity**
- Content already dark, or you use AVKit's standard playback controls (they supply their own dimming) → skip the dimming layer

### Where Glass Belongs
- Functional layer only: tab bars, sidebars, toolbars, navigation, controls. Use standard materials (below) for content-layer surfaces such as app backgrounds
- Exception: transient content-layer controls such as sliders and toggles take on a glass look while someone is actively using them
- Custom controls: apply glass sparingly, only to the most important functional elements — overuse pulls attention from content. System components adopt it automatically

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Standard Materials (Content Layer)

Blur, vibrancy, and blending materials give structure to the content *beneath* the glass layer.

- **Pick by purpose, not by color** — system settings can change a material's look, so match the material/vibrancy style to the use case
- **Use vibrant (system) colors on top of materials** — e.g. `systemGray3` on a material reads poorly; a vibrant label color doesn't
- **Thickness trade-off** — thicker (more opaque) materials give better contrast for text and fine detail; thinner ones keep more of the background visible for context
- SwiftUI: `Material` (`.ultraThin`, `.thin`, `.regular`, `.thick`); UIKit: `UIVisualEffectView`; AppKit: `NSVisualEffectView`

| Platform | Guidance |
|----------|----------|
| iOS, iPadOS | Four materials: ultra-thin, thin, regular (default), thick. Vibrancy for labels (default, secondary, tertiary, quaternary), fills (default, secondary, tertiary), and one separator level. Avoid quaternary labels on thin/ultra-thin — contrast too low |
| macOS | Purpose-specific `NSVisualEffectView.Material`s plus vibrant versions of all system colors. Two blending modes: behind-window and within-window. Test where vibrancy helps before enabling it in custom views |
| tvOS | Glass on navigation, Top Shelf, Control Center; image views and buttons adopt it on focus. Standard materials: `ultraThin` full-screen light, `thin` overlay light, `regular` overlay, `thick` overlay dark |
| visionOS | Windows use a fixed system *glass* material — prefer translucency over opaque fills. Custom components: `thin` for interactive/selected items, `regular` to separate sections (sidebar, grouped table), `thick` for a dark element on a `regular` background. Vibrancy: `label` (standard), `secondaryLabel` (footnotes/subtitles), `tertiaryLabel` (inactive only) |
| watchOS | Materials give context in full-screen modals; keep the default material backgrounds of modal sheets |

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Basic Implementation

```swift
// Default glass (regular variant, capsule shape)
Text("Hello, Liquid Glass!")
    .padding()
    .glassEffect()

// Explicit parameters
Text("Custom Glass")
    .padding()
    .glassEffect(.regular, in: .capsule, isEnabled: true)

// API signature
func glassEffect<S: Shape>(
    _ glass: Glass = .regular,
    in shape: S = DefaultGlassEffectShape,
    isEnabled: Bool = true
) -> some View
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Tinting

Use tint to convey **semantic meaning** (primary action, state), NOT decoration:

```swift
// Tinted glass
Text("Primary").padding().glassEffect(.regular.tint(.blue))

// Subtle tint
Text("Subtle").padding().glassEffect(.regular.tint(.purple.opacity(0.6)))
```

Source: [HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)

## Interactive Glass

Enables scaling on press, bouncing, shimmering, and touch-point illumination. On macOS 27, custom glass marked interactive also responds to clicks, tuned for the pointer:

```swift
Button("Tap Me") { /* action */ }
    .glassEffect(.regular.interactive())

// Chaining
.glassEffect(.regular.tint(.orange).interactive())
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Shapes

```swift
.glassEffect(.regular, in: .capsule)                              // Default
.glassEffect(.regular, in: .circle)                                // Circular
.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))    // Rounded rect
.glassEffect(.regular, in: .rect(cornerRadius: .containerConcentric))  // Matches container corners
.glassEffect(.regular, in: .ellipse)                               // Ellipse
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## GlassEffectContainer

**Critical**: Multiple glass elements MUST be wrapped in a container. Glass cannot sample other glass.

```swift
GlassEffectContainer {
    HStack(spacing: 20) {
        Image(systemName: "pencil")
            .frame(width: 44, height: 44)
            .glassEffect(.regular.interactive())
        Image(systemName: "eraser")
            .frame(width: 44, height: 44)
            .glassEffect(.regular.interactive())
    }
}

// With spacing control (elements within range morph together)
GlassEffectContainer(spacing: 40.0) {
    // Glass elements within 40pt blend/morph during transitions
}
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Morphing Transitions

Requirements: Same `GlassEffectContainer` + `glassEffectID` with shared namespace:

```swift
struct MorphingExample: View {
    @State private var isExpanded = false
    @Namespace private var namespace

    var body: some View {
        GlassEffectContainer(spacing: 30) {
            Button(isExpanded ? "Collapse" : "Expand") {
                withAnimation(.bouncy) { isExpanded.toggle() }
            }
            .glassEffect()
            .glassEffectID("toggle", in: namespace)

            if isExpanded {
                Button("Action") { }
                    .glassEffect()
                    .glassEffectID("action", in: namespace)
            }
        }
    }
}
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Button Styles

```swift
Button("Cancel") { }.buttonStyle(.glass)           // Secondary - translucent
Button("Save") { }.buttonStyle(.glassProminent)     // Primary - opaque
    .tint(.blue)
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Toolbars

Toolbars automatically receive Liquid Glass (iOS 26+):

```swift
.toolbar {
    ToolbarItem(placement: .cancellationAction) {
        Button("Cancel", systemImage: "xmark") { }
    }
    ToolbarItem(placement: .confirmationAction) {
        Button("Done", systemImage: "checkmark") { }  // Auto .glassProminent
    }
}
```

Features:
- Prioritizes symbols over text
- `ToolbarSpacer(.fixed, spacing: 20)` for grouping
- `.badge(5)` for notification counts
- `.sharedBackgroundVisibility(.hidden)` to remove glass from specific items
- 27 adds visibility priority, `ToolbarOverflowMenu`, `.topBarPinnedTrailing`, and minimization — see [hig-components.md](hig-components.md#ios-27-toolbar-additions)

Glass-era toolbar rules:
- **Few groups** — group by function and frequency; aim for three groups at most. Navigation and Done/Close/Save get their own distinct groups
- **One prominent action** (e.g. Done, Submit), tinted, on the trailing side; otherwise keep tinted controls rare
- **Symbols over text** — borderless system symbols; keep text-labeled buttons apart (fixed space) so labels don't merge or look like one symbol+text button
- **Color** — don't give item labels a color close to the content background; over bright, colorful content keep the default monochrome toolbar
- Use a scroll edge effect (`ScrollEdgeEffectStyle`) when the bar needs separating from content, not a solid background

Source: [HIG — Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

## TabView

```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Search", systemImage: "magnifyingglass", role: .search) { SearchView() }
    // role: .search creates floating search button (bottom-right)
}
.tabBarMinimizeBehavior(.onScrollDown)  // Collapses during scroll
.tabViewBottomAccessory {  // Persistent mini player etc.
    NowPlayingBar()
}
```

- The iPhone tab bar floats at the bottom on a glass background that lets content peek through; a dedicated search tab sits at the trailing end
- With an accessory (e.g. Music's MiniPlayer), the bar can minimize on scroll-down and pull the accessory inline; tapping a tab or scrolling to the top restores it
- Over bright, colorful content use a monochrome tab bar or a clearly differentiated accent color
- Fewer tabs navigate more easily; if people customize tabs, default to five or fewer. Overflow becomes a More tab — avoid relying on it
- Badges (red oval, number or `!`) only for critical, new information
- iPadOS: the tab bar sits near the top and can offer conversion to a sidebar for richer navigation

Source: [HIG — Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)

## Sheets

Sheets auto-apply Liquid Glass (iOS 26+):

```swift
.sheet(isPresented: $showSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])
}
// ❌ Don't: .presentationBackground(Color.white)
// ✅ Do: Let system apply glass automatically
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## NavigationSplitView

Sidebar automatically gets floating Liquid Glass:

```swift
NavigationSplitView {
    SidebarList()
} detail: {
    HeroImage()
        .backgroundExtensionEffect()  // Mirrors + blurs the image under the sidebar
}
```

- Sidebars (iOS, iPadOS, macOS) float in the glass layer; extend rich content beneath them — horizontal scrolling or a background extension effect (`backgroundExtensionEffect()` / `UIBackgroundExtensionView`) on the *content*, not the sidebar
- Show at most two hierarchy levels; deeper data → add a content list column (split view)
- Sidebar icons use the accent color by default (and follow the user's macOS accent color); fixed colors only sparingly, when they carry meaning (Mail's yellow VIP)
- Let people hide/show the sidebar with familiar interactions (iPadOS edge swipe; macOS button or View menu commands) but don't hide it by default

Source: [HIG — Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars)

## Accessibility

Liquid Glass auto-adapts — no code needed:
- **Reduce Transparency**: Increases frosting for clarity
- **Increase Contrast**: Stark colors and borders
- **Reduce Motion**: Tones down animations/elastic effects
- **Liquid Glass slider (27)**: A Settings slider from ultra-clear to fully tinted (iOS, iPadOS, macOS, watchOS, visionOS), replacing the 26.1 Tinted toggle. Standard glass follows it automatically; there's no public API to read its value

```swift
// Manual override (rarely needed)
@Environment(\.accessibilityReduceTransparency) var reduceTransparency
.glassEffect(reduceTransparency ? .identity : .regular)
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Advanced APIs

### glassEffectUnion
Manually combine distant glass effects:
```swift
Button("Edit") { }
    .buttonStyle(.glass)
    .glassEffectUnion(id: "tools", namespace: controls)
// ... large gap ...
Button("Delete") { }
    .buttonStyle(.glass)
    .glassEffectUnion(id: "tools", namespace: controls)
```

### glassEffectTransition
```swift
.glassEffectTransition(.materialize)    // Material appearance
.glassEffectTransition(.matchedGeometry) // Default matched geometry
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## What Changed in 27

Introduced in 26, refined in 27. Existing glass code keeps working and picks up the new look on recompile.

- **Refined material** — more uniform refraction and improved contrast; standard glass adapts to the user's Liquid Glass slider automatically
- **Scroll edge effects** — `.automatic` now has its own visuals instead of switching between soft and hard. If you forced `.soft`, re-evaluate: it no longer matches the system default
- **Toolbar minimization** — navigation bars can slide away on scroll (an integrated top tab bar minimizes with them). UIKit: `navigationItem.navigationBarMinimization`
- **Prominent tab** — `role: .prominent` gives one tab a separate trailing position in the tab bar. Only one tab can be prominent; without one, a `.search` tab may get the treatment
- **Interactive glass on macOS** — `.interactive()` custom glass responds fluidly to clicks and the pointer
- **Compatibility opt-out removed** — `UIDesignRequiresCompatibility` is ignored when building for iOS, iPadOS, Mac Catalyst, macOS, or tvOS 27

```swift
NavigationStack {
    ScrollView { /* ... */ }
        .toolbarMinimizationBehavior(.onScrollDown, for: .navigationBar)
        // Only for full-bleed media that must not reflow as the bar hides
        .toolbarMinimizationSafeAreaAdjustment(.disabled, for: .navigationBar)
}

TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Cart", systemImage: "cart", role: .prominent) { CartView() }
}
```

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Migration Checklist

1. **Recompile with Xcode 27** (Swift 6.4; requires macOS Tahoe 26.6+) — system controls adopt the refined glass automatically
2. **Delete `UIDesignRequiresCompatibility`** from Info.plist — ignored with the 27 SDK, so every app gets Liquid Glass
3. **Remove custom backgrounds** from sheets, nav bars, tab bars
4. **Wrap multiple glass elements** in `GlassEffectContainer`
5. **Update app icons** to multi-layer format via Icon Composer
6. **Test with Reduce Transparency** enabled, and at both ends of the Liquid Glass slider
7. **Remove custom toolbar styling** that conflicts with glass
8. **Re-check scroll edge effect overrides** (especially `.soft`) against the new `.automatic` look
9. **Use `.scrollContentBackground(.hidden)`** in Forms for glass effect
10. **Test on older devices** (iPhone 11-13 may show GPU lag)
11. **Mind the SDK deadline** — from April 2027, iOS, iPadOS, tvOS, visionOS, and watchOS uploads must be built with the 27 SDKs

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Performance Tips

- Always use `GlassEffectContainer` for multiple elements (shared sampling)
- Toggle with `.identity` instead of removing/adding glass (avoids layout recalc)
- Avoid continuous animations on glass elements
- Profile with Instruments for GPU usage on older devices
- Glass auto-adapts between light/dark based on background content

Source: [HIG — Materials](https://developer.apple.com/design/human-interface-guidelines/materials)
