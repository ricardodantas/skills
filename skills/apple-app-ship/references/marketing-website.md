# Marketing Website

Build a dark, premium marketing site using **Astro + Tailwind CSS**.

## Stack

- Astro v5+ (static site generator)
- Tailwind CSS v3+ (dark theme)
- Fonts: Cabinet Grotesk (display) + DM Sans (body) or similar
- Deploy: Bunny.net CDN, Vercel, Netlify, or GitHub Pages

## Project Structure

```
app-website/
├── src/
│   ├── components/
│   │   ├── Header.astro      # Nav: logo + links + CTA badge
│   │   └── Footer.astro      # Columns: Product, Legal, Social
│   ├── layouts/
│   │   └── Layout.astro      # HTML head, meta, JSON-LD, Smart App Banner
│   ├── pages/
│   │   ├── index.astro       # Landing page
│   │   ├── privacy.astro     # Privacy policy
│   │   ├── terms.astro       # Terms of service
│   │   ├── support.astro     # FAQ with collapsible <details> + FAQ schema
│   │   └── 404.astro         # Custom 404
│   ├── styles/
│   │   └── global.css        # Tailwind imports + custom styles
│   └── config.ts             # App constants (urls, app store id, flags)
├── public/
│   ├── mockups/              # Device screenshots (webp preferred)
│   ├── _headers              # Security headers + cache rules
│   ├── llms.txt              # LLM-friendly app description
│   ├── robots.txt
│   └── favicon.svg
├── AGENTS.md                 # Agent instructions
├── README.md
└── astro.config.mjs
```

## Required Pages (5)

### 1. Landing (`index.astro`)
- Hero: headline + App Store badge + device mockup
- Features: 3-4 sections with device screenshots in CSS frames
- Platform grid: icons for each supported platform
- Pricing: "Pay Once. Own It Forever." section (one-time purchase)
- CTA: final App Store badge

### 2. Privacy (`privacy.astro`)
- "Data Not Collected" if applicable
- Clear sections: data collection, analytics, third-party, contact

### 3. Terms (`terms.astro`)
- Standard terms for paid app (no subscription)
- Sections: license, purchases, limitations, changes, contact

### 4. Support (`support.astro`)
- Collapsible FAQ using `<details><summary>` elements
- FAQ Schema (`@type: FAQPage`) structured data for SEO
- Contact email link

### 5. 404 (`404.astro`)
- Branded error page with link home

## CSS Device Frames

Pure CSS device frames for screenshots — no images needed:

```css
/* iPhone frame */
.device-iphone {
  position: relative;
  background: #1c1c1e;
  border-radius: 3rem;
  padding: 0.75rem;
  box-shadow: 0 25px 60px rgba(0,0,0,0.4);
}
.device-iphone > div {
  border-radius: 2.25rem;
  overflow: hidden;
}
/* Dynamic Island */
.device-iphone::after {
  content: '';
  position: absolute;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  width: 90px;
  height: 24px;
  background: #1c1c1e;
  border-radius: 12px;
  z-index: 10;
}

/* iPad frame */
.device-ipad {
  background: #1c1c1e;
  border-radius: 1.25rem;
  padding: 0.5rem;
  box-shadow: 0 25px 50px rgba(0,0,0,0.35);
}
.device-ipad > div {
  border-radius: 0.75rem;
  overflow: hidden;
}

/* MacBook frame */
.device-macbook {
  background: #2c2c2e;
  border-radius: 0.75rem;
  padding: 0.25rem 0.25rem 0;
  box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}
.device-macbook > div {
  border-radius: 0.5rem 0.5rem 0 0;
  overflow: hidden;
}
```

## SEO Essentials

In `Layout.astro`:
- `<meta name="apple-itunes-app" content="app-id=YOUR_APP_ID">` (Smart App Banner)
- Open Graph tags (title, description, image, url)
- Twitter cards
- JSON-LD structured data (`@type: SoftwareApplication`)
- Canonical URLs
- Sitemap via `@astrojs/sitemap`

## `config.ts` Pattern

```typescript
export const SITE_URL = 'https://yourapp.com';
export const APP_STORE_URL = 'https://apps.apple.com/app/yourapp/idXXXXXXXXXX';
export const APP_STORE_ID = 'XXXXXXXXXX';
export const SUPPORT_EMAIL = 'hello@yourapp.com';
export const COMING_SOON = false; // Toggle pre-launch mode
export const APP_PRICE = '$9.99';
```

## `_headers` (CDN Security)

```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/mockups/*
  Cache-Control: public, max-age=31536000, immutable

/_astro/*
  Cache-Control: public, max-age=31536000, immutable
```

## `llms.txt`

Plain text file describing the app for LLMs. Include: name, tagline, key features, platforms, price, links.
