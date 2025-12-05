# Example 5: Host Next.js Application

**When to use**: Building a web application that needs to be accessible via browser.

## Workflow

```bash
# Initialize sandbox
uv run sbx init
# Capture sandbox_id from output

# Create Next.js app
uv run sbx exec <sandbox_id> "npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --no-git" --cwd /home/user --timeout 120

# Start dev server with external access
uv run sbx exec <sandbox_id> "npm run dev -- -H 0.0.0.0" --background --cwd /home/user/my-app

# Get the public URL (ALWAYS use this command - never construct URLs manually)
uv run sbx sandbox get-host <sandbox_id> --port 3000
# Returns: https://3000-<sandbox_id>.e2b.app
```

## Key Points

- **Use `-H 0.0.0.0`** to bind server to all interfaces (required for external access)
- **Use `--background`** to keep server running
- **Always use `get-host`** to get the URL - never construct it manually
- Next.js defaults to port 3000

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Cannot access URL | Verify you used `get-host` command, check server is running |
| Connection refused | Ensure `-H 0.0.0.0` was used when starting server |
| Blank page | Check browser console for errors |
