from pydantic import BaseModel
from typing import List
from uuid import uuid4
from pydantic import Field

class OrderItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    customer_id: str
    items: List[OrderItem]
    status: str 