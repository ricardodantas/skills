# App Icon Design

## Overview

Starting with iOS 26, app icons use a **multi-layer Liquid Glass format** created with Apple's **Icon Composer** tool. Icons feature translucency, glass-like shimmer, and react to device movement. The 27 OSes render icons with a new, **sharper** Liquid Glass material; Icon Composer 2 lets you tune and preview it.

- The icon shows up far beyond the Home Screen: search results, notifications, Settings, share sheets — design for recognition at a glance
- Keep one visually consistent design across every platform you ship on, so people never mistake it for two different apps
- Interface icons (glyphs inside your UI) follow different rules — see [Interface Icons](#interface-icons-glyphs)

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Icon Composer

Icon Composer is Apple's tool for creating layered Liquid Glass icons for **iOS, iPadOS, macOS, and watchOS**. The current release is **Icon Composer 2** (ships alongside Xcode 27). tvOS and visionOS icons are still built as image stacks in Xcode (see [Platform Notes](#platform-notes)).

### Key Features
- **Multi-platform from single design** — One design adapts to iPhone, iPad, Mac, Apple Watch
- **Background layer defined in the tool** — solid colors and gradients, so importing a background image is rarely needed
- **Liquid Glass properties** — Adjust specular highlights, refraction, blur, translucency, shadows
- **Appearance annotations** — Default, Dark, Mono (the system builds the clear and tinted looks; see [Appearance Modes](#appearance-modes))
- **Real-time preview** — See dynamic lighting, different backgrounds, various sizes, and different system versions
- **Xcode integration** — New icon file type syncs directly to project
- **Export** — Flattened version available for marketing materials

### New in Icon Composer 2
- **Sharper rendering mode** for the 27 OSes, adding refractivity, outside specular, and deeper shadows (set per group in the Style inspector)
- **Design-generation preview** — the canvas Effects buttons (e.g. 26 vs 27) compare the original and new design generations; when the icon looks right in both, add it to Xcode for use across all OS versions
- **Specular** — Off, Automatic (default), Inside, or Outside

### Download
- Included with Xcode; also available from developer.apple.com/icon-composer
- Requires macOS Tahoe 26.4 or later

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Multi-Layer Icon Format

### Layer Structure
Icons consist of multiple layers that create depth with Liquid Glass:
1. **Background layer** — Base color/gradient
2. **Middle layers** — Design elements, patterns
3. **Foreground layer** — Primary symbol/glyph

| Platform | Layers | System treatment |
|----------|--------|------------------|
| iOS, iPadOS, macOS, watchOS | Background + one or more foreground layers | Liquid Glass: specular highlights, refraction, translucency; adapts with icon size and may differ between system versions |
| tvOS | 2–5 layers | Parallax: icon lifts, sways, and illuminates on focus |
| visionOS | Background + 1–2 layers on top | 3D object that expands on gaze; system shadows between layers, upper-layer alpha used for an embossed look |

### Liquid Glass Properties Per Layer
- **Specular highlights** — Light reflection intensity
- **Refraction** — How strongly the layer bends and picks up what's behind it (subtle edge bend to lens-like) — visible only on the 27 OSes
- **Blur** — Frosted glass effect amount
- **Translucency** — How much background shows through
- **Shadows** — Depth and dimension

### Layer Rules
- **Crisp edges on foreground shapes** — soft or feathered edges spoil the system-drawn highlights and shadows
- **Vary opacity across foreground layers** for depth; import them fully opaque and dial transparency in Icon Composer so you can see how it interacts with system effects
- **Background** — should stand out while emphasizing the foreground; if you use a gradient, check it under system lighting. An imported background must be full-bleed and opaque
- **Formats** — prefer vector (SVG or PDF); outline artwork and convert text to outlines. Use PNG (lossless) for mesh gradients and raster art
- **Group layers** to apply effects at the group level — groups get extra Liquid Glass controls (specular, refraction, translucency)

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Icon Shape & Masking

| Platform | Layers you supply | Shape after masking |
|----------|-------------------|---------------------|
| iOS, iPadOS, macOS | Square | Rounded rectangle, concentric with device bezel and UI corners |
| tvOS | Rectangle (landscape) | Rounded rectangle |
| visionOS, watchOS | Square | Circle |

- **Rounder enclosure shapes** in iOS 26 (updated from iOS 18 superellipse)
- **Supply unmasked layers** — the system masks every layer edge. Pre-masked or pre-rounded art breaks specular highlights and produces jagged edges
- **Keep primary content centered** so corner adjustment and masking don't truncate it — especially for the circular visionOS and watchOS icons. Use the grids in the Apple Design Resources production templates
- Single design scales across platforms by default; customize per-platform if needed

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Icon Design Guidelines

### Design Principles
1. **Simplicity** — One core idea, a minimal number of shapes. Fine detail gets busy under system shadows/highlights and vanishes at small sizes
2. **Simple background** — a solid color or gradient; you don't need to fill the whole canvas
3. **Filled, overlapping shapes** — solid overlapping foreground shapes (with transparency and blur) read as depth; outline-only shapes don't
4. **Text only when essential** — text can't be localized or read by accessibility, is often too small, and the app name usually sits right beside the icon. A single-letter mnemonic is fine; avoid words like "Watch", "Play", "New", or "For visionOS"
5. **Illustrations over photos** — photos lose detail at small sizes, across appearances, and when split into layers. Avoid hairline strokes and sharp corners
6. **Don't replicate UI** — no standard UI components or screenshots in the icon
7. **No Apple hardware replicas** — they're copyrighted
8. **Unique silhouette** — Distinguishable from other icons even as a shape

### Color
- Use a limited, distinctive color palette
- Ensure sufficient contrast with any wallpaper
- Gradients work well with Liquid Glass depth effect — but verify them under system lighting
- Test against light and dark wallpapers

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Visual Effects

- **Let the system draw effects** — skip baked-in specular highlights, inter-layer drop shadows, bevels, blurs, and glows. Custom effects are static, conflict with the dynamic system ones, and look dated
- If you do add a custom effect, make it intentional and test it in Icon Composer, on a simulated device in Xcode's Device Hub, and on hardware
- Avoid overly complex layers — Liquid Glass refraction amplifies complexity
- Test with dynamic lighting to ensure layers look good in motion

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Appearance Modes

On iOS, iPadOS, and macOS people choose how Home Screen icons look. Any variant you don't design, the system generates.

| Mode | Description | Context |
|------|-------------|---------|
| **Default** | Full color, standard appearance | Light mode, default wallpapers |
| **Dark** | Subdued colors adapted for dark backgrounds | Dark mode |
| **Clear** (light / dark) | Transparent Liquid Glass | Clear Home Screen look (introduced in iOS 26) |
| **Tinted** (light / dark) | Single-color tinted | Tinted Home Screen look |

In Icon Composer you annotate **Default, Dark, and Mono** variants.

- **Keep core features identical across appearances** — don't swap elements in and out per variant; people should find the app after switching looks
- **Derive dark from light** — complementary colors, no glaring brights; colored backgrounds usually give the most contrast in dark icons
- **Dark, clear, and tinted are progressively more subdued** — the icon must stay visible and recognizable next to system icons and widgets in each
- **Alternate icons** — people can pick one in your app's settings (iOS, iPadOS, tvOS, and compatible apps on visionOS). Keep each alternate clearly tied to your app so it isn't mistaken for another one

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Platform Notes

- **tvOS** — build layers as an image stack in Xcode; keep a safe zone because focus scaling and motion crop edges (foreground layers are cropped more than background). Put any text above the other layers so parallax doesn't crop it. Preview with the Parallax Previewer / Parallax Exporter plug-in from Apple Design Resources
- **visionOS** — image stack in Xcode; don't put a hole- or concave-looking shape in the background layer (system shadows and highlights make it pop out instead of recede)
- **watchOS** — don't use a black background; lighten it so the icon doesn't disappear into the display
- **iOS, iPadOS, macOS** — no extra considerations beyond the above

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Specifications

| Platform | Layout canvas | Style | Appearances |
|----------|---------------|-------|-------------|
| iOS, iPadOS, macOS | 1024×1024 px, square | Layered | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | 800×480 px, landscape rectangle | Layered (parallax) | — |
| visionOS | 1024×1024 px, square | Layered (3D) | — |
| watchOS | 1088×1088 px, square | Layered | — |

- The system scales your icon down for smaller placements (Settings, notifications, etc.) — you don't hand-produce each size
- Color spaces: sRGB, Gray Gamma 2.2 (grayscale), and Display P3 (wide gamut; not on visionOS)

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Workflow

1. **Design** artwork layers in your vector tool (Figma, Sketch, Illustrator)
2. **Import** layers into Icon Composer; define the background there
3. **Adjust** placement and Liquid Glass properties (specular, refraction, blur, translucency, shadow), per layer or per group
4. **Preview** across sizes, backgrounds, appearance modes, lighting, and both design generations (new and original)
5. **Annotate** Dark and Mono variants (within same file)
6. **Add to Xcode** — Icon Composer file integrates directly
7. **Export** flattened version for marketing/App Store if needed

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Common Mistakes
- ❌ Flat single-layer icons (look outdated on iOS 26 and later)
- ❌ Checking only one design generation (test the icon in both the new 27 rendering and the original)
- ❌ Including rounded corners or circular masks in artwork (system applies the mask)
- ❌ Soft/feathered foreground edges, or baked-in shadows and highlights
- ❌ Nonessential text in icons (illegible at small sizes, not localizable)
- ❌ Too much detail (Liquid Glass refraction makes it noisy)
- ❌ Not testing Dark, Clear, and Tinted looks (icon may be invisible)
- ❌ Not testing at the smallest system placements
- ❌ Black watchOS icon background

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)

## Interface Icons (Glyphs)

Small, streamlined icons inside your UI (toolbars, menus, buttons). Prefer [SF Symbols](sf-symbols.md); design custom glyphs only when no symbol fits. Like symbols, glyphs use black and clear areas so the system can recolor them.

- **Simplify** — one familiar metaphor tied directly to the action or content
- **Consistency across the set** — same size, level of detail, stroke weight, and perspective; nudge sizes of visually light glyphs so they balance with heavier ones
- **Match adjacent text weight** unless you intend emphasis
- **Optical centering** — asymmetric glyphs (e.g. a download arrow) can look off-center when geometrically centered; bake the correction into the asset's padding
- **No custom selected state** in toolbars, tab bars, and buttons — the system handles it (a selected toolbar item gets the accent color)
- **Inclusive imagery** — gender-neutral figures, culturally neutral metaphors
- **Text in glyphs** — only when essential (e.g. text formatting); localize characters and supply a right-to-left flipped version of abstract "text" glyphs
- **Vector format** (PDF or SVG) so the system scales it; PNG needs multiple resolutions. Or make a custom SF Symbol
- **Accessibility label** on every custom glyph for VoiceOver
- **No Apple hardware replicas** — use Apple Design Resources images or the product SF Symbols

### Standard Symbols for Common Actions

| Action | Symbol | Action | Symbol |
|--------|--------|--------|--------|
| Cut | `scissors` | Undo / Redo | `arrow.uturn.backward` / `arrow.uturn.forward` |
| Copy | `document.on.document` | Compose | `square.and.pencil` |
| Paste | `document.on.clipboard` | Duplicate | `plus.square.on.square` |
| Done / Save | `checkmark` | Rename | `pencil` |
| Cancel / Close | `xmark` | Move to / Folder | `folder` |
| Delete | `trash` | Attach | `paperclip` |
| Add | `plus` | More | `ellipsis` |
| Select | `checkmark.circle` | Search | `magnifyingglass` |
| Find | `text.page.badge.magnifyingglass` | Filter | `line.3.horizontal.decrease` |
| Share / Export | `square.and.arrow.up` | Print | `printer` |
| Account / Profile | `person.crop.circle` | Like / Dislike | `hand.thumbsup` / `hand.thumbsdown` |
| Bring to Front | `square.3.layers.3d.top.filled` | Send to Back | `square.3.layers.3d.bottom.filled` |

Text formatting uses `bold`, `italic`, `underline`, `textformat.superscript`, `textformat.subscript`, `text.alignleft`, `text.aligncenter`, `text.justify`, `text.alignright`.

### macOS Document Icons
- Without a custom document icon, macOS composites your app icon plus the file extension onto the folded-corner page
- A custom one combines any of: background fill, center image, text; the system layers, masks, and adds the folded corner
- Keep designs simple — they render as small as 16×16 px; drop fine detail (grid lines, etc.) in the smallest sizes
- Keep important content out of the top-right corner of the fill (the fold covers it)
- Background fill sizes (@1x / @2x px): 512/1024, 256/512, 128/256, 32/64, 16/32
- Center image is half the canvas (e.g. 16×16 px for a 32×32 icon); sizes: 256/512, 128/256, 32/64, 16/32. Keep ~10% margin so the image fills ~80% (≈205×205 px in a 256 canvas)
- Text defaults to the extension, auto-scaled and uppercased; supply a short descriptive term if the extension is obscure (e.g. "scene" rather than "scn")

Source: [HIG — Icons](https://developer.apple.com/design/human-interface-guidelines/icons)
