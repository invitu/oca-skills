# Commits

Source: `contributing-commit-message`, `ai-policy`, `odoo-git-guidelines`
(`sources.json`).

## Header

`[TAG] <module>: <summary>`

- Several modules: `[FIX] module_a, module_b: ...`. Avoid commits that touch
  many modules; split by module so each can be reverted alone.
- Summary: imperative present (`Fix`, `Remove`, not `Fixes`), English, no
  final period, about 50 characters. A header that is too long appears
  truncated with `[...]` in the pull request.
- Never a summary like `bugfix` or `improvements`.

## Tags

| Tag | Use |
|---|---|
| `[FIX]` | bug fix |
| `[IMP]` | non-blocking improvement |
| `[ADD]` | new module |
| `[MIG]` | migration of a module to another series |
| `[REF]` | refactoring |
| `[REM]` | removal |
| `[PERF]` | performance |
| `[REV]` | revert |

Other tags follow the Odoo git guidelines of the series.

## Body

A blank line after the header, then lines of 80 characters at most:
- the problem, or the need;
- how the change addresses it;
- the tests added.

Short, without storytelling. No mention of a review, a spec or a
conversation.

## Trailer

`Assisted-by: <model name>` (OCA AI policy, current version:
https://github.com/OCA/.github/blob/master/AI_POLICY.md), one line per
agent or model, no blank line between them, also shown in the pull request
description. Never `Co-authored-by`, never added to a CONTRIBUTORS file.

## Granularity

- One commit per logical change. No `Fix pep8`, `Code review` or `Add
  unittest` commit for a commit being proposed: amend it.
- The title of a pull request follows the same rules as the header.
