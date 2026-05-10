# SOP — Read Your Own Journal

- **Owner:** any specialist agent at session start or task pickup
- **Triggered by:** session boot, before starting work on a new task
- **Output:** prior learning loaded and explicitly named in the task's update log
- **References:** [[SOP-write-journal-entry]]

## Purpose

Continuity for the assignee. Your journal is what you've already learned that future-you will want to reuse. Reading it before starting work is how you avoid relearning lessons you already paid for. The cost is 30 seconds. The cost of skipping it is repeating mistakes the previous you wrote down.

## When to call

- Every session boot, after Larry hands you a task and before you start working.
- When you're about to do something that pattern-matches an old situation, even if you already booted earlier.

## Steps

### 1. Read what the task creator already pre-loaded for you

Open the task you're about to claim. Read the `linked_journal_entries` array in frontmatter. The task creator already identified entries they think are relevant. Read those in full — `## What I learned`, `## When this applies`, and especially `## When this does NOT apply`.

This is the highest-value step. Skip it and you ignore curated priors.

```bash
TASK="Team Knowledge/tasks/in-progress/<id>-<slug>.md"
awk '/^linked_journal_entries:/' "$TASK"
```

For each basename listed, find and read:

```bash
ME="<Your Name> - <Your Role>"
for entry in <basenames>; do
  cat "Team/${ME}/journal/${entry}.md"
done
```

### 2. List your most recent entries

```bash
ls -t "Team/${ME}/journal/" 2>/dev/null | grep -v '^_template' | head -10
```

Read the titles (the `# ...` line) and the `## What I learned` section of each. 30-second skim. This catches recent lessons the task creator might not have known about.

### 3. Match by tag against your current task

Look at the task's `tags`:

```bash
TASK_TAGS="<tag1> <tag2> <tag3>"
for tag in $TASK_TAGS; do
  grep -lE "tags:.*\b${tag}\b" "Team/${ME}/journal/"*.md 2>/dev/null
done
```

For every match not already covered by step 1: read the entry in full.

### 4. Match by topic

If the task title contains a keyword that matches an existing journal entry's `topic:` field, read that entry.

```bash
grep -liE "^topic: <topic-keyword>" "Team/${ME}/journal/"*.md
```

### 5. Note what's missing

If the task is in a domain where you have NO journal entries yet, that's signal — you're about to do something for the first time (or for the first time you're capturing). Make a mental note: write a journal entry at session close if you learn something durable.

### 6. Carry priors into the work — visibly

Before starting the task, name the priors you're carrying. Append to the task's `## Updates`:

```
- 2026-05-10 09:18 (mack) — priors loaded: [[2026-05-09-tauri-appimage-vs-deb]] applies; [[2026-04-12-rust-toolchain-pinning]] also applies
```

This makes the resumption surface auditable. If you forgot a relevant prior and made a mistake, the absence is visible in the update log. Future-anyone reading the task knows what you knew when you started.

## Anti-pattern: read-everything-every-time

If your journal grows past ~50 entries, don't read every entry every time. Steps 1 (task `linked_journal_entries`) + 2 (10 most recent) + 3 (tag match) + 4 (topic match) cuts it. The full archive is searchable when you need it.

## Worked example

Knox, booted by Larry to work on `tsk-2026-05-12-001-tauri-windows-codesign`. Tags: `[tauri, windows, codesign, ci]`.

Step 1 — task's `linked_journal_entries` includes `[2026-04-15-tauri-v2-capabilities-default]`. Knox reads it in full.

Step 2 — recent entries:

```
2026-05-09-tauri-appimage-vs-deb.md
2026-05-04-rust-toolchain-pinning.md
2026-04-28-mac-notarytool-vs-altool.md
```

Knox skims titles. The notarytool one and the toolchain-pinning one stand out.

Step 3 — tag match for `tauri`:

```
.../2026-05-09-tauri-appimage-vs-deb.md   (already read)
.../2026-04-28-mac-notarytool-vs-altool.md
.../2026-04-15-tauri-v2-capabilities-default.md   (already read)
```

Knox reads the notarytool one. The "When does NOT apply" section says ignore for Windows. Good — saved a wrong path.

Step 5 — no prior Windows-codesign entry exists. Note to self: journal at close.

Step 6 — appends to the task's `## Updates`:

```
- 2026-05-12 09:30 (knox) — priors loaded: [[2026-04-15-tauri-v2-capabilities-default]] (capabilities convention applies); [[2026-04-28-mac-notarytool-vs-altool]] (Mac-only — does NOT apply for Windows). No prior Windows-codesign entry; will journal at close if I learn something durable.
```

Then starts the task.

## Common mistakes

- Skipping this step because "I just want to start." 30 seconds saves 30 minutes.
- Reading only by recency, not by tag/topic/`linked_journal_entries`. The relevant entry might be three months old and pre-loaded by the task creator.
- Reading old entries and silently using them without naming the priors. If you're going to follow a journal entry's advice, name it in the task's update log. Audit trail.
- Forgetting to journal new lessons at the end of the session. The journal is a feedback loop. Read AND write.
