from backend.core.permissions import RiskLevel

def classify_policy(text:str) -> RiskLevel:
    if "delete" in text.lower() or "remove" in text.lower():
        return RiskLevel.HIGH
    if "scan" in text.lower() or "read" in text.lower():
        return RiskLevel.MEDIUM
    return RiskLevel.LOW

