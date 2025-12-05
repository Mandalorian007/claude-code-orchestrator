#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""
Link skill prompts to commands directory.

Scans .claude/skills/ for skills with a prompts/ directory and creates
symlinks in .claude/commands/ to enable /skill-name:prompt invocation.

Usage:
    uv run .claude/scripts/link_skill_prompts.py
"""

from pathlib import Path


def main():
    script_dir = Path(__file__).parent
    claude_dir = script_dir.parent

    skills_dir = claude_dir / "skills"
    commands_dir = claude_dir / "commands"

    if not skills_dir.exists():
        print(f"No skills directory found at {skills_dir}")
        return

    commands_dir.mkdir(exist_ok=True)

    linked = 0
    skipped = 0

    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir():
            continue

        skill_name = skill_path.name
        prompts_dir = skill_path / "prompts"

        if not prompts_dir.exists():
            print(f"  [{skill_name}] No prompts/ directory, skipping")
            skipped += 1
            continue

        link_path = commands_dir / skill_name
        relative_target = Path("..") / "skills" / skill_name / "prompts"

        if link_path.exists() or link_path.is_symlink():
            if link_path.is_symlink():
                current_target = link_path.resolve()
                expected_target = prompts_dir.resolve()
                if current_target == expected_target:
                    print(f"  [{skill_name}] Already linked correctly")
                else:
                    print(f"  [{skill_name}] Symlink exists but points elsewhere: {link_path.readlink()}")
            else:
                print(f"  [{skill_name}] Path exists but is not a symlink: {link_path}")
            skipped += 1
            continue

        link_path.symlink_to(relative_target)
        print(f"  [{skill_name}] Created: {link_path} -> {relative_target}")
        linked += 1

    print()
    print(f"Done. Linked {linked} skill(s), {skipped} skipped.")


if __name__ == "__main__":
    main()
