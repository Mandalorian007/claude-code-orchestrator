---
description: Create a full-stack implementation plan
argument-hint: [prompt]
---

# Plan

Create an implementation plan for: $ARGUMENTS

If no prompt provided, stop and ask.

## Stack

- Next.js 15 (App Router) + TypeScript
- Shadcn/ui + Tailwind CSS
- SQLite (better-sqlite3)

## Output

Save to `specs/<kebab-case-name>.md`

## Plan Format

```md
# Plan: <name>

## Objective
<what will be accomplished - running Next.js app with API routes and SQLite persistence>

## Project Structure
```
app/
├── layout.tsx
├── page.tsx
├── globals.css
├── api/
│   └── [resource]/
│       └── route.ts
├── [feature]/
│   └── page.tsx
components/
├── ui/
└── [feature]/
lib/
├── db.ts
└── utils.ts
```

## Dependencies
```bash
pnpm create next-app@latest . --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button card input label table dialog
pnpm add better-sqlite3
pnpm add -D @types/better-sqlite3
```

## Steps

### 1. Bootstrap & Verify
- Create Next.js app
- Initialize Shadcn/ui
- Install SQLite
- Run dev server to verify

### 2. Database Setup
- Create `lib/db.ts` with connection
- Define schema, create tables
- Add seed data if needed

### 3. API Routes
- Create route handlers in `app/api/`
- Implement CRUD operations
- Add validation and error handling

### 4. UI Components
- Build layouts and navigation
- Create feature components
- Wire to API routes
- Add loading/error states

### 5. Testing & Verification
- Test API routes with curl
- Run `pnpm build`
- Verify user flows

## Browser UI Testing

<3-5 workflows validating core features, 3-8 steps each>

### User Story Workflow 1: <Feature Name>
<one-sentence description>

- [] Open public URL
- [] <action: click, type, scroll, etc.>
- [] <action>
- [] CONFIRM: <expected outcome>

### User Story Workflow 2: <Feature Name>
...

## Validation Commands
```bash
pnpm build
pnpm dev
curl http://localhost:3000/api/[resource]
```

## Acceptance Criteria
<specific, measurable criteria for completion>
```
