from core.policies import classify_policy
from core.permissions import RiskLevel

def assess_risk(message:str) -> RiskLevel:
    return classify_policy(message)