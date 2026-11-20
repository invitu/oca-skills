# Security audit

Source: to confirm (not yet in `sources.json`).

Run after implementation, on a module or a diff, by a role that did not write
the code. It does not replace security by design (`security.md`): it checks
that the design was followed and finds what was missed.

Sweep the code for each pattern, then judge each hit against its question. A
hit is not a finding by itself. Names and details depend on the series: read
the Odoo security documentation of the target series (`references.md`).

| Sweep for | Judge |
|---|---|
| `sudo(`, `with_user(`, `with_company(` | smallest scope? one-sentence reason? model, id, field, values or domain controlled by the caller? in controllers, are request keys whitelisted? |
| `cr.execute`, SQL wrappers, string building near SQL | ORM possible? values passed as parameters? identifiers through the framework's safe wrapper? |
| domains built from a request, an RPC call or a stored value | built with the domain API, not concatenated? user part validated? |
| public model methods (no leading `_`) | needed from outside? arguments validated? caller's rights checked inside? |
| `@http.route` | authentication matches the exposure? writes use POST? CSRF on, except dedicated webhooks? no state change on GET? |
| `Markup(`, `markup(`, `innerHTML`, `insertAdjacentHTML`, `t-raw` | only literals marked safe? user content escaped? |
| fields holding passwords, tokens, secrets | restricted with `groups`? readable through a `related` field or a search? |
| `related=` crossing models | does it reach sensitive data with elevated rights in this series? |
| `open(` | the framework's confined file API instead? |
| `eval(`, `exec(`, `safe_eval` | none? otherwise parsed with `json` or `ast.literal_eval`? |
| `pickle` | never on untrusted data |
| `getattr(`, `setattr(` on records | item access with a validated field name instead? |
| `==` on a secret or token | constant-time comparison, or a database lookup? |
| `create` override that checks `vals` before `super()` | bypassable through context defaults or stored defaults? check where the framework builds the final values in this series |
| `security/` files | create, write, delete granted to everyone, portal or public? every operation that needs a restriction covered? multi-company restriction present? sensitive models restricted by domain? |
| mutable default arguments | none |
| `cr.commit()` | none |
| keys, tokens, passwords in code, data, tests | none |
| new external dependency | needed, license known, maintained? |

The audit is complete when every pattern has been swept and every hit
judged. Report each finding with severity (`blocking`, `suggestion`), file and
line, the scenario in which it fails, and the fix described in words, no
code.
