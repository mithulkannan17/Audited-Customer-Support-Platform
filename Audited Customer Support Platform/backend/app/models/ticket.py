from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime


class SupportTicket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    order_id: str
    status: str = "OPEN"
    created_at: datetime = Field(default_factory=datetime.utcnow)
