
import os
from execution.mcp_client import MCPExecutionAdapter

def get_execution_adapter():
    return MCPExecutionAdapter(
        server_url=os.getenv("MCP_SERVER_URL", "http://localhost:3333")
    )
