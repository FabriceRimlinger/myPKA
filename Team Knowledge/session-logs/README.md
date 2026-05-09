# Session Logs — the team's auto-memory

This folder is the AI team's structured memory across sessions. It is written
by agents, not by you. You can read it. You should occasionally skim it. You
do not need to maintain it.

## What lives here

`Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<session-id>.md`

One file per session entry. Sessions can write multiple entries — see "When
agents write" below. Folders nest by year and month. The agent creates the
`YYYY/` and `MM/` subfolder if it does not exist yet.

## When agents write here

1. **At session close** (`/close-session`). Larry runs the close-session
   protocol, sweeps any open tasks, writes a `close-session` entry summarizing
   what landed, what got deferred, and what changed.
2. **Mid-session, when something durable happens.** Agents may proactively
   append an entry during a session if a realignment with you produces a new
   insight, a new rule, a new decision worth remembering, or a clarification
   that changes how the team will operate going forward. This is not a
   chatlog — only durable signal lands here.

The four entry types:

| `type:` | When to write |
|---|---|
| `close-session` | End-of-session summary, written by Larry on `/close-session`. |
| `mid-session-insight` | Something the team learned mid-session that the next session needs to know. |
| `realignment` | You pushed back on a plan or corrected a misread. Capture the correction verbatim. |
| `proactive` | An agent flagged an issue, opportunity, or pattern worth surfacing without being asked. |

## What graduates out

Session logs are append-only working memory. When something written here turns
out to be **set in stone** — repeatable, applicable beyond the moment — it
graduates to the right home in `Team Knowledge/`:

- A repeatable procedure → an SOP (`Team Knowledge/SOPs/SOP-NNN-<slug>.md`).
- A multi-agent recurring orchestration → a Workstream
  (`Team Knowledge/Workstreams/WS-NNN-<slug>.md`).
- A static reference rule (naming, tone, defaults) → a Guideline
  (`Team Knowledge/Guidelines/GL-NNN-<slug>.md`).

Larry handles graduation as Librarian. The session log entry stays where it
is (append-only), and the new SOP/Workstream/Guideline cross-links back via
`[[wikilinks]]`.

## How to use this as a human

You usually do not need to. The team uses this folder to remember itself. If
you want to know what the team has been doing, the most recent file in the
deepest `YYYY/MM/` folder is the right read.

## Naming and structure

- Filename: `YYYY-MM-DD-HH-MM_<session-id>.md`. ISO datetime prefix to the
  minute, then an underscore, then a short kebab-case session id derived from
  the session's main theme.
- Folder: nest by year and month — `YYYY/MM/`.
- Frontmatter: every entry uses the frontmatter schema in `_template.md`.

See `_template.md` in this folder for the entry skeleton.
