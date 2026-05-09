# WS-002 - External Knowledge Import

- **Status:** Active (since v1.4.0)
- **Type:** Workstream — a multi-agent composition. The agents below collaborate to deliver the outcome. New Workstreams emerge when patterns repeat across session-logs; this one ships pre-canonicalized because the import flow needs the connection-half (Mack) and the content-shape (Silas) split working out of the box.
- **Owners:** **Silas (pre-hired)** is the primary executor — runs §2 onward (clarifying questions, inventory, plan, entity creation, wikilink normalization, session-log entry). **Mack (pre-hired)** runs the §1 connection layer when the source is reachable only via OAuth/API/MCP — fetches the bytes, lands them at a path, hands off to Silas. **Pax** for unfamiliar source formats that need research before the import plan is drafted.
- **References:** [[GL-001-file-naming-conventions]], [[GL-002-frontmatter-conventions]], [[SOP-002-convert-mypka-to-sqlite]], [[WS-001-daily-journaling]], [[Team Knowledge/Templates/INDEX]]
- **Triggered by:** any user phrasing that signals "bring my old notes from another tool into this myPKA." Trigger phrase contract is defined in the root `AGENTS.md` under **External Knowledge Import Triggers (LLM-agnostic)**. This Workstream is the canonical procedure those triggers run.

## Purpose

Take a user's existing knowledge base — exported from any PKM tool, sitting in a folder, a zip, an API, an MCP server, or a SQLite file — and land it inside this myPKA folder as a set of properly-shaped notes: correct folder, correct frontmatter per [[GL-002-frontmatter-conventions]], correct slug per [[GL-001-file-naming-conventions]], wikilinks normalized, attachments routed to `PKM/Images/YYYY/...`, and a session-log entry capturing what came in.

The Workstream is **procedure-only**. It does not perform any import on its own. The LLM running this procedure is the executor; the user is the source-of-truth on entity intent (what counts as a person vs a one-off mention, what's a project vs a note, etc.).

## What this Workstream does not do

- Does not migrate the **myPKA format** (markdown ↔ SQLite). That's [[SOP-002-convert-mypka-to-sqlite]]. WS-002 *invokes* SOP-002 in the SQLite-source case (see §5).
- Does not write new templates or new frontmatter fields. If a source has a concept that doesn't map to any of the eight entity types, the LLM raises it during the planning step (§4) and either drops the field, stores it in the body, or proposes a Guideline edit. It does not invent ad-hoc YAML keys.
- Does not delete or modify the source. The source is read-only throughout.
- Does not run an unattended bulk write. Every plan goes through user approval before any file is created.

## Inputs

The LLM accepts any of four source shapes. The detection step (§1) decides which.

| Source shape | Examples | How the LLM reads it |
|---|---|---|
| **File-based export** | Heptabase backup (folder of `.md` + `attachments/`), Notion export (zip of html/md + assets), Obsidian vault (folder), Roam JSON/EDN dump, Logseq folder, Mem export, Capacities export, Apple Notes export (HTML or plain), generic markdown folder | Filesystem reads. Walk the folder. Parse files. |
| **Live API** | Notion API (token + workspace), Evernote API, Readwise API (when used as a connector rather than via MCP) | Authenticated HTTP. Token via env var or user prompt. List → fetch → transform. |
| **MCP server (already running)** | Tana MCP, Mem MCP, Readwise MCP, Notion MCP | The LLM calls the server's tools directly. No re-auth. |
| **SQLite database** | Native Heptabase DB (`heptabase.db`), Logseq SQLite store, Capacities DB, any tool that exposes a `.db` file | Read-only `sqlite3` queries. See §5 for the special branch. |

## Step-by-step procedure

### Step 1 — Source detection

The LLM walks this decision tree based on what the user provides:

1. **Did the user paste a path?**
   - Path ends in `.zip` or `.tar.gz` → archive. Ask the user whether to extract in-place or to a temp dir. Treat as file-based after extraction.
   - Path is a directory → file-based export. Sniff for known signatures (see table below).
   - Path ends in `.db` or `.sqlite` → SQLite source. Jump to §5.
   - Path ends in `.json` or `.edn` → structured dump. Most often Roam, sometimes Mem. Treat as file-based.
2. **Did the user mention an API token / endpoint?** → Live API. Confirm scope (full workspace? a specific page tree?). Mask the token in any echo.
3. **Did the user say "I have [tool] MCP running" or did the LLM detect an MCP server with a tool name like `tana_*`, `mem_*`, `readwise_*`?** → MCP source. List the server's available tools, then plan around what's queryable.
4. **Did the user just name a tool with no path?** → Ask: "Do you have an export I should read, an API token, or is the [tool] MCP server already running?" Do not guess.

**Source signatures** the LLM can use to confirm a folder's origin:

| Tool | Tell |
|---|---|
| Heptabase | `Map.json` or `Whiteboards/` folder; per-card files; `attachments/` sibling |
| Notion (export) | `*.zip` containing folders named `<page-title> <hash>/` and `<page-title> <hash>.md` files |
| Obsidian | `.obsidian/` config folder at the root |
| Roam (JSON) | top-level array of page objects with `title`, `children`, `uid` |
| Roam (EDN) | starts with `^{:datoms` |
| Logseq | `pages/`, `journals/`, `assets/` siblings; `logseq/config.edn` |
| Mem | mostly markdown with `mem://` URIs in body |
| Capacities | `space.json` or `space.db` |
| Apple Notes export | folder of `.html` files with `iCloud` in metadata, or plain `.txt` per note |

If the signature is ambiguous, ask the user. Do not over-fit.

### Step 2 — Mandatory clarifying questions

Before any inventory, before any write, the LLM asks the user this set. They are not optional. Skip none. The answers shape the plan.

1. **Where is the source?** Absolute path / API endpoint + token / MCP server name.
2. **Entity intent.** Are there entities (people, organizations, projects, goals, habits, topics, key elements) inside the source you want extracted into PKM/CRM and PKM/My Life — or do you want everything filed as notes-as-notes into `PKM/Documents/`? Most users want extraction. Confirm explicitly.
3. **Existing frontmatter in the source.** Does the source already have YAML frontmatter? Three sub-questions if yes:
   - **Preserve as-is?** Keep every key the user already wrote.
   - **Normalize to GL-002?** Map known keys to the canonical schema, drop unknown keys to the body as a "## Source frontmatter (raw)" section.
   - **Override?** Replace source frontmatter with template-derived frontmatter, keep body only.
   Default if user is unsure: **normalize**. Surface the dropped keys so nothing disappears silently.
4. **Date field mapping.** Most sources have multiple timestamp fields (`created_at`, `updated_at`, `last_edited`, etc.). Which one becomes the canonical `date:` per [[GL-002-frontmatter-conventions]]? Default: `created_at`. Offer to also store `modified` if the source has a meaningful update timestamp.
5. **SQLite source branch.** If the source is SQLite-backed, ask: "Do you want to upgrade myPKA to SQLite first via [[SOP-002-convert-mypka-to-sqlite]], so we can move structured rows directly across — or transcribe everything to markdown into the existing folder structure?" See §5 for the full dialogue.
6. **Conflict policy.** If a target file already exists (e.g. `PKM/CRM/People/jane-doe.md` already lives in your myPKA), what's the rule?
   - **Skip** — leave the existing file alone, log the skip.
   - **Overwrite** — replace existing content with imported content (destructive; require explicit confirm).
   - **Rename** — write the new note as `<slug>-from-<source>.md` (e.g. `jane-doe-from-heptabase.md`) and let the user reconcile manually.
   Default: **rename**. Never silently overwrite.
7. **Attachment handling.** Two sub-questions: should images be (a) copied into `PKM/Images/YYYY/MM/` (default), or (b) referenced in place by absolute path (faster, but breaks if the source moves)? And what's the date to nest them under — the source's `created_at` for the parent note, or today?
8. **Tag policy.** If the source has tags, two options: (a) flatten into the YAML `tags: [...]` array per [[GL-002-frontmatter-conventions]] (default), or (b) reshape recurring tags into Topic notes under `PKM/My Life/Topics/`. The second is heavier but produces more interconnected wikis.

### Step 3 — Inventory

Once Step 2 answers are in, the LLM scans the source and produces an inventory **without writing anything to your myPKA yet**. The output is a count summary the user can sanity-check.

- **File-based:** walk the folder, count by extension and by detected entity type.
- **API:** paginate-list. Count by object type.
- **MCP:** call the server's list/search tools. Count by returned type.
- **SQLite:** `SELECT COUNT(*)` per source table. (If the user picked the SOP-002 path, hand off there now and stop.)

The inventory must include: total file/object count, count per detected entity type, count of attachments/images, count of unresolved internal links, and a short list of "didn't recognize this — what is it?" outliers.

### Step 4 — Plan + user approval

The LLM proposes a migration plan to the user. The plan is text, not action. The user must approve before any write happens.

The plan contains:

1. **Entity-count table.** "We see N people, M organizations, K projects, J goals, H habits, T topics, E key elements, D documents, X images, Y journal entries."
2. **Sample mapping per type.** For each non-zero entity type, show one before/after pair: source file → target path, source frontmatter → mapped GL-002 frontmatter, source body → cleaned body. The user can spot mis-mapping early.
3. **Wikilink normalization plan.** "We'll rewrite [[Source Title]] → [[source-title]] (kebab-case slug) where the target slug exists; we'll create stubs for the N links that don't resolve yet."
4. **Conflict report.** "F target paths already exist in your myPKA. Per your conflict policy (skip / overwrite / rename), here's what happens to each."
5. **Anomaly list.** Files that didn't parse, oversize attachments, password-protected blocks, encoding errors, anything odd.
6. **Estimated write count.** "We will create A new markdown files, B new image files, modify C INDEX.md files."

User approves → proceed to Step 5. User asks for changes → loop back to Step 2 or Step 4 as needed. User says no → stop, no writes happened, log the abort to the session-log.

### Step 5 — Create entities (per type)

For each entity discovered, the LLM:

1. Loads the matching template from `Team Knowledge/Templates/<type>.md`.
2. Populates frontmatter per [[GL-002-frontmatter-conventions]]. Source-side fields the schema doesn't accept go either to the body under a `## Notes from import` section or are dropped per the user's frontmatter answer in Step 2.
3. Generates the slug per [[GL-001-file-naming-conventions]] (kebab-case, ASCII, no special chars).
4. Writes to the destination per the mapping table in §6. Auto-creates `YYYY/MM/` folders as needed (same rule as [[WS-001-daily-journaling]]).
5. Updates the section's `INDEX.md` to list the new file.

**The eight entity templates are the only legal write targets for structured notes.** If a source concept doesn't map to one of the eight, file it as a `Document` (the catch-all) and note it in the import session-log for later review. Never invent a ninth type without going through SOP-001.

### Step 6 — Normalize wikilinks

After all files are on disk, walk every imported note and rewrite cross-references:

- `[[Source Title]]` → `[[<kebab-case-slug>]]` if the slug resolves to a file the LLM just created or one already in your myPKA.
- `[[orphan-link]]` (no resolve) → leave as-is and log to the orphans list. Do not auto-create empty stubs to make it resolve; let the user decide.
- Embeds (`![[...]]`) follow the same rule but pointed at the new `PKM/Images/YYYY/MM/` paths.

Idempotency: this step must be safe to re-run. The LLM tracks which notes it has already normalized via a small in-memory log; it does not double-rewrite.

### Step 7 — Import session-log entry

Write a session-log entry of type `proactive` under `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<agent>_external-knowledge-import.md`. The body must capture, at minimum:

- **Source:** tool name, path / endpoint / MCP server, size summary.
- **Decisions:** the user's answers to all eight clarifying questions.
- **Counts:** entities created per type, images copied, wikilinks rewritten, conflicts handled, anomalies parked.
- **Orphan wikilinks:** the full list, so the user can resolve them later.
- **What didn't import:** files that failed to parse, password-protected blocks, oversize attachments, encoding errors. Each with a one-line reason.
- **Cross-links:** to the trigger session entry, to any SOP-002 invocation, to the templates used.

This is the audit trail. Without it, the user has no way to verify the migration matches their intent.

### Step 8 — Optional graduation pass

While reading the source, the LLM may have encountered procedures that look like SOP / Workstream candidates (e.g. the source had a "Weekly Review" template the user clearly used; the source had a structured "Hiring Pipeline" view). The LLM lists those at the end of the session-log under `## Graduation candidates` and asks the user whether to spin any up via [[SOP-001-how-to-add-a-new-specialist]] or as a new SOP/Workstream. Do not auto-create them.

## Mapping table — generic source concept → myPKA destination

This is the canonical map. Every concrete source format collapses into this set of seven destinations. If a source format ships a concept that does not appear here, it goes to `PKM/Documents/` as a document-typed note with the source concept name preserved in the body, and the LLM flags it for graduation review (§8).

| Source concept | myPKA destination | Notes |
|---|---|---|
| daily note / journal entry / diary | `PKM/Journal/YYYY/MM/YYYY-MM-DD.md` (or `YYYY-MM-DD-<slug>.md` if the source has a per-day theme) | Apply the daily-note frontmatter shape used by [[WS-001-daily-journaling]]. If multiple entries exist for the same date, append as new sections in chronological order. |
| person / contact / human | `PKM/CRM/People/<slug>.md` | Use `Team Knowledge/Templates/person.md`. Required fields per [[GL-002-frontmatter-conventions]] §5. |
| company / institution / venue | `PKM/CRM/Organizations/<slug>.md` | Use `Team Knowledge/Templates/organization.md`. Cross-link to People who work there. |
| project / time-bound effort with a finish line | `PKM/My Life/Projects/<slug>.md` | Use `Team Knowledge/Templates/project.md`. |
| goal / objective / OKR / aspiration with a horizon | `PKM/My Life/Goals/<slug>.md` | Use `Team Knowledge/Templates/goal.md`. Goals link upward to a Key Element. |
| habit / routine / rhythm with a cadence | `PKM/My Life/Habits/<slug>.md` | Use `Team Knowledge/Templates/habit.md`. |
| topic / area / category / interest | `PKM/My Life/Topics/<slug>.md` | Use `Team Knowledge/Templates/topic.md`. Stable categories of attention, not projects. |
| MOC / index / hub / area-of-life / dimension | `PKM/My Life/Key Elements/<slug>.md` | Use `Team Knowledge/Templates/key-element.md`. Key Elements are dimensions (Health, Family, Career), not goals. |
| reference document / file-record / passport / contract / certificate | `PKM/Documents/<slug>.md` | Use `Team Knowledge/Templates/document.md`. |
| arbitrary note that doesn't fit the seven concept types above | `PKM/Documents/<slug>.md` | Same destination as references — Document is the catch-all for "this is content, but it isn't a Person/Org/Project/Goal/Habit/Topic/Key Element". Flag to the user during planning. |
| backlinks / wikilinks (`[[Title]]`, `((uid))`, `@mention`) | normalize to `[[<kebab-case-slug>]]` form | Slug rules per [[GL-001-file-naming-conventions]]. Roam-style block refs (`((uid))`) lose their granularity — they become a link to the parent page note. The LLM warns the user about this lossy step. |
| tags (`#tag`, `tag::value`, `tags: [...]`) | YAML `tags: [...]` array | Per [[GL-002-frontmatter-conventions]]. Hierarchical tags (`#parent/child`) flatten unless the user picked the "tags-to-Topics" option in Step 2. |
| attachments / images / inline files | `PKM/Images/YYYY/MM/<filename>` | Date subfolder uses the **parent note's** `created_at`, not today (per Step 2 answer). Filename preserved when sensible; collisions get a `-N` suffix. Embed via `![[Images/YYYY/MM/<filename>]]` per the [[WS-001-daily-journaling]] embed rule. |

## §5 — Special case: SQLite source detected

When Step 1 determines the source is a SQLite database, the LLM presents this dialogue **before** anything else:

> I see a SQLite database at `<path>`. Two ways to bring it in:
>
> **Option A — Upgrade myPKA to SQLite first.** I run [[SOP-002-convert-mypka-to-sqlite]] to turn this myPKA into a `.db` of its own, then port your source DB's rows into the new schema as a structured merge. Best when your source is large (5K+ rows), already DB-shaped, and you plan to keep it as DB going forward. You keep markdown as canonical for everything that doesn't fit the schema.
>
> **Option B — Transcribe to markdown.** I read the source DB row-by-row and write each row out as a markdown note in the matching `PKM/` folder, exactly the way I'd handle a markdown export. Best when your source is smaller, you want to read your knowledge as plain text in any editor, and you don't yet need DB performance.
>
> Which do you want?

If **A**: hand off to [[SOP-002-convert-mypka-to-sqlite]]. WS-002 stops here — SOP-002 is the executor. Reference WS-002 in SOP-002's session-log so the chain is traceable.

If **B**: continue with Step 2. Treat the source as a structured object stream, one row per entity, just as if it had been a JSON dump.

Default if the user is unsure: **B**. Markdown stays accessible. SOP-002 can always be run later.

## Edge cases / known gotchas

- **Duplicate detection.** When the source has the same person/org listed multiple times under different titles ("Jane Doe" and "Jane M. Doe"), the LLM uses content-hash + email/phone match where available to flag duplicates during the plan step (§4). It never auto-merges. The user picks the canonical record.
- **Encoding.** UTF-8 is expected. If the source is UTF-16 or Latin-1 (common with old Apple Notes / Evernote dumps), the LLM transcodes on read, never on write. Vault writes are always UTF-8 + LF.
- **Enormous attachments.** Files over ~25 MB are flagged in the plan, not auto-copied. The user picks: copy anyway, leave-by-reference, or skip with a body note pointing at the original location.
- **Password-protected blocks.** Notion's "locked" pages, encrypted Heptabase cards, password-protected Apple Notes — the LLM cannot read these. They get a body note: "Password-protected in source; not imported. Source path: `<path>`." and an entry in the session-log's "didn't import" section.
- **Partial failures.** If a write fails mid-batch (disk full, permission denied, OS interrupt), the LLM stops, reports the last-good file, and writes a partial-import session-log. Re-running the Workstream is idempotent — already-written files are detected by slug and skipped per the user's conflict policy.
- **Circular wikilinks.** A → B → A is fine and stays. The Step-6 normalization is graph-aware enough to not re-rewrite already-normalized links.
- **Tool says it has tags but they're stored as folders.** Some tools (early Bear, some Obsidian setups) encode tags as folder structure. The LLM detects this in Step 1 (folder names that look like `#projects/active`) and asks in Step 2: "These look like folder-based tags — should I lift them into the `tags:` array, or keep folder structure as Topic notes?"
- **Block references.** Roam, Logseq, and Tana have block-level addressing. The LLM imports the parent page as one note and flattens block refs to inline quotes with a "(was a block ref in source)" footnote. The session-log captures the block-id mapping for the user's audit.
- **Per-tool format drift.** Source export formats change between tool versions. If signature sniffing in Step 1 returns "Notion-like but not exactly v3 format," the LLM flags it and runs Pax (or the user's research specialist) to disambiguate before proceeding. Better a 5-minute pause than a wrong import.

## Definition of done

The Workstream is complete when **all** of these are true:

1. The user-approved entity counts from Step 4 match the actual file counts on disk per destination (within the tolerance for skipped/anomaly items the user explicitly approved).
2. Every new file in the eight entity folders validates against [[GL-002-frontmatter-conventions]] (required fields present, no ad-hoc keys, types correct).
3. Slugs match [[GL-001-file-naming-conventions]] (kebab-case, ASCII, no collisions in the same folder).
4. Wikilink rewrite pass produced zero broken links **except** the explicitly-logged orphans list. Orphans are surfaced to the user, not silently created as stubs.
5. Every relevant `INDEX.md` lists the new entries.
6. The import session-log exists at `Team Knowledge/session-logs/YYYY/MM/YYYY-MM-DD-HH-MM_<agent>_external-knowledge-import.md` and contains all eight sections from Step 7.
7. Larry's Librarian pass at session close (per [[WS-001-daily-journaling]] §5) finds no new SSOT violations.

## Trigger phrases

The trigger contract for this Workstream is in the root `AGENTS.md` under **External Knowledge Import Triggers (LLM-agnostic)**. Pattern-match intent, not literal strings. If a tool name in the user's request isn't recognized, ask clarifying questions per Step 2 — never refuse.
