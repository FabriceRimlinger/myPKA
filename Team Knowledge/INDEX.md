# Team Knowledge - Master Hub

This is the operations side of your myPKA. It holds the team's procedures, orchestrations, reference material, and session history. The user's personal knowledge lives in [[PKM/INDEX]].

## Sections

- **[[Team Knowledge/SOPs/INDEX|SOPs]]** — agent skills. Canonical step-by-step procedures, one job per file, LLM-agnostic and reusable across agents. Each SOP has a default owner, but any agent can invoke it. Think of SOPs the way Claude skills work. Filenames: `SOP-NNN-<title>.md`.
- **[[Team Knowledge/Workstreams/INDEX|Workstreams]]** — multi-agent compositions. Recurring orchestrations where more than one specialist collaborates. Workstreams string SOPs together — think of them the way Claude plugins compose skills. Emergent: the scaffold ships only canonical day-1 flows; new Workstreams get authored when a pattern repeats. Filenames: `WS-NNN-<title>.md`.
- **[[Team Knowledge/Guidelines/INDEX|Guidelines]]** — general rules every agent reads. Static constraints (naming, frontmatter, design system) that SOPs and Workstreams `[[wikilink]]` to rather than duplicate. Filenames: `GL-NNN-<title>.md`.
- **session-logs/** — append-only record of every working session, written by Larry. Path: `session-logs/YYYY/MM/YYYY-MM-DD-<slug>.md`.

## Taxonomy in plain English

- An **SOP** is an agent skill. It answers "how do I do X?" in clear steps. Like a Claude skill — discrete, named, callable. Default owner runs it most often; any agent can invoke it.
- A **Workstream** is a multi-agent composition. It answers "how do we deliver X together, recurring?" Like a Claude plugin — strings skills into a flow. Ships only when the pattern is canonical; new ones emerge from repeated session-log patterns.
- A **Guideline** is a general rule. It answers "what is the rule for X?" Static reference every relevant agent reads. Never a procedure.

When in doubt: write a Guideline first if the rule is static. Write an SOP if the procedure has steps and one default owner. Write a Workstream only when more than one specialist is involved AND the pattern repeats.

## SSOT applies here too

If naming rules belong in [[GL-001-file-naming-conventions]], do not restate them inside an SOP or Workstream. Link to the Guideline instead.

## Cross-session learnings

When the team learns something durable across sessions, Larry appends it to a "Cross-session learnings" section at the bottom of this file. Session-specific notes stay in the session log under `session-logs/YYYY/MM/`.

### Cross-session learnings

(empty on day one - Larry fills this as the team operates)

## Active session log

The current session log lives in `session-logs/YYYY/MM/`. Larry writes one per session at close.
