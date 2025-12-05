# Setup

Run the setup scripts and report results to the user.

## Steps

1. Link skill prompts to commands:
   ```
   uv run .claude/scripts/link_skill_prompts.py
   ```

2. Check environment variables:
   ```
   uv run .claude/scripts/check_env.py
   ```

## Report

Summarize the setup status:
- Which skills were linked (or already linked)
- Whether all required environment variables are set
- If anything is missing, provide clear instructions on how to fix it
