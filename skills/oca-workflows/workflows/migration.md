# Migration of a module to another Odoo series

**Input**: the module, its repository, the source series and the target
series. Task name: `<module>-migration-<target series>`.

| # | Step | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | availability check | the repository on the target series, the migration issue of the repository | result in the task folder | if the module already exists there, stop; if a pull request is open, report it |
| 2 | migration plan (role to write) | the documents of `oca-guidelines/guidelines/references-migration.md` for each step (OCA migration guide of the target series, OpenUpgrade analysis of the pair of series), the module code | plan | points to confirm marked "TO CONFIRM" |
| 3 | human | plan | status | |
| 4 | `oca-dev` | validated plan | code | commit `[MIG] <module>: Migration to <series>` |
| 5 | `oca-validator`, then `oca-tests` | plan, code | validation, results | loop to 4 on failure |
| 6 | `oca-reviewer` | diff | verdict | independent |
| 7 | human | verdict | push, pull request | |

Run `oca-security-audit` on the diff, before step 6, only if the diff
contains a pattern of `oca-guidelines/guidelines/security-audit.md` (see
`common.md`, Security).

The exact procedure is not restated here: read the documents listed under
`oca-guidelines/guidelines/references-migration.md`
before step 2.

## Over several series

Migrating from one series to a later one that is not the next (for example
from 17.0 to 20.0) is done as one migration per pair of consecutive series
(17.0 to 18.0, then 18.0 to 19.0, then 19.0 to 20.0). Each step has its own
plan, reading the documents of that pair, and its own commit.

## Several modules

Apply this workflow to each module, in the order of the dependency graph:
a module is migrated after the modules it depends on. The map from
`oca-project-map` (`multi-module-project.md`, step 0) gives that order.
Data model changes of
the pair of series that affect the project's modules are listed in the plan
of each module.
