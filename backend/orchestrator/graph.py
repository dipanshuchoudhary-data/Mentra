# backend/orchestrator/graph.py
from langgraph.graph import StateGraph,START,END
from core.states import TaskState
from core.permissions import requires_approval
from agents.planner import plan_task
from agents.security import assess_risk
from execution.registry import get_execution_adapter
from core.verification import verify_execution
from audit.logger import audit_log

async def planning_node(task):
    task.state = TaskState.PLANNING
    task.summary = await plan_task(task.message)
    audit_log(task.task_id, "PLANNED")
    return task

def risk_node(task):
    task.risk = assess_risk(task.message)
    audit_log(task.task_id, f"RISK_{task.risk}")
    return task

def approval_gate(task):
    if requires_approval(task.risk):
        task.state = TaskState.AWAITING_APPROVAL
        audit_log(task.task_id, "AWAITING_APPROVAL")
        return task
    task.state = TaskState.EXECUTING
    return task

async def execution_node(task):
    adapter = get_execution_adapter()
    audit_log(task.task_id, "EXECUTION_START")

    task.execution_result = await adapter.execute(
        task_id=task.task_id,
        payload={
            "message": task.message,
            "plan": task.summary,
        },
    )

    task.state = TaskState.VERIFYING
    audit_log(task.task_id, "EXECUTION_DONE")
    return task

def verify_node(task):
    return verify_execution(task)

graph = StateGraph(object)

graph.add_node("plan", planning_node)
graph.add_node("risk", risk_node)
graph.add_node("approve", approval_gate)
graph.add_node("execute", execution_node)
graph.add_node("verify", verify_node)

graph.set_entry_point(START,"plan")
graph.add_edge("plan", "risk")
graph.add_edge("risk", "approve")
graph.add_edge("approve", "execute")
graph.add_edge("execute", "verify")
graph.add_edge("verify",END)

workflow = graph.compile()
