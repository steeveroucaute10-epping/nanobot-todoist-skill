#!/usr/bin/env python3
"""
Test script for Todoist MCP skill.
Run with: python test_skill.py
Requires: TODOIST_API_TOKEN environment variable set
"""

import os
import sys

sys.path.insert(0, "src")

# Check for token before importing (which would fail on tool call anyway)
if not os.environ.get("TODOIST_API_TOKEN"):
    print("ERROR: Set TODOIST_API_TOKEN before running.")
    print("  Windows: $env:TODOIST_API_TOKEN = 'your-token'")
    print("  Get token: https://app.todoist.com/prefs/integrations")
    sys.exit(1)

from todoist_mcp.server import create_task, list_projects, create_reminder_task


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


def main():
    print("Testing Todoist MCP skill...")
    results = []
    results.append(("list_projects", test_list_projects()))
    results.append(("create_task", test_create_task()))
    results.append(("create_reminder_task", test_create_reminder_task()))

    print("\n" + "=" * 40)
    passed = sum(1 for _, ok in results if ok)
    print(f"Result: {passed}/{len(results)} tests passed")
    if passed == len(results):
        print("Skill is ready for nanobot!")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
