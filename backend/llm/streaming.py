import asyncio
from collections.abc import AsyncGenerator

async def stream_text_chunks(text:str) -> AsyncGenerator[str,None]:
    """
    Token-agnostic streaming.
    Chunk-based to stay model-agnostic.
    """

    words = text.split()
    for word in word:
        yield word + " "
        await asyncio.sleep(0.03)