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

3. **Add GitHub token** for repo operations:
   ```
   GH_TOKEN=ghp_...
   ```

4. **Validate environment** (in Claude Code):
   ```
   /prime
   ```

## Skills

### Agent Sandboxes

Remote code execution in isolated E2B environments.

```bash
cd .claude/skills/agent-sandboxes/sandbox_cli/
uv run sbx --help
```

| Command | Purpose |
|---------|---------|
| `sbx init` | Create a new sandbox |
| `sbx exec` | Run commands in sandbox |
| `sbx files` | File operations (ls, read, write, upload, download) |
| `sbx sandbox` | Lifecycle management (info, kill, pause, get-host) |
| `sbx git` | Git operations with auto-auth |

### Playwright

Local browser automation using Playwright's Chromium.

```bash
cd .claude/skills/playwright/playwright_cli/
uv run pw --help
```

| Command | Purpose |
|---------|---------|
| `pw init` | Install Playwright and Chromium |
| `pw start` | Start browser session |
| `pw nav` | Navigate to URL |
| `pw screenshot` | Capture page screenshot |
| `pw click` / `pw type` | Interact with elements |
| `pw a11y` | Get accessibility tree |
| `pw close` | Close browser session |

## Workflows

### Plan Only

Create an implementation plan for a full-stack app:

```
/workflow:plan "Build a todo app with categories"
```

### Full Workflow

Execute the complete pipeline—**Plan → Build → Host → Test**:

```
/workflow:plan-build-host-test "Build a todo app with categories"
```

## Sandbox Templates

| Template | vCPU | RAM | Best For |
|----------|------|-----|----------|
| `fullstack-app-template-lite` | 2 | 4GB | Simple apps (default) |
| `fullstack-app-template-standard` | 4 | 4GB | Parallel builds |
| `fullstack-app-template-heavy` | 4 | 8GB | Multi-browser testing |
| `fullstack-app-template-max` | 8 | 8GB | Maximum performance |

## Documentation

- [Agent Sandboxes Skill](.claude/skills/agent-sandboxes/SKILL.md)
- [Playwright Skill](.claude/skills/playwright/SKILL.md)
- [E2B Docs](https://e2b.dev/docs)

## Credits

Forked from [disler/agent-sandbox-skill](https://github.com/disler/agent-sandbox-skill).
