---
name: hugo-write-post
description: Learn a Hugo blog author's writing style from their existing posts and write a new post on a given topic that reads exactly like them, placed with correct Hugo front matter. Use inside a Hugo (gohugo.io) repository when the user wants to write or generate a blog post in their own voice — "write a post about X like I usually write", "draft a blog post in my style", "add an article to content/", mimic my tone, or match my writing. Delegates the prose to the social-content skill.
---

# Hugo Write Post

Write a new blog post for a Hugo site that matches how the author already writes. This skill
learns the author's voice and conventions from their existing posts, delegates the writing to the
`social-content` companion skill, then places the result as a proper Hugo content file.

Hugo specifics (front-matter formats, `hugo new`, archetypes, sections, taxonomies, build/serve)
live in [references/hugo.md](references/hugo.md) — read it when placing the file or resolving
conventions.

## Workflow

### 0. Preflight — companion skill

The prose is written by the `social-content` skill. Confirm it's available (it appears in your
available skills). If it's missing, tell the user and offer to install it —
`npx skills find social-content` — and don't start writing until it's available.

### 1. Confirm this is a Hugo repo

Look for a Hugo config (`hugo.toml`, `hugo.yaml`, `hugo.json`, or `config/…`) alongside a
`content/` directory (and usually `archetypes/`). If they're absent, stop and tell the user this
skill only runs inside a Hugo site.

### 2. Get the topic

Ask the user for the post topic if they haven't given one. Capture any specifics (angle, key
points, target length) they volunteer — but do not invent constraints they didn't ask for.

### 3. Learn the author's voice

Run the analyzer to extract the mechanical conventions across existing posts:

```bash
scripts/analyze_style.py content            # defaults to ./content, recent 5
scripts/analyze_style.py content --recent 8 # sample more posts
```

It reports the front-matter format and key frequency, the section/dir posts live in, the filename
pattern, length/heading/list/code stats, the tag/category vocabulary, and the most-recent files.

Then **read the 2–3 most-recent full posts** it lists to capture the qualitative voice that a
script can't: tone, sentence rhythm, opening and closing patterns, formatting habits, how headings
and lists are used, first vs third person. Summarize all of this into a short **style profile**
(mechanical conventions + voice) — this is what makes the output read like the author.

### 4. Write the post with social-content

Hand `social-content` the topic **and** the full style profile plus 1–2 representative excerpts,
instructing it to write a complete blog post in that exact voice, structure, and length. It is the
primary writer — don't hand-write the body yourself when it's available.

### 5. Place the file with correct front matter

Prefer Hugo's own generator so archetypes and front matter are honored:

```bash
hugo new content <section>/<slug>.md        # e.g. hugo new content posts/my-topic.md
```

Match the author's conventions from the style profile: same section/dir, filename pattern, and
front-matter format (TOML `+++`, YAML `---`, or JSON). If `hugo new` isn't available, mirror the
newest post's front-matter shape by hand. Fill the fields the author actually uses (title, date =
now, tags/categories drawn from their existing vocabulary, description, slug). Default `draft:
false` (publishable) unless the user asks for a draft. Then write the body from step 4.

See [references/hugo.md](references/hugo.md) for the details.

### 6. Style-fidelity check

The post must read **exactly** like the author. Compare the draft against the style profile:

- Front-matter keys/format match the author's posts
- Word count within the author's typical range
- Heading density, list/code usage, and paragraph length in the author's habit
- Tone, person, opening/closing pattern match

If anything is off, send it back through `social-content` with the specific gap and revise. Repeat
until it matches.

### 7. Preview (optional)

Offer to render it so the user can check it:

```bash
hugo server -D        # live preview incl. drafts
hugo                  # one-off build
```

Report the created file path and the local URL.
