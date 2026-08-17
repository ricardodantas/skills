# Liquid Glass Design Language

## Overview

Liquid Glass is Apple's unified design language introduced at WWDC 2025 (June 9, 2025). It's a translucent, dynamic material that reflects and refracts surrounding content. Shipped in iOS 26, iPadOS 26, macOS Tahoe, tvOS 26, visionOS 26, and watchOS 26.

**Key principle**: Liquid Glass is ONLY for the navigation/control layer that floats above content. Never apply to content itself.

## Core Characteristics

- **Lensing** — Bends and concentrates light in real-time (not just blur)
- **Materialization** — Elements appear by gradually modulating light bending
- **Fluidity** — Gel-like flexibility with instant touch responsiveness
- **Morphing** — Dynamic transformation between control states
- **Adaptivity** — Multi-layer composition adjusting to content, color scheme, and size
- **Device motion response** — Reacts to iPhone/iPad gyroscope for parallax effect

## Material Variants

| Variant | Use Case | Transparency |
|---------|----------|-------------|
| `.regular` | Default — toolbars, nav bars, tab bars, buttons | Medium, fully adaptive |
| `.clear` | Small floating controls over media-rich backgrounds | High, requires bold foreground |
| `.identity` | Conditional disable (no effect) | N/A |

### When to Use `.clear` (ALL must be true):
- Element sits over media-rich content
- Content won't be negatively affected by dimming layer
- Content above glass is bold and bright

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

## Tinting

Use tint to convey **semantic meaning** (primary action, state), NOT decoration:

```swift
// Tinted glass
Text("Primary").padding().glassEffect(.regular.tint(.blue))

// Subtle tint
Text("Subtle").padding().glassEffect(.regular.tint(.purple.opacity(0.6)))
```

## Interactive Glass (iOS only)

Enables scaling on press, bouncing, shimmering, and touch-point illumination:

```swift
Button("Tap Me") { /* action */ }
    .glassEffect(.regular.interactive())

// Chaining
.glassEffect(.regular.tint(.orange).interactive())
```

## Shapes

```swift
.glassEffect(.regular, in: .capsule)                              // Default
.glassEffect(.regular, in: .circle)                                // Circular
.glassEffect(.regular, in: RoundedRectangle(cornerRadius: 16))    // Rounded rect
.glassEffect(.regular, in: .rect(cornerRadius: .containerConcentric))  // Matches container corners
.glassEffect(.regular, in: .ellipse)                               // Ellipse
```

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

## Button Styles

```swift
Button("Cancel") { }.buttonStyle(.glass)           // Secondary - translucent
Button("Save") { }.buttonStyle(.glassProminent)     // Primary - opaque
    .tint(.blue)
```

## Toolbars

Toolbars automatically receive Liquid Glass in iOS 26:

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

## Sheets

iOS 26 sheets auto-apply Liquid Glass:

```swift
.sheet(isPresented: $showSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])
}
// ❌ Don't: .presentationBackground(Color.white)
// ✅ Do: Let system apply glass automatically
```

## NavigationSplitView

Sidebar automatically gets floating Liquid Glass:

```swift
NavigationSplitView {
    SidebarList()
        .backgroundExtensionEffect()  // Extends beyond safe area
} detail: {
    DetailView()
}
```

## Accessibility

Liquid Glass auto-adapts — no code needed:
- **Reduce Transparency**: Increases frosting for clarity
- **Increase Contrast**: Stark colors and borders
- **Reduce Motion**: Tones down animations/elastic effects
- **iOS 26.1+ Tinted Mode**: User-controlled opacity (Settings → Display & Brightness → Liquid Glass)

```swift
// Manual override (rarely needed)
@Environment(\.accessibilityReduceTransparency) var reduceTransparency
.glassEffect(reduceTransparency ? .identity : .regular)
```

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

## Migration Checklist

1. **Recompile with Xcode 26** — System controls auto-adopt Liquid Glass
2. **Remove custom backgrounds** from sheets, nav bars, tab bars
3. **Wrap multiple glass elements** in `GlassEffectContainer`
4. **Update app icons** to multi-layer format via Icon Composer
5. **Test with Reduce Transparency** enabled
6. **Remove custom toolbar styling** that conflicts with glass
7. **Use `.scrollContentBackground(.hidden)`** in Forms for glass effect
8. **Test on older devices** (iPhone 11-13 may show GPU lag)
9. **Full adoption required by iOS 27** — retention option will be removed

## Performance Tips

- Always use `GlassEffectContainer` for multiple elements (shared sampling)
- Toggle with `.identity` instead of removing/adding glass (avoids layout recalc)
- Avoid continuous animations on glass elements
- Profile with Instruments for GPU usage on older devices
- Glass auto-adapts between light/dark based on background content
