# App Store Images

Generate marketing images for App Store Connect using **Node.js + sharp**.

## Required Sizes

| Platform | Dimensions | Device |
|----------|-----------|--------|
| iPhone 6.9" | 1320×2868 | iPhone 16 Pro Max |
| iPhone 6.7" | 1290×2796 | iPhone 15 Plus (optional) |
| iPad 13" | 2064×2752 | iPad Pro 13" M4 |
| Mac | 2880×1800 | MacBook Pro |

Apple requires 5-10 screenshots per device. Aim for 5-6.

## Design Language

Each image: dark background + accent glow gradients + bold 2-line headline + subtitle + device frame with screenshot bleeding off bottom.

```
┌──────────────────────────┐
│                          │
│      Line 1 (white)      │
│      Line 2 (accent)     │
│    Subtitle (45% white)  │
│                          │
│    ┌──────────────────┐  │
│    │  ┌────────────┐  │  │
│    │  │ DynIsland  │  │  │
│    │  │            │  │  │
│    │  │ Screenshot │  │  │
│    │  │            │  │  │
│    │  │            │  │  │
│    │  │    ...     │  │  │
└────┴──┴────────────┴──┴──┘
     frame  screenshot bleeds off
```

### Color Scheme Per App

Configure three values:
- `BG` — Dark background (e.g., `#0c0a06`)
- `ACCENT` — Brand color for headline line 2 + glow (e.g., `#FF9500`)
- `ACCENT_WARM` — Darker variant for bottom glow (e.g., `#E08600`)

## Script Usage

The reusable generator script is at `scripts/generate-appstore-images.js`.

Copy it to your app's `app_store_images/` folder, install sharp, and configure:

```bash
mkdir -p app_store_images && cd app_store_images
npm init -y && npm install sharp
cp <skill-dir>/scripts/generate-appstore-images.js .
```

Edit the config section at the top:
- `PLATFORM`: `'iphone'`, `'ipad'`, or `'mac'`
- `BG`, `ACCENT`, `ACCENT_WARM`: brand colors
- `SCREENSHOTS_DIR`: path to simulator screenshots
- `slides[]`: array of `{ file, line1, line2, accentLine, sub, out }`

Run: `node generate-appstore-images.js`

Or create 3 separate scripts (recommended): `generate-iphone.js`, `generate-ipad.js`, `generate-mac.js`.

## Device Frame Specs

### iPhone Frame
- `framePadding`: 14px (bezel thickness)
- `outerRadius`: 72px
- `innerRadius`: 58px
- Bezel fill: `#1c1c1e`
- Subtle stroke: `rgba(255,255,255,0.06)` 1px

### iPad Frame
- `framePadding`: 16px
- `outerRadius`: 40px
- `innerRadius`: 24px
- Same bezel + stroke
- No Dynamic Island

### Mac (no frame)
- Just rounded corners (14px radius) on screenshot
- No bezel frame — screenshot placed directly on background

## Dynamic Island (iPhone Only)

**Critical**: iOS Simulator does NOT render the hardware Dynamic Island cutout. Draw it as an SVG overlay ON TOP of the screenshot.

Real iPhone 16 Pro dimensions:
- Width: 31.3% of screen width (126pt on 402pt screen)
- Height: width × 0.286 (ratio 3.5:1, = 36pt)
- Corner radius: half the height (perfect pill)
- Fill: `#020202` (near-black, not pure black)
- Position: `framePadding + scaledH × 0.0075` from top of frame

```javascript
const diW = Math.round(scaledW * 0.313);
const diH = Math.round(diW * 0.286);
const diR = Math.round(diH / 2);
const diX = Math.round((frameW - diW) / 2);
const diY = framePadding + Math.round(scaledH * 0.0075);
```

**Lessons learned**:
- Ratios of 8:1 or 10:1 look too thin — must be 3.5:1
- Must composite AFTER screenshot (not draw in frame SVG underneath)
- Fill `#020202` looks more natural than `#000000` or `#111111`

## Shadow

Add drop shadow behind device frame for depth:

```javascript
const shadowPad = 60;
const shadowBuf = await sharp({
  create: { width: frameW + shadowPad * 2, height: visibleFrameH + shadowPad * 2,
            channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } }
}).composite([{
  input: await sharp({
    create: { width: frameW, height: visibleFrameH, channels: 4,
              background: { r: 0, g: 0, b: 0, alpha: 150 } }
  }).png().toBuffer(),
  top: shadowPad + 12, left: shadowPad,
}]).blur(40).png().toBuffer();
```

### iPad Shadow Clamping

iPad frames nearly fill the canvas width. Clamp shadow dimensions to canvas to avoid sharp's "Image to composite must have same dimensions or smaller" error:

```javascript
const shadowTotalW = Math.min(frameW + shadowPad * 2, CANVAS_W);
const shadowTotalH = Math.min(visibleFrameH + shadowPad * 2, CANVAS_H);
```

## Headline Text

SVG text overlay composited at top of canvas:
- Font: `system-ui, -apple-system, sans-serif`
- Line 1: 82px (iPhone) / 86px (iPad) / 88px (Mac), weight 700
- Line 2: same size, in accent color
- Subtitle: 36-38px, weight 500, `rgba(255,255,255,0.45)`
- `letter-spacing: -2`

## Slide Configuration

```javascript
const slides = [
  {
    file: 'Screenshot 2026-02-27 at 11.50.48.png',  // Comment: what screen
    line1: 'Your Voice,',
    line2: 'Organized.',
    accentLine: 2,        // Which line gets accent color (1 or 2)
    sub: 'Subtitle text goes here.',
    out: '01-library.png', // Output filename (numbered for ordering)
  },
];
```

**Always comment which screen each file shows** — prevents screenshot mismatches.

## Screenshot Tips

- Use iOS Simulator for consistent screenshots (no notifications, clean status bar)
- iPhone 17 Pro Max = 1320×2868 (same as 6.9" requirement)
- iPad Pro 13" M5 = 2064×2752 (exact match)
- Use portrait orientation only (landscape won't fit the template)
- Populate with debug data seeder before taking screenshots
- macOS screenshots vary in size — the script scales them to fit
