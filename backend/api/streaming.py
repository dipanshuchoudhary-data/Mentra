import asyncio
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from llm.client import MockLLMClient

router = APIRouter()
llm = MockLLMClient()

@router.get("/llm")
async def stream_llm(prompt: str):

    async def event_generator():
        async for chunk in llm.stream_text(prompt):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.05)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
