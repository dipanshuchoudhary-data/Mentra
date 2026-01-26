
import uuid
from core.states import TaskState
from db.firestore import FirestoreDB
from db.models import TaskRecord
from orchestrator.workflow import run_task
from audit.logger import audit_log


class TaskManager:
    def __init__(self):
        self.db = FirestoreDB()

    def create_task(self, user_id: str, message: str) -> TaskRecord:
        task = TaskRecord(
            task_id=str(uuid.uuid4()),
            user_id=user_id,
            message=message,
            state=TaskState.CREATED,
        )
        self.db.save_task(task)
        audit_log(task.task_id, "CREATED", {"user_id": user_id})

        task = run_task(task)
        self.db.update_task(task)
        return task

    def get_task(self, task_id: str, user_id: str) -> TaskRecord:
        task = self.db.get_task(task_id)
        if task.user_id != user_id:
            raise PermissionError("Forbidden")
        return task

    def update_task(self, task: TaskRecord, user_id: str):
        if task.user_id != user_id:
            raise PermissionError("Forbidden")
        self.db.update_task(task)

    def list_tasks(
        self,
        user_id: str,
        limit: int = 10,
        cursor: str | None = None,
    ):
        return self.db.list_tasks(user_id=user_id, limit=limit, cursor=cursor)
