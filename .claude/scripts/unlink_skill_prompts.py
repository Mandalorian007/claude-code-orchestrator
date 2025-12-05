#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""
Remove skill prompt symlinks from commands directory.

Scans .claude/commands/ for symlinks that point to skill prompts directories
and removes them.

Usage:
    uv run .claude/scripts/unlink_skill_prompts.py
"""

from pathlib import Path


def main():
    script_dir = Path(__file__).parent
    claude_dir = script_dir.parent

    commands_dir = claude_dir / "commands"

    if not commands_dir.exists():
        print(f"No commands directory found at {commands_dir}")
        return

    removed = 0
    skipped = 0

    for item in commands_dir.iterdir():
        if not item.is_symlink():
            continue

        try:
            target = item.readlink()
            target_str = str(target)
            if "skills" in target_str and "prompts" in target_str:
                item.unlink()
                print(f"  Removed: {item} -> {target}")
                removed += 1
            else:
                skipped += 1
        except OSError:
            skipped += 1
            continue

    print()
    print(f"Done. Removed {removed} symlink(s), {skipped} skipped.")


if __name__ == "__main__":
    main()
