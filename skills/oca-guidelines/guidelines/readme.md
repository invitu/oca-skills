# Module README

Source: `readme-fragments`, `readme-template-*`, `contributing-directories`,
`contributing-file-naming` (`sources.json`). The image limits (200 KB, 10 per
module) are a rule of these skills, not an OCA rule.

Applies to a new module meant for OCA and, for an existing module, to the
fragments the task allows (`licensing.md`).

## Fragments

`README.rst` is generated from `readme/`: never create or edit it. All the
fragments of a module use one format (`.md` or `.rst`), never both. Follow
the format already used by the module or the repository.

| Fragment | Status | Content |
|---|---|---|
| `DESCRIPTION` | required | What the module does and what it is for, 2 or 3 paragraphs at most |
| `USAGE` | required | How an end user uses it, step by step. No visible effect on the interface: `This module does not impact the user interface.` |
| `CONTRIBUTORS` | required | `- Name <email> (optional website)`, one per line |
| `CONFIGURE` | when there is something to configure | How an administrator configures it before use: path, steps, screenshots |
| `INSTALL` | only for specific instructions | For system administrators, for example a non-Python dependency |
| `CONTEXT` | optional, recommended | The business need, use cases, related modules |
| `ROADMAP` | optional | Known limits and possible improvements |
| `CREDITS` | optional | Sponsors, beyond authors and contributors |
| `DEVELOP` | optional | Follow the repository's examples |
| `HISTORY` | generated | Never written by hand. If the repository has `readme/newsfragments/`, add a fragment like the existing ones; otherwise TO CONFIRM |

## Style

- Short, precise, succinct, and explicit enough for a human who does not
  know the code.
- English, present tense, the words of the interface (menu and field names).
- Describes what the user sees and does. Never the architecture, the design
  choices, the code, or how the module was built.
- No mention of a review, a request, a previous version or a conversation.
- One fact in one fragment. `DESCRIPTION` says what, `USAGE` says how,
  `CONFIGURE` says what to set first.
- Source every statement in the spec, the architecture or the code. Never
  describe a behavior that was not read there.

## Images

Screenshots make `USAGE` and `CONFIGURE` clearer. Optional, never decorative.

- Files in `static/description/`, copied into the module: never an external
  URL. Referenced from a fragment as
  `![short description](../static/description/<name>.png)`.
- PNG or GIF. At most 200 KB per image and 10 images per module (limits set
  here, open to discussion by the community). Crop to the relevant area,
  descriptive file name, no personal data.
- A screenshot shows the real interface of the module. Never an image
  drawn to look like it.
- If the agent cannot produce the screenshots, it says so, and the human
  chooses: add the images, or no images.

## Checks

- Required fragments present, no `README.rst` modified, one format.
- Every image exists at the referenced path and respects the limits.
- Every sentence is true of the code.
