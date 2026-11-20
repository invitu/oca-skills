# Efficiency (tokens and energy)

Every token costs energy in a data center. Work with the least that gives a
correct result.

- Read only what the task needs: search first (list, grep), then read the
  relevant lines or files. Never read a whole repository, a whole file or a
  whole set of guidelines "to be safe".
- Do not read twice. What was read is recorded in the task files ("Sources
  consulted"): reuse it. Read again only a file that changed.
- Load a guideline file or an official document only when the point at hand
  is not already settled by what was read in this task, and read only the
  part that covers it.
- Prefer a deterministic tool to reasoning when it gives the same answer:
  `grep`, `pre-commit`, `pylint-odoo`, the project scripts. When available,
  run it instead of checking by reading.
- Run the narrowest check: the tests of the modules concerned, not the whole
  suite; the changed files, not the whole repository.
- Use a local copy of a source before the network.
- A guideline that has a `Source:` is a summary. At its first loading in the
  task, run `python3 -I <skill folder>/scripts/check_sources.py --series
  <series> <guidelines loaded>`, and only for those. Entries that are fine
  are not listed. `CHANGED`: read the `extract`, apply the source, write the
  difference. `NOT_FOUND`, `SECTION_NOT_FOUND`, `UNREACHABLE`: continue with
  the guideline and say "source not verified"; for the first two, offer the
  issue at the end of the task (`source-check.md`).
- Make independent calls in the same step.
- Write short outputs: lists and tables, no recap of the input, no narration
  of the steps, no content repeated between files.
- Stop at the first blocking problem and report it. Do not iterate beyond
  the round trips set by the workflow.
- Do not start a role whose input is not ready, and do not run a role whose
  result the task does not need.
