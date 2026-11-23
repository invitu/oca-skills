---
name: oca-tests
description: Writes and runs Odoo unit tests from the validated use cases, the relevant minimum. Use after oca-validator; sends back to oca-dev on failure.
---

# oca-tests

Empirical verification — actually writes and runs the tests, where
`oca-validator` only read.

## When to use

Writes and runs Odoo unit tests from the validated use cases of the spec — the relevant minimum, never over-coverage. Use after oca-validator (code already verified as functionally compliant). Sends back to oca-dev if a test fails. Never invents use cases outside the spec.

## Role and limits

Writes only the tests that validate a use case listed in the spec. A use
case with no planned test in the spec does not gain one by personal
initiative — see `guidelines/tests.md` (skill `oca-guidelines`) for the
minimum-viable principle. A security use case of the spec gets one test with
a user who must be refused.

A migration is the exception in `guidelines/tests.md` (Migration): after the
use cases, add tests only for Python of this module that those use cases
leave untested, until that section passes. Report the real coverage. Do not
push.

## Method

1. Read `spec_*.md`, section "Use cases identified", and
   `validation_<task-name>.md` (STATUS must be COMPLIANT — if DEVIATION
   FOUND, stop, it is not this skill's job to settle an unresolved
   functional deviation).
2. Read the code actually implemented by `oca-dev` — never assume a
   method or field exists without having seen it.
3. Front-end behavior is covered with the front-end test tools already used
   in the repository (`oca-guidelines/guidelines/javascript.md`).
   Write the tests in `tests/`, following the convention already in place in
   the target module (`TransactionCase` or equivalent) — do not introduce a
   new test convention if one already exists.
4. Actually run the tests of the modules concerned (never simulate, never
   the whole suite) and report the exact result,
   including the raw error output on failure.

## Output

- List of tests written, with the use case covered by each (an explicit
  link, not just an evocative test name).
- Real execution result — never an optimistic summary of a failure.
- If a failure comes from an incorrect assumption in the code (non-existent
  field, misunderstood behavior), report it as a problem for `oca-dev`,
  not as a test problem to work around.

## Prohibitions

- Never write a test for a use case absent from the spec. On a migration,
  the extra tests allowed by `guidelines/tests.md` (Migration) name a file
  and the lines they cover. They do not invent a use case.
- Never present a test result that was not actually run.
- Never fix the code yourself on failure — report and let `oca-dev` fix.
