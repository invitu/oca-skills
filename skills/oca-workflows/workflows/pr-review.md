# Review of someone else's pull request

**Input**: `OCA/<repo>` and the pull request number. Task name:
`<repo>-pr-<number>`.

| # | Role | Reads | Writes | Notes |
|---|---|---|---|---|
| 1 | `oca-pr-review` | the pull request, its diff, its CI results, real code | `pr_review_*.md` | read-only, independent |
| 2 | human | the review | review posted on the pull request | the human decides to post it, edit it or drop it |

Nothing is modified on the pull request by the role.
