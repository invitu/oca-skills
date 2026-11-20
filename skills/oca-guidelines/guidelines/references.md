# Official references

The files of this skill summarize rules. The documents below are the source
and prevail over them. They change, and many differ from one Odoo series to
another. Consult one only when the point at hand needs it and the summary
does not settle it, for the series of the target repository, and read only
the part that covers it. Do not read it again within the same task. `<series>` stands for that series
(for example the branch name of the repository).

## Reference for migrations and conventions

https://github.com/OCA/maintainer-tools/wiki

Start from this wiki for any migration and for any OCA convention. Its index
leads to the page of each series and to the other documents. The documents
listed below are the ones known to hang from it or to complete it.

## General

| Subject | Document |
|---|---|
| AI policy (disclosure, `Assisted-by:` trailer) | https://github.com/OCA/.github/blob/master/AI_POLICY.md |
| OCA contribution guidelines | https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst |
| Code of conduct and organization-wide files | https://github.com/OCA/.github/tree/master |
| Odoo coding guidelines | https://www.odoo.com/documentation/<series>/contributing/development/coding_guidelines.html |
| Repository template (CI, pre-commit, `.pylintrc`) | https://github.com/OCA/oca-addons-repo-template |
| Odoo security (access rights, record rules, pitfalls) | https://www.odoo.com/documentation/<series>/developer/reference/backend/security.html |
| Allowed licenses, valid series | `.pylintrc` or `.pylintrc-mandatory` of the target repository |

## By topic

| Topic | File |
|---|---|
| Series maintained by Odoo, series warning, Odoo's own skills | `references-series.md` |
| Migration between series (OCA guides, OpenUpgrade, tools) | `references-migration.md` |
| Learning the conventions of a repository in practice | `references-conventions.md` |
| Checking that a guideline is current, reporting a broken source | `source-check.md` |

## Reading a source file

To read a file of a GitHub repository without the web interface, use
`https://raw.githubusercontent.com/<owner>/<repo>/refs/heads/<branch>/<path>`.

## Rules

- For a commit message, a license, a manifest, a migration, a security
  point or a pull request, consult the document above that covers it, once
  per task.
- Read it for the series of the target repository. If no page exists for
  that series, read the one of the closest series and mark the point
  "TO CONFIRM".
- If a local file and a document disagree, the document wins. Report the
  difference in your output so that the local file can be corrected.
- If a document cannot be read, say so, apply the local file and mark the
  point "TO CONFIRM".
