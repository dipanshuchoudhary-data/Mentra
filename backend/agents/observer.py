def explain_block(reason: str) -> str:
    """
    Human-readable explanation for blocked tasks.
    Used when state == BLOCKED.
    """
    return f"Action blocked: {reason}"