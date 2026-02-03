from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.orchestrator.chat_engine import run_chat_turn
from backend.db.chat_store import ChatStore

router = APIRouter()
store = ChatStore()


class ChatInput(BaseModel):
    session_id: str | None = None
    message: str
    user_id: str | None = None


@router.post("/chat")
async def chat(inp: ChatInput):
    session = await run_chat_turn(
        session_id=inp.session_id,
        user_input=inp.message,
        user_id=inp.user_id,
    )
    return session.model_dump()


@router.get("/chat/{session_id}")
def get_chat(session_id: str):
    try:
        session = store.get_session(session_id)
        return session.model_dump()
    except KeyError:
        raise HTTPException(status_code=404, detail="Chat not found")


@router.get("/chats")
def list_chats(user_id: str | None = None):
    sessions = store.list_sessions(user_id)
    return [s.model_dump() for s in sessions]
