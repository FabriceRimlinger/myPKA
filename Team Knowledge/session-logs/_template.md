---
agent_id: larry
session_id: <kebab-case-session-id>
timestamp: 2026-05-09T15:00:00Z
type: close-session  # close-session | mid-session-insight | realignment | proactive
linked_sops: []           # ["SOP-001-how-to-add-a-new-specialist"]
linked_workstreams: []    # ["WS-001-daily-journaling"]
linked_guidelines: []     # ["GL-001-file-naming-conventions"]
---

# <Session theme in one line>

## Context

What was the session about. One or two sentences. What did the user come in
asking for, what state was your myPKA in.

## What we did

Bulleted list of concrete actions the team took during the session. Each
item names the specialist who did the work.

- Penn captured the dinner notes into `2026-05-04-first-day.md`.
- Pax returned a triangulated brief on X to `Deliverables/...`.
- Larry consolidated two duplicate facts about Y into `[[<canonical-file>]]`.

## Decisions made

Decisions that change how the team will operate going forward. Not opinions —
decisions. Each decision states the question and the resolution.

- **Question:** Should we keep expansion-spec at root or move it under Expansions?
  **Decision:** Move it under `Expansions/docs/` so all Expansion material lives
  in one folder.

## Insights

Things the team learned that are worth remembering across sessions but are not
yet ready to graduate to an SOP, Workstream, or Guideline. If an insight here
keeps showing up across multiple session logs, Larry graduates it.

- ...

## Realignments

If the user pushed back on a plan or corrected a misread, capture the
correction verbatim. This is persistent team memory — the next session reads
it and behaves accordingly.

- _(none this session)_

## Open threads

Anything not closed during the session that the next session needs to pick up.
For close-session entries: this is what got swept into the user's working
memory or flagged for follow-up. Never let an open thread die silently — if
it's truly dead, write that explicitly here and close it.

- [ ] Follow up with Pax on the Y comparison after {{USER_NAME}} reviews v1.
- [ ] {{USER_NAME}} to confirm whether Z gets renamed before v1.3.

## Next steps

What the team is set up to do at the start of the next session. Concrete and
short. Not a wishlist.

- ...

## Cross-links

- `[[<previous-session-log-slug>]]` — reference to the closest related prior
  session log, if any. Larry adds this on close-session.
