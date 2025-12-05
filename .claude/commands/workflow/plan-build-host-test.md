---
description: Complete workflow - plan, build, host, and test
argument-hint: [prompt]
---

# Plan → Build → Host → Test

Execute the full workflow for: $ARGUMENTS

## References

- `.claude/skills/agent-sandboxes/SKILL.md` for sandbox operations
- `.claude/skills/playwright/SKILL.md` for browser testing

## Steps

1. **Plan** - Run `/workflow:plan [prompt]`, capture plan path
2. **Build** - Init sandbox, implement plan top-to-bottom, run validation commands
3. **Host** - Start server with `--hostname 0.0.0.0`, get public URL via `get-host`
4. **Test** - Validate DB tables/queries, run unit tests, then browser UI workflows against public URL

## Report

Summary with sandbox ID and public URL.
