#!/usr/bin/env python3
"""Synchronize external documentation mirrors and regenerate README."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
MIRRORS_FILE = REPO_ROOT / ".github/mirrors.json"
README_FILE = REPO_ROOT / "README.md"
META_FILENAME = ".mirror-meta.json"
TREE_EXCLUDES = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}


class SyncError(RuntimeError):
    """Raised when a mirror cannot be synchronized."""


def run(cmd: Sequence[str], *, cwd: Path | None = None) -> str:
    """Execute a shell command and return stdout."""

    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    return result.stdout.strip()


def load_config(config_path: Path) -> List[dict]:
    if not config_path.exists():
        raise SyncError(f"Missing config file: {config_path}")
    data = json.loads(config_path.read_text())
    if not isinstance(data, list):
        raise SyncError("mirrors.json must contain a list")
    for entry in data:
        if not isinstance(entry, dict):
            raise SyncError("Each mirror entry must be an object")
        for key in ("owner", "repo", "branch", "docsPath"):
            if key not in entry:
                raise SyncError(f"Mirror entry missing '{key}' field: {entry}")
    return data


def sparse_checkout(entry: dict) -> tuple[Path, str]:
    owner = entry["owner"]
    repo = entry["repo"]
    branch = entry["branch"]
    docs_path = entry["docsPath"]

    repo_url = f"https://github.com/{owner}/{repo}.git"
    token = os.getenv("MIRROR_GIT_TOKEN")
    if token:
        repo_url = f"https://{token}@github.com/{owner}/{repo}.git"

    checkout_dir = Path(tempfile.mkdtemp(prefix="mirror-"))
    try:
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--filter=blob:none",
                "--sparse",
                "-b",
                branch,
                repo_url,
                str(checkout_dir),
            ]
        )
        run(["git", "sparse-checkout", "set", docs_path], cwd=checkout_dir)
        source_dir = checkout_dir / docs_path
        if not source_dir.exists():
            raise SyncError(
                f"Docs path '{docs_path}' not found in {owner}/{repo}@{branch}"
            )
        commit = run(["git", "rev-parse", "HEAD"], cwd=checkout_dir)
        return source_dir, commit
    except Exception:
        shutil.rmtree(checkout_dir, ignore_errors=True)
        raise


def copy_tree(src: Path, dest: Path, *, dry_run: bool) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    tracked_files = set()
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if path.is_dir():
            if not dry_run:
                (dest / rel).mkdir(parents=True, exist_ok=True)
            continue
        tracked_files.add(rel)
        if dry_run:
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    if dest.exists() and not dry_run:
        for path in sorted(dest.rglob("*"), reverse=True):
            if path.name == META_FILENAME:
                continue
            rel = path.relative_to(dest)
            if path.is_file() and rel not in tracked_files:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()


def write_meta(dest: Path, entry: dict, commit: str, *, dry_run: bool) -> None:
    meta = {
        "owner": entry["owner"],
        "repo": entry["repo"],
        "branch": entry["branch"],
        "docsPath": entry["docsPath"],
        "sourceCommit": commit,
        "syncedAt": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }
    if dry_run:
        print(f"[dry-run] Would write metadata: {meta}")
        return
    (dest / META_FILENAME).write_text(json.dumps(meta, indent=2) + "\n")


def generate_tree(root: Path) -> str:
    def should_skip(path: Path) -> bool:
        return path.name in TREE_EXCLUDES or path.name == META_FILENAME

    def entries(path: Path) -> List[Path]:
        return sorted(
            [p for p in path.iterdir() if not should_skip(p)],
            key=lambda p: (0 if p.is_dir() else 1, p.name.lower()),
        )

    lines: List[str] = ["."]

    def walk(dir_path: Path, prefix: str = "") -> None:
        children = entries(dir_path)
        for idx, child in enumerate(children):
            connector = "└── " if idx == len(children) - 1 else "├── "
            lines.append(f"{prefix}{connector}{child.name}")
            if child.is_dir():
                next_prefix = prefix + ("    " if idx == len(children) - 1 else "│   ")
                walk(child, next_prefix)

    walk(root)
    return "\n".join(lines)


def collect_meta(entries: Iterable[dict]) -> List[dict]:
    collected: List[dict] = []
    for entry in entries:
        dest = REPO_ROOT / entry["owner"] / entry["repo"] / META_FILENAME
        if dest.exists():
            collected.append(json.loads(dest.read_text()))
        else:
            collected.append({
                "owner": entry["owner"],
                "repo": entry["repo"],
                "branch": entry["branch"],
                "docsPath": entry["docsPath"],
                "sourceCommit": "-",
                "syncedAt": "-",
            })
    return collected


def write_readme(entries: List[dict]) -> None:
    tree = generate_tree(REPO_ROOT)
    meta_rows = collect_meta(entries)
    table_lines = [
        "| Mirror | Upstream | Branch | Docs Path | Last Commit | Synced At |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    if not meta_rows:
        table_lines.append("| _none_ | – | – | – | – | – |")
    else:
        for meta in meta_rows:
            mirror_name = f"{meta['owner']}/{meta['repo']}"
            upstream = f"https://github.com/{meta['owner']}/{meta['repo']}"
            table_lines.append(
                "| {mirror} | [{upstream}]({upstream}) | {branch} | {path} | {commit} | {synced} |".format(
                    mirror=mirror_name,
                    upstream=upstream,
                    branch=meta.get("branch", "-"),
                    path=meta.get("docsPath", "-"),
                    commit=meta.get("sourceCommit", "-"),
                    synced=meta.get("syncedAt", "-"),
                )
            )

    table = "\n".join(table_lines)

    schema_path = "./.github/mirrors.schema.json"
    script_path = "python3 .github/scripts/sync_mirrors.py"

    readme = f"""# Docs Mirrors

_This file is auto-generated by `scripts/sync_mirrors.py`. Do not edit manually._

## Repository Tree

```
{tree}
```

## Mirror Status

{table}

## Managing Mirrors

- Update `.github/mirrors.json` (it follows [`mirrors.schema.json`]({schema_path})) directly in the GitHub web editor or via PR to add/remove mirrors.
- Each entry requires `owner`, `repo`, `branch`, and `docsPath`.
- The daily `Sync Mirrors` workflow clones every configured docs path, refreshes this repo, and rewrites this README.
- To sync immediately, run `{script_path}` locally (use `--only owner/repo` to target a single mirror).

"""

    README_FILE.write_text(readme)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=MIRRORS_FILE,
        type=Path,
        help="Path to mirrors.json",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="OWNER/REPO",
        help="Limit syncing to specific mirrors",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch mirrors without writing to the working tree",
    )
    parser.add_argument(
        "--skip-sync",
        action="store_true",
        help="Skip cloning/updating mirrors and only regenerate README",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    targets = {
        t.lower(): t for t in args.only
    }  # preserve case for logs, compare lowercase
    processed_entries: List[dict] = []

    for entry in config:
        mirror_name = f"{entry['owner']}/{entry['repo']}"
        processed_entries.append(entry)
        if targets and mirror_name.lower() not in targets:
            continue
        if args.skip_sync:
            print(f"Skipping sync for {mirror_name} (--skip-sync enabled).")
            continue
        print(f"Syncing {mirror_name}...")
        source_dir, commit = sparse_checkout(entry)
        dest_dir = REPO_ROOT / entry["owner"] / entry["repo"]
        try:
            copy_tree(source_dir, dest_dir, dry_run=args.dry_run)
            write_meta(dest_dir, entry, commit, dry_run=args.dry_run)
        finally:
            shutil.rmtree(source_dir.parents[0], ignore_errors=True)

    write_readme(processed_entries)
    print("README.md regenerated.")


if __name__ == "__main__":
    try:
        main()
    except SyncError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
