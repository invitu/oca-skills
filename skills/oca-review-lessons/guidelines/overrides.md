# Overrides of oca-guidelines

Source: rule of these skills, from review evidence (`evidence.md`).

This pack is listed after `oca-guidelines`, so these rules win.

## tests.md

Replaced by `tests.md` of this pack: an existing test or fixture is extended
before a test is added, and a bug fix adds at most one test method.

## manifest.md, licensing.md: `version` of an existing module

Unchanged by default: the merge bot bumps it. Exception: a change that ships a
migration script bumps `version` to the version that names its
`migrations/<version>/` folder, otherwise the script never runs ("Please
don't change manifest version, unless you provide migration scripts with the
change"). Say so in the pull request.

## licensing.md: `i18n/*.po` of an existing module

Unchanged by default: `.pot` files are regenerated on merge and translations
are done in Weblate. Exception: when the task deliberately changes an existing
translatable source string, the same `msgid` is updated in the `.pot` and in
every `.po` of the module, so existing translations survive ("You have to adapt
the translations as well"). A `.po` diff from a local re-export is never
committed.

## readme.md: `CONTRIBUTORS` of an existing module

A small fix does not add its author to `readme/CONTRIBUTORS`; a copyright line
in the touched file is enough ("for this tiny contribution, adding you in the
README in the module contributors seems too much"). `CREDITS` is for funders,
not authors.

## oca-pr-review output

The AI policy says not to post AI-generated review comments, and maintainers
apply it to reviews a human posts on an agent's behalf ("AI reviews must be
done with other GitHub user. A disclaimer on the foot doesn't serve."). So
`pr_review_<task>.md` gives the human findings with evidence and a suggested
verdict for the human's own judgment, without a summary message ready to
post. The human writes and posts the review in their own words.
