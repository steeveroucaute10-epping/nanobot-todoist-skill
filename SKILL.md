---
name: todoist
description: Todoist task management integration. Use when the user (1) wants to be reminded of something, add an item to their todo list, or create a task; (2) asks what they have due today, what's overdue, or what's due this week; (3) wants to see their projects or add a task to a specific project. Requires the Todoist MCP server to be configured in Nanobot.
---

# Todoist Integration

Use the Todoist MCP tools when the user asks about reminders, todos, or tasks.

**Configuration:** See [references/setup.md](references/setup.md).

## Tool selection

| User intent | Tool |
|-------------|------|
| Create a task with full control (project, due date, priority) | `create_task` |
| Quick reminder ("remind me to X") | `create_reminder_task` |
| See projects or get project ID | `list_projects` |
| "What do I have today?" | `list_tasks_today` |
| "What's overdue?" / "What did I miss?" | `list_tasks_overdue` |
| "What's due this week?" | `list_tasks_this_week` |

## Guidelines

- **create_task**: Use `due_string` for natural dates ("today", "tomorrow", "next monday", "in 2 days"). Omit `project_id` for Inbox.
- **create_reminder_task**: Default `when` is "today". Use for simple reminders.
- Prefer `create_reminder_task` for quick "remind me to X" requests; use `create_task` when the user specifies project, priority, or complex due dates.
