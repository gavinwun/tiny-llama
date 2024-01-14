from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str = Field(..., pattern='^(system|user|assistant)$')  # updated pattern
    content: str

class Messages(BaseModel):
    messages: list[Message]
    api_key: str