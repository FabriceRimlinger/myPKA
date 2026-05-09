# GL-003 - Design System

> **This Guideline is a general rule every creative agent reads on every relevant action.** Charta, Pixel, and any future visual specialist consume this file at the start of every task. Iris is the default author, but the values are the user's. This Guideline starts empty by design — Iris helps you populate it via [[SOP-009-author-a-design-system]]. Once filled, every creative agent reads from here for consistent style.

> **Empty is honest; placeholder is dangerous.** Until you've actually chosen a value, the placeholder stays. A populated-with-defaults design system silently sets choices you never made. If a section below is still showing `<your brand X>`, the agent reads that as "not yet pinned" and either routes to Iris first or works in flagged fallback mode.

> **Edits are Iris-only.** The user proposes; Iris authors. Charta and Pixel only ever read this file. The split keeps the schema coherent — multiple authors silently drift it.

---

## 1. Identity

- **Brand name:** `<your brand name>`  *(canonical capitalization, spacing, punctuation locked here)*
- **Voice/tone descriptors:** `<adjective 1>`, `<adjective 2>`, `<adjective 3>`  *(three to five; aim for combinations that aren't generic — "professional" and "innovative" are useless; "calm but direct" is useful)*
- **Audience:** `<one sentence on who you're speaking to — a person, not a demographic>`

---

## 2. Color palette

| Role | Token | Value | Intent |
|---|---|---|---|
| Primary | `--color-primary` | `<#hex>` | `<what is this color for? where does it appear?>` |
| Secondary | `--color-secondary` | `<#hex>` | `<intent>` |
| Accent | `--color-accent` | `<#hex>` | `<intent — usually the punctuation color, the brass-moment>` |
| Neutral 0 (lightest) | `--color-neutral-0` | `<#hex>` | `<canvas / page background>` |
| Neutral 1 | `--color-neutral-1` | `<#hex>` | `<elevated surfaces>` |
| Neutral 2 | `--color-neutral-2` | `<#hex>` | `<borders, dividers>` |
| Neutral 3 | `--color-neutral-3` | `<#hex>` | `<muted text>` |
| Neutral 4 | `--color-neutral-4` | `<#hex>` | `<body text>` |
| Neutral 5 (darkest) | `--color-neutral-5` | `<#hex>` | `<headings, high-contrast text>` |
| Status: success | `--color-success` | `<#hex>` | `<success state — optional; delete if not needed>` |
| Status: warning | `--color-warning` | `<#hex>` | `<warning state — optional>` |
| Status: error | `--color-error` | `<#hex>` | `<error state — optional>` |
| Status: info | `--color-info` | `<#hex>` | `<info state — optional>` |

*Each color: hex value + one-line intent. Status row group is optional — delete if your brand is editorial-only and never ships UI states.*

---

## 3. Typography

| Role | Family | Weights | Usage |
|---|---|---|---|
| Heading | `<your heading font>` | `<weights used, e.g. 700>` | `<H1, H2, section headers, hero display>` |
| Body | `<your body font>` | `<weights used, e.g. 400, 500>` | `<paragraph copy, labels, captions>` |
| Mono (optional) | `<your mono font>` | `<weights, e.g. 500>` | `<code, numerics, tabular data — delete row if unused>` |

**Type scale** *(optional but recommended; pick one and lock):*

| Token | Size | Line-height | Use |
|---|---|---|---|
| `--text-display` | `<px or rem>` | `<value>` | Hero / display titles |
| `--text-h1` | `<px or rem>` | `<value>` | Page titles |
| `--text-h2` | `<px or rem>` | `<value>` | Section heads |
| `--text-h3` | `<px or rem>` | `<value>` | Subsection heads |
| `--text-body` | `<px or rem>` | `<value>` | Paragraph copy |
| `--text-caption` | `<px or rem>` | `<value>` | Captions, labels, fine print |

---

## 4. Spacing scale

- **Base unit:** `<4px or 8px>`  *(4px gives finer-grained control; 8px is more opinionated and harder to drift from)*

| Token | Value | Use |
|---|---|---|
| `--space-xs` | `<base × 1>` | Hairline gaps, icon-to-text spacing |
| `--space-sm` | `<base × 2>` | Button padding, dense list items |
| `--space-md` | `<base × 3 or × 4>` | Card padding, paragraph spacing |
| `--space-lg` | `<base × 6>` | Section spacing within a page |
| `--space-xl` | `<base × 8>` | Section spacing on hero / landing |
| `--space-2xl` | `<base × 12>` | Page-level rhythm, between major blocks |

---

## 5. Imagery style

- **Photography style:** `<editorial / candid / studio / lifestyle / none>`
  *Notes:* `<the look you're going for; link one example image if you have one>`
- **Illustration style:** `<line / painted / flat / 3D / mixed / none>`
  *Notes:* `<the look you're going for; link one example>`
- **Icon style:** `<line / filled / two-tone / hand-drawn / none>`
  *Family:* `<Lucide / Phosphor / Heroicons / Tabler / custom — pick one and lock>`

This section drives Pixel's prompt construction directly. The more concrete you are here, the more on-brand Pixel's outputs.

---

## 6. Voice samples

Three short example sentences in your intended voice. These are the canonical reference for any caption, headline, or body copy a creative agent writes.

1. `<your first voice sample sentence>`
2. `<your second voice sample sentence>`
3. `<your third voice sample sentence>`

*If you're stuck: write the first sentence of an email to your ideal customer. Then write a button label. Then write a one-line product tagline.*

---

## How agents use this file

- **At session start, every creative agent reads this Guideline.** Charta and Pixel always; Iris on every authoring or audit task.
- **If a section the task needs is empty (still showing `<placeholder>` values),** the agent does not improvise. Two paths:
  1. Route to Iris via [[SOP-009-author-a-design-system]] to populate.
  2. Work in flagged fallback mode (neutral-style for Pixel, no-style for Charta) and note in the deliverable: "GL-003 §X not populated; revisit when populated."
- **When this Guideline evolves,** in-flight deliverables that referenced the changed section are flagged for re-render. Older deliverables become stale candidates and get re-rendered next time they are touched (boy-scout rule), not bulk-rebuilt on the spot.
- **Audit cadence.** Iris runs [[SOP-010-audit-content-for-design-system-compliance]] when the user requests it, when a token is added, or when drift is suspected. The audit names violations; the user decides which to fix.

## References

- [[SOP-009-author-a-design-system]] — the procedure for populating or extending this Guideline.
- [[SOP-010-audit-content-for-design-system-compliance]] — the procedure for verifying deliverables against this Guideline.
- [[SOP-007-build-an-infographic]] — Charta's skill; reads from this Guideline.
- [[SOP-008-generate-a-styled-image]] — Pixel's skill; reads from this Guideline.
- [[GL-001-file-naming-conventions]] — slug, date, filename rules.
- [[GL-002-frontmatter-conventions]] — entity frontmatter schema.
- [[Team/Iris - Design System Architect/AGENTS]] — Iris's contract; the default author of this Guideline.
