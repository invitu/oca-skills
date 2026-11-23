# __manifest__.py

Source: to confirm for the rules below, except "Migration to another
series", which is `oca-migration-guide` in `sources.json`.

## Existing module
- `version`: not modified, except a migration to another series (below)
- `license`: never modified
- Other keys (`depends`, `data`, `assets`...): modifiable if the task
  justifies it
- README: do not edit `README.rst`, it is generated from `readme/*.md`

## New module
- `version` follows the OCA format `<series>.<major>.<minor>.<patch>` (for
  example `<series>.1.0.0`), where `<series>` is the target repository's branch
- `license`: the license chosen by the human validator in
  `architecture_*.md`, among those in the target repository's
  `license-allowed`
- `author` includes `'Odoo Community Association (OCA)'`

## Migration to another series

Source: `oca-migration-guide` (`sources.json`, pointer). The page depends
on the series, so it is not fingerprinted: a hash of one series would be
wrong for the next.

Set `version` to the string written in the OCA migration guide of the
target series (its tasks list). Read that page for the series of the task.
Do not reuse the string of another series. `license` still does not change.
