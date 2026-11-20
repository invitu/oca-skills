To add or change a guideline that summarizes an official document, write it from the source, add a `Source:` line, register the source in `skills/oca-guidelines/sources.json`, then record its fingerprint:

```bash
python3 -I skills/oca-guidelines/scripts/check_sources.py --accept <id>
```

`skills/oca-guidelines/AUTHORING.md` explains how the guidelines are organized. The tests of the scripts:

```bash
python3 -I skills/oca-project-map/tests/test_extract_modules.py
python3 -I skills/oca-guidelines/tests/test_check_sources.py
```
