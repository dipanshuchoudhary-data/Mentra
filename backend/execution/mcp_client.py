import os
from typing import Any, Dict

from dotenv import load_dotenv
from fastmcp import Client

load_dotenv()

# ------------------------------------------------------------------
# MCP CLIENT (LONG-LIVED, SSE)
# ------------------------------------------------------------------

MCP_SERVER_URL = os.environ["EXPENSE_MCP_URL"]

# IMPORTANT:
# - transport MUST be positional ("sse")
# - this client must stay alive for the app lifetime
mcp_client = Client(
    MCP_SERVER_URL,
    "sse",
)

_mcp_connected = False


async def ensure_mcp_connected() -> None:
    """
    Ensure MCP SSE session is established exactly once.
    """
    global _mcp_connected

    if not _mcp_connected:
        await mcp_client.__aenter__()
        _mcp_connected = True


# ------------------------------------------------------------------
# EXECUTION ADAPTER (USED BY ORCHESTRATOR / TOOLS)
# ------------------------------------------------------------------

class MCPExecutionAdapter:
    """
    Thin execution adapter used by the orchestrator layer.

    Phase-2:
    - Enforces presence of user_id before any MCP call
    """

    async def execute(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """
        Execute an MCP tool using the active SSE session.
        """

        user_id = args.get("user_id")

        if not user_id:
            raise RuntimeError(
                f"MCPExecutionAdapter.execute called for '{tool_name}' without user_id"
            )

        await ensure_mcp_connected()
        return await mcp_client.session.call_tool(tool_name, args)
