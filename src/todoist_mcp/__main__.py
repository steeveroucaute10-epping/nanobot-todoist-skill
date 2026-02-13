"""
Entry point for running the Todoist MCP server.

Supports both stdio (for nanobot command-based config) and streamable HTTP.
"""

import sys

from .server import mcp


def main() -> None:
    """Run the MCP server."""
    if "--http" in sys.argv:
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
