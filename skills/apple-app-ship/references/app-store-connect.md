# App Store Connect Submission

## App Store Metadata

### Required Fields

| Field | Notes |
|-------|-------|
| App Name | 30 chars max |
| Subtitle | 30 chars max — key value prop |
| Description | Up to 4000 chars. First 3 lines visible without "more" |
| Keywords | 100 chars, comma-separated. No spaces after commas |
| Category | Primary + Secondary |
| Content Rating | Auto-generated from questionnaire |
| Copyright | © 2026 Your Name |
| Support URL | yourapp.com/support |
| Marketing URL | yourapp.com |
| Privacy Policy URL | yourapp.com/privacy |

### Description Template

```
[One-liner value prop — what the app does and why it's great.]

[2-3 sentences expanding on the core experience.]

KEY FEATURES
• Feature 1 — brief description
• Feature 2 — brief description
• Feature 3 — brief description
• Feature 4 — brief description
• Feature 5 — brief description

AVAILABLE ON
• iPhone & iPad
• Mac (Apple Silicon)
• Apple Watch
• Apple TV

[Closing line — brand promise or differentiator.]

Pay once. Own it forever. No subscriptions. No ads. No tracking.
```

### Keywords Strategy

- Use all 100 characters
- No spaces after commas (wastes chars)
- Don't repeat words from app name/subtitle
- Include competitor names (controversial but common)
- Include misspellings/synonyms users might search
- Singular forms (Apple indexes plurals automatically)

## Privacy Labels

For apps that collect NO data:
- Select "Data Not Collected" for all categories
- Privacy Policy URL still required

For apps with analytics:
- Declare exactly what's collected
- "Data Not Linked to You" if no account system

## App Review Notes

Template:
```
This app does not require an account or login.
[Briefly explain any non-obvious features.]
[If using health data, camera, microphone, etc., explain why.]
No in-app purchases. One-time purchase only.
```

## Pricing

For one-time purchase apps:
- Set price tier in App Store Connect → Pricing and Availability
- Common indie price: $4.99–$14.99
- Use "Universal Purchase" for single purchase across all platforms
- Set availability for all desired countries

## Review Checklist

- [ ] All screenshots uploaded (5-10 per device size)
- [ ] App previews (optional video, 15-30s)
- [ ] Description finalized
- [ ] Keywords optimized (100 chars used)
- [ ] Privacy policy URL working
- [ ] Support URL working
- [ ] Age rating questionnaire completed
- [ ] Build uploaded via Xcode → Archive → Upload
- [ ] TestFlight testing completed
- [ ] "What's New" text (for updates)

## Common Rejection Reasons

1. **Guideline 2.1 — Performance**: App crashes or has major bugs
2. **Guideline 2.3 — Metadata**: Screenshots don't match app, misleading description
3. **Guideline 5.1.1 — Privacy**: Missing privacy policy or usage descriptions
4. **Guideline 4.0 — Design**: Non-native UI, web wrapper, or broken layouts
5. **Guideline 3.1.1 — Payments**: Using non-Apple payment for digital goods

## Build & Upload

```bash
# In Xcode:
# 1. Product → Archive
# 2. Window → Organizer → Distribute App
# 3. App Store Connect → Upload
# 4. Wait for processing (5-30 min)
# 5. Select build in App Store Connect → TestFlight or Submit
```

## Post-Launch

- Monitor Crash Reports in Xcode Organizer
- Respond to App Store reviews
- Track downloads in App Store Connect → Analytics
- Plan updates based on user feedback
