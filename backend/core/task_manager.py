from typing import Dict, Any, List

from backend.orchestrator.graph import workflow


class TaskManager:
    """
    Runs the LangGraph workflow.
    Thin wrapper only.

    Phase-2:
    - user_id is mandatory
    - never allow workflow execution without identity
    """

    async def run(
        self,
        messages: List[dict],
        thread_id: str,
        user_id: str,
    ) -> Dict[str, Any]:

        if not user_id:
            raise RuntimeError("TaskManager.run called without user_id")

        state: Dict[str, Any] = {
            "messages": messages,
            "thread_id": thread_id,
            "user_id": user_id,
        }

        final_state = await workflow.ainvoke(state)
        return final_state
