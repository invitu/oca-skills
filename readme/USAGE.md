To use the skills:

1. Pick the workflow that matches the task in `skills/oca-workflows/SKILL.md` (new module, bug fix, enhancement, pull request review, migration...), after reading `common.md`.
2. Run the roles in the order of the workflow. Each role reads the files of the previous ones and writes its own in the task folder.
3. At each human step, read the file and set its status to `VALIDATED`, or send it back.
4. Let each role load `oca-guidelines` files only when its task needs them.

To inventory the modules of a multi-module project:

```bash
python3 -I skills/oca-project-map/scripts/extract_modules.py --target <series> <repository> [<repository> ...]
```

To check that the guidelines used by a task are still current:

```bash
python3 -I skills/oca-guidelines/scripts/check_sources.py --series <series> <guideline> [<guideline> ...]
```
