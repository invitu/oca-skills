**Principles the skills are built on**

- **Economy.** Every token costs energy. Roles read only what the task needs, prefer deterministic tools (`grep`, `pre-commit`, scripts) to reasoning, run the narrowest checks, and write short outputs (`oca-guidelines/guidelines/efficiency.md`).
- **Security by design.** Security is planned in the spec and the architecture, implemented by default, and checked by the validator and the tests. An independent audit (`oca-security-audit`) comes later and never replaces it.
- **OCA rules first.** The OCA guidelines, the `.pylintrc` and the pre-commit configuration of the target repository prevail. Odoo's own guidelines and skills complete them where OCA is silent. A rule pack added after `oca-guidelines` can add or override rules, and the last pack wins.
- **Official sources.** Each guideline summarizes official documents, named in its `Source:` line and registered with a fingerprint in `oca-guidelines/sources.json`. A script detects when a source changed, and a broken source is reported by an issue that a human confirms.
- **Real code, never assumptions.** A model, field, method or API is read in the real source before it is used. What cannot be verified is marked `TO CONFIRM`.
- **Humans decide.** A human validates the status of each file, chooses the license among the options the agents list, and posts, pushes and merges. Judging roles are independent of the roles that wrote what they judge. The OCA AI policy applies: `Assisted-by:` trailer, no unsupervised agent.
- **Any series.** No rule is tied to a version. An Odoo series that is no longer maintained gets a warning, never a block.
- **Learn from the repository.** A convention that is not written is learned from the target repository's modules and reviews, not from a list of people.
