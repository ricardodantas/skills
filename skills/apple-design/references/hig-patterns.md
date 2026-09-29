# HIG Patterns

## Navigation

### Navigation Models

#### Hierarchical (Push/Pop)
- Use `NavigationStack` (SwiftUI) or `UINavigationController` (UIKit)
- Drill down through content levels; back button auto-provided
- Best for: Settings, detail views, content hierarchies
```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.title, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

#### Flat (Tab-based)
- Use `TabView` for top-level sections (max 5 tabs visible)
- Each tab maintains its own navigation stack
- Best for: Apps with distinct functional areas
```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Search", systemImage: "magnifyingglass", role: .search) { SearchView() }
    Tab("Profile", systemImage: "person") { ProfileView() }
}
.tabViewStyle(.sidebarAdaptable)  // iPadOS: tab bar can expand into a sidebar
```
- iPadOS: the tab bar sits near the top; with `.sidebarAdaptable` it converts to a sidebar, and in iPadOS 27 it expands into a full sidebar. For a sidebar-only layout, use `NavigationSplitView`
- iOS 27: `role: .prominent` sets one tab apart at the trailing end (e.g., Cart); only one per tab bar

#### Split View (iPad/Mac)
- `NavigationSplitView` for sidebar + content + detail
- Sidebar auto-gets Liquid Glass styling (iOS 26+)
- Collapses to hierarchical on compact width
```swift
NavigationSplitView {
    SidebarView()
} content: {
    ContentListView()
} detail: {
    DetailView()
}
```

### Navigation Best Practices
- Always provide a clear path back (system back button/gesture)
- Use `navigationTitle()` on every screen
- Support swipe-back gesture (don't override edge pan)
- Deep link support via `.onOpenURL()` or `NavigationPath`
- Avoid more than 3-4 levels of hierarchical depth
- Tab bar: Use SF Symbols for tab icons, short labels (1-2 words)

Source: [HIG — Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars), [HIG — Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars), [HIG — Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

## Modality

### When to Use Modals
- Task requires completion or explicit dismissal
- Self-contained workflow (compose, create, settings)
- Critical alerts requiring immediate attention
- **Don't** use for information that could be inline

### Presentation Styles
| Style | Use | SwiftUI |
|-------|-----|---------|
| Sheet (page) | Forms, creation flows | `.sheet()` |
| Full screen cover | Immersive tasks, media | `.fullScreenCover()` |
| Popover | Quick options (iPad) | `.popover()` |
| Alert | Critical decisions | `.alert()` |
| Confirmation dialog | Destructive actions | `.confirmationDialog()` |

### Sheet Best Practices (iOS 26+)
- Use `.presentationDetents([.medium, .large])` for resizable sheets
- Liquid Glass is applied automatically — don't set custom backgrounds
- iOS 27: `.navigationTransition(.crossFade)` on the sheet content fades it in over the current view instead of sliding up to cover it
- Provide clear dismiss affordance (X button or "Done")
- Support drag-to-dismiss (default behavior)
```swift
.sheet(isPresented: $showSheet) {
    NavigationStack {
        FormContent()
            .navigationTitle("New Item")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { showSheet = false }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") { save(); showSheet = false }
                }
            }
    }
    .presentationDetents([.medium, .large])
}
```

### Snippets
Siri, Spotlight, and Shortcuts.
Compact views an App Intent shows in response to an action — not a sheet you present yourself. iOS, iPadOS, and macOS only.
- **Confirmation** snippet: lets people confirm or cancel (system Cancel + primary button). Label the primary button with the action ("Order", not "OK"); default is Continue
- **Result** snippet: shows an outcome, dismissed with Done. Every snippet intent ends in a result; confirmation is optional
- Keep custom views ≤ 400 pt tall, concise, and legible in light and dark at large text sizes
- Convey purpose visually — don't rely on the spoken dialogue text; deep-link to your app for more detail

Source: [HIG — Modality](https://developer.apple.com/design/human-interface-guidelines/modality), [HIG — Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets), [HIG — Snippets](https://developer.apple.com/design/human-interface-guidelines/snippets)

## Search

### Search Implementation
```swift
NavigationStack {
    ContentView()
}
.searchable(text: $searchText, prompt: "Search items")
```

### Search Best Practices
- Give important search a primary position: a search tab, or a toolbar field — prefer the **bottom** toolbar when there's room; use the top when bottom content must stay uncovered
- Search tab has two styles: a **standard tab** opening a landing page (suggestions, discovery — e.g., Apple TV) or a **button appearance** that focuses the field and keyboard immediately and returns to the previous tab on exit (quick lookups)
- Use an inline field only for search scoped to the adjacent content
- iPadOS/macOS: search field at the trailing side of the toolbar; top of sidebar to filter it; a sidebar/tab item for discovery-heavy search
- Show suggestions with `.searchSuggestions { }`
- Support search scopes for filtering: `.searchScopes($scope) { }`
- Use `.searchToolbarBehavior(.minimized)` for secondary search
- Use `Tab("Search", ..., role: .search)` for a search tab in TabView (iOS 26+)
- Show recent searches and suggestions
- Debounce network-backed searches so results don't flicker on every keystroke (tune the delay to your backend)

Source: [HIG — Searching](https://developer.apple.com/design/human-interface-guidelines/searching)

## Settings

### In-App Settings
- Use `Form` with `Section` for grouped settings
- Use system controls: `Toggle`, `Picker`, `Stepper`, `Slider`
- Group related settings in sections with headers/footers
- Use `NavigationLink` for sub-settings screens
- Sync with system settings where applicable (Dark Mode, notifications)

```swift
Form {
    Section("General") {
        Toggle("Notifications", isOn: $notifications)
        Picker("Theme", selection: $theme) {
            Text("System").tag(Theme.system)
            Text("Light").tag(Theme.light)
            Text("Dark").tag(Theme.dark)
        }
    }
    Section("Account") {
        NavigationLink("Profile") { ProfileSettings() }
        NavigationLink("Privacy") { PrivacySettings() }
    }
}
```

Source: [HIG — Settings](https://developer.apple.com/design/human-interface-guidelines/settings)

## Onboarding

### Best Practices
- Keep it brief; don't ask people to memorize much, and let them start using the app quickly
- Show value immediately — let users start using the app fast
- Request permissions in context (not upfront)
- Use illustrations/animations to explain unique features
- Provide skip option
- Don't repeat Apple's built-in tutorials
- Request only essential permissions, explain why each is needed

### Permission Requests
- Ask at point of use, not at launch
- Provide clear usage description strings in Info.plist
- Explain benefit to user before triggering system prompt
- Gracefully handle denial — show how to enable later

Source: [HIG — Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding), [HIG — Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy)

## Data Display Patterns

### Lists
- Use `List` for scrollable content (auto-styling, swipe actions)
- Support `.swipeActions()` for contextual actions
- Use `.refreshable()` for pull-to-refresh
- Show empty state with helpful message when no data

### Loading States
- Use `ProgressView()` for indeterminate loading
- Show skeleton/placeholder content for better perceived performance
- Never block the entire UI for loading

### Error States
- Show inline errors near the source (not just alerts)
- Provide retry action
- Use `.alert()` only for critical errors requiring attention

Source: [HIG — Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables), [HIG — Loading](https://developer.apple.com/design/human-interface-guidelines/loading)

## Feedback

- Make every piece of feedback accessible (not color- or motion-only)
- Prefer status woven into the UI instead of interrupting; reserve alerts for critical, ideally actionable, information
- Warn before *unexpected* irreversible data loss — not when loss is the expected result
- Confirm completion of significant tasks when it helps; when a command can't run, say why
- **watchOS**: avoid indeterminate spinners — show determinate progress or content instead

Source: [HIG — Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

## Entering Data

- Gather what you can from the system (settings, or location/calendar with permission) instead of asking
- Make the expected input obvious: placeholder like "username@company.com" or a label like "Email"; prefill sensible defaults
- Use `SecureField` for sensitive input; never prefill passwords — ask, or use biometrics/keychain. tvOS digit entry can hide numerals; visionOS blurs secure fields during AirPlay
- Offer choices (pickers, menus) instead of free text where possible; accept drag-and-drop and paste
- Validate dynamically as people type; keep Next/Continue disabled until required fields are filled
- **macOS**: an expansion tooltip can reveal clipped text in a narrow field

Source: [HIG — Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)

## Drag and Drop

- Support it broadly, but always offer alternatives: menu commands for copy/move, plus `accessibilityDragSourceDescriptors` / `accessibilityDropPointDescriptors` on iOS/iPadOS
- Same container → move; different container → copy. Holding Option (hardware keyboard) forces a copy
- Support multi-item drags; make drops undoable, or confirm irreversible ones
- Show the drag image after about 3 pt of movement; group multiple items with flocking; don't let the image change wildly
- Highlight a valid destination (or insertion point) only while hovering it; show nothing or `circle.slash` for invalid targets; on a failed drop, animate the item back or fade it out
- Offer multiple representations (highest fidelity first); on drop, take the richest one you support and extract only what's relevant
- Auto-scroll destinations; show progress or placeholders for slow transfers; keep text styling when both sides support it, else adopt the destination style
- Spring loading: buttons and segmented controls can activate while content hovers (iPad) or on force click (Mac)
- **iOS/iPadOS**: allow multiple simultaneous drags and drops (iPadOS: adding items mid-drag). **macOS**: drag from inactive windows without activating them, drag to Finder in an openable format, badge multi-item drags, use copy, drag-link, disappearing-item, and not-allowed pointers. **visionOS**: launch your app for content dropped into empty space (`NSUserActivity`). Not in tvOS or watchOS

Source: [HIG — Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop)

## Undo and Redo

- Make results predictable and visible — show what changed after an undo or redo
- Support multiple levels of undo; consider a "revert all changes" option for bulk rollback
- Show undo/redo buttons only when truly needed
- **iOS/iPadOS**: don't redefine the standard undo gestures; describe the action briefly — the system prefixes the alert title with "Undo"/"Redo"
- **macOS**: put Undo/Redo in the Edit menu with ⌘Z and ⇧⌘Z
- Not supported in tvOS or watchOS

Source: [HIG — Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)

## Launching

- Launch instantly; provide a launch screen where the platform requires one
- Make the launch screen nearly identical to your first screen — no text, no ads. If you truly need a splash, put it at the start of onboarding instead
- Restore the previous state on relaunch so people continue where they left off
- **iOS/iPadOS**: launch in the appropriate orientation. **tvOS**: live-viewing apps can start playback soon after launch. **visionOS**: consider launching into the Shared Space even if the app goes fully immersive

Source: [HIG — Launching](https://developer.apple.com/design/human-interface-guidelines/launching)

## Managing Accounts

- Require an account only when core functionality needs it; explain the benefit and delay sign-in as long as possible
- Prefer Sign in with Apple; otherwise passkeys; if you keep passwords, add two-factor authentication
- Name the authentication method you use, mention only methods available in context, don't add an app-level "enable Face ID" toggle, and don't call account credentials a "passcode"
- **Deletion is required** if you allow in-app account creation: an easy in-app path to real deletion (not just deactivation), consistent with your website; optionally schedule it; say when it will complete and notify when done; explain billing/cancellation for subscriptions
- TV provider accounts: hide sign-out when signed in at the system level; never tell people to sign out via privacy controls
- **tvOS**: let people sign up or authenticate on another device; minimize typing; don't re-ask for profile selection on shared accounts. **watchOS**: rely on iCloud Keychain sync

Source: [HIG — Managing accounts](https://developer.apple.com/design/human-interface-guidelines/managing-accounts)

## Managing Notifications

Use *communication* notifications (with SiriKit intents) for calls and messages; give every other notification an interruption level that reflects its real urgency:

| Level | Use | Breaks through Focus / scheduled summary | Overrides Ring/Silent |
|-------|-----|------------------------------------------|-----------------------|
| Passive | Read at leisure | No | No |
| Active (default) | Nice to know on arrival | No | No |
| Time Sensitive | Needs attention now — events happening now or within an hour | Yes | No |
| Critical | Urgent health/safety only | Yes | Yes |

- Never send marketing via notifications without explicit opt-in, and never at Time Sensitive level
- Ask for promotional opt-in with your own clear UI, and offer an in-app settings screen to change it
- **watchOS**: people manage settings in the Watch app on iPhone and can swipe left on an arriving notification for options like muting

Source: [HIG — Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications)

## Ratings and Reviews

- Ask only after people have shown real engagement — never on first launch, during onboarding, or mid-task
- Don't pester; leave at least a week or two between requests
- Prefer the system prompt (`RequestReviewAction`); the system shows it at most **three times per app in 365 days**
- Resetting your summary rating is a trade-off: a fresher score vs. fewer ratings shown

Source: [HIG — Ratings and reviews](https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews)

## Playing Haptics

- Use system haptic patterns only for their documented meanings, and consistently
- Pair haptics with visual/audio feedback; keep them short, tied to discrete events, and don't overuse them
- Make haptics optional, and remember they can affect other experiences on the device
- Custom haptics combine *transient* taps and *continuous* vibrations
- **iOS**: standard toggles, sliders, and pickers already play haptics. `UIFeedbackGenerator` offers notification (success, warning, error), impact (light, medium, heavy, rigid, soft — matched to the size/stiffness of colliding objects), and selection (value changing)
- **macOS** (Force Touch trackpad): alignment, level change, and generic feedback for drags and force clicks
- **watchOS**: notification, up, down, success, failure, retry, start, stop, and click — use click sparingly, as overlapping clicks confuse

Source: [HIG — Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

## Charting Data

- Chart only to highlight something important; keep charts simple and reveal extra detail progressively instead of packing data in
- Prefer familiar chart types; teach people how to read a novel one
- Add titles, subtitles, annotations, or a one-line summary headline to surface the takeaway
- Size charts to their purpose and detail level; keep styles consistent across charts and continuous across charts showing the same data
- Every chart must be accessible: accessibility labels for values/components plus accessibility elements for interaction. A summary headline does not replace labels
- Component-level guidance (marks, axes, platform notes): see `hig-components-extended.md#charts`

Source: [HIG — Charting data](https://developer.apple.com/design/human-interface-guidelines/charting-data)
