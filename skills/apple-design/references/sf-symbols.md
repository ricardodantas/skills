# SF Symbols

## Overview

SF Symbols 7 is a library of **6,900+ symbols** designed to integrate with San Francisco (SF), the system font for Apple platforms. Available across iOS, macOS, watchOS, tvOS, and visionOS.

## Key Features
- **9 weights** — Ultralight through Black (matching SF font weights)
- **3 scales** — Small, Medium, Large
- **Automatic text alignment** — Symbols align with adjacent text
- **Dynamic Type support** — Scale with user's text size preference
- **Localization** — Variants for Latin, Greek, Cyrillic, Hebrew, Arabic, CJK, Thai, Devanagari, Indic

## Usage

### SwiftUI
```swift
// Basic
Image(systemName: "heart.fill")

// With font matching
Image(systemName: "gear")
    .font(.title)

// With label
Label("Settings", systemImage: "gear")

// Sizing
Image(systemName: "star")
    .imageScale(.large)  // .small, .medium, .large
```

### UIKit
```swift
let image = UIImage(systemName: "heart.fill")
let config = UIImage.SymbolConfiguration(pointSize: 24, weight: .medium)
let image = UIImage(systemName: "heart.fill", withConfiguration: config)
```

## Rendering Modes

| Mode | Description | Use |
|------|-------------|-----|
| **Monochrome** | Single color, uniform | Default, simple icons |
| **Hierarchical** | Single color, layered opacity | Depth within one hue |
| **Palette** | Multiple custom colors per layer | Brand colors, multi-tone |
| **Multicolor** | Predefined Apple colors | System-standard appearance |

```swift
// Monochrome (default)
Image(systemName: "heart.fill")
    .foregroundStyle(.red)

// Hierarchical
Image(systemName: "square.stack.3d.up.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.blue)

// Palette
Image(systemName: "person.crop.circle.badge.plus")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.blue, .green)

// Multicolor
Image(systemName: "externaldrive.badge.wifi")
    .symbolRenderingMode(.multicolor)
```

## Symbol Effects (Animations)

### Available Effects
```swift
// Bounce
Image(systemName: "bell").symbolEffect(.bounce)

// Pulse (opacity)
Image(systemName: "network").symbolEffect(.pulse)

// Variable color (waves)
Image(systemName: "wifi").symbolEffect(.variableColor)

// Scale
Image(systemName: "heart").symbolEffect(.scale.up)

// Appear/Disappear
Image(systemName: "plus").symbolEffect(.appear)

// Replace (transition between symbols)
Image(systemName: isOn ? "bell.fill" : "bell")
    .contentTransition(.symbolEffect(.replace))

// Draw On/Off (NEW in SF Symbols 7)
Image(systemName: "checkmark").symbolEffect(.drawOn)
```

### Animation Options
```swift
// One-shot
.symbolEffect(.bounce, value: triggerValue)

// Continuous
.symbolEffect(.pulse.continuous)

// Playback modes for Draw
// .wholeSymbol — all layers together
// .byLayer — offset layer start times
// .individually — one layer at a time
```

## Variable Symbols

Some symbols support continuous values (0.0–1.0):

```swift
Image(systemName: "speaker.wave.3", variableValue: volume)
// Progressively fills waves based on volume value
```

## SF Symbols 7 New Features

- **Draw animations** — Calligraphic handwriting-style animate on/off
- **Variable Draw** — Layers as progress indicators with draw animation
- **Enhanced Magic Replace** — Preserves shared enclosure shapes during transitions
- **Gradients** — Auto-generated linear gradient from single source color
- **Hundreds of new symbols** — Updated for Liquid Glass design language

## Categories

Common categories for finding symbols:
- **General**: `star`, `heart`, `bookmark`, `flag`, `bell`, `tag`
- **Communication**: `message`, `envelope`, `phone`, `video`
- **Weather**: `sun.max`, `cloud`, `cloud.rain`, `snow`
- **Devices**: `iphone`, `desktopcomputer`, `applewatch`
- **Editing**: `pencil`, `scissors`, `paintbrush`, `eraser`
- **Media**: `play`, `pause`, `stop`, `forward`, `backward`
- **Navigation**: `chevron.right`, `arrow.left`, `house`, `magnifyingglass`
- **People**: `person`, `person.2`, `figure.walk`
- **Nature**: `leaf`, `flame`, `drop`, `ant`
- **Health**: `heart.text.square`, `waveform.path.ecg`
- **Accessibility**: `accessibility`, `figure.roll`, `ear`

## Custom Symbols

1. Export an existing symbol as SVG template from SF Symbols app
2. Edit in vector tool (Figma, Illustrator, Sketch)
3. Maintain the template structure (layers, margins, alignment guides)
4. Import back into SF Symbols app to validate
5. Add to Xcode asset catalog

### Custom Symbol Requirements
- Must maintain 9 weight variants (or subset that auto-interpolates)
- Respect alignment guides and margins from template
- Support all 3 scales
- For Draw animations: add guide points via SF Symbols 7 annotation tools

## Best Practices

- **Prefer SF Symbols over custom icons** for system concepts (share, delete, settings, etc.)
- Use **semantic names** when searching: describe the concept, not the shape
- Match symbol weight to adjacent text weight
- Use **hierarchical rendering** for added depth without extra colors
- Use **`.symbolVariant(.fill)`** for selected/active states, outline for inactive
- Don't use symbols at very small sizes where they become illegible
- Provide accessibility labels for symbol-only buttons
- Use `.contentTransition(.symbolEffect(.replace))` for smooth state changes
- Download the **SF Symbols app** (macOS) to browse and search all symbols
