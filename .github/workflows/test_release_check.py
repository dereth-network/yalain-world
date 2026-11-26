"""Tests of release-check.py's `versions`: a pack the last release held that changed must move its version.

    python3 -m unittest discover -s .github/workflows
"""
import importlib.util, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("release_check", HERE / "release-check.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

PACK = 'format_version = 1\nname = "{name}"\nversion = "{version}"\ngame = "ac2"\nlicense = "CC0-1.0"\n'


class Versions(unittest.TestCase):
    def setUp(self):
        self.was = os.getcwd()
        self.root = Path(tempfile.mkdtemp(prefix="release-check-"))
        os.chdir(self.root)
        self.env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                    "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.invalid",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.invalid"}
        self.git("init", "-q", "-b", "main")
        (self.root / "release.toml").write_text('version = "0.2.0"\n')
        for name in ("camps", "quests", "loot"):
            self.pack(name, "0.1.0")
            self.write(f"{name}/server/rows.toml", f"# {name}\n")
        self.commit()
        self.git("tag", "v0.1.0")

    def tearDown(self):
        os.chdir(self.was)
        shutil.rmtree(self.root, ignore_errors=True)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, env=self.env, check=True,
                              capture_output=True, text=True).stdout

    def write(self, path, text):
        (self.root / path).parent.mkdir(parents=True, exist_ok=True)
        (self.root / path).write_text(text)

    def pack(self, name, version):
        self.write(f"{name}/pack.toml", PACK.format(name=name, version=version))

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", "change")

    def unmoved(self):
        return rc.unmoved("v0.1.0")

    def test_a_changed_pack_that_kept_its_version_is_refused(self):
        self.write("camps/server/rows.toml", "# camps, more\n")
        self.commit()
        self.assertEqual(self.unmoved(), [("camps", "0.1.0")])

    def test_a_changed_pack_that_moved_its_version_passes(self):
        self.write("camps/server/rows.toml", "# camps, more\n")
        self.pack("camps", "0.1.1")
        self.commit()
        self.assertEqual(self.unmoved(), [])

    def test_a_new_file_in_a_released_pack_is_a_change(self):
        self.write("camps/server/landblocks/0101.toml", "# a landblock\n")
        self.commit()
        self.assertEqual(self.unmoved(), [("camps", "0.1.0")])

    def test_a_change_to_pack_toml_beside_its_version_is_a_change(self):
        self.write("quests/pack.toml", PACK.format(name="quests", version="0.1.0") + 'description = "More."\n')
        self.commit()
        self.assertEqual(self.unmoved(), [("quests", "0.1.0")])

    def test_moving_only_the_version_passes(self):
        self.pack("loot", "0.2.0")
        self.commit()
        self.assertEqual(self.unmoved(), [])

    def test_a_new_pack_passes_at_any_version(self):
        self.pack("wilds", "0.1.0")
        self.write("wilds/server/rows.toml", "# wilds\n")
        self.commit()
        self.assertEqual(self.unmoved(), [])

    def test_untouched_and_removed_packs_pass(self):
        self.git("rm", "-q", "-r", "loot")
        self.commit()
        self.assertEqual(self.unmoved(), [])

    def test_a_file_moved_between_packs_changes_both(self):
        self.git("mv", "camps/server/rows.toml", "quests/server/camps.toml")
        self.commit()
        self.assertEqual(self.unmoved(), [("camps", "0.1.0"), ("quests", "0.1.0")])

    def test_the_command_compares_with_the_newest_tag_that_is_not_release_toml_s(self):
        self.write("camps/server/rows.toml", "# camps, more\n")
        self.commit()
        self.git("tag", "v0.2.0")  # release.toml's own tag, when the release is tagged
        run = subprocess.run([sys.executable, str(HERE / "release-check.py"), "versions"], cwd=self.root,
                             env=self.env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("camps changed since v0.1.0 but is still version 0.1.0", run.stdout)
        self.pack("camps", "0.2.0")
        self.commit()
        run = subprocess.run([sys.executable, str(HERE / "release-check.py"), "versions"], cwd=self.root,
                             env=self.env, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
