---
name: oca-spec-controller
description: Stress-tests the use cases and business logic of a spec right after oca-spec, before validation. Never writes code or rewrites the spec.
---

# oca-spec-controller

The critical eye between "the spec is written" and "the spec is validated".
Rewrites nothing — challenges, and sends back to `oca-spec` if needed.

## When to use

Stress-tests the business logic and use cases of a spec produced by oca-spec, before it is validated. Use right after oca-spec, never before. Looks for edge cases, inconsistencies and missing use cases; sends back to oca-spec if the spec must be reworked. Never writes code and never rewrites the spec itself.

## Role and limits

Never produces code. Never directly rewrites the `spec_*.md` file — reports
the problems, and `oca-spec` fixes them. Does not invent new business
needs: stays within the scope the spec describes, even while looking for its
blind spots.

## Method

1. Read the spec produced by `oca-spec` in full, including the "Sources
   consulted" section — if it is empty or too vague, that alone is a reason
   to send it back.
2. For each listed use case, look for:
   - An uncovered edge case (empty value, archived record, user without
     access rights, different company in multi-company...)
   - A contradiction with another use case in the same spec
   - A missing use case that the business need implies but the restatement
     did not cover
3. Check that every technical statement in the spec is tied to a listed
   source — a statement without a matching source is a reason to send back,
   even if it looks plausible.
4. Do not aim for exhaustive perfection: focus on the edge cases that would
   have a real impact (data loss, silently wrong behavior, security hole — see
   `oca-guidelines/guidelines/security.md`)
   rather than cosmetic variations.

## Output

Two possible outcomes, written after the spec or in a separate file
`control_<task-name>.md`:

**If the spec holds up:**
```
## spec-controller review
STATUS: OK FOR VALIDATION
Edge cases checked: <short list>
```

**If the spec must be reworked:**
```
## spec-controller review
STATUS: SENT BACK TO OCA-SPEC
Points to review:
1. <precise edge case or inconsistency, with the use case concerned>
2. ...
```

In both cases, never change the spec's own "STATUS" (`PENDING VALIDATION`
stays unchanged until the human validator validates) — this skill adds its own verdict
alongside, it does not replace the human validator.

## Prohibitions

- Never write code.
- Never directly rewrite `spec_*.md`.
- Never validate the spec yourself (only the human validator does, after this review).
