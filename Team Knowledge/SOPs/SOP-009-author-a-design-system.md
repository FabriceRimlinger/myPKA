# SOP-009 - Author a Design System

- **Status:** Active (since v1.6.0)
- **Default owner:** Iris
- **Reusable by any agent.** This is a skill, not a 1:1 ownership. Any specialist can run this procedure when the user asks to set up or extend their visual identity. In practice Iris runs it, but if the team grows and another design-flavored agent gets hired, they can invoke this SOP without re-deriving the procedure.
- **Triggered by:** "set up my design system", "let's pin my brand", "what colors / fonts / spacing should I use", "I want to add a new accent / type role / token", first creative request when [[GL-003-design-system]] is empty.
- **References:** [[GL-003-design-system]] (the artifact this SOP populates), [[GL-001-file-naming-conventions]], [[Team/Iris - Design System Architect/AGENTS]], [[SOP-010-audit-content-for-design-system-compliance]] (the companion audit skill).

## Purpose

Walk the user through populating [[GL-003-design-system]] in a single guided session: identity, color palette, typography, spacing scale, imagery style, voice samples. The output is a populated GL-003 file that Charta, Pixel, and any future creative agent reads on every task.

The procedure is decision-led, not prescriptive. The user picks; this SOP asks the right questions in the right order.

## What this SOP does not do

- Does not pick values unilaterally. Every value comes from the user. Agents do not decide the brand.
- Does not produce visual deliverables (slides, images, infographics). That is [[SOP-007-build-an-infographic]] and [[SOP-008-generate-a-styled-image]].
- Does not audit existing deliverables against GL-003. That is [[SOP-010-audit-content-for-design-system-compliance]].

## When to run this SOP

- **First creative request gate.** When the user asks for any creative work (slide, image, infographic, thumbnail, PDF) and GL-003 is empty (or empty for the section the work needs), this SOP runs first.
- **Schema evolution.** When the user wants to add or change a token (new accent color, new heading font, additional spacing token), this SOP runs targeted on the affected section.
- **Voluntary setup.** The user explicitly asks to pin the design system before any creative work is requested.

If the user explicitly chooses to skip GL-003 setup ("let's just hack it together for now"), creative work proceeds in flagged "no-style fallback" mode. The deliverable carries a "GL-003 not populated" note. This SOP is invoked the next time the user wants consistency.

## Inputs

- **The brand context.** What is being designed for: a personal knowledge folder (myPKA), a consulting business, a SaaS product, a podcast, a course brand, a side project.
- **Existing visual references (optional).** Sites, decks, palettes, mood boards the user already likes. These accelerate the session but are not required.
- **Constraints (optional).** Existing logo, an established product color, a partner brand the user has to coordinate with.

## Step-by-step procedure

### Step 1 — Open or create GL-003

Path: `Team Knowledge/Guidelines/GL-003-design-system.md`. The file ships as an empty template.

Read it through with the user. Confirm which sections are still empty vs. already populated. The session focuses on the empty (or to-be-changed) sections.

### Step 2 — Section: Identity

Prompts:

1. **Brand name.** "What's the canonical name? Capitalization, spacing, punctuation locked from now on?"
2. **Voice/tone descriptors.** "Pick three to five adjectives that describe how this brand sounds when it speaks. Direct? Warm? Playful? Technical? Restrained? Aim for combinations that aren't generic — 'professional' and 'innovative' are useless. 'Calm but direct' is useful."
3. **Audience.** "One sentence on who you're speaking to. Not a demographic — a *person*. The audience constrains every later choice."

Write the answers verbatim into GL-003 §Identity, replacing the placeholders.

### Step 3 — Section: Color palette

Prompts:

1. **Primary.** "Your signature color. The one a viewer should associate with this brand at a glance. Hex value? If you don't have one, name two-to-three options and pick."
2. **Secondary.** "The supporting color. Used for backgrounds, surfaces, secondary CTAs. Often a neutral that complements the primary."
3. **Accent.** "The punctuation color. Used sparingly — the brass-moment of any composition. Often warm, often saturated."
4. **Neutrals.** "The canvas, the text, the borders. A warm or cool gray ramp. Five-to-seven steps from light to dark."
5. **Status (optional).** "Do you need success, warning, error, info colors? If your deliverables are mostly editorial (essays, decks, social), probably no. If they're product-flavored (UI, dashboards), yes."

For each color: hex value + one-line intent comment. Write into GL-003 §Color palette.

If the user is stuck, offer two-to-three concrete pairings as choices, never an open palette of possibilities.

### Step 4 — Section: Typography

Prompts:

1. **Heading font.** "Display face for titles and section heads. Serif (editorial character), heavy sans (modern punch), or display script (ornament)? Specific family in mind?"
2. **Body font.** "Workhorse face for paragraph copy. Almost always a clean sans (Inter, Geist, Source Sans, system-ui) for legibility. Pick one and lock it."
3. **Mono font (optional).** "Code, numerics, tabular data. JetBrains Mono, Geist Mono, IBM Plex Mono, system mono. Skip if the brand never shows code or tabular data."

For each font: family name, weights used, one-line role description ("Inter Bold 700 for H1, Inter Regular 400 for body, Inter Medium 500 for emphasis"). Write into GL-003 §Typography.

### Step 5 — Section: Spacing scale

Prompts:

1. **Base unit.** "4px or 8px. 4px gives finer-grained control; 8px is more opinionated and harder to drift from."
2. **Tokens.** "Six tokens — `xs`, `sm`, `md`, `lg`, `xl`, `2xl` — mapped to multiples of the base unit. Default ladder: 4, 8, 16, 24, 32, 48 (4px base) or 8, 16, 24, 32, 48, 64 (8px base)."

Write into GL-003 §Spacing scale.

### Step 6 — Section: Imagery style

Prompts:

1. **Photography style.** "Editorial (dramatic, intentional), candid (real, casual), studio (clean, isolated subject), lifestyle (people in scenes), or no photography at all. If yes, link one example image you love."
2. **Illustration style.** "Line (thin strokes, no fill), painted (watercolor, brushstroke), flat (geometric, solid colors), 3D, mixed, or none. Link one example."
3. **Icon style.** "Line, filled, two-tone, hand-drawn, or none. Most brands pick one icon family (Lucide, Phosphor, Heroicons, Tabler) and lock it."

Write into GL-003 §Imagery style. This section drives Pixel's prompt construction directly.

### Step 7 — Section: Voice samples

Ask the user to write three short example sentences in the brand's intended voice. Captions, headlines, or one-liners. Concrete, not abstract.

If the user is stuck, offer this prompt: "Write the first sentence of an email to your ideal customer. Now write a button label. Now write a one-line product tagline."

Write the three verbatim into GL-003 §Voice samples. These are the canonical reference for any caption, headline, or body copy a creative agent writes.

### Step 8 — Confirm and lock

Read the populated sections back to the user. Confirm:

- Every value has an intent comment.
- No section was filled with "sensible defaults" the user didn't actually pick.
- Sections the user explicitly chose to skip are clearly marked as empty (not partially populated).

Save the file.

### Step 9 — Announce downstream impact

Tell the user (and Larry):

- Charta and Pixel now read GL-003 on every task.
- Any in-flight deliverable that ran in fallback mode is flagged for re-render against the new GL-003.
- Old deliverables are stale; they get re-rendered next time they're touched, not bulk-rebuilt now.
- If a creative request lands and a section is still empty, the agent flags it back and Iris extends GL-003 in a follow-up session.

### Step 10 — Session-log entry

Write `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<agent-id>_<topic-slug>.md` with type `end-of-session`. Capture:

- Which sections were populated this session
- The user's specific choices and the reasoning they gave
- Sections explicitly left empty for now
- Any in-flight deliverables that need a re-render
- Any cross-agent impact (Charta and Pixel both pick up the new tokens automatically; no re-config needed)

## Common mistakes to avoid

- Pre-populating GL-003 with "sensible defaults" before the user has chosen. The worst outcome — silent choices the user never made.
- Leaving a section half-populated without flagging. A partial GL-003 is more dangerous than an empty one because agents will use the populated values and silently default the missing ones.
- Skipping the intent comment ("`#1A1A1A` — primary background, used for app canvas and dark-mode hero sections"). When values evolve, the intent is the anchor that keeps meaning stable.
- Letting the user pick generic adjectives ("professional", "innovative", "modern") for voice/tone. Push for specificity — combinations that aren't generic.
- Editing GL-003 without a session-log entry. Schema changes are documented; the session-log is the changelog.
- Letting Charta or Pixel work blind because "we'll do GL-003 later". The first creative request is the right moment to populate.
