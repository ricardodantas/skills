# Platform-Specific Design

## Device Sizes & Previewing

Apple no longer publishes a per-device point-size table: the HIG Layout page dropped its device specifications in its September 9, 2026 update, and no other developer.apple.com or apple.com page lists point sizes for the current lineup (iPhone 17 family, iPhone Air, iPhone Duo, 42/46 mm Apple Watch). apple.com tech specs give pixels, not points.

- **Don't hard-code device sizes.** Lay out with size classes, safe areas, layout margins, and layout guides; the same app may run at many sizes (iPad resizing, iPhone Mirroring on Mac, iPhone Duo poses)
- **Preview in Xcode's Device Hub** — run on simulated devices (including iPhone Duo poses) to catch clipping; test the largest and smallest layouts first, plus other localizations and text sizes
- The size tables below are **partial and legacy** (older models only, kept as rough reference) — not the current lineup

Source: [HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

## iOS (iPhone)

### Device Traits
- **Display** — medium-size, high resolution
- **Ergonomics** — held in one or both hands, rotated freely; viewing distance a foot or two at most
- **Inputs** — Multi-Touch gestures, virtual keyboard, voice; apps often use personal data, gyroscope/accelerometer, and spatial interactions
- **Sessions** — from a minute-long check-in to hours of browsing, games, or media; people switch apps constantly
- **System features** — widgets, Home Screen quick actions, Spotlight, Shortcuts, activity views

### Key Characteristics
- **Single-column layout** in portrait (compact width)
- **Tab bar** navigation at bottom (max 5 visible tabs)
- **Edge-to-edge** content with safe area insets
- **Touch-first** — 44×44 pt default tap targets (28×28 pt minimum)
- **Gestures**: Swipe back, pull-to-refresh, swipe actions on rows

### Best Practices
- Keep onscreen controls few; make secondary details and actions discoverable with minimal effort
- Adapt to orientation, Dark Mode, and Dynamic Type changes
- Put frequent controls in the middle or bottom of the display (easiest to reach); support swipe-to-go-back and row swipe actions
- With permission, use platform data instead of asking people to type it — Apple Pay, biometric authentication, location

### iOS 26 Specifics (Liquid Glass baseline)
- Liquid Glass tab bars, toolbars, navigation bars
- Tab bar minimizes on scroll (`.tabBarMinimizeBehavior(.onScrollDown)`)
- Floating search button with `Tab(..., role: .search)`
- Dynamic wallpapers influence Liquid Glass appearance
- Layered app icons with motion parallax
- Edge-to-edge Safari

### iOS 27 Specifics (current)
- Refined Liquid Glass: more uniform refraction, improved contrast
- Settings slider from ultra-clear to fully tinted replaces the 26.1 Tinted toggle; standard glass adapts automatically (no public API to read the value)
- `UIDesignRequiresCompatibility` is ignored when building with the 27 SDK — the Liquid Glass opt-out is gone
- Toolbars: `toolbarMinimizationBehavior(_:for:)`, `ToolbarContent.visibilityPriority(_:)`, `ToolbarOverflowMenu`, `ToolbarItemPlacement.topBarPinnedTrailing`
- Tabs/navigation: `TabRole.prominent`, `NavigationTransition.crossFade`

### Widgets & Live Activities (27)
- New `systemExtraLargePortrait` widget family (iOS, iPadOS, macOS 27)
- Live Activities can appear in the landscape Dynamic Island; adapt with `isDynamicIslandLimitedInWidth`
- Full widget and Live Activity guidance: [hig-system-experiences.md](hig-system-experiences.md#widgets)

## iPhone Duo (iOS 27.1+)

Two displays joined by a center hinge: a compact-width outer display (closed) and a regular-width inner display (open). Still iPhone — iOS patterns apply. Standard components plus a resizable layout adapt to its poses with little extra work.

### Anatomy & Poses
- **Outer display** (closed): bars sit on the side to save vertical space; they stay on the side when the device opens in landscape
- **Cameras** — the outer front camera sits in a corner, always visible, aligned with the side controls; the inner camera hides behind the display until active
- **Poses** — half-folded like a book, flat on a surface, standing on an edge. Don't design per pose: a compact-width layout (outer) and a regular-width layout (inner) cover them all; let the layout expand instead of reinventing it
- Preview every pose in Xcode's Device Hub

### Best Practices
- **Build to resize** — size classes, layout margins, safe areas; no fixed widths or per-display layouts. Split View multitasking also runs on the inner display
- **Consistent across displays** — same functionality and element state on both; optionally show one extra hierarchy level on the inner display (Mail: list *or* message when closed, both side by side when open)
- **Same functionality in every pose** — controls may overflow and content may move, but everything stays reachable
- **Games** — playable in every pose; you may lock orientation but must fill the screen. Keep text/control sizes stable; prefer changing aspect ratio over letterboxing/pillarboxing, and fill unavoidable bars with artwork

### Reserved Regions
- **Outer camera** (always) — expands into the Dynamic Island for Live Activities; side controls account for it automatically
- **Inner camera** (only while active) — UI moves aside when it turns on
- **Fold region** (when partially open) — splits the inner display into usable regions and excludes the center
- Alerts, context menus, and sheets move off the fold automatically; split views rebalance column widths and margins to the inner display's symmetry. Use `ReservedRegion` (SwiftUI) / `UIView.ReservedRegion` (UIKit) for custom content
- Prefer self-adapting containers (e.g. Notes' split view equalizes panes when folded); prefer even column counts in grids
- **Avoid extreme reflow when folding** — move only what must move; small adjustments beat rearrangement

### Split & Arrangement Views
- **Split views** expand on the inner display and collapse to one pane on the outer display, like regular ↔ compact on other iPhones
- **`ArrangementView`** (SwiftUI) / `UIArrangementViewController` (UIKit) holds a primary and a secondary view:
  - *Split* — divides the area; side by side when wider than tall, stacked when taller than wide (axes can be restricted)
  - *Overlay* — primary sits over the secondary; when partially folded, each takes a side (secondary can be collapsed)
- A layout that's already an `HStack`/`VStack` maps to split; a `ZStack` maps to overlay
- Keep navigation containers (split views, tab views) *outside* the arrangement view

### Vertical Controls
Toolbars, tab bars, status bar, and Dynamic Island move to the side — except on the inner display in portrait, which keeps horizontal bars.
- In Split View on the inner display, each app puts controls on its outer edge. Side controls stay aligned with the hardware (same side in right-to-left languages)
- **Account for asymmetry** — use safe areas so controls (yours or the neighbor app's) never cover content
- **Keep relative positions stable across poses** so people don't relearn where actions are
- **Order** — Back/Close at the top of the vertical axis, then prominent actions like Done; keep other items in their original groups (the system separates former top- and bottom-bar items)
- **Overflow** runs bottom-to-top by default; set visibility priority on groups first, then items (`ToolbarItemVisibilityPriority` / `UIBarButtonItemVisibilityPriority`). Keep frequent actions (Compose, New Note) and badged/status items visible longest
- **Don't override the default bar placement**
- **Full-width layouts** suit non-scrolling, immersive UIs (Calculator) if nothing collides with the Dynamic Island or status bar; a full-width header/background with inset scrolling content also works
- **Group, don't space** — `ToolbarItemGroup` / `UIBarButtonItemGroup` add adaptive spacing; no fixed spacers
- **Keep controls next to the content they affect** — e.g. Mail's list controls stay above the leading pane
- **Title + symbol on every non-text item** (`Label` / `UIBarButtonItem`) — the title feeds overflow menus and expanded forms. Minimize text-only buttons: text labels stay in a horizontal bar
- **Compression** — `ToolbarVerticalCompressionBehavior` / `UIVerticalBarCompressionBehavior`: navigation-focused views keep the tab bar and overflow toolbar items (default, `.prefersTabBar`); task-focused views minimize the tab bar to keep the toolbar (`.prefersToolbarItems` / `.prefersBarItems`)
- **Use the system overflow menu** (`ToolbarOverflowMenu` / `additionalOverflowItems`) instead of your own; reserve the ellipsis symbol for overflow

Source: [HIG — Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo)

## iPadOS

### Device Traits
- **Display** — large, high resolution
- **Ergonomics** — handheld, on a surface, or on a stand; usually within about 3 feet
- **Inputs** — Multi-Touch, virtual or attached keyboard, pointing device, Apple Pencil, voice — often combined
- **Sessions** — quick actions to hours of games, media, creation, or productivity; several apps onscreen at once, plus drag and drop between them
- **System features** — multitasking, widgets, drag and drop

### Key Characteristics
- **Multi-column** layouts (NavigationSplitView)
- **Sidebar** navigation (primary pattern)
- **Multitasking** — Split View, Slide Over, Stage Manager
- **Pointer/keyboard** support essential
- **Regular width** size class in most orientations

### Best Practices
- Use the large display to elevate content: fewer modal views and full-screen transitions; controls easy to reach but out of the way
- Let viewing distance and input mode drive the size and density of content
- Support touch, keyboard/trackpad, and Pencil — and interactions that combine them
- Adapt to orientation, multitasking modes, Dark Mode, and Dynamic Type, and run well on macOS

### iPad-Specific Patterns
- Popovers instead of action sheets
- Drag and drop between apps
- Keyboard shortcuts (`.keyboardShortcut()`)
- Pencil support where relevant
- `.navigationSplitViewColumnWidth()` for sidebar sizing

### iPadOS 27
- Tab bar expands into a full sidebar — design tabs so they read well in both forms
- Optional always-visible menu bar; app name shown in the status bar — keep menu bar commands complete
- iPhone apps are resizable on iPad — support size-class changes instead of fixed iPhone dimensions
- Menu item images are hidden by default in the menu bar

Source: [HIG — Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados)

## macOS

### Device Traits
- **Display** — large, high resolution; workspace often extended with extra displays, including an iPad
- **Ergonomics** — stationary on a desk; roughly 1–3 feet away
- **Inputs** — physical keyboard, pointing devices, game controllers, Siri, in any combination
- **Sessions** — minutes to hours of deep focus, with many apps open and frequent active/inactive switching
- **System features** — menu bar, file management, full screen, Dock menus

### Key Characteristics
- **Menu bar** with full menu hierarchy — required for Mac apps
- **Window management** — Resize, minimize, full screen, multiple windows
- **Keyboard-first** with comprehensive shortcuts
- **Right-click** context menus everywhere
- **Smaller hit targets** — Pointer precision allows smaller controls
- **Toolbar** at window top (not bottom)

### Best Practices
- Show more content in fewer nested levels with less modality, without cramming density
- Let people resize, hide, show, and move windows; support full-screen mode
- Expose every command in the menu bar; support keyboard shortcuts and keyboard-only work
- Enable pixel-precise selection and editing with high-precision input
- Allow personalization: customizable toolbars, window configuration, colors, fonts
- Layout: keep controls and critical info away from the window's bottom edge (windows often hang off-screen); keep content out from behind the camera housing (`NSPrefersDisplaySafeAreaCompatibilityMode`)

### macOS 27 "Golden Gate" Specifics
- Apple silicon Macs only
- Uniform top toolbar, edge-to-edge sidebars, colored sidebar icons
- Updated window shapes and menu bar icons
- Menu item images hidden by default in the menu bar; override with `NSMenuItem.preferredImageVisibility`
- AppKit: `tabs` role for `NSSegmentedControl`, `NSToolbarItemGroup.role`, `NSRefreshController`; titlebar accessories can draw glass outside their bounds
- SwiftUI bordered `Menu`/`Picker` no longer use `NSPopUpButton`
- History: macOS Tahoe (26) brought Liquid Glass to the Mac (transparent menu bar, floating glass sidebar)

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

Source: [HIG — Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos)

## watchOS

### Device Traits
- **Display** — small, high resolution, readable on the wrist
- **Ergonomics** — about a foot away on wrist raise, operated with the other hand; Always On shows the face when the wrist drops
- **Inputs** — Digital Crown (vertical navigation, data inspection), tap/swipe/drag even in motion, Action button (eyes-free essential action), shortcuts; sensor data such as GPS, blood oxygen, heart, altimeter, accelerometer, gyroscope
- **Sessions** — many glances a day, interactions under a minute; complications, notifications, and Siri often get more use than the app itself
- **System features** — complications, notifications, Always On, watch faces

### Key Characteristics
- **Glanceable** — Information in 2-3 seconds
- **Brief interactions** — Most sessions < 10 seconds
- **Single-column** vertical scroll
- **Digital Crown** for scrolling and input
- **Complications** for at-a-glance data on watch face
- **Small screen** — case sizes vary across the lineup; preview in Device Hub rather than hard-coding (see [Device Sizes & Previewing](#device-sizes--previewing))

### Design Principles
- Quick, glanceable, single-screen interactions — critical info plus one or two gestures
- Shallow navigation hierarchy; use the Digital Crown for vertical scrolling and moving between screens
- Anticipate needs with on-device data; surface what's relevant now or very soon
- Use background color for supporting information and materials for hierarchy and sense of place
- Work independently of iPhone, adding detail beyond notifications and complications
- Minimal text, large fonts
- Dark backgrounds (OLED power saving)
- System navigation (page-based or hierarchical)
- Use `.navigationBarTitleDisplayMode(.large)` for readability
- Haptic feedback for interactions
- Layout: at most three glyph buttons or two text buttons side by side (two short text buttons only on a non-scrolling screen); otherwise let text buttons span the full width
- Support autorotation for views people show to others (an image, a QR code)

### watchOS 26 Specifics
- Location-aware widgets in Smart Stack
- Fluid Control Center navigation
- Liquid Glass UI kit

### watchOS 27
- Dynamic app grid, one-handed tap gesture for the Smart Stack
- New suggestion widgets, Siri Modular face
- Higher-contrast glass; no new UI APIs

### Complications / Widgets
See [hig-system-experiences.md](hig-system-experiences.md#complications) for sizes and rules; Digital Crown input is in [hig-inputs.md](hig-inputs.md#digital-crown).
- Complications show relevant, possibly dynamic data on every wrist raise and deep-link into the app on tap
- Notifications deliver timely, high-value info with actions, no app launch needed
- Provide WidgetKit timeline entries
- Support multiple widget families: `.accessoryCircular`, `.accessoryRectangular`, `.accessoryInline`, `.accessoryCorner`

Source: [HIG — Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos)

## tvOS

### Device Traits
- **Display** — very large, high resolution
- **Ergonomics** — viewers often 8 feet or more away, sometimes moving around the room
- **Inputs** — Siri Remote, game controllers, voice, and apps on other devices
- **Sessions** — hours-long immersion, often with picture in picture alongside
- **System features** — TV app integration, SharePlay, Top Shelf, TV provider accounts

### Key Characteristics
- **10-foot UI** — Large text, high contrast, designed for viewing distance
- **Focus-based** navigation (no touch, no pointer)
- **Siri Remote** — Swipe, click, Menu button
- **Parallax** effects on focused elements
- **Top shelf** — Showcase content on home screen

### Design Principles
- Content-forward: Full-bleed images, minimal chrome
- Default body text 29 pt (minimum 23 pt)
- Focus states: Clear visual indicator of focused element — let the focus system highlight and enlarge items
- Layered images for parallax effect
- Avoid dense text or complex forms
- Cinematic feel: edge-to-edge artwork, subtle fluid motion, engaging audio, legible across the room
- Multiuser: easy, infrequent sign-in, shared sign-in, automatic profile switching when the viewer changes

### Layout
- **Safe area** — inset primary content **60 pt** top/bottom and **80 pt** left/right (overscan and TV settings)
- Leave padding between focusable items — focused items grow and must not cover neighbors
- Grids (horizontal spacing **40 pt**, minimum vertical spacing **100 pt** for all):

| Columns | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---------|---|---|---|---|---|---|---|---|
| Unfocused content width (pt) | 860 | 560 | 410 | 320 | 260 | 217 | 184 | 160 |

- Add extra vertical space for titled rows; keep spacing consistent; make partially visible offscreen items equal width on both sides

### tvOS 26
- Liquid Glass design language
- Parallax with Liquid Glass materials

### tvOS 27
- System-wide Dynamic Type — test layouts at larger text sizes

Source: [HIG — Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos)

## visionOS (Apple Vision Pro)

### Key Characteristics
- **Spatial computing** — Windows float in 3D space; an unbounded canvas for windows, volumes, and 3D objects
- **Eye tracking + hand gestures** — look at an element, then an *indirect* gesture (tap) activates it; *direct* touch also works
- **Windows, Volumes, Immersive Spaces** — Three content types
- **Shared Space vs. Full Space** — apps launch in the Shared Space beside other apps; a Full Space runs your app alone (blend with surroundings, open a portal, or replace the world)
- **Passthrough** — live camera view of the room; people adjust how much with the Digital Crown
- **Glass material** background (original inspiration for Liquid Glass)
- **No fixed screen** — Adaptive layout; a visionOS *point* is an angle, not a pixel count

### Design Principles
- Windows: Standard 2D content in floating panels — prefer them for contained, UI-centric tasks
- Volumes: 3D objects viewable from all angles (a window without a visible frame)
- Immersive Spaces: Full environment replacement — pick the *minimum* immersion each moment needs
- **Interactive spacing** — look targets need room for the hover effect: place regular-size buttons with centers at least **60 pt** apart and **16 pt** or more between them; never overlap controls
- Use system glass material for window backgrounds
- Support resizing; min/max sizes are for preventing overlap or unwieldy layouts, not for blocking resize. Keep content horizontally centered at large sizes
- Use 3D inside windows sparingly and inset it; bigger 3D belongs in a volume or immersive space
- Put supplemental content in an adjacent window (`defaultWindowPlacement(_:)`), not in an ornament — ornaments are for app controls like toolbars and playback
- Avoid overwhelming with too many floating windows
- SharePlay shows participants as spatial Personas for shared activities

### Depth & Scale
- System depth cues (color temperature, reflections, shadow) are automatic; SwiftUI adds subtle depth to 2D windows
- Depth cues must be accurate — conflicting cues cause discomfort. Use depth for hierarchy (a sheet comes forward, the window recedes) and on large elements like tab bars/toolbars, not on small ones (a button's symbol)
- Don't add depth to text; limit the number of distinct depths (refocusing tires the eyes)
- **Dynamic scale** (default) keeps windows the same apparent size at any distance; **fixed scale** makes objects shrink with distance — use it sparingly for noninteractive, life-size objects

### visionOS 26
- Persistent spatial widgets
- Immersive photo experiences
- Liquid Glass refinements

### visionOS 27
- Siri orb
- Immersive environments created from panoramas and websites

### Ergonomics
- Keep important content centered in the field of view; the system positions content relative to the wearer's head (sitting, standing, or lying down)
- Anchor content in the room, not to the head — head-locked content feels confining
- Avoid requiring head turns, repositioning, or much physical movement; content comes to people, not the reverse
- Prefer indirect gestures (hands at rest); keep direct-touch targets close and interactions short
- Avoid fast, jarring motion or motion without a stationary frame of reference; nothing distracting or high-contrast in the periphery during immersion
- People recenter with the Digital Crown — no app work needed
- Place large floor-based immersive content on a horizontal plane aligned to the floor

### Immersion
- Styles: **mixed** (content blended with passthrough; no boundary — nearby content turns semi-opaque near physical objects), **progressive** (environment partially replaces passthrough; Digital Crown range defaults to 120–360°), **full** (360° environment replaces passthrough)
- Progressive and full set a boundary about **1.5 m** from the starting head position — visuals fade past it. If people may need to move farther, use mixed
- Prefer launching in the Shared Space or mixed style; reserve deeper immersion for meaningful moments. Keep passthrough tints subtle
- Environments: expansive, low-distraction, gentle animation, always a ground plane; avoid a flat 360° image (no sense of scale)
- Let people choose when to enter and exit; provide an obvious in-app exit and say whether it returns or quits (offer pause/save if it quits). Don't force people to use system controls to reduce immersion
- Make transitions smooth and trackable; avoid sudden changes
- In mixed immersion don't obscure too much passthrough; in progressive/full, don't encourage walking around
- Spatial Audio soundscapes: avoid obvious loops; duck or stop when people play other audio

Source: [HIG — Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos) · [HIG — Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) · [HIG — Immersive experiences](https://developer.apple.com/design/human-interface-guidelines/immersive-experiences)

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

### Adapting to Size
- **Decide layout by size class, never by device type or orientation** — size classes report the space actually available
- Consider every size-class combination in both aspect ratios (iPad windows, iPhone Mirroring, iPhone Duo)
- Keep functionality identical as size changes; you may show more of it (e.g. tab bar → sidebar, expose items from an overflow menu), and keep the layout recognizable for the platform
- Respect safe areas and layout guides; support Dynamic Type by letting rows grow and side-by-side views stack
- Scale background art to fill new aspect ratios instead of distorting it

### Universal Design (iOS 26+, 27 SDK)
- Liquid Glass (introduced in 26, refined in 27) provides visual consistency across all platforms
- Build with Xcode 27: the compatibility opt-out is ignored, and from April 2027 iOS, iPadOS, tvOS, visionOS, and watchOS uploads require the 27 SDKs
- Each platform maintains its own interaction paradigms
- Single SwiftUI codebase can adapt via size classes and platform checks
- App icons: One design in Icon Composer, auto-adapts per platform
- SF Symbols work identically across all platforms

Source: [HIG — Layout](https://developer.apple.com/design/human-interface-guidelines/layout)
