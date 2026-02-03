from backend.core.policies import classify_policy
from backend.core.permissions import RiskLevel

def assess_risk(message:str) -> RiskLevel:
    return classify_policy(message)