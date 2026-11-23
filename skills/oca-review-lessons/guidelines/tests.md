# Unit tests

Source: rule of these skills, from review evidence (`evidence.md`). Overrides
`oca-guidelines/guidelines/tests.md`.

The CI of a repository runs every test of every module on each pull request,
so each test costs every later contributor time ("extending CI times a lot").

- **Extend before adding.** First an existing test that already runs the flow:
  add the case or one assertion there. Then an existing fixture ("just take one
  of the already existing CSVs ... and add that padding in it"). Then, only if
  neither works, one new test method. A new test class, fixture file or records
  in a shared base class need a reason stated in the task files.
- **One use case, not its variants.** "You just need to check the new case, not
  all the variants." A use case of the spec is covered by an assertion, not
  necessarily by a method of its own.
- **Business flows.** No direct call of private, compute or onchange methods
  ("They should be triggered through business flows"); no synthetic flow;
  run real libraries or servers rather than patching everything.
- **Fails without the change.** Checked by running it without the change, or
  reported as not checked.
- **Existing assertions are not bent** to make new code pass: "These changes
  on the tests highlights that something is not going correct."
- **Fixed expected values**, not recomputed with the code's own logic.
- **No demo data** (not loaded by default from 19.0); data in `setUpClass`.
  Accounting tests: `post_install` and the base test classes of the series,
  so a chart of accounts is loaded, instead of creating accounts; never force
  one country's chart.
- **Cheap setup.** `setUpClass`, tracking disabled (or `BaseCommon`); nothing
  added to a base class that many classes inherit.
- `freeze_time` on methods, not on the class; `assertRaises(UserError)`
  without matching the message unless the message is the point; keep existing
  `mute_logger`.
- Before changing test base classes, read the migration guide of the series
  (for example `_test_user_groups = None` with `BaseCommon` from 20.0).
