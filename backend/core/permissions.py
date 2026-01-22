from enum import Enum

class RiskLevel(str,Enum):
    LOW="LOW"
    MEDIUM="MEDIUM"
    HIGH="HIGH"

def requires_approval(risk:RiskLevel) -> bool:
    return risk in {RiskLevel.MEDIUM,RiskLevel.HIGH}

