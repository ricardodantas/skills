# Research Playbook

How to research an app idea fast with **parallel subagents**, which sources to hit per dimension,
and how to check the latest Apple/Android frameworks. Referenced from SKILL.md step 3-4.

## Contents
- [Fan-out strategy](#fan-out-strategy)
- [Dimension briefs](#dimension-briefs)
- [Source lists](#source-lists)
- [Framework check (Apple & Android)](#framework-check-apple--android)
- [Verification rules](#verification-rules)

## Fan-out strategy

Dispatch **independent** research threads in parallel with the `task` tool (one `research` or
`explore` subagent per dimension) so reading happens concurrently. Rules:

- Launch all independent subagents in **one batch**; don't serialize what can run together.
- Give each subagent a **self-contained brief**: the idea in one line, its dimension, the exact
  sources to check, and the output shape (bullets + links + a 1-10 read on its dimension).
- Prefer an installed companion skill when it owns the dimension (see SKILL.md preflight table) —
  tell the subagent to use it. Otherwise the subagent does direct web research.
- Keep dimensions that must react to each other (final scoring, platform call) in the **main
  thread** — subagents gather, you synthesize.
- Merge on return: dedupe findings, resolve contradictions by trusting the higher-quality source,
  and note where evidence is thin.

Suggested parallel set: **A** communities/pain points (Apple), **B** communities/pain points
(Android), **C** competitors, **D** market size & trends, **E** demographics, **F** monetization,
**G** framework check. Collapse to fewer subagents for a narrow idea; a single-platform idea can
skip the other platform's community thread.

## Dimension briefs

Each brief = what to find + where + what to return.

- **A/B — Community pain points.** Search the platform communities (below) for recurring
  frustration matching the idea. Return: concrete complaints with engagement (upvotes/replies),
  who feels it, how often, current workarounds, and whether the pain is "hair on fire." Delegate to
  `apple-app-research` / `ios-app-research` / `android-app-research` when present — they ship the
  Viability Gauntlet and source lists.
- **C — Competitors.** Find every existing app/tool (App Store, Play Store, web, OSS, built-in OS
  features). Return: names, install/review counts, price model, top 1-star complaints (the unmet
  need), and the specific gap the idea would exploit. Use `competitor-alternatives` if present.
- **D — Market size & trends.** Is the category growing, flat, or declining? Return: trend evidence
  (search interest, category reports, news), tailwinds/headwinds, and "why now" triggers.
- **E — Demographics.** Who is the buyer, how many, where, ability/willingness to pay. Return: a
  concrete persona (not "everyone"), rough addressable size, and platform skew (Apple users skew
  higher-spend; Android skews larger + free-expecting).
- **F — Monetization.** How would this actually make money on each platform? Return: model
  (subscription / one-time / freemium+IAP / B2B / ads), evidence that people pay in this category,
  and an honest revenue read at realistic (not optimistic) conversion. Use `pricing-strategy` if
  present.
- **G — Framework check.** See [Framework check](#framework-check-apple--android).

## Source lists

These are the **fallback** for when a platform companion skill isn't installed; when it is, prefer
its own maintained source list and add anything below it lacks.

**Apple communities:** r/apple, r/ios, r/iphone, r/ipad, r/macos, r/macapps, r/shortcuts,
r/iOSProgramming, r/SwiftUI, r/VisionPro, r/AppleWatch; Apple Support Communities, Hacker News,
Product Hunt, Indie Hackers, MacStories, Mac Power Users forum.

**Android communities:** r/android, r/androidapps, r/androiddev, r/GooglePixel, r/samsung,
r/oneplus, r/Xiaomi, r/WearOS, r/AndroidAuto, r/degoogle, r/fdroid; XDA Developers, Android Police
comments, Hacker News, Product Hunt.

**Market / trend / demographic:** Google Trends, App Store & Play Store category charts and review
counts, Statista/Data.ai/Sensor Tower summaries (where accessible), Exploding Topics, category
news, and first-party platform usage reports. Prefer primary sources over secondary write-ups.

If a headless fetch returns empty markup on a JS-rendered page, use the `podman-browser` skill (if
installed) to render it.

## Framework check (Apple & Android)

Determine whether the **latest** platform capabilities change the verdict. A new framework can make
an idea newly **possible** (greenfield), newly **redundant** (the OS now does it), or newly
**threatened** (the platform owner will absorb it). Check both:

- **Apple:** current SwiftUI, App Intents / Shortcuts, WidgetKit / Live Activities, HealthKit,
  CarPlay, visionOS/RealityKit, Continuity, Apple Intelligence, Screen Time / Family Controls,
  and any capability the idea depends on. Note sandbox/entitlement limits that could kill the UX.
  The `apple-app-ship` skill covers Apple build/ship specifics if the idea proceeds.
- **Android:** current Jetpack Compose, App Actions, Health Connect, Wear OS, Android Auto,
  background-work and permission restrictions (which Google keeps tightening), and Gemini
  integration points. Flag OEM fragmentation risk.

Pin facts to the platform's **current** version via `find-docs` (Context7) rather than relying on
possibly-stale memory. Ask: "does a built-in feature already cover 80% of this?" — if yes, that
caps the Feasibility/Differentiation scores.

## Verification rules

- **Cite every non-obvious claim** with a link; a market you can't source is a market you invented.
- **Verify, don't infer** — do not conclude demand from an app name or a single post; require
  corroboration across sources.
- **Weight by quality** — first-party docs, real review counts, and high-engagement threads over
  blog opinion.
- **Separate signal from noise** — one loud complaint is not a market; a recurring, upvoted,
  cross-community pattern is.
- **State confidence** — when evidence is thin, say so and lower the score; never pad a weak case.
