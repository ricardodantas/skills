# HIG Foundations

## Design Principles

Apple reintroduced eight design principles in the HIG on June 8, 2026 (WWDC26 session "Principles of great design"). Use them to judge trade-offs when no specific guideline applies:

1. **Purpose** — Design with intention; serve people's real needs.
2. **Agency** — Keep people in control and let them recover from mistakes.
3. **Responsibility** — Protect privacy and safety; act in people's best interests.
4. **Familiarity** — Build on what people already know: recognizable metaphors, consistent patterns.
5. **Flexibility** — Adapt to contexts, devices, abilities, and personal preferences.
6. **Simplicity** — Remove friction with clear language, strong hierarchy, and concise interfaces.
7. **Craft** — Sweat the details; iterate on quality.
8. **Delight** — Choose the emotions you want to evoke and reinforce them throughout.

Source: [HIG — Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines), [WWDC26 — Principles of great design](https://developer.apple.com/videos/play/wwdc2026/250)

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
- Test at all Dynamic Type sizes including accessibility sizes (Body reaches 53 pt at AX5)
- Prefer **bold weight for emphasis** over color alone
- Line spacing: use system defaults; don't compress leading

Source: [HIG — Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

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
- Minimum contrast ratio: **4.5:1** for body text, **3:1** for 18 pt+ or bold text (WCAG AA)
- Don't rely on color alone to convey meaning — combine with icons, text, or shapes
- Test with color blindness simulators
- Provide both light and dark variants for any custom colors via Asset Catalog
- Use P3 wide color gamut for richer colors on supported displays

Source: [HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color)

## Dark Mode

- Respect the systemwide setting — don't add an app-only appearance switch; people may read it as your app being broken. Auto mode can flip appearance while your app is running
- Dark-only is acceptable only in rare cases, like immersive media viewing (e.g., Stocks)
- Dark palette colors aren't simple inversions of light ones; use semantic colors or asset-catalog Color Sets with light and dark variants — never hard-coded values
- Contrast: at least **4.5:1**; aim for **7:1** with custom foreground/background colors, especially small text
- Test with Increase Contrast and Reduce Transparency, separately and together — dark text on dark backgrounds can lose legibility
- Slightly darken content images with white backgrounds so they don't glow
- Prefer SF Symbols; design separate light/dark variants of custom icons when edges vanish (e.g., add an outline on dark)
- Use the system label colors (primary → quaternary) and system text views instead of drawing text yourself
- **iOS/iPadOS**: backgrounds come in *base* (dimmer) and *elevated* (brighter) sets; the system switches to elevated for foreground UI like sheets and popovers, so prefer system backgrounds over custom ones
- **macOS**: with the graphite accent, windows pick up desktop tinting; give custom components with a visible background slight transparency in neutral states only (not in colored states)
- Not supported in visionOS or watchOS

Source: [HIG — Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

## Layout

### Key Measurements
- **Safe area insets**: Always respect. Content must not extend under notch, home indicator, or status bar
- **Margins**: use system layout margins and the readable-content guide; don't hard-code values
- **tvOS safe area**: inset primary content 60 pt top/bottom, 80 pt left/right
- **visionOS**: keep button centers at least 60 pt apart
- **Bar heights** vary by device, Dynamic Type, and Liquid Glass; read safe-area insets at runtime, never hard-code them

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

Source: [HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

## Icons

### App Icons
- See `icon-design.md` for full details
- iOS 26+: Multi-layer Liquid Glass icons via Icon Composer; the 27 OSes render them with a sharper material (Icon Composer 2 previews both design generations)
- Single 1024×1024 design; system generates all sizes
- Support Default, Dark, and Mono annotations; people can pick default, dark, clear, or tinted, and the system generates any variant you don't provide
- No transparency in final icon (system applies shape mask)

### SF Symbols
- See `sf-symbols.md` for full details
- SF Symbols 8: 7,000+ symbols, 9 weights, 3 scales
- Use `Image(systemName:)` in SwiftUI
- Preferred over custom icons for system concepts

Source: [HIG — App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons), [HIG — SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols), [SF Symbols](https://developer.apple.com/sf-symbols/)

## Accessibility

### Required Support
1. **VoiceOver** — All interactive elements must have accessibility labels (more in [hig-technologies.md](hig-technologies.md#voiceover))
2. **Dynamic Type** — All text must scale with user's preferred size
3. **Reduce Motion** — Provide alternatives to animations
4. **Reduce Transparency** — Liquid Glass auto-adapts; verify legibility. In 27, a Settings slider (ultra-clear to fully tinted) replaces the 26.1 Tinted toggle; standard glass follows it automatically and there's no API to read its value, so test both extremes
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
- Touch targets: **44×44 pt** default on iOS (28×28 pt minimum; see the per-platform table below)
- Never disable user interaction for accessibility-critical controls
- Support Smart Invert (avoid bitmap-inverted images with `.accessibilityIgnoresInvertColors`)

### Color Accessibility
- Don't use color as the sole indicator (add icons/text)
- Contrast ratio ≥ 4.5:1 for text up to 17 pt; ≥ 3:1 for 18 pt and larger, or any bold text
- Test with Accessibility Inspector and color blindness filters

### Per-Platform Sizes
| Platform | Default / min control size | Default / min text size |
|----------|----------------------------|-------------------------|
| iOS, iPadOS | 44×44 / 28×28 pt | 17 / 11 pt |
| macOS | 28×28 / 20×20 pt | 13 / 10 pt |
| tvOS | 66×66 / 56×56 pt | 29 / 23 pt |
| visionOS | 60×60 / 28×28 pt | 17 / 12 pt |
| watchOS | 44×44 / 28×28 pt | 16 / 12 pt |

- Spacing: about **12 pt** of padding around bezeled elements, about **24 pt** around the visible edges of unbezeled ones
- Let people enlarge text by at least **200%** (**140%** on watchOS)

### Motion, Flashing, Gestures
- With Reduce Motion: slow and soften animation (especially in the periphery), swap x/y/z transitions for fades, don't animate depth changes or into/out of blurs
- Respect Dim Flashing Lights in video playback and let people opt out of flashing
- Caption video and audio-only content, including game cutscenes
- Use the simplest gesture for frequent actions (no custom multi-finger or multi-hand gestures) and always offer an onscreen alternative — e.g., a button beside swipe-to-dismiss

Source: [HIG — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Motion

System components already animate (Liquid Glass reacts more strongly to touch than to a trackpad). For custom motion:
- Add motion only when it serves the experience; gratuitous animation distracts and can cause discomfort
- Never make motion the only carrier of important information — pair it with haptics or audio, and honor Reduce Motion
- Feedback motion should follow the gesture's physics (a view pulled down from the top dismisses upward, not sideways)
- Keep feedback animations brief and precise; skip custom motion on frequent interactions
- Let people cancel or interrupt animations instead of waiting for them
- Consider animated SF Symbols (SF Symbols 5+) before building custom animations
- Games: target a steady **30–60 fps** by default on each platform; offer performance/battery options
- **visionOS**: avoid motion in peripheral vision; make large moving objects more translucent or lower-contrast; fade out/in to relocate objects; don't rotate the virtual world; give a stationary frame of reference; avoid sustained oscillation, especially near **0.2 Hz**

Source: [HIG — Motion](https://developer.apple.com/design/human-interface-guidelines/motion)

## Writing

- Define a voice (keep a list of common terms) and vary tone with context — direct for a fall alert, celebratory for a streak
- Be clear and brief; plain language, no jargon or gendered terms; write with localization and VoiceOver in mind
- Put the most important information first; split multiple ideas across screens
- Label buttons with verbs ("Send", not "Let's do it!"); avoid "Click here" for links
- Pick a capitalization style per element type (title case vs. sentence case) and apply it everywhere
- Multi-step flows: start with "Get Started", use one of "Continue"/"Next" consistently, end with "Done"
- Use possessives sparingly ("Favorites", not "Your Favorites"); avoid "we" — "Unable to load content" beats "We're having trouble…"
- Match gesture vocabulary to the device (tap on touch devices, not click); be brief on small screens and on TV, which is shared and read from a distance
- Empty states: explain the next step and offer a button for it; don't put crucial info there
- Errors: show them next to the problem, don't blame, say how to fix it ("Choose a password with at least 8 characters"), skip "oops"
- Settings: describe what the "on" state does; link directly to a setting rather than describing its location
- Text fields: label every field and use placeholder hints for format ("name@example.com")

Source: [HIG — Writing](https://developer.apple.com/design/human-interface-guidelines/writing)

## Right to Left

System frameworks flip standard components automatically for Arabic, Hebrew, and other RTL languages. When fine-tuning:
- Mirror text alignment with the layout; but align a paragraph (3+ lines) by *its own* language, and keep all items in a list aligned the same way
- Never reverse the digits within a number (phone, card, "541"); do reverse the order of numerals along progress bars, sliders, and ratings
- Arabic may use Western or Eastern Arabic numerals depending on region; number-centric apps should pick per locale
- Flip controls showing progress or fixed order (sliders, back/next buttons — back points right in RTL), including their end-cap glyphs
- Keep controls that indicate a real direction ("to the right") unflipped
- Next to all-caps Latin text, Arabic/Hebrew often needs about **2 pt** larger type to look balanced
- Don't flip photos, illustrations, logos, or universal marks (checkmark); reverse image *order* when sequence matters
- Flip icons that depict text or forward/backward motion; don't flip real-world objects (clocks, right-handed tools). SF Symbols ships RTL and localized variants; set directionality on custom symbols
- For complex icons, judge each component — keep negation slashes consistent, move badges if balance requires

Source: [HIG — Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left)

## Inclusion

- Address people as *you*; don't call them "the user" or "the player". (Writing guidance says to avoid *we*; if you use it, reserve it for your app or company)
- Define specialized terms, replace colloquialisms with plain language, and think twice before adding humor
- Avoid needless gender references; prefer customizable avatars/characters and non-gendered generic figures
- When gender is truly required, offer inclusive options (e.g., nonbinary, self-identify, decline to state) and let people set pronouns
- Show a range of people, places, and families; avoid stereotyped jobs, behaviors, or culture-specific experiences presented as universal
- Disability: support VoiceOver, Display Accommodations, captions, Switch Control, and Speak Screen; include people with disabilities in imagery; write people-first and never use a disability as a negative metaphor
- Prepare for localization: SF Symbols for glyphs, and check that color meanings hold in each culture

Source: [HIG — Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion)

## Privacy

- Request only the data you need, as narrowly as possible; process on device where you can; respect Hide My Email and Mail Privacy Protection
- Ask for permission at the moment a feature needs it — not at launch unless the app can't work without it
- Purpose strings: say concretely how you use the data; sentence case, active voice, ending period
- Optional pre-permission screen: a single button titled like "Continue" or "Next" that leads to the system alert — no cancel, close, or extra actions
- App Tracking Transparency: no misleading pre-alert, no incentives, no withholding features, no "Allow"-style buttons, no mock-ups of the system alert or visual cues toward its Allow button
- Location button: a one-time, lightweight way to share location; you can set its system title, filled/outlined glyph, colors, and corner radius — nothing else — and it must not truncate at any text size or language
- Authentication: prefer passkeys, Sign in with Apple, or Password AutoFill; add two-factor if you keep passwords; use Face ID/Touch ID/Optic ID for kept-signed-in apps; store secrets in the keychain; never roll your own scheme
- **macOS**: sign with Developer ID outside the store, use the app sandbox, don't assume who's signed in
- **visionOS**: ARKit data needs a Full Space plus permission (plane estimation, scene reconstruction, image anchoring, hand tracking); replace iPad camera features with content import

Source: [HIG — Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)
