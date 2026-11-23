---
name: oca-review-lessons
description: Rule pack of what OCA reviewers repeatedly ask to change, learned from review comments; list it after oca-guidelines for any change meant for an OCA repository.
---

# oca-review-lessons

A rule pack (see `oca-guidelines/AUTHORING.md`). It adds the rules that OCA
reviewers keep asking for and that the written guidelines do not state, and
overrides a few rules of `oca-guidelines` where review practice is more
precise (`guidelines/overrides.md`).

## When to use

List this pack after `oca-guidelines` in `architecture_<task>.md` for any
module or diff meant for an OCA repository. `oca-dev`, `oca-tests`,
`oca-reviewer` and `oca-pr-review` load the files below when their task
touches the subject. The rules are not from an official document: each one
was asked for in several reviews, and `evidence.md` links examples.

| File | Read it when |
|---|---|
| `guidelines/overrides.md` | always, with `oca-guidelines`: rules of the base pack this pack changes |
| `guidelines/ai-tells.md` | before a diff, test, commit message, PR text or reply leaves the task |
| `guidelines/tests.md` | planning or writing tests (overrides the base `tests.md`) |
| `guidelines/scope-and-correctness.md` | choosing where a change goes; writing or reviewing Python, XML, security, docs |
| `guidelines/pr-text-and-replies.md` | writing a PR description or a reply to a review |
| `guidelines/migration-history.md` | migrating, backporting or forward-porting a module |
| `evidence.md` | checking where a rule comes from, or adding one |

## Adding a rule

A rule joins this pack when reviewers asked for it in at least two pull
requests, ideally from different reviewers or repositories. Add it to the
matching file in one or two sentences, with a short verbatim quote, and the
links in `evidence.md`. Attribute to the pull request, not to the person.
