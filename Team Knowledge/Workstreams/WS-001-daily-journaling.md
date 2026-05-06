# WS-001 - Daily Journaling

- **Owners:** Penn (capture and writing), Larry (routing and Librarian pass)
- **References:** [[SOP-001-how-to-add-a-new-specialist]], [[GL-001-file-naming-conventions]], [[Team/Penn - Journal Writer/AGENTS]], [[Team/Larry - Orchestrator/AGENTS]]
- **Trigger:** any user input that contains a thought, observation, encounter, screenshot, photo, or voice note.

## Purpose

Turn raw daily inputs into structured PKM entries. The Journal is the inbox. People, organizations, and topics referenced in journal entries get cross-linked into the CRM and My Life sections.

## Inputs

- **Text** - the user types or pastes a thought.
- **Image** - the user drops a screenshot, photo, or business card.
- **Audio** - the user shares a voice note (transcribed by the LLM if it can; otherwise stored and flagged).

## Choreography

### Step 1 - Larry receives the input

Larry checks the routing cheatsheet in his AGENTS.md. Daily journaling triggers route to Penn.

### Step 2 - Penn writes the Journal entry

- **Path:** `PKM/Journal/YYYY/MM/YYYY-MM-DD-<slug>.md`.
- **Auto-create folders:** if `YYYY/` or `YYYY/MM/` does not exist, Penn creates them.
- **Filename:** ISO date prefix plus a kebab-case slug derived from the day's main theme. See [[GL-001-file-naming-conventions]].
- **Format:** plain markdown. One entry per day. If the day already has an entry, Penn appends a new section to the existing file.

### Step 3 - Penn handles images

- **Path:** `PKM/Images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>`.
- **Auto-create folders:** same rule as Journal.
- **Filename pattern:** see [[GL-001-file-naming-conventions]].
- **Embed in Journal:** Penn embeds the image in the Journal entry with `![[Images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>]]`. The image lives in `PKM/Images/`. The Journal entry references it. Image is never duplicated into the Journal folder.

### Step 4 - Penn cross-links to PKM

For each entity mentioned in the input, Penn routes by type. Use the table below as the routing map:

| Type of mention | Destination folder | Filename pattern | Notes |
|---|---|---|---|
| Person | `PKM/CRM/People/` | `firstname-lastname.md` (or `title-lastname.md`) | Stub if missing. Embed any business card or photo via `![[Images/...]]`. |
| Organization, company, venue | `PKM/CRM/Organizations/` | `<org-slug>.md` | Stub if missing. Cross-link to People who work there. |
| Interest area or recurring subject | `PKM/My Life/Topics/` | `<topic-slug>.md` | Stub if missing. Topics are stable categories of attention, not projects. |
| Habit, ongoing rhythm, routine | `PKM/My Life/Habits/` | `<habit-slug>.md` | Stub if missing. Habits have a cadence and a definition of done. |
| Concrete time-bound effort | `PKM/My Life/Projects/` | `<project-slug>.md` | Stub if missing. Projects have a finish line. |
| Outcome or aspiration with horizon | `PKM/My Life/Goals/` | `<goal-slug>.md` | Stub if missing. Goals link to the Key Element they belong to. |
| Stable life dimension (Health, Family, Career, etc.) | `PKM/My Life/Key Elements/` | `<element-slug>.md` | Stub if missing. Key Elements are dimensions, not goals. |
| Real-world document (passport, contract, certificate, ID) | `PKM/Documents/` | `<doc-slug>.md` | Stub if missing. Document records hold metadata: physical location, digital location, expiry, renewal trigger. The actual file (if scanned) goes under `PKM/Images/` and is embedded. |

For every routed entity:

- If a file already exists at the destination, Penn `[[wikilinks]]` to it from the Journal entry. No restating biographical or contextual details that already live in the canonical file.
- If no file exists, Penn creates a stub at the right path with the minimum content needed for the link to resolve, then `[[wikilinks]]` to it from the Journal entry.

This is how the Journal becomes the connective tissue of the vault.

### Step 4a - Decision rule: stub vs inline mention

Create a stub when the entity has any of:

- A name the user is likely to refer to again (people, organizations, recurring topics).
- A property the user will want to retrieve later (passport expiry, project finish line, goal horizon).
- Cross-cutting relevance (a person who appears in multiple contexts, a topic that recurs).

Inline-mention only (no stub) when:

- The reference is a one-off and clearly will not return (a passing name, a one-time anecdote).
- The user explicitly says "don't file this" or similar.

When in doubt, create the stub. A stub costs nothing. A missing reference costs the wiki its connectivity.

### Step 5 - Larry's Librarian pass at session close

At session close, Larry scans the new Journal entry, the new image (if any), and any newly created CRM or My Life stubs:

- Confirms `[[wikilinks]]` resolve.
- Confirms images sit in `PKM/Images/YYYY/MM/`, not duplicated elsewhere.
- Confirms each new stub is listed in its section's `INDEX.md`.
- Flags SSOT violations to the user.

## What this Workstream does not do

- Does not write business workflows. Those are handled by future specialists hired through Nolan via [[SOP-001-how-to-add-a-new-specialist]].
- Does not produce research reports. Pax handles that.
- Does not edit the user's existing CRM entries. Penn appends, never overwrites, unless the user asks.

## Naming and image rules

All naming questions resolve to [[GL-001-file-naming-conventions]]. If you need to know how to name a slug, what date format to use, or how to handle filename collisions, look there. Do not restate naming rules inside this Workstream.
