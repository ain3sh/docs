#!/usr/bin/env python3
"""
Unified synchronization script for documentation mirrors and Gemini File Search stores.

Flow:
  1. Load configuration (mirrors.json) and state (.reference-sync)
  2. Sync mirrors in parallel (detect upstream changes)
  3. Detect changed directories for Gemini indexing
  4. Upload to Gemini in parallel
  5. Update state file and README
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set

# ============================================================================
# CONSTANTS
# ============================================================================

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = REPO_ROOT / "mirrors.json"
STATE_FILE = REPO_ROOT / ".reference-sync"
README_FILE = REPO_ROOT / "README.md"
SCHEMA_FILE = REPO_ROOT / ".github" / "mirrors.schema.json"
META_FILENAME = ".mirror-meta.json"

TREE_EXCLUDES = {
    ".git",
    ".github",
    "search-context",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}

GEMINI_SUPPORTED_EXTENSIONS = {
    ".md",
    ".mdx",
    ".txt",
    ".py",
    ".js",
    ".json",
    ".ts",
    ".tsx",
    ".jsx",
    ".rst",
    ".pdf",
}

MIN_FILE_SIZE = 10
GEMINI_COST_PER_MILLION_TOKENS = 0.15  # Gemini File Search indexing cost

# ============================================================================
# ERROR HANDLING
# ============================================================================


class SyncError(RuntimeError):
    """Raised when a sync operation cannot be completed."""


# ============================================================================
# UTILITIES
# ============================================================================


def run(cmd: List[str], *, cwd: Path | None = None) -> str:
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


def get_current_commit() -> str:
    """Get current HEAD commit SHA."""
    return run(["git", "rev-parse", "HEAD"])


def format_timestamp() -> str:
    """Return current UTC timestamp in ISO format."""
    # RFC 3339, Z-normalized (no redundant "+00:00Z")
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def stable_json_hash(value: object) -> str:
    """Compute a stable hash for JSON-serializable values."""
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ============================================================================
# CONFIGURATION & STATE
# ============================================================================


def load_config() -> dict:
    """Load and validate mirrors.json."""
    if not CONFIG_FILE.exists():
        raise SyncError(f"Missing config file: {CONFIG_FILE}")

    data = json.loads(CONFIG_FILE.read_text())

    # Validate structure
    if not isinstance(data, dict):
        raise SyncError("mirrors.json must be an object")

    if "mirrors" not in data:
        raise SyncError("mirrors.json must have a 'mirrors' key")

    mirrors = data["mirrors"]
    if not isinstance(mirrors, list):
        raise SyncError("mirrors.json['mirrors'] must be a list")

    for entry in mirrors:
        if not isinstance(entry, dict):
            raise SyncError("Each mirror entry must be an object")
        for key in ("owner", "repo", "branch", "docsPath"):
            if key not in entry:
                raise SyncError(f"Mirror entry missing '{key}' field: {entry}")

    # Validate against schema if available
    if SCHEMA_FILE.exists():
        try:
            import jsonschema

            schema = json.loads(SCHEMA_FILE.read_text())
            jsonschema.validate(data, schema)
        except ImportError:
            print("  ℹ️  jsonschema not installed, skipping validation", file=sys.stderr)
        except Exception as e:
            print(f"  ⚠️  Schema validation warning: {e}", file=sys.stderr)

    return data


def load_state() -> dict:
    """Load .reference-sync state file with unified stores structure."""
    empty_state = {"lastSync": None, "lastCommit": None, "stores": {}}

    if not STATE_FILE.exists():
        return empty_state

    try:
        data = json.loads(STATE_FILE.read_text())
    except Exception as e:
        print(f"  ⚠️  Warning: Could not load state file: {e}", file=sys.stderr)
        print("  Starting with fresh state", file=sys.stderr)
        return empty_state

    # Already in unified format
    if "stores" in data and "mirrors" not in data and "gemini_stores" not in data:
        return data

    # Migrate from flat mirrors + gemini_stores to unified stores
    if "mirrors" in data or "gemini_stores" in data:
        print("  📦 Migrating to unified stores structure...")
        stores = {}
        old_mirrors = data.get("mirrors", {})
        old_gemini = data.get("gemini_stores", {})

        # Merge mirror and gemini data by store ID
        all_ids = set(old_mirrors.keys()) | set(old_gemini.keys())
        for store_id in all_ids:
            mirror_data = old_mirrors.get(store_id, {})
            gemini_data = old_gemini.get(store_id, {})
            stores[store_id] = {
                "commit": mirror_data.get("lastCommit"),
                "synced": mirror_data.get("lastSync"),
                "status": mirror_data.get("status"),
                "gemini": {
                    "files": gemini_data.get("files", 0),
                    "cost": gemini_data.get("cost", 0.0),
                    "synced": gemini_data.get("lastSync"),
                    "status": gemini_data.get("status"),
                } if gemini_data else None,
            }

        return {
            "lastSync": data.get("lastSync"),
            "lastCommit": data.get("lastCommit"),
            "stores": stores,
        }

    # Migrate from old "owners" structure
    if "owners" in data:
        print("  📦 Migrating from owners structure...")
        stores = {}
        owners_data = data.get("owners", {})

        for owner, owner_data in owners_data.items():
            for repo, mirror_data in owner_data.get("mirrors", {}).items():
                store_id = f"{owner}/{repo}"
                gemini_data = owner_data.get("gemini")
                stores[store_id] = {
                    "commit": mirror_data.get("commit"),
                    "synced": mirror_data.get("synced"),
                    "status": mirror_data.get("status"),
                    "gemini": gemini_data,
                }

        return {
            "lastSync": data.get("lastSync"),
            "lastCommit": data.get("lastCommit"),
            "stores": stores,
        }

    return empty_state


def save_state(state: dict) -> None:
    """Save .reference-sync state file."""
    state["lastSync"] = format_timestamp()
    state["lastCommit"] = get_current_commit()
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


# ============================================================================
# MIRROR SYNC OPERATIONS
# ============================================================================


def get_upstream_commit(owner: str, repo: str, branch: str) -> str:
    """Get latest commit SHA from upstream using git ls-remote."""
    repo_url = f"https://github.com/{owner}/{repo}.git"
    token = os.getenv("MIRROR_GIT_TOKEN")
    if token:
        repo_url = f"https://{token}@github.com/{owner}/{repo}.git"

    try:
        output = run(["git", "ls-remote", repo_url, f"refs/heads/{branch}"])
        if not output:
            raise SyncError(f"Branch {branch} not found in {owner}/{repo}")
        commit_sha = output.split()[0]
        return commit_sha
    except SyncError:
        raise
    except Exception as e:
        raise SyncError(f"Failed to get upstream commit for {owner}/{repo}@{branch}: {e}") from e


def sparse_checkout(entry: dict) -> tuple[Path, str]:
    """Perform sparse checkout of a repository's docs path."""
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
            raise SyncError(f"Docs path '{docs_path}' not found in {owner}/{repo}@{branch}")
        commit = run(["git", "rev-parse", "HEAD"], cwd=checkout_dir)
        return source_dir, commit
    except SyncError:
        shutil.rmtree(checkout_dir, ignore_errors=True)
        raise
    except Exception as e:
        shutil.rmtree(checkout_dir, ignore_errors=True)
        raise SyncError(f"Failed to checkout {owner}/{repo}@{branch}") from e


def copy_tree(src: Path, dest: Path) -> None:
    """Copy directory tree and clean up stale files."""
    dest.mkdir(parents=True, exist_ok=True)
    tracked_files = set()

    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if path.is_dir():
            (dest / rel).mkdir(parents=True, exist_ok=True)
            continue
        tracked_files.add(rel)
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)

    # Clean up stale files
    if dest.exists():
        for path in sorted(dest.rglob("*"), reverse=True):
            if path.name == META_FILENAME:
                continue
            rel = path.relative_to(dest)
            if path.is_file() and rel not in tracked_files:
                path.unlink()
            elif path.is_dir() and not any(path.iterdir()):
                path.rmdir()


def write_mirror_meta(dest: Path, entry: dict, commit: str) -> None:
    """Write .mirror-meta.json for a mirror."""
    meta = {
        "owner": entry["owner"],
        "repo": entry["repo"],
        "branch": entry["branch"],
        "docsPath": entry["docsPath"],
        "sourceCommit": commit,
        "syncedAt": format_timestamp(),
    }
    (dest / META_FILENAME).write_text(json.dumps(meta, indent=2) + "\n")


def sync_mirror(entry: dict, state: dict) -> dict:
    """
    Sync a single mirror.
    Returns dict with keys: status, commit, changed
    """
    owner = entry["owner"]
    repo = entry["repo"]
    mirror_id = f"{owner}/{repo}"

    # Check if upstream changed
    try:
        upstream_commit = get_upstream_commit(owner, repo, entry["branch"])
    except SyncError as e:
        print(f"  ⚠️  {mirror_id}: {e}", file=sys.stderr)
        return {"status": "failed", "error": str(e), "changed": False}

    # Mirror configuration and local state must match mirrors.json (branch/docsPath)
    last = state.get("stores", {}).get(mirror_id, {})
    last_commit = last.get("commit")
    last_branch = last.get("branch")
    last_docs_path = last.get("docsPath")
    dest_dir = REPO_ROOT / owner / repo

    config_changed = (
        last_branch != entry.get("branch") or last_docs_path != entry.get("docsPath")
    )
    dest_missing = not dest_dir.exists()

    if upstream_commit == last_commit and not config_changed and not dest_missing:
        return {"status": "unchanged", "commit": upstream_commit, "changed": False}

    # Perform sync
    try:
        source_dir, commit = sparse_checkout(entry)
        try:
            copy_tree(source_dir, dest_dir)
            write_mirror_meta(dest_dir, entry, commit)
        finally:
            shutil.rmtree(source_dir.parent, ignore_errors=True)

        return {"status": "success", "commit": commit, "changed": True}
    except Exception as e:
        print(f"  ❌ {mirror_id}: {e}", file=sys.stderr)
        return {"status": "failed", "error": str(e), "changed": False}


def sync_all_mirrors(mirrors: List[dict], state: dict, *, parallel: bool = True) -> Dict[str, dict]:
    """Sync all mirrors, optionally in parallel."""
    print(f"\n{'='*60}")
    print(f"🔄 SYNCING {len(mirrors)} MIRRORS")
    print(f"{'='*60}")

    results = {}

    if parallel:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(sync_mirror, mirror, state): mirror for mirror in mirrors}

            for future in as_completed(futures):
                mirror = futures[future]
                mirror_id = f"{mirror['owner']}/{mirror['repo']}"
                try:
                    result = future.result()
                    results[mirror_id] = result
                    status_icon = {"success": "✅", "unchanged": "⏭️", "failed": "❌"}.get(
                        result["status"], "❓"
                    )
                    print(f"  {status_icon} {mirror_id}")
                except Exception as e:
                    print(f"  ❌ {mirror_id}: {e}")
                    results[mirror_id] = {"status": "failed", "error": str(e), "changed": False}
    else:
        for mirror in mirrors:
            mirror_id = f"{mirror['owner']}/{mirror['repo']}"
            print(f"  Syncing {mirror_id}...")
            result = sync_mirror(mirror, state)
            results[mirror_id] = result
            status_icon = {"success": "✅", "unchanged": "⏭️", "failed": "❌"}.get(
                result["status"], "❓"
            )
            print(f"  {status_icon} {mirror_id}")

    return results


# ============================================================================
# GEMINI STORE DETECTION
# ============================================================================


def is_excluded(path: str, exclusions: List[str]) -> bool:
    """Check if path matches any exclusion pattern."""
    for pattern in exclusions:
        # Exact match
        if path == pattern:
            return True
        # Prefix match (pattern/*)
        if pattern.endswith("/*"):
            prefix = pattern[:-2]
            if path.startswith(prefix + "/") or path == prefix:
                return True
        # Simple prefix match (for patterns like "temp")
        if path.startswith(pattern + "/") or path == pattern:
            return True
    return False


def get_valid_mirror_ids(mirrors: List[dict]) -> Set[str]:
    """Get the set of valid mirror IDs (owner/repo format) from config."""
    return {f"{m['owner']}/{m['repo']}" for m in mirrors}


def cleanup_stale_mirror_directories(valid_mirror_ids: Set[str]) -> List[str]:
    """Remove local mirror directories that are no longer present in mirrors.json.

    Safety: only removes directories that contain a .mirror-meta.json file, since those
    are explicitly managed by this sync workflow.
    """
    removed: List[str] = []

    for owner_dir in REPO_ROOT.iterdir():
        if not owner_dir.is_dir() or owner_dir.name.startswith("."):
            continue
        if owner_dir.name in TREE_EXCLUDES:
            continue

        for repo_dir in owner_dir.iterdir():
            if not repo_dir.is_dir() or repo_dir.name.startswith("."):
                continue

            mirror_meta = repo_dir / META_FILENAME
            if not mirror_meta.exists():
                continue

            mirror_id = f"{owner_dir.name}/{repo_dir.name}"
            if mirror_id in valid_mirror_ids:
                continue

            print(f"  🧹 Removing stale mirror directory: {mirror_id}")
            shutil.rmtree(repo_dir, ignore_errors=True)
            removed.append(mirror_id)

        # Clean up empty owner directories (only if they became empty)
        try:
            if owner_dir.exists() and not any(owner_dir.iterdir()):
                owner_dir.rmdir()
        except OSError:
            pass

    return removed


def determine_stores_to_index(
    *,
    mirrors: List[dict],
    state: dict,
    mirror_results: Dict[str, dict],
    gemini_exclusions: List[str],
) -> List[str]:
    """Decide which mirror stores require (re)indexing.

    mirrors.json is the source of truth.

    Index when:
      - a mirror was updated in this run, or
      - the store has never been indexed successfully, or
      - geminiExclusions changed since last run (forces a full reindex).
    """

    valid_ids = get_valid_mirror_ids(mirrors)

    exclusions_hash = stable_json_hash(gemini_exclusions)
    previous_hash = state.get("geminiExclusionsHash")
    if previous_hash == exclusions_hash:
        exclusions_changed = False
    elif previous_hash is None:
        # If we have existing successful indexes but no recorded hash, play it safe
        # and rebuild once to ensure exclusions are applied.
        has_any_index = any(
            (s.get("gemini") or {}).get("status") == "success"
            for s in state.get("stores", {}).values()
        )
        exclusions_changed = has_any_index
    else:
        exclusions_changed = True

    changed_mirrors = {
        mirror_id
        for mirror_id, result in mirror_results.items()
        if result.get("status") == "success" and result.get("changed") is True
    }

    needs_first_index = {
        store_id
        for store_id in valid_ids
        if (state.get("stores", {}).get(store_id, {}) or {}).get("gemini") is None
        or ((state.get("stores", {}).get(store_id, {}) or {}).get("gemini") or {}).get("status") != "success"
    }

    if exclusions_changed:
        print("  🔁 geminiExclusions changed - forcing full reindex")
        return sorted(valid_ids)

    return sorted(changed_mirrors | needs_first_index)


# ============================================================================
# GEMINI SYNC OPERATIONS
# ============================================================================


def should_process_file(file_path: Path) -> bool:
    """Check if a file should be uploaded to Gemini."""
    if file_path.suffix.lower() not in GEMINI_SUPPORTED_EXTENSIONS:
        return False

    try:
        size = file_path.stat().st_size
    except OSError:
        return False

    if size < MIN_FILE_SIZE:
        return False

    # Skip nearly-empty __init__.py files
    if file_path.name == "__init__.py" and size < 100:
        return False

    return True


def prepare_file_for_upload(file_path: Path, *, store_dir: Path, temp_dir: Path) -> tuple[Path, str]:
    """Prepare file for upload.

    - Uses the store-relative path as the display name (so citations match the repo).
    - Converts `.mdx` to `.md` for upload to ensure markdown parsing, while preserving
      the original `.mdx` display name.
    """
    rel = file_path.relative_to(store_dir)
    display_name = rel.as_posix()

    if file_path.suffix.lower() == ".mdx":
        upload_rel = rel.with_suffix(".md")
        upload_path = temp_dir / upload_rel
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, upload_path)
        return upload_path, display_name

    return file_path, display_name


def sync_gemini_store(
    client,
    store_name: str,
    stores_by_display: dict,
    gemini_exclusions: List[str],
) -> dict:
    """
    Sync a single Gemini FileSearchStore.
    Returns dict with keys: status, files, cost, lastSync
    """
    from google.genai import types

    print(f"\n{'='*60}")
    print(f"📤 Processing store: {store_name}")
    print(f"{'='*60}")

    # Delete any existing stores with this display name (dedupe + ensure correctness)
    existing_stores = stores_by_display.get(store_name, [])
    if existing_stores:
        for existing_store in existing_stores:
            try:
                print(f"  Deleting existing store: {existing_store.name}")
                client.file_search_stores.delete(
                    name=existing_store.name,
                    config=types.DeleteFileSearchStoreConfig(force=True)
                )
            except Exception as e:
                print(f"  ⚠️  Error deleting store: {e}", file=sys.stderr)
        time.sleep(2)  # Allow backend cleanup

    # Create new store
    try:
        store = client.file_search_stores.create(
            config=types.CreateFileSearchStoreConfig(display_name=store_name)
        )
        print(f"  ✅ Created store: {store.name} (display: {store_name})")
    except Exception as e:
        print(f"  ❌ Failed to create store: {e}", file=sys.stderr)
        return {"status": "failed", "error": str(e)}

    # Verify the store was actually created
    try:
        verified = client.file_search_stores.get(name=store.name)
        if not verified:
            print(f"  ❌ Store verification failed: store not found after creation")
            return {"status": "failed", "error": "Store creation not verified"}
        print(f"  ✅ Store verified: {verified.display_name}")
    except Exception as e:
        print(f"  ⚠️  Could not verify store (continuing anyway): {e}", file=sys.stderr)

    # Collect files
    store_dir = REPO_ROOT / store_name
    if not store_dir.exists():
        print(f"  ⚠️  Store directory does not exist: {store_dir}")
        return {"status": "failed", "error": "Directory not found"}

    files = []
    skipped = 0

    for file_path in store_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.name.startswith(".") or file_path.name == META_FILENAME:
            skipped += 1
            continue
        rel = file_path.relative_to(store_dir).as_posix()
        if is_excluded(rel, gemini_exclusions):
            skipped += 1
            continue
        if should_process_file(file_path):
            files.append(file_path)
        else:
            skipped += 1

    print(f"  Found {len(files)} files to upload (skipped {skipped})")

    if not files:
        return {"status": "success", "files": 0, "cost": 0.0, "lastSync": format_timestamp()}

    # Upload files in parallel
    operations = []
    total_tokens = 0
    failed_uploads = []

    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)

        def upload_one(fp: Path):
            try:
                up_path, display_name = prepare_file_for_upload(
                    fp,
                    store_dir=store_dir,
                    temp_dir=tmp_dir,
                )
                size = up_path.stat().st_size
                est_tokens = size // 4
                op = client.file_search_stores.upload_to_file_search_store(
                    file=str(up_path),
                    file_search_store_name=store.name,
                    config=types.UploadToFileSearchStoreConfig(
                        display_name=display_name,
                    ),
                )
                return (op, est_tokens, fp, None)
            except Exception as ex:
                return (None, 0, fp, str(ex))

        print("  Uploading files...")
        with ThreadPoolExecutor(max_workers=10) as pool:
            futures = {pool.submit(upload_one, f): f for f in files}
            for i, fut in enumerate(as_completed(futures), 1):
                op, tokens, fp, err = fut.result()
                if err:
                    failed_uploads.append((fp.name, err))
                    if len(failed_uploads) <= 3:
                        print(f"    ❌ [{i}/{len(files)}] {fp.name}: {err}")
                else:
                    operations.append(op)
                    total_tokens += tokens
                    if i % 20 == 0 or i == len(files):
                        print(f"    ✅ [{i}/{len(files)}] queued")

    # Wait for operations to complete
    if operations:
        print(f"  Waiting for {len(operations)} uploads to complete...")
        completed = 0
        start = time.time()
        max_wait = 600

        while completed < len(operations):
            if time.time() - start > max_wait:
                print(f"  ⚠️  Timeout: {completed}/{len(operations)} completed")
                break

            newly_completed = 0
            for idx, op in enumerate(operations):
                if not getattr(op, "done", False):
                    try:
                        operations[idx] = client.operations.get(op)
                        if getattr(operations[idx], "done", False):
                            newly_completed += 1
                    except Exception as e:
                        print(f"    ⚠️  Failed to poll operation {idx}: {e}", file=sys.stderr)
                        # Continue polling other operations

            if newly_completed:
                completed += newly_completed
                print(f"    [{completed}/{len(operations)}] completed")

            if completed < len(operations):
                time.sleep(2)

    cost = (total_tokens / 1_000_000) * GEMINI_COST_PER_MILLION_TOKENS

    print(f"  ✅ Store sync complete:")
    print(f"     Files indexed: {len(operations)}")
    print(f"     Estimated tokens: {total_tokens:,}")
    print(f"     Cost: ${cost:.4f}")

    if failed_uploads:
        print(f"     Failed uploads: {len(failed_uploads)}")

    return {
        "status": "success",
        "files": len(operations),
        "cost": cost,
        "lastSync": format_timestamp(),
    }


def sync_gemini_stores(
    stores_to_sync: List[str],
    valid_stores: Set[str],
    gemini_exclusions: List[str],
) -> dict:
    """Sync changed stores and clean up stale stores from Gemini."""
    print(f"\n{'='*60}")
    print(f"🚀 SYNCING {len(stores_to_sync)} GEMINI STORES")
    print(f"{'='*60}")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  ⚠️  GEMINI_API_KEY not set, skipping Gemini sync", file=sys.stderr)
        return {
            "storesUpdated": 0,
            "filesUploaded": 0,
            "totalCost": 0.0,
            "lastSync": format_timestamp(),
            "stores": {},
        }

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
    except ImportError:
        print("  ⚠️  google-genai not installed, skipping Gemini sync", file=sys.stderr)
        return {
            "storesUpdated": 0,
            "filesUploaded": 0,
            "totalCost": 0.0,
            "lastSync": format_timestamp(),
            "stores": {},
        }
    except Exception as e:
        print(f"  ❌ Failed to initialize Gemini client: {e}", file=sys.stderr)
        return {
            "storesUpdated": 0,
            "filesUploaded": 0,
            "totalCost": 0.0,
            "lastSync": format_timestamp(),
            "stores": {},
        }

    # Fetch existing stores
    print("  Fetching existing stores...")
    try:
        existing = list(
            client.file_search_stores.list(
                config=types.ListFileSearchStoresConfig(page_size=20)
            )
        )
        stores_by_display: Dict[str, list] = {}
        for s in existing:
            if not getattr(s, "display_name", None):
                continue
            stores_by_display.setdefault(s.display_name, []).append(s)
        print(f"  Found {len(existing)} existing stores")
    except Exception as e:
        print(f"  ⚠️  Could not list stores: {e}", file=sys.stderr)
        stores_by_display = {}

    # Delete stale stores not in valid_stores
    stale_store_names = set(stores_by_display.keys()) - valid_stores
    if stale_store_names:
        print(f"  🧹 Deleting {len(stale_store_names)} stale Gemini stores: {', '.join(sorted(stale_store_names))}")
        for store_name in sorted(stale_store_names):
            try:
                for store in stores_by_display.get(store_name, []):
                    print(f"    Deleting {store_name} ({store.name})...")
                    client.file_search_stores.delete(
                        name=store.name,
                        config=types.DeleteFileSearchStoreConfig(force=True)
                    )
                stores_by_display.pop(store_name, None)
            except Exception as e:
                print(f"    ❌ Failed to delete {store_name}: {e}", file=sys.stderr)

    # If duplicates exist for a valid display name, delete them all and force a reindex.
    forced_reindex: Set[str] = set()
    for display_name, stores in list(stores_by_display.items()):
        if display_name in valid_stores and len(stores) > 1:
            forced_reindex.add(display_name)
            print(f"  🧹 {display_name}: {len(stores)} duplicate stores found; deleting and rebuilding")
            for store in stores:
                try:
                    client.file_search_stores.delete(
                        name=store.name,
                        config=types.DeleteFileSearchStoreConfig(force=True)
                    )
                except Exception as e:
                    print(f"    ❌ Failed to delete duplicate {store.name}: {e}", file=sys.stderr)
            stores_by_display[display_name] = []

    stores_to_sync = sorted(set(stores_to_sync) | forced_reindex)

    # Sync each store in parallel
    results = {}
    total_files = 0
    total_cost = 0.0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(sync_gemini_store, client, store_name, stores_by_display, gemini_exclusions): store_name
            for store_name in stores_to_sync
        }

        for future in as_completed(futures):
            store_name = futures[future]
            try:
                result = future.result()
                results[store_name] = result

                if result.get("status") == "success":
                    total_files += result.get("files", 0)
                    total_cost += result.get("cost", 0.0)
                    print(f"  ✅ {store_name}: {result.get('files', 0)} files, ${result.get('cost', 0.0):.4f}")
            except Exception as e:
                print(f"  ❌ {store_name}: {e}", file=sys.stderr)
                results[store_name] = {"status": "failed", "error": str(e)}

    successful = sum(1 for r in results.values() if r.get("status") == "success")

    print(f"\n{'='*60}")
    print("✅ GEMINI SYNC COMPLETE")
    print(f"  Stores updated: {successful}/{len(stores_to_sync)}")
    print(f"  Files uploaded: {total_files}")
    print(f"  Total cost: ${total_cost:.4f}")
    print(f"{'='*60}")

    return {
        "storesUpdated": successful,
        "filesUploaded": total_files,
        "totalCost": total_cost,
        "lastSync": format_timestamp(),
        "stores": results,
    }


# ============================================================================
# README GENERATION
# ============================================================================


def generate_tree(root: Path, mirrors: List[dict]) -> str:
    """Generate tree visualization of repository."""

    def should_skip(path: Path) -> bool:
        return path.name in TREE_EXCLUDES or path.name == META_FILENAME

    mirror_pairs = {(m["owner"], m["repo"]) for m in mirrors}

    def entries(path: Path) -> List[Path]:
        return sorted(
            [p for p in path.iterdir() if not should_skip(p)],
            key=lambda p: (0 if p.is_dir() else 1, p.name.lower()),
        )

    lines = ["."]

    def walk(dir_path: Path, prefix: str = "") -> None:
        children = entries(dir_path)
        for idx, child in enumerate(children):
            connector = "└── " if idx == len(children) - 1 else "├── "
            lines.append(f"{prefix}{connector}{child.name}")
            if child.is_dir():
                rel_parts = child.relative_to(root).parts
                mirror_repo = rel_parts[:2]
                is_mirror_child = (
                    len(rel_parts) >= 3
                    and len(mirror_repo) == 2
                    and (mirror_repo[0], mirror_repo[1]) in mirror_pairs
                )
                if is_mirror_child:
                    continue
                next_prefix = prefix + ("    " if idx == len(children) - 1 else "│   ")
                walk(child, next_prefix)

    walk(root)
    return "\n".join(lines)


def collect_mirror_metadata(mirrors: List[dict]) -> List[dict]:
    """Collect metadata for all mirrors."""
    collected = []
    for mirror in mirrors:
        dest = REPO_ROOT / mirror["owner"] / mirror["repo"] / META_FILENAME
        if dest.exists():
            collected.append(json.loads(dest.read_text()))
        else:
            collected.append(
                {
                    "owner": mirror["owner"],
                    "repo": mirror["repo"],
                    "branch": mirror["branch"],
                    "docsPath": mirror["docsPath"],
                    "sourceCommit": "-",
                    "syncedAt": "-",
                }
            )
    return collected


def update_readme(config: dict, state: dict) -> None:
    """Generate and update only dynamic sections of README.md."""
    mirrors = config["mirrors"]
    tree = generate_tree(REPO_ROOT, mirrors)
    meta_rows = collect_mirror_metadata(mirrors)

    # Build mirror status table
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
            commit = meta.get("sourceCommit", "-")
            if commit != "-" and len(commit) > 7:
                commit = commit[:7]
            table_lines.append(
                f"| {mirror_name} | [{upstream}]({upstream}) | "
                f"{meta.get('branch', '-')} | {meta.get('docsPath', '-')} | "
                f"{commit} | {meta.get('syncedAt', '-')} |"
            )

    table = "\n".join(table_lines)

    # Build Gemini stats from unified stores structure
    stores_with_gemini = [s for s in state.get("stores", {}).values() if s.get("gemini")]
    total_files = sum(s["gemini"].get("files", 0) for s in stores_with_gemini)
    total_cost = sum(s["gemini"].get("cost", 0.0) for s in stores_with_gemini)
    stores_count = len(stores_with_gemini)
    last_sync = state.get("lastSync", "Never")
    gemini_section = f"""- **Stores**: {stores_count}
- **Files indexed**: {total_files}
- **Total cost**: ${total_cost:.4f}
- **Last sync**: {last_sync}"""

    # Read existing README or create template
    if README_FILE.exists():
        content = README_FILE.read_text()
    else:
        content = """# Documentation References

<!-- AUTO:MIRROR_STATUS -->
<!-- /AUTO:MIRROR_STATUS -->

<!-- AUTO:SEMANTIC_SEARCH -->
<!-- /AUTO:SEMANTIC_SEARCH -->

<!-- AUTO:REPOSITORY_TREE -->
<!-- /AUTO:REPOSITORY_TREE -->

## Managing Mirrors

- Update `mirrors.json` (validated against [`.github/mirrors.schema.json`](./.github/mirrors.schema.json))
- Each entry requires `owner`, `repo`, `branch`, and `docsPath`
- Optional `geminiExclusions` array to exclude directories from semantic search indexing
- Daily sync workflow runs at 3 AM UTC
- Manual trigger available via GitHub Actions

## Configuration

Add exclusion patterns to `mirrors.json`:

```json
{
  "geminiExclusions": [
    "archived",
    "temp/*",
    "build"
  ]
}

"""

    # Replace dynamic sections only
    content = re.sub(
        r'<!-- AUTO:MIRROR_STATUS -->.*?<!-- /AUTO:MIRROR_STATUS -->',
        f'<!-- AUTO:MIRROR_STATUS -->\n## Mirror Status\n\n{table}\n<!-- /AUTO:MIRROR_STATUS -->',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'<!-- AUTO:SEMANTIC_SEARCH -->.*?<!-- /AUTO:SEMANTIC_SEARCH -->',
        f'<!-- AUTO:SEMANTIC_SEARCH -->\n## Semantic Search\n\nThis repository includes automated indexing for Gemini File Search API.\n\n{gemini_section}\n\nUse the [search-context MCP server](https://github.com/ain3sh/search-context) to query these docs semantically.\n<!-- /AUTO:SEMANTIC_SEARCH -->',
        content,
        flags=re.DOTALL
    )
    
    content = re.sub(
        r'<!-- AUTO:REPOSITORY_TREE -->.*?<!-- /AUTO:REPOSITORY_TREE -->',
        f'<!-- AUTO:REPOSITORY_TREE -->\n## Repository Tree\n\n```\n{tree}\n```\n<!-- /AUTO:REPOSITORY_TREE -->',
        content,
        flags=re.DOTALL
    )
    
    README_FILE.write_text(content)
    print(f"\n✅ README.md updated (preserved manual edits)")


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-mirrors",
        action="store_true",
        help="Skip mirror sync (only update Gemini stores and README)",
    )
    parser.add_argument(
        "--skip-gemini",
        action="store_true",
        help="Skip Gemini store sync (only sync mirrors and README)",
    )
    parser.add_argument(
        "--only-mirror",
        action="append",
        default=[],
        metavar="OWNER/REPO",
        help="Limit mirror sync to specific mirrors",
    )
    parser.add_argument(
        "--no-parallel",
        action="store_true",
        help="Disable parallel processing (useful for debugging)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("=" * 60)
    print("📚 DOCUMENTATION REFERENCE SYNC")
    print("=" * 60)

    # Load configuration and state
    config = load_config()
    state = load_state()

    mirrors = config["mirrors"]
    gemini_exclusions = config.get("geminiExclusions", [])

    # Filter mirrors if requested
    if args.only_mirror:
        targets = {t.lower(): t for t in args.only_mirror}
        mirrors = [
            m
            for m in mirrors
            if f"{m['owner']}/{m['repo']}".lower() in targets
        ]
        print(f"  Limiting to {len(mirrors)} mirror(s)")

    # Get valid mirror IDs (owner/repo format) from config
    valid_mirror_ids = get_valid_mirror_ids(mirrors)
    mirror_config_by_id = {f"{m['owner']}/{m['repo']}": m for m in mirrors}

    # Ensure stores dict exists
    if "stores" not in state:
        state["stores"] = {}

    # Step 1: Sync mirrors
    if not args.skip_mirrors:
        mirror_results = sync_all_mirrors(mirrors, state, parallel=not args.no_parallel)

        # Update state with new results (unified stores structure)
        for mirror_id, result in mirror_results.items():
            if result["status"] in ("success", "unchanged"):
                if mirror_id not in state["stores"]:
                    state["stores"][mirror_id] = {"gemini": None}
                mirror_cfg = mirror_config_by_id.get(mirror_id, {})
                state["stores"][mirror_id]["commit"] = result["commit"]
                state["stores"][mirror_id]["branch"] = mirror_cfg.get("branch")
                state["stores"][mirror_id]["docsPath"] = mirror_cfg.get("docsPath")
                state["stores"][mirror_id]["synced"] = format_timestamp()
                state["stores"][mirror_id]["status"] = result["status"]
    else:
        print("\n⏭️  Skipping mirror sync (--skip-mirrors)")
        mirror_results = {}

    # Filter out stale stores not in mirrors.json
    existing_stores = set(state.get("stores", {}).keys())
    stale_stores = existing_stores - valid_mirror_ids
    if stale_stores:
        print(f"  🧹 Removing {len(stale_stores)} stale stores from state: {', '.join(sorted(stale_stores))}")
        for store_id in stale_stores:
            del state["stores"][store_id]

    # Remove stale mirror directories on disk (those no longer in mirrors.json)
    removed_dirs = cleanup_stale_mirror_directories(valid_mirror_ids)
    if removed_dirs:
        print(f"  ✅ Removed {len(removed_dirs)} stale mirror director(ies)")

    # Step 2: Detect and sync Gemini stores
    if not args.skip_gemini:
        stores_to_sync = determine_stores_to_index(
            mirrors=mirrors,
            state=state,
            mirror_results=mirror_results,
            gemini_exclusions=gemini_exclusions,
        )

        # Always run sync to cleanup stale stores, even if no changes detected
        gemini_results = sync_gemini_stores(
            stores_to_sync,
            valid_mirror_ids,
            gemini_exclusions,
        )

        # Record exclusions hash only when we attempted Gemini sync
        state["geminiExclusionsHash"] = stable_json_hash(gemini_exclusions)

        # Update gemini info in unified stores structure
        for store_name, store_data in gemini_results.get("stores", {}).items():
            if store_name not in state["stores"]:
                state["stores"][store_name] = {}
            state["stores"][store_name]["gemini"] = {
                "files": store_data.get("files", 0),
                "cost": store_data.get("cost", 0.0),
                "synced": store_data.get("lastSync", format_timestamp()),
                "status": store_data.get("status", "unknown"),
            }
    else:
        print("\n⏭️  Skipping Gemini sync (--skip-gemini)")

    # Compute aggregate stats for summary
    total_files = sum(
        s.get("gemini", {}).get("files", 0) for s in state.get("stores", {}).values()
        if s.get("gemini")
    )
    total_cost = sum(
        s.get("gemini", {}).get("cost", 0.0) for s in state.get("stores", {}).values()
        if s.get("gemini")
    )

    # Step 3: Update state and README
    save_state(state)
    update_readme(config, state)

    # Summary
    print(f"\n{'='*60}")
    print("✅ SYNC COMPLETE")
    print(f"{'='*60}")
    if not args.skip_mirrors:
        success_count = sum(1 for r in mirror_results.values() if r["status"] == "success")
        unchanged_count = sum(1 for r in mirror_results.values() if r["status"] == "unchanged")
        print(f"  Mirrors synced: {success_count} updated, {unchanged_count} unchanged")
    if not args.skip_gemini:
        stores_count = sum(1 for s in state.get("stores", {}).values() if s.get("gemini"))
        print(f"  Gemini stores: {stores_count}")
        print(f"  Total files indexed: {total_files}")
        print(f"  Total cost: ${total_cost:.4f}")
    print(f"{'='*60}")


if __name__ == "__main__":
    try:
        main()
    except SyncError as exc:
        print(f"\n❌ Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as exc:
        print(f"\n❌ Unexpected error: {exc}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)
