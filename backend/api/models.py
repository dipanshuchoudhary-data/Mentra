
from pydantic import BaseModel
from backend.core.states import TaskState


class TaskResponse(BaseModel):
    task_id: str
    user_id: str
    message: str
    state: TaskState
    summary: str | None = None
    risk: str | None = None
    execution_result: dict | None = None
    error: str | None = None


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    next_cursor: str | None = None
