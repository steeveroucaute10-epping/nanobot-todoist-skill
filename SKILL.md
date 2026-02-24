---
name: todoist
description: Todoist task management integration. You must use this skill for any action that creates, updates, completes, deletes, or queries Todoist tasks, reminders, or projects. Never claim that a Todoist change succeeded unless you have called the appropriate Todoist MCP tool and received a response. Never invent Todoist task IDs.
---

# Todoist Integration

Use the Todoist MCP tools when the user asks about reminders, todos, or tasks. If you cannot call the tools or the call fails, clearly say so — do not claim the action was completed.

**Backend:** Python MCP server (`run.py`). Nanobot spawns it via config. See [references/setup.md](references/setup.md) for `pip install`, `python run.py` path, and systemd env.

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
- After successfully creating a task, confirm using only the fields returned by the tool (content, project, due date, real task ID). Do not fabricate or guess these values.
