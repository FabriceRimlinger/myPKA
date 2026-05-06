<!--
myPKA Scaffold - © 2026 Paperless Movement S.L.
Licensed under CC BY-NC-SA 4.0 - see LICENSE
ICOR, Paperless Movement are registered trademarks. See NOTICE.md
-->

# myPKA

**An AI powered Personal Knowledge Assistance system, based on our business-proven ICOR methodology. Plain markdown. Any LLM. Yours forever.**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Built on ICOR](https://img.shields.io/badge/built%20on-ICOR-C99A57)

myPKA is a folder. You drop it on your machine, point your LLM at it, and you have a four-person AI team that organizes your life end to end. **It works on its own.** No database to set up, no SaaS to log into, no vendor to lose your data to.

**Watch the full walkthrough on YouTube:**

[![myPKA on YouTube - Stop Renting Your Knowledge. Switch OFF AI Auto-Memory.](assets/youtube/launch-thumbnail.png)](https://www.youtube.com/watch?v=4C2w8eIG48A&feature=youtu.be)

> **Why this is different from other scaffolds.** Most folder structures are someone's preference dressed up as a system. myPKA is the working slice of **ICOR**, a methodology Paperless Movement S.L. and thousands of professionals world wide have been running their own business on for years. Every folder, every routing decision, every specialist contract maps to a piece of that framework. The structure is not arbitrary. The reasoning is teachable. Both matter when you scale past the first week.

## Get going now

1. Clone or download the repo into a folder you'll actually use.
2. Open the folder in your LLM tool (Claude Code, Codex CLI, Gemini CLI, Cursor, or Obsidian + chat plugin).
3. Paste the contents of `initialize yourself in this folder` as your first message.
4. The LLM reads `ADAPTER-PROMPT.md`, writes a tool-specific pointer file (`CLAUDE.md`, `GEMINI.md`, etc.), and reports the team is online.
5. Ask "Who are you?" and you'll see Larry is at your service.

That's the whole setup. There is no install step.

Once you have the team online and start using it, you'll hit moments where you wonder why a folder is shaped the way it is. That's where the courses come in. They teach the WHY behind every folder choice, so you understand why the team is built like real humans operating on the **ICOR methodology**, not just another AI scaffold. More on that below.

## What you get

A working knowledge system, fully assembled, that does this on day one:

- **Organizes your life from a single daily journal.** You write what happened. The team files the people, projects, decisions, and ideas where they belong. Connections between notes are made for you.
- **Runs in any LLM you already use.** Claude Code (and Claude Cowork), Codex CLI, Gemini CLI, Cursor, ChatGPT, Obsidian with a chat plugin. The same scaffold, the same team, the same files. You change models. Your knowledge doesn't move.
- **Stays in plain markdown.** Every note is a `.md` file. You can read it without the AI. You can grep it. You can sync it with Dropbox or git. You can open it in Obsidian and keep working with no AI at all.
- **Upgrades to SQLite when you outgrow plain files.** Once the vault gets large, paste the prompt at `Team Knowledge/SOPs/SOP-002-convert-vault-to-sqlite.md` into your LLM. Markdown stays canonical. SQLite becomes a fast lookup layer on top.

There is no lock-in. The whole system is text on your disk. It works in Obsidian today. It upgrades to SQLite when you want it. It runs on whichever model or LLM you prefer, and it keeps running when you switch.

## Who this is for

- **Knowledge workers** who want a local folder setup instead of handing over their knowledge to Notion, Tana etc. and want an AI team that actually files things. Transparent and accessible.
- **Founders and operators** running multiple projects who need a knowledge system that thinks across People, Topics, Goals, Habits, and Key Elements without manual cross-linking.
- **Parents and generalists** with too many inputs (school stuff, health stuff, ideas, contacts) and no structure to hold it.
- **AI tinkerers** who want a real reference architecture for a multi-agent setup, not a toy demo.

If you've ever opened a blank Obsidian vault and didn't know where to put anything, this is for you.

## Meet the team

Four specialists ship pre-loaded. **You only ever talk to Larry.** Larry routes.

<table>
<tr>
<td width="140" align="center"><img src="assets/team/larry.png" width="120" alt="Larry the Red Fox - Team Leader and Orchestrator" /></td>
<td><b>Larry - Team Leader & Orchestrator</b><br/><i>A Red Fox. Sharp ears, sharper instincts.</i><br/><br/>Every request you make lands with Larry first. He clarifies, picks the right specialist, hands off the brief, and synthesizes the answer back to you. He's also the team's <b>Librarian</b> (keeps the wiki clean, fixes broken <code>[[wikilinks]]</code>, enforces the SSOT Golden Rule) and <b>Session-Log Author</b> (writes a daily log of what the team did and what changed). Larry never executes specialist work himself - that's the iron rule.</td>
</tr>
<tr>
<td width="140" align="center"><img src="assets/team/nolan.png" width="120" alt="Nolan the Pitbull - Talent Acquisition" /></td>
<td><b>Nolan - Talent Acquisition</b><br/><i>A Pitbull in glasses. Loyal, methodical, allergic to lazy hires.</i><br/><br/>When you outgrow the four shipped specialists, Nolan handles the hire end-to-end: briefs Pax for research, drafts the new specialist's contract (<code>AGENTS.md</code>), validates against the SOP, and gets your sign-off before adding anyone to the roster. Nolan is the reason your team scales without diluting.</td>
</tr>
<tr>
<td width="140" align="center"><img src="assets/team/pax.png" width="120" alt="Pax the Raven - Deep Research" /></td>
<td><b>Pax - Deep Research</b><br/><i>A Raven. Patient, source-cited, allergic to a single-source answer.</i><br/><br/>When something matters - a hire, a market read, a "is this actually true" - Pax goes wide before going deep. Returns a triangulated brief in <code>Deliverables/</code>, never a one-shot opinion.</td>
</tr>
</table>

**Penn - Journal Writer.** The team's scribe. Drop screenshots, voice memos, business cards, or rough thoughts into `Team Inbox/`. Penn files everything into the right corner of `PKM/` with the right `[[wikilinks]]`.

Each specialist has a contract at `Team/<Name> - <Role>/AGENTS.md`. Full routing table at `Team/agent-index.md`.

> The full Paperless Movement team - including the AI specialists you can add via the **AI Library** - is at [myicor.com](https://myicor.com).

## What lives where

- `PKM/` is your knowledge. `My Life/` holds the five life concepts (Goals, Habits, Topics, Projects, Key Elements). `Documents/`, `CRM/`, `Images/`, and `Journal/` sit alongside it. Notes connect through `[[wikilinks]]`, not nested folders.
- `Team/` holds your specialists. One folder per agent. Each has its own `AGENTS.md`.
- `Team Knowledge/` holds the team's playbook. SOPs are atomic procedures. Workstreams orchestrate multi-agent flows. Guidelines are static reference info.
- `Deliverables/` is where the team puts work-in-progress and finished artifacts - research briefs, hire workups, multi-file projects. Time-stamped, ephemeral, the team's working surface. **Pax** drops research here. **Nolan** drops hire workups here. **Larry** collects multi-specialist work here.
- `Team Inbox/` is your drop zone for raw inputs. Drop screenshots, voice memos, business cards, links, or a quick braindump and the team files them into PKM. *"I have something, not sure where"* goes here. **Penn** usually picks it up, **Larry** routes it.
- `AGENTS.md` at the root is the source of truth for how the whole team behaves.

## Coming from another tool?

- **Obsidian users**: open the folder as a vault. Wikilinks, tags, and Markdown work as you expect. The scaffold adds an AI team on top of the vault you already understand.
- **Notion users**: the closest analogue is "Pages with AI inside, but the pages are files on your disk." You lose Notion's database views. You gain ownership of every byte and the ability to swap LLMs without migrating.
- **Roam / Logseq users**: same daily-note instinct. The team handles the cross-linking you used to do by hand.

## The deeper story: ICOR methodology

If you want to really manage your life efficiently and run this folder structure the way it is meant to work, the methodology is the missing layer.

myPKA is built on the **My Life** part of the **ICOR methodology**. ICOR is tool-agnostic Paperless Movement S.L. and thousands of professionals use to run both personal life and business: five life concepts on one side, five business concepts on the other, with a shared way of capturing, processing, and acting on information. We have been running on it for years. The scaffold you just downloaded is one slice of that framework, made operational.

Watch the deep-dive walkthrough where Tom builds the system from scratch and explains the reasoning behind each folder, each agent, and each routing rule:

**[Watch the deep-dive on YouTube](https://www.youtube.com/watch?v=4C2w8eIG48A&feature=youtu.be)**

The full courses live at **[myicor.com](https://myicor.com)**. They cover:

- **The Personal half (myPKA)**: the WHY behind every folder in this scaffold, how the five life concepts (Goals, Habits, Topics, Projects, Key Elements) connect, and how to operate the team so it actually saves you time instead of becoming another tool to manage.
- **The Business half**: the same framework extended to companies, including the operating system Paperless Movement S.L. runs on internally.

The scaffold works on its own. The course is for people who want to understand why it works, so they can extend it without breaking the model.

## AI Library (membership)

Once you've used myPKA for a while, you'll want more than four specialists. The **AI Library** at [myicor.com](https://myicor.com) is the membership layer. These extensions are not in this repo and are not planned to be open-sourced:

- **Slack integration** so the team can read and act on conversations from your workspace.
- **Obsidian optimizations** including templates, plugins, and views tuned to the scaffold.
- **Prebuilt specialists** that drop into the `Team/` folder: a Frontend Developer, a Marketing Lead, a Customer Support Manager, a Bookkeeper, and others.
- **Workstream packs** for hiring, launches, weekly planning, and yearly reviews.
- **Office hours and walkthroughs** with the team that builds this scaffold.

Membership-only is honest, not a gate. The scaffold here is genuinely complete. The AI Library is for people running serious work on top of it.

## License and trademarks

- **Content and code**: [CC BY-NC-SA 4.0](LICENSE). Free for personal and non-commercial use, with attribution and share-alike.
- **Registered trademarks (US)**:
  - PAPERLESS MOVEMENT - USPTO Reg. No. 6,689,873
  - ICOR - USPTO Reg. Nos. 6,607,819 and 6,608,200
- **Common-law marks**: myICOR, myPKA
- See [NOTICE.md](NOTICE.md) for trademark usage guidelines.
- Commercial licensing: support@myicor.com

## Disclaimer

The myPKA scaffold is a teaching artifact, not a production system. It is provided **as is**, without warranty of any kind, express or implied. The authors and copyright holders make no guarantees about fitness for a particular purpose, the behaviour of any LLM you point at the folder, the safety of any AI agent's reads or writes, or the integrity of your data over time.

You are responsible for your own backups, your own data hygiene, your own choice of LLM tools and what you allow them to access on your machine. We are not liable for data loss, business interruption, or any other damages arising from use of this scaffold or its examples. **Use at your own risk.**

See [LICENSE](LICENSE) for the full disclaimer of warranties and limitation of liability.

## Built by

myPKA is built by **Dr. Thomas Rödl** and **Paco Cantero** at **Paperless Movement S.L.**, the company behind myICOR and the ICOR methodology. We use this scaffold every day. The version you're looking at is the version we run.

If it helps you, the best thank-you is to come learn the methodology at [myicor.com](https://myicor.com).
