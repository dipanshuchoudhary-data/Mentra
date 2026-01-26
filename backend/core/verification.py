
from core.states import TaskState
from core.result_schema import ExecutionResult
from audit.logger import audit_log


def verify_execution(task):
    result = ExecutionResult(**task.execution_result)

    if result.status == "success":
        task.state = TaskState.COMPLETED
        audit_log(task.task_id, "VERIFICATION_SUCCESS")
        return task

    task.state = TaskState.FAILED
    task.error = result.error
    audit_log(task.task_id, "VERIFICATION_FAILED")
    return task
