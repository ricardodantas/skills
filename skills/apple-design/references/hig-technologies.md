# HIG Technologies

Design rules for Apple technologies you integrate: brand-asset usage, required flows, and
platform limits. Paraphrased from the HIG; follow each Source link for artwork and full detail.

## Sign in with Apple
- Ask people to sign in only when it gives them something, and as late as possible. Let them explore first
- If an account is required, explain why and have them set it up before you show any sign-in options
- In commerce, offer account creation after purchase (e.g., on the order confirmation page). Don't re-ask for a name or email Apple Pay already supplied
- Offer to link an existing account (e.g., when the shared email matches). Show the current method somewhere, like "Using Sign in with Apple" in account settings
- Data: say which extra fields are required and which are optional. Never ask for a password. Don't ask for a personal email when someone chose a private relay address
- **Button prominence:** make it no smaller than other sign-in buttons, and don't make people scroll to reach it
- **System button** (`ASAuthorizationAppleIDButton`; `WKInterfaceAuthorizationAppleIDButton` on watchOS): Apple-approved look, auto-localized title, VoiceOver label, and adjustable corner radius (iOS, macOS, web)
  - Titles: *Sign in with Apple* / *Sign up with Apple* / *Continue with Apple*. watchOS has only *Sign in*. Pick one and use it consistently
  - Styles: **white** goes on dark backgrounds; **white with outline** (iOS, macOS, web) goes on white or light backgrounds, never on dark or saturated ones; **black** goes on light backgrounds, never on dark ones. The watchOS button uses a dark-gray fill, not pure black
  - Corner radius can range from square to capsule. Match your other buttons
  - Minimum size: **140 pt wide × 30 pt tall**. Keep a clear margin of **≥ 1/10 of the button height** around it
- **Custom buttons** (iOS, macOS, web; App Review checks every one):
  - Use only the Apple logo artwork from Apple Design Resources. Never draw your own Apple logo, and never use the logo alone as the button
  - Match the logo file's height to the button's height. Don't crop it or add vertical padding
  - Fixed: the three titles above; logo and title both black or both white; a logo-plus-text button is always a rectangle, while a logo-only button can be a circle or rectangle
  - Adjustable: title font, weight and size; all-caps; background (black or white, with at most a subtle texture or gradient); corner radius; bezel and shadow
  - Logo + text: the title's font size is about 43% of the button height (e.g., 44 pt button with a 19 pt font, 56 pt with 24 pt). Center the title vertically. Keep at least 8% of the button width as margin after the title. PNG artwork works only at a 44 pt height; use SVG or PDF for other sizes
  - Logo-only: always 1:1. Don't add horizontal padding. Use a mask for circle or rounded-rect shapes. PNG only at 44×44 pt. Keep a margin of ≥ 1/10 of the height

Source: [HIG — Sign in with Apple](https://developer.apple.com/design/human-interface-guidelines/sign-in-with-apple)

## Apple Pay
- Offer Apple Pay wherever the device or browser supports it. Hide it where it isn't supported. Not supported in tvOS
- If you check for an active Wallet card, Apple Pay **must** be the primary option (not necessarily the only one) everywhere you run that check. Don't put it in a separate step
- Use Apple Pay buttons only to start a payment, or to start Apple Pay setup. Never hide a button or make it look disabled. If a selection (size, color) is missing, point that out after the tap
- A custom payment button must not show "Apple Pay" or the Apple Pay logo. Put the **Apple Pay mark** or text elsewhere on the page instead. The mark means only "accepted here". Never use it as a button
- **Checkout flow:** keep your branding and don't open new pages or windows. Put Apple Pay first, make it larger, or set it apart with a divider. Buy buttons on product pages buy that one item and ignore the cart; express checkout covers the whole cart
  - Collect options, optional extras (gift notes) and split shipping before the sheet, which can't take optional input. Prefer Apple Pay's contact and shipping data. Offer account creation on the confirmation page, prefilled, never before purchase
  - Report the result in the sheet, then show a thank-you page. If you name Apple Pay there, write "1234 (Apple Pay)" or "Paid with Apple Pay"
- **Payment sheet:** request only essential fields (no shipping address for a digital gift card). Show the applied promo code or allow entry on the sheet. Line items cover charges, discounts, pending amounts, donations and recurring payments, one line each, never the product list
  - The total reads "Pay [Business Name]" (the name on the card statement), or "Pay [End Merchant (via You)]" for an intermediary. Mark amounts that may change as Amount Pending where local rules allow. Add no spinners of your own
- **Errors:** accept flexible input (ZIP+4, phone numbers with or without dashes). Return the right status code with a specific, field-level message: a noun phrase in sentence case, no ending punctuation, ≤ 128 characters. On cancel or timeout, cancel the in-progress payment
- **Subscriptions:** explain the terms before the sheet appears. Line items repeat the billing frequency, discounts, fees, trial amount ($0 if free), the regular price, and the date billing starts. Show the sheet on a plan change only if the price goes up
- **Donations** (approved nonprofits only): add a donation line item and preset amounts plus an Other Amount option
- **Buttons:** always create them with the API (`PKPaymentButton` type and style; `WKInterfacePaymentButton`). Never draw or copy a custom one
  - Types: Buy, Pay, Check Out, Continue, Book, Donate, Subscribe, Reload, Add Money, Top Up, Order, Rent, Support, Contribute, Tip, a plain Apple Pay button, and Set Up Apple Pay (for Settings, profile, or interstitial screens)
  - Styles: *automatic* follows the system appearance. **Black** goes on light backgrounds, not dark ones. **White with outline** goes on light backgrounds without enough contrast, not on dark or saturated ones. **White** goes on dark backgrounds
  - Make it no smaller than other payment buttons and visible without scrolling. Put it **right of** Add to Cart when side by side, and **above** it when stacked. Corner radius can range from square to capsule
  - Minimum size: plain Apple Pay **100×30 pt**. Book, Buy, Check Out, Donate, Set Up and Subscribe need **140×30 pt**. Margins must be ≥ **1/10 of the button height**
- **Mark:** use Apple's artwork. You may change only its height, and it must be ≥ other payment marks. Don't change width, radius or aspect ratio, and don't remove the border, add effects, or flip, rotate or animate it. Keep clear space of ≥ 1/10 of its height
- **Website icon:** 60×60 pt (120 px @2x, 180 px @3x). It appears during authorization, e.g. Handoff
- **In text:** write "Apple Pay": two words, capital A and P. Never plural or possessive, never translated, never the Apple logo in place of "Apple". In the US, add ® on the first mention in body text, but not in checkout options. Use your own font, not Apple's typography. Show text-only Apple Pay only when every other payment option is text-only too

Source: [HIG — Apple Pay](https://developer.apple.com/design/human-interface-guidelines/apple-pay)

## Apple In-App Purchase
Formerly "In-App Purchase"; renamed in the HIG in September 2026. Types: consumable, non-consumable, auto-renewable subscription, and non-renewing subscription.
- Let people experience the app before asking them to pay. Style the store to match your app
- Use short product names that don't truncate. Show the **total billing price** for every item
- Hide the store, or explain why it's unavailable, when `canMakePayments` is false (e.g., parental restrictions)
- **Never modify or copy the system confirmation sheet**
- Family Sharing: say so where people browse ("Family" or "Shareable" in the name). Write copy that works for both the purchaser and family members
- Refund help: offer a custom help screen (missing purchase, FAQ, contact) and keep the refund action visible without scrolling. Call it "Refund" or "Request a Refund", which opens `beginRefundRequest`. Show product image, name and purchase date. Don't guess at Apple's refund policy
- **Subscriptions:** show the value in onboarding with a clear call to action and terms. Offer several levels and durations; free access (freemium, metered, trial) helps. Prompt at relevant moments and never prompt existing subscribers. Add a sign-in option for purchases made elsewhere, and a subscribe entry in Settings
  - The sign-up screen must include: name, duration, what each period provides, the localized billing amount, and sign-in or restore, plus Terms and Privacy Policy links. Intro offers list the intro price, its duration and the standard price after. Say the trial ends in an automatic charge and give the amount. tvOS: sign up on another device
- **Offer codes** (iOS/iPadOS): one-time codes or custom codes. Custom codes are alphanumeric ASCII only and can't be redeemed in App Store account settings, so tell people where to redeem them. Add a "Redeem Code" button (paywall, onboarding, settings) that opens the system redemption sheet. Provide a promotional image, or the app icon appears instead
- **Manage subscriptions:** show a plan summary with the renewal date. Prefer the system manage UI (`showManageSubscriptions`). You may offer retention deals, but cancelling must always be easy to find
- **watchOS:** show the same required sign-up info; a modal sheet works well. Be honest about what the watch version includes. Keep options easy to compare: one button per option, or a list plus one button

Source: [HIG — Apple In-App Purchase](https://developer.apple.com/design/human-interface-guidelines/apple-in-app-purchase)

## Wallet
- **Adding passes:** offer the one-tap system add sheet when an action creates a pass. Add frequent, predictable passes (flight check-in) in the background after a one-time authorization. Add related passes together (every leg of a trip). If people decline, don't ask again; keep an **Add to Apple Wallet** button (`PKAddPassButton`) by the pass info, and link to existing passes with "View in Wallet"
- **Lifecycle:** set expiration, relevant date and voided state so Wallet hides stale passes. Delete only with permission. Give time and place relevance so the pass surfaces on the Lock Screen. Send change messages only for time-critical updates (gate change), never marketing
- **Design:** a clean pass that fits Wallet, not a copy of the physical card. Critical info goes in header fields (visible when collapsed); rarely needed info goes on the back. Use brand color and art with labels that contrast on solid and image backgrounds. Write device-neutral copy ("Slide to view" fails on Watch); Watch shows fewer fields and images, so don't rely on optional elements or pad images
  - Styles: boarding pass, coupon, event ticket (poster or standard), store card, poster generic, generic. Airline boarding passes, poster event tickets and poster generic passes need semantic tags; also include pass fields for older iOS. Design and preview in Pass Designer
- **Pass images** (PNG, @2x and @3x; no text or barcodes baked into images; keep files small):

| Image | Size (pt) | Used by |
|---|---|---|
| `icon.png` | 38×38 (system rounds corners) | All |
| `logo.png` | 50 tall, 50–160 wide (no inner drop shadow) | Non-semantic styles |
| `primaryLogo.png` | 30 tall, 30–126 wide | Airline, poster event, poster generic |
| `secondaryLogo.png` | 12 tall, 12–135 wide | Poster event |
| `strip.png` | 375×144 | Coupon, store card |
| `thumbnail.png` | 90 tall, 60–90 wide | Event ticket, generic |
| `background.png` | 343×503 | Non-poster event ticket |
| `artwork.png` | 358×448 (keep to safe area; a material strip covers the bottom) | Poster event, poster generic |
| `footer.png` | 268×15 | Airline boarding pass |

- **Order tracking:** add the order automatically after Apple Pay (`PKPaymentOrderDetails`) or offer the **Track with Apple Wallet** button (`AddOrderToWalletButton`)
  - Supply data right after the order is placed, even if partial, and keep the status current
  - Logo and product images: 300×300 px, PNG or JPEG, **non-transparent** background. Show products plainly, not in lifestyle shots
  - Include a carrier link, a pickup barcode, and several contact methods (a website link at minimum). For Issue or Canceled, say why and what to do next
- **Verify with Wallet** (identity, iOS 16+): show the button only on devices that support it, with a fallback method. Ask only at the moment of need and only for what you need (an age threshold, not a birth date). Say if and how long you keep the data
  - The purpose string is one direct, sentence-case sentence that ends with a period
  - Labels: Verify Age, Verify Identity, Continue (when Wallet is one step of a longer check), or a generic label when none of those fit; each has a multiline variant. The button is always white text on black; use the outlined style on dark backgrounds. Corner radius is adjustable
- Not supported in tvOS

Source: [HIG — Wallet](https://developer.apple.com/design/human-interface-guidelines/wallet)

## Tap to Pay on iPhone
iOS only. Requires a supported PSP, the entitlement, and ProximityReader.
- Let merchants accept the terms before any customer-facing flow (onboarding, in-app messaging). Show the terms only to admin users; others get a message saying an admin is needed. Prompt an iOS update first if the PSP requires it
- Offer a tutorial (Learn More, after the terms, for new users, and always in Settings or Help). You can use `ProximityReaderDiscovery` for Apple's localized education. A custom tutorial must cover each payment type, card placement, and PIN entry, including accessibility mode
- **Checkout:**
  - Always show the Tap to Pay option, even before it's enabled. Tapping it shows the terms if needed
  - Call `prepare` at launch and every time the app returns to the foreground
  - Never hide the option during configuration; show progress instead (determinate when the API reports progress)
  - Make it reachable without scrolling. If it's your only payment method, open it automatically at checkout
  - Tips and other changes to the total come first, so the Tap to Pay screen shows the final amount
- **Button label:** "Tap to Pay on iPhone", or "Tap to Pay" when space is tight. An app with only this payment method can reuse its Charge or Checkout button
  - Icon: `wave.3.right.circle` or `.fill`. **Never include the Apple logo**
  - Color and shape can match your app
- For card reads with no amount (lookup, refund, verify), use generic labels like "Look Up", "Store Card", "Verify" or "Refund", never "Tap to Pay". Loyalty-only reads get their own button with no payment wording
- **Results:** start processing early (`returnReadResultImmediately`). Show your own authorization progress once the checkmark animation ends. Show declined and approved results clearly and offer a digital receipt. On failure, offer another payment method or a retry. Explain merchant-fixable errors and link to support

Source: [HIG — Tap to Pay on iPhone](https://developer.apple.com/design/human-interface-guidelines/tap-to-pay-on-iphone)

## CarPlay
iOS only. Build with system templates (audio, communication, navigation, fueling, etc.); the system renders them and handles every display and input type.
- The car's controls do all the work. Don't require iPhone input or unlocking while driving, finish setup before the car moves, and report errors in CarPlay, never on the phone
- **Audio:** don't autoplay unless the app plays a single source or is resuming. Start the audio session only when ready, because it silences the radio. Show Now Playing as soon as audio can play and load metadata afterward. Resume only after temporary interruptions like a call. You may adjust relative levels, but never the overall volume
- **Layout:** keep it clean and easy to scan, with key content and controls in the top half and larger targets for important items. Common displays: 800×480, 960×540, 1280×720, 1920×720 px; the system handles scaling
- **Color:** use a limited palette tied to your logo, and don't give interactive and static elements the same color. Test in a real car in daylight and at night. Support light and dark
- **Icons:** mirror the iPhone icon, and never on a black background (lighten it or add a border). Sizes: 120×120 px @2x, 180×180 px @3x. Provide @2x and @3x for all artwork

Source: [HIG — CarPlay](https://developer.apple.com/design/human-interface-guidelines/carplay)

## Siri
Revised for Siri AI (June 2026). Use App Intents to expose features and content to Apple Intelligence and Siri.
- Map features to **app schemas** where one fits. Use App Shortcuts for custom actions outside the schema domains
- Give Siri context:
  - Annotate onscreen views and content with **app entities** (onscreen awareness)
  - Donate entities to the on-device Spotlight index
  - Donate the actions people take as intents so Siri can anticipate them
- Start from your most popular actions and when they happen. Use terms people already know. Surface relevant personal context (recent searches, favorites, wishlists)
- No ads, marketing, or In-App Purchase pitches in anything Siri delivers
- Write custom responses only when the built-in ones fall short. Keep them clear and brief, and make them work both spoken and on screen and on any device
  - Leave out your app name. Avoid unnecessary gendered pronouns. For long option lists, ask an open-ended question. Give specific error messages
- Snippets (e.g., a playback-control snippet): see [Snippets](hig-patterns.md#snippets)
- **Editorial:** call Siri "Siri", never "she" or "her". Never impersonate Siri or make a response look like it comes from Apple. Don't use reserved phrases ("Hey Siri", "Call 911"). When localizing, translate only "Hey"; never translate "Siri"

Source: [HIG — Siri](https://developer.apple.com/design/human-interface-guidelines/siri)

## Generative AI
Updated June 2026 (refining results, feedback during generation, choosing a model type).
- Design responsibly and keep people in control. The app must still work well when generative features are unavailable or turned off
- **Transparency:** say where the app uses AI and what the feature can and can't do
- **Privacy:** choose a model type that fits the feature and protects privacy. Ask before using personal or usage data, and say how it's used and stored
- **Inputs:** show people how to phrase requests. Reduce hallucinations and warn about them. Get permission before irreversible or risky actions
- **Outputs:**
  - Make refine and revert easy, and confirm when a correction has taken effect
  - When a request is blocked, help people rephrase it
  - Test for harmful or unexpected results, and avoid reproducing copyrighted content
  - Plan for processing time with specific, reassuring progress feedback. Consider offering alternate versions
- **Improvement:** let people give feedback on outputs, and build features that can adapt as models change

Source: [HIG — Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai)

## HealthKit
- Request health data only when needed, and add purpose text to the standard permission screen. Publish a privacy policy. Manage sharing only through system privacy settings
- **Activity rings:** use them only for Move, Exercise and Stand, and only for one person's progress. Never use them as decoration or branding. Keep the ring and background colors and the margins. Make other ring-like elements look clearly different. Activity notifications carry only app-specific info
- **Apple Health icon:** use only Apple's artwork, unaltered, with the name *Apple Health* nearby. Size it consistently with other health-app icons. Not a button, never inline in text, never a stand-in for the words. Keep clear space of ≥ 1/10 of its height. Don't show Health app screenshots
- **Editorial:** say "Apple Health" or "the Apple Health app". Don't say "HealthKit" to users. Use the system's localized name for Health

Source: [HIG — HealthKit](https://developer.apple.com/design/human-interface-guidelines/healthkit)

## Augmented reality
- Give AR as much of the screen as possible. Use realistic, correctly scaled assets on detected surfaces, with environment lighting, soft top-down shadows and camera grain. Update **60 times per second** so objects don't jump
- Keep controls reachable without regripping the device, and translucent so they don't block the scene. Explain requirements up front. Build in rest breaks and encourage movement gradually. Think about safety
- **Coaching:** use the system coaching view, or model a custom one on it, and hide unrelated UI while it's up
- **Placement:** show a surface indicator aligned to the detected plane. Place objects immediately and refine their position quietly afterward. Use plane classification (e.g., furniture only on "floor"). Give cues that point to offscreen objects
- **Gestures:** tap objects directly rather than through screen-space controls. One-finger drag moves an object along its surface; two-finger rotate turns it on a single axis. Allow scaling only when it makes sense. Objects shouldn't jump or vanish
- **Image detection** works best with ≤ 100 reference images. When a tracked image disappears, wait up to ~1 s before removing attached content
- **Copy:** don't use jargon like "ARKit" or "tracking". Prefer 3D hints in 3D space. Put critical text in screen space; text placed in 3D must face the viewer
- **Interruptions:** use coaching for relocalization and hide objects until they're repositioned. Offer a reset option. Show an indicator when face tracking is lost
- **AR glyph and badges:** only for ARKit experiences. You may change the glyph's size and color, but never alter a badge in any way. Prefer the full AR badge to the glyph-only one. Badge only when some items support AR and some don't; keep the badge in the same corner every time. Clear space: ≥ 10% of the glyph's or badge's height

Source: [HIG — Augmented reality](https://developer.apple.com/design/human-interface-guidelines/augmented-reality)

## SharePlay
Reorganized September 2026, with expanded visionOS guidance and custom spatial templates.
- Use it for real-time shared experiences that fit what people are doing together, and make them work across Apple platforms
- Starting and joining should take little effort. Describe activities briefly. Keep people oriented when the activity changes. Use the term *SharePlay* correctly
- iOS, iPadOS and macOS: support Picture in Picture for shared video
- **visionOS:**
  - Prefer starting from a window, and save unique views for moments that need them
  - Resolve conflicts between participants naturally. Let people opt in to immersion changes mid-task and adjust for comfort and accessibility
  - Make leaving and rejoining easy, and support people who don't use a spatial Persona
  - Choose the system spatial template that fits, or build a custom one. Split complex activities into stages, let people start template transitions, and keep transitions smooth
  - **Custom templates:** account for people in the same room. Orient seats toward the content and support the maximum seat count. Space seats **at least a meter apart** and set the order people take them. Keep roles separate from seats

Source: [HIG — SharePlay](https://developer.apple.com/design/human-interface-guidelines/shareplay)

## Live Photos
- Apply edits to every frame, and keep the content intact (don't trim away the motion or sound). Make sharing work well
- Show when a Live Photo is downloading and when it's ready to play. Where Live Photos aren't supported, show it as a still
- To mark a Live Photo, use a hint of motion (a custom effect). If motion isn't possible, use the system badge, with or without text, in the same spot on every photo, usually a corner. **Never add a play button** that looks like video playback
- visionOS can display Live Photos but can't capture them

Source: [HIG — Live Photos](https://developer.apple.com/design/human-interface-guidelines/live-photos)

## Game Center
- **Access point:** show it on menu screens (main menu, settings), never during gameplay, splash screens, cinematics or pre-menu tutorials. Pin it to one corner, check it doesn't cover important controls, and consider pausing while the Game Overlay or dashboard is open
- **Custom UI:** use Game Center artwork from Apple Design Resources, unmodified. Use the official terms: Game Center, Game Center Profile, Achievements, Leaderboards, Challenges, Add Friends
- **Achievements:** make rewarding art (without it a placeholder appears). A circular mask is applied, so keep content centered
- **Leaderboards:** classic (all-time) or recurring (resets on an interval you set). Group boards into sets (difficulty, activity, genre) and give each board its own image. tvOS needs layered artwork that animates on focus
- **Challenges:** short skill runs of **1–5 minutes** that one player can finish alone. Track the most recent score, not personal bests or cumulative progress. Deep-link straight to the right mode or level, running any required tutorial first. Keep key art clear of the title overlay and localize any text
- **Multiplayer:** party codes (typically 8 alphanumeric characters): show the current code in-game and allow manual entry. Let players join late, leave, and come back
- Artwork specs (all 72 DPI min, sRGB or P3):

| Asset | Size (pt; @2x px) | Notes |
|---|---|---|
| Achievement (iOS, iPadOS, macOS, visionOS) | 512×512 (1024×1024) | Mask ⌀ 512 pt |
| Achievement (tvOS) | 320×320 (640×640) | Mask ⌀ 200 pt |
| Leaderboard (iOS, iPadOS, macOS) | 512×512 (1024×1024) | Cropped area 512×312 |
| Leaderboard (tvOS) | 659×371 (1318×742) | Focused 618×348, unfocused 548×309 |
| Challenge / activity | 1920×1080 (3840×2160) | Cropped area 1465×767 |

- watchOS has no system Game Center UI; Game Center content appears on the paired iPhone

Source: [HIG — Game Center](https://developer.apple.com/design/human-interface-guidelines/game-center)

## Machine learning
- **Explicit feedback:** request it rarely and keep it voluntary. Describe each option and what it does in plain words. Act on it immediately and keep the result
- **Implicit feedback:** protect the data and give people control. Don't narrow what people can explore. Combine signals, weight recent behavior, and hold back sensitive suggestions. Watch for confirmation bias
- **Calibration:** do it once and keep it quick. Ask only for essentials and explain why. Help right away if progress stalls. Confirm success, allow cancel at any time, and let people edit or remove what they gave
- **Corrections:** make them familiar and immediately useful, and let people undo them. Prefer guided corrections to freeform ones. Don't use corrections to cover for poor results
- **Mistakes:** expect them and weigh their consequences. Proactive features need extra care
- **Confidence:** translate scores into ideas people understand, or imply them through ranking. Show numbers only where people expect statistics. Hide low-confidence results when confidence tracks quality
- **Attribution** ("Because you read…"): factual, not too specific or too vague, no jargon
- **Limitations:** set expectations, show how to get good results, and say when a limitation is fixed
- **Multiple options:** a few diverse choices, most likely first

Source: [HIG — Machine learning](https://developer.apple.com/design/human-interface-guidelines/machine-learning)

## VoiceOver
- Label every key element. Describe meaningful images and make charts and infographics fully accessible. Hide purely decorative images
- Use titles and headings to show hierarchy. Define grouping, order and links between elements. Announce content or layout changes. Support the rotor
- visionOS: custom gestures may not be accessible, so provide alternatives
- Details and the system-wide accessibility rules: [Accessibility](hig-foundations.md#accessibility)

Source: [HIG — VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover)

## Mac Catalyst
- **iPad idiom:** the UI scales to 77% on Mac, so iPad 17 pt body text shows at 13 pt and looks slightly less crisp. **Mac idiom:** everything renders at 100%. Audit and adjust the layout, since text can look too large. Limit appearance customizations to ones macOS and iPadOS share
- Replace a tab bar with a sidebar split view (or a segmented control), keep every tab's content reachable, and list top-level items in the View menu
- Move controls from the iPad main UI into the window toolbar. Move buttons away from the bottom and side screen edges
- Context menus convert automatically. Mac users expect one on every object
- Pointer, keyboard focus and window management come for free. Good Split View and Slide Over support prepares the app for free-form Mac window resizing

Source: [HIG — Mac Catalyst](https://developer.apple.com/design/human-interface-guidelines/mac-catalyst)

## AirPlay
- Prefer the system media player. Stream at the highest resolution, and stream only what people expect. Support both streaming and mirroring, and handle remote-control events
- Keep playing when the app goes to the background or the device locks. Don't interrupt other apps' audio unless you're starting immersive content. Let people use the rest of the app during playback
- A custom player must match the system controls. Use only Apple's AirPlay symbols, placed at the **lower-right** (iOS/iPadOS 16+)
- **AirPlay icon (marketing):** black on light backgrounds, white on dark ones, or a custom color only if the other technology icons share it. Position it consistently with those icons. Never put the icon or name in a custom button. Keep your own app more prominent than AirPlay
- **Text:** capitalize it as *AirPlay* and use it only as a noun ("works with AirPlay", "supports AirPlay"). "Apple AirPlay" is fine

Source: [HIG — AirPlay](https://developer.apple.com/design/human-interface-guidelines/airplay)

## HomeKit
- **Terms:** home, room (just a name), zone (a group of rooms), scene, accessory. In the UI, say what a service or characteristic does ("ceiling fan light", "brightness"); never show the words "service" or "characteristic"
- **Setup:** use the system setup flow. Explain why you need Home data. Don't require an account or personal info, and respect the choices people made during setup
  - Suggest fitting service names. Names may contain only letters, numbers, spaces and apostrophes; must start and end with a letter or number; no emoji; no location words
- **Siri:** show example voice commands during setup, and suggest zones and service groups where they help. Offer shortcuts only for features HomeKit doesn't cover, and explain how they differ from HomeKit control
- **Icons:** use the HomeKit icon for setup and instructions, and the Apple Home app icon only to mean the app or to link to its App Store page. Use only Apple artwork. Black, white or a shared custom color, matching your other tech icons. Non-interactive, never inline in text
- **Text:** write *HomeKit* (one word, capital H and K) and *Apple Home* (two words). Don't use HomeKit as a descriptor or as the subject that does things. Keep your app more prominent than HomeKit

Source: [HIG — HomeKit](https://developer.apple.com/design/human-interface-guidelines/homekit)

## ID Verifier
iPhone reads mobile IDs in person without extra hardware.
- Request only what you need; ask for an age threshold, not a birth date or current age
- The button that starts verification uses a label like "Verify Age" or "Verify Identity". No NFC or QR symbols and **never the Apple logo**
- For Display Only requests, let the operator record the visual check, e.g. "Matches Person" or "Doesn't Match Person" buttons next to the portrait
- Register with Apple Business Register (if eligible) so customers see your organization's details. Related in-app verification: [Wallet](#wallet)

Source: [HIG — ID Verifier](https://developer.apple.com/design/human-interface-guidelines/id-verifier)

## Always On
- Hide sensitive data (balances, health info, notification content) from casual observers
- Dim what isn't essential, and dim secondary text, images and fills even more. Replace rich images or large color areas with dimmed colors
- Update rarely and subtly (e.g., a sports app updates only the score). Motion is especially distracting on a phone lying face up
- iPhone: Always On shows Lock Screen widgets and Live Activities. Apple Watch: dims the face but keeps showing a frontmost or background-session app

Source: [HIG — Always On](https://developer.apple.com/design/human-interface-guidelines/always-on)

## Maps
- Emphasis styles: *default* (fully saturated) or *muted* (desaturated, so your data stands out)
- **Apple logo and legal link:** always visible, fixed to the map, and never moving with your UI. Pad them about **7 pt on the sides and 10 pt above and below**. With a bottom card, place them **10 pt above the card's lowest resting position**
- **Annotations:** style them to match your app (the default is a red marker with a white pin). Glyph strings should be 2–3 characters
- **Overlays:** *above roads* (the default; buildings and trees stay visible) or *above labels* (hides everything beneath). Make custom controls contrast with the map using a thin stroke, light shadow, or blend mode
- **Place cards:** automatic, callout (full or compact), caption ("Open in Apple Maps" link), or sheet. Full callouts show as a popover on iPad and Mac and as a sheet on iPhone. Pick the style that doesn't repeat info you already show. Keep the selected location visible (use an offset). Outside a map, signal tappable places with location cues like a pin icon next to the name
- **Indoor maps:** add detail as people zoom in. Offer a floor picker with short floor numbers. Dim surrounding non-interactive areas. Route to nearby transit. Limit scrolling so part of the venue stays onscreen. Match your app's style, not Apple Maps'
- watchOS: the map must fit the screen with no scrolling, showing the smallest region that includes every point of interest

Source: [HIG — Maps](https://developer.apple.com/design/human-interface-guidelines/maps)

## App Clips
- Let people finish one task, or a demo, right away. Keep it small and linear, with no web views and no marketing-only clips. Open to the most relevant screen. Don't require an account. Offer Sign in with Apple and Apple Pay. Make it shareable
- Suggest the full app only after the task is done, politely. Request extended notification permission only when truly needed, and keep notifications tied to the task
- **App Clip card:** informative photo or graphic, no text in the image. 1800×1200 px PNG or JPEG, no transparency. Title ≤ 30 characters, subtitle ≤ 56. Action verb: *View* (media or info), *Play* (games), *Open* (everything else)
- **App Clip Codes** (scan-only or NFC-integrated): always use the generated code (App Store Connect or the App Clip Code Generator). Don't add symbols. Pick color pairs with enough contrast. Include the App Clip logo when space allows
  - Place on flat or cylindrical surfaces, upright and unobstructed. On a cylinder, the code spans ≤ 1/6 of the circumference. Clear space equals the gap between the center glyph and the code ring
  - Minimum size: **3/4 in (1.9 cm)** printed, **256×256 px** digital (PNG or SVG). With NFC, the tag must be ≥ 35 mm, so the code is ≥ 1.37 in (3.48 cm). Keep scan distance to code size at ≤ **20:1**
  - Add a call to action ("Scan to…", or for NFC "Hold your iPhone near the…"). Use the NFC tag type the HIG specifies, high-quality non-textured print, and the calibration sheets. Stop showing a code when its App Clip is retired. Never use it in your company or product name

Source: [HIG — App Clips](https://developer.apple.com/design/human-interface-guidelines/app-clips)

## iMessage apps and stickers
iOS and iPadOS only. Also available in Messages and FaceTime effects.
- Give each iMessage app one primary experience; split different functions into separate apps. Consider surfacing shareable or collaborative content from your main app
- Put the most-used features in the compact view (below the transcript, about the height of the keyboard). Allow text editing only in the expanded view
- Stickers must stay legible on any background and when rotated or scaled; transparency helps them blend in. Give each one a localized alternative description for VoiceOver
- **Icons** (square corners; the system masks them): Messages and notifications use 148×110, 143×100, 120×90 (180×135 @3x), 64×48 (96×72), 54×40 (81×60) px. Settings 58×58 (87×87) px. App Store 1024×1024 px
- **Stickers:** one size per pack, supplied at @3x: small 300×300, regular 408×408, large 618×618 px. **≤ 500 KB** per file. PNG (8-bit alpha, static), APNG (8-bit alpha, animated), GIF (single-color transparency, animated), JPEG (no alpha, static)

Source: [HIG — iMessage apps and stickers](https://developer.apple.com/design/human-interface-guidelines/imessage-apps-and-stickers)

## NFC
- In the UI, say "scan" or "hold near", not "tap" or "touch", and don't encourage physical contact. Never say "NFC", "Core NFC" or "tag"; name the object instead ("Scan the [object]")
- Scan-sheet text is one short, complete sentence in sentence case with a period that names the object. Change it for repeat scans ("Now hold your iPhone near another [object].")
- Support background tag reading, and always keep an in-app scan option for devices that can't read in the background

Source: [HIG — NFC](https://developer.apple.com/design/human-interface-guidelines/nfc)

## CareKit and ResearchKit
- **CareKit privacy:** same as [HealthKit](#healthkit): request access only when needed, explain why, and manage sharing through system settings
- **CareKit tasks:** each needs a title and a schedule; instructions and group ID are optional. Pick the card style that fits: simple (one step), instructions, log, checklist, or grid (multistep buttons). Use color to reinforce meaning. Keep descriptions accurate and simple, and add video or images for complex tasks
- **CareKit charts:** short labels, distinct colors, a legend, clear time units. Consolidate large data sets, and offset data to keep charts proportional. Color-code care team contacts. Keep notifications to a minimum. Design a relevant care symbol with subtle branding
- **ResearchKit onboarding:** keep screens in order: eligibility first, asking only what's needed, then informed consent split into short sections (optionally with a comprehension quiz), then permissions for only the data the study needs, with reasons
- **ResearchKit surveys:** say up front how many questions and how long. One question per screen, with a progress indicator, as short as possible, and a clear end. Active tasks need plain instructions, any timing requirements, and an obvious finish
- Provide an encouraging results dashboard, and a profile screen with the consent document, privacy policy, and an easy way to leave the study

Source: [HIG — CareKit](https://developer.apple.com/design/human-interface-guidelines/carekit) · [HIG — ResearchKit](https://developer.apple.com/design/human-interface-guidelines/researchkit)
