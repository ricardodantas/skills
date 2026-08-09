---
name: app-idea-research
description: Research and validate an app or software product idea end-to-end and deliver a brutally honest go/no-go verdict. Orchestrates installed research skills and fans out parallel subagents to analyze community pain points (Reddit and forums), competitors, market size and trends, target demographics, monetization, and the latest Apple and Android frameworks — then synthesizes one report with 1-10 scores, a platform recommendation (iOS/Mac-only, Android-only, or multiplatform), a detailed concept description, and concrete examples. Use when the user asks "is this app idea worth building", "validate my app idea", "should I build X", "research this product/startup idea", "is there a market for an X app", "will this app make money", or wants competitor/market/demographic research plus a build/no-build recommendation.
---

# App Idea Research

Validate an app idea against reality and return a **brutally honest** verdict — is it worth
building, for which platform, and why. This skill **orchestrates other installed skills** and
**fans out parallel subagents** to research fast, then synthesizes a single scored report.

Be the skeptic the idea needs. Most app ideas should get a **PASS**. Kill weak ideas early;
only recommend BUILD when the evidence survives scrutiny. Never inflate scores to be encouraging.

## Workflow

1. **Frame the idea** — restate the concept in one sentence, the target user, and the core job.
   If the idea is vague, ask one clarifying question, then proceed with a stated assumption.
2. **Preflight companion skills** — check which skills from the table below are installed (they
   appear in your available skills). For each research dimension, use the companion if present;
   otherwise fall back to direct web research. Offer `npx skills find <name>` for a missing one.
3. **Fan out parallel research subagents** — dispatch independent `task` (explore/research)
   subagents across the dimensions in parallel. See [references/research-playbook.md](references/research-playbook.md)
   for the per-dimension briefs, source lists, and fan-out guidance.
4. **Check the latest Apple & Android frameworks** — determine whether new platform capabilities
   make the idea newly possible, newly redundant, or newly threatened. Delegate framework/API
   facts to `find-docs` (Context7); see the playbook's framework section.
5. **Synthesize the verdict** — merge subagent findings, resolve contradictions, score each
   dimension 1-10, decide the platform, and write the report using
   [references/verdict-report.md](references/verdict-report.md).
6. **Output** — save the report **and** brief the user (see [Output](#output)).

## Companion skills (preflight registry)

Run this as a preflight: prefer the companion when it is installed; delegate the craft to it
rather than re-deriving it here. For any missing companion, tell the user and offer
`npx skills find <name>`, then fall back to direct web research for that dimension.

| Research dimension | Companion skills |
|--------------------|------------------|
| Apple ecosystem pain points, saturation, gauntlet | `apple-app-research`, `ios-app-research` |
| Android ecosystem pain points, Play Store saturation | `android-app-research` |
| General primary-source investigation (background) | `research` |
| Competitor / alternatives landscape | `competitor-alternatives` |
| Monetization & pricing | `pricing-strategy` |
| Demand, positioning, growth signal | `marketing-ideas`, `launch-strategy` |
| Latest framework / API facts (version-pinned) | `find-docs` |
| Filling a capability gap | `find-skills` |

The `apple-app-research` / `android-app-research` / `ios-app-research` companions already ship a
**Viability Gauntlet**, community source lists, and per-platform scoring — use their output as the
per-platform input to this skill's synthesis. This skill adds the cross-platform decision, the
framework check, and the unified 1-10 verdict.

## Scoring (1-10)

Score each dimension 1-10 from the evidence — not from enthusiasm. Anchors: **1-3** = fatal/weak,
**4-6** = mixed/unproven, **7-8** = strong, **9-10** = exceptional with hard evidence.

| Dimension | Question |
|-----------|----------|
| Demand | Do real people actively want this, with evidence (searches, threads, engagement)? |
| Pain severity | "Hair on fire" problem, or mild annoyance? |
| Monetization | Do people already pay in this category? Realistic revenue at honest conversion? |
| Competition / saturation | How many good incumbents? Fewer + unmet need = higher. |
| Feasibility | Can a small team ship a real MVP quickly, within platform constraints? |
| Timing (why now) | What changed (OS/hardware/regulation/market) that makes now the moment? |
| Differentiation | A defensible wedge, or just "prettier"? A feature is not a product. |
| Distribution | Is there an organic discovery path (the answer to a recurring "what do you use for X?")? |

**Overall = the honest gestalt, not a mean.** Any fatal dimension (e.g. no monetization, an
incumbent gives it away free, platform will absorb it) caps the overall low regardless of the rest.
Map overall to a verdict: **PASS 1-4 · MAYBE 5-6 · BUILD 7-10**.

## Platform decision

Decide the top-line platform from where the pain, willingness-to-pay, and feasibility concentrate:

- **iOS/Mac-only** — demand + monetization live in the Apple ecosystem; needs Apple-specific
  frameworks (Shortcuts, HealthKit, CarPlay, visionOS, Continuity) or Apple's paying user base.
- **Android-only** — pain is Android-specific (fragmentation, OEM quirks, degoogle, Wear OS/Android
  Auto gaps); note that Android monetization is harder — say so plainly.
- **Multiplatform** — the job is platform-agnostic and demand exists on both; only recommend if the
  team can realistically maintain both, else recommend a lead platform first.

State the verdict as one of these three, name the sub-platforms (iPhone/iPad/Mac/Watch/Vision vs
phone/tablet/Wear OS/Android TV/Auto), and justify with the evidence.

## Output

Deliver **both**:

1. **Saved report** — write `app-idea-research-<slug>.md` in the current working directory,
   following [references/verdict-report.md](references/verdict-report.md). `<slug>` is a short
   kebab-case name for the idea. Do **not** commit it — leave that to the user.
2. **In-chat briefing** — lead with the verdict (BUILD/MAYBE/PASS), the overall 1-10, and the
   platform recommendation; then the two or three findings that drove the call. Keep it tight.

Cite evidence with links, verify every claim against its source (don't infer a market from a name),
and lower confidence when evidence is thin — never pad a weak case.
