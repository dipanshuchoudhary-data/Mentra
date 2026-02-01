from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

from backend.orchestrator.chat_engine import run_chat_turn
from backend.db.chat_models import ChatSessionRecord

router = APIRouter(prefix="/agent", tags=["agent"])


# ------------------ schemas ------------------

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    thread_id: Optional[str]


# ------------------ endpoint ------------------

@router.post("/chat", response_model=ChatResponse)
async def agent_chat(req: ChatRequest, request: Request):
    # -------------------------------------------------
    # Phase 2 – enforce trusted identity
    # -------------------------------------------------

    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # -------------------------------------------------

    try:
        result = await run_chat_turn(
            session_id=req.thread_id,
            user_input=req.message,
            user_id=user_id,   # <-- mandatory now
        )

        # ✅ HANDLE BOTH POSSIBLE RETURNS SAFELY
        if isinstance(result, dict):
            reply = result.get("reply", "")
            thread_id = result.get("thread_id")
        elif isinstance(result, ChatSessionRecord):
            reply = ""
            if result.messages:
                reply = result.messages[-1].content
            thread_id = result.session_id
        else:
            raise RuntimeError("Unexpected return type from chat engine")

        return ChatResponse(
            reply=reply,
            thread_id=thread_id,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
