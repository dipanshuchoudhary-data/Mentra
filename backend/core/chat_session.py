from pydantic import BaseModel
from typing import List,Literal
from uuid import uuid4

class ChatMessage(BaseModel):
    role:Literal["user","assistant","tool"]
    content:str

class ChatSession(baseModel):
    session_id:str
    messages:List[ChatMessage]

    @classmethod
    def new(cls):
        return cls(session_id=str(uuid4()),messages=[])
    
    def add_user(self,text:str):
        self.messages.append(ChatMessage(role="user",content=text))

    def add_assistant(self,text:str):
        self.messages.append(ChatMessage(role="assistant",content=text))

    def add_tool(self,text:str):
        self.messages.append(ChatMessage(role="tool",content=text))