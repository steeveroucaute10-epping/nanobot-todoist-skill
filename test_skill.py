#!/usr/bin/env python3
"""
Test script for Todoist MCP skill.
Run with: python test_skill.py
Loads TODOIST_API_TOKEN from .env (or environment variable)
"""

import os
import sys
from pathlib import Path

# Load .env before anything else
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        pass  # dotenv optional if token set via env

sys.path.insert(0, "src")

# Check for token
token = os.environ.get("TODOIST_API_TOKEN")
if not token or token == "your-api-token-here":
    print("ERROR: Set TODOIST_API_TOKEN before running.")
    print("  Edit .env and replace 'your-api-token-here' with your token")
    print("  Or: $env:TODOIST_API_TOKEN = 'your-token'")
    print("  Get token: https://app.todoist.com/prefs/integrations")
    sys.exit(1)

from todoist_mcp.server import (
    create_task,
    create_reminder_task,
    list_projects,
    list_tasks_overdue,
    list_tasks_this_week,
    list_tasks_today,
)


def test_list_projects():
    """Test listing projects."""
    print("\n--- Testing list_projects ---")
    result = list_projects()
    if result.get("success"):
        print("OK - Projects:", [p["name"] for p in result["projects"]])
        return True
    else:
        print("FAILED:", result.get("error", result))
        return False


def test_create_task():
    """Test creating a task (uses Inbox)."""
    print("\n--- Testing create_task ---")
    result = create_task(
        content="[Test] Nanobot skill verification - delete me",
        due_string="today",
    )
    if result.get("success"):
        print("OK - Created:", result["content"])
        print("    URL:", result.get("url"))
        return True
    else:
        print("FAILED:", result.get("error", result))
        return False


def test_create_reminder_task():
    """Test the reminder shortcut."""
    print("\n--- Testing create_reminder_task ---")
    result = create_reminder_task(
        content="[Test] Reminder verification - delete me",
        when="tomorrow",
    )
    if result.get("success"):
        print("OK - Created reminder:", result["content"])
        return True
    else:
        print("FAILED:", result.get("error", result))
        return False


def test_create_task_with_params():
    """Test create_task with specific date, description, and priority."""
    print("\n--- Testing create_task (date, description, priority) ---")
    result = create_task(
        content="[Test] Full params verification - delete me",
        due_string="next friday",
        priority=3,  # high
        description="Test reminder note - verify all params work",
    )
    if not result.get("success"):
        print("FAILED:", result.get("error", result))
        return False
    # Verify all params were applied
    due_str = str(result.get("due", ""))
    has_due = "2026" in due_str or "2025" in due_str  # due date was parsed
    has_priority = result.get("priority") == 3
    if not has_due:
        print("  WARN: due date not set or not parsed")
    if not has_priority:
        print("  WARN: expected priority 3, got", result.get("priority"))
    print("OK - Created:", result["content"])
    print("    Due:", due_str[:50] + "..." if len(due_str) > 50 else due_str, "| Priority:", result.get("priority"))
    return has_due and has_priority


def test_list_tasks_today():
    """Test listing tasks due today."""
    print("\n--- Testing list_tasks_today ---")
    result = list_tasks_today()
    if not result.get("success"):
        print("FAILED:", result.get("error", result))
        return False
    tasks = result.get("tasks", [])
    print("OK - Tasks today:", len(tasks), "|", [t["content"][:30] for t in tasks[:5]])
    return True


def test_list_tasks_overdue():
    """Test listing overdue tasks."""
    print("\n--- Testing list_tasks_overdue ---")
    result = list_tasks_overdue()
    if not result.get("success"):
        print("FAILED:", result.get("error", result))
        return False
    tasks = result.get("tasks", [])
    print("OK - Overdue tasks:", len(tasks), "|", [t["content"][:30] for t in tasks[:5]])
    return True


def test_list_tasks_this_week():
    """Test listing tasks due this week."""
    print("\n--- Testing list_tasks_this_week ---")
    result = list_tasks_this_week()
    if not result.get("success"):
        print("FAILED:", result.get("error", result))
        return False
    tasks = result.get("tasks", [])
    print("OK - Tasks this week:", len(tasks), "|", [t["content"][:30] for t in tasks[:5]])
    return True


def main():
    print("Testing Todoist MCP skill...")
    results = []
    results.append(("list_projects", test_list_projects()))
    results.append(("list_tasks_today", test_list_tasks_today()))
    results.append(("list_tasks_overdue", test_list_tasks_overdue()))
    results.append(("list_tasks_this_week", test_list_tasks_this_week()))
    results.append(("create_task", test_create_task()))
    results.append(("create_task_with_params", test_create_task_with_params()))
    results.append(("create_reminder_task", test_create_reminder_task()))

    print("\n" + "=" * 40)
    passed = sum(1 for _, ok in results if ok)
    print(f"Result: {passed}/{len(results)} tests passed")
    if passed == len(results):
        print("Skill is ready for nanobot!")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
