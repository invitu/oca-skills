# README improvement

Improve the `readme/` fragments of an existing module, without changing its
behavior.

**Input**: the module and what to improve (missing fragment, out-of-date
text, too long or unclear, missing screenshots).

| # | Role | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | `oca-readme` (analysis) | fragments, module code | `readme_plan_*.md` | one line per change, with evidence |
| 2 | human | plan | status of the plan | may remove changes and images |
| 3 | `oca-readme` (apply) | validated plan | fragments, images | only what the plan says |
| 4 | `oca-reviewer` | plan, diff | verdict | independent |
| 5 | human | verdict | commit, push, pull request | commit subject `[IMP] <module>: ...` |

Files that are never touched: see `oca-guidelines/guidelines/licensing.md`
(existing module). Images respect `oca-guidelines/guidelines/readme.md`.

**Stop** when step 4 still fails after 2 round trips.
