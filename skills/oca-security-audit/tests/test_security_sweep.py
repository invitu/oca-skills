import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "security_sweep.py")


def git(repo, *args):
    subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)


def sweep(repo, rng):
    out = subprocess.run(
        [sys.executable, "-I", SCRIPT, "--repo", repo, "--range", rng],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(out)


class TestSweep(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = self.tmp.name
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "a@b.c")
        git(self.repo, "config", "user.name", "t")
        os.makedirs(os.path.join(self.repo, "m", "models"))
        os.makedirs(os.path.join(self.repo, "m", "security"))
        self.write("m/models/a.py", "x = 1\n")
        self.write("m/security/ir.model.access.csv", "id\na\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "base")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        with open(os.path.join(self.repo, rel), "w") as handle:
            handle.write(text)

    def commit(self):
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "change")

    def test_no_pattern(self):
        self.write("m/models/a.py", "x = 2\n")
        self.commit()
        self.assertEqual(sweep(self.repo, "HEAD~1..HEAD"), {"audit_required": False, "hits": []})

    def test_patterns_found_with_line(self):
        self.write("m/models/a.py", "x = 1\nrec = self.env['a'].sudo()\n@http.route('/p')\n")
        self.commit()
        result = sweep(self.repo, "HEAD~1..HEAD")
        self.assertTrue(result["audit_required"])
        self.assertEqual(result["hits"], [["m/models/a.py", 2, "sudo"], ["m/models/a.py", 3, "route"]])

    def test_context_lines_ignored(self):
        self.write("m/models/a.py", "x = 1\ny = 2\n")
        self.commit()
        self.write("m/models/a.py", "x = 1\ny = 3\n")
        self.commit()
        self.assertFalse(sweep(self.repo, "HEAD~1..HEAD")["audit_required"])

    def test_security_file_touched_even_on_removal(self):
        self.write("m/security/ir.model.access.csv", "id\n")
        self.commit()
        self.assertEqual(sweep(self.repo, "HEAD~1..HEAD")["hits"], [["m/security/ir.model.access.csv", 0, "security-file"]])


if __name__ == "__main__":
    unittest.main()
