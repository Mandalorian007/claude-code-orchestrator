# Example 2: Test a Package

**When to use**: Installing and testing Python packages in isolation.

## Workflow

```bash
# Initialize sandbox
uv run sbx init
# Capture sandbox_id from output

# Install uv package manager
uv run sbx exec <sandbox_id> "curl -LsSf https://astral.sh/uv/install.sh | sh" --shell --timeout 120

# Install the package
uv run sbx exec <sandbox_id> "/home/user/.local/bin/uv pip install --system requests"

# Test the package
uv run sbx exec <sandbox_id> "python3 -c 'import requests; print(requests.__version__)'"
```

## Key Points

- Use `--shell` flag when piping commands (`curl | sh`)
- Use `--timeout 120` for installations
- After installing uv, use full path: `/home/user/.local/bin/uv`
