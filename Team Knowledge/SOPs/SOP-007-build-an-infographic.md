# SOP-007 - Build an Infographic

- **Status:** Active (since v1.6.0)
- **Default owner:** Charta
- **Reusable by any agent.** This is a skill, not a 1:1 ownership. Pixel can invoke this SOP when stylizing on top of a structural draft. Penn can invoke it to lay out a captured idea. Any specialist who needs to turn information into a single-image, scannable layout follows this procedure.
- **Triggered by:** "make me an infographic", "lay this out as one image", "I need a flowchart / decision tree / swimlane / timeline / hub-and-spoke / quadrant matrix", "make a one-pager", "create a cheat sheet", "draft the layout, then we'll polish it".
- **References:** [[GL-003-design-system]], [[GL-001-file-naming-conventions]], [[Team/Charta - Infographic Designer/AGENTS]], [[SOP-008-generate-a-styled-image]] (for the stylization handoff).

## Purpose

Turn a brief — a topic, a comparison, a process, a set of steps, a hierarchy — into a single scannable image (or a small carousel) that communicates the point in under ten seconds. The output is production-ready PNG (or PDF) built from HTML/CSS/SVG and rendered via a headless browser.

The procedure is structural. It does not invent content. The user (or Penn for capture-shaped inputs) provides the text; this SOP lays it out.

## What this SOP does not do

- Does not generate photographic, illustrated, or AI-rendered finishes. That is [[SOP-008-generate-a-styled-image]] (Pixel's skill). When a deliverable needs both layout and stylization, run SOP-007 first, then hand off to SOP-008.
- Does not author the design system itself. That is Iris's territory in [[SOP-009-author-a-design-system]].
- Does not write copy. The text is an input, never invented during layout.

## Inputs

- **The brief:** what the infographic is *about*. One sentence is enough; three is better.
- **The content:** the actual rows / nodes / steps / cells. Plain text the layout will hold.
- **The format:** single image, carousel, PDF. If unclear, ask.
- **The aspect:** 16:9 landscape (slide / hero), 1:1 square (social), 1080x1350 (LinkedIn carousel), 1600x900 (X), letter / A4 (PDF). Default to the platform the user names.

## Step-by-step procedure

### Step 1 — Read the design system

Open [[GL-003-design-system]]. Confirm the sections this task needs are populated:

- **Color palette** — for any colored block, border, accent.
- **Typography** — for heading and body type roles.
- **Spacing scale** — for padding, margins, gaps.
- **Imagery style** (only if icons or images are embedded).

If a needed section is empty, **stop**. Two paths:

1. Route to Iris first (run [[SOP-009-author-a-design-system]] for the missing section). Preferred for any non-trivial creative work.
2. Proceed in flagged "no-style fallback" mode: neutral grayscale, system font stack, default 8px spacing. The deliverable explicitly notes "GL-003 §X not populated; revisit when populated."

### Step 2 — Pick the layout shape

The shape decision drops out of the content shape:

| Content shape | Layout |
|---|---|
| 2-3 columns, N rows of attributes | Comparison table (CSS Grid, explicit column tracks) |
| N items, same internal shape (icon + title + 1-2 sentences) | Feature grid (CSS Grid 2-4 cols, equal-height cells) |
| Linear sequence of steps | Process flow (Flex column or row + SVG straight lines) |
| Branching steps with yes/no | Decision tree (Flex rows + diamond clip-path + SVG elbows) |
| Nodes that loop back to start | Circular flow (absolute positioning + SVG arcs) |
| Center node + N peripheral nodes | Hub-and-spoke (absolute positioning + SVG straight or dashed lines) |
| Two axes, four cells | 2x2 matrix / quadrant (CSS Grid 2x2) |
| Time-ordered events | Timeline (Flex row or column + SVG line + dots) |
| Roles (rows) × steps (columns) | Swimlane (CSS Grid, rows=lanes + SVG cross-lane elbows) |
| Too dense for one image, but each chunk self-contained | Carousel (one HTML file per slide; render each to PNG) |

If two shapes fit, default to the simpler one. A flowchart that wants to be a list should be a list.

### Step 3 — Density check

- Single image: 5-9 distinct content blocks. Beyond 9, split.
- Carousel slide: 1-3 content blocks per slide.
- Comparison table: 4-7 rows × 2-4 columns. Beyond, unreadable.

If the content exceeds the budget, propose a split before laying out. Two clean infographics beat one cluttered one.

### Step 4 — Build the HTML/CSS/SVG

Two-layer architecture for any diagram:

- **Layer 1 (HTML/CSS):** Nodes positioned via CSS Grid, Flexbox, or absolute positioning. Card surfaces, text, icons. Read color/type/spacing from GL-003 tokens (literalize the values into CSS at author time, but pull them from GL-003 — never invent).
- **Layer 2 (SVG overlay):** `position: absolute`, same dimensions as Layer 1, `z-index: 5`. All connectors, arrows, curved paths. Reusable `<marker>` definitions in `<defs>`.

Connector quick reference:

```svg
<!-- Always markerUnits="userSpaceOnUse" — never "strokeWidth" -->
<marker id="arrow" markerWidth="12" markerHeight="9"
        refX="11" refY="4.5" orient="auto" markerUnits="userSpaceOnUse">
  <polygon points="0 0, 12 4.5, 0 9" fill="var(--accent)"/>
</marker>
```

- Straight: `<line>` with `marker-end`
- Elbow: `<path d="M x1 y1 L midX y1 L midX y2">`
- Curved: `<path d="M x1 y1 Q cx cy x2 y2">` (quadratic) or `C` (cubic)
- Arc: `<path d="M x1 y1 A rx ry 0 0 1 x2 y2">`
- Dashed: add `stroke-dasharray="8,6"`

Node shape defaults:
- Rectangle: `border-radius: 12px`. Standard.
- Small chip: `border-radius: 4px`. Status, badges.
- Circle: `border-radius: 50%` on perfect-square divs only. Reserved for hub-and-spoke center and cycle nodes.
- Diamond: `clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)`. Decision-only.
- Grouped container: `border: 1px dashed`, label positioned `top: -12px` over the canvas.

Pill shapes (`border-radius: 9999px`) are banned. Avatar/cycle exception applies to perfect-square divs only.

### Step 5 — Render to PNG (or PDF)

Use a headless browser (Puppeteer, Playwright, Chromium-headless). The render command:

```bash
# Pseudocode — adapt to whichever runner the project uses.
node render.js \
  --input ./infographic.html \
  --output ./Deliverables/YYYY-MM-DD-<slug>/infographic.png \
  --width 1280 --height 720 \
  --device-scale-factor 2
```

For PDF: `--pdf` flag, `--format Letter` (or `A4`).

Devic-scale-factor 2 produces retina-quality outputs. Drop to 1 for mobile-only deliverables.

### Step 6 — Quality check

Before delivery, scan the rendered output against these checks:

1. **Scannable in 10 seconds?** A reader who hasn't seen this content gets the point at a glance.
2. **Hierarchy clear?** Three type-size levels max. The eye lands on the title first, then the section, then the body.
3. **Brand consistent?** Every color, font, and spacing value traces to GL-003. No drift.
4. **Connector geometry right?** Arrows point where they should. No overlaps. Elbow turns at right angles. Curves don't kink.
5. **No pills.** Unless the avatar/cycle exception applies.
6. **Text legible at delivery size?** If the deliverable is a thumbnail, type at 1× zoom on a phone.

If any check fails, return to Step 4. A failed deliverable doesn't ship.

### Step 7 — Deliver

Save to `Deliverables/YYYY-MM-DD-<topic-slug>/` (or to a path the user designated). Source HTML/CSS/SVG stays alongside the rendered output so the asset is regeneratable.

Show the user inline (markdown image embed) for review. Do not move to the final location until approved.

### Step 8 — (Optional) Hand off to Pixel for stylization

If the deliverable was structurally complete but needs photographic, illustrated, or AI-generated finishing on top of the layout, hand off to Pixel via [[SOP-008-generate-a-styled-image]]. Pixel takes the rendered HTML or PNG as a structural reference and produces the stylized final.

### Step 9 — Session-log entry

Write `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<agent-id>_<topic-slug>.md` with type `end-of-session`. Capture:

- Brief and content shape
- Layout chosen and why
- Which GL-003 tokens consumed
- Any toolkit pattern worth reusing
- Whether stylization handoff to Pixel happened
- Any flag for stale GL-003 sections

## Common mistakes to avoid

- Skipping the GL-003 read at Step 1. The infographic ends up off-brand.
- Hardcoding values into the source HTML without tracing them to GL-003. The next render against an evolved palette stays stale.
- Cramming 12 blocks into a single image because "the user said one infographic". Two clean infographics always beat one cluttered one.
- Pure CSS connectors for diagrams. SVG overlay always for connectors.
- Inventing diamond shapes for decoration. Diamond is decision-only; its outgoing arrow carries the brass-moment.
- Skipping the inline review and writing straight to the final Deliverables path.
- Forgetting the session-log entry. The next agent who runs SOP-007 needs the breadcrumbs.
