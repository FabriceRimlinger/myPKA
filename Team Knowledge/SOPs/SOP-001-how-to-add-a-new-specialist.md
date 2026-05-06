# SOP-001 - How to Add a New Specialist

- **Owner:** Nolan
- **Co-owner for research step:** Pax
- **Triggered by:** user request to hire, or Larry detecting a gap
- **References:** [[GL-001-file-naming-conventions]], [[Team/agent-index]]

## Purpose

Add a new specialist to the team in a way that keeps the routing table clean, the AGENTS.md contracts consistent, and the SSOT Golden Rule intact. Every hire gets a world-class research brief from Pax before Nolan drafts the contract - this is how the team avoids generic, AI-flavored specialists and ships ones that mirror what the best humans in that role actually do.

## Steps

### 1. Capture the need (Larry -> Nolan)

Larry routes the hiring request to Nolan with a one-sentence brief: what the new specialist will do that no current specialist can. If Nolan cannot finish that sentence with the user, the role is not ready.

### 2. Brief Pax for the research pass (Nolan -> Pax)

Nolan writes a research brief to Pax. Required questions:

- What does the best-in-world version of this specialist actually do, day to day?
- What are the core competencies, and what are the anti-patterns (things mediocre versions of this role do that the team should explicitly avoid)?
- What deliverables does this role produce? What does world-class output look like vs adequate output?
- What boundaries should this role hold? What requests should they refuse or hand back?
- Suggested name candidates (short, distinct, single word, no collision with existing team).

Pax returns a brief sized to the role - usually 400 to 800 words - cited if the research warranted it. The brief lands in `Deliverables/YYYY-MM-DD-<role-slug>-hire-research.md`.

### 3. Pick a name and role (Nolan)

Using Pax's brief, pick:

- **Name:** short, distinct, single word. From Pax's candidates or a variant. Avoid collisions with existing names.
- **Role:** one short phrase. Example: "Frontend Developer" or "Email Marketer."
- **Folder:** `Team/<Name> - <Role>/` (space, hyphen, space). Matches the pattern of the four shipped specialists.

### 4. Draft the AGENTS.md (Nolan)

Create `Team/<Name> - <Role>/AGENTS.md`. Translate Pax's research brief into a contract with these sections:

- **Identity** - name, role, who they report to, operating principle (drawn from Pax's "what world-class does day to day").
- **When Larry routes to them** - the cue patterns.
- **Method or protocol** - how they work, in steps (drawn from Pax's "deliverables and what world-class looks like").
- **Deliverable structure** - what their output looks like.
- **Where they write** - paths and naming. Reference [[GL-001-file-naming-conventions]] for naming.
- **Cross-references** - Guidelines and Workstreams they touch.
- **Scope boundaries** - what they do not do (drawn from Pax's "anti-patterns" and "boundaries").

Keep it short. The shipped four are the template. Do not paste Pax's research brief into the AGENTS.md - the brief stays in `Deliverables/`. The contract references it via `[[wikilink]]` if useful.

### 5. Add the row to agent-index (Nolan)

Edit [[Team/agent-index]]. Add a row with the specialist's name, role, folder link, and the user input patterns that should route to them.

### 6. Update relevant Workstreams (Nolan)

If the new specialist takes part in a recurring orchestration, edit the matching Workstream in `Team Knowledge/Workstreams/` to mention them via `[[wikilinks]]`. Do not duplicate the AGENTS.md content into the Workstream.

### 7. Confirm with the user (Nolan -> Larry -> user)

Show the user the draft AGENTS.md and the updated agent-index, with a one-line summary of what Pax's research surfaced. Make changes only after they approve.

### 8. Log the hire (Larry)

Larry writes a line in the next session log: "Hired <Name> as <Role> after research from Pax. Brief at `[[<research-deliverable-slug>]]`. Contract at `[[Team/<Name> - <Role>/AGENTS]]`." This becomes part of the team's persistent memory.

## Common mistakes to avoid

- Skipping the Pax research step. Even for "obvious" roles, the research surfaces anti-patterns that prevent generic specs.
- Pasting Pax's research brief into the AGENTS.md. The brief is reference material in `Deliverables/`. The AGENTS.md is the contract.
- Duplicating naming rules inside the new AGENTS.md. Link to [[GL-001-file-naming-conventions]] instead.
- Naming the folder with a different separator than other specialists. Always: space, hyphen, space.
- Forgetting to add the row to [[Team/agent-index]]. Larry's routing will skip an unlisted specialist.
- Writing the AGENTS.md in the user's voice instead of as a contract. The file is for the LLM, not the reader.
