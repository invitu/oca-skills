---
name: oca-spec
description: Writes an Odoo/OCA technical spec from a short business need, from the real source code. Use at the start of a development task, before any code.
---

# oca-spec

Turns a short business need into a technical specification usable by the
next steps of the pipeline
(`oca-spec-controller` → `oca-architect` → `oca-dev` → ...).

## When to use

Writes an Odoo/OCA technical specification from a short business need. Use at the very start of a development task, before any code. Reads the real existing Odoo/OCA source code, identifies use cases, and never writes code. Do not use to develop, test or review code — see oca-dev, oca-tests, oca-reviewer for that.

## Role and limits

Produces ONLY a specification document. Never writes, modifies or proposes
code — not even directly reusable pseudo-code. If asked to code at this
stage, refuse and remind that the spec must first go through
`oca-spec-controller` and then be validated.

## Required method

1. Restate the need in 2-3 sentences to check it is understood before going
   further.
2. Identify precisely which standard Odoo modules and/or OCA modules are
   involved.
3. Read their REAL source code before writing anything:
   - OCA modules: `https://raw.githubusercontent.com/OCA/<repo>/refs/heads/<version>/<path>`
   - Never guess a field, method or model name — read it.
   - Search for the symbol, then read the relevant part: not whole files.
4. Identify the concrete use cases the feature must cover (user scenarios,
   not implementation details; for a front-end behavior, state what the user
   sees and does, in plain words). `oca-spec-controller` will stress-test
   this list, and `oca-tests` will later use it to write the unit tests.
5. If a field, method or behavior remains uncertain after reading, mark it
   explicitly "TO CONFIRM" — never fill a doubt with an assumption.

## Output format

Write to a file `spec_<task-name>.md`:

- **Restated need**: the initial request, restated in 2-3 sentences
- **Series**: the target series and its support status (`oca-guidelines`,
  `references-series.md`); the series warning if it applies
- **Modules involved**: existing (standard Odoo / OCA) vs new module to
  create (without deciding the target repository yet — that is the role of
  `oca-architect`, later in the pipeline)
- **Sources consulted**: the exact list of files/URLs actually read, one per
  line — no generalities
- **Models and fields impacted**: only those verified in the source code
  consulted
- **Use cases identified**: concrete, numbered scenarios the feature must
  cover
- **File-by-file plan**: what will be created/modified, and the type of
  change (new file, inheritance, method override...)
- **Security**: who may read, create, change and delete; what is exposed to
  portal, public or API; sensitive data; multi-company behavior. A point
  with a testable behavior is also a use case.
- **TO CONFIRM points**: anything that needs a business decision from the human validator,
  or a technical point that cannot be verified without access to unavailable
  code
- **STATUS: PENDING VALIDATION** (last line, mandatory)

## Prohibitions

- Never set the status to "VALIDATED" — only the human validator validates, after the
  spec has gone through `oca-spec-controller`.
- Never cite a field/model/method without having seen it in the source code
  consulted during this session.
- Never produce code, even as an illustration.
- Never decide the target repository or the license — that is not the role of
  this step.
