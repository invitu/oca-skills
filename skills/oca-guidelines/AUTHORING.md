# oca-guidelines — how this folder is organized

This folder centralizes the rules that `oca-dev`, `oca-validator` and
`oca-reviewer` must apply. It does not replace their judgment, it spares
them from guessing a rule instead of reading it.

## Rule packs

A rule pack is a guideline skill (a folder with a `SKILL.md` and a
`guidelines/` directory). `oca-guidelines` is the base pack. Another pack can
be listed after it in `architecture_<task-name>.md`: it adds rules, or
overrides a rule of the base pack by stating so explicitly. When two packs
disagree, the pack listed last wins.

## Two situations for a module

- **Existing OCA module** (contribution): the file non-modification rules
  (`version`, `README.rst`...) apply STRICTLY.
- **New module** meant to be pushed to OCA: these constraints do not apply
  until it is merged, but the OCA file structure is followed from the
  start.

A guideline that applies to both situations says so at the top of the file.

## Independence from the Odoo series

A guideline must be valid for every series. When a rule exists only from a
given series, or changes between series, the file says so at the top and
points to the official document. No example uses a fixed series where a
placeholder (`<series>`) works.

## When to create a dedicated file vs group

Follows the same principle that Odoo core adopted for its own guidelines
(`skills/odoo-web-guidelines/AUTHORING.md`, PR odoo/odoo#285015): a rule
small enough to fit in one sentence (e.g. "always `return res` after a
`super()` call") joins a file grouped by theme rather than having its own
file. A rule that needs examples, context, or covers an entire subject
(licenses, commit structure) deserves its own file.

## Current files

- `guidelines/efficiency.md` — token and energy economy
- `guidelines/security.md` — security by design
- `guidelines/security-audit.md` — patterns to sweep when auditing
- `guidelines/javascript.md` — front-end code under `static/`
- `guidelines/references.md` — index of the official documents and URLs
- `guidelines/references-series.md`, `references-migration.md`,
  `references-conventions.md` — the parts of the references read on demand
- `guidelines/source-check.md` — checking sources, reporting a broken one
- `guidelines/licensing.md` — allowed licenses, license computed from the
  dependencies, forbidden files
- `guidelines/manifest.md` — `__manifest__.py`: what can be modified
- `guidelines/naming.md` — module, file, Python and XML id names
- `guidelines/models-fields.md` — model/field code conventions
- `guidelines/tests.md` — the minimum-viable testing principle
- `guidelines/commits.md` — commit header, tags, body, trailers
- `guidelines/readme.md` — `readme/` fragments, style, images

## Sources of the guidelines

A guideline that summarizes an official document starts with a `Source:` line
naming entries of `sources.json`. Each entry gives the URL, the part used and
its fingerprint. A rule that is not from an official document is marked as a
rule of these skills. Write a guideline from the source, add its entries,
then run `scripts/check_sources.py --accept <id>` to record the fingerprints.
A guideline whose source is not yet registered says "Source: to confirm".

`issues_repo` in `sources.json` is the `<owner>/<repo>` where broken sources are
reported. Empty: the agent gives the text for a manual report.

## Skill descriptions

The `description` of a skill is loaded in every session: keep it to one or two
sentences (what it does, when to use it). The rest goes under "When to use"
in the body, which is read only when the skill is used.
