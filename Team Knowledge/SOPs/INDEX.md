# SOPs - Index

Atomic step-by-step procedures. One job per file.

Filename pattern: `SOP-NNN-<title>.md`. See [[GL-001-file-naming-conventions]] for slug rules.

## Active SOPs

| SOP | Title | Owner | Description |
|---|---|---|---|
| SOP-001 | [[SOP-001-how-to-add-a-new-specialist]] | Nolan | Step-by-step procedure to draft and onboard a new team specialist. References [[GL-001-file-naming-conventions]]. |
| SOP-002 | [[SOP-002-convert-vault-to-sqlite]] | the user | Generate a SQLite mirror of the markdown vault on demand. Markdown stays canonical; SQLite is a derived performance layer. Body is a paste-into-LLM prompt. |

## How to add a new SOP

1. Pick the next unused number (`SOP-NNN`).
2. Filename: `SOP-NNN-<kebab-case-title>.md`.
3. Owner is the specialist who runs the procedure. Listed in the SOP's frontmatter.
4. Reference [[GL-001-file-naming-conventions]] and any other Guideline instead of duplicating its content.
5. Add a row to this index.
