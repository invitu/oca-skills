# Models and fields

Source: to confirm (not yet in `sources.json`).

- Never put `string=` on a field if the string is identical to the
  humanized field name (e.g. `field_name = fields.Char()` already displays
  "Field Name" — do not add `string="Field Name"`). OCA rule W8113.
- Always `return res` after a `super()` call in an overridden method, unless
  the method returns nothing by nature. OCA rule W8110.
- Never assume a field, model or method exists without having read it in the
  real source code (Odoo Community of the target series, or the target OCA module, via
  raw.githubusercontent.com). Applies to `oca-spec` as much as
  `oca-dev`.
