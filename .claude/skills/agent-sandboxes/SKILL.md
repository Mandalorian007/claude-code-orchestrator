---
name: Agent Sandboxes
description: Operate E2B agent sandboxes using the CLI. Use when user needs to run code in isolation, test packages, execute commands safely, or work with binary files in a sandbox environment. Keywords: sandbox, e2b, isolated environment, run code, test code, safe execution.
---

# Agent Sandboxes

E2B sandboxes for safe code execution in isolated environments.

## Variables

- **SANDBOX_CLI_PATH**: `.claude/skills/agent-sandboxes/sandbox_cli/`

## Instructions

Run from SANDBOX_CLI_PATH:
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli/
uv run sbx --help                  # Discover all commands
uv run sbx <command> --help        # Detailed usage
```

**Rules:**
- **CAPTURE SANDBOX ID in your context** - don't use shell variables
- **Use `sandbox get-host`** to get URLs - never construct manually
- **Don't create files locally** - use the sandbox
- **Never delete sandboxes** unless asked - they auto-timeout (1 hour)

## Special Characters in Files

Shell glob expansion breaks brackets `[]`. Use `--stdin`:
```bash
echo 'const arr = [1, 2];' | uv run sbx files write <id> /path/file.js --stdin
```  

## Troubleshooting

- **"E2B_API_KEY not found"**: Run `/prime` to validate environment
- **"Command not found: sbx"**: Run from SANDBOX_CLI_PATH with `uv run sbx`
- **"Permission denied"**: Use `--root` flag
- **"Git auth failed"**: Verify GH_TOKEN in `.env`
