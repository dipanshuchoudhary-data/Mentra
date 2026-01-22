import asyncio
from llm.client import OpenRouterLLMClient
from llm.models import LLMRequest, LLMIntent

async def test():
    llm = OpenRouterLLMClient()
    req = LLMRequest(
        intent=LLMIntent.PLAN,
        user_input="Scan system for large files"
    )
    async for chunk in llm.stream(req):
        print(chunk, end="")

asyncio.run(test())
