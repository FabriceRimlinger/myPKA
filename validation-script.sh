#!/usr/bin/env bash
# validation-script.sh — verify a folder is myPKA scaffold v1.10.x-compliant.
#
# Usage:
#   bash validation-script.sh <scaffold-root>
#
# Exit codes:
#   0  = compliant
#   1  = one or more checks failed (see stderr)
#   2  = invalid invocation
#
# Dependencies: bash, find, grep, awk, head, wc, basename, dirname. Standard Unix.

set -u

if [ $# -ne 1 ]; then
  echo "Usage: $0 <scaffold-root>" >&2
  exit 2
fi

ROOT="$1"

if [ ! -d "$ROOT" ]; then
  echo "FAIL: '$ROOT' is not a directory" >&2
  exit 2
fi

FAILS=0
WARNS=0

fail() {
  echo "FAIL: $1" >&2
  FAILS=$((FAILS + 1))
}

warn() {
  echo "WARN: $1" >&2
  WARNS=$((WARNS + 1))
}

pass() {
  echo "ok:   $1"
}

# ----------------------------------------------------------------------------
# 1. .scaffold-version exists and is in the v1.10.x line
# ----------------------------------------------------------------------------
# v1.10.x patch releases (1.10.0, 1.10.1, ...) all share the same structural
# requirements, so any 1.10.x value passes this check. Bump the regex when a
# 1.11.x line introduces structural changes.

VERSION_FILE="$ROOT/.scaffold-version"
if [ ! -f "$VERSION_FILE" ]; then
  fail ".scaffold-version not found at $VERSION_FILE"
else
  VERSION=$(head -n1 "$VERSION_FILE" | tr -d '[:space:]')
  case "$VERSION" in
    1.10.*)
      pass ".scaffold-version is $VERSION (v1.10.x line)"
      ;;
    *)
      fail ".scaffold-version is '$VERSION', expected '1.10.x'"
      ;;
  esac
fi

# ----------------------------------------------------------------------------
# 2. Task folders exist
# ----------------------------------------------------------------------------

for sub in open in-progress done cancelled; do
  DIR="$ROOT/Team Knowledge/tasks/$sub"
  if [ -d "$DIR" ]; then
    pass "tasks/$sub/ exists"
  else
    fail "tasks/$sub/ missing at $DIR"
  fi
done

# Catch the common mistake of creating a blocked/ folder. Blocked tasks live in in-progress/ with blocked_reason set.
if [ -d "$ROOT/Team Knowledge/tasks/blocked" ]; then
  warn "tasks/blocked/ exists but should not — blocked tasks live in in-progress/ with blocked_reason set in frontmatter"
fi

# ----------------------------------------------------------------------------
# 3. Required task templates and INDEX
# ----------------------------------------------------------------------------

for f in "_template.md" "INDEX.md"; do
  PATH_F="$ROOT/Team Knowledge/tasks/$f"
  if [ -f "$PATH_F" ]; then
    pass "tasks/$f exists"
  else
    fail "tasks/$f missing at $PATH_F"
  fi
done

# ----------------------------------------------------------------------------
# 4. Per-agent journal folders + templates
# ----------------------------------------------------------------------------

if [ ! -d "$ROOT/Team" ]; then
  fail "Team/ directory missing at $ROOT/Team"
else
  AGENTS_FOUND=0
  while IFS= read -r AGENTS_FILE; do
    AGENT_DIR=$(dirname "$AGENTS_FILE")
    AGENT_NAME=$(basename "$AGENT_DIR")
    AGENTS_FOUND=$((AGENTS_FOUND + 1))

    JOURNAL_DIR="$AGENT_DIR/journal"
    if [ ! -d "$JOURNAL_DIR" ]; then
      fail "no journal/ for agent '$AGENT_NAME' (expected at $JOURNAL_DIR)"
    else
      pass "journal/ exists for '$AGENT_NAME'"
      if [ ! -f "$JOURNAL_DIR/_template.md" ]; then
        warn "no _template.md in '$AGENT_NAME' journal/"
      fi
    fi
  done < <(find "$ROOT/Team" -mindepth 2 -maxdepth 2 -name "AGENTS.md" -type f 2>/dev/null)

  if [ "$AGENTS_FOUND" -eq 0 ]; then
    warn "no agent AGENTS.md files found under Team/ — folder may be empty or non-standard"
  else
    pass "scanned $AGENTS_FOUND agent(s) for journal compliance"
  fi
fi

# ----------------------------------------------------------------------------
# 5. Required SOPs exist
# ----------------------------------------------------------------------------

REQUIRED_SOPS=(
  "SOP-create-task.md"
  "SOP-claim-task.md"
  "SOP-close-task.md"
  "SOP-list-open-tasks.md"
  "SOP-rebuild-task-index.md"
  "SOP-write-journal-entry.md"
  "SOP-read-own-journal.md"
  "SOP-write-session-log.md"
)

for sop in "${REQUIRED_SOPS[@]}"; do
  if [ -f "$ROOT/Team Knowledge/SOPs/$sop" ]; then
    pass "SOP exists: $sop"
  else
    fail "SOP missing: Team Knowledge/SOPs/$sop"
  fi
done

# ----------------------------------------------------------------------------
# 6. No tsk-*.md files outside the tasks/ tree (catch accidental spillage)
# ----------------------------------------------------------------------------

STRAY=$(find "$ROOT" -name "tsk-*.md" -type f 2>/dev/null | grep -v "/Team Knowledge/tasks/" || true)
if [ -n "$STRAY" ]; then
  fail "stray tsk-*.md files outside tasks/ tree:"
  echo "$STRAY" | sed 's/^/      /' >&2
else
  pass "no stray tsk-*.md files"
fi

# ----------------------------------------------------------------------------
# 7. No path-based wikilinks to tasks/ (must be basename-only)
# ----------------------------------------------------------------------------

# Look for [[tasks/... or [[Team Knowledge/tasks/... patterns in any markdown file under root
PATHLINKS=$(grep -rE '\[\[(Team Knowledge/)?tasks/' "$ROOT" --include='*.md' 2>/dev/null || true)
if [ -n "$PATHLINKS" ]; then
  warn "path-based wikilinks to tasks/ found (should be basename-only — see SOP-rebuild-task-index):"
  echo "$PATHLINKS" | head -10 | sed 's/^/      /' >&2
  if [ "$(echo "$PATHLINKS" | wc -l)" -gt 10 ]; then
    echo "      ...(truncated)" >&2
  fi
else
  pass "no path-based task wikilinks"
fi

# ----------------------------------------------------------------------------
# 8. Frontmatter sanity: each task file has id+title+assignee+priority+status
# ----------------------------------------------------------------------------

TASK_FILES=$(find "$ROOT/Team Knowledge/tasks" -name "tsk-*.md" -type f 2>/dev/null || true)
TASKS_CHECKED=0
TASKS_BAD=0

if [ -n "$TASK_FILES" ]; then
  while IFS= read -r tf; do
    TASKS_CHECKED=$((TASKS_CHECKED + 1))
    MISSING=""
    for field in "id" "title" "assignee" "priority" "status" "created" "updated" "created_by" \
                 "linked_sops" "linked_workstreams" "linked_guidelines" \
                 "linked_my_life" "linked_session_logs" "linked_journal_entries"; do
      if ! awk -v fld="$field" '
        BEGIN { in_fm=0 }
        NR==1 && /^---$/ { in_fm=1; next }
        in_fm && /^---$/ { exit 1 }
        in_fm && $0 ~ "^"fld":" { found=1; exit 0 }
        END { exit (found ? 0 : 1) }
      ' "$tf" 2>/dev/null; then
        MISSING="$MISSING $field"
      fi
    done
    if [ -n "$MISSING" ]; then
      fail "task '$tf' missing required frontmatter:$MISSING"
      TASKS_BAD=$((TASKS_BAD + 1))
    fi

    # status field must match folder
    FOLDER=$(basename "$(dirname "$tf")")
    case "$FOLDER" in
      open|in-progress) EXPECTED="$FOLDER" ;;
      [0-9][0-9]) # month folder under done/ or cancelled/
        PARENT_OF_PARENT=$(basename "$(dirname "$(dirname "$tf")")")
        case "$PARENT_OF_PARENT" in
          done|cancelled) EXPECTED="$PARENT_OF_PARENT" ;;
          *) EXPECTED="" ;;
        esac
        ;;
      *) EXPECTED="" ;;
    esac
    if [ -n "$EXPECTED" ]; then
      ACTUAL=$(awk '
        BEGIN { in_fm=0 }
        NR==1 && /^---$/ { in_fm=1; next }
        in_fm && /^---$/ { exit }
        in_fm && /^status:/ { sub(/^status:[ ]*/, ""); print; exit }
      ' "$tf")
      if [ "$ACTUAL" != "$EXPECTED" ]; then
        warn "task '$tf' has status '$ACTUAL' but folder is '$EXPECTED'"
      fi
    fi
  done <<< "$TASK_FILES"
  pass "checked $TASKS_CHECKED task file(s); $TASKS_BAD with frontmatter issues"
else
  pass "no task files yet (clean v1.10.x install)"
fi

# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------

echo
echo "========================================"
echo "Validation summary for $ROOT"
echo "  Failures: $FAILS"
echo "  Warnings: $WARNS"
echo "========================================"

if [ "$FAILS" -gt 0 ]; then
  exit 1
fi

exit 0
