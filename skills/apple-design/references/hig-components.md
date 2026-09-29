# HIG Components

Presentation, layout, content, and status components (popovers, windows, split views, scroll views, page controls, disclosure controls, text and web views, charts, gauges, rating indicators) are in `hig-components-extended.md`.

## Buttons

### Button Styles (iOS 26 Liquid Glass)
| Style | Appearance | Use |
|-------|-----------|-----|
| `.glass` | Translucent, see-through | Secondary actions |
| `.glassProminent` | Opaque, no show-through | Primary actions |
| `.borderedProminent` | Filled with tint | Primary (pre-iOS 26) |
| `.bordered` | Tinted outline | Secondary |
| `.borderless` | Text only | Tertiary/inline |
| `.plain` | No styling | Custom layouts |

### Button Sizes
```swift
.controlSize(.mini)        // Smallest
.controlSize(.small)       // Compact
.controlSize(.regular)     // Default
.controlSize(.large)       // Prominent
.controlSize(.extraLarge)  // iOS 26+ hero actions
```

### Button Border Shapes
```swift
.buttonBorderShape(.capsule)                    // Default pill shape
.buttonBorderShape(.roundedRectangle(radius: 8)) // Rounded rect
.buttonBorderShape(.circle)                      // Circular (icon buttons)
```

### Destructive Actions
- Use `.role(.destructive)` for red-tinted destructive buttons
- Always confirm destructive actions with `.confirmationDialog()`
- Place destructive actions where accidental taps are unlikely

Source: [HIG — Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)

## Forms & Input

### Text Input
```swift
TextField("Name", text: $name)
    .textContentType(.name)           // Autofill support
    .autocorrectionDisabled()
    .textInputAutocapitalization(.words)

SecureField("Password", text: $password)
    .textContentType(.password)

// iOS 27+: match text field shape to neighboring buttons
HStack {
    TextField("Search", text: $query)
    Button("Go", action: search)
}
.buttonBorderShape(.capsule)
.textInputBorderShape(.capsule)
```

### Content Types (for Autofill)
`.name`, `.emailAddress`, `.telephoneNumber`, `.streetAddressLine1`, `.postalCode`, `.creditCardNumber`, `.password`, `.newPassword`, `.oneTimeCode`, `.URL`

### Pickers
```swift
// Inline picker
Picker("Color", selection: $color) {
    ForEach(colors) { Text($0.name).tag($0) }
}

// Date picker
DatePicker("Date", selection: $date, displayedComponents: [.date, .hourAndMinute])

// Color picker
ColorPicker("Accent", selection: $accentColor)
```

### Toggles & Sliders
```swift
Toggle("Enable Feature", isOn: $enabled)
    .toggleStyle(.switch)  // Default iOS toggle

Slider(value: $volume, in: 0...1) {
    Text("Volume")
} minimumValueLabel: {
    Image(systemName: "speaker")
} maximumValueLabel: {
    Image(systemName: "speaker.wave.3")
}

Stepper("Quantity: \(quantity)", value: $quantity, in: 1...99)
```

### Segmented Controls
Linear set of segments, each acting as a button. Not available in watchOS.
- Use for closely related choices that affect an object, state, or view, or when selection state must stay visible
- Limit segments: about 5–7 in wide layouts, about **5 on iPhone**; keep segment widths consistent
- Use either text or images in one control, not a mix; keep content similar in size; label with nouns or noun phrases
- **iOS/iPadOS**: good for switching between closely related subviews. **macOS**: use a tab view (not a segmented control) to switch main-window views; add introductory text if the purpose is unclear; consider spring loading. **tvOS**: prefer a split view for content filtering; keep other focusable items away from it. **visionOS**: icon-only segments show your descriptive text as a tooltip on gaze
```swift
Picker("View", selection: $mode) {
    Text("List").tag(Mode.list)
    Text("Grid").tag(Mode.grid)
}
.pickerStyle(.segmented)
```

Source: [HIG — Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields), [HIG — Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers), [HIG — Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles), [HIG — Sliders](https://developer.apple.com/design/human-interface-guidelines/sliders), [HIG — Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)

## Lists

### Basic List
```swift
List {
    Section("Favorites") {
        ForEach(favorites) { item in
            NavigationLink(value: item) {
                Label(item.name, systemImage: item.icon)
            }
        }
        .onDelete(perform: deleteFavorites)
        .onMove(perform: moveFavorites)
    }
}
.listStyle(.insetGrouped)  // Default iOS style
```

### List Styles
- `.insetGrouped` — Default iOS (rounded sections with inset)
- `.grouped` — Flush sections
- `.plain` — No section decoration
- `.sidebar` — macOS/iPad sidebar

### Swipe Actions
```swift
.swipeActions(edge: .trailing) {
    Button(role: .destructive) { delete(item) } label: {
        Label("Delete", systemImage: "trash")
    }
}
.swipeActions(edge: .leading) {
    Button { pin(item) } label: {
        Label("Pin", systemImage: "pin")
    }
    .tint(.yellow)
}
```

### Swipe & Reorder Outside `List` (iOS 27+)
`swipeActions` and drag-to-reorder now work in any container — stacks, grids, custom layouts. `List` coordinates swipes itself; other containers add `.swipeActionsContainer()` so only one row's actions open at a time.
```swift
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item)
                .swipeActions {
                    Button("Delete", role: .destructive) { delete(item) }
                }
        }
        .reorderable()
    }
    .reorderContainer(for: Item.self) { difference in
        apply(difference)
    }
}
.swipeActionsContainer()
```

Source: [HIG — Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

## Sheets & Alerts

### Alerts
```swift
.alert("Delete Item?", isPresented: $showAlert) {
    Button("Delete", role: .destructive) { deleteItem() }
    Button("Cancel", role: .cancel) { }
} message: {
    Text("This action cannot be undone.")
}
```

### Confirmation Dialogs
```swift
.confirmationDialog("Options", isPresented: $showOptions) {
    Button("Share") { share() }
    Button("Duplicate") { duplicate() }
    Button("Delete", role: .destructive) { delete() }
    Button("Cancel", role: .cancel) { }
}
```

### Sheets
```swift
.sheet(isPresented: $showSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
        .presentationCornerRadius(20)
}
```

Source: [HIG — Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts), [HIG — Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets), [HIG — Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

## Menus & Context Menus

### Context Menu
```swift
.contextMenu {
    Button("Copy", systemImage: "doc.on.doc") { copy() }
    Button("Share", systemImage: "square.and.arrow.up") { share() }
    Divider()
    Button("Delete", systemImage: "trash", role: .destructive) { delete() }
} preview: {
    PreviewView(item: item)  // Optional preview
}
```

### Pull-Down Menu
```swift
Menu("Options") {
    Button("Sort by Name", systemImage: "textformat") { sortByName() }
    Button("Sort by Date", systemImage: "calendar") { sortByDate() }
    Menu("Filter") {
        Button("All") { }
        Button("Recent") { }
    }
}
```

### Menu Item Icons (27)
Keyboard shortcuts for menu items: [hig-inputs.md](hig-inputs.md#keyboards).
- iPadOS and macOS **menu bars** hide item images by default in 27, keeping icons for key actions only
- Use icons sparingly and with purpose; give all items in a group icons, or none
- To force an icon: SwiftUI `.labelStyle(.titleAndIcon)` on the item's `Label`; UIKit `UIMenuElement.preferredImageVisibility`; AppKit `NSMenuItem.preferredImageVisibility`
- Menus in 27 can show a system **Ask Siri** item when there's content relevant to Siri
```swift
CommandMenu("Stickers") {
    Button { openStore() } label: {
        Label("Store", systemImage: "bag.fill")
            .labelStyle(.titleAndIcon)  // Keep this icon visible in the menu bar
    }
}
```

Source: [HIG — Menus](https://developer.apple.com/design/human-interface-guidelines/menus), [HIG — Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus), [HIG — Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

## Toolbars (iOS 26+ Liquid Glass)

### Toolbar Placements
| Placement | Location |
|-----------|----------|
| `.topBarLeading` | Top left |
| `.topBarTrailing` | Top right |
| `.topBarPinnedTrailing` | Top right, pinned — stays put as other items overflow (iOS 27+) |
| `.bottomBar` | Bottom floating bar |
| `.confirmationAction` | Primary action (auto `.glassProminent`) |
| `.cancellationAction` | Cancel/dismiss |
| `.principal` | Center of toolbar |

### Toolbar Implementation
```swift
.toolbar {
    ToolbarItem(placement: .topBarTrailing) {
        Button("Edit", systemImage: "pencil") { }
    }
    ToolbarItemGroup(placement: .bottomBar) {
        Button("Share", systemImage: "square.and.arrow.up") { }
        Button("Delete", systemImage: "trash") { }
    }
}
```

### iOS 26+ Toolbar Features
- Toolbars auto-apply Liquid Glass
- `.confirmationAction` gets `.glassProminent` automatically
- `ToolbarSpacer(.fixed, spacing: 20)` for grouping
- `.sharedBackgroundVisibility(.hidden)` to remove glass from specific items
- `.badge(5)` for notification counts

### iOS 27 Toolbar Additions
- `.visibilityPriority(.high)` on `ToolbarContent` keeps key actions visible as space shrinks; lower-priority items move to the overflow menu first
- `ToolbarOverflowMenu { }` sends secondary actions (archive, delete) straight to the overflow menu (iOS, iPadOS, visionOS)
- `.topBarPinnedTrailing` anchors an item; it overflows only when search is active and space runs out
- `.toolbarMinimizationBehavior(.onScrollDown, for: .navigationBar)` lets the navigation bar slide away on scroll; pair with `.toolbarMinimizationSafeAreaAdjustment(.disabled, for: .navigationBar)` only for full-bleed media
```swift
.toolbar {
    ToolbarItem { FilterButton() }
    ToolbarItem { ShareButton() }
        .visibilityPriority(.high)
    ToolbarItem(placement: .topBarPinnedTrailing) { ProfileButton() }
    ToolbarOverflowMenu {
        Button("Archive", systemImage: "archivebox") { archive() }
        Button("Delete", systemImage: "trash", role: .destructive) { delete() }
    }
}
```

Source: [HIG — Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars)

## Progress & Activity

```swift
// Indeterminate spinner
ProgressView()

// Determinate progress
ProgressView(value: progress, total: 100) {
    Text("Downloading...")
}

// Custom label
ProgressView("Loading...", value: 0.7)
```

Source: [HIG — Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators)

## Images & Media

```swift
// Async image loading
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .success(let image):
        image.resizable().aspectRatio(contentMode: .fill)
    case .failure:
        Image(systemName: "photo").foregroundStyle(.secondary)
    case .empty:
        ProgressView()
    @unknown default:
        EmptyView()
    }
}

// Always maintain aspect ratio (never distort)
Image("photo")
    .resizable()
    .aspectRatio(contentMode: .fit)  // or .fill with .clipped()
```

Source: [HIG — Image views](https://developer.apple.com/design/human-interface-guidelines/image-views)

## Empty States

Always show helpful content when there's no data:
```swift
ContentUnavailableView {
    Label("No Results", systemImage: "magnifyingglass")
} description: {
    Text("Try a different search term.")
} actions: {
    Button("Clear Search") { searchText = "" }
}
```

Source: [HIG — Writing](https://developer.apple.com/design/human-interface-guidelines/writing)
