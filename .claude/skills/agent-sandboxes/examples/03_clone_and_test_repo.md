# Example 3: Clone and Test Repository

**When to use**: Cloning a GitHub repo and running tests or commands in it.

## Workflow

```bash
# Initialize sandbox
uv run sbx init
# Capture sandbox_id from output

# Clone repository
uv run sbx exec <sandbox_id> "git clone https://github.com/user/repo /home/user/repo"

# Install dependencies and run tests
uv run sbx exec <sandbox_id> "pip install -r requirements.txt && pytest" --cwd /home/user/repo --shell --timeout 300
```

## Key Points

- Use `--cwd` to run commands in a directory (better than `cd`)
- Use `--shell` when chaining commands with `&&`
- Use `--timeout 300` for long-running tests
- Git is pre-installed in sandboxes
- For private repos, ensure `GH_TOKEN` is set in `.env`
