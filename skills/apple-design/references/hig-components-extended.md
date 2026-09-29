# HIG Components — Extended

Component groups not covered in `hig-components.md`: presentation, layout and organization, content, and status. Core controls (buttons, text fields, pickers, segmented controls, lists, sheets, menus, toolbars) live in `hig-components.md`.

## Popovers

Transient view anchored to the control that opened it.
- Use for a small amount of information or functionality; keep it modest in size and animate size changes smoothly
- Anchor it to the control that opened it, and show only one at a time — never layer another view over it
- Let one tap/click close a popover and open another
- A Close button is only for confirmation or guidance; nonmodal popovers that close automatically must save work first
- Don't use a popover for warnings (use an alert), and don't say "popover" in help text
- **iOS/iPadOS**: avoid popovers in compact views (adapt them to a sheet, as below). **macOS**: consider letting people detach a popover into its own panel, with minimal visual change
```swift
Button("Filter", systemImage: "line.3.horizontal.decrease") { showFilter = true }
    .popover(isPresented: $showFilter, arrowEdge: .bottom) {
        FilterOptions()
            .presentationCompactAdaptation(.sheet)
    }
```

Source: [HIG — Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers)

## Windows

- Windows must resize fluidly for multitasking and multiwindow use
- Open new windows at the right moment and not excessively; consider offering to open content in a new window
- Avoid custom window chrome; say "window" in user-facing text
- **iPadOS**: keep toolbar items clear of the window controls; consider a gesture to open content in a new window (`UIWindowScene.ActivationInteraction`)
- **macOS**: custom windows still use system appearances; avoid bottom bars for critical info or actions — use them only for small status related to the window or selection
- **visionOS windows**: use them for familiar 2D tasks; keep the glass background; default size is **1280×720 pt** — choose an initial size and shape that fit the content with little empty space, and set minimum/maximum sizes; keep 3D content inside a window shallow
- **visionOS volumes**: use for rich 3D content; make 2D elements readable from multiple angles; generally use dynamic scaling; rely on the default baseplate to show edges; put high-value controls in an ornament

Source: [HIG — Windows](https://developer.apple.com/design/human-interface-guidelines/windows)

## Split Views

Adjacent panes (sidebar/content/detail). SwiftUI: `NavigationSplitView`; see `hig-patterns.md#split-view-ipadmac`.
- Keep the current selection highlighted in each pane that leads to the detail view; consider drag and drop between panes
- **iOS**: use in regular, not compact, environments. **iPadOS**: handle narrow, compact, and intermediate window widths
- **macOS**: set sensible min/max pane sizes; let people hide panes and offer more than one way to reveal them; prefer the thin divider
- **tvOS**: keep panes balanced; one title above the whole split view, aligned to suit the secondary pane's content
- **visionOS**: prefer a split view over a new window for supplementary info
- **watchOS**: open straight to the most relevant detail; put multiple detail pages in a vertical tab view

Source: [HIG — Split views](https://developer.apple.com/design/human-interface-guidelines/split-views)

## Scroll Views

- Support standard scroll gestures and keyboard shortcuts; make it apparent that content scrolls
- Never nest scroll views with the same orientation
- Consider paging when content suits it; auto-scroll when it helps people keep their place; set sensible min/max zoom if you support zoom
- **Scroll edge effects** (Liquid Glass): prefer the automatic style, use one only where content scrolls beneath floating UI, and apply at most one per view
- **iOS/iPadOS**: show a page control in paging mode, and don't show a scroll indicator on the same axis. **macOS**: small or mini scroll bars in panels, with all controls in the panel sized to match. **visionOS**: leave room for the scroll indicator; support Look to Scroll for reading/browsing views (not secondary content), define clear scroll areas, and drop custom scroll effects first. **watchOS**: prefer vertical scrolling; use tab views for paging, one screen height per page

Source: [HIG — Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views)

## Page Controls

Row of dots for a flat, ordered list of pages. Not available in macOS.
- Use only for sequential pages, not hierarchies; center it at the bottom of the view
- Keep page counts modest — more than about 10 dots are hard to count at a glance
- Custom indicator images: simple, no negative space, text, or inner lines; no more than two distinct images; don't color them; customize only when it adds meaning
- **iOS/iPadOS**: don't animate page transitions while scrubbing; don't support the scrubber with the minimal background style. **tvOS**: use for collections of full-screen pages. **watchOS**: vertical pagination into purposeful pages, each about one screen tall
```swift
TabView {
    ForEach(pages) { PageView(page: $0) }
}
.tabViewStyle(.page(indexDisplayMode: .always))
```

Source: [HIG — Page controls](https://developer.apple.com/design/human-interface-guidelines/page-controls)

## Disclosure Controls

Reveal and hide related information or functionality. Not in tvOS or watchOS.
- **Disclosure triangle** (`NSButton.BezelStyle.disclosure`): always give it a descriptive label
- **Disclosure button** (`.pushDisclosure`): place it next to the content it shows/hides; at most one per view
- **iOS, iPadOS, visionOS**: use SwiftUI `DisclosureGroup`
```swift
DisclosureGroup("Advanced Options", isExpanded: $showAdvanced) {
    Toggle("Beta features", isOn: $beta)
}
```

Source: [HIG — Disclosure controls](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls)

## Text Views

Multiline, styled, optionally editable text (SwiftUI `TextEditor`, UIKit `UITextView`).
- Use when text is long, editable, or specially formatted; use a text field for short single-line input
- Keep text legible (support Dynamic Type; see `hig-foundations.md#typography`) and make useful text selectable
- **iOS/iPadOS**: show the keyboard type that fits the content. **tvOS**: use text fields for editable text instead

Source: [HIG — Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)

## Web Views

Embedded web content inside your app (`WKWebView`; SwiftUI `WebView` on 26+). Not in tvOS or watchOS.
- Support back and forward navigation when people can follow links
- Don't build a general-purpose web browser out of a web view

Source: [HIG — Web views](https://developer.apple.com/design/human-interface-guidelines/web-views)

## Charts

Swift Charts components; for when and what to chart, see `hig-patterns.md#charting-data`.
- **Marks**: pick the mark type (bar, line, point, area…) for what the data needs to say; combine marks only when it adds clarity
- **Axes**: choose fixed vs. dynamic range by meaning; set the lower bound to suit the mark type and use; use familiar tick sequences; tailor grid lines/labels to the use case
- **Description**: say what the chart shows before people look, and summarize its main message
- Keep a clear visual hierarchy; in compact layouts give the plot area maximum width; align the chart with surrounding UI
- Interaction is optional — never hide critical information behind it; support keyboard (including Full Keyboard Access) and Switch Control; help people notice important changes
- **Color**: never the only differentiator; separate adjacent color areas visually
- **Accessibility**: consider Audio Graphs for VoiceOver, write labels that serve the chart's purpose, and hide visible axis/tick text from assistive tech to avoid duplication
- **watchOS**: avoid complex chart interactions

Source: [HIG — Charts](https://developer.apple.com/design/human-interface-guidelines/charts)

## Gauges

Show a value within a range (SwiftUI `Gauge`, AppKit `NSLevelIndicator`).
- Label the current value and both ends of the range succinctly
- A gradient fill can help communicate what the gauge measures
- **macOS**: use the continuous level-indicator style for large ranges; change fill color to flag significant parts of the range
```swift
Gauge(value: temp, in: 0...40) {
    Text("Temperature")
} currentValueLabel: {
    Text("\(Int(temp))°")
} minimumValueLabel: { Text("0") } maximumValueLabel: { Text("40") }
.gaugeStyle(.accessoryCircular)
```

Source: [HIG — Gauges](https://developer.apple.com/design/human-interface-guidelines/gauges)

## Rating Indicators

macOS only (`NSLevelIndicator.Style.rating`): a row of symbols, stars by default, showing a rank.
- Make ratings easy to change, inline, without a separate editing screen
- If you swap the star for a custom symbol, make its meaning obvious
- In right-to-left layouts, rating controls run from the right (see `hig-foundations.md#right-to-left`)

Source: [HIG — Rating indicators](https://developer.apple.com/design/human-interface-guidelines/rating-indicators)
