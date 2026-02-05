from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from pydantic import Field

class SupportTicket(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    order_id: str
    status: str =  "OPEN"
    created_at: datetime = datetime.utcnow()

    