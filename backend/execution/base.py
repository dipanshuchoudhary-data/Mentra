from abc import ABC, abstractmethod

class ExecutionResult(dict):
    pass


class ExecutionAdapter(ABC):
    @abstractmethod
    async def execute(self, task_id: str, payload: dict) -> ExecutionResult:
        ...
