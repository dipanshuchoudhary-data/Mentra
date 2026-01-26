import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from llm.client import OpenRouterLLMClient
from llm.models import LLMRequest, LLMIntent

router = APIRouter()
llm = OpenRouterLLMClient()


@router.get("/llm")
async def stream_llm(prompt: str):
    async def event_generator():
        req = LLMRequest(
            intent=LLMIntent.CHAT,
            user_input=prompt,
        )
        async for chunk in llm.stream(req):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
