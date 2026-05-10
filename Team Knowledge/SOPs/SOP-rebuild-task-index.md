# SOP — Rebuild Task Index

- **Owner:** any agent (called automatically by every other task-touching SOP)
- **Triggered by:** end of [[SOP-create-task]], [[SOP-claim-task]], [[SOP-close-task]]; or session boot if `INDEX.md` is stale
- **Output:** rewritten `Team Knowledge/tasks/INDEX.md`
- **References:** all task SOPs

## Purpose

`INDEX.md` is the resumption-summary view of the task folder. It exists so an agent or Tom can read one file at session boot and know what's open, in-progress, blocked, and recently closed without walking the tree.

This SOP keeps that view fresh. Every task-touching SOP calls it as the last step. Larry also calls it at session boot if the index mtime is older than the newest task file's mtime.

## Performance budget

Acceptance criterion: this must work on 50+ tasks, fast. Implementation uses `awk` for frontmatter parsing — single-pass, no yaml-library dependency. Sub-500ms target on 1000 tasks.

## Steps

### 1. Collect all task files

```bash
TASKS_ROOT="Team Knowledge/tasks"
FILES=$(find "$TASKS_ROOT/open" "$TASKS_ROOT/in-progress" "$TASKS_ROOT/done" "$TASKS_ROOT/cancelled" -name "tsk-*.md" -type f 2>/dev/null)
```

Note: there is no `blocked/` folder. Blocked tasks live in `in-progress/` with `blocked_reason` set.

### 2. Parse each file's frontmatter

For each file, extract `id`, `title`, `assignee`, `priority`, `status`, `created`, `updated`, `parent`, `blocked_reason`, `blocked_by`. The frontmatter is between the first two `---` lines. Single awk pass:

```bash
parse_task() {
  local f="$1"
  awk -v file="$f" '
    BEGIN { in_fm=0; }
    NR==1 && /^---$/ { in_fm=1; next; }
    in_fm && /^---$/ { in_fm=0; exit; }
    in_fm && /^[a-z_]+:/ {
      key = $1; sub(/:$/, "", key);
      val = $0; sub(/^[^:]*:[ ]*/, "", val);
      gsub(/^"|"$/, "", val);
      printf "%s\t%s\n", key, val;
    }
  ' "$f"
}
```

### 3. Group by status

- `open` (priority-sorted, then date-sorted within priority)
- `in-progress` (date of claim, descending; blocked tasks flagged)
- `recently_closed`: from `done/` only, last 7 days, descending
- `recently_cancelled`: from `cancelled/` only, last 7 days, descending

### 4. Render INDEX.md

```markdown
# Tasks Index

_Auto-generated. Do not edit by hand. Run `SOP-rebuild-task-index` to regenerate._

_Last rebuilt: <RFC3339 UTC>_

## Summary
- Open: <N>
- In progress: <N> (<M> blocked)
- Done (this month): <N>
- Cancelled (this month): <N>

## Open (<N>)

### Priority 1 — urgent
- [[<id>-<slug>]] — <title> — assignee: <name> — created <date>
  - sub: [[<child-id>-<child-slug>]] — assignee: <name>

### Priority 2 — high
...

### Priority 3 — normal
...

### Priority 4 — low
...

## In progress (<N>)
- [[<id>-<slug>]] — assignee: <name> — claimed <date>
- [[<id>-<slug>]] — assignee: <name> — BLOCKED: <blocked_reason one-liner>

## By assignee
- mack: <N> open, <N> in-progress (<M> blocked)
- knox: ...

## Recently closed (last 7 days)
- <date> [[<id>-<slug>]] — done — <closer-name>
- <date> [[<id>-<slug>]] — cancelled — <closer-name>
```

### 5. Write atomically

```bash
TMP=$(mktemp)
# render to $TMP
mv "$TMP" "$TASKS_ROOT/INDEX.md"
```

Atomic move so concurrent readers never see a partial file.

### 6. Validate

```bash
grep -q "^_Auto-generated\." "$TASKS_ROOT/INDEX.md" || { echo "rebuild failed"; exit 1; }
```

## Drift correction

While iterating, the rebuild SOP fixes two kinds of drift it encounters:

### Status-vs-folder mismatch

If a task's `status:` field disagrees with its folder location, **the folder wins**. The rebuild SOP updates the frontmatter `status:` field in place, bumps `updated`, and appends an update line:

```
- <date> <time> (rebuild) — corrected status field to match folder
```

This is the only context where an automated process edits a task body.

### Filename-vs-id drift

If a task's filename slug doesn't match its frontmatter `title`-slug (because the title was edited), the rebuild SOP renames the file with `git mv` to align them. The id portion of the filename is authoritative and never changes.

## Worked example

Knox just closed a task. The close SOP's last step is:

```bash
bash <path-to>/rebuild-task-index.sh
```

Or, if running by hand inside an LLM session, the SOP body is the spec the LLM follows:

> Re-render `Team Knowledge/tasks/INDEX.md` from current state of `Team Knowledge/tasks/`. Walk all `tsk-*.md` files under `open/`, `in-progress/`, `done/<YYYY>/<MM>/`, `cancelled/<YYYY>/<MM>/`. Parse each frontmatter. For each in `in-progress/` with `blocked_reason` not null, flag as BLOCKED. Render per the structure in this SOP. Write atomically.

## Common mistakes

- Hand-editing `INDEX.md`. Edits are lost on next rebuild. Add anything durable to a task body or a journal entry.
- Forgetting to walk `done/<YYYY>/<MM>/` and `cancelled/<YYYY>/<MM>/`. The "recently closed" section needs them.
- Looking for blocked tasks in a `blocked/` folder. There is no such folder. Blocked tasks are in `in-progress/` with `blocked_reason` set.
- Running the rebuild during a `git mv` (race). Don't. Run after every SOP completes its move; that ordering is built into the other SOPs.
