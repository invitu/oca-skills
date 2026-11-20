# Is the guideline current

Part of `references.md`. The short version is in `efficiency.md`.

A guideline with a `Source:` line summarizes an official document listed in
`sources.json`. At its first loading in a task, run (the `--series` option
only when a source depends on the series):

```bash
python3 -I <skill folder>/scripts/check_sources.py --series <series> <guideline> [<guideline> ...]
```

with the guidelines loaded for this task, no others. A source checked less
than 7 days ago is not downloaded again. The output lists only the entries
that need a decision, with a count of the others (`--verbose` lists all of
them). Per entry:

| State | What to do |
|---|---|
| `OK`, `POINTER`, `NEEDS_SERIES` | continue with the guideline; read a `POINTER` page only if the task is about its subject |
| `CHANGED` | read the `extract` given, apply the source, write the difference in the output |
| `NOT_FOUND`, `SECTION_NOT_FOUND` | the source moved or disappeared: continue with the guideline, say "source not verified", and offer the issue below at the end of the task |
| `UNREACHABLE` | continue with the guideline, say "source not verified" |

A missing source never stops the task. Never rewrite a guideline yourself.

**Reporting a broken source.** The script logs it. At the end of the task:
1. Run `check_sources.py --issue-text`. It prints the repository, the title
   and the text of the issue, already written. Show them to the human and ask
   whether to open it.
2. Only if the human says yes, run
   `check_sources.py --open-issue --confirmed`. It looks for an identical open
   issue first, and creates the issue with `gh` otherwise.
3. If it fails (no `gh`, not signed in, no rights, no `issues_repo` in
   `sources.json`), give the human the text and the link printed by the
   script, to create the issue by hand.
4. If the human says no, do nothing more. The problem stays in the log.
Maintainers: `check_sources.py --report` lists the broken sources logged,
`--all` checks the whole registry (no model needed, suited to a periodic job),
and `--accept <id>` records the new fingerprint once the guideline has been
reviewed.
