"""
Environment file sync commands.
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from ..modules import env as env_module

console = Console()


def get_envs_dir() -> Path:
    """Get the envs/ directory path (relative to project root)."""
    # Path from src/commands/env.py -> project root (6 levels up)
    root = Path(__file__).parent.parent.parent.parent.parent.parent.parent
    return root / "envs"


@click.group()
def env():
    """
    Sync .env files between local envs/ folder and sandbox.

    \b
    COMMANDS
    --------
    push    Local → Sandbox
    pull    Sandbox → Local
    diff    Compare keys (values never shown)

    \b
    Run 'uv run sbx env <command> --help' for details.
    """
    pass


@env.command()
@click.argument("sandbox_id")
@click.argument("project", metavar="PROJECT")
@click.option("--sandbox-path", default="/home/user", help="Base path in sandbox")
def push(sandbox_id, project, sandbox_path):
    """
    Push local env files to sandbox.

    PROJECT is the repo slug or project directory name.

    \b
    STRUCTURE
    ---------
    envs/<project>/           →  /home/user/<project>/
    envs/<project>/.env       →  /home/user/<project>/.env
    envs/<project>/pkg/.env   →  /home/user/<project>/pkg/.env

    \b
    IGNORED
    -------
    .env.example, .env.sample, .env.template
    """
    try:
        envs_dir = get_envs_dir()
        project_dir = envs_dir / project

        if not project_dir.exists():
            console.print(f"[red]✗ Local env directory not found: {project_dir}[/red]")
            console.print(f"[dim]Create it with: mkdir -p envs/{project}[/dim]")
            raise click.Abort()

        console.print(f"[yellow]Pushing env files to sandbox...[/yellow]")
        console.print(f"[dim]Local: envs/{project}/[/dim]")
        console.print(f"[dim]Remote: {sandbox_path}/{project}/[/dim]")

        stats = env_module.push_env_files(
            sandbox_id, envs_dir, project, sandbox_path
        )

        if stats["files_pushed"] > 0:
            console.print(f"\n[green]✓ Pushed {stats['files_pushed']} file(s)[/green]")
            for f in stats["files"]:
                console.print(f"  [dim]→ {f}[/dim]")
        else:
            console.print(f"\n[yellow]No .env files found in envs/{project}/[/yellow]")

        if stats["errors"]:
            console.print(f"\n[red]Errors ({len(stats['errors'])}):[/red]")
            for err in stats["errors"]:
                console.print(f"  [red]✗ {err}[/red]")

    except FileNotFoundError as e:
        console.print(f"[red]✗ {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@env.command()
@click.argument("sandbox_id")
@click.argument("project", metavar="PROJECT")
@click.option("--sandbox-path", default="/home/user", help="Base path in sandbox")
def pull(sandbox_id, project, sandbox_path):
    """
    Pull env files from sandbox to local.

    PROJECT is the repo slug or project directory name.

    \b
    STRUCTURE
    ---------
    /home/user/<project>/.env       →  envs/<project>/.env
    /home/user/<project>/pkg/.env   →  envs/<project>/pkg/.env

    \b
    IGNORED
    -------
    .env.example, .env.sample, .env.template
    """
    try:
        envs_dir = get_envs_dir()

        console.print(f"[yellow]Pulling env files from sandbox...[/yellow]")
        console.print(f"[dim]Remote: {sandbox_path}/{project}/[/dim]")
        console.print(f"[dim]Local: envs/{project}/[/dim]")

        stats = env_module.pull_env_files(
            sandbox_id, envs_dir, project, sandbox_path
        )

        if stats["files_pulled"] > 0:
            console.print(f"\n[green]✓ Pulled {stats['files_pulled']} file(s)[/green]")
            for f in stats["files"]:
                console.print(f"  [dim]← {f}[/dim]")
        else:
            console.print(f"\n[yellow]No .env files found in sandbox[/yellow]")

        if stats["errors"]:
            console.print(f"\n[red]Errors ({len(stats['errors'])}):[/red]")
            for err in stats["errors"]:
                console.print(f"  [red]✗ {err}[/red]")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()


@env.command()
@click.argument("sandbox_id")
@click.argument("project", metavar="PROJECT")
@click.option("--sandbox-path", default="/home/user", help="Base path in sandbox")
def diff(sandbox_id, project, sandbox_path):
    """
    Compare env files between local and sandbox.

    PROJECT is the repo slug or project directory name.
    Values are NEVER shown to protect secrets.

    \b
    Legend:
      + KEY     Only in sandbox (would be pulled)
      - KEY     Only in local (would be pushed)
      ~ KEY     Value differs
    """
    try:
        envs_dir = get_envs_dir()

        console.print(f"[yellow]Comparing env files...[/yellow]")
        console.print(f"[dim]Local: envs/{project}/[/dim]")
        console.print(f"[dim]Remote: {sandbox_path}/{project}/[/dim]")

        results = env_module.diff_env_files(
            sandbox_id, envs_dir, project, sandbox_path
        )

        if not results["files"]:
            console.print(f"\n[yellow]No .env files found in either location[/yellow]")
            return

        # Display results per file
        for rel_path, file_diff in results["files"].items():
            status = file_diff["status"]

            if status == "identical":
                console.print(f"\n[green]✓ {rel_path}[/green] [dim](identical)[/dim]")
                continue

            if status == "only_local":
                console.print(f"\n[yellow]◐ {rel_path}[/yellow] [dim](only in local)[/dim]")
                for key in file_diff["removed"]:
                    console.print(f"  [yellow]- {key}[/yellow]")
                continue

            if status == "only_remote":
                console.print(f"\n[cyan]◑ {rel_path}[/cyan] [dim](only in sandbox)[/dim]")
                for key in file_diff["added"]:
                    console.print(f"  [cyan]+ {key}[/cyan]")
                continue

            # File exists in both with differences
            console.print(f"\n[magenta]~ {rel_path}[/magenta]")

            for key in file_diff["added"]:
                console.print(f"  [cyan]+ {key}[/cyan]")

            for key in file_diff["removed"]:
                console.print(f"  [yellow]- {key}[/yellow]")

            for key in file_diff["changed"]:
                console.print(f"  [magenta]~ {key}[/magenta]")

        # Summary
        summary = results["summary"]
        console.print(f"\n[dim]─────────────────────────────────[/dim]")
        parts = []
        if summary["files_identical"]:
            parts.append(f"[green]{summary['files_identical']} identical[/green]")
        if summary["files_with_differences"]:
            parts.append(f"[magenta]{summary['files_with_differences']} differ[/magenta]")
        if summary["files_only_local"]:
            parts.append(f"[yellow]{summary['files_only_local']} only local[/yellow]")
        if summary["files_only_remote"]:
            parts.append(f"[cyan]{summary['files_only_remote']} only remote[/cyan]")

        if parts:
            console.print(f"Summary: {' | '.join(parts)}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")
        raise click.Abort()
