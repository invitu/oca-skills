# oca-skills

Skills for AI agents that write, fix, migrate and review Odoo modules following the OCA rules. Each skill is a role (specification, architecture, development, tests, security audit, review, README...) or a reference (`oca-guidelines`). The workflows say which roles take part in each type of task, in which order, and where a human validates.

The skills describe roles, sequence and gates. How they are run (by hand, in separate sessions, by sub-agents) is up to the environment. They do not depend on an Odoo series.

**Table of contents**

- [Use cases](#use-cases)
- [Context](#context)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Development](#development)
- [Known issues / roadmap](#known-issues--roadmap)
- [Bug tracker](#bug-tracker)
- [Credits](#credits)

## Use cases

The same roles are combined differently according to the task. Each workflow in `skills/oca-workflows/workflows/` lists the roles that take part, their order, what each reads and writes, and where a human validates.

| Task | Workflow | Roles involved |
|---|---|---|
| New standalone module | `isolated-module.md` | spec, spec controller, architect, dev, validator, tests, security audit, readme, reviewer |
| Project of several modules, possibly in several repositories | `multi-module-project.md` | project map, spec, spec controller, architect, then one `isolated-module.md` per module, then project map update |
| Study before developing | `feasibility.md` | spec, spec controller |
| Fix a bug reported in an issue | `bug-fix.md` | issue fix, dev, validator, tests, security audit, reviewer |
| Enhance an existing module | `enhancement.md` | same as `bug-fix.md`, from an improvement request |
| Migrate a module to another Odoo series | `migration.md` | availability check, migration plan, dev, validator, tests, reviewer |
| Review someone else's pull request | `pr-review.md` | pull request review (read-only) |
| Answer the reviews received on your pull request | `pr-feedback.md` | feedback analysis, dev, validator, tests, security audit, reviewer |
| Improve the README of a module | `readme.md` | readme, reviewer |
| Evaluate a third-party module before adopting it | `module-evaluation.md` | evaluation |
| Triage an issue (maintainer) | `issue-triage.md` | triage |

A task can change workflow as it evolves: a pull request review can lead to an enhancement of the reviewed module, then to an update of its README.

## Context

**Principles the skills are built on**

- **Economy.** Every token costs energy. Roles read only what the task needs, prefer deterministic tools (`grep`, `pre-commit`, scripts) to reasoning, run the narrowest checks, and write short outputs (`oca-guidelines/guidelines/efficiency.md`).
- **Security by design.** Security is planned in the spec and the architecture, implemented by default, and checked by the validator and the tests. An independent audit (`oca-security-audit`) comes later and never replaces it.
- **OCA rules first.** The OCA guidelines, the `.pylintrc` and the pre-commit configuration of the target repository prevail. Odoo's own guidelines and skills complete them where OCA is silent. A rule pack added after `oca-guidelines` can add or override rules, and the last pack wins.
- **Official sources.** Each guideline summarizes official documents, named in its `Source:` line and registered with a fingerprint in `oca-guidelines/sources.json`. A script detects when a source changed, and a broken source is reported by an issue that a human confirms.
- **Real code, never assumptions.** A model, field, method or API is read in the real source before it is used. What cannot be verified is marked `TO CONFIRM`.
- **Humans decide.** A human validates the status of each file, chooses the license among the options the agents list, and posts, pushes and merges. Judging roles are independent of the roles that wrote what they judge. The OCA AI policy applies: `Assisted-by:` trailer, no unsupervised agent.
- **Any series.** No rule is tied to a version. An Odoo series that is no longer maintained gets a warning, never a block.
- **Learn from the repository.** A convention that is not written is learned from the target repository's modules and reviews, not from a list of people.

## Installation

Each folder of `skills/` is a skill: a `SKILL.md` with its own files. Copy or mount the folders you need where your agent environment reads skills. `oca-guidelines` and `oca-workflows` are needed by almost all the others.

The scripts need Python 3. `check_sources.py` needs network access to `raw.githubusercontent.com`, and `gh` only to open an issue on a broken source.

## Configuration

- `skills/oca-guidelines/sources.json`: set `issues_repo` to the repository where broken sources are reported.
- `OCA_SKILLS_CACHE`: folder of the source-check cache and of the log of broken sources (default `~/.cache/oca-skills`).
- `check_sources.py --max-age`: how long a verified source is not downloaded again (default 7 days).
- Rule packs: list the packs that apply to a module, after `oca-guidelines`, in `architecture_<task>.md`. `oca-review-lessons` is a pack of what OCA reviewers repeatedly ask to change; list it for any change meant for an OCA repository.

## Usage

To use the skills:

1. Pick the workflow that matches the task in `skills/oca-workflows/SKILL.md` (new module, bug fix, enhancement, pull request review, migration...), after reading `common.md`.
2. Run the roles in the order of the workflow. Each role reads the files of the previous ones and writes its own in the task folder.
3. At each human step, read the file and set its status to `VALIDATED`, or send it back.
4. Let each role load `oca-guidelines` files only when its task needs them.

To inventory the modules of a multi-module project:

```bash
python3 -I skills/oca-project-map/scripts/extract_modules.py --target <series> <repository> [<repository> ...]
```

To find the sensitive patterns in a diff, before deciding on a security audit:

```bash
python3 -I skills/oca-security-audit/scripts/security_sweep.py --repo <repository> --range <git range>
```

To check that the guidelines used by a task are still current:

```bash
python3 -I skills/oca-guidelines/scripts/check_sources.py --series <series> <guideline> [<guideline> ...]
```

## Development

To add or change a guideline that summarizes an official document, write it from the source, add a `Source:` line, register the source in `skills/oca-guidelines/sources.json`, then record its fingerprint:

```bash
python3 -I skills/oca-guidelines/scripts/check_sources.py --accept <id>
```

`skills/oca-guidelines/AUTHORING.md` explains how the guidelines are organized. The tests of the scripts:

```bash
python3 -I skills/oca-project-map/tests/test_extract_modules.py
python3 -I skills/oca-guidelines/tests/test_check_sources.py
python3 -I skills/oca-security-audit/tests/test_security_sweep.py
```

## Known issues / roadmap

- Roles still to write: module evaluation, issue triage, analysis of the reviews received on a pull request, migration plan.
- Guidelines whose official source is not yet registered: `manifest`, `models-fields`, `tests`, `security`, `security-audit`, `javascript` (marked `Source: to confirm`).
- The skills have not yet been run on real tasks.
- The license of this repository and its place in the OCA organization are to be confirmed with OCA.

## Bug tracker

Bugs are tracked on [GitHub Issues](https://github.com/OCA/oca-skills/issues). In case of trouble, check there if your issue has already been reported.

## Credits

### Contributors

- Cyril VINH-TUNG <cyril@invitu.com>
