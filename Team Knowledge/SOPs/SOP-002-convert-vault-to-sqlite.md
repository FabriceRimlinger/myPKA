# SOP-002 - Convert Markdown Vault to SQLite

- **Owner:** the user (with any code-capable LLM as the executor)
- **Triggered by:** the user decides their markdown vault has outgrown plain files and wants a SQLite mirror for structured queries, analytics, or LLM-side performance.
- **References:** [[GL-001-file-naming-conventions]], [[Team Knowledge/INDEX]]

## Purpose

Generate a SQLite database that mirrors the current state of the markdown vault. The markdown stays the source of truth - SQLite is a derived performance layer, regenerated on demand.

This SOP is a **prompt-as-deliverable**. The body of this file (everything below the divider) is meant to be pasted verbatim into a code-capable LLM (Claude Code, Codex CLI, Cursor, or any chat LLM with code execution). The LLM produces a Python script and the resulting `.db` file. The vault is read-only throughout.

## When to run this SOP

Pick at least two of the following before bothering:

- Vault has crossed roughly 5,000 markdown files and grep-based search is getting slow.
- You are running structured queries the LLM has to repeat often ("show me every Project linked to a Goal under the Health Key Element").
- You want analytics across the vault (entries per week, people-mention frequency, document expiry timelines).
- You are syncing across multiple devices and want a single binary to ship instead of thousands of files.

If none of these apply, stay on markdown. SQLite is overhead you do not need yet.

## When NOT to run this SOP

- Your primary tool is Obsidian and you rely on its graph view or plugins. SQLite does not interoperate with those.
- Your vault is under 1,000 files. Markdown handles that effortlessly.
- You are editing across multiple authors. Two people regenerating SQLite from divergent markdown is a merge nightmare.

## What this SOP produces

1. `vault_to_sqlite.py` at the vault root - the migration script.
2. `mypka_from_vault.db` next to it - the generated database.
3. A migration report at `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-vault-to-sqlite.md` with row counts, parsing failures, and unresolved wikilinks.

The reverse direction (SQLite -> markdown) is reserved for a future SOP. For now, treat the markdown vault as canonical and the SQLite as a snapshot you can regenerate.

---

# Vault to SQLite migration prompt (paste this into your LLM)

You are migrating a markdown-only Personal Knowledge Architecture (myPKA) vault into a SQLite database. The goal is a deterministic, idempotent script and the resulting `.db` file. The markdown vault stays the source of truth.

## Context

- **Vault root:** ask the user for the absolute path. Default to the current working directory if they do not specify.
- **Engine:** Obsidian-flavoured markdown. Cross-references are `[[wikilinks]]`. Embeds are `![[path]]`.
- **Source of truth for each note:** YAML frontmatter on the file plus the structured folder path.
- **Naming convention:** kebab-case slugs, `YYYY-MM-DD-` prefix on date-driven files. See `Team Knowledge/Guidelines/GL-001-file-naming-conventions.md`.

## Folder map

```
PKM/
├── Journal/YYYY/MM/YYYY-MM-DD-<slug>.md       -> journal table
├── CRM/
│   ├── People/<slug>.md                        -> people table (relation != family)
│   └── Organizations/<slug>.md                 -> organizations table
├── My Life/
│   ├── Topics/<slug>.md                        -> topics table
│   ├── Projects/<slug>.md                      -> projects table
│   ├── Key Elements/<slug>.md                  -> key_elements table
│   ├── Goals/<slug>.md                         -> goals table
│   └── Habits/<slug>.md                        -> habits table
├── Documents/<slug>.md                         -> documents table (metadata)
└── Images/YYYY/MM/...                          -> referenced via ![[…]] embeds, not inserted directly
```

INDEX.md files in each folder are navigation hubs. Skip them. Do not insert.

## Step-by-step

### 1. Set up

- Create a fresh empty SQLite file: `mypka_from_vault.db`.
- Define the schema with these tables (and only these): `people`, `organizations`, `topics`, `projects`, `key_elements`, `goals`, `habits`, `journal`, `documents`, `journal_media`, `content_index`. Do not invent columns the markdown has no source for.
- Open one DB connection. Use a single transaction per table for atomicity.

### 2. Build a slug to id resolver

For tables with FK references (`journal.key_element_id`, `journal.project_id`, etc.), you need to map a kebab-case slug back to an integer primary key. Strategy:

1. **First pass insert:** people, organizations, topics, key_elements, projects, goals, habits. These have no FKs to journal or documents.
2. **Build in-memory dicts:** `people_by_slug = {slug: id}`, etc.
3. **Second pass insert:** journal, documents. Resolve FKs via the dicts.
4. **Third pass insert:** junction rows (`journal_media`, `content_index` for wikilink-derived relations).

### 3. Frontmatter to column mapping

Each markdown file starts with a `---`-delimited YAML block. Parse with PyYAML or equivalent. The mapping below tells you which frontmatter keys map to which columns. **If a key is absent, write `NULL`. Do not guess.**

**`people` table** (sources: `PKM/CRM/People/`)

| Column | Source |
|---|---|
| `slug` | filename stem |
| `full_name` | frontmatter `full_name`, fallback to first H1 in body |
| `first_name`, `last_name` | derive by splitting `full_name` on first space if not present in frontmatter |
| `relation` | frontmatter `relation` |
| `email`, `phone`, `city`, `birth_date`, `linkedin_url` | same key in frontmatter |
| `company`, `role`, `last_contact` | same key |
| `notes` | body text after the H1 |

**`organizations`** (sources: `PKM/CRM/Organizations/`)

| Column | Source |
|---|---|
| `slug` | filename stem |
| `name` | frontmatter `name` or first H1 |
| `type` | frontmatter `org_type` |
| `industry`, `website`, `email`, `phone`, `city` | same |

**`topics`, `key_elements`, `projects`, `goals`, `habits`**

For each: `slug` (filename stem), `name` (frontmatter `name` or first H1), `description` (body text), and any other frontmatter keys present. For `parent_id` references, parse the body for `Parent: [[<slug>]]` patterns and resolve in the second pass.

**`journal`** (sources: `PKM/Journal/YYYY/MM/*.md`)

| Column | Source |
|---|---|
| `entry_date` | frontmatter `date`, fallback to filename `YYYY-MM-DD-` prefix |
| `category`, `entry_type`, `mood`, `energy` | same key in frontmatter |
| `title` | first `# ` heading after frontmatter |
| `content` | everything after the title down to (but not including) any `## Media` or `## Links` section |
| `key_element_id`, `project_id`, `topic_id` | resolve from frontmatter slug references |
| `tags` | frontmatter `tags`, JSON-encoded |

**`journal_media`** (sources: `## Media` section in journal entries)

For each `![[Images/YYYY/MM/<file>]]` line, insert one row:

| Column | Source |
|---|---|
| `journal_id` | the parent journal row's id |
| `file_path` | the embed path, normalized to vault-relative |
| `media_type` | infer from filename (screenshot if path contains "screenshot" or "social", else image) |
| `mime_type` | from file extension |
| `caption` | the italic line `_caption text_` immediately under the embed, if present |
| `image_data` | leave NULL. The file on disk is the source of truth. |
| `sort_order` | 0-based index within the `## Media` section |

**`documents`** (sources: `PKM/Documents/*.md`)

| Column | Source |
|---|---|
| `slug` | filename stem |
| `title` | frontmatter `title` or first H1 |
| `doc_type` | frontmatter `doc_type` |
| `physical_location`, `digital_location` | same key |
| `expiry_date`, `renewal_trigger` | same |
| `notes` | body text |

### 4. Wikilink to relation extraction

After all base tables are populated, do a third pass:

- For each journal entry, scan the body for `[[<slug>]]` patterns. Look up each slug in your dicts. For each resolved slug, insert a row into `content_index` with `source_table='journal'`, `source_id=<journal.id>`, and `target_table` + `target_id` from the resolved slug.
- For each document, scan the body for `[[<person-slug>]]` mentions. Look up in `people_by_slug`. Insert into `content_index` analogously.

### 5. Validation

After insert, run these queries and report counts:

```sql
SELECT 'journal', COUNT(*) FROM journal
UNION ALL SELECT 'people', COUNT(*) FROM people
UNION ALL SELECT 'organizations', COUNT(*) FROM organizations
UNION ALL SELECT 'topics', COUNT(*) FROM topics
UNION ALL SELECT 'projects', COUNT(*) FROM projects
UNION ALL SELECT 'key_elements', COUNT(*) FROM key_elements
UNION ALL SELECT 'goals', COUNT(*) FROM goals
UNION ALL SELECT 'habits', COUNT(*) FROM habits
UNION ALL SELECT 'documents', COUNT(*) FROM documents
UNION ALL SELECT 'journal_media', COUNT(*) FROM journal_media
UNION ALL SELECT 'content_index', COUNT(*) FROM content_index;
```

Compare against the file counts on disk:

```bash
find "$VAULT/PKM/Journal" -name '*.md' -not -name 'INDEX.md' | wc -l
find "$VAULT/PKM/CRM/People" -name '*.md' -not -name 'INDEX.md' | wc -l
# ...etc per folder
```

The DB counts should match within a small tolerance. Allow for genuinely empty files or files with no parseable frontmatter, but report each one.

### 6. Idempotency

The script must be safe to re-run. Two acceptable strategies:

- **Drop and recreate:** delete `mypka_from_vault.db`, recreate from scratch on every run. Simplest. Fine for vaults under ~10K files.
- **Upsert by slug:** `INSERT ... ON CONFLICT(slug) DO UPDATE ...`. Required if the user wants to incrementally re-sync as they edit the vault.

Default to drop-and-recreate unless the user asks otherwise.

### 7. Output

Deliver three things:

1. The script itself (`vault_to_sqlite.py`), saved at the vault root.
2. The generated `mypka_from_vault.db` next to it.
3. A migration report at `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-vault-to-sqlite.md` with:
   - Row counts per table.
   - Any files that failed to parse (path + reason).
   - Any wikilinks that did not resolve to an existing slug.
   - Schema produced (the actual CREATE TABLE statements run).

## Hard rules

1. **Do not modify the vault.** Read-only. Write only the `.db`, the script, and the report.
2. **No fabrication.** If a frontmatter key is missing, use `NULL`. Do not infer values from prose unless this SOP explicitly says to.
3. **Preserve filename slugs as primary keys.** Slug uniqueness within a table is the migration's identity contract.
4. **No BLOB inlining by default.** `journal_media.image_data` and any equivalent for documents stays NULL. The filesystem path is the source of truth.
5. **Log skipped content.** Anything that does not parse cleanly goes in the report. Do not silently drop it.

## When done

Report back to the user with:
- Path to the script
- Path to the generated DB
- Row counts
- Path to the migration report
- Any files or wikilinks that need manual reconciliation
