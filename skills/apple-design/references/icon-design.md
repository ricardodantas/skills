# App Icon Design

## Overview

Starting with iOS 26, app icons use a **multi-layer Liquid Glass format** created with Apple's **Icon Composer** tool. Icons feature translucency, glass-like shimmer, and react to device movement.

## Icon Composer

Icon Composer is Apple's tool for creating layered Liquid Glass icons.

### Key Features
- **Multi-platform from single design** — One design adapts to iPhone, iPad, Mac, Apple Watch
- **Liquid Glass properties** — Adjust specular highlights, blur, translucency, shadows
- **Three appearance modes** — Default, Dark, Mono (tinted)
- **Real-time preview** — See dynamic lighting, different backgrounds, various sizes
- **Xcode integration** — New icon file type syncs directly to project
- **Export** — Flattened version available for marketing materials

### Download
- Requires macOS Sequoia 15.3 or later
- Download from developer.apple.com/download

## Multi-Layer Icon Format

### Layer Structure
Icons consist of multiple layers that create depth with Liquid Glass:
1. **Background layer** — Base color/gradient
2. **Middle layers** — Design elements, patterns
3. **Foreground layer** — Primary symbol/glyph

### Liquid Glass Properties Per Layer
- **Specular highlights** — Light reflection intensity
- **Blur** — Frosted glass effect amount
- **Translucency** — How much background shows through
- **Shadows** — Depth and dimension

## Appearance Modes

| Mode | Description | Context |
|------|-------------|---------|
| **Default** | Full color, standard appearance | Light mode, default wallpapers |
| **Dark** | Adapted for dark backgrounds | Dark mode |
| **Mono** | Single-color tinted | Tinted home screen mode |
| **Clear** | Transparent Liquid Glass | New transparent mode (iOS 26) |

## Icon Design Guidelines

### Shape & Grid
- **Rounder enclosure shapes** in iOS 26 (updated from iOS 18 superellipse)
- Updated grid system for cross-platform consistency
- System applies the shape mask — **don't include rounded corners** in your artwork
- Single design scales across platforms by default; customize per-platform if needed

### Sizes
- Design at **1024×1024 px** — system generates all required sizes
- Key rendered sizes: 180×180 (@3x iPhone), 152×152 (@2x iPad), 512×512 (Mac), etc.
- App Store: 1024×1024

### Design Principles
1. **Simplicity** — Single, recognizable element; avoid clutter
2. **Recognizability** — Identifiable at all sizes (including 40×40 pt on Apple Watch)
3. **Consistency** — Match your app's visual identity and color palette
4. **No text** — Text doesn't scale well; use symbol/glyph instead
5. **No photos** — Photos lose detail at small sizes; use simplified graphics
6. **Unique silhouette** — Distinguishable from other icons even as a shape

### Color
- Use a limited, distinctive color palette
- Ensure sufficient contrast with any wallpaper
- Gradients work well with Liquid Glass depth effect
- Test against light and dark wallpapers

### Layer Design Tips
- Keep the foreground glyph centered and sized within the safe zone (~70% of canvas)
- Background layers can extend to edges (system crops with mask)
- Use subtle differences between layers for natural depth
- Avoid overly complex layers — Liquid Glass refraction amplifies complexity
- Test with dynamic lighting to ensure layers look good in motion

## Workflow

1. **Design** artwork layers in your vector tool (Figma, Sketch, Illustrator)
2. **Import** layers into Icon Composer
3. **Adjust** Liquid Glass properties (specular, blur, translucency, shadow)
4. **Preview** across sizes, backgrounds, appearance modes, and lighting
5. **Annotate** Dark and Mono variants (within same file)
6. **Add to Xcode** — Icon Composer file integrates directly
7. **Export** flattened version for marketing/App Store if needed

## Common Mistakes
- ❌ Flat single-layer icons (look outdated on iOS 26)
- ❌ Including rounded corners in artwork (system applies mask)
- ❌ Text in icons (illegible at small sizes)
- ❌ Too much detail (Liquid Glass refraction makes it noisy)
- ❌ Not testing Dark/Mono modes (icon may be invisible)
- ❌ Not testing at small sizes (40pt Apple Watch, 29pt Settings)
- ❌ Using raster images without providing 1024px source
