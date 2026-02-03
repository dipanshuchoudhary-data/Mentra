
from backend.core.permissions import RiskLevel

def assess_risk(user_message:str) -> RiskLevel:
    """
    Deterministic risk classification.
    LLM is NOT used here on purpose.
    """

    msg = user_message.lower()

    if any(k in msg for k in ("delete","remove","wipe","format")):
        return RiskLevel.HIGH
    
    if any(k in msg for k in ("scan","read","list","check")):
        return RiskLevel.MEDIUM
    
    return RiskLevel.LOW