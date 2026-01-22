from typing import AsyncGenerator
from dotenv import load_dotenv
import os

from langchain_openai import ChatOpenAI

from llm.models import LLMRequest, LLMResponse
from llm.prompts import build_prompt

# Load environment variables once, here
load_dotenv()


class OpenRouterLLMClient:
    """
    SINGLE authorized entry point for all LLM calls.

    - Uses OpenRouter via langchain_openai
    - Reasoning-only
    - No tools, no files, no execution
    """

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY not set")

        self.llm = ChatOpenAI(
            model_name="mistralai/mistral-7b-instruct",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=api_key,
            temperature=0.3,
            streaming=True,
        )

    async def generate(self, req: LLMRequest) -> LLMResponse:
        """
        Non-streaming call.
        """
        messages = build_prompt(
            intent=req.intent,
            user_input=req.user_input,
            context=req.context,
        )

        result = await self.llm.ainvoke(messages)

        return LLMResponse(
            text=result.content,
            confidence=0.8,
        )

    async def stream(self, req: LLMRequest) -> AsyncGenerator[str, None]:
        """
        Streaming output, chunk-normalized.
        """
        messages = build_prompt(
            intent=req.intent,
            user_input=req.user_input,
            context=req.context,
        )

        async for chunk in self.llm.astream(messages):
            if chunk.content:
                yield chunk.content
