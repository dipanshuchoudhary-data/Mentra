from enum import Enum

class UserIntent(str,Enum):
    CHAT="chat"
    ACTION="action"
    QUESTION="question"

def classify_intent(text:str) -> UserIntent:
    text = text.lower()
    if any(k in text for k in ("delete","scan","run","execute")):
        return UserIntent.ACTION
    
    if text.endswith("?"):
        return UserIntent.QUESTION
    
    return UserIntent.CHAT