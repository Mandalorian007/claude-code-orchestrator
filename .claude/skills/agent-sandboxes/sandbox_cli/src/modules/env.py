"""
Environment file sync module.
Handles syncing .env files between local envs/ folder and sandbox.
"""

from pathlib import Path
from typing import Dict, List, Set, Tuple
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


def find_local_env_files(envs_dir: Path, project: str) -> List[Path]:
    """
    Find all .env* files in the local envs/<project>/ directory.

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
        if path.is_file() and is_env_file(path.name):
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

            # Read local file
            content = local_path.read_text()

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
    """
    sbx = Sandbox.connect(sandbox_id)
    project_dir = envs_dir / project
    full_sandbox_path = f"{SANDBOX_BASE_PATH}/{project}"

    stats = {
        "files_pulled": 0,
        "files": [],
        "errors": [],
    }

    # Find env files in sandbox
    remote_files = find_remote_env_files(sandbox_id, full_sandbox_path)

    for remote_path in remote_files:
        try:
            # Calculate relative path from project root
            rel_path = remote_path[len(full_sandbox_path):].lstrip("/")
            local_path = project_dir / rel_path

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
            local_vars = parse_env_file(local_path.read_text())
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
            local_vars = parse_env_file(local_path.read_text())
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
