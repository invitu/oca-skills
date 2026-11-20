# Learning the conventions in practice

Part of `references.md`.

Written guidelines do not cover everything. When the point at hand is not
covered, learn from the target repository itself, not from a list of
people: who shapes a repository changes, its code and its reviews are
verifiable.

1. Pick two or three modules of the repository that solve a comparable
   problem (search by model, `_inherit` or name).
2. Find who shaped them: the `maintainers` key of the manifest, and the most
   frequent authors of the module in its git history:

   ```bash
   git log --format='%an' -- <module> | sort | uniq -c | sort -rn | head -5
   ```

   Without a clone, use the commits of the module path through the GitHub
   API.
3. Read two or three recent merged pull requests on comparable modules,
   preferably those with many review comments: the reviews
   (`pulls/<number>/reviews`) and comments (`pulls/<number>/comments`) show
   what reviewers require. Search first, then read only those.
4. Read the `.pre-commit-config.yaml` and `.pylintrc` of the repository.
5. Apply the patterns found. Where they conflict with a guideline, the
   guideline and the official documents win: report the difference.

Do this once per task, only for a point the guidelines do not cover. Report
the modules and pull requests read (paths and numbers, not people).
