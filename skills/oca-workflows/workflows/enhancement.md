# Enhancement of an existing module

A change requested on an existing OCA module, not a bug.

Same steps as `bug-fix.md`, with these differences:

- step 1 starts from the improvement request instead of a bug report: the
  "use cases" are the new behavior and the existing behavior that must not
  change;
- the module already exists, so the forbidden-file rules of
  `oca-guidelines` apply;
- the commit subject at step 9 is `[IMP] <module>: ...`;
- if the change alters what a user sees or configures, add a `readme.md`
  workflow on the affected fragments before the review (step 9).

If the request needs several modules, use `multi-module-project.md`.
