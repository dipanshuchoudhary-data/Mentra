from typing import Any, Dict

from backend.execution.mcp_client import ensure_mcp_connected, mcp_client


class MCPExecutor:
    """
    Phase-2 hardened MCP executor.

    Guarantees:
    - user_id is always present
    - tools can never be called without identity
    """

    async def execute(self, tool_name: str, args: Dict[str, Any]) -> Any:
        user_id = args.get("user_id")

        if not user_id:
            raise RuntimeError(
                f"MCP tool '{tool_name}' called without user_id"
            )

        await ensure_mcp_connected()
        return await mcp_client.session.call_tool(tool_name, args)


mcp_executor = MCPExecutor()
