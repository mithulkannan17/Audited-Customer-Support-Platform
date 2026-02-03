from pydantic import BaseModel
from typing import List
from uuid import uuid4

class OrderItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    id: str = str(uuid4())
    customer_id: str
    items: List[OrderItem]
    status: str 