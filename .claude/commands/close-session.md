---
name: close-session
description: "Close out the current myPKA session: sweep open items, write a session log, run a Librarian pass, optionally graduate insights into Team Knowledge."
user_invocable: true
---

# /close-session — Close out the session

You are Larry. Run these steps in order before ending the session.

This scaffold is markdown-only — no database, no Supabase, no external
services. The session log itself is the single source of truth for what the
team did. Sweep open items into the log; do not try to write to any external
tracker.

## 1. Sweep open items into the session log

Review this session for anything uncompleted that should persist across
sessions:

- Delegations that didn't return (specialist still working / blocked).
- Questions the user asked that weren't resolved.
- Reminders or follow-ups Larry committed to.
- Inbox items not yet processed (`Team Inbox/`).
- Decisions the user deferred ("come back to this in X days").

These go into the **Open threads** section of the session log entry as
checkbox items. Each one names the owner inline.

If there are no open threads, write `_(none — clean close)_` under that
section.

## 2. Write the session log

Create the entry at:

```
Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<session-id>.md
```

- `YYYY-MM-DD-HH-MM` — current datetime to the minute.
- `<session-id>` — short kebab-case slug derived from the session's main
  theme. See [[GL-001-file-naming-conventions]].
- Auto-create the `YYYY/` and `YYYY/MM/` subfolders if they don't exist.

Use the structure in `Team Knowledge/session-logs/_template.md`. Required
frontmatter:

- `agent_id: larry`
- `session_id: <slug>`
- `timestamp: <ISO 8601 UTC>`
- `type: close-session`
- `linked_sops`, `linked_workstreams`, `linked_guidelines` — arrays of any
  Team Knowledge files this session touched or relied on.

Required body sections, in order: Context, What we did, Decisions made,
Insights, Realignments, Open threads, Next steps, Cross-links.

Cross-link the previous session log if there is one — find the most recent
file in `Team Knowledge/session-logs/YYYY/MM/` (current and prior month if
needed) and reference it via `[[<filename-without-extension>]]` in the
Cross-links section.

## 3. Librarian pass

Scan your myPKA for structural drift introduced this session:

- **Broken `[[wikilinks]]`.** Either create a stub at the link target or fix
  the link path. If intent is unclear, flag it in the session log under
  Open threads instead of guessing.
- **Orphaned files.** Files added this session that are not referenced by any
  `INDEX.md` or `[[wikilink]]`. Add them to the appropriate `INDEX.md`.
- **Missing `INDEX.md` entries.** Anything new in `PKM/`, `Team Knowledge/`,
  or `Deliverables/` should appear in its section's `INDEX.md`.
- **SSOT violations.** The same fact written into two files. Pick the
  canonical home, replace duplicates with `[[wikilinks]]`, note the fix in
  the session log under "SSOT / structural fixes" (add this section to the
  body if you used it).

Do not edit the user's PKM content for tone or correctness. Only fix
structural drift. Flag content drift for the user instead of resolving it
yourself.

## 4. Graduate set-in-stone insights (optional)

If this session surfaced something that is now repeatable and durable, move
it from session-log territory into the right Team Knowledge home:

- Repeatable atomic procedure → new `Team Knowledge/SOPs/SOP-NNN-<slug>.md`.
- Recurring multi-agent orchestration → new
  `Team Knowledge/Workstreams/WS-NNN-<slug>.md`.
- Static reference rule → new
  `Team Knowledge/Guidelines/GL-NNN-<slug>.md`.

Numbering follows [[GL-001-file-naming-conventions]] (zero-padded, no skips).
Update the corresponding `INDEX.md` and add `[[wikilinks]]` from the session
log to the new file.

If there is nothing to graduate, skip this step.

## 5. Sign off

Tell the user the session is closed and summarize:

- Session log written: `<path>`
- Open threads count and quick titles.
- Anything graduated to SOPs / Workstreams / Guidelines.
- Anything flagged for the user to resolve.

End the session.
