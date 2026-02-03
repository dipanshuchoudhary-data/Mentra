from typing import Dict, Any

from backend.execution.mcp_executor import mcp_executor
from backend.llm.client import get_llm_client


CONFIRMATION_SYSTEM_PROMPT = (
    "You have successfully completed the requested operation.\n"
    "Confirm the result to the user in ONE short, clear sentence.\n"
    "Do not add any extra explanation."
)


async def execute_tools(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    HARD EXECUTION NODE

    - Ignores any LLM tool_calls
    - Uses only state["intent"] and state["slots"]
    - Forces MCP execution
    - Forces a confirmation message
    """

    intent = state.get("intent")
    slots = state.get("slots") or {}

    # This node is only reached when the graph gate allows it
    # (see graph.py). Still keep a defensive guard.
    if intent != "add_expense":
        return state

    amount = slots.get("amount")
    category = slots.get("category")

    # Defensive guard (should never happen because of the gate)
    if amount is None or category is None:
        return state

    # ------------------ FORCE MCP EXECUTION ------------------

    result = await mcp_executor.execute(
        "add_expense",
        {
            "amount": amount,
            "category": category,
            "thread_id": state.get("thread_id"),
            "user_id": state.get("user_id"),
        },
    )

    # Keep results for observability / debugging
    state["tool_results"] = [
        {
            "tool": "add_expense",
            "result": result,
        }
    ]

    # ------------------ FORCE CONFIRMATION ------------------

    llm = await get_llm_client()

    confirmation_messages = [
        {"role": "system", "content": CONFIRMATION_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"amount={amount}, category={category}",
        },
    ]

    confirmation = await llm.ainvoke(confirmation_messages)

    content = getattr(confirmation, "content", None)

    if not content:
        content = f"Added ₹{amount} under {category}."

    state["final_reply"] = content

    return state


# ------------------------------------------------------------------
# BACKWARD-COMPATIBILITY STUB
# ------------------------------------------------------------------

async def resume_after_approval(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Resume execution after user approval.

    V1 behavior:
    - No approval flow implemented yet
    - Simply continue without executing tools again
    """
    return state

