from langgraph.graph import StateGraph,START,END
from core.states import TaskState
from core.permissions import requires_approval
from agents.planner import plan_task
from agents.security import assess_risk
from audit.logger import audit_log

async def planning_node(task):
    task.state = TaskState.PLANNING
    audit_log(task.task_id,"PLANNING")

    task.summary = await plan_task(task.message)
    return task

def risk_node(task):
    task.risk = assess_risk(task.message)
    audit_log(task.task_id, f"RISK_{task.risk}")
    return task

def approval_gate(task):
    if requires_approval(task.risk):
        task.state = TaskState.AWAITING_APPROVAL
        aduit_log(task.task_id,"AWAITING_APPROVAL")
        return task
    
    task.state = TaskState.COMPLETED
    audit_log(task.task_id,"AUTO_APPROVED")
    return task

graph = StateGraph(object)

graph.add_node("plan",planning_node)
graph.add_node("risk",risk_node)
graph.add_node("approve",approval_gate)

graph.add_edge(START,"plan")
graph.add_edge("plan","risk")
graph.add_edge("risk","approve")
graph.add_edge("approve",END)

workflow = graph.compile()