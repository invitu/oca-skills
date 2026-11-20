---
name: oca-workflows
description: Defines which roles take part in each type of OCA task, in which order and with which human validations. Use at the start of a task and between steps.
---

# oca-workflows

A workflow is a sequence of roles. Each role is a skill (`oca-spec`,
`oca-dev`, `oca-project-map`, `oca-security-audit`, ...). The workflows say who intervenes, in which order, what each
step reads and writes, and where a human validates.

Read `common.md` first (rules shared by all workflows), then the workflow
that matches the task:

| Task | Workflow |
|---|---|
| New module, standalone | `workflows/isolated-module.md` |
| New modules within a bigger project, or across several OCA repositories | `workflows/multi-module-project.md` |
| Bug reported in a GitHub issue | `workflows/bug-fix.md` |
| Improvement of an existing module | `workflows/enhancement.md` |
| Review of someone else's pull request | `workflows/pr-review.md` |
| Answer the reviews received on your own pull request | `workflows/pr-feedback.md` |
| Improve the README of an existing module | `workflows/readme.md` |
| Port a module to another Odoo series | `workflows/migration.md` |
| Study feasibility, without developing | `workflows/feasibility.md` |
| Evaluate a third-party module before adopting it | `workflows/module-evaluation.md` |
| Triage an issue as a maintainer | `workflows/issue-triage.md` |

A step marked "role to write" has no skill yet: do it by hand, or with your
own instructions, and keep the output files described.

## When to use

Defines which roles (oca-spec, oca-dev, oca-tests, ...) take part in each type of OCA task, in which order, with which human validations. Use at the start of a task to choose the workflow, and between steps to know what comes next. Describes the orchestration only; how it is executed (by hand, separate sessions, sub-agents) is up to each environment.
