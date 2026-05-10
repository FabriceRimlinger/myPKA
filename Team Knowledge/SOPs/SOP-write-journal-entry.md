# SOP — Write a Journal Entry

- **Owner:** any specialist agent (each agent owns their own `journal/`)
- **Triggered by:** an insight that will apply to future sessions, not just this one
- **Output:** a new file in `Team/<Name> - <Role>/journal/`
- **References:** [[SOP-read-own-journal]], [[SOP-write-session-log]]

## Purpose

A journal entry is the assignee's continuity surface for cross-session learning. It captures something durable — a lesson, a decision rule, an anti-pattern — that future-you (or another instance of you) will want to apply when a similar situation comes up.

When a future task references this entry in its `linked_journal_entries`, the assignee opens it and recovers the prior learning. That's the whole point.

## What a journal entry IS

A topical, durable note. First-person. Opinionated. Examples:
- "Tauri AppImage breaks on Bun externalBin sidecars — use .deb instead."
- "When pgvector index is over 1M rows, switch from IVFFlat to HNSW."
- "Warm-palette discipline: never use cool greys with the brass accent."

## What a journal entry is NOT

- A session log (chronological, ephemeral, lives in `Team Knowledge/session-logs/`).
- A task (work to do, lives in `Team Knowledge/tasks/`).
- A Guideline (team-wide reference; lives in `Team Knowledge/Guidelines/`).
- A daily diary. Don't write one a day for the sake of it.

If the insight applies team-wide and is permanent, it belongs in `Team Knowledge/Guidelines/` as a `GL-xxx.md`. Journals are agent-scoped. Guidelines are team-scoped.

## When to write

The trigger test:

> "Will I (or another instance of me) want to find this insight three months from now, when I'm halfway through a different task, and have it change what I do?"

Yes → write it. Maybe → write it short. No → don't.

Also: when you close a task and the `## Outcome` is smuggling a durable lesson, lift the lesson out into a journal entry and link from the outcome. Keeps the task scoped to one outcome and the lesson findable.

## Steps

### 1. Pick a topic slug

Single short kebab-case phrase. Becomes part of the filename and the frontmatter `topic` field.

Good: `tauri-build-pipelines`, `pgvector-index-sizing`, `warm-palette-discipline`.
Bad: `learnings`, `notes`, `friday-thoughts`.

### 2. Pick a filename

```
Team/<Name> - <Role>/journal/YYYY-MM-DD-<topical-slug>.md
```

Date is **today** — the birthdate of the insight. Slug describes the *insight*, not the *event* that produced it. "tauri-appimage-vs-deb" not "knox-shipped-v0.4.2".

### 3. Copy the template

```bash
cp "Team/<Name> - <Role>/journal/_template.md" \
   "Team/<Name> - <Role>/journal/YYYY-MM-DD-<slug>.md"
```

### 4. Fill the frontmatter

```yaml
---
agent_id: <self>
type: journal-entry
created: <RFC3339 UTC>
updated: <RFC3339 UTC>
topic: <topic-slug>
tags: [tag1, tag2]
linked_session_logs: [<session-log-basename>]
linked_tasks: [<task-id-if-relevant>]
related_journal_entries: []
status: durable
---
```

`status: durable` is the default. Mark `superseded` later if a newer entry replaces this one.

`linked_session_logs` is the session(s) that birthed the insight. `linked_tasks` is the task(s) that birthed it. Both can be plural.

### 5. Fill the body

Use the section headers in the template. Tight is better:

```markdown
# {The insight in one sentence — this is the title}

## Context
{Two sentences max. What happened that made me write this down.}

## What I learned
{The actual insight. Direct, opinionated, no hedging. Caveats go in "When this does NOT apply."}

## When this applies
{Concrete trigger conditions. "Next time I'm packaging a Tauri app for Linux and the sidecar is a Bun standalone, ..."}

## When this does NOT apply
{Anti-applicability. Equally important.}

## Evidence
{Wikilinks to session-logs, tasks, commits, external docs.}
```

### 6. Cross-link from the source

If the insight came out of a session, append a one-line wikilink at the bottom of the session log: `Journal: [[YYYY-MM-DD-<slug>]]`.

If it came out of a task `## Outcome`, link from there AND add the journal basename to the task's `linked_journal_entries` frontmatter array.

### 7. Tag-budget check

Tags should be functionally distinct, not synonyms. `tauri` and `tauri-v2` is fine; `tauri` and `tauri-app` is not. Aim for 2–5 tags.

## Worked example

Knox, after shipping v0.4.2:

File: `Team/Knox - Cross-Platform Native Developer/journal/2026-05-09-tauri-appimage-vs-deb.md`

```markdown
---
agent_id: knox
type: journal-entry
created: 2026-05-09T18:42:00Z
updated: 2026-05-09T18:42:00Z
topic: tauri-build-pipelines
tags: [tauri, linux, appimage, deb, bun]
linked_session_logs: [2026-05-09-17-30_knox_v0.4.2-tauri-linux-deb-pivot]
linked_tasks: []
related_journal_entries: []
status: durable
---

# Linux: don't ship Tauri+Bun-sidecar as AppImage. Ship .deb.

## Context
v0.4.0–v0.4.1 the linux-x64 Tauri leg failed to bundle. v0.4.2 pivoted to .deb and shipped clean.

## What I learned
`linuxdeploy-plugin-gtk` runs `ldd` on every executable in `usr/bin/`. Bun-compiled standalones are self-extracting archives, not normal ELFs — `ldd` aborts the build. There is no clean workaround as of 2026-05; relocating the binary breaks Tauri's `externalBin` spawn contract on Mac/Win, and skipping the gtk plugin breaks the AppImage at runtime. `.deb` has no equivalent scan and works out of the box.

## When this applies
- Packaging a Tauri v2 app for Linux
- Sidecar is a Bun standalone or any other self-extracting binary
- Targeting Debian/Ubuntu/Mint/Pop!_OS users

## When this does NOT apply
- Sidecar is a normal dynamically-linked ELF (works fine in AppImage)
- Targeting Arch / Fedora / NixOS where .deb isn't the native format
- After Tauri ships PR #12491 (linuxdeploy pre-deploy filter)

## Evidence
- [[2026-05-09-17-30_knox_v0.4.2-tauri-linux-deb-pivot]] (session log with full RCA)
- Tauri PR https://github.com/tauri-apps/tauri/pull/12491
- Commit dd624ac → 293a30b on `mypka-interface-browser`
```

Knox then appends to the session log: `Journal: [[2026-05-09-tauri-appimage-vs-deb]]`.

## Common mistakes

- Writing a journal entry that's really just a session-log recap. If it doesn't pass the three-month-from-now test, it's a session-log.
- Vague titles ("learnings from Tauri"). The title IS the insight. State it.
- No "When this does NOT apply" section. Without it, future-you applies the insight where it doesn't fit.
- Writing a journal entry instead of proposing a Guideline. If the rule applies team-wide and is permanent, it's a Guideline. Journals are agent-scoped.
- Editing an old journal entry to update it. Instead: write a new one, mark the old `status: superseded`, link them via `related_journal_entries`. Keeps the audit trail.
- Forgetting to add the entry to the originating task's `linked_journal_entries`. Future-anyone resuming that task should find the lesson without grepping.
