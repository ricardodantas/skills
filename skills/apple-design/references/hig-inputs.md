# HIG Inputs

How people drive your app — touch, keyboard, pointer, Pencil, hardware buttons, eyes, remotes, and controllers — and the per-platform rules for each. Pair with [platform-specific.md](platform-specific.md) for platform context.

## Gestures

- Never make a gesture the only path: people use voice, keyboard, Switch Control
- Standard gestures keep standard meanings; don't repurpose tap/swipe for app-unique actions or invent gestures for standard ones (activating, scrolling)
- Give immediate feedback during the gesture; make it obvious when a gesture can't apply (locked object, disabled button)
- **Custom gestures** only for frequent specialized tasks (games, drawing): discoverable, easy, distinct, never the sole way to do something important; teach them in context
- Shortcut gestures supplement, never replace, visible controls (edge-swipe back *and* a Back button)
- Don't collide with system gestures (watchOS edge swipes, visionOS hand-roll overlays)

**Standard gestures**
| Gesture | Platforms | Meaning |
|---------|-----------|---------|
| Tap | all | Activate, select |
| Swipe | all | Reveal actions, dismiss, scroll |
| Drag | all | Move an element |
| Touch/pinch and hold | all but macOS | More controls/options |
| Double tap | all | Zoom in/out; primary action on Watch |
| Zoom, Rotate | all but watchOS | Magnify; rotate selection |

- **iOS/iPadOS extras:** 3-finger swipe left/right = undo/redo; 3-finger pinch in/out = copy/paste; 4-finger swipe = switch apps (iPad); shake = undo/redo. Allow simultaneous recognition when it helps (game joystick + fire button)
- **macOS:** keyboard and mouse first; standard gestures via Magic Trackpad/Mouse
- **visionOS:** *indirect* (look to target, pinch to act — default for UI) and *direct* (touch within reach — tiring, so for occasional close-up objects). Offer both where possible; don't require specific body positions. Custom hand gestures need a Full Space plus hand-tracking permission; favor comfort, avoid two-hand-only or hand-specific gestures. Keep the area around the palm free (system Home/Control Center overlays, visionOS 2+); avoid custom hand-roll gestures; an immersive game may defer the overlay with `persistentSystemOverlays(_:)`
- **watchOS double tap** (watchOS 11+): scrolls lists and vertical tabs; can trigger a view's primary action (`handGestureShortcut(_:isEnabled:)` with `.primaryAction`) — only in non-scrolling views, on the most-used button (e.g. play/pause)

Source: [HIG — Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)

## Keyboards

Physical keyboards work everywhere except Apple Watch; Mac users rely on them constantly, iPad users often. SwiftUI: `.keyboardShortcut()` / `KeyboardShortcut`.

- Support **Full Keyboard Access** (iOS, iPadOS, macOS, visionOS) — every window, menu, and control reachable by keyboard; test it from Accessibility settings
- Keep standard shortcuts standard (⌘C/V/X/Z, ⇧⌘Z redo, ⌘F find, ⌘, settings, ⌘? help, ⌘W close, ⌘Q quit, ⌘. cancel…). Repurpose one only when its action can't exist in your app (e.g. no text styling → ⌘I could be Get Info). Full table on the HIG page
- Custom shortcuts only for the most frequent app-specific commands — too many makes the app feel hard
- Modifiers: **Command** primary; **Shift** secondary/complementary; **Option** sparingly for power features; avoid **Control** (system uses it)
- List modifiers in the order Control, Option, Shift, Command
- For the upper character of a two-character key, show that character, not Shift (⌘? not ⇧⌘/)
- Don't make a new shortcut by adding a modifier to an unrelated existing one (⇧⌘Z must relate to undo)
- Honor modifier conventions: ⌘-drag moves as a group, ⇧-resize keeps aspect ratio, held arrow keys nudge by the smallest unit
- The system localizes and mirrors shortcuts for RTL — don't hard-code alternatives
- Games: people expect ⌘Q etc. to work but also want rebindable keys — see [Game Controls](#game-controls)
- **visionOS:** holding ⌘ shows a flat shortcut list grouped by menu category, without submenus — write self-explanatory titles (`discoverabilityTitle`). A physical keyboard also brings up a virtual overlay with completions

Source: [HIG — Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

## Pointing Devices

Trackpad/mouse on Mac, and as an extra (not a replacement) input on iPad and Vision Pro. Not supported in tvOS or watchOS.

- Same gesture means the same thing everywhere; never redefine systemwide trackpad gestures (Dock, Mission Control), even in games
- One consistent experience across touch, eyes, pointer, and keyboard; modifier-key behavior (e.g. ⌥-drag duplicates) must match for touch and pointer
- Let the pointer reveal auto-hiding controls (minimized toolbar, video controls)

**iPadOS pointer**
- Default shape is a circle; context shapes like I-beam over text. Distinguish pointer vs finger only when it adds value (precise scrubbing)
- Content effects: **highlight** — small elements with transparent background (bar buttons, tab bars, segmented controls); **lift** — small opaque elements (app icons); **hover** — large elements with custom scale/tint/shadow and no shape change. Prefer system effects, especially for custom controls that act like standard ones
- Magnetism pulls the pointer to lift/highlight elements and text areas, not hover ones
- Hit-region padding: about **12 pt** around bezeled elements, about **24 pt** around unbezeled ones; make adjacent bar-button regions contiguous
- Give a nonstandard lift element its corner radius (`UIPointerShape.roundedRect(_:radius:)`)
- Band selection for multiple items in custom views (`UIBandSelectionInteraction`, iPadOS 15+)
- Accessories (`UIPointerAccessory`): simple images; animate them to signal state (`plus` → `circle.slash`)
- No decorative effects, no instructional text on the pointer; useful annotations (X/Y values, dimensions) are fine; keep custom shapes obvious
- Custom hover: scale only when there's room (not table rows); tint-only in tight spaces; never shadow without scale

**macOS** — honor standard clicks/gestures people can customize (secondary click, smart zoom, swipe
between pages, force click…). Use standard `NSCursor` styles: `arrow`, `iBeam`, `pointingHand` for links, `openHand`/`closedHand` for panning, `crosshair`, `dragCopy` (⌥-drag), `dragLink` (⌥⌘-drag),
`operationNotAllowed`, `disappearingItem`, `contextualMenu`, directional `resize*` cursors.

**visionOS** — pointer works alongside eyes and hands; gaze sets the pointer's context (window), and
the pointer hides during trackpad gestures. No work needed from your app.

Source: [HIG — Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

## Apple Pencil & Scribble

iPadOS only. Pencil can report tilt (altitude), pressure, orientation (azimuth), and — on Pencil Pro — barrel roll. Frameworks: PencilKit, PaperKit.

- Behave like a real pen: mark the instant the tip lands (no mode switch or button first); support natural habits such as writing in margins
- Controls must respond to Pencil too, so people aren't forced to switch to a finger
- Map pressure/tilt to continuous stroke properties (width, opacity) — keep it simple
- Feedback must look directly connected to the tip; no action at a distance
- Keep controls clear of either hand; let people move them for left/right-handed use
- **Hover:** preview what the tool will do (size, color) near the tip; don't vary the preview with height; show a mid-range value, not the extremes; never trigger actions on hover; limit hover previews to Pencil, not the pointer. Hover + squeeze/modifier can open a tool menu near the tip
- **Double tap:** respect the user's system setting (eraser toggle, previous tool, color picker, off); a custom mode must be opt-in, discoverable, and visibly indicated. Never use it to change content destructively — prefer easily undone actions
- **Squeeze (Pencil Pro):** one quick, discrete action; show results (e.g. a menu) next to the tip; nondestructive and undoable. People may map squeeze to an App Shortcut instead
- **Barrel roll (Pencil Pro):** only alters the mark (e.g. highlighter angle) — never navigation or UI
- **Scribble:** works in all standard text inputs except password fields. Custom fields shouldn't need a tap first; enable writing wherever text entry feels natural, even blank space (`UIIndirectScribbleInteraction`). While writing: no autocompletion overlay, hide placeholder text, don't move/resize/autoscroll the field; enlarge small fields before or between writing (`UIScribbleInteraction`)
- **PencilKit canvas:** colors adapt to Dark Mode by default — turn that off when drawing over PDFs/photos. The tool picker lacks undo/redo in compact width — add toolbar buttons and support the 3-finger undo/redo swipe

Source: [HIG — Apple Pencil and Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble)

## Digital Crown

Apple Watch and Apple Vision Pro. On Vision Pro the Crown is system-only (volume, immersion level, recenter, Accessibility, Home) — apps get no direct Crown input.

- **watchOS 10+:** the Crown is the primary navigation input — Smart Stack, app grid, vertical tabs, lists, variable-height pages. Build vertically so the Crown moves between key elements; always provide a touch equivalent
- Where no navigation is needed, use it to inspect data (World Clock scrubs time)
- Always show visual feedback for rotation, and scale changes to rotation speed without making values hard to land on
- Keep default haptic detents when they fit; turn them off if they clash with your animation; tables can use linear instead of per-row detents (helpful for uneven row heights). API: `WKCrownDelegate`

Source: [HIG — Digital Crown](https://developer.apple.com/design/human-interface-guidelines/digital-crown)

## Action Button

Supported iPhone and Apple Watch models (not iPadOS, macOS, tvOS, visionOS). People bind it in Settings to a system function or one of your App Shortcuts (or a Control — see [Controls](hig-system-experiences.md#controls)).

- Offer a few essential, frequently used actions ("Start Egg Timer"); no "open app" shortcut — the system already provides that
- Labels: title case, start with a verb, present tense, no articles/prepositions, **≤ 3 words** ("Start Race", not "Start the Race")
- Let the system teach setup; don't duplicate Settings guidance in your app
- **iOS:** finish the task in place — prompt with a snippet, then run a Live Activity (like Set Timer) instead of launching the app
- **watchOS (Ultra):** first press starts a workout, dive, or waypoint; later presses should advance it (mark segment, next leg) — ideally one memorable secondary action. Use presses to add function, not to stop (put Stop in the UI). Action + side button together should pause, except where pausing is unsafe (dive apps)

Source: [HIG — Action button](https://developer.apple.com/design/human-interface-guidelines/action-button)

## Camera Control

iPhone models with the button (introduced on iPhone 16 / 16 Pro); iOS only. A light press shows an overlay beside the button; a light double press lists controls; sliding adjusts the value. API: `AVCaptureControl` (AVFoundation).

- Two control types: **slider** (continuous, e.g. contrast) and **picker** (discrete, e.g. grid on/off); system zoom-factor and exposure-bias controls are available to include
- SF Symbols only (no custom symbols); symbols describe the function, not the current state (e.g. `bolt.fill` flash, `camera.filters`)
- Short names (labels follow Dynamic Type); show units/context on slider values (EV, %) via `localizedValueFormat`; set `prominentValues` so sliding snaps to common stops
- Keep your UI out of the overlay area in portrait and landscape; maximize the viewfinder; don't duplicate overlay controls on screen
- The control set is fixed at runtime — enable/disable per mode instead. Put frequent controls in the middle; the system remembers the last one used
- Ship a locked camera capture extension so the button can launch your camera from the Lock Screen, Home Screen, or other apps (see [Controls](hig-system-experiences.md#controls))

Source: [HIG — Camera Control](https://developer.apple.com/design/human-interface-guidelines/camera-control)

## Eyes (visionOS)

People look at an element to target it; the system shows a **hover effect**, then an indirect pinch acts on it. Some components expand on gaze (tab bars reveal labels, buttons show tooltips). Hover is separate from keyboard/controller focus effects (see [Focus & Selection](#focus--selection)).

- Always offer other ways to interact (accessibility features)
- Keep needed objects in the field of view; avoid rapid eye jumps across wide areas or depths; place content read over time **≥ 1 m** away
- Prefer standard components — they respond to gaze consistently
- Cut visual noise and motion near targets (revealing content beside a looked-at button pulls the eye)
- Spacing: at least **16 pt** margin around each interactive item, or centers **≥ 60 pt** apart
- Don't fill the field of view with repeating patterns (depth illusions)
- Guide attention with subtle cues (center placement, gentle motion, contrast, scale)
- Make targets rounded — corners pull the eye away from the center
- Multi-element controls (image + label) need one containing shape for the highlight
- **Custom hover effects** (UI elements and RealityKit entities): run out of process — your app never learns what someone looked at, so an effect can change appearance but can't trigger logic. Use sparingly for special moments. Delay: none (subtle affordances, e.g. slider knob), short (quick-act elements like tab expansion), long (extra info like tooltips). Keep at least one primary view unchanged between states; test on device

Source: [HIG — Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)

## Focus & Selection

Focus marks what a keyboard, remote, or controller will act on. iPadOS, macOS, tvOS, visionOS (not iOS or watchOS). Focusing often selects, except where that would jump context (tvOS needs a separate click to open).

- Use system focus effects; custom only when truly necessary
- Never move focus on your own — except with directional input when the focused item disappears (move to a neighbor); otherwise just hide the indicator
- Match platform reach: iPadOS/macOS Full Keyboard Access covers controls, so you only add focus for content (list items, text/search fields); tvOS needs every element focusable
- Focus ring for text/search fields; row highlight for lists/collections. Focused list rows use white text on the accent color, unfocused use gray (`UICollectionView`, `NSTableView`)
- **iPadOS (15+):** Tab moves between focus groups (sidebar, grid, list) in reading order; arrows move within a group. Halo (focus ring) via `UIFocusHaloEffect` — reshape it for rounded or custom paths and keep badges/parents from clipping it. Group custom stacks with `focusGroupIdentifier`; mark the default item with `UIFocusGroupPriority`
- **tvOS:** directional focus with parallax; full-screen content takes gestures directly (no focus); avoid pointers outside gameplay. Design all five states — unfocused, focused (scaled up, supply larger assets and leave room), highlighted (pressed), selected, unavailable
- **visionOS:** same focus system as iPadOS/tvOS for connected keyboards and controllers

Source: [HIG — Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection)

## Game Controls

Controllers work on every platform except watchOS, but they're optional — always keep the platform's default input (touch, keyboard/mouse, remote, eyes and hands) as a fallback.

**Touch (iOS/iPadOS, Touch Controller framework)**
- Use virtual controls only when needed; prefer direct interaction (tap an object to select it)
- Stay inside safe areas, clear of the Home indicator and Dynamic Island; primary buttons near the thumbs, menus at the top
- Sizes: **≥ 44×44 pt** for frequent controls, **≥ 28×28 pt** for minor ones (menus)
- Visible press state (e.g. glow seen around the thumb) plus sound and haptics
- Icons show the action (a sword for attack), never controller names like A/X/R1
- Hide controls when irrelevant (e.g. movement stick until touched); merge actions into one control via double tap or touch and hold
- Left side = movement (thumbstick appears where the thumb lands); right side = camera via direct pan

**Physical controllers (Game Controller framework)**
- tvOS/visionOS may require a controller ("Game Controller Required" badge, `GCRequiresControllerUserInteraction`) — still detect absence and prompt to connect
- Auto-detect paired controllers; label with the connected controller's own scheme (`GCControllerElement`) and SF Symbols glyphs, not text; match the active player's controller
- Menus outside gameplay: **A** activate, **B** back/cancel, shoulders switch sections, sticks/D-pad move selection, **Menu** opens settings/pauses, Home/logo reserved for the system
- **visionOS spatial controllers** (e.g. PlayStation VR2 Sense): mirror hand input — look + trigger for indirect, reach + trigger for direct

**Keyboard bindings**
- Favor single keys (I = Inventory, M = Map, Space = main action); cluster related commands near WASD or the number row
- Test on Apple keyboards (remap Control-based bindings to Command beside the Space bar)
- Let players rebind keys

Source: [HIG — Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls)

## Remotes (tvOS)

The Siri Remote (clickpad + touch surface) is Apple TV's primary input.

- Standard gestures for standard actions outside gameplay; swipe direction = focus direction; custom gestures mainly for games
- Show feedback for gestures (a resting thumb hints where to swipe for the info area)
- **Press** = intentional (choose, confirm, fire); **tap** = navigation/info only — ignore stray taps, especially during live video. Positional taps (up/down/left/right) only if intuitive
- **Back** opens the parent screen (top level → Home Screen), not necessarily the previous one. In gameplay, Back opens a pause menu; Back again resumes. Press and hold Back always goes Home
- **Play/Pause** plays, pauses, resumes media; in games it can act as a secondary button or skip intros
- Swipe scrolls with momentum (edge swipes go faster); press-then-swipe enters scrubbing
- Compatible remotes with guide/page buttons: open your EPG on "guide"/"browse", page within it; during playback page up/down changes channel

Source: [HIG — Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes)

## Motion & Nearby Interactions

**Gyroscope and accelerometer** (Core Motion; iOS, iPadOS, watchOS; tvOS via the Siri Remote gyro)
- Collect motion data only for a real benefit (fitness feedback, gameplay) — never just to have it
- Outside active gameplay, don't drive UI directly with device motion: hard to repeat precisely, physically hard for some people, and costly for battery

Source: [HIG — Gyroscope and accelerometer](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer)

**Nearby interactions** (Nearby Interaction framework, Ultra Wideband devices; iOS gets distance +
direction, watchOS distance only and apps must be foreground; not macOS, tvOS, visionOS)
- Needs permission; session-scoped random device IDs protect privacy
- Anchor the task in a physical action (bring devices together to hand off audio)
- Use distance, direction, and context (share sheet suggests the person you're facing); sharpen feedback as things get closer (arrow → pulsing circle when finding an AirTag)
- Continuous feedback; blend visual (on screen) with audio/haptics (while looking at the world)
- Never the only way to do a task
- Encourage portrait implicitly (landscape reduces accuracy); direction only works inside the sensor's field of view; tell people in onboarding that bodies and large objects in between degrade it

Source: [HIG — Nearby interactions](https://developer.apple.com/design/human-interface-guidelines/nearby-interactions)
