"""What release.yml checks, in one place it can be tried without a run.

release-check.py pin
    Reads release.toml. Refuses a tag that doesn't name its version, or an unset pin. Writes the
    pins to GITHUB_OUTPUT when set, else prints them.

release-check.py verify <builder checkout> <release folder> <what rustc -V said>
    Refuses unless the archive is the hash release.toml states, and the builder, its Cargo.lock and
    the compiler are the ones it pins.

release-check.py versions [<previous tag>]
    Refuses when a pack the previous release held has changed since, but its pack.toml still has
    the version it was released with. A pack new since then, or removed, may have any version, and a
    change to the version line alone is no change. The previous release is the newest v* tag that
    isn't release.toml's.
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


def git(*args):
    done = subprocess.run(["git", *args], capture_output=True)
    if done.returncode != 0:
        refuse(f"git {' '.join(args)}: {done.stderr.decode(errors='replace').strip()}")
    return done.stdout


def pack_toml(ref, pack):
    """A pack's pack.toml at `ref`, or None when it has none."""
    done = subprocess.run(["git", "show", f"{ref}:{pack}/pack.toml"], capture_output=True)
    return done.stdout.decode("utf-8") if done.returncode == 0 else None


def unmoved(previous, head="HEAD"):
    """The packs released at `previous` that changed by `head` and kept their version: [(pack, version)]."""
    released = sorted(
        path[: -len("/pack.toml")]
        for path in git("ls-tree", "-r", "-z", "--name-only", previous).decode("utf-8").split("\0")
        if path.count("/") == 1 and path.endswith("/pack.toml")
    )
    # A file moved between packs changes both.
    changed = {
        path.split("/", 1)[0]
        for path in git("diff", "--no-renames", "-z", "--name-only", previous, head).decode("utf-8").split("\0")
        if "/" in path
    }
    out = []
    for pack in released:
        after = pack_toml(head, pack) if pack in changed else None
        if after is None:
            continue
        # Any change with the version unmoved is a change beside the version line.
        version = tomllib.loads(pack_toml(previous, pack)).get("version")
        if tomllib.loads(after).get("version") == version:
            out.append((pack, version))
    return out


def versions(previous=None):
    if previous is None:
        tag = f"v{pins()['version']}"
        tags = git("tag", "--list", "v*", "--sort=-v:refname").decode("utf-8").split()
        previous = next((t for t in tags if t != tag), None)
        if previous is None:
            print("no earlier release: every pack is new")
            return
    stale = unmoved(previous)
    for pack, version in stale:
        print(f"::error::{pack} changed since {previous} but is still version {version}: "
              f"move its version in {pack}/pack.toml")
    if stale:
        sys.exit(1)
    print(f"every pack changed since {previous} moved its version")


if __name__ == "__main__":
    if sys.argv[1:2] == ["pin"]:
        pin()
    elif sys.argv[1:2] == ["verify"] and len(sys.argv) == 5:
        verify(*sys.argv[2:])
    elif sys.argv[1:2] == ["versions"] and len(sys.argv) <= 3:
        versions(*sys.argv[2:])
    else:
        sys.exit(__doc__)
