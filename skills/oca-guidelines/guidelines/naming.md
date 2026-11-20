# Naming

Source: `contributing-modules`, `contributing-file-naming`,
`contributing-xmlid`, `contributing-symbols`, `contributing-models`
(`sources.json`). Applies to a new module. On an existing module, follow the
names it already uses.

## Module name

- `[a-z0-9_]` only, singular (or `multi`), except when it is built from an
  Odoo module or object name that is already plural.
- Base for other modules: prefix `base_` (`base_location_nuts`).
- Localization: prefix `l10n_<country code>_` (`l10n_es_pos`).
- Extends an Odoo module: prefix with that module's name (`mail_forward`).
- Combines an Odoo module and an OCA module: the Odoo name first
  (`crm_partner_firstname`).
- Before proposing a name, check that no module of the available addons
  already uses it.

## Files

Only `[a-z0-9_]`. Split by the model, created or inherited:

| Content | File |
|---|---|
| models | `models/<model>.py` |
| views | `views/<model>_views.xml` |
| data | `data/<model>_data.xml` |
| demo | `demo/<model>_demo.xml` |
| templates | `templates/<model>_template.xml` |
| single controller file | `controllers/main.py` |
| static files | `static/<type>/<module_name>.<ext>` |

`<model>` is the model name with dots replaced by underscores
(`res.partner` gives `res_partner`). A model used only as a one2many of a
main model can stay in the file of that main model.

## Python

- Model: dotted lowercase, singular (`sale.order`). Class: UpperCamelCase.
- Variables: snake_case. Constants: UPPERCASE. Meaningful names, one letter
  only in a lambda or a loop index.
- `_id` or `_ids` suffix only for a variable that holds ids, not records.
- Methods: `_compute_<field>`, `_inverse_<field>`, `_search_<field>`,
  `_default_<field>`, `_onchange_<field>`, `_check_<constraint>`; an action
  called from a button or menu starts with `action_`.

## XML ids

Never prefix with the module name. `<model>` is the model name with dots
replaced by underscores.

| Record | Id |
|---|---|
| data | `<model>_<record_name>` |
| menu | `<model>_menu` |
| view | `<model>_view_<type>` (`form`, `kanban`, `search`, the list type as the series names it...) |
| main action | `<model>_action`; other actions `<model>_action_<detail>` |
| group | `<model>_group_<group>` (`user`, `manager`...) |
| rule | `<model>_rule_<group>` |

A view that inherits another keeps the name of the original when the
original does not follow these patterns. A module extends a given view only
once.
