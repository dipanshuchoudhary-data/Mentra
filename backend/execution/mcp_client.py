
from execution.base import ExecutionAdapter, ExecutionResult
from fastmcp import Client as FastMCPClient


class MCPExecutionAdapter(ExecutionAdapter):
    def __init__(self, server_url: str):
        self.client = FastMCPClient(server_url)

    async def execute(self, task_id: str, payload: dict) -> ExecutionResult:
        result = await self.client.call(
            "execute",
            task_id=task_id,
            payload=payload,
        )
        return ExecutionResult(result)
