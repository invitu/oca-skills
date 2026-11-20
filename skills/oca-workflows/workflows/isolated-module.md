# Isolated module

A new module, standalone, in one repository.

**Input**: a business need, short.

| # | Role | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | `oca-spec` | the need, real source code | `spec_*.md` | |
| 2 | `oca-spec-controller` | the spec | `control_*.md` | independent |
| 3 | human | spec, control | status of the spec | back to 1 if sent back |
| 4 | `oca-architect` | validated spec | `architecture_*.md` | |
| 5 | human | architecture | status of the architecture | |
| 6 | `oca-dev` (phase 1) | both validated files | code | |
| 7 | `oca-validator` | spec, architecture, code | `validation_*.md` | independent |
| 8 | `oca-tests` | spec, validation, code | tests, results | loop to 6 on failure |
| 9 | `oca-security-audit` | spec, architecture, code | `audit_security_*.md` | independent; loop to 6 on a blocking finding |
| 10 | `oca-readme` | validated spec and architecture, code | `readme/` fragments, images | after the code is stable |
| 11 | human | code, readme | request to clean up | |
| 12 | `oca-dev` (phase 2) | code | cleaned comments | |
| 13 | `oca-reviewer` | architecture, diff | verdict | independent |
| 14 | human | verdict | commit, push, pull request | |

**Stop** when step 7, 8 or 9 still fails after 2 round trips.
