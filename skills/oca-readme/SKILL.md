---
name: oca-readme
description: Writes or improves the readme/ fragments of an Odoo/OCA module from its validated spec and code. Never edits README.rst, never invents a screenshot.
---

# oca-readme

Writes what a human reads first: the module README, as `readme/` fragments.

## When to use

Writes the readme/ fragments of a new Odoo/OCA module from its validated spec and its code, or improves the fragments of an existing module from a validated plan. Short, precise, true of the code. Never edits README.rst and never invents a screenshot. Do not use to write code, tests or to review.

## Role and limits

Writes only `readme/` fragments and the images they reference in
`static/description/`. Never edits `README.rst`, `index.html`, code, or
anything else. Never describes a behavior it did not read in the spec, the
architecture or the code.

## Entry guard (blocking)

- New module: `spec_*.md` and `architecture_*.md` are `STATUS: VALIDATED`,
  and the code exists. The README is written after the code, so it
  describes what the module really does.
- Existing module (improvement): the request is clear and the module code is
  available. Without a validated plan, only the analysis mode below.
- Otherwise stop and report what is missing.

## Method

Load `oca-guidelines/guidelines/readme.md` (and the pack's `licensing.md`
for an existing module). Read the existing fragments of the module and of
one similar module of the repository to follow its format.

**New module**
1. From the spec: the need and the behavior (`DESCRIPTION`, `CONTEXT`).
2. From the code, one targeted pass: menus, fields and buttons as the user
   sees them (`views/`, `security/` groups), settings (`CONFIGURE`),
   external dependencies (`INSTALL`).
3. Write the required fragments, then the others only when the module has
   something to say. Contributors come from the task instructions;
   missing: `TO CONFIRM`.
4. Images: see below.

**Improvement of an existing module**
1. Analysis. Compare each fragment with the guideline and with the code.
   Write `readme_plan_<task>.md`: one line per change, with the fragment,
   the change and its evidence (file and line of the code, or the rule), and
   the screenshots that would help. Nothing else. Last line:
   `STATUS: PENDING VALIDATION`.
2. Only after the human sets `STATUS: VALIDATED`: apply exactly the plan, and
   touch no other fragment.

**Images**
Produce a screenshot only where a user would otherwise hesitate (`USAGE` and
`CONFIGURE` steps), within the limits of `readme.md`. Capture the real
interface with the tools of the environment. If no tool can, write nothing
and report it: the human then adds the images, or chooses to have none.
Never create an image that imitates the interface.

## Output

The fragments written, the images added with their size, and the lines left
as `TO CONFIRM`. Do not run the reviewer yourself.

## Prohibitions

- Never edit `README.rst`, `index.html`, `HISTORY` by hand, or code.
- Never go beyond the validated plan on an existing module.
- Never write architecture, design choices, or session narration.
- Never invent a behavior, a screenshot or a contributor.
- Never set a status to `VALIDATED`: only a human does.
