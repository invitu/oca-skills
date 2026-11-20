# __manifest__.py

Source: to confirm (not yet in `sources.json`).

## Existing module
- `version`: never modified
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
