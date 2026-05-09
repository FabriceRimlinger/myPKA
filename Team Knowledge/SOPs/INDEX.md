# SOPs - Index

**SOPs are agent skills.** Each SOP is a canonical procedure — a step-by-step recipe for one job. They are LLM-agnostic and reusable across agents: an SOP has a **default owner** (the specialist who runs it most often), but any agent can invoke an SOP when they need its procedure. Think of SOPs the way Claude skills work — discrete, named, callable.

Filename pattern: `SOP-NNN-<title>.md`. See [[GL-001-file-naming-conventions]] for slug rules. Numbering follows authorship order, not topic — gaps are intentional and reserve slots for future agents.

## Active SOPs

| SOP | Title | Default owner | Description |
|---|---|---|---|
| SOP-001 | [[SOP-001-how-to-add-a-new-specialist]] | Nolan | Step-by-step procedure to draft and onboard a new team specialist. References [[GL-001-file-naming-conventions]]. |
| SOP-002 | [[SOP-002-convert-mypka-to-sqlite]] | Silas (run by the user via paste-into-LLM prompt) | Generate a SQLite mirror of your myPKA on demand. Markdown stays canonical; SQLite is a derived performance layer. Body is a paste-into-LLM prompt. |
| SOP-007 | [[SOP-007-build-an-infographic]] | Charta | Structure-first content design via HTML/CSS/SVG, render to PNG/PDF via headless browser. Includes layout-shape decision tree, density rules, and the two-layer (HTML+SVG) diagram architecture. Reads from [[GL-003-design-system]]. |
| SOP-008 | [[SOP-008-generate-a-styled-image]] | Pixel | Multi-reference image generation with three capability paths: local image-gen, Mack-wired external API/MCP, fallback design-brief-for-human. Five-part prompt construction, visual quality scoring, variant strategy. Reads from [[GL-003-design-system]]. |
| SOP-009 | [[SOP-009-author-a-design-system]] | Iris | Guided session walking the user through populating [[GL-003-design-system]]: identity, color palette, typography, spacing scale, imagery style, voice samples. Decision-led, not prescriptive — the user picks; Iris asks. |
| SOP-010 | [[SOP-010-audit-content-for-design-system-compliance]] | Iris | Verify visual deliverables against [[GL-003-design-system]]. Per-deliverable audit checklist, severity classification, report format. Audits surface violations; the user decides what to fix. |

*Reserved (genuinely open for future agents):* SOP-003, SOP-004, SOP-005, SOP-006. Do not back-fill these slots without coordinating across the team.

## How to add a new SOP

1. Pick the next unused number (`SOP-NNN`) — by authorship order, not topic. Don't reuse reserved numbers.
2. Filename: `SOP-NNN-<kebab-case-title>.md`.
3. Header includes the default owner, status, triggers, references, and an explicit "Reusable by any agent" note — the SOP is a skill, not 1:1 ownership.
4. Reference [[GL-001-file-naming-conventions]] and any other Guideline instead of duplicating its content.
5. Add a row to this index.
