# Migration between series

Part of `references.md`.

Migration documents (see the wiki above) exist per pair of consecutive series. A migration over
several series is done one step at a time, reading the documents of each
step.

| Subject | Document |
|---|---|
| OCA migration guide for a target series (from the wiki index) | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-<series> |
| Modules missing from a migration issue | https://github.com/OCA/maintainer-tools/wiki/%5BFAQ%5D-Missing-modules-in-migration-issue-list |
| Migration issue of a repository | issue "Migration to version <series>" in the repository |
| Automatic code transformation | https://github.com/OCA/odoo-module-migrator |
| Migration of the git history, port of missing commits | https://github.com/OCA/oca-port |
| OpenUpgrade repository | https://github.com/OCA/OpenUpgrade |
| OpenUpgrade documentation: data model changes between two series, module coverage (one page per pair of series) | https://oca.github.io/OpenUpgrade/ |
| Migration scripts and analysis of a module (series 14.0 and later) | https://github.com/OCA/OpenUpgrade/tree/<target series>/openupgrade_scripts/scripts/<module>/ |
| Analysis of a custom set of modules between two series | https://github.com/OCA/server-tools/tree/<series>/upgrade_analysis |

`oca-port` and `odoo-module-migrator` are run by a human, with a fork and
possibly a GitHub token. The skills read their documentation and the OCA
guide; they do not run them unless the task says so.
