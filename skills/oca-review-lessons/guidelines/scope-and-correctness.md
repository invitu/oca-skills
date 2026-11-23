# Scope, placement and correctness

Source: rule of these skills, from review evidence (`evidence.md`).

What reviewers check first, in this order. Each point is a blocking finding
for `oca-reviewer` and `oca-pr-review` when it applies.

## Placement

- Country-specific code goes to `l10n-<country>`, generic code does not ("As
  this seems applicable only on Germany, I think this should go to
  OCA/l10n-germany"); a feature goes where its base module lives.
- Behaviour not everyone wants goes into a separate, opt-in module rather than
  the base one ("It's very bloated"). A change of default behaviour for
  existing users needs an opt-in.
- Existing work first: another OCA module, an open pull request, the same fix
  on another branch ("I wonder why you didn't cherry-pick ...").
- Fewer fields, options and modules: "Can we avoid to add yet another field?"

## Root cause and evidence

- The fix addresses the cause, not the symptom: "This is not fixing the
  underlying issue." A problem caused by a wrong configuration is fixed in the
  configuration ("a liquidity account shouldn't be reconcilable").
- A claim the change rests on (an API limit, an error, a dependency version)
  comes with its evidence: "Can you put here the error you mention?"
- The commit message names every behaviour the commit changes: "This is
  changing more than what the message says."

## Correctness

- Posted documents do not change: a compute dependency on configuration
  rewrites history ("Imagine all the past invoices being changed").
- A write before a `raise` is rolled back.
- `self.env.company` (or better the record's company), never
  `self.env.user.company_id` for the current company.
- No arbitrary record to fill a missing value: "randomly assign one journal is
  not OK."
- The ORM tool of the series over tricks: computed writable fields instead of
  inverse/onchange hacks, `_rec_names_search`, `_for_xml_id`,
  `@api.ondelete(at_uninstall=False)`; checked in the target series.
- Onchange methods work in memory: assign, never `unlink()`.
- An override calls `super()` only for the records it does not handle
  (`self -= handled`), and has a docstring saying why it exists.
- Stored or not is decided and stated: storing costs writes and breaks
  multi-language display; not storing lets values on posted documents change.
- Narrow context keys (`mail_create_nosubscribe`, not `tracking_disable`) in
  business code.
- New private methods carry a module-specific name to avoid clashes.
- Minimal access rights (`1,1,1,0` when only sudo code deletes); no redundant
  lines for implied groups; no negative groups; a changed `noupdate` record
  rule needs a migration script.
- No external assets: libraries are vendored ("Systems may be isolated and
  don't access any external resource").
- On a released series: no renamed XML id, a renamed overridable method keeps
  its old name calling the new one, no change of `depends` or
  `external_dependencies`, no module split.

## Readability and documentation

- The why of anything surprising is commented ("your 'you' of 6 months in the
  future won't remember why you did these changes"); new overridable methods
  have a docstring.
- Translated strings: arguments inside the call
  (`self.env._("Text %s", value)` or `_()` per series), named placeholders, no
  f-string or `.format()` on the translated string.
- A behaviour change updates every `readme/` sentence it makes false.

## Process

- CI green before asking for review; a pull request with failing tests is a
  draft.
- One branch first; ports after review.
- Pre-commit differs from CI: the copier template of the repository is
  outdated; that is a separate pull request.
