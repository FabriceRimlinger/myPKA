# SOP-010 - Audit Content for Design-System Compliance

- **Status:** Active (since v1.6.0)
- **Default owner:** Iris
- **Reusable by any agent.** This is a skill, not a 1:1 ownership. Charta and Pixel can self-audit before delivering. The user can request a full deliverables sweep. Any specialist who needs to verify visual consistency against [[GL-003-design-system]] can run this procedure.
- **Triggered by:** "audit my deliverables", "are my slides on-brand", "is this consistent with my brand", "the visuals look inconsistent across decks", new GL-003 token added that needs propagation, periodic sweep.
- **References:** [[GL-003-design-system]] (the SSOT being audited against), [[SOP-009-author-a-design-system]] (the authoring partner skill), [[Team/Iris - Design System Architect/AGENTS]].

## Purpose

Verify that visual deliverables (infographics, images, slide decks, social cards, PDFs) read cleanly from [[GL-003-design-system]]. Surface drift — values that don't trace to a token, fonts off the stack, spacing off the scale, imagery off the style guide. Recommend fixes; never auto-rewrite.

## What this SOP does not do

- Does not author or change GL-003. That is [[SOP-009-author-a-design-system]].
- Does not auto-fix the user's deliverables. Audit, report, recommend. The user (or Charta/Pixel under user direction) applies fixes.
- Does not audit content correctness — copy errors, factual claims, methodology drift. Out of scope. Visual-only.

## Inputs

- **Scope.** Single deliverable, a folder of deliverables, the entire `Deliverables/` tree, or a specific date range. The user names the scope; if unclear, ask.
- **Severity threshold.** Default: report all violations. Optional: "only HIGH severity" if the user wants a triage view.

## Step-by-step procedure

### Step 1 — Read the SSOT

Open [[GL-003-design-system]]. Confirm which sections are populated. The audit scope is bounded by the populated sections — if §Imagery style is empty, the audit cannot flag imagery-style drift, only flag that the section is empty and any creative work made imagery decisions blind.

If the user requested an audit and GL-003 is mostly empty, the audit reframes: the deliverable here is "GL-003 needs populating; here's the list of decisions deliverables already made that should be pinned." Route to [[SOP-009-author-a-design-system]] to populate first; resume audit afterward.

### Step 2 — Inventory the deliverables

List every file in scope. For each, identify the type:

- HTML/CSS source (Charta's structural layouts)
- Rendered PNG/PDF (Charta or Pixel outputs)
- Generated images (Pixel outputs)
- Markdown deliverables that embed images

Static text files (`.md` reports without images) are skipped. The audit is visual.

### Step 3 — Per-deliverable audit checklist

For each deliverable in scope, run these checks:

1. **Color compliance.** Are the colors in the deliverable in GL-003 §Color palette? Off-palette hexes are flagged.
   - For HTML/CSS sources: grep for hex/rgba/oklch values; cross-reference each against §Color palette.
   - For rendered images: visual inspection or a color-pick of dominant areas.
2. **Font compliance.** Are the fonts in the deliverable in GL-003 §Typography? Off-stack faces are flagged.
   - HTML sources: grep for `font-family` declarations; cross-reference against §Typography.
   - Images with text: visual identification (or note "font unidentifiable from raster").
3. **Spacing compliance.** Are spacing values multiples of the base unit per GL-003 §Spacing scale? Arbitrary `12px` in an 8px-base scale is flagged.
   - HTML sources: grep for `padding`, `margin`, `gap` values; check against the token ladder.
   - Images: not auditable from raster.
4. **Imagery compliance.** Does the imagery match GL-003 §Imagery style?
   - Photography style flag if a brand whose imagery direction is "flat illustration" ships an editorial photo.
   - Icon family flag if multiple icon styles appear in the same deliverable.
5. **Voice compliance.** Does any embedded copy match GL-003 §Voice samples?
   - Quote cards, captions, headlines: read against the canonical voice.
   - Generic-corporate copy in a brand whose voice is "playful and direct" is flagged.
6. **Status semantic.** Are status colors (success/warning/error/info) used semantically? A success-green used as a generic accent is flagged.
7. **GL-003 stale flag.** Does the deliverable's session-log entry note "fallback no-style mode used"? If yes, the deliverable is a known-stale candidate for re-render.

### Step 4 — Severity classification

For each violation, classify:

- **HIGH.** Off-palette color in a primary brand surface; off-stack font in a hero deliverable; voice drift in a customer-facing piece.
- **MEDIUM.** Arbitrary spacing value; icon family inconsistency within a deck.
- **LOW.** Minor color drift in a low-visibility area; spacing off by one unit step.

A deliverable can carry multiple violations. The deliverable's overall severity is the highest single violation's severity.

### Step 5 — Write the audit report

Path: `Deliverables/YYYY-MM-DD-design-system-audit.md`.

Structure:

```markdown
# Design System Audit — YYYY-MM-DD

## Scope
- <files / folders / date range audited>
- GL-003 sections audited against: <list of populated sections>
- GL-003 sections empty (audit blind to these): <list>

## Summary
- N deliverables audited
- M violations found across L deliverables
- Severity breakdown: H high, M medium, L low

## Violations

### <deliverable-1-path>
| Severity | Category | Detail | Recommendation |
|---|---|---|---|
| HIGH | Color | `#3D6B9F` not in §Color palette | Replace with `--color-primary` or add to §Color palette via [[SOP-009-author-a-design-system]] |
| MEDIUM | Spacing | `13px` not on 4px scale | Replace with `var(--space-md)` (16px) |
...

### <deliverable-2-path>
...

## Stale-flag candidates

Deliverables whose session-log entry noted "fallback no-style mode used":
- <path> — flag in session-log: <date>
- <path> — flag in session-log: <date>

These are eligible for re-render against the current GL-003 next time they are touched (boy-scout rule).

## Recommendation

<one-paragraph next-step recommendation>
```

### Step 6 — Surface to user; never auto-fix

Present the report to the user (via Larry). Ask which violations they want fixed and in what order.

For each approved fix:

- **Charta** re-renders any HTML/CSS deliverable against the corrected tokens via [[SOP-007-build-an-infographic]].
- **Pixel** regenerates any image deliverable with corrected prompts and references via [[SOP-008-generate-a-styled-image]].
- **Iris** extends GL-003 if the violation surfaced a missing token via [[SOP-009-author-a-design-system]].

Iris does **not** silently rewrite the user's deliverables. The audit names; the user decides; Charta/Pixel/Iris execute.

### Step 7 — Session-log entry

Write `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<agent-id>_audit-<topic-slug>.md` with type `end-of-session`. Capture:

- Audit scope and report path
- Violation counts by severity
- Which violations the user chose to fix
- Which violations were deferred
- Any GL-003 gaps the audit surfaced (route to SOP-009 for follow-up)

## Common mistakes to avoid

- Auditing against an empty GL-003. Without a populated SSOT, there's nothing to audit against — the deliverable is "populate GL-003 first", not "here's a violation list".
- Auto-fixing the user's deliverables. The audit names; the user decides.
- Treating GL-003 stale-flag candidates as violations. They are *deliberately* flagged in the deliverable; the boy-scout rule covers them on next touch.
- Conflating visual drift with content drift. The audit is visual-only. Copy errors, factual claims, methodology drift are out of scope.
- Skipping the per-deliverable severity classification. A flat list of violations without triage is unactionable.
- Forgetting the session-log entry. The next audit needs the breadcrumbs.
