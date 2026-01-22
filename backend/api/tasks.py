from fastapi import FastAPI
from pydantic import BaseModel
from core.task_manager import TaskManager
from core.state import TaskState

router = APIRouter()
task_manager = TaskManager()

class CreateTaskRequest(BaseModel):
    user_id:str
    message:str

@router.post("/create")
async def create_task(req: CreateTaskRequest):
    task = task_manager.create_task(
        user_id=req.user_id,
        message = req.message
    )

    return{
        "task_id":task.task_id,
        "state":task.state,
        "summary":task.summary
    }

@router.get("/{task_id}")
async def get_task(task_id:str):
    task = task_manager.get_task(task_id)
    return task.model_dump()