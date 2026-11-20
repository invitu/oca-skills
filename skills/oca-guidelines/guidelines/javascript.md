# JavaScript, Owl and styles

Source: to confirm (not yet in `sources.json`).

Applies to files under `static/src` and `static/tests` of a module.

- Odoo publishes its front-end house rules; they are written for the series
  of their branch (the Owl version and the available helpers change between
  series). Read the section that matches the file you touch, in the series
  of the target repository (`references.md`).
- The repository's lint and format configuration (pre-commit, ESLint,
  Prettier) wins over any other style source. Run it rather than checking
  by reading.
- Before using or flagging a helper, hook or API, confirm it exists in the
  target series (`git grep` in the framework sources).
- Avoid patching existing JavaScript when an extension point exists.
- A front-end behavior is described in the spec in plain words (what the
  user sees and does), so it can be validated without reading code, and it
  is covered by the repository's front-end test tools.
- Escaping and unsafe HTML: `security.md`.
