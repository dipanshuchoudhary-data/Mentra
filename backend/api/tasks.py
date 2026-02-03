from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel

from backend.core.task_manager import TaskManager
from backend.api.dependencies import guarded
from backend.api.models import TaskResponse, TaskListResponse

router = APIRouter()
manager = TaskManager()


class TaskCreate(BaseModel):
    message: str


@router.post("/", response_model=TaskResponse)
def create_task(
    req: TaskCreate,
    user_id: str = Depends(guarded),
):
    task = manager.create_task(user_id=user_id, message=req.message)
    return task.model_dump()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    user_id: str = Depends(guarded),
):
    try:
        task = manager.get_task(task_id, user_id)
        return task.model_dump()
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("/", response_model=TaskListResponse)
def list_tasks(
    limit: int = Query(10, le=50),
    cursor: str | None = Query(None),
    user_id: str = Depends(guarded),
):
    tasks, next_cursor = manager.list_tasks(
        user_id=user_id,
        limit=limit,
        cursor=cursor,
    )
    return {
        "tasks": [t.model_dump() for t in tasks],
        "next_cursor": next_cursor,
    }
