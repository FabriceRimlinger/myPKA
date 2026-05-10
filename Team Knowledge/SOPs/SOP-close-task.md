# SOP — Close a Task (Done or Cancelled)

- **Owner:** the agent finishing the task (for done) or the user/Larry (for cancel)
- **Triggered by:** task work shipping or being abandoned
- **Output:** task file archived in `done/<YYYY>/<MM>/` or `cancelled/<YYYY>/<MM>/`
- **References:** [[SOP-rebuild-task-index]], [[SOP-write-journal-entry]]

## Purpose

Closing a task is recording "this resumption point is now history." The `## Outcome` section is the continuity payload — what shipped, where it lives, what follow-ups exist. Future-anyone reading the closed task should be able to reconstruct what was accomplished without opening anything else.

## Two sub-procedures

- **§A Done:** terminal success. Move to `done/<YYYY>/<MM>/`.
- **§B Cancel:** terminal abandonment. Move to `cancelled/<YYYY>/<MM>/`.

Both terminal. Once a task is in `done/` or `cancelled/`, do not move it back. If the work needs to reopen, create a new task with `parent: <old-id>`.

## §A — Mark a task done

### Pre-flight

1. **Verify success criteria.** Re-read the task body's `## Success criteria`. All met? If not, the task isn't done.

2. **Check sub-tasks.**
   ```bash
   grep -rl "parent: <id>" "Team Knowledge/tasks/open" "Team Knowledge/tasks/in-progress"
   ```
   If any sub-tasks are still open or in-progress: surface them. Decide explicitly whether to (a) close them too, (b) leave them as standalone follow-ups, or (c) hold this parent open until they settle. Document the decision in the parent's `## Outcome`.

### Steps

1. **Determine the archive path.**
   ```bash
   YEAR=$(date -u +%Y)
   MONTH=$(date -u +%m)
   DEST="Team Knowledge/tasks/done/${YEAR}/${MONTH}"
   mkdir -p "$DEST"
   ```

2. **Move the file.** Source is `in-progress/`:
   ```bash
   git mv "Team Knowledge/tasks/in-progress/<id>-<slug>.md" "$DEST/<id>-<slug>.md"
   ```

3. **Update frontmatter:** `status: done`, bump `updated`. Clear `blocked_reason` and `blocked_by` if they were set.

4. **Write the `## Outcome` section.** Mandatory. Shape:

   ```markdown
   ## Outcome

   What shipped: <one-paragraph summary>.

   Where it lives: [[<wikilink to commit, file, or session-log>]].

   Follow-ups: [[<sub-task ids if any>]] or "none."

   Lessons: <optional, [[wikilink]] to a journal entry if you wrote one>.
   ```

5. **Append final update line:**
   ```
   - 2026-05-10 17:42 (<your-name>) — done: <one-line summary>
   ```

6. **If you learned something durable, write a journal entry.** See [[SOP-write-journal-entry]]. Link it from the `## Outcome` section, and add the entry's basename to `linked_journal_entries:` in this task's frontmatter (so future readers of this task get the lesson).

7. **Append the close to the linked session log.** If `linked_session_logs` includes the current session, no extra step. If you closed during a different session, add this session's basename to the array. Continuity needs the session log to know the task closed in this session.

8. **Rebuild the index.**

## §B — Cancel a task

### When to call

Requirements changed. Duplicate of another task. Permanent blocker. User decided otherwise.

### Steps

1. **Determine archive path.**
   ```bash
   YEAR=$(date -u +%Y)
   MONTH=$(date -u +%m)
   DEST="Team Knowledge/tasks/cancelled/${YEAR}/${MONTH}"
   mkdir -p "$DEST"
   ```

2. **Move the file.** Source can be `open/` or `in-progress/`:
   ```bash
   git mv "Team Knowledge/tasks/<source>/<id>-<slug>.md" "$DEST/<id>-<slug>.md"
   ```

3. **Update frontmatter:** `status: cancelled`, bump `updated`. Clear `blocked_reason` and `blocked_by`.

4. **Write `## Outcome` explaining the cancellation.**
   ```markdown
   ## Outcome (cancelled)

   Reason: <why we cancelled>.

   Superseded by: [[<other-task-id>]] (if applicable, otherwise "n/a").
   ```

5. **Append final update:**
   ```
   - 2026-05-10 16:00 (<your-name>) — cancelled: <one-line reason>
   ```

6. **Rebuild the index.**

## "Done-ish but not really"

You shipped most of the work but a piece slipped to a follow-up. Two options:

- **Close as done, create a new task for the follow-up** with `parent: <this-id>`. Preferred — keeps each task scoped to one outcome.
- **Set `blocked_reason` on this task** with the follow-up as `blocked_by`. Use only if the follow-up is small and same-day. Otherwise `in-progress/` stagnates.

## Worked example (done)

Mack closes the mux-webhook task:

```bash
mkdir -p "Team Knowledge/tasks/done/2026/05"
git mv "Team Knowledge/tasks/in-progress/tsk-2026-05-09-001-mux-webhook-401.md" \
       "Team Knowledge/tasks/done/2026/05/tsk-2026-05-09-001-mux-webhook-401.md"
```

Frontmatter: `status: done`, `updated: 2026-05-10T17:42:00Z`.

Body, `## Outcome`:

```markdown
## Outcome

What shipped: rotated MUX_WEBHOOK_SECRET in Vercel prod env, redeployed `/api/mux-webhook`, verified 200 on signed test payload. Root cause: secret was rotated in Mux dashboard but the Vercel env var was set via the team's old "manual paste" flow which wasn't part of the rotation runbook.

Where it lives: commit ab12cd3 in `myicor-20251024`. Session-log [[2026-05-10-09-15_mack_mux-webhook-recovery]].

Follow-ups: [[tsk-2026-05-10-001-document-secret-rotation-runbook]].

Lessons: [[2026-05-10-secret-rotation-discipline]] (journal).
```

Mack also writes the journal entry [[2026-05-10-secret-rotation-discipline]] and adds it to this task's `linked_journal_entries`. He adds the current session log to `linked_session_logs`.

Final update line:

```
- 2026-05-10 17:42 (mack) — done: rotated secret + verified webhook 200
```

Rebuild index. Report to Larry: `Closed [[tsk-2026-05-09-001-mux-webhook-401]]. One follow-up: [[tsk-2026-05-10-001-document-secret-rotation-runbook]]. Journal: [[2026-05-10-secret-rotation-discipline]].`

## Common mistakes

- Closing without writing `## Outcome`. The future archaeologist learns nothing from this archive.
- Closing a parent while children are still open without acknowledging them.
- Marking done when blocker resolved but success criteria not actually re-checked. Resist.
- Cancelling without a reason. "Cancelled" with no `## Outcome` is indistinguishable from data loss.
- Forgetting to add a journal entry's basename to `linked_journal_entries` when you wrote one. The body wikilink points there but a future task that wants to find related learning will grep frontmatter, not bodies.
