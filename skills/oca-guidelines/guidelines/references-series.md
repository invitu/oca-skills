# Series

Part of `references.md`.

OCA does not limit the series it works on: any series can be the target.
The series is stated in the task. When it is no longer maintained by Odoo,
warn, and continue.

| Subject | Document |
|---|---|
| Series maintained by Odoo and their end-of-support dates | https://www.odoo.com/documentation/<latest series>/administration/supported_versions.html |
| Latest series | the highest `<n>.0` branch of https://github.com/odoo/odoo |

Odoo supports the 3 last major series. If the target series is older than
those, or its end-of-support date has passed, write a "Series warning" in
the spec (or the first output of the task) with these points, in a few
lines:

- Odoo no longer maintains this series: no fixes, including security fixes.
- Work on it usually costs more tokens: fewer matching examples and tools,
  more verification of what exists.
- Migrating to a maintained series is worth considering.

The warning is informative: it never blocks the task.

## Odoo's own skills

Odoo ships agent skills in `skills/` of its source tree, from series 20.0
(https://github.com/odoo/odoo/tree/<series>/skills). They are house rules
written for the series of their branch.

- OCA rules, the target repository's `.pylintrc` and pre-commit prevail.
- Read their task table, then only the section that matches the file you
  touch, and only when `oca-guidelines` does not settle the point.
- Check that a rule applies to the target series before using it.
