# Example 5: Host Next.js Application

## When to Use
Read this when you're building a Next.js web application that needs to be accessible via a browser.

## User Request Pattern
```
Build me a web app/site
Create a dashboard/UI
Build a Next.js application
I want to see this running in my browser
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
# YOU capture and remember: sandbox_id = "sbx_frontend123app"
# Default timeout: 1 hour
```

### Step 3: Create Next.js Application

```bash
# Create Next.js app with TypeScript and Tailwind
uv run sbx exec sbx_frontend123app "npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --no-git" --cwd /home/user --timeout 120

# Install dependencies
uv run sbx exec sbx_frontend123app "npm install" --cwd /home/user/my-app
```

### Step 4: Configure for External Access

Update `next.config.js` to bind to `0.0.0.0`:
```bash
uv run sbx files write sbx_frontend123app /home/user/my-app/next.config.ts "
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  // Allow external access from E2B sandbox
  experimental: {
    serverActions: {
      allowedOrigins: ['*'],
    },
  },
}

export default nextConfig

// For dev server, use: npm run dev -- -H 0.0.0.0
"
```

### Step 5: Start the Server in Background

```bash
uv run sbx exec sbx_frontend123app "npm run dev -- -H 0.0.0.0" --background --cwd /home/user/my-app
```

**Key points**:
- Use `--background` flag to keep server running
- `-H 0.0.0.0` binds to all interfaces for external access
- Next.js defaults to port 3000

### Step 6: Get the Public URL

**CRITICAL**: Always use the `get-host` command to get the actual URL:

```bash
uv run sbx sandbox get-host sbx_frontend123app --port 3000
```

This returns the authoritative URL:
```
https://3000-sbx_frontend123app.e2b.app
```

**IMPORTANT**:
- **Do NOT construct or infer the URL** - it will fail
- **Always use `sbx sandbox get-host <sandbox_id> --port 3000`**
- Use the exact URL returned by this command

### Step 7: Verify and Share

```bash
# Get the URL - capture output in your context
uv run sbx sandbox get-host sbx_frontend123app --port 3000
# Output: https://3000-sbx_frontend123app.e2b.app
# YOU remember this URL

# Test it
curl https://3000-sbx_frontend123app.e2b.app
```

Share with the user:
```
Your application is now running at:
https://3000-sbx_frontend123app.e2b.app

The app will remain available for 1 hour (auto-timeout).
```

### Step 8: Report to User

Report the sandbox ID and URL. The sandbox auto-terminates after 1 hour.

**Never delete the sandbox unless explicitly asked to do so.**

## Key Points

### Port Configuration
- **Always use port 3000** (Next.js default)
- Use `-H 0.0.0.0` when starting dev server for external access

### Server Requirements
- **Host**: Must bind to `0.0.0.0` to be accessible externally
- **Port**: 3000 (Next.js default)
- **Background**: Always use `--background` flag

### Getting the URL
**ONLY METHOD**: Use `sbx sandbox get-host <sandbox_id> --port 3000`

Never construct or infer the URL - always use the get-host command.

## Troubleshooting

**"Cannot access the URL"**:
- Verify you used `get-host` command (don't construct manually)
- Check server is running: `uv run sbx sandbox status <sandbox_id>`
- Ensure `-H 0.0.0.0` was used when starting the server

**"Connection refused"**:
- Server might have crashed - check logs
- Restart server in background with `-H 0.0.0.0`

**"Frontend shows blank page"**:
- Check browser console for errors
- Verify the build succeeded
- Check API routes are accessible

## Complete Example

```bash
# 1. Initialize
uv run sbx init
# Captured: sbx_myapp123

# 2. Create Next.js app
uv run sbx exec sbx_myapp123 "npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --no-git" --cwd /home/user --timeout 120

# 3. Start dev server with external access
uv run sbx exec sbx_myapp123 "npm run dev -- -H 0.0.0.0" --background --cwd /home/user/my-app

# 4. Get public URL
uv run sbx sandbox get-host sbx_myapp123 --port 3000
# Returns: https://3000-sbx_myapp123.e2b.app
# YOU remember this URL

# 5. Verify
curl https://3000-sbx_myapp123.e2b.app

# 6. Share URL with user
# Sandbox auto-terminates after 1 hour
```
