---
name: oca-project-map
description: Generates and updates the map of a multi-module Odoo/OCA project from real manifests and code: dependencies, series, models, license alerts.
---

# oca-project-map

An overview of all the modules of a project, verifiable in the code. Other
roles read it instead of re-reading every manifest.

## When to use

Generates and updates the map of a multi-module Odoo/OCA project (modules, repositories, dependencies, models, license alerts, series, modules to migrate) from the real manifests and code. Use from the parent folder of the project, at the start of a multi-module project, before a multi-module migration, and after a module is merged. Never writes code, never modifies a module, never chooses a license.

## Role and limits

Writes only `docs/map.proposed.md`. Never modifies `docs/map.md` (a human
replaces it after review), a module, or a source document in `docs/`. Never
executes module code.

## Entry guard (blocking)

- The working folder contains `docs/` and the project's repositories. In a
  task folder (one target repository and a `deps/` folder), stop: the map is
  updated from the parent folder.
- The target series is given. If it is not, ask. Never guess it.

## Method

1. Run the inventory, which reads every manifest once:

```bash
python3 -I <skill folder>/scripts/extract_modules.py --target <series> [--external-licenses docs/external_licenses.json] <repo1> <repo2> ...
```

   `docs/external_licenses.json` (written by a human, optional) gives the
   license of dependencies outside the project:
   `{"base": "LGPL-3", "sale": {"license": "LGPL-3", "depends": ["base"]}}`.
   Without it, each such dependency is reported `UNKNOWN_EXTERNAL_LICENSE`.
   The output is compact. `--full` gives every field, indented, only if a
   field you need is missing.
2. Build the map from the JSON only. Do not re-read the manifests, and add no
   information that is not in the JSON or in a cited file. One column per
   module field, one line per alert. Fields added by another skill that
   post-processed the JSON are shown the same way. If `errors` is not
   empty, copy them under "TO CONFIRM".
3. Read `oca-guidelines/guidelines/licensing.md` only if an alert needs it.
4. **Series**: if the target series is no longer maintained by Odoo, add the
   warning described in `oca-guidelines/guidelines/references-series.md`; the task continues.
5. **Modules to migrate** (`version_state` = `to_migrate`) whose repository is
   an OCA repository: check once whether the module already exists in the
   target series, with
   `https://raw.githubusercontent.com/OCA/<repo>/refs/heads/<series>/<module>/__manifest__.py`.
   Write "available in <series> at OCA" or "absent from <series>". Check
   impossible: "TO CONFIRM". `migration_order` gives the levels: level 0 is
   migrated first.
6. **Linked features**: if `docs/` holds feature tables (CSV or Markdown),
   link each row to a module, citing the row or the code file. No evidence:
   "TO CONFIRM". Reference lists are not reproduced.
7. **Licenses**: show `minimum_license` and `license_options` for each
   module. `license_options` lists the licenses the repository allows and
   that respect the minimum; it is a list for a human to choose from, not a
   choice. `null` means the repository list or the minimum is unknown: write
   "TO CONFIRM".

## Alerts

| Alert | Meaning |
|---|---|
| `LICENSE_NOT_ALLOWED` | declared license is not in the repository's `license-allowed` |
| `INSUFFICIENT_LICENSE` | declared license is less strict than the minimum license |
| `TO_CONFIRM_GPL2_ONLY` | a dependency is GPL-2 without "or later": report, do not decide |
| `TO_CONFIRM_OPEN_DEPENDS_ON_PROPRIETARY` | an open module depends on a proprietary one |
| `UNKNOWN_EXTERNAL_LICENSE` | list the modules concerned and propose the JSON to complete |
| `OCA_DEPENDS_ON_NON_OCA` | a module of an OCA repository depends on a project module of a non-OCA repository |
| `MISSING_LICENSE`, `UNKNOWN_LICENSE`, `UNKNOWN_VERSION` | missing or unreadable data: a human arbitrates |
| `DEPENDENCY_CYCLE` | cycle in the project graph |
| `UP_TO_DATE_DEPENDS_ON_MODULE_TO_MIGRATE` | a module on the target series depends on a module to migrate |

Never decide a question of legal compatibility.

## Update after a merged module

Rerun the inventory, compare with `docs/map.md`, and write
`docs/map.proposed.md`: added modules marked "added", modified rows listed
under "Changes".

## Format of `docs/map.proposed.md`

- Target series, with the series warning if any.
- Modules table: module, repository, series, version state, declared
  license, minimum license, license options, project dependencies, external
  dependencies, models created, models extended, linked features, state
  (`existing` or `added`).
- Migration order, by levels.
- Dependency graph in Mermaid (`graph LR`), project dependencies only,
  modules to migrate flagged with a class.
- Alerts.
- TO CONFIRM.
- `STATUS: PENDING VALIDATION` (last line, mandatory).

## Prohibitions

- Never modify `docs/map.md`, a module or a source document.
- Never write a dependency, a model or a link that does not come from the
  script or from a cited file.
- Never choose a license, never decide legal compatibility.
- Never set the status to `VALIDATED`: only a human does.
