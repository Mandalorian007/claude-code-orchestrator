---
description: Creates a full-stack engineering implementation plan using Next.js and saves it to specs directory
argument-hint: [user_prompt]
---

# Quick Plan

Create a detailed implementation plan for a net-new full stack application based on the `USER_PROMPT`. This uses a standardized, pre-validated stack optimized for the E2B sandbox environment. Think deeply and produce a comprehensive specification in `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that another engineer can implement directly. Ensure the plan includes real validation steps—assume the agent has already run the generated application once to confirm it boots before detailing tests.

## Variables

USER_PROMPT: $1
FRAMEWORK: `next.js 15 app-router typescript` (static default)
UI_LIBRARY: `shadcn/ui tailwindcss` (static default)
DATABASE: `sqlite better-sqlite3` (static default)
PLAN_OUTPUT_DIRECTORY: `<your temp directory>/specs/`
BROWSER_UI_TESTING_STEPS_PER_WORKFLOW: 3-8 (static default)
BROWSER_UI_TESTING_TOTAL_WORKFLOWS: 3-5 (static default)

## Instructions

- IMPORTANT: If no `USER_PROMPT` is provided, stop and ask the user to provide it.
- Carefully analyze the user's requirements provided in the USER_PROMPT variable and expand them into a full-stack scope (pages, API routes, database).
- Determine the task type (chore|feature|refactor|fix|enhancement) and complexity (simple|medium|complex).
- Use the standardized stack: **Next.js 15 (App Router) + TypeScript + Shadcn/ui + Tailwind CSS** with **SQLite (better-sqlite3)** for persistence. This is a unified full-stack framework—no separate backend process needed.
- Think deeply (ultrathink) about architecture, data flow, and component structure. Next.js API routes handle backend logic in the same codebase.
- Include a dependencies section detailing required packages (with `npm` or `npx` commands).
- Define how to test API routes, components, and database operations. Assume the agent has already run the application once so we know the scaffold works; testing should include real runs, not hypothetical steps.
- Follow the Plan Format below to create a comprehensive implementation plan, saving it to `PLAN_OUTPUT_DIRECTORY/<descriptive-name>.md`.
- Generate a descriptive, kebab-case filename based on the main topic of the plan.
- Ensure the plan is detailed enough that another developer could follow it to implement the solution.
- Consider edge cases, error handling, performance, and scalability concerns.
- BROWSER_UI_TESTING_TOTAL_WORKFLOWS is the total number of user-story workflows to define for browser-based validation.
- BROWSER_UI_TESTING_STEPS_PER_WORKFLOW is the number of UI interaction steps to define for each user-story workflow.
- When writing `### 6. Browser UI Testing` section, craft user-stories against the critical paths of the application. Focus on the 80/20 of the application working.

## Workflow

1. Analyze Requirements - THINK HARD and parse the USER_PROMPT to understand the desired features, user journeys, and constraints.
2. Confirm Stack - Use the standardized stack (Next.js 15 + Shadcn/ui + SQLite) and note any prerequisites.
3. Define Structure - Map out the app directory structure, API routes, components, and database schema.
4. Design Solution - Develop architecture, API surface, data models, and UI composition.
5. Document Plan - Write the structured markdown with phases, tasks, dependencies, and testing.
6. Generate Filename - Create a descriptive kebab-case filename based on the plan's main topic.
7. Browser UI Testing - Define user-story workflows for browser-based validation. Each workflow should have BROWSER_UI_TESTING_STEPS_PER_WORKFLOW steps that validate ONE specific user feature through actual UI interactions.
8. Save & Report - Follow the `Report` section to write the plan to `PLAN_OUTPUT_DIRECTORY/<filename>.md` and provide a summary of key components.

## Plan Format

Follow this format when creating implementation plans:

```md
# Plan: <task name>

## Task Description
<describe the net-new full stack app based on the prompt; stack: Next.js 15 (App Router) + Shadcn/ui + Tailwind + SQLite>

## Objective
<clearly state what will be accomplished when this plan is complete (running Next.js app with API routes and SQLite persistence)>

<if task_type is feature or complexity is medium/complex, include these sections:>
## Problem Statement
<define the specific problem or opportunity this app addresses>

## Solution Approach
<describe the proposed solution approach, architecture, and how it addresses the objective; include data flow from UI → API route → database>
</if>

## Relevant Files
Use these files and directories to complete the task:

<list files with bullet points explaining their purpose. Include the 'cp .env' command to copy the .env file into the sandbox if you need API keys.>

### Project Structure
```
app/
├── layout.tsx              # Root layout with providers
├── page.tsx                # Home page
├── globals.css             # Tailwind + custom styles
├── api/
│   └── [resource]/
│       └── route.ts        # API route handlers (GET, POST, PUT, DELETE)
├── [feature]/
│   └── page.tsx            # Feature pages
components/
├── ui/                     # Shadcn components
└── [feature]/              # Feature-specific components
lib/
├── db.ts                   # SQLite connection and queries
└── utils.ts                # Shared utilities
```

### New Files
- <list key files to create with brief descriptions>
- <.env.local file with any API keys needed>

### Dependencies
```bash
# Create Next.js app with TypeScript and Tailwind
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"

# Add Shadcn/ui
npx shadcn@latest init
npx shadcn@latest add button card input label table dialog

# Add SQLite
npm install better-sqlite3
npm install -D @types/better-sqlite3

# Add any additional dependencies
npm install <other-deps>
```

<if complexity is medium/complex, include this section:>
## Implementation Phases
### Phase 1: Foundation
<scaffold Next.js project, initialize Shadcn/ui, set up SQLite database schema, and run dev server to confirm it boots>

### Phase 2: Core Implementation
<implement database operations, API routes, and UI components for core features>

### Phase 3: Polish
<add error handling, loading states, form validation, and UI polish>
</if>

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

<list step by step tasks as h3 headers with bullet points>

### 1. Bootstrap & Verify Stack
- Create Next.js app: `npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir=false --import-alias="@/*"`
- Initialize Shadcn/ui: `npx shadcn@latest init` (select defaults)
- Add required Shadcn components: `npx shadcn@latest add button card input ...`
- Install SQLite: `npm install better-sqlite3 && npm install -D @types/better-sqlite3`
- Run dev server to verify: `npm run dev`

### 2. Database Setup
- Create `lib/db.ts` with SQLite connection
- Define schema and create tables
- Add seed data if needed
- Test database operations

### 3. API Routes
- Create API route handlers in `app/api/`
- Implement CRUD operations
- Add input validation and error handling
- Test endpoints with curl

### 4. UI Components
- Build page layouts and navigation
- Create feature components using Shadcn/ui
- Wire components to API routes
- Add loading and error states

### 5. Testing & Verification
- Test all API routes: `curl http://localhost:3000/api/...`
- Run build to check for errors: `npm run build`
- Verify full user flows work end-to-end

<if task_type is feature or complexity is medium/complex, include this section:>
## Testing Strategy
- API Routes: Test each endpoint with curl, verify response codes and data
- Database: Verify schema, test CRUD operations, check data persistence
- UI: Verify components render, forms submit, data displays correctly
</if>

### 6. Browser UI Testing

Define `BROWSER_UI_TESTING_TOTAL_WORKFLOWS` total user-story workflows for browser-based validation. Each workflow validates ONE specific user feature through `BROWSER_UI_TESTING_STEPS_PER_WORKFLOW` UI interaction steps.

<for each core user feature, create workflows following this template:>

### User Story Workflow <N>: <Feature Name>
<one-sentence description of what this workflow validates>

- [] Open public URL at `<url>`
- [] <UI action: click, type, select, scroll, etc.>
- [] <UI action>
- [] <UI action - repeat BROWSER_UI_TESTING_STEPS_PER_WORKFLOW times>
- [] CONFIRM: <expected visual/functional outcome>

<example ui validation workflows - replace with actual features from the app:>

### User Story Workflow 1: Create New Item
Validates that a user can successfully create and see a new item in the list.

- [] Open public URL at `https://3000-<sandbox_id>.e2b.app`
- [] Click "Add New" button
- [] Fill in the form fields (name, description)
- [] Click "Save" button
- [] CONFIRM: New item appears in the list with correct data

### User Story Workflow 2: Edit Existing Item
Validates that a user can modify an existing item.

- [] Open public URL and locate an existing item
- [] Click the "Edit" button on the item
- [] Modify one or more fields
- [] Click "Update" button
- [] CONFIRM: Item displays updated values

### User Story Workflow 3: Delete Item
Validates that a user can remove an item.

- [] Open public URL and locate an existing item
- [] Click the "Delete" button
- [] Confirm deletion in the modal/prompt
- [] CONFIRM: Item is removed from the list

<add additional workflows as needed based on the app's core features>

</example ui validation workflows>

## Acceptance Criteria
<list specific, measurable criteria that must be met for the task to be considered complete>

## Validation Commands
Execute these commands to validate the task is complete:

```bash
# Build the application (catches TypeScript and build errors)
npm run build

# Start production server
npm run start

# Or run dev server
npm run dev

# Test API endpoints
curl http://localhost:3000/api/[resource]
curl -X POST http://localhost:3000/api/[resource] -H "Content-Type: application/json" -d '{"field": "value"}'
```

## Notes
<additional context, dependencies, or deployment considerations>
```

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```
✅ Implementation Plan Created

File: PLAN_OUTPUT_DIRECTORY/<filename>.md
Topic: <brief description of what the plan covers>
Key Components:
- <main component 1>
- <main component 2>
- <main component 3>
- <number of user story workflows defined>
```
