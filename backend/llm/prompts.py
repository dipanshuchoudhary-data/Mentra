from llm.models import LLMIntent


def build_prompt(intent: LLMIntent, user_input: str, context: str | None) -> str:
    system_rules = (
        "SYSTEM ROLE:\n"
        "You are a controlled reasoning engine operating inside a larger AI system.\n"
        "Your sole responsibility is to think, analyze, explain, or summarize.\n\n"

        "STRICT CONSTRAINTS:\n"
        "- Do NOT execute actions.\n"
        "- Do NOT suggest using tools, code, or external systems.\n"
        "- Do NOT assume real-world access.\n"
        "- Do NOT roleplay as an assistant.\n"
        "- Output only the reasoning result.\n\n"

        "QUALITY BAR:\n"
        "- Be precise, structured, and concise.\n"
        "- Avoid speculation.\n"
        "- Prefer explicit logic over verbosity.\n"
    )

    if intent == LLMIntent.PLAN:
        return (
            f"{system_rules}"
            "TASK TYPE: STRATEGIC PLANNING\n"
            "OBJECTIVE: Produce a high-level, step-by-step plan.\n"
            "SCOPE: Reasoning only. No execution details.\n\n"
            f"USER INPUT:\n{user_input}\n"
        )

    if intent == LLMIntent.RISK_CLASSIFICATION:
        return (
            f"{system_rules}"
            "TASK TYPE: RISK ASSESSMENT\n"
            "OBJECTIVE: Classify the request into exactly one category: LOW, MEDIUM, or HIGH.\n"
            "CRITERIA:\n"
            "- LOW: Benign, informational, or harmless.\n"
            "- MEDIUM: Ambiguous, dual-use, or potentially sensitive.\n"
            "- HIGH: Dangerous, illegal, or policy-restricted.\n\n"
            "OUTPUT FORMAT:\n"
            "Return only one word: LOW, MEDIUM, or HIGH.\n\n"
            f"USER INPUT:\n{user_input}\n"
        )

    if intent == LLMIntent.EXPLAIN:
        return (
            f"{system_rules}"
            "TASK TYPE: USER EXPLANATION\n"
            "OBJECTIVE: Explain the system’s behavior clearly to a non-technical user.\n"
            "STYLE: Simple language. No jargon. No internal system references.\n\n"
            f"CONTEXT:\n{context}\n"
        )

    if intent == LLMIntent.SUMMARY:
        return (
            f"{system_rules}"
            "TASK TYPE: EXECUTIVE SUMMARY\n"
            "OBJECTIVE: Summarize the outcome in a concise, neutral tone.\n"
            "STYLE: Factual. High signal. No analysis.\n\n"
            f"CONTEXT:\n{context}\n"
        )

    return (
        f"{system_rules}"
        "TASK TYPE: GENERAL REASONING\n"
        "OBJECTIVE: Provide a helpful, safe reasoning response.\n\n"
        f"USER INPUT:\n{user_input}\n"
    )
