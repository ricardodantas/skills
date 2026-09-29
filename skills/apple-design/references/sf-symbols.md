# SF Symbols

## Overview

SF Symbols 8 offers **7,000+ symbols** that align with San Francisco, the Apple system font, across iOS, iPadOS, macOS, watchOS, tvOS, and visionOS. (Apple's What's New page calls it SF Symbols 8; the download is packaged as `SF-Symbols-27.dmg`.)

- Use symbols anywhere an interface icon can go: toolbars, tab bars, context menus, inline in text
- **Availability is versioned** — symbols and symbol features from a given year don't exist on earlier OS versions
- **License limits** — the terms forbid using symbols (or confusingly similar images) in app icons, logos, or any trademarked use

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols), [SF Symbols](https://developer.apple.com/sf-symbols/)

## Key Features
- **9 weights** — Ultralight through Black, each matching an SF font weight for exact weight-matching with adjacent text
- **3 scales** — Small, Medium (default), Large — defined relative to SF's cap height, so you can change a symbol's emphasis without breaking weight matching at the same point size
- **Automatic text alignment** — Symbols align with adjacent text
- **Dynamic Type support** — Scale with user's text size preference
- **Localization** — Script-specific variants (Latin, Arabic, Hebrew, Hindi, Thai, Chinese, Japanese, Korean, Cyrillic, Devanagari, several Indic numeral systems) that switch automatically with the device language

Scale APIs: `imageScale(_:)` (SwiftUI), `UIImage.SymbolScale` (UIKit), `NSImage.SymbolConfiguration` (AppKit).

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

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

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

## Rendering Modes

Symbols are built from layers with hierarchy levels (primary, secondary, tertiary). `cloud.sun.rain.fill`, for example, puts the cloud, the sun, and the raindrops on three separate layers; rendering modes color those layers differently.

| Mode | Description | Use |
|------|-------------|-----|
| **Monochrome** | One color on every layer (paths filled, or cut out of a filled path) | Default, simple icons |
| **Hierarchical** | One color, opacity stepped down per hierarchy level | Depth within one hue |
| **Palette** | One color per layer; with only two colors on a three-level symbol, secondary and tertiary share the second | Brand colors, multi-tone |
| **Multicolor** | Intrinsic colors that carry meaning (e.g. green `leaf`, red `trash.slash`); some layers accept your colors | System-standard appearance |

- **Use system colors** in any mode so symbols adapt to Dark Mode, vibrancy, and accessibility settings
- **Check legibility per context** — the automatic setting picks a symbol's preferred mode, but size and background contrast can make another mode read better

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

### Gradients (SF Symbols 7+)
- Generates a smooth linear gradient from a single source color
- Works in every rendering mode, with system or custom colors, and on custom symbols
- Renders at any size but looks best large

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

## Design Variants

| Variant | Best for |
|---------|----------|
| **Outline** (most common) | Toolbars, lists, next to text — no solid areas, reads like text |
| **Fill** | Emphasis: iOS tab bars, swipe actions, accent-colored selection |
| **Slash** | Showing an item or action is unavailable |
| **Enclosed** (circle, square, rectangle) | Better legibility at small sizes |

- Enclosed and slash variants often combine with outline or fill
- The hosting view usually picks outline vs. fill for you — an iOS tab bar prefers fill, a toolbar takes outline — so don't hard-code the variant there

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

## Symbol Effects (Animations)

Animations work on every symbol (including custom ones) in all rendering modes, weights, and scales. You can run them once or indefinitely, change speed, and choose whether to reverse before repeating.

| Effect | What it does | Use it to |
|--------|--------------|-----------|
| **Appear / Disappear** | Symbol gradually emerges / recedes | Show or hide an element |
| **Bounce** | Brief elastic up or down scale, then returns; plays once by default | Signal an action happened or is needed |
| **Scale** | Grows or shrinks and *stays* until changed | Highlight a selection, confirm a choice |
| **Pulse** | Varies opacity of layers annotated to pulse (optionally all) | Ongoing activity |
| **Variable color** | Steps opacity through layers — cumulative or iterative; can autoreverse or hide inactive layers | Progress, connecting, broadcasting, playback |
| **Replace** | Swaps symbols: down-up (state change), up-up (forward progress), off-up (emphasize next state) | State changes |
| **Magic Replace** | Default replace between related shapes (slashes draw, badges swap); falls back to down-up for unrelated symbols | Toggle-like changes |
| **Wiggle** | Moves back and forth along an axis | Call attention, reinforce direction |
| **Breathe** | Changes opacity *and* size smoothly | Live status such as recording |
| **Rotate** | Spins the whole symbol or only some layers (By Layer) | Work in progress |
| **Draw On / Off** (SF Symbols 7+) | Draws along guide points onto / off screen; all layers, staggered, or one at a time | Progress, directional meaning |

Variable-color layer order is annotated as **open loop** (linear; ends don't meet) or **closed loop** (a full shape, like a circular progress ring — repeats seamlessly).

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

// Wiggle / Breathe / Rotate
Image(systemName: "arrow.down").symbolEffect(.wiggle)
Image(systemName: "record.circle").symbolEffect(.breathe)
Image(systemName: "gear").symbolEffect(.rotate)

// Replace (transition between symbols)
Image(systemName: isOn ? "bell.fill" : "bell")
    .contentTransition(.symbolEffect(.replace))

// Draw On/Off (since SF Symbols 7)
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

### Animation Guidance
- **Be judicious** — no hard limit, but many simultaneous animations overwhelm and distract
- **Give each animation a clear purpose** — every effect implies a specific meaning; make sure combinations don't confuse
- **Use animation to say more in less space** — feedback that something happened, without extra UI
- **Match your app's tone** and brand

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

## Variable Symbols

Some symbols support continuous values (0.0–1.0):

```swift
Image(systemName: "speaker.wave.3", variableValue: volume)
// Progressively fills waves based on volume value
```

- Layers light up as the value crosses system-defined thresholds between 0 and 100% (e.g. `speaker.wave.3`: zero to three waves)
- Layers that don't represent the changing quantity (the speaker body) opt out; any number of layers can take part
- **Communicate change, not depth** — for depth and hierarchy use Hierarchical rendering instead

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

## SF Symbols 8 New Features

- **7,000+ symbols** — New symbols and design updates to existing ones; the new symbols require iOS, iPadOS, macOS, watchOS, tvOS, or visionOS 27
- **Enhanced Search** — Semantic search in the SF Symbols app: describe the concept in your own words and it surfaces matches even when the terms aren't in the symbol's name

### From SF Symbols 7 (still current)
- **Draw animations** — Calligraphic handwriting-style animate on/off
- **Variable Draw** — Layers as progress indicators with draw animation
- **Enhanced Magic Replace** — Preserves shared enclosure shapes during transitions
- **Gradients** — Auto-generated linear gradient from single source color

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

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

For the standard symbol per common action (copy, paste, share, filter, …) see [icon-design.md](icon-design.md#standard-symbols-for-common-actions).

Source: [HIG — Icons](https://developer.apple.com/design/human-interface-guidelines/icons)

## Custom Symbols

1. Export an existing symbol as SVG template from SF Symbols app
2. Edit in vector tool (Figma, Illustrator, Sketch)
3. Maintain the template structure (layers, margins, alignment guides)
4. Import back into SF Symbols app to validate
5. **Annotate** each layer with a color or hierarchy level (primary/secondary/tertiary) for the rendering modes you support
6. Add to Xcode asset catalog

### Custom Symbol Requirements
- Must maintain 9 weight variants (or subset that auto-interpolates)
- Respect alignment guides and margins from template
- Support all 3 scales
- Match system symbols in detail, optical weight, alignment, position, and perspective — simple, recognizable, inclusive, directly tied to the action
- For Draw animations: add guide points with the SF Symbols app's annotation tools (introduced in SF Symbols 7)

### Custom Symbol Guidance
- **Negative side margins** help optical alignment when a badge widens a symbol; name them with the configuration pattern (e.g. `left-margin-Regular-M`)
- **Animate by layer** — annotate layers in the SF Symbols app; Z-order sets variable-color order (front-to-back or back-to-front); group related layers to move together
- **Draw whole shapes** — instead of cutting gaps, draw the full shape plus an offset path annotated as an *erase* layer (e.g. a `person.2.fill`-style design). Keeps layer data intact for animation
- **Test every animation preset** — paths can look wrong in motion
- **Don't bake in enclosures or badges** — use the SF Symbols app's component library to generate those variants
- **Accessibility label** for every custom symbol
- **No Apple product replicas**, and symbols marked as Apple features/products can't be customized

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)

## Best Practices

- **Prefer SF Symbols over custom icons** for system concepts (share, delete, settings, etc.)
- Use **semantic names** when searching: describe the concept, not the shape (Enhanced Search in SF Symbols 8 matches on meaning)
- Gate symbols new in SF Symbols 8 behind the 27 OSes (`if #available`) or provide a fallback for older deployment targets
- Match symbol weight to adjacent text weight
- Use **hierarchical rendering** for added depth without extra colors
- Use **`.symbolVariant(.fill)`** for selected/active states, outline for inactive
- Don't use symbols at very small sizes where they become illegible
- Provide accessibility labels for symbol-only buttons
- Use `.contentTransition(.symbolEffect(.replace))` for smooth state changes
- Download the **SF Symbols app** (macOS) to browse and search all symbols

Source: [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols)
