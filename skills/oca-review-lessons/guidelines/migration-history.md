# Migration and port history

Source: rule of these skills, from review evidence (`evidence.md`), applying
the OCA migration guides (`oca-guidelines/guidelines/references-migration.md`).

Reviewers reject a migration or a port without the module's commit history:
"commit history missing, use oca-port or follow [the migration guide]".

## Migration to the next series

- Use `oca-port` (https://github.com/OCA/oca-port), or the method of the
  migration guide of the target series: `git format-patch --keep-subject` of
  the module from the source branch, `git am -3 --keep`, then a
  `[IMP] <module>: pre-commit auto fixes` commit, then the work.
- Exactly one `[MIG] <module>: Migration to <series>` commit after the
  pre-commit one ("You should leave only 2 migration commits instead of 3").
- Pending fixes of the source branch go in before the migration commit
  ("Please include #<n> before migration commit").
- Only what the migration requires: "you are dirtying the migration commit
  with that changes that make the review harder". A refactoring is a separate
  `[REF]` commit or pull request, and keeps the original author's structure
  unless the author takes over maintenance.
- A renamed module has its path rewritten in the whole history
  (`git filter-repo --path-rename`), or the next migration loses it.
- Two modules merged into one: both histories, then one commit that moves
  them; their `.po` files merged (`pomerge`) so translations survive.
- Copyright years and original authors are not changed.

## Backports and forward-ports

- `git cherry-pick -x` keeps authorship and the reference; the commits of
  other people stay separate ("This commit was done by another person, so this
  would destroy attribution").
- One module per port pull request: "You shouldn't mix in one PR unrelated
  fw-ports of several modules."
- A backport of a module that exists only on a newer branch keeps that
  history too.
