
from fastapi import APIRouter, HTTPException, Depends

from backend.core.states import TaskState
from backend.core.task_manager import TaskManager
from backend.orchestrator.workflow import resume_after_approval
from backend.audit.logger import audit_log
from backend.api.dependencies import guarded
from backend.api.models import TaskResponse


router = APIRouter()
manager = TaskManager()


@router.post("/{task_id}/approve", response_model=TaskResponse)
def approve(
    task_id: str,
    user_id: str = Depends(guarded),
):
    try:
        task = manager.get_task(task_id, user_id)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")

    if task.state != TaskState.AWAITING_APPROVAL:
        raise HTTPException(status_code=400, detail="Not awaiting approval")

    audit_log(task.task_id, "USER_APPROVED", {"user_id": user_id})
    task = resume_after_approval(task)
    manager.update_task(task, user_id)
    return task.model_dump()


@router.post("/{task_id}/reject", response_model=TaskResponse)
def reject(
    task_id: str,
    user_id: str = Depends(guarded),
):
    try:
        task = manager.get_task(task_id, user_id)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Forbidden")

    if task.state != TaskState.AWAITING_APPROVAL:
        raise HTTPException(status_code=400, detail="Not awaiting approval")

    task.state = TaskState.BLOCKED
    audit_log(task.task_id, "USER_REJECTED", {"user_id": user_id})
    manager.update_task(task, user_id)
    return task.model_dump()
