#!/usr/bin/env python3
"""
Run the Todoist MCP server or invoke tools directly from the command line.

Usage:
  python run.py                         # Stdio MCP transport (for nanobot mcpServers config)
  python run.py --http                  # HTTP MCP transport on port 8000
  python run.py list_projects           # CLI: list projects (JSON output)
  python run.py list_tasks_today        # CLI: tasks due today
  python run.py list_tasks_overdue      # CLI: overdue tasks
  python run.py list_tasks_this_week    # CLI: tasks due this week
  python run.py create_task "Title" --due "tomorrow" --priority 3
  python run.py create_reminder "Title" --when "today"

TODOIST_API_TOKEN: On Raspberry Pi, provided via systemd EnvironmentFile.
For local dev/testing, loaded from .env if present (see .env.example).
Works correctly when Nanobot spawns this process from any working directory.
"""

import json
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).parent.resolve()

_env_path = _SKILL_DIR / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        import os
        try:
            for line in _env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip("'\""))
        except Exception:
            pass

_src = _SKILL_DIR / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))


_CLI_COMMANDS = {
    "list_projects", "list_tasks_today", "list_tasks_overdue",
    "list_tasks_this_week", "create_task", "create_reminder",
}


def _parse_cli_args(args: list[str]) -> tuple[str, dict]:
    """Parse CLI arguments into (command, kwargs)."""
    command = args[0]
    positional = []
    kwargs = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i].lstrip("-").replace("-", "_")
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                kwargs[key] = args[i + 1]
                i += 2
            else:
                kwargs[key] = True
                i += 1
        else:
            positional.append(args[i])
            i += 1
    return command, positional, kwargs


def _run_cli(args: list[str]) -> None:
    """Run a tool directly and print JSON result."""
    from todoist_mcp.server import (
        create_task, create_reminder_task, list_projects,
        list_tasks_today, list_tasks_overdue, list_tasks_this_week,
    )

    command, positional, kwargs = _parse_cli_args(args)

    if command == "list_projects":
        result = list_projects()
    elif command == "list_tasks_today":
        result = list_tasks_today()
    elif command == "list_tasks_overdue":
        result = list_tasks_overdue()
    elif command == "list_tasks_this_week":
        result = list_tasks_this_week()
    elif command == "create_task":
        content = positional[0] if positional else kwargs.pop("content", "")
        if not content:
            print(json.dumps({"success": False, "error": "content is required"}))
            sys.exit(1)
        result = create_task(
            content=content,
            due_string=kwargs.get("due"),
            priority=int(kwargs["priority"]) if "priority" in kwargs else None,
            description=kwargs.get("description"),
            project_id=kwargs.get("project_id"),
        )
    elif command == "create_reminder":
        content = positional[0] if positional else kwargs.pop("content", "")
        if not content:
            print(json.dumps({"success": False, "error": "content is required"}))
            sys.exit(1)
        result = create_reminder_task(content=content, when=kwargs.get("when", "today"))
    else:
        print(json.dumps({"success": False, "error": f"Unknown command: {command}"}))
        sys.exit(1)

    print(json.dumps(result, default=str))


def main() -> None:
    args = sys.argv[1:]

    if args and args[0] in _CLI_COMMANDS:
        _run_cli(args)
    else:
        from todoist_mcp.server import mcp
        if "--http" in args:
            mcp.run(transport="streamable-http")
        else:
            mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
