import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "extract_modules.py")


def make_repo(root, name, url, modules, allowed=None):
    repo = os.path.join(root, name)
    os.makedirs(os.path.join(repo, ".git"))
    with open(os.path.join(repo, ".git", "config"), "w") as fh:
        fh.write("[remote \"origin\"]\n\turl = %s\n" % url)
    if allowed:
        with open(os.path.join(repo, ".pylintrc-mandatory"), "w") as fh:
            fh.write("[MASTER]\nlicense-allowed=%s\n[MESSAGES CONTROL]\nenable=\n    license-allowed,\n" % allowed)
    for mod, (lic, version, depends) in modules.items():
        os.makedirs(os.path.join(repo, mod))
        with open(os.path.join(repo, mod, "__manifest__.py"), "w") as fh:
            fh.write(repr({"name": mod, "license": lic, "version": version, "depends": depends}))
        open(os.path.join(repo, mod, "__init__.py"), "w").close()
    return repo


class TestExtract(unittest.TestCase):
    def run_script(self, root, repos):
        out = subprocess.run(
            [sys.executable, "-I", SCRIPT, "--target", "18.0"] + [os.path.join(root, r) for r in repos],
            check=True, capture_output=True, text=True).stdout
        data = json.loads(out)
        return {m["module"]: m for m in data["modules"]}, data

    def test_alerts(self):
        with tempfile.TemporaryDirectory() as root:
            make_repo(root, "oca", "https://github.com/OCA/foo.git", {
                "a": ("AGPL-3", "18.0.1.0.0", ["p"]),
                "b": ("LGPL-3", "18.0.1.0.0", ["g"]),
                "c": ("OPL-1", "18.0.1.0.0", []),
                "d": ("LGPL-3", "18.0.1.0.0", ["a"]),
                "old": ("AGPL-3", "17.0.1.0.0", []),
                "new": ("AGPL-3", "18.0.1.0.0", ["old"]),
                "x": ("AGPL-3", "18.0.1.0.0", ["y"]),
                "y": ("AGPL-3", "18.0.1.0.0", ["x"]),
            }, allowed="AGPL-3,GPL-2 or any later version,LGPL-3")
            make_repo(root, "priv", "https://example.com/priv.git", {
                "p": ("OPL-1", "18.0.1.0.0", []),
                "g": ("GPL-2", "18.0.1.0.0", []),
            })
            mods, data = self.run_script(root, ["oca", "priv"])
        types = {(a["type"], a.get("module")) for a in data["alerts"]}
        self.assertIn(("OCA_DEPENDS_ON_NON_OCA", "a"), types)
        self.assertIn(("TO_CONFIRM_GPL2_ONLY", "b"), types)
        self.assertIn(("LICENSE_NOT_ALLOWED", "c"), types)
        self.assertIn(("INSUFFICIENT_LICENSE", "d"), types)
        self.assertIn(("UP_TO_DATE_DEPENDS_ON_MODULE_TO_MIGRATE", "new"), types)
        self.assertTrue(any(a["type"] == "DEPENDENCY_CYCLE" for a in data["alerts"]))
        self.assertEqual(data["migration_order"], [["old"]])
        self.assertEqual(mods["d"]["minimum_license"], "AGPL-3")
        self.assertEqual(mods["d"]["license_options"], ["AGPL-3"])
        self.assertIsNone(mods["p"]["license_options"])
        self.assertEqual(mods["b"]["license_options"], None)


if __name__ == "__main__":
    unittest.main()
