
import asyncio
from orchestrator.graph import workflow
from audit.logger import audit_log
from core.states import TaskState

def run_task(task):
    audit_log(task.task_id, "WORKFLOW_START")
    result = asyncio.run(workflow.ainvoke(task))
    audit_log(task.task_id, "WORKFLOW_END")
    return result

def resume_after_approval(task):
    if task.state != TaskState.AWAITING_APPROVAL:
        return task
    audit_log(task.task_id, "RESUME_AFTER_APPROVAL")
    task.state = TaskState.EXECUTING
    return asyncio.run(workflow.ainvoke(task))
