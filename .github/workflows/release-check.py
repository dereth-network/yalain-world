"""What release.yml checks, in one place it can be tried without a run.

release-check.py pin
    Reads release.toml. Refuses a tag that doesn't name its version, or an unset pin. Writes the
    pins to GITHUB_OUTPUT when set, else prints them.

release-check.py verify <builder checkout> <release folder> <what rustc -V said>
    Refuses unless the archive is the hash release.toml states, and the builder, its Cargo.lock and
    the compiler are the ones it pins.
"""
import hashlib, os, subprocess, sys, tomllib
from pathlib import Path


def refuse(why):
    print(f"::error::{why}")
    sys.exit(1)


def pins():
    return tomllib.load(open("release.toml", "rb"))


def pin():
    t = pins()
    version = t["version"]
    if not version:
        refuse("release.toml doesn't set version")
    tag = f"v{version}"
    if os.environ.get("GITHUB_REF_TYPE") == "tag" and os.environ["GITHUB_REF_NAME"] != tag:
        refuse(f"the tag {os.environ['GITHUB_REF_NAME']} doesn't name release.toml's version {version}")
    wanted = {
        "builder.commit": t["builder"]["commit"],
        "builder.cargo_lock_sha256": t["builder"]["cargo_lock_sha256"],
        "builder.toolchain": t["builder"]["toolchain"],
        "archive.sha256": t["archive"]["sha256"],
    }
    for name, value in wanted.items():
        if not value:
            refuse(f"release.toml doesn't set {name}")
    out = {
        "tag": tag,
        "commit": t["builder"]["commit"],
        "toolchain": t["builder"]["toolchain"].split()[1],
    }
    text = "".join(f"{k}={v}\n" for k, v in out.items())
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(text)
    else:
        print(text, end="")


def verify(builder, release, rustc_said):
    t, builder, release = pins(), Path(builder), Path(release)
    pinned, tag = t["builder"], f"v{t['version']}"

    head = subprocess.run(
        ["git", "-C", str(builder), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    if head != pinned["commit"]:
        refuse(f"the builder is at {head}, release.toml pins {pinned['commit']}")
    lock = hashlib.sha256((builder / "Cargo.lock").read_bytes()).hexdigest()
    if lock != pinned["cargo_lock_sha256"]:
        refuse(f"the builder's Cargo.lock is {lock}, release.toml pins {pinned['cargo_lock_sha256']}")
    if rustc_said.strip() != pinned["toolchain"]:
        refuse(f"built with {rustc_said.strip()}, release.toml pins {pinned['toolchain']}")

    archive = release / f"yalain-world-{tag}.zip"
    if not archive.is_file():
        refuse(f"{archive} wasn't made")
    sha = hashlib.sha256(archive.read_bytes()).hexdigest()
    if sha != t["archive"]["sha256"]:
        refuse(f"the archive is {sha}, release.toml states {t['archive']['sha256']}: nothing published")
    notes = release / f"yalain-world-{tag}.notes.md"
    if not notes.is_file():
        refuse(f"{notes} wasn't made")
    files = sorted(p.name for p in release.iterdir() if p.is_file())
    if len(files) != 3:
        refuse(f"the release folder holds {files}")
    print(f"{tag}: archive {sha}, as release.toml states")


if __name__ == "__main__":
    if sys.argv[1:2] == ["pin"]:
        pin()
    elif sys.argv[1:2] == ["verify"] and len(sys.argv) == 5:
        verify(*sys.argv[2:])
    else:
        sys.exit(__doc__)
