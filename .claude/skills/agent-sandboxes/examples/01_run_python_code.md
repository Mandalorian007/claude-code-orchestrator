# Example 1: Run Python Code Safely

**When to use**: Testing or executing Python code in isolation.

## Workflow

```bash
# Initialize sandbox
uv run sbx init
# Capture sandbox_id from output (e.g., sbx_abc123)

# Write the script
uv run sbx files write <sandbox_id> /home/user/test.py "import sys; print(sys.version)"

# Run the script
uv run sbx exec <sandbox_id> "python3 /home/user/test.py"
```

## Key Points

- Use `sbx files write` for text files
- Use `sbx exec` to run commands
- Python 3 is pre-installed in sandboxes
