# github/ — repository presentation assets

These assets power the GitHub README, social cards, and the YouTube thumbnail
embedded at the top of the public README.

If you cloned this scaffold for personal use and don't plan to publish it back
to GitHub, you can safely delete this entire folder. The myPKA system itself
does not read or depend on anything in here. Larry, Penn, Pax, Nolan, Mack,
Silas, Charta, Pixel, and Iris never touch it.

## What lives here

- `team/` — portrait PNGs of the shipped specialists, used in the README's
  "Meet the team" table. Larry, Nolan, Pax, and Penn have portraits today;
  Mack, Silas, Charta, Pixel, and Iris portraits land in a later release.
- `youtube/` — thumbnail used as the clickable launch-video tile at the top of
  the README.

## Naming convention

`<context>/<slug>.<ext>` — flat inside each subfolder, kebab-case, no dates.
Replace files in place when refreshing them; the README references them by path.

## Why "github" and not "assets"

The folder name is the documentation. "github" tells future readers — and you
six months from now — that the contents are GitHub-meta, not part of the
scaffold's operating surface. Anything that powers the team or the user's
knowledge lives elsewhere.
