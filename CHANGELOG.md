# Changelog

All notable changes to the myPKA scaffold are tracked here. Versions follow semver: MAJOR for breaking structural changes, MINOR for additions, PATCH for fixes.

## [1.9.0] - 2026-05-09

**Host subagent binding ships out of the box.** First activation now generates host-specific subagent shims so the eight deputies (Penn, Pax, Nolan, Mack, Silas, Charta, Pixel, Iris) can dispatch in parallel via the host's agent runtime — not role-played in a single context. Larry is excluded (he's the main-session identity, not a dispatched subagent).

The contract: **two layers, never three.** The wiki contract at `Team/<Name>/AGENTS.md` is canonical and host-agnostic. The host shim (`.claude/agents/<slug>.md` for Claude Code; `.codex/agents/<slug>.md` for Codex if supported; per-spec for Gemini) is a thin pointer that the host runtime reads to dispatch the specialist. We do NOT add a third layer (e.g. a `CLAUDE.md` inside each `Team/<Name>/`) — that violates SSOT.

### Added

- `.claude/agents/{charta,iris,mack,nolan,pax,penn,pixel,silas}.md` — Claude Code subagent shims for the eight deputies. YAML frontmatter (`name`, `description`, `tools`) + body that points back to the wiki contract via path. ~30-60 lines each. Larry is intentionally excluded.
- `ADAPTER-PROMPT.md` Step 7 (new) — host-agnostic procedure to walk `Team/`, derive each slug, and generate host-specific shims on first init. Per-host matrix: Claude Code → `.claude/agents/`, Codex CLI → `.codex/agents/` (when supported), Gemini CLI → per spec, Cursor / chat-only → noted limitation. **Idempotent** — re-running Step 7 skips any pre-existing shims (never overwrites user customizations). Report-back template adds `HOST SUBAGENT BINDING` field listing written + skipped.

### Changed

- `Team/Nolan - HR/AGENTS.md` — every hire now ships two artifacts: the wiki contract AND the host shim(s) for every host the user has activated. Detection by pointer-file presence (`CLAUDE.md`, `AGENTS.md.codex`, `GEMINI.md`, `.cursor/rules/main.md`).
- `Team Knowledge/SOPs/SOP-001-how-to-add-a-new-specialist.md` §5 — host-agnostic principle plus host-specific shim path matrix. Two artifacts always go together.
- `VERSION` 1.8.2 → 1.9.0.

### Notes

- No code, schema, or contract changes vs 1.8.x. Host bindings are additive; the wiki contracts are unchanged.
- The `mypka-scaffold-latest.zip` URL pattern is preserved.
- Existing v1.8.x users who upgrade get the eight shims AND the new Step 7 in the next adapter run. The idempotency rule means any manual customizations to existing shim paths are preserved.

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
