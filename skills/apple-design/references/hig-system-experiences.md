# HIG System Experiences

Surfaces where your app shows up outside its own windows: widgets, Live Activities, Controls, notifications, App Shortcuts, watch complications and faces, the status bar, and tvOS Top Shelf. For Siri/Spotlight snippets see [Snippets](hig-patterns.md#snippets); for what changed in the 27 releases see [platform-specific.md](platform-specific.md).

## Widgets

Glanceable, periodically refreshed content plus light interaction, built with WidgetKit + SwiftUI. Not supported in tvOS.

**Families and where they appear**
| Family | iPhone | iPad | Mac | Vision Pro | Watch |
|--------|--------|------|-----|------------|-------|
| `systemSmall` | Home Screen, Today, StandBy, CarPlay | Home, Today, Lock Screen | Desktop, Notification Center | Surfaces | — |
| `systemMedium` / `systemLarge` | Home, Today | Home, Today | Desktop, NC | Surfaces | — |
| `systemExtraLarge` | — | Home, Today | Desktop, NC | Surfaces | — |
| `systemExtraLargePortrait` | See note | See note | See note | Surfaces | — |
| `accessoryCircular` / `accessoryRectangular` | Lock Screen | Lock Screen | — | — | Complications, Smart Stack |
| `accessoryInline` | Lock Screen | Lock Screen | — | — | Complications |
| `accessoryCorner` | — | — | — | — | Complications |

Note: the HIG table (last revised Dec 2025) lists extra large portrait for visionOS only; the 27 SDK adds it on iOS, iPadOS, and macOS — see [platform-specific.md](platform-specific.md).

**Rendering modes** (`WidgetRenderingMode`)
- **Full color** — your colors untouched (Home Screen light/dark, Mac desktop, Vision Pro default)
- **Accented** — system strips the background (tint or Liquid Glass for the clear look) and paints two groups: primary and accent. Mark accent views with `widgetAccentable(_:)`. On Watch, accent takes the watch face color; elsewhere both groups go white
- **Vibrant** — iPhone/iPad Lock Screen, StandBy in low light, and the Mac desktop: desaturated, colored for the background. Render at full opacity; use white/light gray for primary content and darker grays for secondary — opaque grays, not white-with-opacity
- Home Screen appearances are light, dark, clear, and tinted — never rely on color alone for meaning; limit full-color images (album art) and keep them smaller than the widget

**Content and layout**
- One focused idea tied to the app's core purpose; dynamic content that changes during the day. Don't just replicate the app icon
- Offer more sizes only when each adds value — don't stretch small content to fill a large widget
- Standard margin **16 pt**; tighter **11 pt** works for grouped graphics/buttons. Mac desktop and Lock Screen/StandBy use smaller margins. Use `ContainerRelativeShape` for concentric corners
- System font, text styles, SF Symbols; text **≥ 11 pt**; never rasterize text
- Brand lightly; if a logo is needed (multi-source content), a small one top-right is enough
- Don't mimic your widget inside the app; tell signed-out users what signing in unlocks

**Updates and interactivity**
- No real-time updates — the system budgets refreshes. Let the system render dates/timers; if people check more often than you can refresh, show "last updated"
- Animate data changes with transitions up to **2 s**
- Tapping outside controls opens the app — deep-link to the exact content
- Buttons/toggles only for simple, related actions; avoid app-like layouts. Inline accessory widgets get one tap target
- Need live progress? Use a Live Activity instead

**Gallery**
- Realistic preview (simulated data if real data is slow); placeholder = static UI + semi-opaque shapes for text/images
- Description starts with a verb ("See the current forecast…"); never "This widget shows…"
- Group all sizes under one description; you may tint the Add button with a brand color

**Platform notes**
- **iOS/iPadOS Lock Screen:** follows complication principles — design both together. Always-On lowers luminance; check gray contrast
- **StandBy/CarPlay:** two small widgets side by side, background removed, scaled up. No background color, bigger text, fewer rich images; night mode tints red
- **visionOS:** 3D objects pinned to surfaces, persisting across restarts; people scale them **75–125%**. Design two proximity levels (`simplified` far = bigger type, no controls; `default` near = more detail). Mounting: elevated (default, any surface) or recessed (vertical only). Treatment: `paper` (reacts to room light) or `glass` (foreground stays bright — for dense info). Test every tint palette and each elevated frame width
- **watchOS Smart Stack:** default black background — use a meaningful color instead (e.g. red/green for stock moves); supply relevance (RelevanceKit) so the system surfaces it

**Key sizes (pt)**
| Context | Small | Medium | Large | Extra large |
|---------|-------|--------|-------|-------------|
| iPhone 430×932 | 170×170 | 364×170 | 364×382 | — |
| iPhone 393×852 | 158×158 | 338×158 | 338×354 | — |
| iPad 1024×1366 (device) | 160×160 | 356×160 | 356×356 | 748×356 |
| visionOS | 158×158 | 338×158 | 338×354 | 450×338 (portrait 338×450) |

- iPhone accessory on 430×932: circular 76×76, rectangular 172×76, inline 257×26
- watchOS Smart Stack widget: 40 mm 152×69.5 · 41 mm 165×72.5 · 44 mm 173×76.5 · 45 mm 184×80.5 · 49 mm 191×81.5. Full per-device tables on the HIG page

Source: [HIG — Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets)

## Live Activities

Track a task or event with a clear start and end — ideally **≤ 8 hours** — in the Dynamic Island, Lock Screen, StandBy, Mac menu bar, Watch Smart Stack, and CarPlay Dashboard. Built with ActivityKit + WidgetKit. Not supported in tvOS or visionOS.

**Presentations you must design**
- **Compact** — leading + trailing views either side of the TrueDepth camera when one activity runs. Read as one unit; keep narrow, snug to the camera, no padding, balanced widths (shorten units). Both halves deep-link to the same screen
- **Minimal** — when several run; one attached, one detached (circle or oval). Show live data (a countdown), not just a logo
- **Expanded** — touch and hold; an enlarged compact layout, wrapped tightly around the camera
- **Lock Screen** — banner at the bottom; also the alert banner on devices without Dynamic Island. Don't copy notification layout. Standard margin **14 pt**
- **StandBy** — minimal, then Lock Screen presentation scaled **2×**; prefer the default background, keep margins, check the red Night Mode tint

**Rules**
- Show only what matters at a glance; tap opens the app at the right place
- No ads or promotions; hide sensitive data (innocuous summary or redaction)
- Match app personality in light and dark; logo mark without a container, never the full app icon
- Dynamic Island background is always black opaque — use bold colors; tint the key line to match. Custom background color allowed only on the Lock Screen presentation (check Always-On contrast; verify the generated dismiss button color, `activitySystemActionForegroundColor(_:)`)
- Large, medium-or-heavier text; concentric margins (`ContainerRelativeShape`); separate blocks with an inset shape or thick line, never edge-to-edge
- Grow and shrink height on Lock Screen/expanded as content changes
- Animations **≤ 2 s**; animate elements to new positions instead of removing/re-adding; none run on reduced-luminance Always-On
- At most one interactive element, for pause/resume-style actions (playback, workout, recording)
- Start when expected (order placed, match begins); let people stop it from the matching app view; offer an App Shortcut to start it (e.g. from the Action button)
- Update only on real changes; alert only for essential updates, and never duplicate them as push notifications. Prefer one rotating activity over several parallel ones
- End immediately when done. Dynamic Island and CarPlay drop it at once; Lock Screen, Mac menu bar, and Smart Stack keep it up to **4 hours** — set a custom dismissal, usually **15–30 min**

**Other contexts**
- **CarPlay** — compact halves merged into one layout; controls are disabled. Declare `ActivityFamily.small` for a custom layout. Sizes 240×78, 240×100, 170×78 pt
- **watchOS** — top of the Smart Stack; default merges compact halves. A custom layout can add a button/toggle, but it's also used in CarPlay (where controls don't work)
- **macOS** — shows in the menu bar of a paired Mac; clicking opens iPhone Mirroring

**Sizes (pt)**
- iPhone 430×932: compact 62.33×36.67 each side; minimal 36.67–45 × 36.67; expanded and Lock Screen 408 × 84–160. iPhone 393×852: compact 52.33×36.67; expanded/Lock Screen 371 × 84–160
- Dynamic Island corner radius **44 pt**; compact/minimal width 230 (Pro, standard) or 250 (Pro Max, Plus, Air); expanded 371 or 408
- iPad Lock Screen: 500 × 84–160 on 1366×1024, 425 × 84–160 on smaller iPads; Watch uses the Smart Stack widget sizes

27: Live Activities can appear in the landscape Dynamic Island — adapt with
`isDynamicIslandLimitedInWidth` (see [platform-specific.md](platform-specific.md)).

Source: [HIG — Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities)

## Controls

A button or toggle from your app in Control Center, the Lock Screen, or the Action button (iOS, iPadOS, macOS; not watchOS, tvOS, visionOS). Built with WidgetKit + App Intents.

- Anatomy: symbol + title + optional value. Control Center shows symbol (title/value at larger sizes); Lock Screen shows symbol only; Action button shows symbol + value in the Dynamic Island
- Offer actions worth doing without opening the app (e.g. start a Live Activity)
- Symbol must explain the action alone. Toggles need on and off symbols (`door.garage.open` / `door.garage.closed`); animate state changes; animate continuously while a long action runs
- Tint color applies to the "on" symbol and the Dynamic Island readout — pick a brand color
- Keep state current: after interaction, on completion, or via push
- Prompt for configuration on add when needed (`promptsForUserConfiguration()`)
- Action button hint text starts with a verb ("Hold for Silent") — `controlWidgetActionHint(_:)`
- Placeholder title/value when they vary; redact title/value (and optionally state) when locked
- Require unlock for security actions (doors, car) — `IntentAuthenticationPolicy`
- **Locked camera capture** (iOS 18+, `LockedCameraCapture`): a control can open your capture UI on a locked device; reuse your in-app camera UI; anything beyond capture requires unlock

Source: [HIG — Controls](https://developer.apple.com/design/human-interface-guidelines/controls)

## Notifications

Timely, high-value information people can read at a glance. Requires permission first.

- Concise; one notification per thing — don't repeat unanswered ones
- Don't instruct people to do tasks in the app; offer actions instead
- Errors belong in alerts, not notifications
- App in foreground: surface the info quietly (badge, insert into the view)
- No sensitive or private content — assume others can see it
- **Title:** short, title-style caps, no trailing punctuation; skip generic titles and let the system show the app name. Communication notifications show the sender instead
- **Body:** full sentences, sentence case; let the system truncate. Provide `hiddenPreviewsBodyPlaceholder` text ("New comment") for hidden previews
- Don't add your app name or icon — the system does
- Optional short, distinctive sound; never the only carrier of meaning; no custom vibration
- **Actions:** up to **4** buttons; short title-case labels describing the result; no "Open app" action; prefer nondestructive; add an SF Symbol icon to each
- **Badges:** only for unread count — never scores, prices, dates. Keep current (zero clears Notification Center); don't fake badges; don't rely on them alone
- **watchOS:** short look (wrist raised; discreet, not the sole channel) then long look (scrollable with Crown). Always ship a static long look, prefer a dynamic one too. Sash = app icon + name, colored or blurred. Default content background is transparent; to match system notifications use white at **18%** opacity. Up to **4** custom actions above the system Dismiss. Double tap triggers the first nondestructive action — put the most common one first

Source: [HIG — Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications)

## App Shortcuts

Key tasks exposed through App Intents to Siri, Spotlight, the Shortcuts app, the Action button (iPhone, Apple Watch), and Apple Pencil squeeze. Available right after install. Up to **10** per app. Not supported in tvOS; on macOS, App Shortcuts aren't offered but App Intents actions still work in the Shortcuts app.

- **27:** if your app fits a domain covered by app schemas, adopt them first so Siri and Apple Intelligence can surface features contextually; use App Shortcuts for what schemas don't cover
- Pick the most common, important tasks; best when finishable without leaving context, but opening the app for multistep work is fine
- At most one optional parameter with predictable values ("Start [morning, sleep] meditation"); if missing, ask — suggest a sensible default plus a short list
- Phrases must be short, speakable, include the app name (creatively), and have natural variants (`AppShortcutPhrase`). Too complex aloud = too complex
- Respond with spoken dialogue plus a [snippet](hig-patterns.md#snippets) (static info or confirmation) or a Live Activity (`LiveActivityIntent`) for ongoing timers/countdowns
- Put all critical info in the full dialogue text — responses may play on AirPods or HomePod
- Promote shortcuts with occasional in-app tips (`SiriTipUIView`)
- iOS/iPadOS: shown in Spotlight Top Hit / Shortcuts area with an SF Symbol or item preview; your order sets the initial ranking, then usage takes over
- Copy: "App Shortcuts" and "Shortcuts" are title case and plural; a single "shortcut" is lowercase

Source: [HIG — App Shortcuts](https://developer.apple.com/design/human-interface-guidelines/app-shortcuts)

## Complications

Timely data on the watch face (watchOS only), built as WidgetKit accessory widgets. Families: circular (incl. extra-large for X-Large face and bezel text), corner, inline (utilitarian small and large), rectangular. Legacy ClockKit templates remain for older watchOS.

- Show essential, changing data — a static launcher gets moved off the face
- Support every family you can; where you have nothing useful, show an app image that still launches
- Offer several complications per family (e.g. swim/bike/run) and a distinct deep link for each; pair them with a shareable preconfigured watch face
- Always-On makes the face visible to others — protect sensitive data
- Data is a timeline with limited daily reloads and stored entries — schedule entries for when the data matters (meeting an hour before, forecast at forecast time)
- Gauges: **closed** for percent-of-whole (battery), **open** for arbitrary ranges (speed), **segmented** for fast-changing ranged values (noise)
- Tinted mode: system desaturates and applies one color from the wearer's choice — never rely on color alone; supply alternate tinted images when desaturation looks bad
- Lines **≥ 2 pt**; provide static placeholder images for every complication (`placeholder(in:)`)
- Bezel text around a circular complication can run nearly 180° before truncating
- Rectangular (watchOS 10+) may appear in the Smart Stack — add meaningful background color, relevance via App Intents, or a Smart Stack–specific layout (see [Widgets](#widgets))

**Default SwiftUI text** (all rounded; 40 / 41 / 44 / 45–49 mm)
| Family | Weight | Size (pt) |
|--------|--------|-----------|
| Circular | Medium | 12 / 12.5 / 13 / 14.5 |
| Circular extra-large | Medium | 34.5 / 36.5 / 36.5 / 41 |
| Corner | Semibold | 10 / 10.5 / 11 / 12 |
| Rectangular | Medium | 16.5 / 17.5 / 18 / 19.5 |

**Common image sizes (pt; 40 / 41 / 44 / 45–49 mm)**
- Circular image 42 / 44.5 / 47 / 50; extra-large circular image 120 / 127 / 132 / 143
- Corner circular 32 / 34 / 36 / 38; corner gauge/text 20 / 21 / 22 / 24
- Rectangular large image with title 150×47 / 159×50 / 171×54 / 178.5×56; without title 162×69 / 171.5×73 / 184×78 / 193×82
- Full tables (gauges, stacks, placeholders, legacy templates) are on the HIG page

Source: [HIG — Complications](https://developer.apple.com/design/human-interface-guidelines/complications)

## Watch Faces

People can share configured faces (watchOS 7+) — from your app, website, Messages, Mail, or social. watchOS only.

- Ship shareable faces that showcase several of your complications (plus accent color, images, styles where the face allows); if the app isn't installed, the system offers to install it
- Show a preview of each face — email it to yourself from the iOS Watch app, optionally composite a hardware bezel from Apple Design Resources
- Cover all devices: some faces (Infograph, Infograph Modular, Meridian, Modular Compact, California, Chronograph Pro, Gradient, Solar Dial) need Series 4+, so offer an alternative for older watches and label supported devices
- On an incompatible-face error, offer the alternative configuration right away instead of an error

Source: [HIG — Watch faces](https://developer.apple.com/design/human-interface-guidelines/watch-faces)

## Status Bars

iOS and iPadOS only. (On iPhone Duo the status bar can move to the side — see [platform-specific.md](platform-specific.md).)

- The bar is transparent by default: keep it legible and don't let controls sit behind it looking tappable — prefer a scroll edge effect that blurs content under it (`ScrollEdgeEffectStyle`, `UIScrollEdgeEffect`)
- Hide it temporarily for full-screen media (like Photos); never permanently — bring it back with a simple, discoverable gesture such as a single tap
- Style via `preferredStatusBarStyle` / `UIStatusBarStyle`

Source: [HIG — Status bars](https://developer.apple.com/design/human-interface-guidelines/status-bars)

## Top Shelf

tvOS Home Screen showcase shown when your app is in the Dock and focused. Templates are in Apple Design Resources.

- Goal: jump straight into content — new releases, upcoming titles, personalized picks, resume playback. Skip things already bought or watched; no ads, avoid prices
- Prefer dynamic, full-screen content built from layered images; otherwise supply at least one static fallback of **2320×720 pt** (system flips and blurs it to fit 1920 px wide at 16:9). A static image isn't focusable — don't make it look interactive
- **Carousel actions** — full-screen video/images with Play + More Info buttons; give a short title (optional subtitle). Good for content people already know (photos, franchises)
- **Carousel details** — adds metadata (summary, cast); title near the top, optional attribution phrase above it
- **Sectioned content row** — focusable labeled row; load enough images to fill the width and include at least one label. Mixed aspect ratios scale up to the tallest
- **Scrolling inset banner** — auto-advancing wide banners; use **3–8** images; text must be baked into the image (put it on its own layer and repeat it in the accessibility label)

| Image | Actual (pt) | Focused/safe (pt) | Unfocused (pt) |
|-------|-------------|-------------------|----------------|
| Poster 2:3 | 404×608 | 380×570 | 333×570 |
| Square 1:1 | 608×608 | 570×570 | 500×500 |
| 16:9 | 908×512 | 852×479 | 782×440 |
| Inset banner | 1940×692 | 1740×620 | 1740×560 |

Source: [HIG — Top Shelf](https://developer.apple.com/design/human-interface-guidelines/top-shelf)
