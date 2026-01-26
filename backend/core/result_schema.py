
from pydantic import BaseModel
from typing import Literal, Any


class ExecutionResult(BaseModel):
    status: Literal["success", "failure"]
    output: Any | None = None
    error: str | None = None
