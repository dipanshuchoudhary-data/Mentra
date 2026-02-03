from typing import Dict, Any

from langgraph.graph import StateGraph, START, END

from backend.agents.planner import plan_task
from backend.orchestrator.workflow import execute_tools


# ------------------ condition ------------------

def has_tool_calls(state: Dict[str, Any]) -> bool:
    """
    HARD EXECUTION GATE (code decides, not LLM)

    We keep this function name for compatibility,
    but it no longer checks LLM tool calls.

    It returns True only when:
    - intent == add_expense
    - required slots are present
    """

    intent = state.get("intent")
    slots = state.get("slots") or {}

    if intent != "add_expense":
        return False

    amount = slots.get("amount")
    category = slots.get("category")

    return amount is not None and category is not None


# ------------------ graph ------------------

graph = StateGraph(dict)

graph.add_node("plan", plan_task)
graph.add_node("execute", execute_tools)

# Start → plan
graph.add_edge(START, "plan")

# CRITICAL FIX:
# execute runs ONLY when the system gate allows it
# (NOT when the LLM asks for tools)
graph.add_conditional_edges(
    "plan",
    has_tool_calls,
    {
        True: "execute",
        False: END,
    },
)

# execute → end
graph.add_edge("execute", END)

# Compile workflow
workflow = graph.compile()
