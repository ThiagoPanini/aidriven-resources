#!/usr/bin/env python3
"""Automate maintainer release flows.

Two intentionally separate steps are supported:

* ``prepare`` creates and pushes a ``release/vX.Y.Z`` branch with the manifest
  version bump and local release preflight.
* ``publish`` tags the merged release from ``main`` and pushes the tag.

The tag step stays separate because the release workflow enforces provenance:
the tag must point at the commit produced by merging a ``release/v*`` PR.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "manifest.json"
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def run(cmd: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def normalize_version(raw: str) -> tuple[str, str, str]:
    version = raw.strip()
    if version.startswith("v"):
        version = version[1:]
    if not SEMVER_RE.match(version):
        raise SystemExit(f"error: '{raw}' is not a valid semantic version")
    tag = f"v{version}"
    branch = f"release/{tag}"
    return version, tag, branch


def ensure_clean_tree() -> None:
    status = run(["git", "status", "--porcelain"], capture=True).stdout.strip()
    if status:
        raise SystemExit(
            "error: working tree is not clean; commit, stash, or discard changes before releasing"
        )


def ensure_ref_absent(kind: str, ref: str) -> None:
    if kind == "branch":
        local_cmd = ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{ref}"]
        remote_cmd = ["git", "ls-remote", "--exit-code", "--heads", "origin", ref]
    elif kind == "tag":
        local_cmd = ["git", "show-ref", "--verify", "--quiet", f"refs/tags/{ref}"]
        remote_cmd = ["git", "ls-remote", "--exit-code", "--tags", "origin", ref]
    else:
        raise ValueError(f"unsupported ref kind: {kind}")

    local = subprocess.run(local_cmd, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if local.returncode == 0:
        raise SystemExit(f"error: local {kind} '{ref}' already exists")

    remote = subprocess.run(remote_cmd, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if remote.returncode == 0:
        raise SystemExit(f"error: remote {kind} '{ref}' already exists on origin")


def checkout_updated_main() -> None:
    run(["git", "checkout", "main"])
    run(["git", "pull", "--ff-only", "origin", "main"])


def read_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def bump_manifest_version(version: str) -> None:
    manifest = read_manifest()
    current = manifest.get("version")
    if current == version:
        raise SystemExit(f"error: manifest.json is already at version {version}")
    manifest["version"] = version
    write_manifest(manifest)


def ensure_manifest_version(version: str) -> None:
    current = read_manifest().get("version")
    if current != version:
        raise SystemExit(
            f"error: manifest.json version is {current!r}, expected {version!r}; "
            "merge the matching release PR before publishing"
        )


def prepare_release(args: argparse.Namespace) -> int:
    version, tag, branch = normalize_version(args.version)
    ensure_clean_tree()
    ensure_ref_absent("branch", branch)

    checkout_updated_main()
    run(["git", "checkout", "-b", branch])
    bump_manifest_version(version)
    run(["make", "sync"])
    run(["make", "release-check"])
    run(["git", "add", "manifest.json"])
    run(["git", "commit", "-m", f"release: {tag}"])
    run(["git", "push", "-u", "origin", branch])

    print(f"prepared {branch}; open a PR titled 'release: {tag}'")
    return 0


def publish_release(args: argparse.Namespace) -> int:
    version, tag, _branch = normalize_version(args.version)
    ensure_clean_tree()
    ensure_ref_absent("tag", tag)

    checkout_updated_main()
    ensure_manifest_version(version)
    run(["make", "release-check"])
    run(["git", "tag", tag])
    run(["git", "push", "origin", tag])

    print(f"pushed {tag}; the Release workflow will publish after preflight")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare or publish aidriven-resources releases.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Create and push release/vX.Y.Z")
    prepare.add_argument("version", help="Release version, with or without leading 'v'")
    prepare.set_defaults(func=prepare_release)

    publish = subparsers.add_parser("publish", help="Tag main and push vX.Y.Z after release PR merge")
    publish.add_argument("version", help="Release version, with or without leading 'v'")
    publish.set_defaults(func=publish_release)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except subprocess.CalledProcessError as exc:
        return exc.returncode


if __name__ == "__main__":
    sys.exit(main())
