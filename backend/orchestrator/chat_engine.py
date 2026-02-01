
from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional, Dict, Any, List

from backend.db.chat_store import ChatStore
from backend.db.chat_models import ChatSessionRecord, ChatMessage
from backend.core.task_manager import TaskManager

store = ChatStore()
task_manager = TaskManager()


async def run_chat_turn(
    session_id: Optional[str],
    user_input: str,
    user_id: str,
) -> Dict[str, Any]:
    """
    Chat engine.
    Executes the workflow once and returns the final reply.

    Phase-2:
    - user_id is mandatory
    - session ownership is enforced
    """

    # -------------------------------------------------
    # Phase 2 – hard enforcement
    # -------------------------------------------------

    if not user_id:
        raise RuntimeError("run_chat_turn called without user_id")

    # ------------------ load or create session ------------------

    if session_id:
        session = store.get_session(session_id)

        if not session:
            raise RuntimeError("Chat session not found")

        # Enforce ownership
        if session.user_id != user_id:
            raise RuntimeError("Unauthorized access to chat session")

    else:
        session = ChatSessionRecord(
            session_id=str(uuid4()),
            user_id=user_id,
            message="",
            messages=[],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        store.create_session(session)

    # ------------------ store user message ------------------

    user_msg = ChatMessage(
        role="user",
        content=user_input,
        timestamp=datetime.now(timezone.utc),
    )

    store.append_message(session.session_id, user_msg)

    # ------------------ reload session ------------------

    session = store.get_session(session.session_id)

    if not session:
        raise RuntimeError("Failed to reload chat session")

    # ------------------ build history ------------------

    messages: List[Dict[str, Any]] = [
        {"role": m["role"], "content": m["content"]}
        if isinstance(m, dict)
        else {"role": m.role, "content": m.content}
        for m in (session.messages or [])
    ]

    # ------------------ run workflow ------------------

    result = await task_manager.run(
        messages=messages,
        thread_id=session.session_id,
        user_id=user_id,
    )

    reply = result.get("final_reply") if isinstance(result, dict) else None

    if not reply and isinstance(result, dict):
        reply = result.get("llm_response")

    if not reply:
        reply = "I could not process that request."

    # ------------------ persist assistant reply ------------------

    assistant_msg = ChatMessage(
        role="assistant",
        content=reply,
        timestamp=datetime.now(timezone.utc),
    )

    store.append_message(session.session_id, assistant_msg)

    return {
        "reply": reply,
        "thread_id": session.session_id,
    }
