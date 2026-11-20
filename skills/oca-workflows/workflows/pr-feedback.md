# Answer the reviews received on your own pull request

**Input**: `OCA/<repo>` and the number of your pull request. Task name:
`<repo>-pr-<number>-feedback`.

| # | Role | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | feedback analysis (role to write) | reviews and comments, the diff, real code | `feedback_*.md` | one line per remark: change to make, or reason to decline, with evidence |
| 2 | human | `feedback_*.md` | status, replies posted | |
| 3 | `oca-dev` | validated `feedback_*.md` | code | only the accepted changes |
| 4 | `oca-validator`, then `oca-tests` | feedback file, code | validation, results | loop to 3 on failure |
| 5 | `oca-security-audit` | feedback file, diff | `audit_security_*.md` | independent; on the changed code only |
| 6 | `oca-reviewer` | diff | verdict | independent |
| 7 | human | verdict | push, replies | |
