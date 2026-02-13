#!/usr/bin/env python3
"""
Run the Todoist MCP server.

Usage:
  python run.py           # Stdio transport (for nanobot command config)
  python run.py --http    # HTTP transport on port 8000

Loads TODOIST_API_TOKEN from .env if present.
"""

import sys
from pathlib import Path

# Load .env for local development
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
    except ImportError:
        pass

# Add src to path for development
sys.path.insert(0, "src")

from todoist_mcp.server import mcp


def main() -> None:
    if "--http" in sys.argv:
        # Streamable HTTP - defaults to port 8000, endpoint at /mcp
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
