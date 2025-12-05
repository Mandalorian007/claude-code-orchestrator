# Prime

Validate environment and understand the codebase.

## Step 1: Validate Environment

Run `uv run .claude/scripts/check_env.py` to check required variables.

If anything is missing, help the user fix it:
- `E2B_API_KEY`: Get from https://e2b.dev/dashboard/keys
- `GH_TOKEN`: GitHub PAT with repo scope

Stop here if environment is not valid.

## Step 2: Understand Codebase

@README.md
@.claude/skills/*/SKILL.md
@.claude/commands/workflow/
!`git ls-files`

## Report

1. Environment status
2. Your understanding of the codebase and instructions
