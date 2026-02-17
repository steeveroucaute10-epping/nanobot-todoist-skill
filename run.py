#!/usr/bin/env python3
"""
Run the Todoist MCP server.

Usage:
  python run.py           # Stdio transport (for nanobot command config)
  python run.py --http    # HTTP transport on port 8000

Loads TODOIST_API_TOKEN from .env if present.
Works correctly when Nanobot spawns this process from any working directory.
"""

import sys
from pathlib import Path

# Resolve skill directory (parent of this script) - works when Nanobot runs from any cwd
_SKILL_DIR = Path(__file__).parent.resolve()

# Load .env from skill directory for local development
_env_path = _SKILL_DIR / ".env"
if _env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass

# Ensure src is on path (for development / non-installed runs)
_src = _SKILL_DIR / "src"
if _src.exists() and str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from todoist_mcp.server import mcp


def main() -> None:
    if "--http" in sys.argv:
        # Streamable HTTP - defaults to port 8000, endpoint at /mcp
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
