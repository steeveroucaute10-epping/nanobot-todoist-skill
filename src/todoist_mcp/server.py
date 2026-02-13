"""
Todoist MCP Server for Nanobot.

Exposes Todoist API functionality as MCP tools so nanobot can create
and manage todos when reminding the user about items.
"""

import os
from typing import Optional

from mcp.server.fastmcp import FastMCP
from todoist_api_python.api import TodoistAPI

# Initialize FastMCP server
mcp = FastMCP("Todoist")


def _get_api() -> TodoistAPI:
    """Get Todoist API client with token from environment."""
    token = os.environ.get("TODOIST_API_TOKEN")
    if not token:
        raise ValueError(
            "TODOIST_API_TOKEN environment variable is not set. "
            "Get your API token from https://app.todoist.com/prefs/integrations"
        )
    return TodoistAPI(token)


@mcp.tool()
def create_task(
    content: str,
    project_id: Optional[str] = None,
    due_string: Optional[str] = None,
    priority: Optional[int] = None,
    description: Optional[str] = None,
) -> dict:
    """
    Create a new task in Todoist.

    Use this when the user wants to be reminded of something, add an item to their
    todo list, or create a task. Nanobot can invoke this when the user says things
    like "remind me to..." or "add to my todo list...".

    Args:
        content: The task content/title (required). Be concise and actionable.
        project_id: Optional project ID. If not provided, task goes to Inbox.
        due_string: Optional due date. Supports natural language: "today", "tomorrow",
            "next monday", "in 2 days", "2025-02-15", etc.
        priority: Optional priority 1-4 (1=normal, 2=medium, 3=high, 4=urgent).
        description: Optional longer description for the task.

    Returns:
        The created task details including id, url, and content.
    """
    api = _get_api()
    kwargs = {"content": content, "labels": ["nanobot"]}
    if project_id:
        kwargs["project_id"] = project_id
    if due_string:
        kwargs["due_string"] = due_string
    if priority is not None and 1 <= priority <= 4:
        kwargs["priority"] = priority
    if description:
        kwargs["description"] = description

    try:
        task = api.add_task(**kwargs)
        return {
            "success": True,
            "id": task.id,
            "content": task.content,
            "url": task.url,
            "due": str(task.due) if task.due else None,
            "priority": getattr(task, "priority", None),
            "message": f"Created task: {task.content}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create task: {e}",
        }


@mcp.tool()
def list_projects() -> dict:
    """
    List all Todoist projects.

    Use this to help the user choose which project to add a task to,
    or to get project IDs for the create_task tool.

    Returns:
        List of projects with id, name, and whether it's the inbox.
    """
    api = _get_api()
    try:
        # get_projects() returns Iterator[list[Project]] in todoist-api-python 3.x
        all_projects = [p for batch in api.get_projects() for p in batch]
        return {
            "success": True,
            "projects": [
                {
                    "id": p.id,
                    "name": p.name,
                    "is_inbox": getattr(p, "is_inbox_project", False),
                }
                for p in all_projects
            ],
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to list projects: {e}",
        }


@mcp.tool()
def create_reminder_task(content: str, when: str = "today") -> dict:
    """
    Create a task optimized for reminders - quick and simple.

    Use when nanobot needs to remind the user of something. This is a convenience
    wrapper that creates a task with a due date.

    Args:
        content: What to be reminded about (e.g., "Call the dentist").
        when: When to be reminded. Default "today". Supports: "today", "tomorrow",
            "next week", "in 2 hours", etc.

    Returns:
        The created task details.
    """
    return create_task(content=content, due_string=when)


def _list_tasks_with_filter(filter_query: str) -> dict:
    """Fetch tasks matching a Todoist filter query. Returns standardized task list."""
    api = _get_api()
    try:
        # filter_tasks() returns Iterator[list[Task]] in todoist-api-python 3.x
        all_tasks = [t for batch in api.filter_tasks(query=filter_query) for t in batch]
        return {
            "success": True,
            "tasks": [
                {
                    "id": t.id,
                    "content": t.content,
                    "url": t.url,
                    "due": str(t.due) if t.due else None,
                    "priority": getattr(t, "priority", None),
                    "project_id": getattr(t, "project_id", None),
                }
                for t in all_tasks
            ],
            "count": len(all_tasks),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to list tasks: {e}",
        }


@mcp.tool()
def list_tasks_today() -> dict:
    """
    List tasks due today.

    Use when the user asks what they need to do today, what's on their plate today,
    or what tasks are due today.

    Returns:
        List of tasks with id, content, url, due date, and priority.
    """
    return _list_tasks_with_filter("today")


@mcp.tool()
def list_tasks_overdue() -> dict:
    """
    List overdue tasks (past their due date).

    Use when the user asks about late tasks, overdue items, or what they've missed.

    Returns:
        List of tasks with id, content, url, due date, and priority.
    """
    return _list_tasks_with_filter("overdue")


@mcp.tool()
def list_tasks_this_week() -> dict:
    """
    List tasks due this week (including today and overdue).

    Use when the user asks what they need to do this week, their weekly tasks,
    or what's coming up this week.

    Returns:
        List of tasks with id, content, url, due date, and priority.
    """
    return _list_tasks_with_filter("due before: next week")
