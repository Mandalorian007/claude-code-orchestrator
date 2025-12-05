# Example 3: Clone and Test Repository

## When to Use
Read this when you need to clone a GitHub repository and run tests or commands in the repo context.

## User Request Pattern
```
Clone this GitHub repo and run its tests
Test this repository in a sandbox
Clone and build this project
```

## Workflow

### Step 1: Validate Environment
```bash
cd .claude/skills/agent-sandboxes/sandbox_cli
grep "E2B_API_KEY" ../../../../.env
```

### Step 2: Initialize Sandbox
```bash
uv run sbx init
# YOU capture and remember: sandbox_id = "sbx_repo123test"
# Default timeout: 1 hour
```

### Step 3: Clone Repository
```bash
uv run sbx exec sbx_repo123test "git clone https://github.com/user/repo /home/user/repo"
```

### Step 4: Install Dependencies and Run Tests
Use `--cwd` to run commands in the repository directory:
```bash
uv run sbx exec sbx_repo123test "pip install -r requirements.txt && pytest" --cwd /home/user/repo --shell --timeout 300
```

Key flags:
- `--cwd /home/user/repo` - Run in the repo directory
- `--shell` - Enable shell features for `&&`
- `--timeout 300` - Give tests enough time to complete

### Step 5: Report Results and Clean Up
```bash
uv run sbx sandbox kill sbx_repo123test
```

## Key Points
- Default timeout is 1 hour - sufficient for most repos
- Clone to `/home/user/` directory for easy access
- Use `--cwd` flag to run commands in specific directories (better than `cd`)
- Use `--shell` when chaining commands with `&&`
- Increase command timeout for long tests with `--timeout 300`
- Git is pre-installed in E2B sandboxes
- Always clean up the sandbox when done
