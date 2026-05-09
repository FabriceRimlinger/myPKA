# SOP-008 - Generate a Styled Image

- **Status:** Active (since v1.6.0)
- **Default owner:** Pixel
- **Reusable by any agent.** This is a skill, not a 1:1 ownership. Charta can invoke this SOP when a layout draft needs a stylized finish. Penn can invoke it to turn a captured idea into a hero image. Any specialist who needs to produce a styled visual (thumbnail, social image, hero illustration, quote card, multi-reference composite) follows this procedure.
- **Triggered by:** "make me a thumbnail", "stylize this", "create a hero image", "design a quote card", "use these references and generate X", "make this look photographic / illustrated / painted", "the image-gen isn't available in my LLM, can we still do this".
- **References:** [[GL-003-design-system]], [[GL-001-file-naming-conventions]], [[Team/Pixel - Visual Specialist/AGENTS]], [[Team/Mack - Automation Specialist/AGENTS]] (for the connection-half handoff), [[SOP-007-build-an-infographic]] (when stylizing on top of a Charta layout).

## Purpose

Take a brief — a topic, a mood, an intent, optionally a structural draft from Charta — and produce a finished stylized image. The procedure handles three capability scenarios:

1. **Local image-gen available.** The user's LLM can generate images natively. Drive directly.
2. **Local image-gen unavailable.** Mack wires up an external API/MCP (Gemini, OpenAI Images, Flux via Replicate, etc.); Pixel drives the prompt once online.
3. **No image-gen at all (user opts out).** Fallback to "design brief for human" mode: a detailed brief the user can paste into any external tool (Midjourney, DALL-E, Sora, Stable Diffusion, Canva AI, a designer).

The procedure is stylistic. It does not invent text content; the user provides any caption / headline / copy.

## What this SOP does not do

- Does not lay out structural visual content (tables, grids, diagrams). That is [[SOP-007-build-an-infographic]] (Charta's skill). When a deliverable needs structure first, run SOP-007, then SOP-008 for the finish.
- Does not author the design system. That is [[SOP-009-author-a-design-system]] (Iris's skill).
- Does not generate synthetic likenesses of real people. Reference photos required for any real person in frame.

## Inputs

- **The brief:** what the image is *of* and *for*. Subject, intent, where it'll be used (YouTube thumbnail / LinkedIn hero / Instagram square / blog post / quote card).
- **Reference images (when applicable):** identity photos for any real person; visual anchors for palette, composition, mood, material.
- **Aspect / format:** 16:9, 1:1, 9:16 (vertical), 1080x1350 (LinkedIn carousel), 1600x900 (X). Default to the platform.
- **Text content (when applicable):** the caption, headline, or copy that goes into the image. Verbatim from the user.
- **Optional structural draft:** a Charta-rendered HTML layout or PNG that the stylization extends.

## Step-by-step procedure

### Step 1 — Read the design system

Open [[GL-003-design-system]]. Confirm the sections this task needs are populated:

- **Color palette** — for prompt phrasing ("warm walnut and brass on a deep charcoal canvas").
- **Imagery style** — photography / illustration / icon direction. Drives prompt vocabulary directly.
- **Typography** — for any text overlay's type role.
- **Voice samples** — for any caption text the agent writes.

If a needed section is empty, **stop**. Two paths:

1. Route to Iris first (run [[SOP-009-author-a-design-system]] for the missing section). Preferred for any non-trivial creative work.
2. Proceed in flagged "neutral-style fallback" mode: editorial photography default, neutral palette, system font for any text. The deliverable explicitly notes "GL-003 §X not populated; revisit when populated."

### Step 2 — Check image-gen capability

Before drafting the prompt, confirm the path:

- **Path A — Local image-gen available.** The LLM has native image generation, OR an image-gen MCP is already running, OR an API client (`generate-image.py` or equivalent) is already configured with a working API key. Proceed to Step 3.
- **Path B — Local image-gen unavailable, but the user wants to wire something up.** Hand the connection half to Mack:
  > *"To generate this image, we need an image-gen path. I can either drive Gemini's image API, OpenAI Images, Flux via Replicate, or any image-capable MCP server. Mack can wire up whichever you prefer — credentials in `.env`, idempotent retries, the works. Which option do you want, or should Mack pick a sensible default?"*
  Once Mack confirms the connection is online, return to Step 3.
- **Path C — No image-gen, fallback mode.** The user explicitly does not want to wire anything up. Skip to Step 7 (write the design brief).

### Step 3 — Construct the prompt

Every image-gen prompt has the same five parts in order:

1. **Aspect / format.** State at the start, repeat in the requirements list at the end. "Generate a 16:9 landscape image..." Do not let the model default to square unless square is wanted.
2. **Identity anchor (if any real person is in frame).** Reference photo(s) anchored as the first content element. "Using the reference photo of [person], ..."
3. **Scene description.** What's happening, where, who's doing what. Concrete nouns. Save adjectives for step 5.
4. **Material and lighting.** Textures, light source, time of day. This is where GL-003 imagery direction lands directly.
5. **Style modifiers and negatives.** "Editorial photography, shallow depth of field, no text overlay, no logos, no busy background." Negatives are explicit; the model does not infer.

Example skeleton (adapt to GL-003 imagery direction):

```
Generate a 16:9 landscape image.
Subject: <subject described in concrete nouns>.
Setting: <location, time of day>.
Lighting: <directional / soft / dramatic>, <warm / cool> color temperature.
Materials: <walnut, brass, leather, paper — pulled from GL-003 §Imagery style>.
Composition: <focal point, depth, what's in/out of frame>.
Style: <editorial photography / line illustration / flat illustration / painted — pulled from GL-003 §Imagery style>.
Aspect: 16:9 landscape, NOT square.
Negatives: no text overlay, no logos, no <whatever should not appear>.
```

### Step 4 — Pass references explicitly

When using reference images:

- Pass through the model's native reference parameter (`--reference`, `image=`, multimodal input). Do NOT describe the reference in prose and hope the model gets it.
- Identity references go FIRST in the input order.
- Keep the set small and high-signal: 3-5 references for most tasks. Pro models (Gemini 3 Pro Image, etc.) accept up to 14 — only push that high when each reference adds a distinct cue.
- Real photos for real people, always. If there's no reference photo, there's no person.

### Step 5 — Generate

Run the generator. Save raw output to a working folder, not the final location:

```bash
# Pseudocode — adapt to whichever generator is online.
generate-image \
  --prompt "$PROMPT" \
  --reference "$REF1" --reference "$REF2" \
  --aspect landscape \
  --size 1K \
  --output ./working/raw-output.png
```

Generate variants (default 3) for any non-trivial deliverable. Different prompt seeds, slight prompt variations, or different reference orderings — give the user a real choice.

### Step 6 — Score and iterate

For each generated image, score against the visual-quality heuristics:

| Factor | Question |
|---|---|
| Composition | Focal point unambiguous? Eye lands within 0.3 seconds? |
| Clarity | Subject describable in one sentence? |
| Brand fit | Palette, lighting, material match GL-003 §Imagery style? |
| Contrast | Visual punch against the platform background it'll be viewed on? |
| Specificity | Single concrete detail makes it not generic? |
| Type legibility | If text overlay: readable at thumbnail size on a phone? |
| Faithfulness | Delivers on the prompt and the user's request? |

- Fail 3+ → regenerate with sharper prompt.
- Fail 1-2 → targeted iteration (change lighting / tighten composition / adjust palette) without rewriting from scratch.
- Pass all → ready for review.

### Step 7 — (Path C only) Write the design brief

If image-gen is unavailable and the user opted for fallback:

Write a markdown brief at `Deliverables/YYYY-MM-DD-<topic-slug>/design-brief.md`. Sections:

- **Subject & intent** — what the image is and what it's for.
- **Canonical prompt** — the five-part prompt from Step 3, ready to paste into Midjourney / DALL-E / Sora / Canva AI.
- **References** — list paths or URLs of reference images the user should attach.
- **Aspect & size** — final output spec.
- **Style notes** — pulled from GL-003 §Imagery style.
- **Iteration suggestions** — three prompt variations the user can try if the first pass misses.

The brief is the deliverable. The user owns the rendering.

### Step 8 — Inline review before delivery

Show the user inline (markdown image embed for generated; markdown for the brief). Wait for explicit approval. Do **not** move to final location until approved.

If the user wants iteration, return to Step 3-6.

### Step 9 — Deliver

Save the approved image to `Deliverables/YYYY-MM-DD-<topic-slug>/` (or to a path the user designated). Keep the canonical prompt and reference manifest alongside so the asset is regeneratable.

Filename per [[GL-001-file-naming-conventions]]: kebab-case, no spaces, with date prefix where applicable.

### Step 10 — Session-log entry

Write `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<agent-id>_<topic-slug>.md` with type `end-of-session`. Capture:

- Subject and intent
- Which path (A/B/C) was used; if B, which generator Mack wired up
- Canonical prompt and references
- Which GL-003 tokens drove styling
- What the user picked from the variants
- Any prompt pattern worth reusing across future tasks
- Any flag for stale GL-003 sections

## Common mistakes to avoid

- Skipping the GL-003 read at Step 1. The output is off-brand.
- Letting the prompt default to square because the aspect wasn't pinned. State aspect at start AND in requirements list.
- Describing reference images in prose instead of passing them through the model's reference parameter. Wastes prompt budget and produces drift.
- Generating a synthetic likeness of a real person from a description. Always reference photos or no person.
- Skipping the variant generation. A single output is hard to score; three give the user real choice.
- Writing straight to the final Deliverables path without inline review.
- Silently downgrading from local image-gen → fallback brief without naming the Mack-wires-it-up middle option.
- Forgetting the session-log entry. Future runs of SOP-008 lose the breadcrumbs.
