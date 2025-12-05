"""
Git operations with automatic authentication.
"""

import json
import os
import re
import click
from urllib.parse import urlparse, urlunparse
from rich.console import Console
from ..modules import commands as cmd_module

console = Console()


# Regex patterns for GitHub URL parsing
GITHUB_HTTPS_PATTERN = re.compile(
    r"https://(?:[^@]+@)?github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$"
)
GITHUB_SSH_PATTERN = re.compile(
    r"git@github\.com:([^/]+)/([^/]+?)(?:\.git)?/?$"
)


def _parse_github_url(url: str) -> tuple[str, str] | None:
    """Parse owner and repo from a GitHub URL.

    Returns (owner, repo) tuple or None if not a valid GitHub URL.
    Handles:
      - https://github.com/owner/repo.git
      - https://token@github.com/owner/repo.git
      - git@github.com:owner/repo.git
    """
    # Try HTTPS pattern first
    match = GITHUB_HTTPS_PATTERN.match(url)
    if match:
        return match.group(1), match.group(2)

    # Try SSH pattern
    match = GITHUB_SSH_PATTERN.match(url)
    if match:
        return match.group(1), match.group(2)

    return None


def _auth_url(url: str) -> str:
    """Inject GH_TOKEN into GitHub HTTPS URLs."""
    token = os.environ.get("GH_TOKEN")
    if not token:
        return url
    p = urlparse(url)
    if p.scheme == "https" and "github.com" in p.netloc and "@" not in p.netloc:
        return urlunparse(p._replace(netloc=f"{token}@{p.netloc}"))
    return url


@click.group()
def git():
    """Git operations (GH_TOKEN auth automatic)."""
    pass


@git.command()
@click.argument("sandbox_id")
@click.argument("url")
@click.option("--branch", "-b", default=None, help="Branch to clone")
@click.option("--path", "-p", default="/home/user", help="Target directory")
def clone(sandbox_id, url, branch, path):
    """Clone a repository.

    Automatically injects GH_TOKEN for GitHub URLs.
    Token is read from local environment.

    Examples:
        sbx git clone abc123 https://github.com/user/repo.git
        sbx git clone abc123 https://github.com/user/repo.git --branch main
    """
    # Use -c credential.helper= to disable interactive prompts (fails in sandbox)
    cmd = ["git", "-c", "credential.helper=", "clone"]
    if branch:
        cmd.extend(["-b", branch])
    cmd.append(_auth_url(url))

    console.print(f"[yellow]Cloning {url}...[/yellow]")

    # Only set GIT_TERMINAL_PROMPT=0 to prevent hanging on credential prompt
    # Don't set GIT_ASKPASS as it interferes with public repo access
    git_envs = {"GIT_TERMINAL_PROMPT": "0"}

    try:
        result = cmd_module.run_command(
            sandbox_id, " ".join(cmd), cwd=path, timeout=120, envs=git_envs
        )
        if result["exit_code"] == 0:
            console.print("[green]✓ Cloned[/green]")
            # Git clone progress goes to stderr, show it on success too
            if result.get("stderr"):
                # Redact token from output
                output = _redact_token(result["stderr"])
                console.print(f"[dim]{output}[/dim]")
        else:
            _print_error(result["stderr"], "Clone")
    except Exception as e:
        _print_error(str(e), "Clone")


def _redact_token(text: str) -> str:
    """Redact GH_TOKEN from text to prevent leakage."""
    token = os.environ.get("GH_TOKEN")
    if token and text:
        return text.replace(token, "***")
    return text


def _print_error(error_text: str, operation: str = "Operation"):
    """Print error with token redacted."""
    console.print(f"[red]✗ {operation} failed[/red]")
    if error_text:
        console.print(f"[dim]{_redact_token(error_text)}[/dim]")


def _get_remote_url(sandbox_id: str, path: str) -> str:
    """Get the remote origin URL from a repo."""
    result = cmd_module.run_command(sandbox_id, "git remote get-url origin", cwd=path)
    if result["exit_code"] == 0:
        return result["stdout"].strip()
    return ""


def _set_auth_remote(sandbox_id: str, path: str) -> bool:
    """Set remote URL with auth token.

    Returns True if successful, False otherwise.
    """
    remote_url = _get_remote_url(sandbox_id, path)
    if not remote_url:
        console.print("[dim]Warning: Could not get remote URL[/dim]")
        return False

    auth_url = _auth_url(remote_url)
    result = cmd_module.run_command(
        sandbox_id, f"git remote set-url origin {auth_url}", cwd=path
    )
    if result["exit_code"] != 0:
        console.print("[dim]Warning: Could not set auth remote[/dim]")
        return False
    return True


@git.command()
@click.argument("sandbox_id")
@click.option("--path", "-p", default="/home/user/project", help="Repository path")
@click.option("--branch", "-b", default=None, help="Branch to push (default: current)")
@click.option("--set-upstream", "-u", is_flag=True, help="Set upstream for new branch")
def push(sandbox_id, path, branch, set_upstream):
    """Push commits to remote.

    Examples:
        sbx git push abc123 --path /home/user/repo
        sbx git push abc123 --path /home/user/repo --branch feature-x -u
    """
    _set_auth_remote(sandbox_id, path)

    cmd = ["git", "push"]
    if set_upstream:
        cmd.append("-u")
        cmd.append("origin")
        if branch:
            cmd.append(branch)
        else:
            # Get current branch name
            result = cmd_module.run_command(sandbox_id, "git branch --show-current", cwd=path)
            if result["exit_code"] == 0:
                cmd.append(result["stdout"].strip())
    elif branch:
        cmd.extend(["origin", branch])

    console.print(f"[yellow]Pushing...[/yellow]")
    git_envs = {"GIT_TERMINAL_PROMPT": "0"}

    try:
        result = cmd_module.run_command(sandbox_id, " ".join(cmd), cwd=path, timeout=120, envs=git_envs)
        if result["exit_code"] == 0:
            console.print("[green]✓ Pushed[/green]")
        else:
            _print_error(result["stderr"], "Push")
    except Exception as e:
        _print_error(str(e), "Push")


@git.command()
@click.argument("sandbox_id")
@click.argument("title")
@click.option("--body", "-b", default="", help="PR description")
@click.option("--path", "-p", default="/home/user/project", help="Repository path")
@click.option("--base", default="main", help="Base branch (default: main)")
def pr(sandbox_id, title, body, path, base):
    """Create a pull request.

    Examples:
        sbx git pr abc123 "Fix bug" --path /home/user/repo
        sbx git pr abc123 "Add feature" --body "Detailed description" --base main
    """
    import base64

    # Get current branch
    result = cmd_module.run_command(sandbox_id, "git branch --show-current", cwd=path)
    if result["exit_code"] != 0:
        console.print("[red]✗ Could not determine current branch[/red]")
        return
    head_branch = result["stdout"].strip()

    # Get repo info from remote URL
    remote_url = _get_remote_url(sandbox_id, path)
    if not remote_url:
        console.print("[red]✗ Could not get remote URL[/red]")
        return

    # Parse owner/repo using clean regex
    parsed = _parse_github_url(remote_url)
    if not parsed:
        console.print("[red]✗ Could not parse GitHub URL[/red]")
        console.print(f"[dim]URL: {_redact_token(remote_url)}[/dim]")
        return
    owner, repo = parsed

    # Require GH_TOKEN for PR creation
    token = os.environ.get("GH_TOKEN")
    if not token:
        console.print("[red]✗ GH_TOKEN not set[/red]")
        return

    # Build JSON payload and base64 encode to avoid shell escaping issues
    pr_data = json.dumps({
        "title": title,
        "body": body,
        "head": head_branch,
        "base": base,
    })
    pr_data_b64 = base64.b64encode(pr_data.encode()).decode()

    # Use base64 decode in curl to handle special characters safely
    curl_cmd = (
        f'echo "{pr_data_b64}" | base64 -d | '
        f'curl -s -X POST "https://api.github.com/repos/{owner}/{repo}/pulls" '
        f'-H "Authorization: Bearer {token}" '
        f'-H "Accept: application/vnd.github+json" '
        f'-H "Content-Type: application/json" '
        f'-d @-'
    )

    console.print(f"[yellow]Creating PR: {title}[/yellow]")
    console.print(f"[dim]{head_branch} → {base}[/dim]")

    try:
        result = cmd_module.run_command(sandbox_id, curl_cmd, cwd=path, timeout=120)
        if result["exit_code"] == 0:
            try:
                response = json.loads(result["stdout"])
                if "html_url" in response:
                    console.print(f"[green]✓ PR created: {response['html_url']}[/green]")
                elif "message" in response:
                    console.print(f"[red]✗ {response['message']}[/red]")
                    if "errors" in response:
                        for err in response["errors"]:
                            console.print(f"[dim]  - {err.get('message', err)}[/dim]")
                else:
                    console.print("[red]✗ Unexpected response[/red]")
            except json.JSONDecodeError:
                console.print("[red]✗ Invalid response from GitHub API[/red]")
                if result["stdout"]:
                    console.print(f"[dim]{_redact_token(result['stdout'])}[/dim]")
        else:
            _print_error(result["stderr"], "PR creation")
    except Exception as e:
        _print_error(str(e), "PR creation")
