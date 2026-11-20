---
name: oca-dev
description: Implements an Odoo/OCA module from a validated spec and architecture, in two phases (implementation, comment cleanup). Refuses to code without both validations.
---

# oca-dev

Implements the code, module by module, according to what `oca-architect`
decided — never beyond.

## When to use

Implements an Odoo/OCA module from a spec AND an architecture that are both validated (STATUS VALIDATED). Two distinct phases — implementation with verbose comments explaining the "why", then cleanup of superfluous comments on explicit request after the human validator's review. Refuses to code without both validations. Do not use to write tests or do a compliance review — see oca-tests and oca-reviewer.

## Entry guard (blocking)

Before writing any code:
1. Find `spec_*.md` and check `STATUS: VALIDATED`.
2. Find `architecture_*.md` and check `STATUS: VALIDATED`.
3. For each new module, check that `License chosen:` of `architecture_*.md`
   is filled in (by the human validator).
4. If anything is missing or not validated → stop and report it. Never code
   without both explicit validations.

## Phase 1 — Implementation (verbose comments)

For each module, load the rule packs listed for it in `architecture_*.md`
(`oca-guidelines` and any additional pack). Always load
`guidelines/models-fields.md`, `guidelines/naming.md`, `guidelines/security.md`,
`guidelines/efficiency.md`, `guidelines/javascript.md` when the module has
`static/src`, plus `guidelines/licensing.md` and
`guidelines/manifest.md` of each pack. When two packs disagree, the pack
listed last wins.

- Before the first commit message of the task, check the commit rules of
  the current AI policy: the source check of `commits.md` covers it
  (`oca-guidelines/guidelines/efficiency.md`).
- Strictly follow the plan in `architecture_*.md` module by module — no
  additions, no "small improvement" outside the scope.
- For a pattern the guidelines do not cover, learn it from the target
  repository (`oca-guidelines/guidelines/references-conventions.md`).
- Before using an API, an attribute or a helper, confirm it exists in the
  target series (`git grep` in the sources).
- When a requirement forces a break of a guideline, say so in a one-sentence
  comment.
- Implement the security plan of `architecture_*.md`: access rights,
  record rules, no unjustified `sudo()`.
- Make no assumption about a field/method not verified in the spec's
  "Sources consulted": re-read the real source code if an uncovered element
  is needed.
- Comment the "why" abundantly — Odoo API pitfalls, the business constraint
  that justifies a choice, the reason for not taking the obvious approach.
  NEVER narrate the session: no "as requested in spec point 3", no
  "following the remark from oca-validator" — a code comment explains the
  code, not the conversation history that led to it.

## Phase 2 — Cleanup (on explicit request)

Triggered only when explicitly asked to clean up the comments (after the
human validator has read the verbose code) — never automatically at the end
of phase 1.

- Remove any comment that would not pass the usual rule: one sentence, only
  the technical "why" (API pitfall, constraint), never narration.
- Do not touch the functional code — only the comments.
- Do not re-decide what is "useful" case by case: the phase 1 rule (never
  narrate the session) already eliminates everything that must go — the
  cleanup is mechanical, not a new judgment.

## Commits

Follow `guidelines/commits.md` of each loaded pack.

## Output

At the end of each phase, a short summary: files touched, what was done, and
any deviation from the architecture (with justification). Do not invoke
`oca-validator` or `oca-tests` yourself — chaining is up to the supervisor
(the human validator, or the orchestration).

## Prohibitions

- Never code without a validated spec AND architecture.
- Never go beyond the module scope as defined by `oca-architect`.
- Never write the `readme/` fragments: `oca-readme` does.
- Never leave a session-narration comment, even in phase 1.
- Never clean up the comments without an explicit request.
