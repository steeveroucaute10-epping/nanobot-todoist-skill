#!/usr/bin/env python3
"""
Test script for Todoist MCP skill.
Run with: python test_skill.py
Loads TODOIST_API_TOKEN from .env (or environment variable)
"""

import os
import sys
from pathlib import Path

# Resolve skill directory (same as run.py) so tests work from any CWD
_SKILL_DIR = Path(__file__).parent.resolve()
env_path = _SKILL_DIR / ".env"

# Load .env before anything else
_dotenv_loaded = False
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        _dotenv_loaded = True
    except ImportError:
        # No python-dotenv: try reading .env manually for TODOIST_API_TOKEN
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("TODOIST_API_TOKEN=") and not line.startswith("#"):
                    value = line.split("=", 1)[1].strip().strip("'\"")
                    if value and value != "your-api-token-here":
                        os.environ["TODOIST_API_TOKEN"] = value
                        _dotenv_loaded = True
                    break
        except Exception:
            pass

# Ensure src is on path (for running from any directory)
_src = _SKILL_DIR / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

# Check for token
token = os.environ.get("TODOIST_API_TOKEN")
if not token or token.strip() == "" or token == "your-api-token-here":
    print("ERROR: Set TODOIST_API_TOKEN before running.")
    print("  .env path checked:", env_path)
    print("  .env exists:", env_path.exists())
    if env_path.exists():
        print("  Use exactly one line in .env:  TODOIST_API_TOKEN=your-token-here")
        print("  (no spaces around =, no quotes unless token has spaces)")
    print("  Or set in shell: $env:TODOIST_API_TOKEN = 'your-token'  (PowerShell)")
    print("  Get token: https://app.todoist.com/prefs/integrations")
    sys.exit(1)

from todoist_mcp.server import (
    complete_task,
    create_task,
    create_reminder_task,
    list_projects,
    list_tasks_by_filter,
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


def test_list_tasks_by_filter():
    """Test listing tasks with a custom filter query."""
    print("\n--- Testing list_tasks_by_filter (due: tomorrow) ---")
    result = list_tasks_by_filter(filter_query="due: tomorrow")
    if not result.get("success"):
        print("FAILED:", result.get("error", result))
        return False
    tasks = result.get("tasks", [])
    print("OK - Tasks due tomorrow:", len(tasks), "|", [t["content"][:30] for t in tasks[:5]])
    return True


def test_complete_task():
    """Test completing a task: create one, then complete it."""
    print("\n--- Testing complete_task ---")
    create_result = create_task(
        content="[Test] Complete-me verification - delete me",
        due_string="today",
    )
    if not create_result.get("success"):
        print("FAILED creating task:", create_result.get("error", create_result))
        return False
    task_id = create_result["id"]
    result = complete_task(task_id=task_id)
    if result.get("success"):
        print("OK - Completed task", task_id)
        return True
    else:
        print("FAILED:", result.get("error", result))
        return False


def main():
    print("Testing Todoist MCP skill...")
    results = []
    results.append(("list_projects", test_list_projects()))
    results.append(("list_tasks_today", test_list_tasks_today()))
    results.append(("list_tasks_overdue", test_list_tasks_overdue()))
    results.append(("list_tasks_this_week", test_list_tasks_this_week()))
    results.append(("list_tasks_by_filter", test_list_tasks_by_filter()))
    results.append(("complete_task", test_complete_task()))
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
