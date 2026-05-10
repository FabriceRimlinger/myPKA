<!--
myPKA Scaffold - © 2026 Paperless Movement S.L.
Licensed under CC BY-NC-SA 4.0 - see LICENSE
ICOR, Paperless Movement are registered trademarks. See NOTICE.md
-->

# myPKA

**An AI powered Personal Knowledge Assistance system, based on our business-proven ICOR methodology. Plain markdown. Any LLM. Yours forever.**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.10.0-blue)
![Built on ICOR](https://img.shields.io/badge/built%20on-ICOR-C99A57)

myPKA is a folder. You drop it on your machine, point your LLM at it, and you have a nine-person AI team that organizes your life end to end. **It works on its own.** No database to set up, no SaaS to log into, no vendor to lose your data to.

**Watch the full walkthrough on YouTube:**

[![myPKA on YouTube - Stop Renting Your Knowledge. Switch OFF AI Auto-Memory.](github/youtube/launch-thumbnail.png)](https://www.youtube.com/watch?v=4C2w8eIG48A&feature=youtu.be)

> **Why this is different from other scaffolds.** Most folder structures are someone's preference dressed up as a system. myPKA is the working slice of **ICOR**, a methodology Paperless Movement S.L. and thousands of professionals world wide have been running their own business on for years. Every folder, every routing decision, every specialist contract maps to a piece of that framework. The structure is not arbitrary. The reasoning is teachable. Both matter when you scale past the first week.

## What's new in v1.10.0

This release adds three things, all in service of one outcome: **the team picks up where it left off, even across sessions, even when a different specialist takes over.**

- **A markdown-first task system.** Unfinished work gets written down as a plain `.md` file in `Team Knowledge/tasks/`. Folder location is the status. Frontmatter holds the cross-references back to the SOP, workstream, guideline, life entry, session log, and journal entry that give the work its context. Whoever opens the task next is one wikilink away from everything they need.
- **Per-agent journals.** Each specialist now has a `journal/` inside their team folder. They write a short entry whenever they learn something durable — an anti-pattern, a decision rule, a "next time, do it this way." The next session starts smarter than the last one ended.
- **An LLM-readable migration changelog.** `CHANGELOG-MIGRATION.md` at the root is a numbered, idempotent recipe any LLM can follow to upgrade an older myPKA folder. The folder is the database; the upgrade story lives in the folder too.

That's it. No new tools, no new dependencies. Just three small additions to the same plain-markdown shape. Additive — v1.9.x folders gain new directories without losing anything.

## Get going now

1. Clone or download the repo into a folder you'll actually use.
2. Open the folder in your LLM tool (Claude Code, Codex CLI, Gemini CLI, Cursor, or Obsidian + chat plugin).
3. Paste the contents of `initialize yourself in this folder` as your first message.
4. The LLM reads `ADAPTER-PROMPT.md`, writes a tool-specific pointer file (`CLAUDE.md`, `GEMINI.md`, etc.), and reports the team is online.
5. Ask "Who are you?" and you'll see Larry is at your service.
6. Ask "What's open?" and Larry walks the new `Team Knowledge/tasks/open/` folder for you.

That's the whole setup. There is no install step.

Once you have the team online and start using it, you'll hit moments where you wonder why a folder is shaped the way it is. That's where the courses come in. They teach the WHY behind every folder choice, so you understand why the team is built like real humans operating on the **ICOR methodology**, not just another AI scaffold. More on that below.

## What you get

A working knowledge system, fully assembled, that does this on day one:

- **Organizes your life from a single daily journal.** You write what happened. The team files the people, projects, decisions, and ideas where they belong. Connections between notes are made for you.
- **Remembers unfinished work for you.** When something can't finish in one turn, the team writes it down as a task in `Team Knowledge/tasks/`. Next session, Larry walks `tasks/open/` and surfaces what's waiting. The team genuinely picks up where it left off.
- **Carries learning forward.** Each specialist keeps a journal of durable insights at `Team/<Name>/journal/`. When a task references one of their entries, they re-read their own past thinking before starting work.
- **Runs in any LLM you already use.** Claude Code (and Claude Cowork), Codex CLI, Gemini CLI, Cursor, ChatGPT, Obsidian with a chat plugin. The same scaffold, the same team, the same files. You change models. Your knowledge doesn't move. Session-log triggers (`close session`, `keep this in mind`, `let's realign`, etc.) work with any LLM that reads `AGENTS.md` — ChatGPT, Claude, Gemini, Cursor, Cline, Codex, and the rest. Not Claude-only.
- **Stays in plain markdown.** Every note is a `.md` file. You can read it without the AI. You can grep it. You can sync it with Dropbox or git. You can open it in Obsidian and keep working with no AI at all.
- **Upgrades to SQLite when you outgrow plain files.** Once your myPKA gets large, paste the prompt at `Team Knowledge/SOPs/SOP-002-convert-mypka-to-sqlite.md` into your LLM. Markdown stays canonical. SQLite becomes a fast lookup layer on top.
- **Imports from any PKM tool.** Drop your existing notes (Heptabase backup, Notion export, Obsidian vault, Roam graph, Logseq folder, Apple Notes export, Evernote dump, Tana via MCP, etc.) anywhere on disk, then ask your LLM something like *"import my Notion export from `~/Downloads/notion.zip`"* or *"how do I bring in my Heptabase backup?"*. The scaffold ships with [[Team Knowledge/Workstreams/WS-002-import-external-knowledge-base]] — the LLM follows it to extract entities (people, organizations, projects, goals, habits, topics, key elements, documents), normalize wikilinks to the slug form, copy attachments into `PKM/Images/YYYY/MM/`, and place files into the right folders, asking clarifying questions where needed and never overwriting your myPKA without explicit approval. Works with any LLM that reads `AGENTS.md`.

There is no lock-in. The whole system is text on your disk. It works in Obsidian today. It upgrades to SQLite when you want it. It runs on whichever model or LLM you prefer, and it keeps running when you switch.

## Who this is for

- **Knowledge workers** who want a local folder setup instead of handing over their knowledge to Notion, Tana etc. and want an AI team that actually files things. Transparent and accessible.
- **Founders and operators** running multiple projects who need a knowledge system that thinks across People, Topics, Goals, Habits, and Key Elements without manual cross-linking.
- **Parents and generalists** with too many inputs (school stuff, health stuff, ideas, contacts) and no structure to hold it.
- **AI tinkerers** who want a real reference architecture for a multi-agent setup, not a toy demo.

If you've ever opened a blank Obsidian vault and didn't know where to put anything, this is for you. (Yes — myPKA is fully Obsidian-compatible. Open the folder as an Obsidian vault and everything just works.)

## Meet the team

Nine specialists ship pre-loaded. **You only ever talk to Larry.** Larry routes.

<table>
<tr>
<td width="140" align="center"><img src="github/team/larry.png" width="120" alt="Larry the Red Fox - Team Leader and Orchestrator" /></td>
<td><b>Larry - Team Leader & Orchestrator</b><br/><i>A Red Fox. Sharp ears, sharper instincts.</i><br/><br/>Every request you make lands with Larry first. He clarifies, picks the right specialist, hands off the brief, and synthesizes the answer back to you. He's also the team's <b>Librarian</b> (keeps the wiki clean, fixes broken <code>[[wikilinks]]</code>, enforces the SSOT Golden Rule), <b>Session-Log Author</b> (writes a daily log of what the team did and what changed), and as of v1.10.0, the team's <b>Task Walker</b> (surfaces what's open at session start). Larry never executes specialist work himself - that's the iron rule.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/nolan.png" width="120" alt="Nolan the Pitbull - Talent Acquisition" /></td>
<td><b>Nolan - Talent Acquisition</b><br/><i>A Pitbull in glasses. Loyal, methodical, allergic to lazy hires.</i><br/><br/>When you outgrow the nine shipped specialists, Nolan handles the hire end-to-end: briefs Pax for research, drafts the new specialist's contract (<code>AGENTS.md</code>), validates against the SOP, and gets your sign-off before adding anyone to the roster. Nolan is the reason your team scales without diluting.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/pax.png" width="120" alt="Pax the Raven - Deep Research" /></td>
<td><b>Pax - Deep Research</b><br/><i>A Raven. Patient, source-cited, allergic to a single-source answer.</i><br/><br/>When something matters - a hire, a market read, a "is this actually true" - Pax goes wide before going deep. Returns a triangulated brief in <code>Deliverables/</code>, never a one-shot opinion.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/penn.png" width="120" alt="Penn the Owl - Journal Writer" /></td>
<td><b>Penn - Journal Writer</b><br/><i>A Barn Owl. Quiet, watchful, careful filer.</i><br/><br/>Penn handles the team's scribe duties. Drop screenshots, voice memos, business cards, or rough thoughts into <code>Team Inbox/</code>. Penn files everything into the right corner of <code>PKM/</code> with the right <code>[[wikilinks]]</code>. He never forgets where things go and never assumes you're done thinking when you drop something in.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/mack.png" width="120" alt="Mack - Automation and Integration Specialist" /></td>
<td><b>Mack - Automation & Integration Specialist</b><br/><i>The connection layer. Quiet when it works, loud when it breaks.</i><br/><br/>Mack wires your myPKA to the rest of the world. MCP server setup, API integrations, webhook receivers, OAuth flows, and any automation that needs to run reliably in the background. When an external knowledge import needs an authenticated fetch first (Notion API, Apple Notes export, a live MCP server), Mack establishes the connection, lands the bytes at a path, and hands off to Silas to run the actual import. Idempotency, retries, structured logs, credentials in <code>.env</code> — never in code.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/silas.png" width="120" alt="Silas - Database Architect" /></td>
<td><b>Silas - Database Architect</b><br/><i>Schema is destiny. Slugs are primary keys.</i><br/><br/>Silas guards the structural integrity of your knowledge base. He runs external knowledge imports (drop a Notion zip, a Heptabase backup, an Obsidian vault, a Roam graph — Silas runs <code>WS-002</code> and lands the entities in the right folders), audits frontmatter against <code>GL-002</code>, catches schema drift before it spreads, and runs the markdown-to-SQLite conversion (<code>SOP-002</code>) when your myPKA outgrows plain files. Markdown stays canonical; the SQLite mirror is a regenerable performance layer. Silas never invents fields, never silently rewrites content, and never lets ad-hoc YAML keys accumulate.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/charta.png" width="120" alt="Charta - Infographic Designer" /></td>
<td><b>Charta - Infographic Designer</b><br/><i>Structure over decoration. Code is the canvas.</i><br/><br/>Charta turns information into single-image, scannable visuals. Comparison tables, feature grids, decision guides, process flows, flowcharts, decision trees, timelines, swimlanes, hub-and-spoke diagrams, quadrant matrices, carousels, PDFs from clean HTML. Her canonical skill is <code>SOP-007</code> (build an infographic): structure-first content design via HTML/CSS/SVG, render to PNG/PDF via headless browser. Charta reads from <code>GL-003</code> (the design system) on every task — no ad-hoc palette choices, no random font picks. When a deliverable needs photographic or AI-generated finishing, Charta drafts the structure and hands off to Pixel.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/pixel.png" width="120" alt="Pixel - Visual Specialist" /></td>
<td><b>Pixel - Visual Specialist</b><br/><i>Every image is built one pixel at a time. Precision matters.</i><br/><br/>Pixel handles image stylization: thumbnails, social images, hero illustrations, quote cards, multi-reference composites. Her canonical skill is <code>SOP-008</code> (generate a styled image): five-part prompt construction, multi-reference handling, three capability paths (local image-gen / Mack-wired external API/MCP / fallback design-brief-for-human). Pixel reads from <code>GL-003</code> for palette, imagery direction, type roles, and voice. When the user's LLM lacks image generation, Pixel routes the connection half to Mack to wire up Gemini / OpenAI Images / Flux / any image-capable MCP, then drives the prompt once it's online.</td>
</tr>
<tr>
<td width="140" align="center"><img src="github/team/iris.png" width="120" alt="Iris - Design System Architect" /></td>
<td><b>Iris - Design System Architect</b><br/><i>A design system is a living contract. Every hardcoded color is a broken promise.</i><br/><br/>Iris is the brand and design-system specialist. She authors <code>GL-003</code> (the design system: identity, color palette, typography, spacing scale, imagery style, voice samples) through guided sessions with you, never pre-populated with "sensible defaults" you didn't pick. Her canonical skills are <code>SOP-009</code> (author the design system) and <code>SOP-010</code> (audit deliverables against it). The first time you ask for any creative work without GL-003 populated, Larry routes to Iris first to pin the values — once filled, every creative agent reads from here for consistent style.</td>
</tr>
</table>

Each specialist has a contract at `Team/<Name> - <Role>/AGENTS.md`, and as of v1.10.0, a `journal/` folder for durable insights. Full routing table at `Team/agent-index.md`.

> The full Paperless Movement team - including the AI specialists you can add via the **AI Library** - is at [myicor.com](https://myicor.com).

## What lives where

- `PKM/` is your knowledge. `My Life/` holds the five life concepts (Goals, Habits, Topics, Projects, Key Elements). `Documents/`, `CRM/`, `Images/`, and `Journal/` sit alongside it. Notes connect through `[[wikilinks]]`, not nested folders.
- `Team/` holds your specialists. One folder per agent. Each has its own `AGENTS.md` and, as of v1.10.0, its own `journal/` for durable cross-session insights.
- `Team Knowledge/` holds the team's playbook. SOPs are atomic procedures. Workstreams orchestrate multi-agent flows. Guidelines are static reference info. **`tasks/` is new in v1.10.0** and holds unfinished work the team is tracking across sessions (`open/`, `in-progress/`, `done/<YYYY>/<MM>/`, `cancelled/<YYYY>/<MM>/`).
- `Deliverables/` is where the team puts work-in-progress and finished artifacts - research briefs, hire workups, multi-file projects. Time-stamped, ephemeral, the team's working surface. **Pax** drops research here. **Nolan** drops hire workups here. **Larry** collects multi-specialist work here.
- `Team Inbox/` is your drop zone for raw inputs. Drop screenshots, voice memos, business cards, links, or a quick braindump and the team files them into PKM. *"I have something, not sure where"* goes here. **Penn** usually picks it up, **Larry** routes it.
- `AGENTS.md` at the root is the source of truth for how the whole team behaves.

> **Note on note shape.** Every entity note (a Person, an Organization, a Project, a Goal, a Habit, a Topic, a Key Element, a Document) starts from a template in `Team Knowledge/Templates/`. Structured data lives in YAML frontmatter at the top of the file; narrative lives in the body. The canonical field schemas are in [[Team Knowledge/Guidelines/GL-002-frontmatter-conventions]]. The mypka-interface Properties tab and the SQLite migration both read frontmatter — keep your facts there, your stories in the body.

## How a task flows

Here's the whole shape, in plain English.

You ask the team to do something that won't finish in one turn. Larry (or whoever picked up the request) writes a small markdown file into `Team Knowledge/tasks/open/`. The frontmatter names who it's for, why it matters, and what context already exists: which SOP applies, which workstream it belongs to, which session log birthed it, which life entry it touches, which journal entry the assignee should re-read first. The body restates the work in your words.

When the assignee picks it up, the file moves from `open/` to `in-progress/` and they leave a one-line update inside it. They keep working. If they get blocked, they write the reason in the frontmatter so they (or someone else) know what to chase. When it's done, the file moves to `done/<year>/<month>/` with the outcome written in.

Next session, Larry walks `tasks/open/` and `tasks/in-progress/` first, before doing anything else. The team starts the day knowing what's waiting and where things stood. Nothing falls on the floor between sessions.

The journal sits next to this. When the assignee learns something durable while working a task — a build pattern that worked, an anti-pattern they want to remember, a rule of thumb — they write a short entry in their `journal/`. The next time a task references that entry, they re-read their own past thinking before starting. Learning compounds across sessions.

## Migrating from v1.9.x to v1.10.0

v1.10.0 is purely additive. v1.9.x folders gain new directories and templates. Nothing existing is moved, renamed, or modified.

Open `CHANGELOG-MIGRATION.md` at the root and ask your LLM to run the recipe. It's nine numbered, idempotent steps. You can audit each one before it runs. After the migration, run `bash validation-script.sh .` from the scaffold root — it exits 0 when the upgrade is structurally complete.

## Principles

A few things we believe, that the folder is shaped around.

- **Continuity over ceremony.** The team should be able to pick up where it left off, across sessions, even when a different specialist takes over. Tasks and journals serve that, nothing else. There is no lifecycle theater.
- **The folder is the database.** Plain markdown, on your disk, readable without the AI. Frontmatter is the machine-readable layer. Wikilinks are the navigation layer. All three reinforce each other so any one of them is enough to act.
- **Portability is the point.** You can swap LLM tools without migrating. You can sync the folder with Dropbox, iCloud, or git. You can open it in Obsidian on your phone. Your knowledge follows you, not the vendor.
- **LLM-agnostic by construction.** Anything the team does, any agent can do, with `mv`, `mkdir`, `grep`, `awk`. No model-specific magic. No proprietary tool calls. If you can read markdown, you can run myPKA.
- **Additive upgrades only.** When the scaffold gains a capability, older folders gain it without losing anything. Migration is plain-text recipes you can audit. Nothing destructive without your explicit OK.

## Coming from another tool?

- **Obsidian users**: open your myPKA folder as an Obsidian vault. Wikilinks, tags, and Markdown work as you expect. The scaffold adds an AI team on top of the folder you already understand.
- **Notion users**: the closest analogue is "Pages with AI inside, but the pages are files on your disk." You lose Notion's database views. You gain ownership of every byte and the ability to swap LLMs without migrating.
- **Roam / Logseq users**: same daily-note instinct. The team handles the cross-linking you used to do by hand.

## The deeper story: ICOR methodology

If you want to really manage your life efficiently and run this folder structure the way it is meant to work, the methodology is the missing layer.

myPKA is built on the **My Life** part of the **ICOR methodology**. ICOR is tool-agnostic Paperless Movement S.L. and thousands of professionals use to run both personal life and business: five life concepts on one side, five business concepts on the other, with a shared way of capturing, processing, and acting on information. We have been running on it for years. The scaffold you just downloaded is one slice of that framework, made operational.

Watch the deep-dive walkthrough where Dr. Thomas Rödl builds the system from scratch and explains the reasoning behind each folder, each agent, and each routing rule:

**[Watch the deep-dive on YouTube](https://www.youtube.com/watch?v=4C2w8eIG48A&feature=youtu.be)**

The full courses live at **[myicor.com](https://myicor.com)**. They cover:

- **The Personal half (myPKA)**: the WHY behind every folder in this scaffold, how the five life concepts (Goals, Habits, Topics, Projects, Key Elements) connect, and how to operate the team so it actually saves you time instead of becoming another tool to manage.
- **The Business half**: the same framework extended to companies, including the operating system Paperless Movement S.L. runs on internally.

The scaffold works on its own. The course is for people who want to understand why it works, so they can extend it without breaking the model.

## AI Library (membership)

Once you've used myPKA for a while, you'll want more than nine specialists. The **AI Library** at [myicor.com](https://myicor.com) is the membership layer where you download **Expansions** — drop-in folders that grow your team. These Expansions are not in this repo and are not planned to be open-sourced:

- **Slack Expansion** so the team can read and act on conversations from your workspace.
- **Obsidian optimizations** including templates, plugins, and views tuned to the scaffold.
- **Agent packs** that drop into your `Expansions/` folder: an App Developer pack (Felix + Vex + Vera), a Marketing pack, a Customer Support pack, a Bookkeeping pack, and others.
- **Connector Expansions** for the tools you already live in (Notion, Readwise, Linear, …).
- **Office hours and walkthroughs** with the team that builds this scaffold.

Membership-only is honest, not a gate. The scaffold here is genuinely complete. The AI Library is for people running serious work on top of it. See `Expansions/docs/expansion-spec.md` for the install model.

## License and trademarks

- **Content and code**: [CC BY-NC-SA 4.0](LICENSE). Free for personal and non-commercial use, with attribution and share-alike.
- **Registered trademarks (US)**:
  - PAPERLESS MOVEMENT - USPTO Reg. No. 6,689,873
  - ICOR - USPTO Reg. Nos. 6,607,819 and 6,608,200
- **Common-law marks**: myICOR, myPKA
- See [NOTICE.md](NOTICE.md) for trademark usage guidelines.
- Commercial licensing: contact@myicor.com

## Disclaimer

The myPKA scaffold is a teaching artifact, not a production system. It is provided **as is**, without warranty of any kind, express or implied. The authors and copyright holders make no guarantees about fitness for a particular purpose, the behaviour of any LLM you point at the folder, the safety of any AI agent's reads or writes, or the integrity of your data over time.

You are responsible for your own backups, your own data hygiene, your own choice of LLM tools and what you allow them to access on your machine. We are not liable for data loss, business interruption, or any other damages arising from use of this scaffold or its examples. **Use at your own risk.**

See [LICENSE](LICENSE) for the full disclaimer of warranties and limitation of liability.

## Built by

myPKA is built by **Dr. Thomas Rödl** and **Paco Cantero** at **Paperless Movement S.L.**, the company behind myICOR and the ICOR methodology. We use this scaffold every day. The version you're looking at is the version we run.

If it helps you, the best thank-you is to come learn the methodology at [myicor.com](https://myicor.com).
