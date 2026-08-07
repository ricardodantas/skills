#!/usr/bin/env node
/**
 * App Store Marketing Image Generator
 *
 * Generates App Store screenshots with device frames, headlines, and shadows.
 * Supports iPhone (with Dynamic Island), iPad, and Mac.
 *
 * Usage:
 *   1. Copy this script to your app's app_store_images/ directory
 *   2. Install sharp: npm init -y && npm install sharp
 *   3. Edit the CONFIG section below
 *   4. Run: node generate-appstore-images.js
 *
 * Or create platform-specific copies:
 *   generate-iphone.js, generate-ipad.js, generate-mac.js
 */

const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

// ============================================================
// CONFIG — Edit this section for your app
// ============================================================

const PLATFORM = 'iphone'; // 'iphone' | 'ipad' | 'mac'

// Canvas dimensions per platform
const CANVAS = {
  iphone: { w: 1320, h: 2868 },
  ipad:   { w: 2064, h: 2752 },
  mac:    { w: 2880, h: 1800 },
};

// Brand colors
const BG = '#0c0a06';           // Dark background
const ACCENT = '#FF9500';        // Primary accent (headline line 2 + glow)
const ACCENT_WARM = '#E08600';   // Secondary accent (bottom glow)

// Paths
const SCREENSHOTS_DIR = path.resolve(__dirname, '../screenshots/ios/6.9'); // Adjust per platform
const OUT_DIR = path.resolve(__dirname, PLATFORM);
fs.mkdirSync(OUT_DIR, { recursive: true });

// Slides — one per output image
const slides = [
  {
    file: 'screenshot-filename.png',  // Source screenshot filename
    line1: 'Headline',
    line2: 'Line Two',
    accentLine: 2,                    // 1 or 2 — which line gets accent color
    sub: 'Subtitle line one.\nOptional second line.',
    out: '01-name.png',               // Output filename (numbered for order)
  },
  // Add more slides...
];

// ============================================================
// GENERATOR — Usually no edits needed below
// ============================================================

const { w: CANVAS_W, h: CANVAS_H } = CANVAS[PLATFORM];

// Device frame parameters
const FRAME = {
  iphone: { padding: 14, outerR: 72, innerR: 58 },
  ipad:   { padding: 16, outerR: 40, innerR: 24 },
  mac:    { padding: 0,  outerR: 14, innerR: 14 },
};

// Layout
const LAYOUT = {
  iphone: { margin: 200, frameY: 430, textH: 420, textTop: 40, fontSize: 82, subSize: 36 },
  ipad:   { margin: 120, frameY: 370, textH: 340, textTop: 30, fontSize: 86, subSize: 38 },
  mac:    { margin: 100, frameY: 330, textH: 300, textTop: 30, fontSize: 88, subSize: 36 },
};

const frame = FRAME[PLATFORM];
const layout = LAYOUT[PLATFORM];

function createBgSvg() {
  return `<svg width="${CANVAS_W}" height="${CANVAS_H}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="g1" cx="50%" cy="12%" r="50%">
        <stop offset="0%" stop-color="${ACCENT}" stop-opacity="0.12"/>
        <stop offset="100%" stop-color="${ACCENT}" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="g2" cx="50%" cy="88%" r="45%">
        <stop offset="0%" stop-color="${ACCENT_WARM}" stop-opacity="0.07"/>
        <stop offset="100%" stop-color="${ACCENT_WARM}" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <rect width="${CANVAS_W}" height="${CANVAS_H}" fill="${BG}"/>
    <rect width="${CANVAS_W}" height="${CANVAS_H}" fill="url(#g1)"/>
    <rect width="${CANVAS_W}" height="${CANVAS_H}" fill="url(#g2)"/>
  </svg>`;
}

function createTextSvg(slide) {
  const w = CANVAS_W;
  const line1Fill = slide.accentLine === 1 ? ACCENT : 'white';
  const line2Fill = slide.accentLine === 2 ? ACCENT : 'white';
  const subLines = (slide.sub || '').split('\n');
  const fs1 = layout.fontSize;

  let subTspans = `<tspan x="${w/2}" y="${fs1 * 2 + 70}">${subLines[0]}</tspan>`;
  if (subLines[1]) subTspans += `<tspan x="${w/2}" dy="48">${subLines[1]}</tspan>`;

  return `<svg width="${w}" height="${layout.textH}" xmlns="http://www.w3.org/2000/svg">
    <text x="${w/2}" y="${fs1 + 28}" text-anchor="middle"
      font-family="system-ui, -apple-system, sans-serif" font-size="${fs1}" font-weight="700"
      letter-spacing="-2" fill="${line1Fill}">${slide.line1}</text>
    <text x="${w/2}" y="${fs1 * 2 + 28}" text-anchor="middle"
      font-family="system-ui, -apple-system, sans-serif" font-size="${fs1}" font-weight="700"
      letter-spacing="-2" fill="${line2Fill}">${slide.line2}</text>
    <text text-anchor="middle"
      font-family="system-ui, -apple-system, sans-serif" font-size="${layout.subSize}" font-weight="500"
      fill="rgba(255,255,255,0.45)">${subTspans}</text>
  </svg>`;
}

async function generateSlide(slide) {
  const srcPath = path.join(SCREENSHOTS_DIR, slide.file);
  const meta = await sharp(srcPath).metadata();

  const maxImgW = CANVAS_W - layout.margin;
  const scale = maxImgW / meta.width;
  const scaledW = Math.round(meta.width * scale);
  const scaledH = Math.round(meta.height * scale);

  // Round screenshot corners
  const roundedMask = Buffer.from(
    `<svg width="${scaledW}" height="${scaledH}"><rect width="${scaledW}" height="${scaledH}" rx="${frame.innerR}" ry="${frame.innerR}" fill="white"/></svg>`
  );
  const screenshot = await sharp(srcPath)
    .resize(scaledW, scaledH, { fit: 'fill' })
    .composite([{ input: roundedMask, blend: 'dest-in' }])
    .png()
    .toBuffer();

  let compositeImage;

  if (PLATFORM === 'mac') {
    // Mac: no bezel frame, just rounded screenshot
    compositeImage = screenshot;
    var imgW = scaledW;
    var imgH = scaledH;
  } else {
    // iPhone/iPad: device frame bezel
    const frameW = scaledW + frame.padding * 2;
    const frameH = scaledH + frame.padding * 2;

    const frameSvg = `<svg width="${frameW}" height="${frameH}" xmlns="http://www.w3.org/2000/svg">
      <rect width="${frameW}" height="${frameH}" rx="${frame.outerR}" ry="${frame.outerR}" fill="#1c1c1e"/>
      <rect x="0.5" y="0.5" width="${frameW-1}" height="${frameH-1}" rx="${frame.outerR}" ry="${frame.outerR}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="1"/>
    </svg>`;

    let frameImg = await sharp(Buffer.from(frameSvg))
      .composite([{ input: screenshot, top: frame.padding, left: frame.padding }])
      .png()
      .toBuffer();

    // Dynamic Island (iPhone only)
    if (PLATFORM === 'iphone') {
      const diW = Math.round(scaledW * 0.313);
      const diH = Math.round(diW * 0.286);
      const diR = Math.round(diH / 2);
      const diX = Math.round((frameW - diW) / 2);
      const diY = frame.padding + Math.round(scaledH * 0.0075);
      const diSvg = `<svg width="${frameW}" height="${frameH}" xmlns="http://www.w3.org/2000/svg">
        <rect x="${diX}" y="${diY}" width="${diW}" height="${diH}" rx="${diR}" ry="${diR}" fill="#020202"/>
      </svg>`;
      frameImg = await sharp(frameImg)
        .composite([{ input: Buffer.from(diSvg), blend: 'over' }])
        .png()
        .toBuffer();
    }

    compositeImage = frameImg;
    var imgW = frameW;
    var imgH = frameH;
  }

  const imgX = Math.max(0, Math.round((CANVAS_W - imgW) / 2));
  const frameY = layout.frameY;
  const visibleH = Math.min(imgH, CANVAS_H - frameY);
  const visibleW = Math.min(imgW, CANVAS_W);
  const clipped = await sharp(compositeImage)
    .extract({ left: 0, top: 0, width: visibleW, height: visibleH })
    .png()
    .toBuffer();

  // Shadow
  const shadowPad = PLATFORM === 'mac' ? 50 : 60;
  const shadowTotalW = Math.min(imgW + shadowPad * 2, CANVAS_W);
  const shadowTotalH = Math.min(visibleH + shadowPad * 2, CANVAS_H);
  const shadowInnerW = Math.min(imgW, shadowTotalW - 4);
  const shadowInnerH = Math.min(visibleH, shadowTotalH - 14);
  const shadowBuf = await sharp({
    create: { width: shadowTotalW, height: shadowTotalH, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } }
  })
    .composite([{
      input: await sharp({ create: { width: shadowInnerW, height: shadowInnerH, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 150 } } }).png().toBuffer(),
      top: Math.round((shadowTotalH - shadowInnerH) / 2) + (PLATFORM === 'mac' ? 10 : 12),
      left: Math.round((shadowTotalW - shadowInnerW) / 2),
    }])
    .blur(PLATFORM === 'mac' ? 35 : 40)
    .png()
    .toBuffer();

  const shadowX = Math.max(0, imgX - Math.round((shadowTotalW - imgW) / 2));
  const shadowY = Math.max(0, frameY - Math.round((shadowTotalH - visibleH) / 2));

  await sharp(Buffer.from(createBgSvg()))
    .resize(CANVAS_W, CANVAS_H)
    .composite([
      { input: Buffer.from(createTextSvg(slide)), top: layout.textTop, left: 0 },
      { input: shadowBuf, top: shadowY, left: shadowX },
      { input: clipped, top: frameY, left: imgX },
    ])
    .png()
    .toFile(path.join(OUT_DIR, slide.out));

  const outMeta = await sharp(path.join(OUT_DIR, slide.out)).metadata();
  console.log(`✓ ${slide.out} — ${outMeta.width}×${outMeta.height}`);
}

(async () => {
  console.log(`Generating ${PLATFORM} App Store images (${CANVAS_W}×${CANVAS_H})...\n`);
  for (const s of slides) await generateSlide(s);
  console.log(`\nDone! ${slides.length} images in ${OUT_DIR}`);
})().catch(e => { console.error(e); process.exit(1); });
