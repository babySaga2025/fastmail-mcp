# Warp Agent Guidelines

## Linear Issue Workflow

When processing requests to review, plan, or implement Linear issues, always follow this workflow:

### 1. Mark Issue as In Progress
Use the Linear MCP integration to update the issue status to "In Progress" before beginning any work.

### 2. Create Feature Branch
Create a new feature branch following the naming convention:
```
feature/DOR-XXX-short-summary
```
Where:
- `DOR-XXX` is the Linear issue identifier (e.g., DOR-123)
- `short-summary` is a brief kebab-case description of the feature/fix

Example: `feature/DOR-456-add-search-filters`

### 3. Implement Changes
- Work on the feature/fix in the newly created branch
- Follow all existing coding standards and testing requirements
- Ensure all changes are properly tested and linted

### 4. Never Auto-Commit
**CRITICAL**: Never commit changes automatically. Always ask the human for review and approval before committing any changes. This includes:
- Individual commits during development
- Final commits before creating PRs
- Any git operations that modify the repository history

### 5. Human Approval Required
Before making any commits:
1. Summarize the changes made
2. Show the human what will be committed
3. Wait for explicit approval to proceed
4. Only commit after receiving clear confirmation

This workflow ensures proper Linear issue tracking, consistent branch naming, and maintains human oversight over all repository changes.