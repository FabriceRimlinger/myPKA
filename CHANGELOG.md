# Changelog

All notable changes to the myPKA scaffold are tracked here. Versions follow semver: MAJOR for breaking structural changes, MINOR for additions, PATCH for fixes.

## [1.8.2] - 2026-05-09

**Personalization placeholder + Tom-stand-in cleanup.** The scaffold's user-stand-in mentions of "Tom" are replaced with `{{USER_NAME}}` placeholder tokens. `ADAPTER-PROMPT.md` now captures the user's first name on first activation and substitutes the placeholder across the scaffold, saving the value to `PKM/.user.yaml` for future reference. Authorship credits ("Tom builds the system from scratch" video walkthrough) keep the formal name "Dr. Thomas Rödl". App Developer Pack `BUILD-NOTES.md` swept the same way.

### Changed

- `Team/Larry - Orchestrator/AGENTS.md` — "Tom double-clicks `start.command`" → "{{USER_NAME}} double-clicks `start.command`".
- `Team Knowledge/session-logs/_template.md` — example follow-up items "Tom reviews v1" → "{{USER_NAME}} reviews v1".
- `Team Knowledge/Workstreams/WS-003-install-an-expansion.md` — "Tom-approved canonical exception" → "Pre-canonicalized exception".
- `README.md`, `WAY-FORWARD.md` — "Tom builds the system" → "Dr. Thomas Rödl builds the system" (formal authorship credit).
- `ADAPTER-PROMPT.md` — new step 4: detect `{{USER_NAME}}` placeholders, ask user for first name, substitute across the scaffold, save to `PKM/.user.yaml`. Report-back template adds a `PERSONALIZATION` field.
- `AGENTS.md` — new "Personalization" section codifies the substitution rule for future content (e.g., Expansions that ship with `{{USER_NAME}}` tokens).
- App Developer Pack 1.0.1 `BUILD-NOTES.md` — swept "Tom" stand-ins to "the user" / "the maintainer".
- `VERSION` 1.8.1 → 1.8.2.

### Notes

- No code, schema, or contract changes. The `mypka-scaffold-latest.zip` URL pattern is preserved.
- App Developer Pack 1.0.1 manifest hash unchanged (only BUILD-NOTES.md edited; expansion.yaml bytes are identical).

## [1.8.1] - 2026-05-09

**Initial public release.** myPKA ships with a 9-person pre-hired AI team (Larry, Nolan, Pax, Penn, Mack, Silas, Charta, Pixel, Iris), full Personal Knowledge Architecture folder structure (PKM/My Life, PKM/CRM, PKM/Documents, PKM/Journal, PKM/Images), Team Knowledge layer (SOPs, Workstreams, Guidelines, Templates, session-logs), and the Expansions architecture for downloadable agent + connector packs.

### Highlights

- **Plain markdown.** Every note is a `.md` file. Works in Claude Code, Codex CLI, Gemini CLI, Cursor, ChatGPT, Obsidian + chat plugin, or any LLM that reads `AGENTS.md`.
- **Session-log triggers (LLM-agnostic).** Natural-language phrases like `close session`, `keep this in mind`, `let's realign` route the team's auto-memory across any LLM — not Claude-only.
- **External knowledge import.** [[WS-002-import-external-knowledge-base]] lets the team pull from Heptabase, Notion, Obsidian, Roam, Logseq, Mem, Capacities, Apple Notes, Evernote, Tana via MCP, or any SQLite-backed PKM tool.
- **Expansions architecture.** Day-1 packs (App Developer Pack, Slack Expansion) ship via the AI Library at [myicor.com](https://myicor.com). [[WS-003-install-an-expansion]] codifies the multi-agent install flow.
- **Frontmatter discipline.** `GL-002` defines field schemas for all eight entity types (Person, Organization, Project, Goal, Habit, Topic, Key Element, Document); `Team Knowledge/Templates/` ships the matching starters.
- **SQLite upgrade path.** [[SOP-002-convert-mypka-to-sqlite]] generates a derived SQLite mirror when the markdown layer outgrows plain files. Markdown stays canonical.
- **Design system primitive.** `GL-003` ships as an empty template; Iris populates it with the user via [[SOP-009-author-a-design-system]] on first creative request, then Charta/Pixel read from it for consistent style.

The `mypka-scaffold-latest.zip` URL pattern is non-negotiable — the myicor.com AI Library download button keeps serving `latest` with zero config changes across releases.
