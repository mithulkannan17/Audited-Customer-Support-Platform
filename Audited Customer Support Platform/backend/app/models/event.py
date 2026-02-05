from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from uuid import uuid4
from pydantic import Field

class ConversationEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    conversation_id: str
    event_type: str
    payload: Dict[str, Any]
    created_at: datetime = datetime.utcnow()
