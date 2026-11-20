import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "check_sources.py")
DOC = "Intro\n=====\n\nText\n\nCommit\n======\n\nrule one\n\nOther\n=====\n\nelse\n"


class Handler(http.server.BaseHTTPRequestHandler):
    doc = DOC
    hits = 0

    def do_GET(self):
        Handler.hits += 1
        if self.path == "/doc":
            body = Handler.doc.encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


class TestCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        cls.base = "http://127.0.0.1:%d" % cls.server.server_port
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def run_check(self, tmp, entries, *args):
        reg = os.path.join(tmp, "sources.json")
        with open(reg, "w") as fh:
            json.dump({"entries": entries}, fh)
        out = subprocess.run(
            [sys.executable, "-I", SCRIPT, "--registry", reg, "--cache-dir", tmp, "--verbose", *args],
            check=True, capture_output=True, text=True).stdout
        return {r["id"]: r for r in json.loads(out)["results"]}

    def entry(self, id_, path="/doc", heading="Commit", **kw):
        base = {"id": id_, "guidelines": ["guidelines/g.md"], "url": self.base + path,
                "mode": "hash", "extract": {"type": "rst_section", "heading": heading},
                "sha256": ""}
        base.update(kw)
        return base

    def test_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            Handler.doc = DOC
            reg = os.path.join(tmp, "sources.json")
            with open(reg, "w") as fh:
                json.dump({"entries": [self.entry("a")]}, fh)
            subprocess.run([sys.executable, "-I", SCRIPT, "--registry", reg, "--cache-dir", tmp,
                            "--accept", "a"], check=True, capture_output=True)
            entries = json.load(open(reg))["entries"]
            sha = entries[0]["sha256"]
            entries += [
                self.entry("missing_section", heading="Nope", sha256=sha),
                self.entry("gone", path="/nothing", sha256=sha),
                self.entry("alt", path="/nothing", sha256=sha, alt=[self.base + "/doc"]),
                self.entry("down", sha256=sha, url="http://127.0.0.1:1/doc"),
            ]
            res = self.run_check(tmp, entries, "g.md")
            self.assertEqual(res["a"]["state"], "OK")
            self.assertEqual(res["missing_section"]["state"], "SECTION_NOT_FOUND")
            self.assertEqual(res["gone"]["state"], "NOT_FOUND")
            self.assertEqual(res["alt"]["state"], "OK")
            self.assertEqual(res["down"]["state"], "UNREACHABLE")
            issues = open(os.path.join(tmp, "sources-issues.jsonl")).read()
            self.assertIn("gone", issues)
            self.assertNotIn("down", issues)

            Handler.doc = DOC.replace("rule one", "rule two")
            res = self.run_check(tmp, entries[:1], "g.md", "--max-age", "1m")
            self.assertEqual(res["a"]["state"], "OK")  # cached, not downloaded again
            os.remove(os.path.join(tmp, "sources-cache.json"))
            res = self.run_check(tmp, entries[:1], "g.md")
            self.assertEqual(res["a"]["state"], "CHANGED")
            self.assertIn("rule two", res["a"]["extract"])
            self.assertNotIn("else", res["a"]["extract"])

    def test_compact_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            Handler.doc = DOC
            reg = os.path.join(tmp, "sources.json")
            with open(reg, "w") as fh:
                json.dump({"entries": [self.entry("a"), self.entry("gone", path="/nothing")]}, fh)
            subprocess.run([sys.executable, "-I", SCRIPT, "--registry", reg, "--cache-dir", tmp,
                            "--accept", "a"], check=True, capture_output=True)
            out = subprocess.run([sys.executable, "-I", SCRIPT, "--registry", reg,
                                  "--cache-dir", tmp, "g.md"], check=True,
                                 capture_output=True, text=True).stdout
            data = json.loads(out)
            self.assertEqual((data["checked"], data["ok"]), (2, 1))
            self.assertEqual([r["id"] for r in data["results"]], ["gone"])

    def test_issue(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = os.path.join(tmp, "sources.json")
            entry = self.entry("gone", path="/nothing", sha256="x")
            with open(reg, "w") as fh:
                json.dump({"issues_repo": "owner/skills", "entries": [entry]}, fh)

            def run(*args, path=None):
                env = dict(os.environ)
                if path:
                    env["PATH"] = path + os.pathsep + env["PATH"]
                return subprocess.run(
                    [sys.executable, "-I", SCRIPT, "--registry", reg, "--cache-dir", tmp, *args],
                    capture_output=True, text=True, env=env)

            self.assertIn("Nothing to report", run("--issue-text").stdout)
            run("g.md")
            text = run("--issue-text").stdout
            self.assertIn("owner/skills", text)
            self.assertIn("`gone`", text)
            self.assertNotEqual(run("--open-issue").returncode, 0)  # needs --confirmed

            bin_ok = os.path.join(tmp, "ok")
            os.makedirs(bin_ok)
            gh = os.path.join(bin_ok, "gh")
            with open(gh, "w") as fh:
                fh.write("#!/bin/sh\nif [ \"$2\" = list ]; then echo '[]'; "
                         "else echo https://github.com/owner/skills/issues/1; fi\n")
            os.chmod(gh, 0o755)
            done = run("--open-issue", "--confirmed", path=bin_ok)
            self.assertIn("CREATED: https://github.com/owner/skills/issues/1", done.stdout)
            self.assertIn("Nothing to report", run("--issue-text").stdout)

    def test_issue_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = os.path.join(tmp, "sources.json")
            with open(reg, "w") as fh:
                json.dump({"issues_repo": "owner/skills",
                           "entries": [self.entry("gone", path="/nothing", sha256="x")]}, fh)
            base = [sys.executable, "-I", SCRIPT, "--registry", reg, "--cache-dir", tmp]
            subprocess.run(base + ["g.md"], check=True, capture_output=True)
            bin_ko = os.path.join(tmp, "ko")
            os.makedirs(bin_ko)
            gh = os.path.join(bin_ko, "gh")
            with open(gh, "w") as fh:
                fh.write("#!/bin/sh\necho 'permission denied' >&2\nexit 1\n")
            os.chmod(gh, 0o755)
            env = dict(os.environ, PATH=bin_ko + os.pathsep + os.environ["PATH"])
            done = subprocess.run(base + ["--open-issue", "--confirmed"], capture_output=True,
                                  text=True, env=env)
            self.assertNotEqual(done.returncode, 0)
            self.assertIn("Create the issue by hand", done.stderr)


if __name__ == "__main__":
    unittest.main()
