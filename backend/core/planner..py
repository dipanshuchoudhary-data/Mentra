from llm.client import OpenRouterLLMClient
from llm.models import LLMRequest,LLMIntent

llm = OpenRouterLLMClient()

async def plan_task(message:str) -> str:
    req = LLMRequest(
        intent=LLMIntent.PLAN,
        user_input=message
    )
    resp = await llm.generate(req)
    return resp.text