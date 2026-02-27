---
name: todoist
description: Todoist task management integration. You must use this skill for any action that creates, updates, completes, deletes, or queries Todoist tasks, reminders, or projects. Never claim that a Todoist change succeeded unless you have called the appropriate Todoist MCP tool and received a response. Never invent Todoist task IDs. Works via MCP tools (preferred) or exec fallback.
---

# Todoist Integration

Use the Todoist MCP tools when the user asks about reminders, todos, or tasks. If you cannot call the tools or the call fails, clearly say so — do not claim the action was completed.

**Backend:** FastMCP server (`run.py` / `src/todoist_mcp/server.py`). Nanobot spawns it via `tools.mcpServers` in `config.json`. See [references/setup.md](references/setup.md) for full setup.

## MCP tools (preferred)

If the Todoist MCP server is configured in `config.json`, these tools are available directly:

| User intent | MCP tool |
|-------------|----------|
| Create a task with full control (project, due date, priority) | `create_task` |
| Quick reminder ("remind me to X") | `create_reminder_task` |
| See projects or get project ID | `list_projects` |
| "What do I have today?" | `list_tasks_today` |
| "What's overdue?" / "What did I miss?" | `list_tasks_overdue` |
| "What's due this week?" | `list_tasks_this_week` |

### Guidelines

- **create_task**: Use `due_string` for natural dates ("today", "tomorrow", "next monday", "in 2 days"). Omit `project_id` for Inbox.
- **create_reminder_task**: Default `when` is "today". Use for simple reminders.
- Prefer `create_reminder_task` for quick "remind me to X" requests; use `create_task` when the user specifies project, priority, or complex due dates.
- After successfully creating a task, confirm using only the fields returned by the tool (content, project, due date, real task ID). Do not fabricate or guess these values.

## Exec fallback

If the MCP tools above are **not available** (e.g. MCP config missing or server didn't start), use the `exec` tool to call `run.py` directly via its CLI wrapper. Replace paths with the actual install location.

| Action | exec command |
|--------|-------------|
| List projects | `exec: /home/pi/nanobot-venv/bin/python /home/pi/.nanobot/workspace/skills/todoist/run.py list_projects` |
| Tasks today | `exec: /home/pi/nanobot-venv/bin/python /home/pi/.nanobot/workspace/skills/todoist/run.py list_tasks_today` |
| Overdue tasks | `exec: /home/pi/nanobot-venv/bin/python /home/pi/.nanobot/workspace/skills/todoist/run.py list_tasks_overdue` |
| Tasks this week | `exec: /home/pi/nanobot-venv/bin/python /home/pi/.nanobot/workspace/skills/todoist/run.py list_tasks_this_week` |
| Create task | `exec: /home/pi/nanobot-venv/bin/python /home/pi/.nanobot/workspace/skills/todoist/run.py create_task "Buy milk" --due "tomorrow"` |
| Quick reminder | `exec: /home/pi/nanobot-venv/bin/python /home/pi/.nanobot/workspace/skills/todoist/run.py create_reminder "Call dentist" --when "today"` |

If exec is used, parse the JSON output to extract results.
