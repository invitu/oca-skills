# Bug fix

A bug reported in a GitHub issue of an OCA repository.

**Input**: `OCA/<repo>` and the issue number. Task name: `<repo>-issue-<number>`.

| # | Role | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | `oca-issue-fix` | the issue and its comments, real code | `spec_*.md`, `architecture_*.md`, `issue_comment_*.md` | stops if a pull request already exists |
| 2 | human | the three files | status, comment posted on the issue | |
| 3 | human | replies of other contributors | | if there are replies, run step 1 again |
| 4 | `oca-dev` (phase 1) | validated spec and architecture | code | |
| 5 | `oca-validator` | spec, code | `validation_*.md` | independent |
| 6 | `oca-tests` | spec, validation, code | regression test, results | loop to 4 on failure |
| 7 | `oca-security-audit` | spec, architecture, diff | `audit_security_*.md` | only if the diff contains a pattern of `oca-guidelines/guidelines/security-audit.md`, on the diff only; independent; loop to 4 on a blocking finding |
| 8 | `oca-dev` (phase 2), on request | code | cleaned comments | |
| 9 | `oca-reviewer` | architecture, diff | verdict | independent |
| 10 | human | verdict | commit `[FIX] <module>: ...`, push, pull request mentioning the issue | |

**Stop** when step 5, 6 or 7 still fails after 2 round trips.
