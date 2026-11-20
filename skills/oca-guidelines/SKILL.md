---
name: oca-guidelines
description: Reference of OCA code rules, licenses, security and conventions, consulted by the other oca-* roles before judging compliance. Never guess a rule.
---

# OCA Guidelines

This skill does nothing on its own: it is a reference consulted by the other
skills. Read `guidelines/efficiency.md` first (short, applies to every
role). Then load only the files whose "Read it when" matches the task, and
only the part you need. A guideline with a `Source:` is checked once per
task (`guidelines/efficiency.md`; details in `guidelines/source-check.md`).
`AUTHORING.md` explains how this reference is organized.

| File | Read it when |
|---|---|
| `guidelines/efficiency.md` | always, first |
| `guidelines/licensing.md` | choosing or checking a license, or touching an existing module's files |
| `guidelines/manifest.md` | creating or changing `__manifest__.py` |
| `guidelines/naming.md` | naming a module, a file, a model, a method or an XML id |
| `guidelines/models-fields.md` | writing or reviewing Python models and fields |
| `guidelines/security.md` | planning, writing or reviewing access rights, exposed routes, SQL, `sudo()` (design side) |
| `guidelines/security-audit.md` | auditing a finished module or diff (`oca-security-audit`, `oca-pr-review`, `oca-reviewer`) |
| `guidelines/javascript.md` | touching `static/src` or `static/tests` |
| `guidelines/tests.md` | planning or writing tests |
| `guidelines/commits.md` | writing a commit message or a pull request |
| `guidelines/readme.md` | writing, improving or reviewing the `readme/` fragments of a module |
| `guidelines/references.md` | a point is not settled by the files above: index of the official documents |
| `guidelines/references-series.md` | the target series, its support status, Odoo's own skills |
| `guidelines/references-migration.md` | migrating a module between series |
| `guidelines/references-conventions.md` | a convention the guidelines do not cover |
| `guidelines/source-check.md` | a source is `CHANGED`, `NOT_FOUND`, or an issue must be offered |

## When to use

Reference for OCA code rules, licenses, security and conventions for Odoo development. To be consulted by oca-dev, oca-validator, oca-reviewer, oca-security-audit and oca-pr-review before judging a module's compliance - never guess a rule, always read it here.
