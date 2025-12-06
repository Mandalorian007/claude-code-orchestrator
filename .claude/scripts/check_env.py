#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# ///
"""
Check that required environment variables are set in .env file.

Verifies E2B_API_KEY and GH_TOKEN are present and have values.

Usage:
    uv run .claude/scripts/check_env.py
"""

from pathlib import Path


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    env_file = project_root / ".env"

    required = ["E2B_API_KEY", "GH_TOKEN", "PERPLEXITY_API_KEY"]
    found = {}
    missing = []

    if not env_file.exists():
        print(f"Error: .env file not found at {env_file}")
        print(f"\nCreate it with: cp .env.sample .env")
        return

    content = env_file.read_text()
    lines = content.splitlines()

    for key in required:
        value = None
        for line in lines:
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == key:
                value = v.strip().strip('"').strip("'")
                break

        if value:
            # Mask the value for display
            masked = value[:4] + "..." + value[-4:] if len(value) > 10 else "****"
            found[key] = masked
        else:
            missing.append(key)

    print("Environment check:")
    print()

    for key in required:
        if key in found:
            print(f"  {key}: {found[key]}")
        else:
            print(f"  {key}: MISSING")

    print()

    if missing:
        print(f"Error: Missing {len(missing)} required variable(s): {', '.join(missing)}")
        print()
        print("Add them to .env:")
        for key in missing:
            print(f"  {key}=your_value_here")
    else:
        print("All required variables are set.")


if __name__ == "__main__":
    main()
