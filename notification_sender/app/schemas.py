from enum import Enum
from pydantic import BaseModel

class MessageType(str, Enum):
    CHAT = "CHAT"
    EMAIL = "EMAIL"

class Message(BaseModel):
    message_type: MessageType
    message_text: str
