# Unit tests

Source: to confirm (not yet in `sources.json`).

- The relevant minimum — one test per use case identified by
  `oca-spec-controller`, no coverage for coverage's sake.
- A use case with no planned test in the spec must not gain one by
  `oca-tests`' own initiative.
- `TransactionCase` (or the equivalent already used in the target module) —
  follow the convention already in place rather than introducing a new one.

## Migration

The three bullets above stay the rule for every task that is not a
migration.

The percentage below is a rule of these skills. It is not an OCA document:
the migration guides do not state a percentage. It is stricter than the
minimum-viable rule above.

Before a migration is handed back for push, all three pass on that module:

- `pre-commit` on the changed files
- the tests of the module
- Python coverage of the module above 99%

A module whose Python is only empty `__init__.py` files skips the
percentage and says why. `oca-tests` reports the real percentage. It does
not push. Use cases are still listed in the spec. Extra tests exist only
to cover Python of this module that those use cases leave untested, and
each one names the file and the lines.
