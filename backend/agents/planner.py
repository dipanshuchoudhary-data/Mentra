from typing import Dict, Any
import json

from backend.llm.client import get_llm_client


EXTRACTION_SYSTEM_PROMPT = (
    "You are an information extraction engine.\n"
    "Extract intent and fields from the last user message.\n\n"
    "Return JSON ONLY. No text. No markdown.\n\n"
    "Schema:\n"
    "{\n"
    '  "intent": "add_expense" | "chat",\n'
    '  "amount": number | null,\n'
    '  "category": string | null\n'
    "}\n\n"
    "Rules:\n"
    "- Never execute anything.\n"
    "- Never describe what you will do.\n"
    "- If the message is normal conversation, set intent = chat.\n"
)


async def plan_task(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Planner (READ-ONLY):
    - Uses LLM only to extract intent and slots
    - NEVER decides execution
    - Handles missing-info clarification
    """

    messages = state.get("messages", [])

    extraction_messages = [
        {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
        *messages,
    ]

    llm = await get_llm_client()
    response = await llm.ainvoke(extraction_messages)

    raw = getattr(response, "content", None)

    # Default safe output
    extracted = {
        "intent": "chat",
        "amount": None,
        "category": None,
    }

    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                extracted["intent"] = parsed.get("intent", "chat")
                extracted["amount"] = parsed.get("amount", None)
                extracted["category"] = parsed.get("category", None)
        except Exception:
            pass

    # Hand off structured data
    state["intent"] = extracted["intent"]
    state["slots"] = {
        "amount": extracted["amount"],
        "category": extracted["category"],
    }

    # Planner never emits tool calls
    state["tool_calls"] = []

    # Do not expose extraction JSON as chat output
    state["llm_response"] = None

    # Missing-info clarification (normal chat, no MCP)
    if extracted["intent"] == "add_expense":
        if extracted["amount"] is None:
            state["final_reply"] = "Please tell me the amount."
        elif extracted["category"] is None:
            state["final_reply"] = "Please tell me the category."

    return state
