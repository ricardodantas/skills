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
```

#### Split View (iPad/Mac)
- `NavigationSplitView` for sidebar + content + detail
- Sidebar auto-gets Liquid Glass styling (iOS 26)
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

### Sheet Best Practices (iOS 26)
- Use `.presentationDetents([.medium, .large])` for resizable sheets
- iOS 26 auto-applies Liquid Glass — don't set custom backgrounds
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

## Search

### Search Implementation
```swift
NavigationStack {
    ContentView()
}
.searchable(text: $searchText, prompt: "Search items")
```

### Search Best Practices
- Place search in toolbar (auto Liquid Glass on iOS 26)
- Show suggestions with `.searchSuggestions { }`
- Support search scopes for filtering: `.searchScopes($scope) { }`
- Use `.searchToolbarBehavior(.minimized)` for secondary search
- iOS 26: Use `Tab("Search", ..., role: .search)` for floating search in TabView
- Show recent searches and suggestions
- Debounce network searches (300-500ms)

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

## Onboarding

### Best Practices
- Keep it short: 3-5 screens maximum
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
