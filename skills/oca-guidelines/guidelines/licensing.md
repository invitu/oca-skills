# Licenses

Source: the `.pylintrc` of the target repository, read at task time. The
minimum-license table is a rule of these skills.

## Allowed licenses

Those listed in `license-allowed` in the target repository's `.pylintrc` (or
`.pylintrc-mandatory`). Read it, do not assume it. A proprietary license
(OPL-1, OEEL-1) is never allowed.

New module: the agent lists the possible licenses (allowed by the
repository and compatible with the minimum license below) with the reason
for each, and recommends one (AGPL-3 is the usual default). The human
validator chooses, on the line `License chosen:` of `architecture_*.md`. An
agent never chooses a license.
Existing module: the license does not change.

## Minimum license

A module's minimum license comes from its dependencies, direct and
transitive. Keep the conservative choice below; the legal minimum is
"TO CONFIRM", never decided by an agent.

| License of a dependency | Effect on the module |
|---|---|
| AGPL-3 | AGPL-3 |
| GPL-3, GPL-2 or any later version | AGPL-3: compatible with GPL-3 (section 13 of both licenses) |
| GPL-2 without "or later" | not compatible with AGPL-3: report it, do not decide |
| LGPL-3 | nothing on its own |
| unknown (external dependency) | minimum undetermined: report it, do not assume |

AGPL-3 is the OCA default and by far the most common license, LGPL-3 the
usual exception, GPL-3 is allowed but rare. Check the repository's
`license-allowed`.

## Dependencies

A module never depends on a private or non-OCA module.

## Existing module: forbidden

- Modifying `version` in `__manifest__.py`
- Modifying `README.rst`, `static/description/index.html`, `pyproject.toml`,
  `i18n/*.po`
- Bumping, refactoring or "improving" beyond the exact scope of the task

**Allowed**: the `readme/` fragments (`readme.md`) and the images they
reference in `static/description/`, code in `models/`, `views/`, `data/`,
`demo/`, `tests/`.

These prohibitions do not apply to a new module meant for OCA, which still
follows the OCA structure (complete manifest, `readme/`).
