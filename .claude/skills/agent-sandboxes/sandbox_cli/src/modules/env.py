"""
Environment file sync module.
Handles syncing .env files between local envs/ folder and sandbox.

1Password Environments Compatibility
-------------------------------------
This module supports 1Password Environments, which mounts .env files as UNIX
named pipes (FIFOs) rather than regular files. Key considerations:

1. Detection: Use is_readable_env_path() instead of Path.is_file(), since
   FIFOs return False for is_file().

2. Reading: FIFOs require special handling:
   - For parsed key-values: use read_env_file_vars() (python-dotenv >= 1.1.2)
   - For raw content: use read_env_file_content() (subprocess cat)

3. Single-read behavior: 1Password FIFOs can only be read ONCE per authorization
   cycle. After reading, the data is consumed until 1Password re-authorizes.
   This is why push (needs raw content) and diff (needs parsed vars) use
   separate read functions - they're different commands, never called together
   on the same file in the same invocation.

See: https://developer.1password.com/docs/environments/local-env-file
"""

import subprocess
from pathlib import Path
from typing import Dict, List

from dotenv import dotenv_values
from e2b import Sandbox


# Base path in sandbox where projects live
SANDBOX_BASE_PATH = "/home/user"

# Files to ignore when syncing (examples/templates, not real secrets)
IGNORED_ENV_PATTERNS = {
    ".env.example",
    ".env.sample",
    ".env.template",
    ".env.defaults",
    ".env.dist",
}


def is_env_file(name: str) -> bool:
    """
    Check if a filename is a valid .env file to sync.

    Matches: .env, .env.local, .env.production, .env.development, etc.
    Ignores: .env.example, .env.sample, .env.template, etc.

    Args:
        name: Filename to check

    Returns:
        True if this is an env file we should sync
    """
    if not name.startswith(".env"):
        return False

    # Check against ignored patterns
    name_lower = name.lower()
    for pattern in IGNORED_ENV_PATTERNS:
        if name_lower == pattern:
            return False

    return True


def parse_env_file(content: str) -> Dict[str, str]:
    """
    Parse .env file content into key-value pairs.

    Args:
        content: Raw .env file content

    Returns:
        Dictionary of environment variable names to values
    """
    env_vars = {}
    for line in content.splitlines():
        line = line.strip()
        # Skip empty lines and comments
        if not line or line.startswith("#"):
            continue
        # Handle KEY=VALUE (with optional quotes)
        if "=" in line:
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Remove surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            env_vars[key] = value
    return env_vars


def is_readable_env_path(path: Path) -> bool:
    """
    Check if a path is a readable env file (regular file or FIFO).

    1Password Environments mounts .env files as FIFOs (named pipes),
    which return False for is_file(). We need to check for both.

    Args:
        path: Path to check

    Returns:
        True if path exists and is readable (file or FIFO)
    """
    return path.exists() and (path.is_file() or path.is_fifo())


def read_env_file_content(path: Path) -> str:
    """
    Read raw content from an env file, supporting both regular files and FIFOs.

    1Password Environments mounts .env files as FIFOs. Standard Python file I/O
    doesn't work with these - we use subprocess to read via cat.

    Args:
        path: Path to the env file

    Returns:
        Raw file content as string
    """
    # Use cat for both regular files and FIFOs - works universally
    # and handles 1Password Environments properly
    result = subprocess.run(
        ["cat", str(path)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to read {path}: {result.stderr}")
    return result.stdout


def read_env_file_vars(path: Path) -> Dict[str, str]:
    """
    Read and parse env file variables using python-dotenv.

    This uses python-dotenv >= 1.1.2 which has native support for
    1Password Environments FIFO mounts.

    Args:
        path: Path to the env file

    Returns:
        Dictionary of environment variable names to values
    """
    return dict(dotenv_values(path))


def find_local_env_files(envs_dir: Path, project: str) -> List[Path]:
    """
    Find all .env* files in the local envs/<project>/ directory.

    Supports both regular files and 1Password Environment FIFO mounts.

    Args:
        envs_dir: Path to the envs/ directory
        project: Project directory name (repo slug or custom name)

    Returns:
        List of paths to .env files
    """
    project_dir = envs_dir / project
    if not project_dir.exists():
        return []

    env_files = []
    for path in project_dir.rglob("*"):
        if is_readable_env_path(path) and is_env_file(path.name):
            env_files.append(path)
    return env_files


def find_remote_env_files(sandbox_id: str, project_path: str, max_depth: int = 5) -> List[str]:
    """
    Find all .env* files in the sandbox project directory.

    Recursively searches the project, skipping large directories like node_modules.
    Ignores example/template files (.env.example, .env.sample, etc.)

    Args:
        sandbox_id: The sandbox ID
        project_path: Path to the project in the sandbox (e.g., /home/user/my-project)
        max_depth: Maximum directory depth to search

    Returns:
        List of absolute paths to .env files in the sandbox
    """
    sbx = Sandbox.connect(sandbox_id)
    env_files = []

    # Directories to skip during recursive search
    skip_dirs = {
        "node_modules", ".git", ".venv", "venv", "__pycache__",
        ".next", ".nuxt", "dist", "build", ".cache", ".turbo"
    }

    def search_dir(path: str, depth: int = 0):
        if depth > max_depth:
            return
        try:
            items = sbx.files.list(path)
            for item in items:
                if item.type.value == "dir":
                    if item.name in skip_dirs:
                        continue
                    search_dir(item.path, depth + 1)
                elif is_env_file(item.name):
                    env_files.append(item.path)
        except Exception:
            pass  # Directory may not be accessible

    search_dir(project_path)
    return env_files


def push_env_files(
    sandbox_id: str,
    envs_dir: Path,
    project: str,
) -> Dict:
    """
    Push local env files to sandbox.

    Args:
        sandbox_id: The sandbox ID
        envs_dir: Path to the local envs/ directory
        project: Project directory name (repo slug or custom name)

    Returns:
        Dictionary with push statistics
    """
    sbx = Sandbox.connect(sandbox_id)
    project_dir = envs_dir / project

    if not project_dir.exists():
        raise FileNotFoundError(f"Local env directory not found: {project_dir}")

    stats = {
        "files_pushed": 0,
        "files": [],
        "errors": [],
    }

    env_files = find_local_env_files(envs_dir, project)

    for local_path in env_files:
        try:
            # Calculate relative path from project dir
            rel_path = local_path.relative_to(project_dir)
            remote_path = f"{SANDBOX_BASE_PATH}/{project}/{rel_path}"

            # Read local file (supports 1Password FIFO mounts)
            content = read_env_file_content(local_path)

            # Ensure parent directory exists
            parent_dir = str(Path(remote_path).parent)
            try:
                sbx.files.make_dir(parent_dir)
            except Exception:
                pass  # Directory may already exist

            # Write to sandbox
            sbx.files.write(remote_path, content)
            stats["files_pushed"] += 1
            stats["files"].append(str(rel_path))

        except Exception as e:
            stats["errors"].append(f"{local_path}: {e}")

    return stats


class FifoWriteError(Exception):
    """Raised when attempting to write to a FIFO (named pipe) file."""
    pass


def pull_env_files(
    sandbox_id: str,
    envs_dir: Path,
    project: str,
) -> Dict:
    """
    Pull env files from sandbox to local.

    Args:
        sandbox_id: The sandbox ID
        envs_dir: Path to the local envs/ directory
        project: Project directory name (repo slug or custom name)

    Returns:
        Dictionary with pull statistics

    Raises:
        FifoWriteError: If a target local file is a FIFO (e.g., 1Password mount)
    """
    sbx = Sandbox.connect(sandbox_id)
    project_dir = envs_dir / project
    full_sandbox_path = f"{SANDBOX_BASE_PATH}/{project}"

    stats = {
        "files_pulled": 0,
        "files": [],
        "errors": [],
        "fifo_files": [],  # Track FIFO files that couldn't be written
    }

    # Find env files in sandbox
    remote_files = find_remote_env_files(sandbox_id, full_sandbox_path)

    for remote_path in remote_files:
        try:
            # Calculate relative path from project root
            rel_path = remote_path[len(full_sandbox_path):].lstrip("/")
            local_path = project_dir / rel_path

            # Check if target is a FIFO (1Password Environment mount)
            if local_path.exists() and local_path.is_fifo():
                stats["fifo_files"].append(rel_path)
                continue

            # Read from sandbox
            content = sbx.files.read(remote_path)

            # Ensure parent directory exists
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Write to local
            local_path.write_text(content)
            stats["files_pulled"] += 1
            stats["files"].append(rel_path)

        except Exception as e:
            stats["errors"].append(f"{remote_path}: {e}")

    # Raise error if any FIFO files were encountered
    if stats["fifo_files"]:
        raise FifoWriteError(stats["fifo_files"])

    return stats


def diff_env_files(
    sandbox_id: str,
    envs_dir: Path,
    project: str,
) -> Dict:
    """
    Compare env files between local and sandbox (keys only).

    Args:
        sandbox_id: The sandbox ID
        envs_dir: Path to the local envs/ directory
        project: Project directory name (repo slug or custom name)

    Returns:
        Dictionary with diff results per file
    """
    sbx = Sandbox.connect(sandbox_id)
    project_dir = envs_dir / project
    full_sandbox_path = f"{SANDBOX_BASE_PATH}/{project}"

    # Find all env files from both sources
    local_files = find_local_env_files(envs_dir, project)
    remote_files = find_remote_env_files(sandbox_id, full_sandbox_path)

    # Build relative path sets
    local_rel_paths = set()
    local_path_map = {}
    for lf in local_files:
        rel = str(lf.relative_to(project_dir))
        local_rel_paths.add(rel)
        local_path_map[rel] = lf

    remote_rel_paths = set()
    remote_path_map = {}
    for rf in remote_files:
        rel = rf[len(full_sandbox_path):].lstrip("/")
        remote_rel_paths.add(rel)
        remote_path_map[rel] = rf

    all_paths = local_rel_paths | remote_rel_paths

    results = {
        "files": {},
        "summary": {
            "files_only_local": 0,
            "files_only_remote": 0,
            "files_with_differences": 0,
            "files_identical": 0,
        }
    }

    for rel_path in sorted(all_paths):
        file_diff = {
            "added": [],      # Keys only in remote (sandbox)
            "removed": [],    # Keys only in local
            "changed": [],    # Keys with different values
            "status": None,   # "only_local", "only_remote", "differs", "identical"
        }

        local_path = local_path_map.get(rel_path)
        remote_path = remote_path_map.get(rel_path)

        if local_path and not remote_path:
            # File only exists locally
            file_diff["status"] = "only_local"
            local_vars = read_env_file_vars(local_path)
            file_diff["removed"] = list(local_vars.keys())
            results["summary"]["files_only_local"] += 1

        elif remote_path and not local_path:
            # File only exists in sandbox
            file_diff["status"] = "only_remote"
            try:
                remote_content = sbx.files.read(remote_path)
                remote_vars = parse_env_file(remote_content)
                file_diff["added"] = list(remote_vars.keys())
            except Exception:
                file_diff["added"] = ["<error reading file>"]
            results["summary"]["files_only_remote"] += 1

        else:
            # File exists in both - compare keys
            local_vars = read_env_file_vars(local_path)
            try:
                remote_content = sbx.files.read(remote_path)
                remote_vars = parse_env_file(remote_content)
            except Exception:
                file_diff["status"] = "error"
                results["files"][rel_path] = file_diff
                continue

            local_keys = set(local_vars.keys())
            remote_keys = set(remote_vars.keys())

            # Keys only in remote
            file_diff["added"] = sorted(remote_keys - local_keys)
            # Keys only in local
            file_diff["removed"] = sorted(local_keys - remote_keys)
            # Keys with different values
            common_keys = local_keys & remote_keys
            for key in sorted(common_keys):
                if local_vars[key] != remote_vars[key]:
                    file_diff["changed"].append(key)

            if file_diff["added"] or file_diff["removed"] or file_diff["changed"]:
                file_diff["status"] = "differs"
                results["summary"]["files_with_differences"] += 1
            else:
                file_diff["status"] = "identical"
                results["summary"]["files_identical"] += 1

        results["files"][rel_path] = file_diff

    return results
