"""
E2B Sandbox CLI - Main entry point.

A comprehensive CLI for managing E2B sandboxes and performing operations.
"""

import os
import click
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables
# Path from src/main.py: src -> sandbox_cli -> agent-sandboxes -> skills -> .claude -> root (6 levels)
root_dir = Path(__file__).parent.parent.parent.parent.parent.parent
load_dotenv(root_dir / ".env")

# Import command groups
from .commands.sandbox import sandbox
from .commands.files import files
from .commands.exec import exec
from .commands.git import git
from .commands.env import env

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    E2B Sandbox CLI - Isolated code execution environments.

    \b
    USAGE
    -----
    cd .claude/skills/agent-sandboxes/sandbox_cli/
    uv run sbx <command> [args]

    \b
    RULES
    -----
    1. Capture sandbox ID in your context (not shell variables)
    2. Use 'sandbox get-host' for URLs - never construct manually
    3. Default timeout: 1 hour
    4. GH_TOKEN from .env provides automatic GitHub auth

    Run 'uv run sbx <command> --help' for usage and examples.
    """
    pass


# Add command groups
cli.add_command(sandbox)
cli.add_command(files)
cli.add_command(exec)
cli.add_command(git)
cli.add_command(env)


# Add an init command for quick sandbox setup
@cli.command()
@click.option(
    "--template",
    "-t",
    default=None,
    help="Sandbox template name or ID",
)
@click.option(
    "--timeout", default=3600, help="Sandbox timeout in seconds (default: 1 hour)"
)
@click.option("--env", "-e", multiple=True, help="Environment variables (KEY=VALUE)")
@click.option("--name", "-n", default=None, help="Sandbox name (stored in metadata)")
def init(template, timeout, env, name):
    """
    Create a new sandbox and display the ID.

    \b
    IMPORTANT: Capture the sandbox ID from output. Do NOT use shell variables.

    \b
    TEMPLATES
    ---------
    fullstack-app-template-lite      2 vCPU, 4GB (default)
    fullstack-app-template-standard  4 vCPU, 4GB
    fullstack-app-template-heavy     4 vCPU, 8GB
    fullstack-app-template-max       8 vCPU, 8GB

    \b
    EXAMPLES
    --------
    # Basic
    uv run sbx init

    # With template
    uv run sbx init --template fullstack-app-template-standard

    # With options
    uv run sbx init --timeout 7200 --name my-project
    uv run sbx init --env API_KEY=secret

    \b
    TYPICAL WORKFLOW
    ----------------
    uv run sbx init                              # Get sandbox ID
    uv run sbx exec <id> "python --version"      # Run command
    uv run sbx files write <id> /home/user/app.py "print('hi')"
    uv run sbx exec <id> "python /home/user/app.py"
    """
    try:
        from .modules import sandbox as sbx_module

        console.print("[yellow]Initializing new sandbox...[/yellow]")
        if template:
            console.print(f"[dim]Template: {template}[/dim]")

        # Parse env vars
        envs = {}
        for e in env:
            if "=" in e:
                key, value = e.split("=", 1)
                envs[key] = value

        # Auto-forward GH_TOKEN for git operations
        if "GH_TOKEN" in os.environ and "GH_TOKEN" not in envs:
            envs["GH_TOKEN"] = os.environ["GH_TOKEN"]

        # Add name to metadata if provided
        metadata = {}
        if name:
            metadata["name"] = name

        sbx = sbx_module.create_sandbox(
            template=template,
            timeout=timeout,
            envs=envs if envs else None,
            metadata=metadata if metadata else None,
        )

        console.print(f"\n[green]✓ Sandbox created successfully![/green]")
        console.print(f"\n[cyan]Sandbox ID:[/cyan] {sbx.sandbox_id}")
        if name:
            console.print(f"[cyan]Name:[/cyan] {name}")
        if template:
            console.print(f"[dim]Template: {template}[/dim]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


if __name__ == "__main__":
    cli()
