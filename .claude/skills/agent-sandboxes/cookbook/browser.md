# Browser Automation Cookbook

Extended patterns and troubleshooting for browser automation. For basic commands, see SKILL.md.

**Important**: Browser commands run on your **local machine**, not in the sandbox. Uses Playwright's isolated Chromium—does not interfere with your Chrome browser.

## Multi-Agent Parallel Execution

Multiple agents can run browsers simultaneously using different ports:

```bash
# Agent 1: uses default port 9222
uv run sbx browser start
uv run sbx browser nav https://app1.example.com

# Agent 2: uses port 9223
uv run sbx browser start --port 9223
uv run sbx browser nav https://app2.example.com --port 9223
```

**Rules for parallel agents**:
1. Generate a unique port (e.g., `9222 + RANDOM % 778`)
2. Use `--port` flag consistently on ALL browser commands
3. Close your own browser when done: `sbx browser close --port <port>`

## Common Patterns

### Form Interaction
```bash
uv run sbx browser type "#username" "testuser"
uv run sbx browser type "#password" "testpass"
uv run sbx browser click "#submit-button"
```

### Data Extraction
```bash
# Get all link texts
uv run sbx browser eval "Array.from(document.querySelectorAll('a')).map(a => a.textContent)"

# Get structured data
uv run sbx browser eval "Array.from(document.querySelectorAll('.item')).map(el => ({title: el.querySelector('h2')?.textContent, price: el.querySelector('.price')?.textContent}))"
```

### Keyboard Navigation
```bash
uv run sbx browser press Tab
uv run sbx browser press Enter
uv run sbx browser press Escape
```

### Page Structure
```bash
uv run sbx browser dom          # Simplified DOM (good for LLMs)
uv run sbx browser dom --full   # Full HTML
uv run sbx browser a11y         # Accessibility tree (best for understanding structure)
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Browser environment not initialized" | Run `uv run sbx browser init` |
| "Could not connect to Chromium on port XXXX" | Start browser first: `uv run sbx browser start --port XXXX` |
| "Port XXXX is already in use" | Use different port, or close existing: `uv run sbx browser close --port XXXX` |
| "Failed to start browser" | Re-run `init`, kill stale processes: `pkill -f "chromium.*remote-debugging"` |
| Multiple agents failing | Each agent MUST use a unique port |
