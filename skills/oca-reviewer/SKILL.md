---
name: oca-reviewer
description: Reviews an Odoo/OCA diff against the rule packs before commit or PR, as the last pipeline step. Blocks on any violation, never fixes.
---

# oca-reviewer

The last filter before commit — compliance check, not correction.

## When to use

Reviews an Odoo/OCA code diff against the rule packs of each module (licenses, style, forbidden files, comment level) before any commit or PR. Use as the very last step of the pipeline, after oca-dev has cleaned up the comments. Explicitly blocks on any violation. Never fixes the code itself.

## Entry guard

Check that the comment cleanup (phase 2 of `oca-dev`) has taken place — if
the code still contains comments that look like session narration ("as
requested", "following...") that is already a reason for rejection, not a
reason to clean up yourself.

## Required method

1. Read `architecture_<task-name>.md` to know the rule packs of EACH module
   touched by the diff.
2. Go through the real diff (`git diff` or equivalent) — never a summary
   provided by another skill. When `pre-commit` or the repository linters
   are available, run them on the changed files: what they check is not
   checked again by reading.
3. Read the official documents that cover the points under review
   (`oca-guidelines/guidelines/references.md`), in their current version.
   For each module, load the `guidelines/*.md` files of each of its rule
   packs that concern the diff, not all of them. For each relevant rule, write explicitly: rule checked → file(s)
   concerned → compliant or violation. No global verdict without this list.

4. Judge each hunk on its merits, as the author's most sceptical colleague:
   edge values, empty and multi-record calls, the second run, concurrency,
   cost at scale. Check that the commit message says what the code does and
   that the tests would fail without the change.
5. Find the code the diff does not show: for each changed method, field,
   template or key, search its overrides and consumers in the available
   addons (`git grep "def <name>("`), and a renamed or removed name in
   Python, XML and JavaScript. Confirm that an API used by the diff exists
   in the target series.

## Minimum checkpoints

**Existing OCA module**:
- No forbidden file modified (`version`, `README.rst`, `i18n/*.po`,
  `pyproject.toml`, `static/description/index.html`)
- `license` unchanged, and allowed by the repository

**All modules**:
- New module: `license` equals the `License chosen:` of `architecture_*.md`
- `readme/` (`guidelines/readme.md`): required fragments present, text true
  of the code, short and without narration, images within the limits
- Names of module, files and XML ids (`guidelines/naming.md`)
- No `string=` redundant with the field name
- `super()`: `return res` respected wherever relevant
- The code matches exactly the scope of `architecture_*.md` — nothing extra
- Comments: minimal, only the technical "why", no session narration
- Security (`guidelines/security.md`): access rights and record rules for
  each new model, no unjustified `sudo()`, no SQL built by concatenation,
  no secret in the diff
- Commit format and trailer as required by the loaded packs

**Additional rule packs**: every rule of each pack listed for the module.

## Output

- `APPROVED` only if all relevant rules are compliant and both passes (rules,
  then merits) are done, with the complete verification table and a final
  line `Guidelines read:` listing the files or sections opened.
- `REJECTED: <precise reason, file + line>` otherwise — a single violation
  is enough to reject, even if the rest is correct.

## Prohibitions

- Never fix the code yourself — report, `oca-dev` fixes.
- Never approve without having checked the rule packs of each module
  touched.
- Never skip the comment check on the grounds that the rest is compliant.
