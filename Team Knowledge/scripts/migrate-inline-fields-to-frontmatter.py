#!/usr/bin/env python3
"""
migrate-inline-fields-to-frontmatter.py
========================================

One-shot migration helper for myPKA scaffold v1.3.0.

Pre-v1.3.0, users wrote entity metadata as inline body text:

    # Dr. Schmidt

    **Full name:** Dr. Andrea Schmidt
    **Role:** practicing physician
    **Organization:** [[dr-schmidt-clinic]]

v1.3.0 introduces YAML frontmatter as the canonical source of truth (per
GL-002 + Templates/). The Properties tab in mypka-interface v0.3.4+ parses
frontmatter; the SQLite converter (SOP-002) extracts structured columns from
frontmatter. Inline body fields parse to NOTHING — silent data loss.

This script scans your vault, detects the old `**Field:** value` pattern,
and rewrites notes with a YAML frontmatter block. Existing frontmatter is
respected (skipped, never double-written). Originals are backed up to `.bak`
when `--apply` is used.

Usage
-----
    # Preview what would change (default mode)
    python3 migrate-inline-fields-to-frontmatter.py /path/to/vault

    # Apply rewrites (creates .bak siblings)
    python3 migrate-inline-fields-to-frontmatter.py /path/to/vault --apply

    # Limit to one entity folder
    python3 migrate-inline-fields-to-frontmatter.py /path/to/vault \\
        --only "PKM/CRM/People"

Why Python (not Bun/TS)?
------------------------
Python 3.9+ is preinstalled on macOS, most Linux distros, and bundled with
Windows via the Microsoft Store. The script uses stdlib only (no PyYAML,
no third-party deps) so users can run it zero-install. Bun would require
users to install Bun first; the audience is non-technical PKM owners.

Field schema source of truth
----------------------------
The FIELD_MAP below is reconciled against GL-002 v1.0 (Team Knowledge/
Guidelines/GL-002-frontmatter-conventions.md). If GL-002 changes (renames a
field, adds a required field, drops one), update FIELD_MAP to match. The
SQLite migration in SOP-002 reads the same names — three files must stay in
lockstep: GL-002, this script's FIELD_MAP, and SOP-002's column list.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Entity-folder → field-name normalization map.
#
# Keys are vault-relative POSIX paths (forward-slashed) of entity folders.
# Values map "case-insensitive inline label" → "snake_case YAML key" per
# GL-002 (Team Knowledge/Guidelines/GL-002-frontmatter-conventions.md).
#
# Reconciled against GL-002 v1.0 (commits 3e679e7 + 3ea7d92 + 15f2ac4 on
# branch v1.3-frontmatter, 2026-05-09).
# ---------------------------------------------------------------------------

# Aliases that always map the same regardless of folder.
COMMON_ALIASES = {
    "tags": "tags",
    "tag": "tags",
}

# Per GL-002 §"People". `full_name` is the required field. Foreign keys are
# stored as slugs.
PEOPLE_FIELDS = {
    "full name": "full_name",
    "name": "full_name",
    "first name": "first_name",
    "last name": "last_name",
    "relation": "relation",
    "role": "role",
    "title": "role",
    "company": "company",
    "organization": "company",
    "org": "company",
    "employer": "company",
    "email": "email",
    "phone": "phone",
    "city": "city",
    "location": "city",
    "birth date": "birth_date",
    "birthday": "birth_date",
    "linkedin": "linkedin_url",
    "linkedin url": "linkedin_url",
    "last contact": "last_contact",
    "last interaction": "last_contact",
}

# Per GL-002 §"Organizations". Note `org_type` (not `type`) and `city` (not
# `location`) — these are intentional column names matching SOP-002.
ORG_FIELDS = {
    "name": "name",
    "legal name": "name",
    "org type": "org_type",
    "type": "org_type",
    "kind": "org_type",
    "industry": "industry",
    "website": "website",
    "url": "website",
    "email": "email",
    "phone": "phone",
    "city": "city",
    "location": "city",
}

# Per GL-002 §"Projects". `name` is required (not `title`). `key_element`,
# `linked_goals`, `linked_people` all store slugs.
PROJECT_FIELDS = {
    "name": "name",
    "title": "name",
    "status": "status",
    "target date": "target_date",
    "due": "target_date",
    "deadline": "target_date",
    "key element": "key_element",
    "linked goals": "linked_goals",
    "goals": "linked_goals",
    "linked people": "linked_people",
    "people": "linked_people",
}

# Per GL-002 §"Goals". `name` is required. `linked_projects` stores slugs.
GOAL_FIELDS = {
    "name": "name",
    "title": "name",
    "status": "status",
    "target date": "target_date",
    "due": "target_date",
    "deadline": "target_date",
    "key element": "key_element",
    "linked projects": "linked_projects",
    "projects": "linked_projects",
}

# Per GL-002 §"Habits". `name` is required. `cadence` enum: daily | weekdays
# | weekly | monthly | adhoc.
HABIT_FIELDS = {
    "name": "name",
    "title": "name",
    "cadence": "cadence",
    "frequency": "cadence",
    "status": "status",
    "started on": "started_on",
    "started": "started_on",
    "start date": "started_on",
    "key element": "key_element",
}

# Per GL-002 §"Topics". `name` is required. `parent_topic` stores a slug.
TOPIC_FIELDS = {
    "name": "name",
    "title": "name",
    "key element": "key_element",
    "parent topic": "parent_topic",
    "parent": "parent_topic",
}

# Per GL-002 §"Key Elements". `name` is required. `description_short` is a
# one-line scalar.
KEY_ELEMENT_FIELDS = {
    "name": "name",
    "title": "name",
    "description short": "description_short",
    "description": "description_short",
    "short description": "description_short",
    "status": "status",
}

# Per GL-002 §"Documents". `title` (NOT `name`) is required. The document
# schema is the broadest in the vault — many optional fields.
DOCUMENT_FIELDS = {
    "title": "title",
    "name": "title",
    "doc type": "doc_type",
    "type": "doc_type",
    "kind": "doc_type",
    "physical location": "physical_location",
    "digital location": "digital_location",
    "file path": "digital_location",
    "issued on": "issued_on",
    "issued": "issued_on",
    "issue date": "issued_on",
    "expiry date": "expiry_date",
    "expires": "expiry_date",
    "expiration": "expiry_date",
    "renewal trigger": "renewal_trigger",
    "renew on": "renewal_trigger",
    "linked people": "linked_people",
    "people": "linked_people",
    "linked organizations": "linked_organizations",
    "organizations": "linked_organizations",
}

FIELD_MAP: dict[str, dict[str, str]] = {
    "PKM/CRM/People": {**COMMON_ALIASES, **PEOPLE_FIELDS},
    "PKM/CRM/Organizations": {**COMMON_ALIASES, **ORG_FIELDS},
    "PKM/My Life/Projects": {**COMMON_ALIASES, **PROJECT_FIELDS},
    "PKM/My Life/Goals": {**COMMON_ALIASES, **GOAL_FIELDS},
    "PKM/My Life/Habits": {**COMMON_ALIASES, **HABIT_FIELDS},
    "PKM/My Life/Topics": {**COMMON_ALIASES, **TOPIC_FIELDS},
    "PKM/My Life/Key Elements": {**COMMON_ALIASES, **KEY_ELEMENT_FIELDS},
    "PKM/Documents": {**COMMON_ALIASES, **DOCUMENT_FIELDS},
}

ENTITY_FOLDERS = list(FIELD_MAP.keys())

# Files that should never be migrated (templates, indexes, README scaffolding).
SKIP_BASENAMES = {"INDEX.md", "README.md", "_template.md"}

# Pattern: a body line starting with `**Field:** value`. We deliberately do
# NOT require a leading bullet — the canonical pre-v1.3 example notes (see
# HANDOFF.md §"What the example note actually does") wrote bare bold-label
# lines, not bulleted ones. The match is anchored at line start with optional
# leading whitespace tolerated.
#
# Both shapes are accepted (Obsidian users use both interchangeably):
#   `**Field:** value`   ← colon inside the bold markers (canonical)
#   `**Field**: value`   ← colon outside the bold markers
#
# The label group strips a trailing colon if it captured one.
INLINE_FIELD_RE = re.compile(
    r"^[ \t]*\*\*(?P<label>[^*\n][^*\n]*?):?\*\*\s*:?\s+(?P<value>\S.*?)\s*$",
    re.MULTILINE,
)

# Detects whether a file already begins with YAML frontmatter.
HAS_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------


@dataclass
class Migration:
    path: Path
    folder_key: str
    original_text: str
    new_text: str
    extracted: dict[str, Any]
    skipped_labels: list[str]


def detect_folder_key(file_path: Path, vault_root: Path) -> str | None:
    """Return the FIELD_MAP key whose path is a parent of file_path."""
    try:
        rel = file_path.relative_to(vault_root).as_posix()
    except ValueError:
        return None
    for folder in ENTITY_FOLDERS:
        if rel.startswith(folder + "/"):
            return folder
    return None


def yaml_quote(value: str) -> str:
    """Conservative YAML quoting for scalar string values.

    Returns either an unquoted scalar (when safe) or a double-quoted scalar
    with internal `"` and `\\` escaped.
    """
    needs_quote = any(ch in value for ch in [":", "#", "\n", "\"", "'"]) or value.strip() != value
    if not needs_quote and value:
        # Avoid triggering YAML bool/null/number coercion on raw scalars.
        lowered = value.lower()
        if lowered in {"yes", "no", "true", "false", "null", "~", "on", "off"}:
            needs_quote = True
        elif re.fullmatch(r"-?\d+(\.\d+)?", value):
            needs_quote = True
    if not needs_quote:
        return value
    escaped = value.replace("\\", "\\\\").replace("\"", "\\\"")
    return f"\"{escaped}\""


def coerce_value(raw: str) -> Any:
    """Convert a raw inline value string into a Python type for YAML emit.

    Heuristics:
      - "[a, b, c]"          → list of strings
      - "[[slug-a]], [[slug-b]]" → list of wikilink slugs (strip [[ ]])
      - "2026-05-09"         → kept as ISO date string
      - everything else      → string scalar
    """
    raw = raw.strip()
    # Bracketed list: [a, b]  (but NOT a single wikilink "[[slug]]")
    if raw.startswith("[") and raw.endswith("]") and not raw.startswith("[["):
        inner = raw[1:-1]
        items = [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]
        return items
    # Multiple wikilinks separated by commas: "[[a]], [[b]]"
    # Only treat as a list when EVERY comma-separated chunk is a wikilink.
    if "[[" in raw and "," in raw:
        chunks = [c.strip() for c in raw.split(",") if c.strip()]
        if all(re.fullmatch(r"\[\[.+?\]\]", c) for c in chunks):
            return [re.sub(r"^\[\[(.+?)\]\]$", r"\1", c) for c in chunks]
    # Single wikilink: [[slug]] → "slug"
    m = re.fullmatch(r"\[\[(.+?)\]\]", raw)
    if m:
        return m.group(1)
    # Everything else (including prose with commas like "Berlin, Germany"
    # or "practicing physician, internal medicine") stays a string scalar.
    return raw


def emit_yaml_block(data: dict[str, Any]) -> str:
    """Stdlib YAML emitter (sufficient for the flat scalar/list shape we use)."""
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {yaml_quote(str(item))}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif value is None:
            lines.append(f"{key}: ")
        else:
            lines.append(f"{key}: {yaml_quote(str(value))}")
    lines.append("---")
    return "\n".join(lines)


def plan_migration(file_path: Path, vault_root: Path) -> Migration | None:
    folder_key = detect_folder_key(file_path, vault_root)
    if folder_key is None:
        return None
    if file_path.name in SKIP_BASENAMES:
        return None

    text = file_path.read_text(encoding="utf-8")
    if HAS_FRONTMATTER_RE.match(text):
        return None  # Already migrated.

    field_map = FIELD_MAP[folder_key]
    extracted: dict[str, Any] = {}
    spans_to_strip: list[tuple[int, int]] = []
    skipped_labels: list[str] = []

    for match in INLINE_FIELD_RE.finditer(text):
        label = match.group("label").strip()
        normalized_label = re.sub(r"\s+", " ", label).lower()
        yaml_key = field_map.get(normalized_label)
        if yaml_key is None:
            skipped_labels.append(label)
            continue
        value = coerce_value(match.group("value"))
        if yaml_key in extracted:
            # Merge if both are list-like; otherwise prefer first occurrence.
            existing = extracted[yaml_key]
            if isinstance(existing, list) and isinstance(value, list):
                existing.extend(v for v in value if v not in existing)
            elif isinstance(existing, list) and value not in existing:
                existing.append(value)
        else:
            extracted[yaml_key] = value
        spans_to_strip.append(match.span())

    if not extracted:
        return None  # Nothing to migrate.

    # Strip matched lines (back-to-front to keep offsets valid).
    new_body = text
    for start, end in sorted(spans_to_strip, reverse=True):
        # Extend `end` to consume the trailing newline that followed the field
        # line, so we don't leave an orphan blank line behind.
        if end < len(new_body) and new_body[end] == "\n":
            end += 1
        new_body = new_body[:start] + new_body[end:]

    # Collapse 3+ consecutive blank lines that may result from stripping.
    new_body = re.sub(r"\n{3,}", "\n\n", new_body).lstrip("\n")

    new_text = emit_yaml_block(extracted) + "\n\n" + new_body
    if not new_text.endswith("\n"):
        new_text += "\n"

    return Migration(
        path=file_path,
        folder_key=folder_key,
        original_text=text,
        new_text=new_text,
        extracted=extracted,
        skipped_labels=skipped_labels,
    )


def render_diff(mig: Migration, vault_root: Path) -> str:
    rel = mig.path.relative_to(vault_root).as_posix()
    diff = difflib.unified_diff(
        mig.original_text.splitlines(keepends=True),
        mig.new_text.splitlines(keepends=True),
        fromfile=f"a/{rel}",
        tofile=f"b/{rel}",
        n=3,
    )
    return "".join(diff)


def iter_candidate_files(vault_root: Path, only: str | None) -> list[Path]:
    targets = [only] if only else ENTITY_FOLDERS
    found: list[Path] = []
    for folder in targets:
        base = vault_root / folder
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path.name in SKIP_BASENAMES:
                continue
            found.append(path)
    return sorted(found)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="migrate-inline-fields-to-frontmatter",
        description=(
            "Convert pre-v1.3.0 inline `**Field:** value` notes into YAML "
            "frontmatter, per GL-002. Default mode is preview-only."
        ),
    )
    parser.add_argument(
        "vault",
        type=Path,
        help="Path to your myPKA vault root (the folder containing PKM/).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply rewrites in place. Originals are saved to `<file>.bak`.",
    )
    parser.add_argument(
        "--only",
        type=str,
        default=None,
        help=(
            "Limit migration to a single entity folder, e.g. 'PKM/CRM/People'. "
            "Default: scan all 8 entity folders."
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file diffs in preview mode (still prints summary).",
    )
    args = parser.parse_args(argv)

    vault_root: Path = args.vault.expanduser().resolve()
    if not vault_root.is_dir():
        print(f"error: vault path not found: {vault_root}", file=sys.stderr)
        return 2

    candidates = iter_candidate_files(vault_root, args.only)
    if not candidates:
        print("No candidate notes found in entity folders. Nothing to do.")
        return 0

    migrations: list[Migration] = []
    already_frontmatter = 0
    no_changes = 0
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        if HAS_FRONTMATTER_RE.match(text):
            already_frontmatter += 1
            continue
        plan = plan_migration(path, vault_root)
        if plan is None:
            no_changes += 1
            continue
        migrations.append(plan)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== migrate-inline-fields-to-frontmatter [{mode}] ===")
    print(f"vault            : {vault_root}")
    print(f"candidates found : {len(candidates)}")
    print(f"already migrated : {already_frontmatter}")
    print(f"no inline fields : {no_changes}")
    print(f"would migrate    : {len(migrations)}")
    print()

    for mig in migrations:
        rel = mig.path.relative_to(vault_root).as_posix()
        print(f"--- {rel}  [{mig.folder_key}]")
        print(f"    extracted: {list(mig.extracted.keys())}")
        if mig.skipped_labels:
            print(f"    skipped (unknown labels): {mig.skipped_labels}")
        if not args.quiet:
            print(render_diff(mig, vault_root))

    if args.apply:
        for mig in migrations:
            backup = mig.path.with_suffix(mig.path.suffix + ".bak")
            backup.write_text(mig.original_text, encoding="utf-8")
            mig.path.write_text(mig.new_text, encoding="utf-8")
            rel = mig.path.relative_to(vault_root).as_posix()
            print(f"applied: {rel}  (backup: {backup.name})")
        print()
        print(f"Done. {len(migrations)} file(s) rewritten.")
    else:
        print("(dry-run) re-run with --apply to write changes.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
