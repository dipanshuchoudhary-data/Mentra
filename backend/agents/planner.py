from llm.client import OpenRouterLLMClient
from llm.models import LLMRequest,LLMIntent

_llm = OpenRouterLLMClient()

async def plan_task(user_message:str) -> str:
    """
    Generate a high-level, non-executable plan.
    Used only during PLANNING state.
    """
    req = LLMRequest(
        intent = LLMIntent.PLAN,
        user_input=user_message,
    )

    resp = await _llm.generate(req)
    return resp.text