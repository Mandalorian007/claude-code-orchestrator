# Claude E2B Orchestrator

A toolkit for Claude Code to orchestrate isolated [E2B sandbox](https://e2b.dev/) environments. Run untrusted code, build applications, and execute arbitrary engineering tasks—all in secure, remote sandboxes that protect your local machine.

## Why Remote Sandboxes?

| Capability | Benefit |
|------------|---------|
| **Isolation** | Sandboxes are fully isolated from your local filesystem and production environment |
| **Scale** | Spawn multiple sandboxes in parallel for concurrent workloads |
| **Agency** | Full control over sandbox environments—install packages, modify files, run servers |

## Setup

### Prerequisites

- Python >= 3.12
- `uv` package manager
- E2B API Key ([get one here](https://e2b.dev/dashboard/keys))

### Installation

1. **Configure environment**:
   ```bash
   cp .env.sample .env
   ```

2. **Add your E2B API key** to `.env`:
   ```
   E2B_API_KEY=sbx_...
   ```

3. **(Optional) Add GitHub token** for private repo cloning:
   ```
   GH_TOKEN=ghp_...
   ```

## Usage

### Quick Start

From Claude Code, use the skill to spin up a sandbox:

```
\agent-sandboxes:sandbox "Run python --version and pip list"
```

### Full Workflow

For complex tasks, use the orchestrated workflow:

```
\agent-sandboxes:plan-build-host-test "<your prompt>" "<workflow_id>"
```

This executes: **Plan** → **Build** → **Host** → **Test**

### Manual CLI

The sandbox CLI can also be used directly:

```bash
cd .claude/skills/agent-sandboxes/sandbox_cli/

# Initialize a sandbox (12-hour timeout)
uv run sbx init --timeout 43200

# Execute commands
uv run sbx exec <sandbox_id> "echo hello"

# File operations
uv run sbx files write <sandbox_id> /home/user/script.py "print('hello')"
uv run sbx files read <sandbox_id> /home/user/output.txt

# Expose a port and get public URL
uv run sbx sandbox get-host <sandbox_id> --port 3000

# Git operations (auto-authenticated if GH_TOKEN set)
uv run sbx git clone <sandbox_id> https://github.com/user/repo.git
```

## CLI Commands

| Command | Purpose |
|---------|---------|
| `sbx init` | Create a new sandbox |
| `sbx exec` | Run commands in sandbox |
| `sbx files` | File operations (ls, read, write, upload, download) |
| `sbx sandbox` | Lifecycle management (info, kill, pause, get-host) |
| `sbx git` | Git operations with auto-auth |
| `sbx browser` | Browser automation via Playwright |

## Sandbox Templates

Pre-built templates with different resource levels:

| Template | vCPU | RAM | Best For |
|----------|------|-----|----------|
| `fullstack-app-template-lite` | 2 | 4GB | Simple apps (default) |
| `fullstack-app-template-standard` | 4 | 4GB | Parallel builds |
| `fullstack-app-template-heavy` | 4 | 8GB | Multi-browser testing |
| `fullstack-app-template-max` | 8 | 8GB | Maximum performance |

## Documentation

- [Skill Guide](.claude/skills/agent-sandboxes/SKILL.md) - Full skill documentation
- [CLI Reference](.claude/skills/agent-sandboxes/sandbox_cli/README.md) - Detailed CLI usage
- [E2B Docs](https://e2b.dev/docs) - E2B platform documentation

## Credits

Forked from [disler/agent-sandbox-skill](https://github.com/disler/agent-sandbox-skill).
