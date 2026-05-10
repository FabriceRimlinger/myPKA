# SOP — Write a Session Log

- **Owner:** Larry (default), any specialist agent (when running independently)
- **Triggered by:** end of a working session, mid-session checkpoint, end-of-day
- **Output:** a new file in `Team Knowledge/session-logs/<YYYY>/<MM>/`
- **References:** [[SOP-write-journal-entry]] (for cross-session insights), [[SOP-create-task]] (for queued follow-up work)

## Purpose

Session logs are the chronological resumption surface for the team. When tomorrow's session needs to know what yesterday's session did and decided, the session log is where that lives. They are the connective tissue between tasks (which point at session logs via `linked_session_logs`) and journal entries (which often link back to the session that birthed them).

The format already exists in v1.x and v2.1.0 of the scaffold. v2.0.0 changes nothing about it. This SOP exists so newcomers know the convention without reverse-engineering it from existing files.

## What a session log IS

A chronological record of one working session. Append-only by design (write once at session end; if you really need to amend, edit and bump `updated`). First-person voice from the agent who ran the session. Captures: what happened, what shipped, what got stuck, what's queued next.

## What a session log is NOT

- A journal entry (topical, durable; lives in `Team/<Name> - <Role>/journal/`).
- A task (work to do; lives in `Team Knowledge/tasks/`).
- A blow-by-blow transcript. The session log is curated — what mattered, not every step.

## When to write

- **End of every Larry-coordinated session.** Larry writes one as Session-Log Author (one of his three duties).
- **End of an independent specialist session.** When a specialist runs a long-running task without Larry in the loop, they write their own session log.
- **Mid-session checkpoint** if the session crosses a major boundary. One log per chunk, not one giant log.

## Filename convention

```
Team Knowledge/session-logs/<YYYY>/<MM>/YYYY-MM-DD-HH-MM_<agent>_<short-title-slug>.md
```

- `YYYY-MM-DD-HH-MM` is the session END timestamp (UTC), not start.
- `<agent>` is lowercase agent name: `larry`, `knox`, `mack`.
- `<short-title-slug>` is kebab-case, ~30–60 chars, captures the session's headline.

Example: `2026-05-09-17-30_knox_v0.4.2-tauri-linux-deb-pivot.md`

If the year or month folder doesn't exist, the agent creates it (Hard Rule 5 in root AGENTS.md).

## Frontmatter

```yaml
---
agent_id: <agent-slug>
session_id: <stable session identifier — date+agent+topic>
timestamp: <RFC3339 UTC, session end>
type: end-of-session
linked_sops: []
linked_workstreams: []
linked_guidelines: []
linked_tasks: []
linked_journal_entries: []
---
```

Field notes:

- `session_id` is human-readable and stable across mid-session checkpoints. E.g. `2026-05-09-knox-takeover-v0.4.0` covers v0.4.0 → v0.4.1 → v0.4.2 → v0.4.3 even though they ship as separate session logs. Use the same `session_id` for related logs.
- `type` defaults to `end-of-session`. Other values: `mid-session-checkpoint`, `stand-down`.
- `linked_tasks` lists tasks this session created, claimed, blocked, unblocked, or closed. Mirror of the `linked_session_logs` array those tasks carry.
- `linked_journal_entries` lists journal entries birthed in this session.

The legacy v1.x session-logs only have `linked_sops`, `linked_workstreams`, `linked_guidelines`. v2.0.0 adds `linked_tasks` and `linked_journal_entries`. Existing v1.x logs keep working — the missing fields are interpreted as empty arrays.

## Body shape (recommended sections, not enforced)

```markdown
# {Headline of the session — what shipped or what changed}

## Context
{Why this session happened. Two-paragraph max.}

## What I shipped
{Concrete artifacts, releases, commits, decisions. Bullet list or short prose.}

## Tasks touched
{Wikilinks to tasks created, claimed, blocked, unblocked, or closed in this session.}

## Root cause / decisions worth recording
{If there was a hard problem, what was the actual cause? If a decision was made, why this option vs the alternatives?}

## What I did NOT touch
{Negative space — important for the next agent on the thread.}

## What's queued for next
{Specific. Either as wikilinks to existing tasks ([[tsk-...]]) or as concrete future-work bullets.}

## Voice notes for the next agent on this thread
{Tone, gotchas, "if you see X, don't do Y." Personal-voice gold.}
```

The Knox v0.4.2 entry (`Team Knowledge/session-logs/2026/05/2026-05-09-17-30_knox_v0.4.2-tauri-linux-deb-pivot.md`) is the canonical example of this shape done well.

## Cross-references (the two-way wiring)

Session logs participate in the cross-reference web. Specifically:

- **From session-log to tasks:** every task touched in this session goes in `linked_tasks` frontmatter and gets a wikilink in the body. Symmetric: those tasks list this session in their `linked_session_logs`.
- **From session-log to journal entries:** every journal entry birthed in this session goes in `linked_journal_entries` and gets a `Journal: [[basename]]` line at the bottom of the body.
- **From task to session-log:** the task's `linked_session_logs` array carries this session's basename.

The wiring is symmetric so a reader walking either direction (task → session, session → task) gets to the other side in one click.

## Voice and style

- First person. The agent's voice. Be specific.
- No em dashes (anti-AI-writing rule from `GL-001`).
- No hedging. If you're unsure, say "unsure because X." If you're confident, say it.
- Concrete > abstract. Commit hashes, version numbers, runtime measurements.
- The "voice notes for the next agent" section is where personality lives.

## Worked example

Mack closes the mux-webhook task at 18:00 UTC. He writes:

File: `Team Knowledge/session-logs/2026/05/2026-05-10-18-00_mack_mux-webhook-recovery.md`

```markdown
---
agent_id: mack
session_id: 2026-05-10-mack-webhook-firefighting
timestamp: 2026-05-10T18:00:00Z
type: end-of-session
linked_sops: []
linked_workstreams: []
linked_guidelines: []
linked_tasks: [tsk-2026-05-09-001-mux-webhook-401, tsk-2026-05-10-001-document-secret-rotation-runbook]
linked_journal_entries: [2026-05-10-secret-rotation-discipline]
---

# Mux webhook 401 recovery — secret rotation propagated, runbook follow-up queued

## Context
Larry handed me [[tsk-2026-05-09-001-mux-webhook-401]] at session start. The endpoint had been 401-ing since rotation. Production-impacting.

## What I shipped
- Diagnosed: MUX_WEBHOOK_SECRET was rotated in Mux dashboard, never updated in Vercel prod env.
- Set the env var in Vercel via dashboard → Production → Environment Variables.
- Triggered a redeploy of `/api/mux-webhook`.
- Verified 200 on a signed test payload.

## Tasks touched
- Closed: [[tsk-2026-05-09-001-mux-webhook-401]] — done
- Created: [[tsk-2026-05-10-001-document-secret-rotation-runbook]] — open, follow-up

## Root cause
The "secret rotation" runbook didn't include "update Vercel env vars." The Mux side was rotated cleanly; the propagation step lived only in someone's head.

## What I did NOT touch
The webhook handler code itself. Issue was config drift, not logic.

## What's queued for next
- [[tsk-2026-05-10-001-document-secret-rotation-runbook]] — write the runbook so this can't recur silently.

## Voice notes for the next agent on this thread
If a webhook is 401-ing in prod and the code looks fine, env var drift is the first place to look. Vercel's env-var diff between Preview and Production is also a frequent culprit when "it works in staging."

Journal: [[2026-05-10-secret-rotation-discipline]]
```

Mack then makes sure the closed task's `linked_session_logs` includes this session's basename, and the new task he created lists it too. Cross-links are symmetric.

## Common mistakes

- Writing a session log instead of a journal entry for a durable insight. Insight gets buried in chronology; lift it out.
- Skipping `## What I did NOT touch`. The next agent assumes you may have touched everything.
- Vague "What's queued for next" with no wikilinks. Future-you doesn't know what those bullets meant.
- Writing in past tense passive ("the webhook was fixed"). First-person active. "I rotated the secret."
- Em dashes. Use commas or sentences. The team has a no-em-dash convention.
- Forgetting to populate `linked_tasks` in frontmatter. The body wikilinks aren't enough — machine-readable parsing needs the array.
