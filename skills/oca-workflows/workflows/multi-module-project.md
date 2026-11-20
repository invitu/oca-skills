# Multi-module project

Several modules, possibly in several OCA repositories, that depend on each
other or on other OCA and extra-OCA modules.

**Input**: the project need, and the existing documents.

| # | Step | Reads | Writes | Notes |
|---|---|---|---|---|
| 0 | `oca-project-map` | manifests and code of every repository | `docs/map.proposed.md`, then `docs/map.md` once a human validates it | modules, repositories, dependencies, Odoo series, modules to migrate, license alerts |
| 1 | `oca-spec` at project level, then `oca-spec-controller` | need, map | project spec, control | independent control |
| 2 | human | spec, control | status of the spec | |
| 3 | `oca-architect` at project level | validated spec, map | architecture: one task per module, with its repository and dependencies | |
| 4 | human | architecture | status | |
| 5 | one isolated-module workflow per task | project documents | module | see `isolated-module.md`, from step 1 |
| 6 | `oca-project-map` update | all repositories | `docs/map.proposed.md` | after each module merged; a human replaces `docs/map.md` |

**Order of tasks**: modules with no dependency on another task come first.
A task starts when every module it depends on is merged. Tasks at the same
level run in parallel (see `common.md`).

**Inherited modules**: a task receives only the modules it depends on,
read-only, not the whole project.

**Checks at step 6** (alerts of the map): no `OCA_DEPENDS_ON_NON_OCA`, every
module is on the project's Odoo series or marked "to migrate", no
`DEPENDENCY_CYCLE`, no `LICENSE_NOT_ALLOWED` or `INSUFFICIENT_LICENSE`.
