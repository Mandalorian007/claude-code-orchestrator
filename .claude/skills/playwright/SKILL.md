---
name: Playwright
description: Browser automation using Playwright. Use for web scraping, UI testing, taking screenshots, form interaction, and any browser-based tasks. Keywords: browser, playwright, chromium, screenshot, scrape, test, click, type, navigate.
---

# Playwright

A standalone CLI for browser automation using Playwright's isolated Chromium. Runs locally on your machine without affecting your Chrome browser.

## Variables

- **PLAYWRIGHT_CLI_PATH**: `.claude/skills/playwright/playwright_cli/`

## Instructions

- **All commands run from PLAYWRIGHT_CLI_PATH** - Change directory first
- **Use `--port` for parallel sessions** - Each session needs a unique port (9222-9999)
- **Browser runs locally** - Uses Playwright's bundled Chromium, not your Chrome
- **Stateful sessions** - Start browser once, then run multiple commands against it

### When to Use This Skill

Use the Playwright skill when you need to:
- **Take screenshots** of any webpage
- **Test UI interactions** - click buttons, fill forms, verify content
- **Scrape web content** - extract data, get page structure
- **Validate hosted applications** - test sandbox-hosted or deployed apps
- **Automate browser tasks** - form submission, navigation flows

### CLI Overview

```bash
cd PLAYWRIGHT_CLI_PATH

uv run pw init                  # One-time setup (install Chromium)
uv run pw start                 # Start browser
uv run pw nav <url>             # Navigate to URL
uv run pw screenshot            # Take screenshot
uv run pw click <selector>      # Click element
uv run pw type <selector> <text> # Type into input
uv run pw press <key>           # Press keyboard key
uv run pw scroll <direction>    # Scroll page
uv run pw eval <js>             # Run JavaScript
uv run pw a11y                  # Get accessibility tree
uv run pw dom                   # Get DOM structure
uv run pw cookies               # Get cookies
uv run pw pick <message>        # Interactive element picker
uv run pw status                # Check if browser running
uv run pw close                 # Close browser
```

## Workflow

### Step 1: Initialize (One-Time)

```bash
cd PLAYWRIGHT_CLI_PATH
uv run pw init
```

This installs Playwright and downloads Chromium. Only needed once per machine.

### Step 2: Start Browser

```bash
uv run pw start                 # Headless mode (default)
uv run pw start --headed        # Show browser window
uv run pw start --port 9223     # Custom port for parallel sessions
uv run pw start --mobile        # iPhone emulation (390x844, touch, mobile UA)
uv run pw start --width 1280 --height 720  # Custom viewport
```

### Step 3: Navigate and Interact

```bash
# Navigate
uv run pw nav https://example.com
uv run pw nav https://example.com --new  # Open in new tab

# Take screenshots
uv run pw screenshot                     # Save to temp directory
uv run pw screenshot --path ./shot.png   # Save to specific path
uv run pw screenshot --full              # Full page screenshot

# Click elements
uv run pw click "#submit-btn"
uv run pw click "button.primary"
uv run pw click "[data-testid='login']"

# Type into inputs
uv run pw type "#username" "testuser"
uv run pw type "input[name='email']" "test@example.com"

# Press keys
uv run pw press Tab
uv run pw press Enter
uv run pw press Escape

# Scroll
uv run pw scroll down
uv run pw scroll up
uv run pw scroll top
uv run pw scroll bottom
uv run pw scroll down --amount 1000  # Custom scroll amount
```

### Step 4: Extract Data

```bash
# Get accessibility tree (best for understanding page structure)
uv run pw a11y

# Get simplified DOM
uv run pw dom

# Get full HTML
uv run pw dom --full

# Run JavaScript to extract data
uv run pw eval "document.title"
uv run pw eval "document.querySelector('h1').textContent"
uv run pw eval "Array.from(document.querySelectorAll('a')).map(a => a.href)"
```

### Step 5: Close Browser

```bash
uv run pw close
uv run pw close --port 9223  # Close specific port
```

## Common Patterns

### Form Submission

```bash
uv run pw nav https://example.com/login
uv run pw type "#username" "testuser"
uv run pw type "#password" "testpass"
uv run pw click "#submit"
uv run pw screenshot --path ./after-login.png
```

### Data Extraction

```bash
uv run pw nav https://example.com/products
uv run pw eval "Array.from(document.querySelectorAll('.product')).map(el => ({
  name: el.querySelector('h2')?.textContent,
  price: el.querySelector('.price')?.textContent
}))"
```

### Visual Testing

```bash
uv run pw nav https://example.com
uv run pw screenshot --path ./homepage.png --full
uv run pw scroll bottom
uv run pw screenshot --path ./footer.png
```

### Parallel Sessions

```bash
# Agent 1 uses port 9222 (default)
uv run pw start --port 9222
uv run pw nav https://site-a.com --port 9222

# Agent 2 uses port 9223
uv run pw start --port 9223
uv run pw nav https://site-b.com --port 9223

# Each agent must close its own browser
uv run pw close --port 9222
uv run pw close --port 9223
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `pw init` | Install Playwright and Chromium |
| `pw start` | Start browser with remote debugging |
| `pw nav <url>` | Navigate to URL |
| `pw screenshot` | Take screenshot |
| `pw click <selector>` | Click element |
| `pw type <selector> <text>` | Type into input |
| `pw press <key>` | Press keyboard key |
| `pw scroll <direction>` | Scroll page |
| `pw eval <js>` | Execute JavaScript |
| `pw a11y` | Get accessibility tree |
| `pw dom` | Get DOM structure |
| `pw cookies` | Get cookies as JSON |
| `pw pick <message>` | Interactive element picker |
| `pw status` | Check browser status |
| `pw close` | Close browser |

### Common Options

| Option | Description |
|--------|-------------|
| `--port PORT` | CDP port (default: 9222) |
| `--headed` | Show browser window |
| `--mobile` | iPhone emulation |
| `--full` | Full page (screenshot/dom) |
| `--path PATH` | Output path (screenshot) |

## Troubleshooting

**"Browser environment not initialized"**:
- Run `uv run pw init` to install Playwright and Chromium

**"Port XXXX is already in use"**:
- Use different port: `uv run pw start --port 9223`
- Or close existing: `uv run pw close --port XXXX`

**"Could not connect to port XXXX"**:
- Start browser first: `uv run pw start --port XXXX`

**"Failed to click/type selector"**:
- Use `uv run pw a11y` to understand page structure
- Verify selector exists: `uv run pw eval "document.querySelector('selector')"`

**Parallel agents conflicting**:
- Each agent MUST use a unique port (9222-9999)
- Each agent must close only its own browser
