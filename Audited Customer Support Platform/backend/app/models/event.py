from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from uuid import uuid4


class ConversationEvent(BaseModel):
    id: str = str(uuid4())
    conversation_id: str
    event_type: str
    payload: Dict[str, Any]
    created_at: datetime = datetime.utcnow()
