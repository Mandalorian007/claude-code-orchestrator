# Claude Code Orchestrator

A skill toolkit for Claude Code to orchestrate development across repositories. Build applications in isolated sandboxes, automate browsers, scrape the web, and search for current information—all from a centralized set of reusable skills.

## Why This Toolkit?

| Capability | Benefit |
|------------|---------|
| **Isolation** | Build and test in remote E2B sandboxes without affecting your local machine |
| **Automation** | Browser automation with Playwright for UI testing and scraping |
| **Research** | Web search and scraping for current information and documentation |
| **Workflows** | End-to-end pipelines from planning to deployment and testing |

## Setup

### Prerequisites

- Python >= 3.12
- `uv` package manager

### Installation

1. **Configure environment**:
   ```bash
   cp .env.sample .env
   ```

2. **Add API keys** to `.env`:
   ```
   E2B_API_KEY=sbx_...           # https://e2b.dev/dashboard/keys
   GH_TOKEN=ghp_...              # GitHub PAT with repo scope
   PERPLEXITY_API_KEY=pplx-...   # https://perplexity.ai/settings/api
   FIRECRAWL_API_KEY=fc-...      # https://firecrawl.dev/app/api-keys
   ```

3. **Prime Claude Code** (run at the start of each session):
   ```
   /prime
   ```
   Validates environment and loads skill context into the model.

## Skills

| Skill | Purpose | Docs |
|-------|---------|------|
| **Agent Sandboxes** | Remote code execution in isolated E2B environments | [SKILL.md](.claude/skills/agent-sandboxes/SKILL.md) |
| **Playwright** | Local browser automation with Chromium | [SKILL.md](.claude/skills/playwright/SKILL.md) |
| **Firecrawl** | Web scraping and URL discovery | [SKILL.md](.claude/skills/firecrawl/SKILL.md) |
| **Internet Search** | Perplexity-powered web search | [SKILL.md](.claude/skills/internet-search/SKILL.md) |

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

## Credits

Inspired by [IndyDevDan's](https://www.youtube.com/@indydevdan) work on multi-agent orchestration: [video](https://www.youtube.com/watch?v=3kgx0YxCriM) | [agent-sandbox-skill](https://github.com/disler/agent-sandbox-skill)
