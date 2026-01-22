from enum import Enum
from pydantic import BaseModel,Field

class LLMIntent(str,Enum):
    CHAT="chat"
    PLAN="plan"
    EXPLAIN="explain"
    RISK_CLASSIFICATION="risk_classification"
    SUMMARY="summary"

class LLMRequest(BaseModel):
    intent:LLMIntent
    user_input:str
    context:str | None=None

class LLMResponse(BaseModel):
    text:str
    confidence:float=Field(ge=0.0,le=1.0)

