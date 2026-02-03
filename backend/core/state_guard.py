from backend.core.states import TaskState

ALLOWED_TRANSITIONS = {
    TaskState.CREATED: {TaskState.PLANNING},
    TaskState.PLANNING: {TaskState.AWAITING_APPROVAL,TaskState.COMPLETED},
    TaskState.AWAITING_APPROVAL:{TaskState.EXECUTING,TaskState.BLOCKED},
    TaskState.EXECUTING: {TaskState.VERIFYING},
    TaskState.VERIFYING:{TaskState.COMPLETED,TaskState.FAILED},
}

def assert_transition(current:TaskState,next_state:TaskState):
    allowed = ALLOWED_TRANSITIONS.get(current,set())
    if next_state not in allowed:
        raise RuntimeError(f"Illegal state transition: {current} -> {next_state}")