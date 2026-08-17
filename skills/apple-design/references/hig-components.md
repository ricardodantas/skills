# HIG Components

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

## Forms & Input

### Text Input
```swift
TextField("Name", text: $name)
    .textContentType(.name)           // Autofill support
    .autocorrectionDisabled()
    .textInputAutocapitalization(.words)

SecureField("Password", text: $password)
    .textContentType(.password)
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

## Toolbars (iOS 26 Liquid Glass)

### Toolbar Placements
| Placement | Location |
|-----------|----------|
| `.topBarLeading` | Top left |
| `.topBarTrailing` | Top right |
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

### iOS 26 Toolbar Features
- Toolbars auto-apply Liquid Glass
- `.confirmationAction` gets `.glassProminent` automatically
- `ToolbarSpacer(.fixed, spacing: 20)` for grouping
- `.sharedBackgroundVisibility(.hidden)` to remove glass from specific items
- `.badge(5)` for notification counts

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
